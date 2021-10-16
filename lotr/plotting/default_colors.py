import numpy as np
from matplotlib.colors import ListedColormap

from lotr.plotting.color_utils import get_continuous_colors, get_n_colors

COLS = dict(
    sides=dict(lf=(0.0, 0.623, 0.886), rt=(0.835, 0.364, 0.282), fw=".5"),
    dff_img="Greens",
    dff_plot="gray",
    time="viridis",
    beh=(0.4,) * 3,
    ring=(0.847, 0.102, 0.376),
    shuf=".7",
    phase=ListedColormap(get_n_colors(1000, lum=45, sat=70, hshift=90) / 255),
    phase_light=ListedColormap(get_n_colors(1000, lum=60, sat=45, hshift=90) / 255),
    dff_opp="PiYG",
    ph_plot=[0.702, 0.129, 0.0470],
)


def get_default_phase_col(phase):
    (col,) = get_continuous_colors([phase], COLS["phase"], vlims=(-np.pi, np.pi)) / 255
    return col
