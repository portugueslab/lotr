import numpy as np
from circle_fit import hyper_fit
from scipy.optimize import curve_fit, quadratic_assignment
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
    phase = np.angle((pcaed[:, comp0] - hf_c[0]) + 1j * (pcaed[:, comp1] - hf_c[1]))

    return pcaed, phase, pca, hf_c


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


def fit_phase_neurons(traces, phase, disable_bar=False):
    """Fit a phase to neurons's activity."""
    n_cells = traces.shape[1]
    cell_phases = np.full(n_cells, np.nan)
    covs = np.full(n_cells, np.nan)

    for i in tqdm(range(traces.shape[1]), disable=disable_bar):
        if not (traces[:, i] == 0).all():
            try:
                ph, c = phase_from_fit(phase, traces[:, i])
                if ph > np.pi:
                    ph = ph - 2 * np.pi
                if ph < -np.pi:
                    ph = ph + 2 * np.pi

                cell_phases[i] = ph
                covs[i] = c[0][0]
            except RuntimeError:
                pass

    return cell_phases, covs


def qap_sorting_and_phase(traces, t_lims=None):
    n_pts, n = traces.shape

    if t_lims is None:
        t_lims = (0, n_pts)

    distance = np.corrcoef(traces[t_lims[0] : t_lims[1], :].T)

    flow = np.zeros((n, n))
    toshift = np.cos(np.linspace(-np.pi, np.pi, n))
    for i in range(n):
        flow[i, :] = np.roll(toshift, i)

    options = {"P0": "randomized"}
    res = min(
        [
            quadratic_assignment(flow, distance, method="faq", options=options)
            for i in range(1000)
        ],
        key=lambda x: x.fun,
    )

    options = {"partial_guess": np.array([np.arange(n), res.col_ind]).T}
    res = quadratic_assignment(flow, distance, method="2opt", options=options)

    perm = res["col_ind"]

    traces_sorted = traces[:, perm]

    base = np.linspace(0, 2 * np.pi, traces_sorted.shape[1])
    com_phase = np.arctan2(
        np.sum(np.sin(base) * traces_sorted, 1), np.sum(np.cos(base) * traces_sorted, 1)
    )

    return perm, com_phase
