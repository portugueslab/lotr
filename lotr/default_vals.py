# Minimum bias value that defines a turn:
TURN_BIAS = 0.2

# Tau for the computation of the regressor. Longer than expected GCaMP tau
# as from trace observation motor-associated transients seem to decay slower
REGRESSOR_TAU = 5

# Window in seconds for smoothing traces when calculating the PCA/phase
TRACES_SMOOTH_S = 5

# Time intervals over which to compute PCA in different experimental conditions
T_START = 100  # exclude the very first part of the exp, after lightsheet laser on
