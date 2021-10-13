import numpy as np
from matplotlib import cm, colors
from matplotlib import pyplot as plt


def plot_arrow(seg, ax=None, col="b", alpha=1, s=10, lw=1):
    ax.plot(seg[:, 0], seg[:, 1], lw=lw, c=col, alpha=alpha)
    ax.scatter(seg[0, 0], seg[0, 1], zorder=100, s=s, color=col, alpha=alpha, lw=0)

    ax.arrow(
        seg[-2, 0],
        seg[-2, 1],
        (seg[-1, 0] - seg[-2, 0]),
        (seg[-1, 1] - seg[-2, 1]),
        head_width=1,
        head_length=1.2,
        lw=lw,
        ec=col,
        fc=col,
        zorder=100,
        alpha=alpha,
    )


def boxplot(data, cols=None, ax=None, widths=0.6, ec=(0.3,) * 3):
    """Plot a cleaned-up boxplot for data list.

    Parameters
    ----------
    data : list of arrays
        List of data arrays to boxplot.
    cols : list of len 3 tuples:
        List of colors for each data.
    ax : plt.Axes
        Axes on which to plot.
    widths :
        Widths of the boxes.
    ec :
        Color of the lines.

    Returns
    -------
    plt.BoxPlot
        Boxplot object.

    """
    if ax is None:
        ax = plt.gca()

    if cols is None:
        cols = [
            None,
        ] * len(data)

    bplot = ax.boxplot(
        data,
        notch=False,
        showfliers=False,
        vert=False,
        patch_artist=True,
        showcaps=False,
        widths=widths,
    )

    for patch, med, col in zip(bplot["boxes"], bplot["medians"], cols):
        patch.set(fc=col, lw=1, ec=col)
        med.set(color=ec)

    for whisk in bplot["whiskers"]:
        whisk.set(lw=1, color=ec)

    return bplot


def color_plot(x, y, ax=None, c=None, vlims=None, cmap="twilight", **kwargs):
    """Line plot with a colormap. It works by plotting many
    different segments with different colors, so way
    less efficient than normal plotting.
    Slow with traces > 10k points.

    Parameters
    ----------
    x : np.array
        X array.
    y : np.array
        Y array.
    ax  plt.Axis
        Axis on which to plot (default=current).
    c : np. array (optional)
        If non linear, array to use to map the colormap (default=linear).
    vlims : 2 elements tuple
        Color limits for the color plot
    cmap : str
        Name of the matplotlib colormap to use
    kwargs : dict
        Additional arguments for the plt.plot function.

    Returns
    -------
    plt.ScatterPlot
        Or whatever the class is called. This is a dummy scatterplot to generate a color
        bar.

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
    dummy_scatter = ax.scatter(
        [None], [None], vmin=vlims[0], vmax=vlims[1], c=[None], cmap=cmap
    )
    for i in range(1, len(x)):
        ax.plot(
            x[i - 1 : i + 1],
            y[i - 1 : i + 1],
            c=cmap_fun(norm(c[i])),
            solid_capstyle="round",
            **kwargs,
        )

    return dummy_scatter
