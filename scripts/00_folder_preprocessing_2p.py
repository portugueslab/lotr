from tqdm import tqdm

from lotr.data_preprocessing.preprocessing import preprocess_folder

if __name__ == "__main__":
    from pathlib import Path

    master_path = Path(r"/Volumes/Shared/experiments/E0040_motions_cardinal/v26")
    fish_list = list(master_path.glob("*_f*"))

    for data_path in fish_list:
        paths = [f.parent for f in data_path.glob("*suite2p/*00*/*meta*")]

        for path in tqdm(paths):
            try:
                preprocess_folder(
                    path,
                    recompute_bout_df=False,
                    recompute_regressors=False,
                    recompute_filtering=True,
                )
            except IndexError:
                print("indexerror", path)
            # print("Problems with path ", path)
