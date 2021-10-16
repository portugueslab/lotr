import numpy as np
import pytest

from lotr import LotrExperiment


@pytest.mark.parametrize(
    "attrib, res", [("fn", 5), ("n_pts", 9900), ("n_rois", 804), ("has_hdn", True)]
)
def test_dataclass_attribs(attrib, res, sample_path):
    exp = LotrExperiment(sample_path)
    assert getattr(exp, attrib) == res


@pytest.mark.parametrize(
    "attrib, res",
    [
        ("traces", 4.2231445),
        ("raw_traces", 104504930.0),
        ("rois_stack", 29304664),
        ("anatomy_stack", 6460928.294495098),
    ],
)
def test_dataclass_array_sums(attrib, res, sample_path):
    exp = LotrExperiment(sample_path)
    assert np.allclose(getattr(exp, attrib).sum(), res)


def test_dataclass_array_anatomy_orientation(sample_path):
    exp = LotrExperiment(sample_path)
    assert np.allclose(exp.plane_ext_um, [0, 177.6, 0, 207.6])
    assert np.allclose(
        exp.anatomy_stack[::4, ::200, ::100],
        [
            [
                [6.3433976, 7.44532549, 8.19880623],
                [7.60578331, 45.48479688, 43.55887663],
            ],
            [
                [10.43550563, 5.36229308, 5.97700588],
                [4.85311289, 12.84962144, 61.30005133],
            ],
        ],
    )
    assert np.allclose(
        exp.rois_stack[::4, ::200, ::100],
        [[[-1, -1, -1], [-1, 57, 53]], [[-1, -1, -1], [-1, 393, 338]]],
    )
