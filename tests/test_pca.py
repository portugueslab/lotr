import pytest
import numpy as np

from lotr import LotrExperiment
from lotr.pca import pca_and_phase


def test_pca_circlefit(sample_path):
    exp = LotrExperiment(sample_path)

    traces = exp.traces[exp.pca_t_slice, exp.hdn_indexes]
    pcaed, phase, _, circle_params = pca_and_phase(traces.T)

    assert np.allclose(pcaed[::50, :2], np.array([[-78.25784, 26.407043],
                                           [-71.45805, 35.18204]]))
    assert np.allclose(phase[::40], np.array([2.9465494, -1.0761138, -1.7919015]))
    assert np.allclose(circle_params, (
    5.229488856660475, 9.91372009897165, 80.72722284980495, 8.968477126020188))