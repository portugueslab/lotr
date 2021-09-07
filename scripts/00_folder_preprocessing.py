import flammkuchen as fl
import numpy as np
import pandas as pd
from bouter.utilities import predictive_tail_fill
from fimpylab import LightsheetExperiment
from tqdm import tqdm

from lotr.behavior import create_motor_regressors
from lotr.data_loading import preprocess_traces
from lotr.utils import pearson_regressors
from lotr.default_vals import TURN_BIAS, TRACES_SMOOTH_S


def preprocess_folder(
    data_path,
    recompute_bout_df=False,
    recompute_filtering=False,
    recompute_regressors=False,
):
    paths = [f.parent for f in data_path.glob("*/*meta*")]

    for path in tqdm(paths):
        exp = LightsheetExperiment(path)
        fn = int(exp.fs_imaging)

        # Extract bout dataframe:
        if not (path / "bouts_df.h5").exists() or recompute_bout_df:
            beh_df = exp.behavior_log
            theta_mat = beh_df.loc[:, [f"theta_0{i}" for i in range(9)]].values
            beh_df.loc[:, [f"theta_0{i}" for i in range(9)]] = predictive_tail_fill(
                theta_mat
            )

            beh_df["tail_sum"] = (beh_df["theta_07"] + beh_df["theta_08"]) - (
                beh_df["theta_00"] + beh_df["theta_01"]
            )
            bouts_df = exp.get_bout_properties()
            # Compute bout index in behavior trace:
            bouts_df["idx"] = [
                np.argmin((beh_df["t"] - bouts_df.loc[i, "t_start"]).abs())
                for i in bouts_df.index
            ]
            bouts_df["fid"] = path.name

            bouts_df["idx_imaging"] = np.round(bouts_df["t_start"] * fn).astype(np.int)

            bouts_df["direction"] = "fw"
            bouts_df.loc[(bouts_df["bias"] > TURN_BIAS), "direction"] = "rt"
            bouts_df.loc[(bouts_df["bias"] < -TURN_BIAS), "direction"] = "lf"

            fl.save(path / "bouts_df.h5", bouts_df)

        # Filter traces:
        if not (path / "filtered_traces.h5").exists() or recompute_filtering:
            traces_raw = fl.load(path / "data_from_suite2p_unfiltered.h5", "/traces").T
            traces = preprocess_traces(
                traces_raw, fn, smooth_wnd_s=TRACES_SMOOTH_S, detrend_wnd_s=900
            )
            traces_und = preprocess_traces(
                traces_raw, fn, smooth_wnd_s=TRACES_SMOOTH_S, detrend_wnd_s=None
            )
            fl.save(path / "filtered_traces.h5", dict(detr=traces, undetr=traces_und))

        # Computer behavior regressors:
        if not (path / "motor_regressors.h5").exists() or recompute_regressors:
            traces = fl.load(path / "filtered_traces.h5", "/detr")
            bouts_df = fl.load(path / path / "bouts_df.h5")
            reg_dict = create_motor_regressors(
                traces.shape[0], bouts_df, fn, min_bias=0.05
            )

            traces_derivative = np.zeros(traces.shape)
            traces_derivative[:-1, :] = np.abs(np.diff(traces, axis=0))

            reg_mat = pearson_regressors(traces, reg_dict.values).T
            reg_mat_diff = pearson_regressors(traces_derivative, reg_dict.values).T

            reg_df = pd.DataFrame(
                np.concatenate([reg_mat, reg_mat_diff], axis=1),
                columns=list(reg_dict.columns)
                + [c + "_dfdt" for c in reg_dict.columns],
            )

            fl.save(path / "motor_regressors.h5", reg_df)


if __name__ == "__main__":
    from pathlib import Path

    preprocess_folder(
        Path("/Users/luigipetrucco/Desktop/hagar_data"),
        recompute_bout_df=False,
        recompute_regressors=False,
    )
    # preprocess_folder(Path("/Users/luigipetrucco/Desktop/source_data_batch1"),
    #                  recompute_bout_df=True)
