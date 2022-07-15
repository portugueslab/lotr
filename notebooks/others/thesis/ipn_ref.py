import tarfile
from pathlib import Path

import flammkuchen as fl
import numpy as np
import requests
import tifffile
from allensdk.core.structure_tree import StructureTree
from bg_atlasapi.utils import retrieve_over_http
from bg_atlasgen.wrapup import wrapup_atlas_from_data
from skimage.measure import marching_cubes_lewiner

# Specify information about the atlas:
RES_UM = 0.5
VERSION = 8
ATLAS_NAME = "ipn_zfish"
SPECIES = "Danio rerio"
ATLAS_LINK = "unpublished"
CITATION = "unpublished"
ORIENTATION = "asl"
ATLAS_PACKAGER = "Luigi Petrucco (luigi.petrucco@gmail.com)"

working_dir = Path("/Users/luigipetrucco/Google Drive/_ipn_zfish_0.5um_v18")

# Generated atlas path:
bg_root_dir = working_dir / "working_atlas_dir"
bg_root_dir.mkdir(exist_ok=True)

reference_stack = tifffile.imread(working_dir / "reference.tiff")

annotation_stack = tifffile.imread(working_dir / "annotation.tiff")

additional_references = dict()
for line in ["16715", "gad1b", "h2b", "gal4_gad1b"]:
    additional_references[line] = tifffile.imread(working_dir / f"{line}.tiff")

# Initiate dictionary with root info:
structures_list = [
    {
        "name": "root",
        "acronym": "root",
        "id": 1,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1],
    },
    {
        "name": "interpeduncular nucleus",
        "acronym": "ipn",
        "id": 2,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 2],
    },
    {
        "name": "interpeduncular nucleus - neuropil",
        "acronym": "ipn_neuropil",
        "id": 3,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 2, 3],
    },
    {
        "name": "dorsal interpeduncular nucleus",
        "acronym": "dipn",
        "id": 4,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 2, 3, 4],
    },
    {
        "name": "ventral interpeduncular nucleus",
        "acronym": "vipn",
        "id": 5,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 2, 3, 5],
    },
    {
        "name": "glomeruli",
        "acronym": "glomeruli",
        "id": 6,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 2, 3, 5, 6],
    },
    {
        "name": "lateral glomerulus (2), right",
        "acronym": "g2_r",
        "id": 9,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 2, 3, 5, 6, 9],
    },
    {
        "name": "medial glomerulus (1), right",
        "acronym": "g1_r",
        "id": 10,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 2, 3, 5, 6, 10],
    },
    {
        "name": "caudal glomerulus (3), right",
        "acronym": "g3_r",
        "id": 20,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 2, 3, 5, 6, 20],
    },
    {
        "name": "lateral glomerulus (2), left",
        "acronym": "g2_l",
        "id": 7,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 2, 3, 5, 6, 7],
    },
    {
        "name": "medial glomerulus (1), left",
        "acronym": "g1_l",
        "id": 8,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 2, 3, 5, 6, 8],
    },
    {
        "name": "caudal glomerulus (3), left",
        "acronym": "g3_l",
        "id": 19,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 2, 3, 5, 6, 19],
    },
    {
        "name": "ipn somas core",
        "acronym": "somas_core",
        "id": 11,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 2, 11],
    },
    {
        "name": "rostral somas",
        "acronym": "rostr_somas",
        "id": 12,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 12],
    },
    {
        "name": "caudal somas",
        "acronym": "caud_somas",
        "id": 13,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 13],
    },
    {
        "name": "fasciculus retroflexus",
        "acronym": "fr",
        "id": 14,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 14],
    },
    {
        "name": "fasciculus retroflexus, left branch",
        "acronym": "fr_l",
        "id": 15,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 14, 15],
    },
    {
        "name": "fasciculus retroflexus, right branch",
        "acronym": "fr_r",
        "id": 16,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 14, 16],
    },
    {
        "name": "dorsal interpeduncular nucleus, left part",
        "acronym": "dipn_l",
        "id": 17,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 2, 3, 4, 17],
    },
    {
        "name": "dorsal interpeduncular nucleus, right part",
        "acronym": "dipn_r",
        "id": 18,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 2, 3, 4, 18],
    },
    {
        "name": "ring neurons of the anterior hindbrain",
        "acronym": "ahb_ring",
        "id": 23,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 23],
    },
    {
        "name": "ring neurons of the anterior hindbrain - left",
        "acronym": "ahb_ring_l",
        "id": 21,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 23, 21],
    },
    {
        "name": "ring neurons of the anterior hindbrain - right",
        "acronym": "ahb_ring_r",
        "id": 22,
        "rgb_triplet": [255, 255, 255],
        "structure_id_path": [1, 23, 22],
    },
]

mesh_dir = working_dir / "meshes_final"

meshes_dict = {r["id"]: mesh_dir / f"{r['id']}.stl" for r in structures_list}

# Wrap up, compress, and remove file:0
print("Finalising atlas")
wrapup_atlas_from_data(
    atlas_name=ATLAS_NAME,
    atlas_minor_version=VERSION,
    citation=CITATION,
    atlas_link=ATLAS_LINK,
    species=SPECIES,
    resolution=(RES_UM,) * 3,
    orientation=ORIENTATION,
    root_id=1,
    reference_stack=reference_stack,
    annotation_stack=annotation_stack,
    structures_list=structures_list,
    meshes_dict=meshes_dict,
    working_dir=bg_root_dir,
    cleanup_files=False,
    compress=True,
    scale_meshes=False,
    additional_references=additional_references,
    atlas_packager=ATLAS_PACKAGER,
)
