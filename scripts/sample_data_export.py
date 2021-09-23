from fimpylab import LightsheetExperiment
from pathlib import Path
import numpy as np
import flammkuchen as fl
from scipy.io import savemat
from lotr.behavior import get_bouts_props_array
from tqdm import tqdm

DEST_DIR = Path("/Users/luigipetrucco/Desktop/sample_data_export")

PATH_LIST = ["/Users/luigipetrucco/Desktop/source_data_old/210314_f1_natmov",
             "/Users/luigipetrucco/Desktop/source_data_old/210601_f0_natmov_noeyes",
             "/Users/luigipetrucco/Desktop/source_data_old/210601_f3_natmov_spont",
             "/Users/luigipetrucco/Desktop/source_data/210715_f5_clol"
             ]

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
        bouts_df["idx_imaging"] = np.round(bouts_df["t_start"]).astype(np.int) * int(exp.fn)

    theta_turned = get_bouts_props_array(
        traces.shape[0], bouts_df, min_bias=0, selection="all", value="bias")

    savemat(DEST_DIR / f"{path.name}_traces_behavior_export.mat",
            dict(traces=traces,
                 ring_idxs=selection + 1,
                 theta_turned=theta_turned))
    fl.save(DEST_DIR / f"{path.name}_traces_behavior_export.h5",
            dict(traces=traces,
                 ring_idxs=selection,
                 theta_turned=theta_turned))