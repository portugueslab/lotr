"""For a discussion over the anatomical space convention, look in the LotrExperiment
class docstring"""

import numpy as np
from bg_space import AnatomicalSpace

from lotr.default_vals import (
    ANATOMICAL_ORIENT_FIGURES,
    ANATOMICAL_ORIENT_SOURCE,
)

source_space = AnatomicalSpace(ANATOMICAL_ORIENT_SOURCE)


def anatomical_angle_remapping(angle):
    """Remap the angle range so that angle 0 starts at 45 degrees
    and angle 360 appears at 135 - for remapping anatomy avoiding midline.
    """
    out = angle.copy()
    out[np.abs(out) < np.pi / 4] = 0
    out = (out - np.sign(out) * np.pi / 4) * 2
    out[np.abs(out) > np.pi] = np.sign(out[np.abs(out) > np.pi]) * np.pi
    return out

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
