# Specify where the dataset is stored.
DATASET_DEFAULT_LOCATION = r"\\FUNES\Shared\experiments\E0071_lotr\full_ring"

# Minimum bias value that defines a turn:
TURN_BIAS = 0.2

# Tau for the computation of the regressor. Longer than expected GCaMP tau
# as from trace observation motor-associated transients seem to decay slower
REGRESSOR_TAU_S = 5

# Window in seconds for smoothing traces when calculating the PCA/phase
TRACES_SMOOTH_S = 5

# Standard sampling frequency to which experiments will be resampled if needed
# (most experiments have this FN already):
DEFAULT_FN = 5

# window before and after bouts for cropping:
PRE_BOUT_WND_S, POST_BOUT_WND_S = 10, 25

# Pad time at beginning and end of experiment in seconds when calculating PCA:
PCA_TIME_PAD_S = 150

# Anatomical orientation of source data
ANATOMICAL_ORIENT_SOURCE = "ilp"

# Anatomical orientation of figures:
ANATOMICAL_ORIENT_FIGURES = "ipl"

# lightsheet microscope pixel size in um, from calibration:
LIGHTSHEET_CAMERA_RES_XY = (0.6, 0.6)
