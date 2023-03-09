import flammkuchen as fl
from tqdm import tqdm

from lotr import DATASET_LOCATION
from lotr.em.loading import load_skeletons_dict_from_zip

data_folder = DATASET_LOCATION / "anatomy" / "annotated_traced_neurons"

files = list([f for f in data_folder.glob("*.zip") if "synapses" not in f.name])

# Make sure we don't have spurious annotations
assert len(files) == 6
remake = True

neurons_dict = dict()
for f in tqdm(files):
    neurons_dict.update(load_skeletons_dict_from_zip(f))

fl.save(data_folder / "all_skeletons.h5", neurons_dict)
