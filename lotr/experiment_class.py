from pathlib import Path

import flammkuchen as fl
from bouter import EmbeddedExperiment


class LotrExperiment(EmbeddedExperiment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scope_config = self["imaging"]["microscope_config"]

        self._dt_imaging = None
        self._resolution = None
        self._n_planes = None
        self._data_shape = None
        self._fn = None
        self._bouts_df = None
        self._traces = None
        self._hdn_indexes = None

    @property
    def fn(self):
        if self._fn is None:
            self._fn = self.scope_config["lightsheet"]["scanning"]["z"]["frequency"]
        return self._fn

    @property
    def dt_imaging(self):
        return 1 / self.fn_imaging

    @property
    def dir_name(self):
        return self.root.name

    @property
    def bouts_df(self):
        if self._bouts_df is None:
            self._bouts_df = fl.load(self.root / "bouts_df.h5")
        return self._bouts_df

    @property
    def traces(self):
        if self._traces is None:
            self._traces = fl.load(self.root / "filtered_traces.h5", "/detr")
        return self._traces

    @property
    def hdn_indexes(self):
        if self._hdn_indexes is None:
            self._hdn_indexes = fl.load(self.root / "selected.h5")
        return self._hdn_indexes

    @property
    def n_pts(self):
        return self.traces.shape[0]

    @property
    def n_rois(self):
        return self.traces.shape[1]

    @property
    def has_hdn(self):
        return (self.root / "selected.h5").exists()  # self.traces.shape[1]

    def find_mirror_dir(self, parent_folder):
        """Find homonym directory in a new parent folder, for file mirroring."""
        parent_folder = Path(parent_folder)
        matches = list(parent_folder.rglob(self.dir_name))
        if len(matches) > 1:
            raise OSError("Multiple folders found for this experiment")
        return matches[0]
