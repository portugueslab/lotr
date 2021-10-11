import pytest

from lotr import DATASET_LOCATION


@pytest.fixture(scope="session", autouse=True)
def sample_path():
    # Will be executed before the first test
    yield DATASET_LOCATION / "210314_f1" / "210314_f1_natmov"
