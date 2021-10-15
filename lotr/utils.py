import numpy as np
from scipy.interpolate import interp1d
from numba import njit


def zscore(array):
    """Nan zscoring function."""
    return (array - np.nanmean(array)) / np.nanstd(array)


def interpolate(source_x, source_y, target_x):
    return interp1d(source_x, source_y, fill_value="extrapolate")(target_x)


def pearson_regressors(traces, regressors):
    """Gives the pearson correlation coefficient. Adapted from Vilim's functions.

    :param traces: the traces, with time in rows
    :param regressors: the regressors, with time in rows
    :return: the pearson correlation coefficient

    Parameters
    ----------
    traces : np.array
        (t, n_rois) array with the traces.
    regressors : np.array
        (t, n_regressors) array with the regressors.

    Returns
    -------
    np.array
        (n_regressors, n_rois) matrix of regressors.

    """
    # two versions, depending whether there is one or multiple regressors
    X = traces
    Y = regressors
    if len(Y.shape) == 1:
        numerator = np.dot(X.T, Y) - X.shape[0] * np.nanmean(X, 0) * np.nanmean(Y)
        denominator = (X.shape[0] - 1) * np.nanstd(X, 0) * np.nanstd(Y)
        result = numerator / denominator
    else:
        numerator = np.dot(X.T, Y) - X.shape[0] * np.outer(
            np.nanmean(X, 0), np.nanmean(Y, 0)
        )
        denominator = (X.shape[0] - 1) * np.outer(np.nanstd(X, 0), np.nanstd(Y, 0))
        result = (numerator / denominator).T

    return result


def linear_regression(X, Y):
    """Get slope and intercept of linear regression between two vectors."""
    X_mat = np.vstack((np.ones(len(X)), X)).T
    return np.linalg.inv(X_mat.T.dot(X_mat)).dot(X_mat.T).dot(Y)


def reduce_to_pi(angle):
    """Puts an angle or array of angles inside the (-pi, pi) range"""
    return np.mod(angle + np.pi, 2 * np.pi) - np.pi


def get_rot_matrix(th):
    return np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])


def get_vect_angle(vect):
    return np.angle(vect[0] + 1j * vect[1])


@njit
def roll_columns_jit(matrix, shifts):
    """Shift every column of the matrix by a specified amount.

    Parameters
    ----------
    matrix : np.array
        (to_roll, n) matrix to roll over the first dimension.
    shifts : np.array
        (to_roll,) array of integer indexes specifying the shift.

    Returns
    -------
    np.array
        matrix shifted over first dimension.

    """
    rolled = np.empty_like(matrix)
    for i in range(matrix.shape[0]):
        rolled[i, :] = np.roll(matrix[i, :], int(shifts[i]))
    return rolled
