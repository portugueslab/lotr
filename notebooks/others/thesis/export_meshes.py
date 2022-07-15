from pathlib import Path

import flammkuchen as fl
from tqdm import tqdm

data_folder = Path("/Volumes/Shared/experiments/E0062_em_ipn/annotated_traced_neurons")
neurons_dict = fl.load(data_folder / "all_skeletons.h5")

dest_dir = data_folder.parent / "ipn_ref_meshes"
dest_dir.mkdir(exist_ok=True)
for s in [1, 2, 4]:
    mesh_folder = dest_dir / f"ipn_ref_meshes_lw{s}"
    mesh_folder.mkdir(exist_ok=True)

    for cid, neuron in tqdm(list(neurons_dict.items())):
        coords = neuron.get_coords("ipn").copy()
        mesh = neuron.generate_mesh(
            space="ipn", soma_radius=2.0, dendrite_radius=0.1 * s, axon_radius=0.1 * s
        )

        file = mesh.export(str(mesh_folder / f"mesh_{neuron.id}.obj"))
