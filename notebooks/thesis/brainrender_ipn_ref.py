from brainrender import Scene
# from vedo.colors import makePalette
from pathlib import Path
from bg_atlasapi import BrainGlobeAtlas
import brainrender
from lotr import DATASET_LOCATION

brainrender.WHOLE_SCREEN = False
brainrender.BACKGROUND_COLOR = "white"

print(BrainGlobeAtlas)
data_folder = Path("/Users/luigipetrucco/Google Drive/data/ipn_tracing/annotated_pooled")
#atlas = Atlas(DATASET_LOCATION.parent / "anatomy" / "ipn_zfish_0.5um_v1.7")

# Render scene
scene = Scene(atlas_name="ipn_zfish_0.5um")  #"ipn_zfish_0.5um")
#scene.add_brain_region(["col_r_med", "col_r_lat"], color="slategray", alpha=0.1)
#scene.add_brain_regions(["core"], use_original_color=False, 
#                        wireframe=True, color="slategray", alpha=0.3)

meshes_folder = data_folder / "ipn_ref_meshes"
#mesh_list = ["53", "84"]
col_list = ["lightcoral", "lightgreen", "lightblue"]

mesh_lists = [[33, 34, 38, 53, 54, 80, 84], ["06", 15, 17, 19, 23, 39, 86],
              [61, 45, 65, 69, 70]]

#for mesh_list, c in zip(mesh_lists, col_list):
#    for m in mesh_list:
#        scene.add(str(meshes_folder / f"mesh{str(m)}.obj"), color=c, alpha=1)
# scene.add_neurons(neurons, color=makePalette(len(neurons), "salmon", "powderblue"))
scene.render()
# scene.export_for_web("/Users/luigipetrucco/Desktop/ipn_gad1blcol.html")