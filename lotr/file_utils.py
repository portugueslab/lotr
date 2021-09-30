from shutil import copy
import re

from tqdm import tqdm


def folder_2_fid(folder):
    """take only actual fish id of date and fish number.
    """

    f_n = "".join(re.split(r"(\d+)", folder.name.split("_")[1])[:2])
    date = folder.name.split("_")[0]

    return f"{date}_{f_n}"


def mirror_all_subfolders(source_master_path, dest_master_path, file_patterns=None):
    dest_master_path.mkdir(exist_ok=True)

    # paths = [source_path / f.name for f in dest_master_path.glob("*_f*")]

    for path in tqdm(list(source_master_path.glob("*[0-9]_f[0-9]*"))):
        mirror_fish_folder(path, dest_master_path / path.name, file_patterns)


def mirror_fish_folder(source_path, dest_path, file_patterns=None,
                       overwrite=False):

    if file_patterns is None:
        file_patterns = [
            "*behavior_log*",
            "*stimulus_log*",
            "*metadata.json",
            "data_from_suite2p_unfiltered.h5",
            "bouts_df.h5",
            "*selected*.h5",
            "filtered_traces.h5"
        ]
    # [

    dest_path.mkdir(exist_ok=True)

    for pattern in file_patterns:
        for file in source_path.glob(pattern):
            if overwrite or not (dest_path / file.name).exists():
                copy(file, dest_path / file.name)
