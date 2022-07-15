from pathlib import Path

import flammkuchen as fl
import navis

data_path = Path(
    "/Users/luigipetrucco/Google Drive/data/all_source_data/anatomy/swc_neurons/swc_ipnspace_flip"
)

neurons = []
for i in data_path.glob("*.swc"):
    print(i)
    try:
        neurons.append(navis.read_swc(i))
    except ValueError:
        print("valueerror")

nlist = navis.NeuronList(neurons)

dps = navis.make_dotprops(nlist, k=5, resample=False, parallel=False)
nbl = navis.nblast(dps, dps, progress=True, n_cores=1)

fl.save(
    data_path / "distance_matrix.h5",
    dict(matrix=nbl.values, ids=[n.name for n in neurons]),
)
