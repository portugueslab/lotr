from pathlib import Path

from lotr.file_utils import mirror_all_subfolders

dest_master_path = Path("/Volumes/Shared/experiments/E0071_lotr/full_ring")
master_path = Path("/Users/luigipetrucco/Desktop/all_source_data/full_ring")

mirror_all_subfolders(
    master_path,
    dest_master_path,
    file_patterns=[
        "*centering_mtx.npy*",
        # "data_from_suite2p_unfiltered.h5",
    ],
)
