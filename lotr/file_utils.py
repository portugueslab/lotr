from shutil import copy
from pathlib import Path
from tqdm import tqdm


def mirror_all_subfolders(source_master_path, dest_master_path, file_patterns=None):
    dest_master_path.mkdir(exist_ok=True)

    # paths = [source_path / f.name for f in dest_master_path.glob("*_f*")]

    for path in tqdm(source_master_path.glob("*[0-9]_f[0-9]*")):
        mirror_fish_folder(path, dest_master_path / path.name, file_patterns)


def mirror_fish_folder(source_path, dest_path, file_patterns=None):

    if file_patterns is None:
        file_patterns = ["*behavior_log*", "*stimulus_log*",
                          "*metadata.json", "data_from_suite2p_unfiltered.h5"]
    # ["bouts_df.h5", , "*selected*.h5",

    dest_path.mkdir(exist_ok=True)

    for pattern in file_patterns:
        for file in source_path.glob(pattern):
            copy(file, dest_path / file.name)
