# LOTR project analysis
![Version](https://img.shields.io/github/v/tag/portugueslab/lotr.svg)
[![zenodo](https://zenodo.org/badge/DOI/10.5281/zenodo.7715409.svg)](https://doi.org/10.5281/zenodo.7715409)
[![tests](https://github.com/portugueslab/lotr/actions/workflows/main.yml/badge.svg)](https://github.com/portugueslab/lotr/actions/workflows/main.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

This repository contains all the code for reproducing analyses and figures for the paper [Petrucco et al, Neural dynamics and architecture of the heading direction circuit in a vertebrate brain](https://www.biorxiv.org/content/10.1101/2022.04.27.489672v1). 


The code is developed and tested in a `python==3.8.16` environment. It has been partially tested also in `python==3.9`,
other versions of Python are not guaranteed to work. We recommend to run this code in a new environment, which you can create with
```shell
create -n lotr-env python==3.8.16
```

## Installation:
Clone the package locally, navigate to the cloned repo, and run
```shell
 pip install -e .
```


To install in developer mode to easily run all notebooks, you can install it in developer mode:
```shell
 pip install -e ".[dev]"
```

### Troubleshooting for `pytables`

If the installation fails while installing `tables` with the error `ERROR:: Could not find a local HDF5 installation.`, you might want to try to `conda install pytables` and then run again the installation.


### Add kernel to jupyter
If you have installed the package in a new environment, and you already have a Jupyter installation, you can add the new kernel with:
```shell
conda activate lotr-env
conda install ipykernel
ipykernel install --name lotr
```
Make sure that your Jupyter is configured to make correct use of the `matplotlib widgets` backends for the plots. Alternatively, you can remove the specification from the notebooks and leave the standard `matplotlib inline` instead.


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


## Quick replication of the paper analyses

If you just want to replicate quickly the analyses in the paper, follow these steps:
1. Clone this repository locally
2. Install the repository as described above - developer mode is recommended to quickly run all notebooks from the terminal.
3. Download the dataset from the Zenodo repository (**TODO** add link) to a local folder.
4. Create a `.txt` file named `dataset_location.txt` in the repository containing a single line with the path location of the data you downloaded.
5. Create a `.txt` file named `figures_location.txt` in the repository containing a single line with the path location of the folder you want to generate figures and logs in.
6. 
Now you have two options:

**Option 1** To execute all analyses in one run the terminal, navigate inside the repository and run :
```
pytest --nbmake "./notebooks/"  -n=auto
```
In this way, all the figures will be created in the folder you specified together with the statistical analyses report.

If you get one or two error in the anatomy notebooks related to EM, it is fine, it is due to the parallelization. You can just rerun them with `pytest --nbmake "./notebooks/activity/"`.

**Option 2** Alternatively, just open the notebooks in the `lotr/notebooks` section and run them one by one as you read though them!

### Statistical tests summary
A custom results logger function will log all the key numbers from the analysis in a single file that you can find in the figure folder as `results_log.txt`. We are depositing the file we get for the paper figures in this folder, so you can compare your numbers with ours.


Under the `[log_info]` are all the ids of experiments that are used for a given logger.
All other tags refer to specific results that you can read about in the notebooks, for which the n, and the momenta presented in the paper are reported. There is also a list of the fish (and when applicable the ROIs or units) from which the result was produced.


### Export all notebooks
To export all testable notebooks to PDFs that you can just read, you can run the following script:
```
python ...lotr/scripts/export_all_notebooks.py
```
Exporting the notebooks will also regenerate the figures!

## Breakdown of the core analysis code
The key figures and results of replication can be reproduced by code in `lotr/notebooks`.

It is organized in four folders:

- `lightsheet`: all analyses for the lightsheet data - the most part of the functional data of the paper.
- `2p`: analyses for the data shown in Figures 5 and 6 (and supplementary) from two-photon data.
- `anatomy`: code to generate all the anatomical figures from confocal and EM data, r1pi neurons positions, and EM data quantification.
- `modeling`: contains proof-of-principle models and simulations that did not make it in the final paper.


**NB**: The names & numbering of the notebooks only loosely correspond to the flow in the paper - match every single plot with the location
of that analysis in the notebooks would be very error-prone. Just read a bit through them and you'll find what you are looking for!


### `lightsheet`
- `0. Bout histogram fitting.ipynb`: show distribution of swim turns and compute thresholds to define directional swims.
- `1a. Introduction to network phase.ipynb`: a tutorial on how we compute phase.
- `1b. Anatomical organization of the network.ipynb`: analysis on the anatomical organization of the functional activity. Contains also an explanation of the registration procedure for PCs across fish.
- `1c. Activation profile.ipynb`: analysis on the shape of the bump.
- `1d. Anatomy plots.ipynb`: plots on the anatomical distribution or ROIs across fish.
- `1e. Anatomical selection.ipynb`: an alternative analysis to show that the circular distribution or PC projections is really a feature of the HB and does not come as an artefact from our selection criteria.
- `1f. Additional illustrative plots.ipynb`: some additional small plot for visualization, mostly of PC projections.
- `2a. Motor triggered rotations.ipynb`: introduction to how the activity in phase space is moved around by directional swims.
- `2b. Phase dynamics.ipynb`: look at network phase changes and swims.
- `2c. Fictive trajectory.ipynb`: introduce the reconstruction of fictive trajectories and compute phase / heading correlations.
- `2d. Some probability checks.ipynb`: control if there is an increased probability of performing left/right swims given a certain network phase (no, there is not).
- `2e. Multiple circles example.ipynb`: plot an interesting fish where continuous swimming in one or the other direction produces multiple crossings of the network bump of the whole network.
- `2f. Motor efferences.ipynb`: compare the position of r1pi neurons compared to the position of neurons whose activity closely map the direction swam by the fish. 
- `2g. Activation profile stability.ipynb`: investigate the stability of the activation bump in periods of no motion.
- `2h. Phase stability.ipynb`: understand how much the activity is stable in periods of no swimming; also, decode direction turned from phase changes.
- `3a. Phase and visual feedback.ipynb`: analyze visual feedback experiments to understand if visual stimuli have an effect on the network phase.
- `4a. Eye motion.ipynb`: this and the following notebook contain the analysis of the relationship between eye motion and phase changes.
- `4b. Eye motion-eye regressors.ipynb`: regressor-based analysis for eye- vs. heading-related signals in r1pi.
- `4c. Eye motion-saccades.ipynb`: compute the saccade-triggered plots shown in the extended data.

### `anatomy`
- `1. Confocal image - gad1b-GFP and h2b-mCherry.ipynb`: generate images for the gad1b:UAS line from confocal data.
- `2. EM reconstruction previews.ipynb`: generate the views of individual EM reconstructed cells, together with the co-registered views with the confocal and functional data.
- `3. Synapses plot.ipynb`: show the position of pre- and post-synaptic contacts for an individual cell.
- `4. EM anatomical organization analysis.ipynb`: analyse the patterns in the distribution of axons and dendrites of r1pi neurons.

### `2p`
- `1. Fish example 2p data.ipynb`: generate plots on rPC / anatomical distribution of ROIs, and network phase /heading direction relationship. 
- `2. Autocorrelation.ipynb`: spatial autocorrelation of 2p signals to show how signals from the 2p match the connectivity profile of the EM data.

### `modelling`
- `1. Anticorrelation and PCA - simulated data.ipynb`: demonstrate that simple anticorrelation patterns cannot produce _per-se_ the observed distributions in PC space.
- `2. Network model.ipynb`: a simple, proof-of-principle model that produces ring-attractor dynamics given a set of reciprocally inhibiting neurons and tonic excitation.


### Support
Feel free to raise an issue in the repository if you are trying to replicate the analysis and encounter any issue!


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

