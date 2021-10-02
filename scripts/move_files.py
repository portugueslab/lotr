from pathlib import Path

from lotr.file_utils import mirror_all_subfolders

master_path = Path(
    "/Volumes/Shared/experiments/E0040_motions_cardinal/batch210922/last"
)
dest_master_path = Path("/Users/luigipetrucco/Desktop/batch_210922")

mirror_all_subfolders(
    master_path,
    dest_master_path,
    file_patterns=[
        "*behavior_log*",
        "*stimulus_log*",
        "*metadata.json",
        # "data_from_suite2p_unfiltered.h5",
    ],
)
