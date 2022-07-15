# Dataset description


## Functional imaging data


### Lightsheet data
In the folder full_ring there are the data from all light-sheet experiments described in the paper. 

---
**Note:**
Large raw data (the original imaging stacks from the microscope, and the 400 Hz videos for DLC eye and tail extraction) are not uploaded here for space reasons and are available only upon request. What we refer to as raw data here is the data (imaging and behavior) that comes out from the first stage of the analysis, which is performed using packages that are standard in neuroscience data pipelines (`suite2p` and `DeepLabCut`); as opposed to preprocessed data, files to cache intermediate refined values between the raw data and the final analyses.
---

For every fish, the folder contains:

**Raw data**:
- `[xxx]_metadata.json`, `[xxx]_behavior_log.hdf5`, `[xxx]_stimulus_log.hdf5`, `[xxx]_img.png`, `[xxx]_video.mp4` (optional) : experiment metadata and the stimulus/behavior log as generated from Stytra (for a thorough description, see the [documentation here](https://portugueslab.github.io/bouter/embedded-fish-behavioral-analysis.html)).


- `data_from_suite2p_unfiltered.h5`: `hdf5` file containing the raw traces extracted from suite2p (using the parameters visible in Suite2p_gad1bls.ipynb), the average stack anatomy, and the ROIs masks stack


- `[xxx]_videoDLC_resnet50_zebrafish-lightsheetaMonth_shuffle1_anhour.h5`, `[xxx]_videoDLC_resnet50_zebrafish-lightsheetaMonth_shuffle1.pickes` (optional) : files from the deeplabcut extraction process, see DLC docs (labels of body parts are very explicit). DLC was run on Google Colab using the standard notebook the package provides.


**Preprocessed data**:          
- `filtered_traces.h5`: traces of dF/F values calculated in the `lotr/scripts/00_folder_preprocessing.py` script as described in the paper methods


- `selected.h5`: contains the list of indexes of r1pi neurons in the dataset, selected as described in the paper methods using the interactive notebook `lotr/notebooks/interactive_processing/PCA rot - selection with Lotr class.ipynb`

- `centering_mtx.npy`: transformation matrix to register each fish to a common reference space.


- `bouts_df.h5`: `pd.DataFrame`  indexes a bunch of parameters (amplitude, angle, etc) for every detected swim episode ("bout", in the zebrafish `lot/scripts/00_folder_preprocessing.py`    lingo). It uses `bouter`, see [the documentation](https://portugueslab.github.io/bouter) for a description of the process


- `motor_regressors.h5`: motor regressors computed for all cells in the dataset as described in the methods section, calculated in the `lotr/scripts/00_folder_preprocessing.py` script. 


- `behavior_from_dlc.h5` (optional): contains extracted and time-aligned data from the DLC tracking, for the animals with a video available.


- `raw_selected_movie.mp4` (optional): Animation showing activity of the r1pi neurons over time, generated using the `lotr/lotr/plotting/gif_gen/raw_activity_movie.py` script.


## Anatomy data

Anatomical data are contained in the `anatomy` folder. It contains confocal/reference data and the electron microscopy (EM) tracing data

**Confocal/reference data**
- `elavl_mcherry_gad1b_gal4_stack`: contains the tiff files for the two channels of an imaged elavl3:mCherry;gad1b:Gal4;UAS:Dendra fish that is used in the paper to illustrate the distribution of expression of the gad1b:Gal4;UAS:Dendra line (fig 1, fig S1).


- `avg_gad1b_confocal`: average of multiple gad1b:Gal4;UAS:Dendra fish registered to the MapZBrain reference.


- `mean_ls_anatomy.tiff`: average of all the lightsheet experiments on gad1b:Gal4;UAS:GCaMP6s fish morphed to the IPN/aHB reference


- `ipn_zfish_0.5um_v1.8`: atlas in `BrainGlobe` standard format (see (here)[#TODO]). Mainly, it contains stacks from different lines co-registered in the same coordinate space. Together, expression patterns in those lines provide a very thorough delineation of the anterior hindbrain regions:
  - `h2b.tiff` : elavl3:H2B-GCaMP6s (nuclear, panneuronal expression)  
  - `16715.tiff`: 16715:Gal4;UAS:GCaMP6s (cytosolic in habenular axons, delimits the IPN)
  - `gad1b.tiff`: gad1b:GFP (cytosolic in all gad1b expressing neurons, direct driver line)
  - `gal4_gad1b.tiff`: gad1b:Gal4;UAS:Dendra (cytosolic in a fraction of gad1b expressing neurons, including r1pi neurons)
  - `annotation.tiff`: annotation of the different regions of the IPN and the aHB. This annotation was used in all the figures where the IPN/dIPN is represented.


**EM data**
- `aHB_dIPN.k.zip`: [Knossos](https://knossos.app/)-compatible dataset (a compressed `XML` file) containing the coordinates and the graphs of all the reconstructed skeletons in the paper dataset. Code for open and plot the skeletons is available in `lotr/lotr/em` and can be seen at work in `lotr/notebooks/anatomy/Figure 4 panels.ipynb`
- `reconstructions`: folder containing the volumetric meshes for the two fully segmented neurons shown in fig s17, as well as the synaptic contacts shown in fig s17.



