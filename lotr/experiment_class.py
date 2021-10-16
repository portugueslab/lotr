from pathlib import Path

import flammkuchen as fl
import numpy as np
from bouter import EmbeddedExperiment

from lotr.anatomy import reshape_stack
from lotr.default_vals import LIGHTSHEET_CAMERA_RES_XY
from lotr.pca import pca_and_phase
from lotr.plotting import color_stack
from lotr.rpca_calculation import get_zero_mean_weights, reorient_pcs


class LotrExperiment(EmbeddedExperiment):
    """Main class for data loading. Look here to follow how any experimental
    quantity loaded in a notebook is taken from the raw files. To check
    how semi-processed files are generated,
    look into lotr/scripts/00_folder_preprocessing.py.

    NOTES: Anatomical space
        Anatomical stacks are returned to follow the following convention:
            (inferior-superior, posterior-anterior, left-right)
        This means that the voxel 0 is located at the ventral-caudal-left corner.

        **Figures are all coded to be top view (left=left of the fish, top=rostral).**

        Therefore:
        plt.imshow for the stacks should be used specifying the origin="lower" argument
        for left to be left of the fish in top view!

        For the coordinates to follow the same convention (origin is set to be
        at the ventral-caudal-left corner when scattering the second two
        coords, left is left and right is right), we have to change their order.
        Coordinates will be:
            (inferior-superior, left-right, posterior-anterior)

        The following code will produce correctly oriented fish:

        # Pixel coordinates:
        plt.imshow(exp.rois_stack.max(0), aspect="auto", origin="lower")
        plt.scatter(exp.coords[:, 1], exp.coords[:, 2])

        # Microns coordinates:
        plt.imshow(exp.rois_stack.max(0), origin="lower", extent=exp.plane_ext_um)
        plt.scatter(exp.coords_um[:, 1], exp.coords_um[:, 2])
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.microscope_config = self["imaging"]["microscope_config"]

        self._dt_imaging = None
        self._resolution = None
        self._n_planes = None
        self._data_shape = None
        self._bouts_df = None
        self._traces = None
        self._hdn_indexes = None
        self._motor_regressors = None
        self._coords = None
        self._raw_traces = None
        self._anatomy_stack = None
        self._rois_stack = None
        self._nonhdn_indexes = None
        self._rndcnt_indexes = None
        self._rpc_scores = None
        self._rpc_angles = None
        self._network_phase = None

    @property
    def fn(self):
        try:
            return int(
                self.microscope_config["lightsheet"]["scanning"]["z"]["frequency"]
            )
        except KeyError:
            return int(self.microscope_config["scanning"]["framerate"])

    @property
    def n_planes(self):
        try:
            return self.microscope_config["lightsheet"]["scanning"]["triggering"][
                "n_planes"
            ]
        except KeyError:
            print("Fix definition for 2p data!")

    @property
    def voxel_size_um(self):
        try:
            z_conf = self.microscope_config["lightsheet"]["scanning"]["z"]
            z_um = (z_conf["piezo_max"] - z_conf["piezo_min"]) / self.n_planes

            return (z_um,) + LIGHTSHEET_CAMERA_RES_XY
            return

        except KeyError:
            print("Fix definition for 2p data!")

    @property
    def lr_extent_um(self):
        return 0, self.rois_stack.shape[2] * self.voxel_size_um[2]

    @property
    def pa_extent_um(self):
        return 0, self.rois_stack.shape[1] * self.voxel_size_um[1]

    @property
    def plane_ext_um(self):
        return self.lr_extent_um + self.pa_extent_um

    @property
    def dt_imaging(self):
        return 1 / self.fn

    @property
    def dir_name(self):
        return self.root.name

    @property
    def bouts_df(self):
        if self._bouts_df is None:
            self._bouts_df = fl.load(self.root / "bouts_df.h5")
        return self._bouts_df

    @property
    def motor_regressors(self):
        if self._motor_regressors is None:
            self._motor_regressors = fl.load(self.root / "motor_regressors.h5")
        return self._motor_regressors

    @property
    def traces(self):
        if self._traces is None:
            self._traces = fl.load(self.root / "filtered_traces.h5", "/detr")
        return self._traces

    @property
    def raw_traces(self):
        if self._raw_traces is None:
            self._raw_traces = fl.load(
                self.root / "data_from_suite2p_unfiltered.h5", "/traces"
            ).T
        return self._raw_traces

    @property
    def rois_stack(self):
        if self._rois_stack is None:
            self._rois_stack = reshape_stack(
                fl.load(self.root / "data_from_suite2p_unfiltered.h5", "/rois_stack")
            )
        return self._rois_stack

    @property
    def anatomy_stack(self):
        if self._anatomy_stack is None:
            self._anatomy_stack = reshape_stack(
                fl.load(self.root / "data_from_suite2p_unfiltered.h5", "/anatomy_stack")
            )
        return self._anatomy_stack

    @property
    def coords(self):
        if self._coords is None:
            self._coords = fl.load(
                self.root / "data_from_suite2p_unfiltered.h5", "/coords"
            )
        return self._coords

    @property
    def coords_um(self):
        return self.coords * self.voxel_size_um

    @property
    def hdn_indexes(self):
        if self._hdn_indexes is None:
            self._hdn_indexes = np.array(fl.load(self.root / "selected.h5"))
        return self._hdn_indexes

    @property
    def nonhdn_indexes(self):
        if self._nonhdn_indexes is None:
            non_hdns = np.ones(self.n_rois, dtype=bool)
            non_hdns[self.hdn_indexes] = False
            self._nonhdn_indexes = non_hdns
        return self._nonhdn_indexes

    @property
    def rndcnt_indexes(self):
        all_possible = np.argwhere(self.nonhdn_indexes).flatten()
        np.random.shuffle(all_possible)
        return all_possible[: len(self.hdn_indexes)]

    @property
    def n_pts(self):
        return self.traces.shape[0]

    @property
    def n_rois(self):
        return self.traces.shape[1]

    @property
    def n_hdns(self):
        return len(self.hdn_indexes)

    @property
    def has_hdn(self):
        return (self.root / "selected.h5").exists()

    @property
    def time_arr(self):
        return np.arange(1, self.n_pts + 1) / self.fn

    @property
    def pca_t_lims(self):
        """Time slicing for the calculation of PCA, excluding the initial part of the
        trace (where drifts/things related to the beginning of the experiment might be
        happening) and the parts with strong stimuli in protocols with dir motion.
        """
        T_PAD_S = 150  # Beginning/end pad time in seconds
        exp_end = int(self["stimulus"]["log"][-1]["t_stop"])

        # TODO use experiment versions here
        stim_type = self.root.name.split("_")[2]

        if stim_type == "cwccw":
            return T_PAD_S, int(self["stimulus"]["log"][1]["t_start"])
        elif stim_type == "2dvr":
            return T_PAD_S, int(self["stimulus"]["log"][2]["t_start"])
        else:
            return T_PAD_S, exp_end - T_PAD_S

    @property
    def pca_t_slice(self):
        t_lims = self.pca_t_lims
        return slice(*[t * self.fn for t in t_lims])

    @property
    def rpc_scores(self):
        """For a tutorial on this calculation, have a look at
        'Anatomical organization of the network.ipynb'
        """
        if self._rpc_scores is None:
            # 1. compute PCs:
            pca_scores, angles, _, circle_params = pca_and_phase(
                self.traces[self.pca_t_slice, self.hdn_indexes].T
            )
            # 2. center on 0:
            centered_pca_scores = pca_scores[:, :2] - circle_params[:2]

            # 3. Find transformation to match anatomy
            # Normalize coords (we don't care about z here)
            w_coords = get_zero_mean_weights(self.coords[self.hdn_indexes, 1:])

            # Find transformation to have at 0 angle rostral ROIs:
            self._rpc_scores = reorient_pcs(centered_pca_scores, w_coords)
        return self._rpc_scores

    @property
    def rpc_angles(self):
        """For a tutorial on this calculation, have a look at
        'Anatomical organization of the network.ipynb'
        """
        if self._rpc_angles is None:
            self._rpc_angles = np.arctan2(self.rpc_scores[:, 1], -self.rpc_scores[:, 0])

        return self._rpc_angles

    @property
    def network_phase(self):
        """For a tutorial on this calculation, have a look at
        'Anatomical organization of the network.ipynb'
        """
        if self._network_phase is None:
            norm_activity = get_zero_mean_weights(self.traces[:, self.hdn_indexes].T).T
            avg_vects = np.einsum("ij,ik->jk", norm_activity.T, self.rpc_scores)

            # This choice of signs ensures that network phase correspond to angle of
            # max activation or ROIs over rPC space:
            self._network_phase = np.arctan2(avg_vects[:, 1], -avg_vects[:, 0])

        return self._network_phase

    def find_mirror_dir(self, parent_folder):
        """Find homonym directory in a new parent folder, for file mirroring."""
        parent_folder = Path(parent_folder)
        matches = list(parent_folder.rglob(self.dir_name))
        if len(matches) > 1:
            raise OSError("Multiple folders found for this experiment")
        return matches[0]

    def color_rois_by(self, values, indexes=None, **kwargs):
        """Color ROI stack by some convention (phase, activity, etc.). If no indexes
        are passed, we assume we are coloring either all ROIs or HDNs.

        Parameters
        ----------
        values : np.array
            Array over which to color the stack
        indexes : np.array (optional)
            Index of ROIs to color (if different from either all or HDNs only)
        kwargs : dict
            Additional kwargs for the color_stack function. Most importantly,
            color_scheme and vlims might be handy to set.

        Returns
        -------

        """
        if indexes is None:
            if len(values) == self.n_rois:
                indexes = np.arange(self.n_rois)
            elif len(values) == len(self.hdn_indexes):
                indexes = self.hdn_indexes
            else:
                raise ValueError(f"Can't infer index for variable of len {len(values)}")

        full_val_arr = np.full(self.n_rois, np.nan)
        full_val_arr[indexes] = values
        return color_stack(self.rois_stack, variable=full_val_arr, **kwargs)
