import numpy as np
from circle_fit import hyper_fit
from scipy.optimize import curve_fit
from sklearn.decomposition import PCA
from tqdm import tqdm

from lotr.behavior import get_fictive_trajectory
from lotr.utils import linear_regression


def fictive_trajectory_and_fit(phase_unwrapped, bouts_df, fn=5, min_bias=0.05):
    if "idx_imaging" not in bouts_df.columns:
        bouts_df["idx_imaging"] = np.round(bouts_df["t_start"]).astype(np.int) * fn

    fictive_trajectory = get_fictive_trajectory(
        len(phase_unwrapped), bouts_df, min_bias=min_bias
    )

    params = linear_regression(phase_unwrapped, fictive_trajectory)

    return fictive_trajectory, params


def pca_and_phase(traces_fit, traces_transform=None, comp0=0, comp1=1):
    """Compute PCA and fit circle and phase to first
    two components.
    """
    if traces_transform is None:
        traces_transform = traces_fit

    # Compute PCA and transform traces:
    pca = PCA(n_components=5).fit(traces_fit)
    pcaed = pca.transform(traces_transform)

    # Fit circle:
    hf_c = hyper_fit(pcaed[:, [comp0, comp1]])

    # Compute phase, after subtracting center of the circle
    phase = np.angle((pcaed[:, 0] - hf_c[0]) + 1j * (pcaed[:, 1] - hf_c[1]))

    return pcaed, phase


def phase_from_fit(x, y):
    """Fit a phase to a sinusoidal cosyne oscillation.
    Phase will be the only parameter we'll optimize on,
    so before, normalize y to loosely fit the range (-1, 1).
    """

    def _cos_fit(x, ph):
        return np.cos(x + ph)

    # Normalize y to fit between -1 and 1:
    y = y - np.percentile(y, 5)
    y = y / np.percentile(y, 99)
    y = y * 2 - 1

    # Fit the trace:
    popt, pcov = curve_fit(_cos_fit, x, y, p0=[0])
    return popt[0], pcov


def fit_phase_neurons(traces, phase):
    """Fit a phase to neurons's activity."""
    n_cells = traces.shape[1]
    cell_phases = np.full(n_cells, np.nan)
    covs = np.full(n_cells, np.nan)

    for i in tqdm(range(traces.shape[1])):
        try:
            ph, c = phase_from_fit(phase, traces[:, i])
            phase[i] = ph
            covs[i] = c[0][0]
        except RuntimeError:
            pass

    return cell_phases, covs
