# Minimum bias value that defines a turn:
TURN_BIAS = 0.2

# Tau for the computation of the regressor. Longer than expected GCaMP tau
# as from trace observation motor-associated transients seem to decay slower
REGRESSOR_TAU = 5

# Window in seconds for smoothing traces when calculating the PCA/phase
TRACES_SMOOTH_S = 5

# Time intervals over which to compute PCA in different experimental conditions
T_START = 100  # exclude the very first part of the exp, after lightsheet laser on

# Specify where the dataset is stored.
DATASET_DEFAULT_LOCATION = (
    r"\\FUNES\Shared\experiments\E0071_lotr\full_ring"
)

# Anatomical orientation of source data
ANATOMICAL_ORIENT_SOURCE = "ilp"

# Anatomical orientation of figures:
ANATOMICAL_ORIENT_FIGURES = "ipl"

# lightsheet microscope pixel size in um, from calibration:
LIGHTSHEET_CAMERA_RES_XY = (0.6, 0.6)
