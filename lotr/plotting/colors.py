"""Coloring code adapted from Vilim's notebook_utilities.stack_coloring
and motions.color.
"""

import colorspacious
import numpy as np


def dark_col(col, val=0.2):
    return [max(0, c - val) for c in col]


def _jch_to_rgb255(x):
    output = np.clip(colorspacious.cspace_convert(x, "JCh", "sRGB1"), 0, 1)
    return (output * 255).astype(np.uint8)


def _get_n_colors(n_cols, lum=60, sat=60, hshift=0):
    return _jch_to_rgb255(
        np.stack(
            [
                np.full(n_cols, lum),
                np.full(n_cols, sat),
                (-np.arange(0, 360, 360 / n_cols) + hshift),
            ],
            1,
        )
    )
