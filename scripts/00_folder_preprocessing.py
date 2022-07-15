from tqdm import tqdm

from lotr.data_preprocessing.preprocessing import preprocess_folder

if __name__ == "__main__":
    from pathlib import Path

    data_path = Path(r"/Volumes/Shared/experiments/E0040_motions_cardinal/v26")
    paths = [f.parent for f in data_path.glob("*/*meta*")]

    all_errors = []
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
        # all_errors.append(str(path))

    with open("all_wrong.txt", "w") as f:
        f.writelines(all_errors)
