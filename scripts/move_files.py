from pathlib import Path

from lotr.file_utils import mirror_all_subfolders

master_path = Path("/Volumes/Shared/experiments/E0040_motions_cardinal/batch210728")
dest_master_path = Path("/Users/luigipetrucco/Desktop/source_data_batch1")

mirror_all_subfolders(
    master_path, dest_master_path, file_patterns=["data_from_suite2p_unfiltered.h5"]
)
