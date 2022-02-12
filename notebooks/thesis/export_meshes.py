from pathlib import Path

import flammkuchen as fl
from tqdm import tqdm

data_folder = Path(
    "/Users/luigipetrucco/Google Drive/data/all_source_data/anatomy/annotated_traced_neurons"
)
neurons_dict = fl.load(data_folder / "all_skeletons.h5")


for s in [1, 2]:
    mesh_folder = data_folder.parent / f"ipn_ref_meshes_s{s}"
    mesh_folder.mkdir(exist_ok=True)

    for cid, neuron in tqdm(list(neurons_dict.items())):
        #if (cid[0] == "p") & (int(cid[1:]) < 41):
        coords = neuron.get_coords("ipn").copy()
        mesh = neuron.generate_mesh(
            space="ipn", soma_radius=2.0, dendrite_radius=0.1*s, axon_radius=0.1*s
        )

        file = mesh.export(str(mesh_folder / f"mesh_{neuron.id}.obj"))
