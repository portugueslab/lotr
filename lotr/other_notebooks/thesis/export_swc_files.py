import os
from collections import deque

import pandas as pd
from bg_atlasapi import BrainGlobeAtlas
from knossos_utils.skeleton import Skeleton
from tqdm import tqdm

from lotr import DATASET_LOCATION
from lotr.em.transformations import em2ipnref


def insert(originalfile, string):
    with open(originalfile, "r") as f:
        with open("newfile.txt", "w") as f2:
            f2.write(string)
            f2.write(f.read())
    os.rename("newfile.txt", originalfile)


def find_link_to_soma(soma_node):
    """Function to find last node linking soma and axon nodes."""

    tovisit = deque()
    tovisit.append(soma_node)
    visited = {soma_node}
    link_to_soma_node = set()
    while len(tovisit) > 0:
        visiting = tovisit.popleft()
        for neighbor in visiting.getNeighbors():
            if "axon" in neighbor.getComment().lower():
                link_to_soma_node.add(visiting)
            else:
                if neighbor not in visited:
                    tovisit.append(neighbor)

        visited.add(visiting)

    if len(link_to_soma_node) > 1:
        print("problems at ", link_to_soma_node)
    return link_to_soma_node.pop()


def label_axon_inplace(axon_node, soma_node):
    """Label as axons all segments linked to axon and away from soma."""
    link_to_soma_node = find_link_to_soma(soma_node)
    queue = deque()
    queue.append(axon_node)
    visited = {axon_node}

    while len(queue) > 0:
        next_node = queue.popleft()
        if next_node is not link_to_soma_node:
            next_node.setPureComment("axon")
            for neighbor in next_node.getNeighbors():
                if neighbor not in visited:
                    queue.append(neighbor)

        visited.add(next_node)


def rebase_df(df):
    rebased = df.copy()
    for i, idx in enumerate(rebased.iloc[:, 0]):
        if df.iloc[i, 6] not in df.iloc[:, 0].values:
            rebased.iloc[i, 6] = -1

        rebased.iloc[rebased.iloc[:, 6] == idx, 6] = i + 1  # 1 starting indexing
        rebased.iloc[i, 0] = i + 1  # 1 starting indexing

    return rebased


master_folder = DATASET_LOCATION / "anatomy" / "swc_neurons"
data_folder = master_folder.parent / "annotated_traced_neurons"
data_folder.exists()
for f in list(data_folder.glob("*.nml")):
    print(
        f.name,
    )

# Create target folder
swc_em_dest_folder = master_folder / "swc_emspace"
swc_em_dest_folder.mkdir(exist_ok=True)

# Loop over all annotation batch files:
for f in list(data_folder.glob("*.nml")):
    skeleton = Skeleton()
    skeleton.fromNml(str(f))

    skeletons = []

    for annotation in list(iter(skeleton.annotations)):

        # Sort out cases where we are reconstructing an axon:
        is_axon = ("axon" in annotation.getComment() or "habaxon" in f.name) and (
            "all_somas" not in f.name
        )
        print(annotation.getComment(), ["not an axon", "is axon"][is_axon])

        # Split large combined annotation into annotations of individual neurons:
        id_cell = annotation.getComment().split(" ")[0]
        new_skeleton = Skeleton()
        new_skeleton.add_annotation(annotation)
        new_skeleton.scaling = skeleton.scaling

        # Cleanup confusing comments and seed as soma:

        if is_axon:
            [n.setPureComment("axon") for n in new_skeleton.getNodes()]

        else:
            print("placing soma")
            soma_node = None
            for node in list(new_skeleton.getNodes()):
                if "soma" in node.getComment().lower():
                    node.setPureComment("soma")
                    node.setRoot()
                if "seed" in node.getComment().lower():
                    node.setRoot()
                    node.setPureComment("soma")
                    soma_node = node

            try:
                axon_node = [
                    n
                    for n in new_skeleton.getNodes()
                    if "axon" in n.getComment().lower()
                ][0]
                label_axon_inplace(
                    axon_node,
                    [n for n in new_skeleton.getNodes() if "soma" in n.getComment()][0],
                )

                [
                    n.setPureComment("dendrite")
                    for n in new_skeleton.getNodes()
                    if "soma" not in n.getComment().lower()
                    and "axon" not in n.getComment().lower()
                ]

            except IndexError:
                print("No axon found")
                pass

        new_skeleton.reset_all_ids()
        new_skeleton.toSWC(
            f"cell_{id_cell}", dest_folder=str(swc_em_dest_folder), px=True
        )

        fname = swc_em_dest_folder / f"cell_{id_cell}.swc"
        df = pd.read_csv(fname, delimiter=" ", header=None)
        df = df.drop_duplicates()

        df.to_csv(fname, sep=" ", header=False, index=False)


swc_ipn_dest_folder = master_folder / "swc_ipnspace"
swc_ipn_dest_folder.mkdir(exist_ok=True)

swc_ipnflip_dest_folder = master_folder / "swc_ipnspace_flip"
swc_ipnflip_dest_folder.mkdir(exist_ok=True)

swc_ipnax_dest_folder = master_folder / "swc_ipnspace_flip_ax"
swc_ipnax_dest_folder.mkdir(exist_ok=True)

swc_ipndend_dest_folder = master_folder / "swc_ipnspace_flip_dend"
swc_ipndend_dest_folder.mkdir(exist_ok=True)


atlas = BrainGlobeAtlas("ipn_zfish_0.5um")
midline = atlas.shape[2] // 2

all_dfs = []
all_flips = []
for f in tqdm(list(swc_em_dest_folder.glob("*.swc"))):
    df = pd.read_csv(f, delimiter=" ", header=None)
    df = df.drop_duplicates()
    df.loc[:, [2, 3, 4]] = em2ipnref(df[[2, 3, 4]].values) * 2
    df.to_csv(swc_ipn_dest_folder / f.name, sep=" ", header=False, index=False)

    flip_df = df.copy()
    # Flip all stuff with dendritic centroid on the left side
    if flip_df.loc[flip_df[1] == 3, 4].median() > midline:
        flip_df.loc[:, 4] = midline - (flip_df.loc[:, 4] - midline)

    flip_df.to_csv(swc_ipnflip_dest_folder / f.name, sep=" ", header=False, index=False)

    dendr_df = flip_df[flip_df[1] == 3].copy()
    axon_df = flip_df[flip_df[1] == 2].copy()

    dendr_df = rebase_df(dendr_df)
    axon_df = rebase_df(axon_df)

    if len(axon_df) > 0:
        axon_df.to_csv(
            swc_ipnax_dest_folder / f.name, sep=" ", header=False, index=False
        )

        dendr_df.to_csv(
            swc_ipndend_dest_folder / f.name, sep=" ", header=False, index=False
        )
    else:
        print("?")

    all_dfs.append(df)

for f in master_folder.glob("*/*.swc"):
    insert(f, f"#{f.stem}\n")
