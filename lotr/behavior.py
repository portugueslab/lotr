import numpy as np


def get_fictive_trajectory(n_pts, bouts_df, min_bias=0.05):
    theta_turns = np.zeros(n_pts)  # initialize theta turns array

    # For every bout, set its bias as the value in the theta_turns array
    # in correspondence of the bout time:
    for i in bouts_df.index:
        if np.abs(bouts_df.loc[i, "bias"]) > min_bias:
            theta_turns[bouts_df.loc[i, "idx_imaging"]] = bouts_df.loc[
                i, "bias"
            ]  # * coef

    # Calculate fictive theta as cumulative sum of theta_turns
    return np.cumsum(theta_turns)
