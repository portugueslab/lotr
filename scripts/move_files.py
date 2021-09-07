from pathlib import Path

from lotr.file_utils import mirror_all_subfolders

master_path = Path("/Volumes/Shared/experiments/E0040_motions_cardinal/v13_cw_ccw/ls_fixed/spont_plus_v13/new")
dest_master_path = Path("/Users/luigipetrucco/Desktop/hagar_data")

mirror_all_subfolders(
    master_path, dest_master_path, file_patterns=["data_from_suite2p_unfiltered.h5"]
)
