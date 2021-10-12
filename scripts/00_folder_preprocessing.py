from tqdm import tqdm

from lotr.preprocessing import preprocess_folder

if __name__ == "__main__":
    from pathlib import Path

    data_path = Path(r"/Users/luigipetrucco/Desktop/210611_f1")
    paths = [f.parent for f in data_path.glob("*/*meta*")]

    all_errors = []
    for path in tqdm(paths):
        preprocess_folder(
            path,
            recompute_bout_df=True,
            recompute_regressors=True,
            recompute_filtering=True,
        )
        # print("Problems with path ", path)
        # all_errors.append(str(path))

    with open("all_wrong.txt", "w") as f:
        f.writelines(all_errors)
