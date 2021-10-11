import numpy as np


def reshape_stack(suite2p_stack):
    """Ensure that a suite2p stack is oriented according to the convention
    (dors-ventr, rostr-caud, )
    top=rostral, left=left throughout the figures. Change here if changes
    are done to the suite2p files. Ideally, it will return unchanged stack after
    dataset is cleaned.

    Parameters
    ----------
    suite2p_tack : np.array
        Stack saved in the suite2p exported data

    Returns
    -------
    np.array
        The reformatted array

    """
    return suite2p_stack