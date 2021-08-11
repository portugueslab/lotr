from matplotlib import pyplot as plt
from matplotlib import collections, cm, colors
import numpy as np
from svgpath2mpl import parse_path


def add_cbar(col_ax, ref_plot, label="", ticks=None,
             ticklabels=None, tick_visible=False,
             **kwargs):
    """Add properly edited colorbar to plot.
    """
    if isinstance(col_ax, tuple) or isinstance(col_ax, list):
        col_ax = plt.gcf().add_axes(col_ax)
    cbar = plt.colorbar(ref_plot, cax=col_ax, **kwargs)
    cbar.ax.set_title(label)
    cbar.set_ticks(ticks)

    if not tick_visible:
        cbar.ax.tick_params(size=0.)
        cbar.outline.set_visible(False)
    if ticklabels is not None:
        cbar.set_ticklabels(ticklabels)

    return cbar


def color_plot(x, y, ax=None, c=None, vlims=None, cmap="twilight", **kwargs):
    """Line plot with a colormap. It works by plotting many
    different segments with different colors, so way
    less efficient than normal plotting.
    Slow with traces > 10k points.
    """
    if ax is None:
        ax = plt.gca()

    if c is None:
        c = np.arange(len(x)) / len(x)
    else:
        c = c

    if vlims is None:
        vlims = np.nanmin(c), np.nanmax(c)

    cmap_fun = cm.get_cmap(cmap)
    norm = colors.Normalize(vmin=vlims[0], vmax=vlims[1])

    # Required for stupid matplotlib to create a usable palette
    dummy_scatter = ax.scatter([None], [None], vmin=vlims[0], vmax=vlims[1], c=[None],
                               cmap=cmap)
    for i in range(1, len(x)):
        ax.plot(x[i - 1:i + 1], y[i - 1:i + 1], c=cmap_fun(norm(c[i])), **kwargs)

    return dummy_scatter


def despine(ax, sides=["right", "top"], rmticks=True):
    if sides == "all":
        sides = ["right", "top", "left", "bottom"]
    if rmticks:
        if sides == "all":
            ax.set(xticks=[], yticks=[])
        if "left" in sides:
            ax.set(yticks=[])
        if "bottom" in sides:
            ax.set(xticks=[])
    [ax.axes.spines[s].set_visible(False) for s in sides]


def add_fish(ax, offset=(0, 0), scale=1):
    path_fish = 'm0 0c-13.119 71.131-12.078 130.72-12.078 138.78-5.372 8.506-3.932 18.626-3.264 23.963-6.671 1.112-2.891 4.002-2.891 5.114s-2.224 8.005.445 9.116c-.223 3.113.222 0 0 1.557-.223 1.556-3.558 3.558-2.891 8.227.667 4.67 3.558 10.228 6.226 9.784 2.224 4.892 5.559 4.669 7.56 4.447 2.001-.223 8.672-.445 10.228-6.004 5.115-1.556 5.562-4.002 5.559-6.67-.003-3.341.223-8.45-3.113-12.008 3.336-4.224.667-13.786-3.335-13.786 1.59-8.161-2.446-13.786-3.558-20.679-2.223-34.909-.298-102.74 1.112-141.84'
    path = parse_path(path_fish)
    min_p = np.min(path.vertices, 0)
    path.vertices -= min_p
    f = np.abs(path.vertices[:, 1]).max() * scale
    path.vertices[:, 0] = path.vertices[:, 0] / f
    path.vertices[:, 1] = path.vertices[:, 1] / f

    path.vertices += np.array(offset)

    collection = collections.PathCollection([path],
                                            linewidths=0,
                                            facecolors=["#909090"])
    ax.add_artist(collection)