__version__ = "0.1.0"
__author__ = "Luigi Petrucco @ portugueslab"

from lotr.experiment_class import LotrExperiment
from lotr.file_utils import retrieve_dataset_location

DATASET_LOCATION = retrieve_dataset_location()

AN_EXP = DATASET_LOCATION / "210314_f1" / "210314_f1_natmov"