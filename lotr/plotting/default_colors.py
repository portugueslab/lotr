import numpy as np
from matplotlib.colors import ListedColormap

from lotr.plotting.color_utils import _get_continuous_colors, get_n_colors

COLS = dict(
    sides=dict(lf=(0.0, 0.623, 0.886), rt=(0.835, 0.364, 0.282)),
    dff_img="Greens",
    dff_plots="gray",
    time="viridis",
    beh=(0.4,) * 3,
    ring=(0.847, 0.102, 0.376),
    phase=ListedColormap(get_n_colors(1000, lum=45, sat=70, hshift=90) / 255),
    phase_light=ListedColormap(get_n_colors(1000, lum=60, sat=45, hshift=90) / 255),
    dff_opp="PiYG",
)


def get_default_phase_col(phase):
    return _get_continuous_colors([phase], COLS["phase"], vlims=(-np.pi, np.pi)) / 255
