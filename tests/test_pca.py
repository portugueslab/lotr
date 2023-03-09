import numpy as np

from lotr import LotrExperiment
from lotr.pca import pca_and_phase

np.random.seed(34224)


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
    print(circle_params)
    assert np.allclose(
        phase[::40], np.array([3.1373436, 2.1166425, 2.2496562]), rtol=1e-03
    )
    assert np.allclose(
        circle_params[2:],
        (79.07544827739056, 12.745134),
        rtol=1e-03,
    )
