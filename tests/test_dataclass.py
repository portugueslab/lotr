import pytest
from lotr import LotrExperiment


@pytest.mark.parametrize("attrib, res",
                         [("fn", 5),
                         ("n_pts", 9900),
                          ("n_rois", 804),
                          ("has_hdn", True)])
def test_dataclass_attribs(attrib, res, sample_path):
    exp = LotrExperiment(sample_path)
    assert getattr(exp, attrib) == res
