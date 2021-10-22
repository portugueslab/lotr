__version__ = "0.1.0"
__author__ = "Luigi Petrucco @ portugueslab"

from pathlib import Path

from lotr.experiment_class import LotrExperiment
from lotr.file_utils import get_dataset_location, get_figures_location

DATASET_LOCATION = get_dataset_location()
FIGURES_LOCATION = get_figures_location()

A_FISH = DATASET_LOCATION / "210314_f1" / "210314_f1_natmov"

dataset_folders = sorted([
    f.parent for f in DATASET_LOCATION.glob("*[0-9]_f[0-9]*/*/selected.h5")
])
