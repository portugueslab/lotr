from pathlib import Path

import flammkuchen as fl
import numpy as np
from fimpylab import LightsheetExperiment
from scipy.io import savemat
from tqdm import tqdm

from lotr.behavior import get_bouts_props_array

DEST_DIR = Path()  # specify destination path

SOURCE_MASTER_DIR = Path()  # specify source path

fish_folders =
PATH_LIST = [SOURCE_MASTER_DIR / fish_folder for fish_folder in fish_folders]

["210314_f1_natmov", "210601_f0_natmov_noeyes", "210601_f3_natmov_spont", "210715_f5_clol",]

for path in tqdm(PATH_LIST):
    path = Path(path)
    traces = fl.load(path / "filtered_traces.h5", "/detr")
    try:
        selection = fl.load(path / "selected_cc.h5")
    except OSError:
        selection = fl.load(path / "selected.h5")

    exp = LightsheetExperiment(path)

    bouts_df = fl.load(path / "bouts_df.h5")
    if "idx_imaging" not in bouts_df.columns:
        bouts_df["idx_imaging"] = np.round(bouts_df["t_start"]).astype(np.int) * int(
            exp.fs
        )

    theta_turned = get_bouts_props_array(
        traces.shape[0], bouts_df, min_bias=0, selection="all", value="bias"
    )

    savemat(
        DEST_DIR / f"{path.name}_traces_behavior_export.mat",
        dict(traces=traces, ring_idxs=selection + 1, theta_turned=theta_turned),
    )
    fl.save(
        DEST_DIR / f"{path.name}_traces_behavior_export.h5",
        dict(traces=traces, ring_idxs=selection, theta_turned=theta_turned),
    )
