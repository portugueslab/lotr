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
