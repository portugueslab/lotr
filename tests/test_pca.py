import pytest
import numpy as np

from lotr import LotrExperiment
from lotr.pca import pca_and_phase


def test_pca_circlefit(sample_path):
    exp = LotrExperiment(sample_path)

    traces = exp.traces[exp.pca_t_slice, exp.hdn_indexes]
    pcaed, phase, _, circle_params = pca_and_phase(traces.T)

    assert np.allclose(
        pcaed[::50, :2],
        np.array(
            [[-62.054733, 0.26362327], [44.070858, -75.87029], [20.567976, -80.72353]]
        ),
        rtol=1e-03,
    )
    assert np.allclose(
        phase[::40], np.array([-3.0476563, 2.2991502, 2.4215913]), rtol=1e-03
    )
    assert np.allclose(
        circle_params,
        (13.556059713029029, 7.387183396771005, 80.56838978387617, 8.825162297678249),
        rtol=1e-03,
    )
