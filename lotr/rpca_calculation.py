import numpy as np

from lotr.utils import get_rot_matrix, get_vect_angle, reduce_to_pi


# TODO This will change with registered coordinates
def get_normalized_coords(coords):
    """ Normalize coords to be used as weights for fit

    Parameters
    ----------
    coords : np.array
        (n_rois, 3) matrix with the roi coordinates.

    Returns
    -------
    np.array
        (n_rois, 3) matrix with the normalized coordinates to be used as weights.


    """

    # For PCA registration, convert coords to have mean 0 anb be used as weights.
    # Use percentiles along every axis to normalize them for removing outliers.
    w_coords = coords - np.percentile(coords, 2, axis=0)
    w_coords[w_coords < 0] = 0

    for i in range(coords.shape[1]):
        thr = np.percentile(coords[:, i], 98)
        coords[coords[:, i] > thr, i] = thr

    w_coords = w_coords / np.sum(w_coords, 0)
    w_coords = w_coords - np.mean(w_coords, 0)

    return w_coords


def reorient_pcs(cpc_loads, w_coords):
    """ Reorient centered principal components (over time) so that the position of
    cells in the PC space matches their anatomical location.

    Parameters
    ----------
    cpc_loads : np.array
        (n_rois, 2) matrix with projection of cells over centered
        principal components.
    w_coords : np.array
        (n_rois, 3) matrix with the coordinates to be used as weights
        (already normalized).

    Returns
    -------
    np.array
        (n_rois, 2) matrix with projection of cells over rotated
        principal components.
    """
    FINAL_TH_SHIFT = 3 * np.pi / 4  # arbitrary final rotation for plotting purposes

    # We compute the PCs vector averages across the population using coordinates along
    # each anatomical axis as weights.
    # The result is a 3 x 2 matrix containing the average vector for each of the
    # 3 anatomical axes used as weights
    avg_vects = np.einsum("ij,ik->jk", cpc_loads, w_coords)

    # We then compute average angle for all axes:
    avg_angles = get_vect_angle(avg_vects)
    # and we take the mean between left-right and front-caud axes angles:
    mean_angle = np.angle(
        np.sum(np.cos(avg_angles[1:])) + 1j * np.sum(np.sin(avg_angles[1:]))
    )

    # Since PC signs can be arbitrary, we need to find whether left and right
    # were flipped. This we decide based on the difference in sign from the angle
    # between the lateral and sagittal axes fit in PC space:
    s = -np.sign(reduce_to_pi(avg_angles[2] - avg_angles[1]))
    invert_mat = np.array([[1, 0], [0, s]])

    # Finally, we combine all transformation. The last rotation is an arbitrary
    # one so that the most rostral ROIs are in the upper part of the plot:
    rpc_loads = (
            get_rot_matrix(FINAL_TH_SHIFT)
            @ invert_mat
            @ get_rot_matrix(-mean_angle)
            @ cpc_loads.T
    ).T

    return rpc_loads
