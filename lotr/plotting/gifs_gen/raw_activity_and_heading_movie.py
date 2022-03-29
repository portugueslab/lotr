import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import cm
from pathlib import Path

from lotr import A_FISH, LotrExperiment
from lotr.file_utils import get_figures_location
from lotr.pca import pca_and_phase
from lotr.plotting import  add_scalebar, despine
from lotr.rpca_calculation import get_zero_mean_weights
from lotr.utils import convolve_with_tau

from lotr.plotting.gifs_gen.gif_utils import make_proj


def rot_coords(contour, alpha):
    return (
        np.array([[np.cos(alpha), np.sin(alpha)], [-np.sin(alpha), np.cos(alpha)]])
        @ contour.T
    ).T

contour = rot_coords(np.load(str(Path(__file__).parent.parent / "assets" / "fish_contour.npy")), np.pi/2)
contour[:, 0] *= -1
contour[:, 0] -= 0.15


def network_phase_animation(dest=None, frames=None):
    if frames is None:
        frames = list(range(0, 4000, 5))
    if dest is None:
        dest = (
            get_figures_location()
            / f"orientation_and_bump_t{frames[0]}-{frames[-1]}+{frames[1]}.mp4"
        )
    # Data preparation
    # ----------------
    # Compute quantities to plot:
    exp = LotrExperiment(A_FISH)
    pca_scores_t, roi_pc_angles, _, circle_params = pca_and_phase(
        exp.traces[:, exp.hdn_indexes].T
    )
    pca_scores_t[:, :2] = pca_scores_t[:, :2] - circle_params[:2]

    norm_activity = get_zero_mean_weights(exp.traces[:, exp.hdn_indexes].T).T
    # avg_vects = np.einsum("ij,ik->jk", norm_activity.T, pca_scores_t[:, :2])

    network_phase = convolve_with_tau(exp.fictive_heading, 5) # get_vect_angle(avg_vects.T)

    # Plot parameters
    # ---------------
    scale_mn = 1
    w_lw, netw_lw = 0.3, 1.5
    w_c = (0.7,) * 3
    colmap = cm.get_cmap("coolwarm")

    # Figure
    # ------
    # Prepare figure globals:
    fig, axs = plt.subplots(1, 2, figsize=(6, 3))
    ax = axs[0]
    ax_bump = axs[1]

    # Timestamp:
    tx = ax.text(-100, 100, "t = 0 s", fontsize=8)

    add_scalebar(ax, xlabel="rPC1", ylabel="rPC2", xlen=30, ylen=30)

    # Network average:
    (network_phase_plot,) = ax.plot(
        [],
        [],
        c=w_c,
        lw=netw_lw,
        label="virtual orientation",
        solid_capstyle="round",
        zorder=-100
    )

    # Legend:
    leg = ax.legend(fontsize=8, frameon=False, bbox_to_anchor=(0.95, 1.1, 0.2, 0.04))
    # leg_line = leg.get_lines()


    ## Raw bump
    selected = exp.hdn_indexes
    rois_stack = exp.rois_stack

    im = ax_bump.imshow(
        make_proj(rois_stack, exp.traces, selected, 0),
        origin="lower",
        cmap="gray",
        vmin=-0.5,
        vmax=0.3,
    )
    # ax.contour(proj[:, :, 0] > 0, levels=1, colors=[COLS["ring"]], linewidths=1)

    tx = ax.text(70, 10, f"{0 / 5:3.0f} s", ha="right", c="w")

    (fish,) = ax.fill(contour[:, 0], contour[:, 1], fc=".6", lw=0, zorder=100)

    # put together all actors:
    actors = (tx, network_phase_plot, im, fish)

    def init():
        # For some mysterious reasons, some of those specifications need to happen
        # in the init. Therefore, we put here a whole bunch of them:
        ax.axis("equal")

        im.set_clim(-0.2, 0.5)
        im.set_zorder(-1000)
        # cbar.outline.set_visible(False)

        ax_bump.set_xlabel("left - right")
        ax_bump.set_ylabel("posterior - anterior")
        despine(ax_bump, "all")
        despine(ax, "all")

        return actors

    def update(frame):
        tx.set_text(f"{frame / exp.fs:3.0f} s")
        network_phase_plot.set_data(
            [0, -np.cos(network_phase[frame]) * scale_mn],
            [0, np.sin(network_phase[frame]) * scale_mn],
        )
        new_col = colmap(network_phase[frame] - network_phase[frame-1] + 0.5)  # get_default_phase_col(network_phase[frame])
        # for line in network_phase_plot, leg_line:
        network_phase_plot.set_color(new_col)
        im.set_data(make_proj(rois_stack, exp.traces, selected, frame))
        ax.set(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5))

        fish.set_xy(rot_coords(contour, network_phase[frame]))

        return actors

    ani = FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=50,
        init_func=init,
        blit=True,
    )
    ani.save(dest, dpi=300)

    return fig


if __name__ == "__main__":
    dest = get_figures_location() / "gifs"
    dest.mkdir(exist_ok=True)
    network_phase_animation(frames=list(range(0, 2000, 2)))
