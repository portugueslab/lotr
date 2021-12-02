from pathlib import Path
from shutil import copy

from tqdm import tqdm

file_patterns = ["*centering_mtx.npy*"]
overwrite = False

dest_master_path = Path("/Volumes/Shared/experiments/E0071_lotr/full_ring")
master_path = Path("/Users/luigipetrucco/Desktop/all_source_data/full_ring")


for path in tqdm(list(master_path.glob("*[0-9]_f[0-9]*/*[0-9]_f[0-9]*"))):
    dest_path = dest_master_path / path.parent.name / path.name
    for pattern in file_patterns:
        for file in path.glob(pattern):
            if overwrite or not (dest_path / file.name).exists():
                copy(file, dest_path / file.name)
