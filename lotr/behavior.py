import numpy as np
from lotr.default_vals import TURN_BIAS, GCAMP_TAU
import pandas as pd
from itertools import product


def get_bouts_props_array(n_pts, bouts_df, min_bias=0.05,
                           selection="all", value="bias"):
    """From a dataframe of bouts compute an array of some given number of timepoints
    containing info on bouts (generally bias or amplitude). Convenient for regressors
    creation and fictive heading computation

    Parameters
    ----------
    n_pts : int
        number of imaging timepoints (len of output)
    bouts_df : pd.DataFrame
        bouts dataframe
    min_bias : float
        Minimum value on the given parameter for the bout to be included
    selection : str
        Selection for bout direction, can be "left", "right", "forward", "all"
    value : str or number
        Can be "bias" (for array of biases), "amp" (for bout vigor amplitude), or
        any other column of the bouts dataframe, or, if a number, the value that will be
        inserted in the array.

    Returns
    -------
    numpy array
        Array of biases over time

    """

    bout_dir_selections = dict(left=bouts_df["bias"] < -TURN_BIAS,
                               right=bouts_df["bias"] > TURN_BIAS,
                               forward=(bouts_df["bias"] < TURN_BIAS) & (
                                           bouts_df["bias"] > -TURN_BIAS),
                               all=~np.isnan(bouts_df["bias"]))

    bout_props_array = np.zeros(n_pts)  # initialize theta turns array

    bout_selection = bout_dir_selections[selection] & (
                np.abs(bouts_df["bias"]) > min_bias)

    # For every bout, set its choosen value as the value in the theta_turns array
    # in correspondence of the bout time:
    if value in bouts_df.columns:
        bout_props_array[bouts_df.loc[bout_selection, "idx_imaging"]] = \
            bouts_df.loc[bout_selection, value]
    else:
        bout_props_array[bouts_df.loc[bout_selection, "idx_imaging"]] = value

    return bout_props_array


def get_fictive_trajectory(n_pts, bouts_df, min_bias=0.05):
    """
    Parameters
    ----------
    n_pts : int
        number of imaging timepoints (len of output)
    bouts_df : pd.DataFrame
        bouts dataframe
    min_bias : float
        Minimum bias for the bout to be included

    Returns
    -------
    numpy array
        Array of fictive heading over time

    """
    theta_turned = get_bouts_props_array(n_pts, bouts_df, min_bias=min_bias,
                                        selection="all", value="bias")
    # Calculate fictive theta as cumulative sum of theta_turns
    return np.cumsum(theta_turned)


def create_motor_regressors(n_pts, df, fn, min_bias=0.05):
    N_KERNEL_PTS = 1000

    regressors_dict = dict()

    for d, v in product(["left", "right", "forward", "all"],
                        ["bias", "med_vig", 1]):
        if d == "forward" and v == "bias":
            continue

        if d == "forward" or d == "all":
            min_bias = 0
        else:
            min_bias = min_bias

        arr = get_bouts_props_array(n_pts, df, min_bias=min_bias,
                                    selection=d, value=v)

        if v == "bias" and d == "all":
            regressors_dict.update({f"{d}_{v}_abs": np.abs(arr)})
        elif d in ["left", "right"]:
            arr = np.abs(arr)

        regressors_dict.update({f"{d}_{v}": arr})

    tau_fs = GCAMP_TAU * fn
    kernel = np.exp(-np.arange(N_KERNEL_PTS) / tau_fs)

    for k, val in regressors_dict.items():
        regressors_dict[k] = np.convolve(val, kernel)[:n_pts]
    return pd.DataFrame(regressors_dict)
