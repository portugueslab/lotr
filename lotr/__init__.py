__version__ = "0.1.0"
__author__ = "Luigi Petrucco @ portugueslab"

from lotr.experiment_class import LotrExperiment
from lotr.file_utils import retrieve_dataset_location, retrieve_figures_location

DATASET_LOCATION = retrieve_dataset_location()
FIGURES_LOCATION = retrieve_figures_location()

A_FISH = DATASET_LOCATION / "210314_f1" / "210314_f1_natmov"
