import pytest

from lotr import DATASET_LOCATION
from lotr.preprocessing import preprocess_folder


# Code for making the data preprocessing optional
def pytest_addoption(parser):
    parser.addoption(
        "--preprocess",
        action="store_true",
        default=False,
        help="force data preprocessing",
    )


@pytest.fixture(scope="session", autouse=True)
def sample_path(pytestconfig):
    # Will be executed before the first test
    path = DATASET_LOCATION / "210314_f1" / "210314_f1_natmov"

    if (
        pytestconfig.getoption("preprocess")
        or not (path / "filtered_traces.h5").exists()
    ):
        preprocess_folder(
            path,
            recompute_bout_df=True,
            recompute_filtering=True,
            recompute_regressors=True,
        )

    yield path
