import numpy as np

# Old, manually found matrix:
em_2_mpinref = np.array(
    [
        [0.0005112, -0.0139081, -0.00390891, 468.00440331],
        [-0.00759618, -0.00207066, 0.02082109, 512.81161961],
        [-0.01246794, 0.00332361, -0.01054555, 593.08389005],
        [0.0, 0.0, 0.0, 1.0],
    ]
)

# New matrix to IPN reference:
th = -3 * (np.pi / 2) / 90  # rotation on the horizontal plane
th2 = -3 * (np.pi / 2) / 90  # rotation on the frontal plane

em_2_ipnref = (
    np.array([[1, 0, 0, 0], [0, 1, 0, 60], [0, 0, 1, 50], [0, 0, 0, 1]])
    @ np.array([[0.98, 0, 0, 5], [0, 0.98, 0, 4], [0, 0, 0.98, -5], [0, 0, 0, 1]])
    @ np.array(
        [
            [np.cos(th), 0, np.sin(th), 0],
            [0, 1, 0, 0],
            [-np.sin(th), 0, np.cos(th), 0],
            [0, 0, 0, 1],
        ]
    )
    @ np.array(
        [
            [1, 0, 0, 0],
            [0, np.cos(th2), np.sin(th2), 0],
            [0, -np.sin(th2), np.cos(th2), 0],
            [0, 0, 0, 1],
        ]
    )
    @ np.array(
        [
            [-9.46313412e-03, 1.36792080e-03, 2.21543909e-02, 4.79759830e01],
            [-3.03246252e-04, 2.08645843e-02, 3.69292093e-03, -4.12226845e02],
            [-1.41111857e-02, 2.02899284e-03, -1.31987230e-02, 4.59158298e02],
            [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
        ]
    )
)


def trasform_pts(pts, mat):
    """Transform array of points using a 4x4 transformation matrix,
    adding 1 column for the offset.
    """

    pts = np.array(pts)
    if len(pts.shape) == 1:
        pts = pts[np.newaxis, :]
    pts = np.insert(pts, pts.shape[1], np.ones(pts.shape[0]), axis=1)
    return (mat @ pts.T).T[:, :3]


def em2mpinref(pts):
    return trasform_pts(pts, em_2_mpinref)


def em2ipnref(pts):
    return trasform_pts(pts, em_2_ipnref)
