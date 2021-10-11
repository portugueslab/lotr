import pytest

from lotr import DATASET_LOCATION
from lotr.preprocessing import preprocess_folder


@pytest.fixture(scope="session", autouse=True)
def sample_path():
    # Will be executed before the first test
    path = DATASET_LOCATION / "210314_f1" / "210314_f1_natmov"
    preprocess_folder(
        path,
        recompute_bout_df=True,
        recompute_filtering=True,
        recompute_regressors=True,
    )

    yield path
