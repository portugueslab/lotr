from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

from lotr.experiment_class import LotrExperiment

master_path = Path("/Users/luigipetrucco/Desktop/all_source_data/full_ring")
file_list = sorted(list(master_path.glob("*/*[0-9]_f*")))

dict_list = []

# Loop over all experiments and create a report in excel.
for f in tqdm(file_list):
    exp = LotrExperiment(f)
    bouts_df = exp.bouts_df
    ring_in_acquisition = (f / "selected.h5").exists()
    if exp.fs == 3:
        imaging_area = "aHB+IPN"
    else:
        imaging_area = "IPN" if "ipn" in f.name else "aHB"

    exp_dict = dict(
        fid=f.parent.name,
        experiment_name=f.name,
        protocol_name=exp.protocol_name,
        protocol_version=exp.protocol_version,
        imaging_area=imaging_area,
        eyes="eye" in f.name and "noeye" not in f.name,
        genotype="gad1b:Gal4;UAS:GCaMP6s",
        hdn_in_acquisition=exp.has_hdn,
        imaged_by=exp["general"]["basic"]["experimenter_name"],
        n_bouts=len(bouts_df),
        n_turns=np.sum(np.abs(bouts_df["bias"]) > 0.2),
        n_rois=exp.n_rois,
        n_hdns=len(exp.hdn_indexes) if exp.has_hdn else None,
    )

    dict_list.append(exp_dict)

exp_df = pd.DataFrame(dict_list)
exp_df = exp_df.set_index("experiment_name")
exp_df.to_excel("/Users/luigipetrucco/Desktop/all_ring_fish_report.xlsx")
