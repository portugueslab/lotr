import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pathlib import Path
import flammkuchen as fl
import seaborn as sns
from bouter import EmbeddedExperiment

sns.set(style="ticks", palette="deep")
cols = sns.color_palette()


plt.rcParams["figure.constrained_layout.use"] = True
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Libertinus Sans"]


path = Path("/Users/luigipetrucco/Desktop/rf_natmov_sourcedata/210314_f1_natmov")
# path = Path("/Users/luigipetrucco/Desktop/rf_v13_cw_ccw_sourcedata/210312_f2")

exp = EmbeddedExperiment(path)
df = exp.get_bout_properties()

data = fl.load(path / "pca_data.h5")
theta = data["theta"]
roi_stack = data["roi_stack"]
pcaed = data["pcaed"]
traces = data["traces"]
selected = data["selected"]

t_left = np.zeros(5000)
t_right = np.zeros(5000)
idx_l = (
    df.loc[(df["bias"] > 0.5) & (df["t_start"] < 1000), "t_start"].values * 5
).astype(np.int)
for i in idx_l:
    t_left[i : i + 4] = 1

idx_r = (
    df.loc[(df["bias"] < -0.5) & (df["t_start"] < 1000), "t_start"].values * 5
).astype(np.int)
for i in idx_r:
    t_right[i : i + 4] = 1


n_tps = len(theta)
n_trail = 15


def make_proj(roi_stack, traces, idxs, t):
    mask = np.zeros(roi_stack.shape)
    for ind in idxs:
        mask[(roi_stack == ind + 1)] = traces[t, ind]

    return mask.mean(0)


fig = plt.figure(figsize=(9, 4), constrained_layout=True)
axs = [fig.add_axes((0.1, 0.15, 0.4, 0.8)), fig.add_axes((0.42, 0.1, 0.6, 0.9))]
col = fig.add_axes((0.9, 0.4, 0.015, 0.15))

ln = axs[0].scatter(
    [], [], cmap="twilight", vmin=-np.pi, vmax=np.pi, linewidth=0.2, edgecolor="k"
)
im = axs[1].imshow(
    make_proj(roi_stack, traces, np.argwhere(selected), 0).T,
    origin="lower",
    cmap="gray",
    vmin=0.0,
    vmax=0.3,
)
tx = axs[1].text(70, 10, f"{0 / 5:3.0f} s", ha="right", c="w")
sc1 = axs[0].scatter([-4], [5], c="r")
sc2 = axs[0].scatter([4], [5], c="g")

actors = (ln, im, tx, sc1, sc2)

cbar = plt.colorbar(im, cax=col, label="norm. dF")
cbar.set_ticks([])


def init():
    axs[0].plot(pcaed[:n_tps, 0], pcaed[:n_tps, 1], c=(0.6,) * 3, zorder=-100)

    axs[0].axis("equal")
    axs[0].set_xlabel("PC 1")
    axs[0].set_ylabel("PC 2")
    ln.set_clim(-np.pi, np.pi)
    ln.set_cmap("twilight")
    sc1.set_cmap("Reds")
    sc2.set_cmap("Blues")

    im.set_clim(0.2, 0.5)
    im.set_zorder(-1000)
    cbar.outline.set_visible(False)

    axs[1].set_xticks([])
    axs[1].set_yticks([])
    axs[1].set_xlabel("left - right")
    axs[1].set_ylabel("posterior - anterior")
    [
        axs[1].axes.spines[s].set_visible(False)
        for s in ["left", "right", "top", "bottom"]
    ]
    # [axs[0].axes.spines[s].set_visible(False) for s in
    # ["left", "right", "top", "bottom"]]
    sns.despine(trim=True)
    # text = axs[1].text(70, 10, f"{0 / 5:3.0f} s", ha="right")

    return actors


def update(frame):
    tx.set_text(f"{frame / 5:3.0f} s")
    ln.set_offsets(pcaed[frame - n_trail : frame, :2])
    ln.set_sizes(np.arange(1, n_trail) * (20 / n_trail))
    ln.set_array(theta[frame - n_trail : frame])
    sc1.set_sizes(t_left[frame : frame + 1] * 150)
    sc2.set_sizes(t_right[frame : frame + 1] * 150)
    im.set_data(make_proj(roi_stack, traces, np.argwhere(selected), frame).T)
    return actors


ani = FuncAnimation(
    fig,
    update,
    frames=np.arange(n_trail, n_tps, 1),
    interval=50,
    init_func=init,
    blit=True,
)
# plt.show()
ani.save(path / "pca_movie.mp4")
# plt.show()
