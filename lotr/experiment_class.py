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

    @property
    def fn_imaging(self):
        if self._fn is None:
            self._fn = self.scope_config["lightsheet"]["scanning"]["z"]["frequency"]
        return self._fn

    @property
    def dt_imaging(self):
        return 1 / self.fn_imaging