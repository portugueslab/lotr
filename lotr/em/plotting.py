import numpy as np
from bg_atlasapi import BrainGlobeAtlas
from matplotlib import pyplot as plt

from lotr.plotting.general import projection_contours


class AtlasPlotter:
    def __init__(
        self,
        atlas_name="ipn_zfish_0.5um",
        structures=None,
        alpha_dict=None,
        projections=None,
    ):
        self.atlas = BrainGlobeAtlas(atlas_name)
        self.space = self.atlas.space

        if structures is None:
            structures = [k for k in self.atlas.structures.keys()]
        self.visible_structures = structures

        if alpha_dict is None:
            alpha_dict = {k: 0.2 for k in self.visible_structures}
        self.alpha_dict = alpha_dict

        # Compute stuff only once:
        self.contours_dict = dict()
        for s in self.visible_structures:
            projection_dict = [self.project_mask(s, p) for p in self.space.sections]
            self.contours_dict[s] = projection_dict

        if projections is None:
            projections = self.space.sections
        self.projections = projections

        self.shape_color = "gray"
        self.shape_linewidth = 0
        self.shape_linecolor = "gray"
        self.shape_alpha = None
        self.shape_fill = True
        self.font_size = 14
        self.custom_switch = None

    def project_mask(self, structure, projection, smooth_wnd=7):
        if type(projection) is str:  # is semantic indication of axis, use space:
            projection = self.space.sections.index(projection)

        mask = self.atlas.get_structure_mask(structure)
        contours = projection_contours(
            mask.max(projection), smooth_wnd=smooth_wnd, thr=0.5
        )

        return contours * self.space.resolution[0]

    def get_switch(self, projection):
        if self.custom_switch is None:
            return 0 if projection == "sagittal" else 1
        else:
            return self.custom_switch[projection]

    def get_bounds(self, projection, edge=115):
        projection_idx = self.space.sections.index(projection)
        swtch = self.get_switch(projection)

        bounds = list()

        pair = self.space.index_pairs[projection_idx]
        for p in pair:
            d = (self.atlas.shape_um[p] - edge) // 2
            bounds.append((d, d + edge))

        return bounds[1 - swtch], bounds[swtch]

    def get_labels(self, projection):
        idx = self.space.sections.index(projection)
        return [["dors.", "right"], ["rostr.", "right"], ["dors.", "caud."]][idx]

    def plot_on_axis(self, ax, projection, title=True, labels=True, edge=115):
        """Prepare background silhouette on a specific axis."""
        projection_idx = self.space.sections.index(projection)
        bs = self.get_bounds(projection, edge=edge)
        swtch = self.get_switch(projection)

        for structure in self.visible_structures:
            cs = self.contours_dict[structure][projection_idx]
            alpha = (
                self.alpha_dict[structure]
                if self.shape_alpha is None
                else self.shape_alpha
            )
            ax.fill(
                cs[:, swtch],
                cs[:, 1 - swtch],
                alpha=alpha,
                facecolor=self.shape_color,
                linewidth=self.shape_linewidth,
                fill=self.shape_fill,
                edgecolor=self.shape_linecolor,
            )

        if labels:
            labels_txt = self.get_labels(projection)
            s = 10
            o = 3
            lw = 1
            col = (0.3,) * 3
            s_px = int(s / self.space.resolution[0])
            ax.plot(
                [bs[1][0] + o, bs[1][0] + s_px + o],
                [bs[0][1] - o, bs[0][1] - o],
                linewidth=lw,
                c=col,
            )
            ax.plot(
                [bs[1][0] + o, bs[1][0] + o],
                [bs[0][1] - o, bs[0][1] - s_px - o],
                linewidth=lw,
                c=col,
            )
            ax.text(
                bs[1][0] + o,
                bs[0][1] - s_px - o * 2,
                labels_txt[0],
                ha="center",
                va="bottom",
                fontsize=self.font_size,
                color=col,
            )
            ax.text(
                bs[1][0] + s_px + o * 2,
                bs[0][1] - o,
                labels_txt[1],
                ha="left",
                va="center",
                fontsize=self.font_size,
                color=col,
            )

        if title:
            ax.set_title(f"{projection} view")
        # if ylabels:
        #     ax.set_ylabel(labels[1 - swtch].lower())
        # if xlabels:
        #     ax.set_xlabel(labels[swtch].lower())

        ax.set_xlim((bs[1][0], bs[1][1]))
        ax.set_ylim((bs[0][1], bs[0][0]))
        ax.set_aspect("equal")
        [
            ax.axes.spines[s].set_visible(False)
            for s in ["left", "right", "top", "bottom"]
        ]

        ax.set_xticks([])
        ax.set_yticks([])

    def plot_neuron_projection(
        self,
        ax,
        neuron,
        projection,
        select="all",
        soma_s=30,
        slice_sel=None,
        soma_lw=0,
        **kwargs,
    ):
        """Plot a neuronal projection an axes."""

        idx = self.space.plane_normals[projection].index(1)
        swtch = self.get_switch(projection)

        cs = neuron.generate_plotlines_from_skeleton(select=select)
        if slice_sel is not None:
            sel = (cs[:, idx] > slice_sel[0]) & (cs[:, idx] < slice_sel[1])
            cs[~sel, :] = np.nan
        cs = np.delete(cs, idx, axis=1)[:, :]

        ax.plot(cs[:, swtch], cs[:, 1 - swtch], **kwargs)
        if neuron.soma_idx is not None and soma_s > 0:
            cs = neuron.coords_ipn[neuron.soma_idx : neuron.soma_idx + 1, :]
            cs = np.delete(cs, idx, axis=1)[:, :]
            scatter_alpha = 1 if "alpha" not in kwargs else kwargs["alpha"]
            ax.scatter(
                cs[:, swtch],
                cs[:, 1 - swtch],
                s=soma_s,
                color=kwargs["color"],
                # color=[c - 0.1 for c in kwargs["color"]],
                alpha=scatter_alpha,
                linewidth=soma_lw,
            )

    def plot_neurons(self, axs, neurons, select="all", **kwargs):
        """Plot neurons projections over a triplet of axs"""
        if type(neurons) is not list:
            neurons = [neurons]

        for neuron in neurons:
            for i, projection in enumerate(self.projections):
                self.plot_neuron_projection(
                    axs[i], neuron, projection, select=select, **kwargs
                )

    def generate_projection_plots(
        self,
        axs=None,
        figsize=(9, 3),
        labels=False,
        title=False,
        tight_layout=False,
        edge=120,
    ):
        """Plot the outline of the IPN structures."""

        if axs is None:
            f, axs = plt.subplots(1, 3, figsize=figsize)
        for i, projection in enumerate(self.projections):
            self.plot_on_axis(axs[i], projection, edge=edge, labels=labels, title=title)

        if tight_layout:
            plt.tight_layout()
