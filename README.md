# LOTR project analysis
[![tests](https://github.com/portugueslab/lotr/actions/workflows/main.yml/badge.svg)](https://github.com/portugueslab/lotr/actions/workflows/main.yml)

This repository contains all the code for reproducing analyses and figures for the paper [Petrucco et al, Neural dynamics and architecture of the heading direction circuit in a vertebrate brain](#TODO bioarxive link). 


The code is developed and tested in a `python==3.8.8` environment.

## Installation:
Clone the package locally, navigate to the cloned repo, and run
```shell
 pip install . -e
```

## Description of the repository
The code is organized in three main parts:

- `lotr/lotr`: contains the core of the code used in the various analyses, as well as all utility funtions used thoughout the notebooks and scripts
- `lotr/scripts`: mostly scripts for data preprocessing. The only one really relevant for reproducing the analyses is `00_folder_preprocessing.py`. This is the place where the `filtered_traces.h5`, `bouts_df.hf` and `motor_regressors.h5` files are generated.
- `lotr/notebooks`: notebooks where all key analyses are illustrated and figures for the whole paper are generated.

### `lotr/lotr`
The core of the paper code. The key parts of the analysis are illustrated in notebooks that explain in details the procedures used, so here we just give an overview of the contents.

The core data-interface class is `lotr.experiment_class.LotrExperiment`. This is used everywhere to read the data from the folder of each fish. 

`lotr.preprocessing` contains utility functions for the data preprocessing.

`lotr.pca` contains functions that are used for calculating the PCA, although it mostly rely on external packages. Functions for the rPC calculation are in `lotr.rpc_calculation`

`lotr.default_vals` has an explicit declaration of the hardcoded variables used throughout the analyses.

`lotr.behavior` contains the functions for analysing the behavior, and estimating the fictive heading direction.

`lotr.analysis` contains functions for some of the paper quantifications. Those functions are all illustrated in the notebooks.

`lotr.em` contains classes and functions for loading, transforming and visualizing the EM data. 

`lotr.plotting` contains utility functions for generating the paper figures.


### `lotr/notebooks`

All the analyses concerning the lightsheet data, including a thorough explanation of the rPC computation, the phase extraction, the virtual heading estimation, etc., are in two folders, `lotr/notebooks/activity` and `lotr/notebooks/activity_not_gh_testable`. The notebooks are split as for the ones where this is possible, they are run in GitHub Actions to ensure that they do not contain bugs. As they can run only with a small example dataset accessible from GH Actions, some notebooks that require the whole dataset have to be excluded Therefore, as long as the tests are passing, `lotr/notebooks/activity` notebooks are guaranteed to work.

Start from these folders if you want to check the main analyses of the paper.

The anatomical visualizations were performed with the notebook in `lotr/notebooks/anatomy`. In particular, the notebooks `Figure 4 panels.ipynb` and `Figure 5 panels.ipynb` contains the EM-related plots of fig 4 and fig 5 of the paper, as well as the relative supplementary figures.

The analyses that concern the 2p data can be found in `lotr/notebooks/2p`. `Figure4.ipynb` generate the plots in fig 4 and fig s19. The `2d_auto-correlation.ipynb` file generate fig 5c,d and fig S21 from the preprocessed data (data are preprocessed in `Fig5_preprocessing.ipynb`).



## Developers

### Installation with notebook clean hook

To commit notebooks without content, install `nb-clean`:
```shell
python3 -m pip install nb-clean
```

And in the repo local path:
```
nb-clean add-filter
```

### Regenerate local figures
To regenerate all figures in the figures folder, run:
```
pytest --cov --nbmake "./notebooks/activity/"  -n=auto
```

### Export all notebooks:
To export all testable notebooks to PDFs, you can run the following script:
```
python ...lotr/scripts/export_all_notebooks.py
```
Exporting the notebooks will also regenerate figures!
