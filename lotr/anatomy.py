import numpy as np
from bg_space import AnatomicalSpace

from lotr.default_vals import ANATOMICAL_ORIENT_SOURCE, ANATOMICAL_ORIENT_FIGURES

source_space = AnatomicalSpace(ANATOMICAL_ORIENT_SOURCE)


def reshape_stack(suite2p_stack):
    """Ensure that a suite2p stack is oriented according to the convention
    (ventr-dors, rostr-caud, left-right)
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
    target_space = AnatomicalSpace(ANATOMICAL_ORIENT_FIGURES)

    return source_space.map_stack_to(target_space, suite2p_stack)