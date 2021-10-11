"""Coloring code adapted from Vilim's notebook_utilities.stack_coloring
and motions.color.
"""
import colorspacious
import matplotlib
import numpy as np
from matplotlib import cm, collections, colors
from matplotlib import pyplot as plt
from numba import njit
from svgpath2mpl import parse_path

COLS = dict(
    sides=dict(
        lf=(0.0, 0.62352941, 0.88627451), rt=(0.83529412, 0.36470588, 0.28235294)
    ),
    dff_img="Greens",
    beh=(0.4,) * 3,
)


def dark_col(col, val=0.2):
    return [max(0, c - val) for c in col]


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


def add_cbar(
    col_ax,
    ref_plot,
    label="",
    ticks=None,
    ticklabels=None,
    tick_visible=False,
    labelsize=None,
    titlesize=10,
    **kwargs,
):
    """Add properly edited colorbar to plot."""
    if isinstance(col_ax, tuple) or isinstance(col_ax, list):
        col_ax = plt.gcf().add_axes(col_ax)
    cbar = plt.colorbar(ref_plot, cax=col_ax, **kwargs)
    cbar.ax.set_title(label, fontsize=titlesize)
    cbar.set_ticks(ticks)

    if not tick_visible:
        cbar.ax.tick_params(size=0.0)
        cbar.outline.set_visible(False)
    if ticklabels is not None:
        cbar.set_ticklabels(ticklabels)

    if labelsize is not None:
        cbar.ax.tick_params(labelsize=labelsize)

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
    dummy_scatter = ax.scatter(
        [None], [None], vmin=vlims[0], vmax=vlims[1], c=[None], cmap=cmap
    )
    for i in range(1, len(x)):
        ax.plot(x[i - 1 : i + 1], y[i - 1 : i + 1], c=cmap_fun(norm(c[i])), **kwargs)

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


def add_scalebar(
    ax=None,
    xlen=None,
    ylen=None,
    xpos=None,
    ypos=None,
    xunits=None,
    yunits=None,
    xlabel=None,
    ylabel=None,
    line_params=None,
    text_params=None,
    disable_axis=True,
    line_spacing_coef=0.1,
    text_spacing_coef=0.06,
):
    """Function to add a scale bar to an existing plot. Currently implemented only
    for both axes.

    Parameters
    ----------
    ax : plt.Axis obj
        The target axis for the scalebar. If none, get current (default=None).
    xlen : Int or Float
        Extension of the bar in x.
    ylen : int or float
        Extension of the bar in y.
    xpos : int or float
        Position of the bar in x.
    ypos : int or float
        Position of the bar in y.
    xunits : str
        Units of the x axis, added after number in label (default=None).
    yunits : str
        Units of the x axis, added after number in label (default=None).
    xlabel : str
        Label over the x axis. Overrides the standard '{number} {units}' (default=None).
    ylabel : str
        Label over the y axis. Overrides the standard '{number} {units}' (default=None).
    line_params : dict
        Dictionary of parameters for the plt.plot function for the line (default=None).
    text_params : dict
        Dictionary of parameters for the plt.txt adding the labels (default=None).
    disable_axis : bool
        Flag to hide the orgiginal axis after the colorbar is added (default=True).
    line_spacing_coef : float
        Spacing between minimum point on the plot and the bar, as a fraction of the
        data extension over that axis (default: 0.1).
    text_spacing_coef : float
        Spacing between the bar and the labels, as a fraction of the bar length (default: 0.06).


    """

    if ax is None:
        ax = plt.gca()

    line_params_def = dict(lw=1, c=(0.3,) * 3)
    text_params_def = dict(fontsize=10)

    for default_params, params_in in zip(
        [line_params_def, text_params_def], [line_params, text_params]
    ):
        if params_in is not None:
            default_params.update(params_in)

    if xlen is None:
        xlen = ax.xaxis.get_ticklocs()[1] - ax.xaxis.get_ticklocs()[0]
    if ylen is None:
        ylen = ax.yaxis.get_ticklocs()[1] - ax.yaxis.get_ticklocs()[0]

    plot_data_lims = (
        ax.dataLim.min - (ax.dataLim.max - ax.dataLim.min) * line_spacing_coef
    )
    if xpos is None:
        xpos = plot_data_lims[0]
    if ypos is None:
        ypos = plot_data_lims[1]

    if xlabel is None:
        xlabel = f"{xlen}" if xunits is None else f"{xlen} {xunits}"
    if ylabel is None:
        ylabel = f"{ylen}" if yunits is None else f"{ylen} {yunits}"

    ax.plot([xpos, xpos, xpos + xlen], [ypos + ylen, ypos, ypos], **line_params_def)
    ax.text(
        xpos - xlen * text_spacing_coef,
        ypos + ylen / 2,
        ylabel,
        ha="right",
        va="center",
        rotation="vertical",
        **text_params_def,
    )
    ax.text(
        xpos + xlen / 2,
        ypos - ylen * text_spacing_coef,
        xlabel,
        ha="center",
        va="top",
        **text_params_def,
    )

    if disable_axis:
        ax.axis("off")


def add_fish(ax, offset=(0, 0), scale=1):
    path_fish = "m0 0c-13.119 71.131-12.078 130.72-12.078 138.78-5.372 8.506-3.932 18.626-3.264 23.963-6.671 1.112-2.891 4.002-2.891 5.114s-2.224 8.005.445 9.116c-.223 3.113.222 0 0 1.557-.223 1.556-3.558 3.558-2.891 8.227.667 4.67 3.558 10.228 6.226 9.784 2.224 4.892 5.559 4.669 7.56 4.447 2.001-.223 8.672-.445 10.228-6.004 5.115-1.556 5.562-4.002 5.559-6.67-.003-3.341.223-8.45-3.113-12.008 3.336-4.224.667-13.786-3.335-13.786 1.59-8.161-2.446-13.786-3.558-20.679-2.223-34.909-.298-102.74 1.112-141.84"
    path = parse_path(path_fish)
    min_p = np.min(path.vertices, 0)
    path.vertices -= min_p
    f = np.abs(path.vertices[:, 1]).max() * scale
    path.vertices[:, 0] = path.vertices[:, 0] / f
    path.vertices[:, 1] = path.vertices[:, 1] / f

    path.vertices += np.array(offset)

    collection = collections.PathCollection(
        [path], linewidths=0, facecolors=["#909090"]
    )
    ax.add_artist(collection)


def get_circle_xy(circle_params):
    """Compute array of x's and y's for plotting a circle, from circle fit parameters."""
    if len(circle_params) == 4:
        xpos, ypos, radius, _ = circle_params
    else:
        xpos, ypos, radius = circle_params
    SPACING = 0.05
    th = np.arange(0, 2 * np.pi + SPACING, SPACING)

    return np.cos(th) * radius + xpos, np.sin(th) * radius + ypos


def _jch_to_rgb255(x):
    output = np.clip(colorspacious.cspace_convert(x, "JCh", "sRGB1"), 0, 1)
    return (output * 255).astype(np.uint8)


@njit
def _fill_roi_stack(
    rois,
    roi_colors,
    background=np.array(
        [
            0,
        ]
        * 4
    ),
):
    coloured = np.zeros(rois.shape + (roi_colors.shape[1],), dtype=roi_colors.dtype)
    for i in range(rois.shape[0]):
        for j in range(rois.shape[1]):
            for k in range(rois.shape[2]):
                if rois[i, j, k] > -1:
                    coloured[i, j, k] = roi_colors[rois[i, j, k], :]
                else:
                    coloured[i, j, k] = background[: roi_colors.shape[1]]
    return coloured


def _get_n_colors(n_cols, lum=60, sat=60, hshift=0):
    return _jch_to_rgb255(
        np.stack(
            [
                np.full(n_cols, lum),
                np.full(n_cols, sat),
                (-np.arange(0, 360, 360 / n_cols) + hshift),
            ],
            1,
        )
    )


def _color_anatomy_rgb(rois, roi_colors, anatomy, alpha=0.9, invert_anatomy=True):
    """Colours a new stack of zeros with ROI colors

    :param rois: the ROI stack
    :param roi_colors: colors for each ROI
    :param anatomy: anatomy stack
    :param alpha: alpha of the ROI coloring
    :return:
    """
    colored_rois = _fill_roi_stack(
        rois,
        roi_colors,
        background=np.array(
            [
                0,
            ]
            * 4
        ),
    )
    overimposed = np.concatenate(
        [
            anatomy[:, :, :, np.newaxis],
        ]
        * 3,
        3,
    )

    if invert_anatomy:
        overimposed = 255 - overimposed

    overimposed[rois > -1] = overimposed[rois > -1] * (1 - alpha)
    overimposed = overimposed + colored_rois * alpha

    return overimposed.astype(np.uint8)


def _get_categorical_colors(variable, color_scheme=None, lum=60, sat=60, hshift=0):
    if color_scheme is None:
        unique_vals = np.unique(variable[variable >= 0])
        colors = _get_n_colors(len(unique_vals), lum=lum, sat=sat, hshift=hshift)
        color_scheme = {v: colors[i] for i, v in enumerate(unique_vals)}

    color_scheme[-1] = np.array([0, 0, 0])

    roi_colors = np.array([color_scheme[v] for v in variable])

    return np.concatenate([roi_colors, np.full((len(variable), 1), 255)], 1)


def _get_continuous_colors(variable, color_scheme=None, vlims=None):
    if color_scheme is None:
        color_scheme = "viridis"

    if vlims is None:
        vlims = np.nanmin(variable), np.nanmax(variable)

    # cmap function:
    cmap_fun = (
        color_scheme if callable(color_scheme) else matplotlib.cm.get_cmap(color_scheme)
    )

    # normalization function:
    norm = matplotlib.colors.Normalize(vmin=vlims[0], vmax=vlims[1])

    return (np.array([cmap_fun(norm(v)) for v in variable]) * 255).astype(np.uint8)


def _normalize_to_255(stack, hist_percentiles=(5, 99)):
    hist_boundaries = [np.percentile(stack, p) for p in hist_percentiles]
    stack = stack - hist_boundaries[0]
    stack = (stack / hist_boundaries[1]) * 255
    stack[stack < 0] = 0
    stack[stack > 255] = 255

    return stack


def color_stack(
    rois,
    variable,
    color_scheme=None,
    anatomy=None,
    categorical=None,
    background="transparent",
    vlims=None,
    lum=60,
    sat=60,
    hshift=0,
    alpha=0.9,
    invert_anatomy=True,
    hist_percentiles=None,
):
    """
    Parameters
    ----------
    rois : 3D np.array
        stack of ROIs (fimpy convention: -1 in empty voxels)

    variable : 1D np.array
        An array of length==n_rois based on which colors stack will be colored.
        If it contains integers, we'll assume the variable is categorical
        unless specified otherwise with the `categorical` parameter.
        ROIs can be excluded from the coloring by setting their value to -1
        (for categorical variables) or to np.nan (for non categorical variables).

    categorical : bool (optional)
        If true, variable will be treated as categorical (normally inferred
        from `variable`).

    color_scheme : str or dict (optional)
        Depending on the variable:
            - categorical: dictionary with the mapping [i] = np.array([r, g, b]).
                By default, a set of constant luminance and saturation colors will be
                generated.
            - non categorical: string specifying a matplotlib color palette.
                By default, viridis will be used.

    anatomy : 3D numpy array (optional)
        If specified, ROIs will be overimposed on it, with tht specified the `alpha`

    background : str or np.array (optional)
        Filling for the empty voxels. Default options are "w", "k" and "transparent".

    vlims : tuple or list (optional)
        Limits for the colormap (used only for non-categorical variable).

    lum : int (optional)
        Luminance for the generation of the categories colors, from 0 to 100
        (used only for categorical variable).

    sat : int (optional)
        Saturation for the generation of the categories colors, from 0 to 100
        (used only for categorical variable).

    hshift : int (optional)
        Hue shift for the generation of the categories colors, from 0 to 360
        (used only for categorical variable).

    alpha : float (optional)
        Alpha value for the overlapping of anatomy and ROIs, from 0 to 1. Default 0.9.

    invert_anatomy : bool (optional)
        If True, anatomy will be inverted (black signal on white background).
        Default True.

    hist_percentiles : tuple (optional)
        Range used for the normalization of the anatomy histogram, if anatomy is not
        already scaled. Default (5, 99)

    Returns
    -------

    """

    BACKGROUNDS = dict(
        k=np.array([0, 0, 0, 255]),
        transparent=np.array(
            [
                0,
            ]
            * 4
        ),
        w=np.array(
            [
                255,
            ]
            * 4
        ),
    )

    # We infer if the variable is categorical or not:
    if categorical is None:
        categorical = np.issubdtype(np.array(variable).dtype, np.integer)

    if categorical:
        # Esclude from the stack rois with nan variable, using the filling function
        # TODO refactor together this and the non categorical condition
        if (variable < 0).any():
            print("excluding")
            nan_filling = np.arange(rois.max() + 1)[:, np.newaxis]
            nan_filling[np.argwhere(variable < 0)[:, 0], :] = -1
            rois = _fill_roi_stack(rois, nan_filling, background=np.array([[-1]]))[
                :, :, :, 0
            ]

        # get roi colors:
        roi_colors = _get_categorical_colors(
            variable, color_scheme=color_scheme, lum=lum, sat=sat, hshift=hshift
        )

    else:
        # Esclude from the stack rois with nan variable, using the filling function:
        if np.isnan(variable).any():
            nan_filling = np.arange(rois.max() + 1)[:, np.newaxis]
            nan_filling[np.argwhere(np.isnan(variable))[:, 0], :] = -1
            rois = _fill_roi_stack(rois, nan_filling, background=np.array([[-1]]))[
                :, :, :, 0
            ]
        # get roi colors:
        roi_colors = _get_continuous_colors(
            variable, color_scheme=color_scheme, vlims=vlims
        )

    if isinstance(background, str):
        background = BACKGROUNDS[background]

    if anatomy is None:
        return _fill_roi_stack(rois, roi_colors, background=background)
    else:
        # If required, normalize the anatomy stack:
        if hist_percentiles is not None or anatomy.max() > 255 or anatomy.min() < 0:
            if hist_percentiles is None:
                hist_percentiles = (5, 99)

            anatomy = _normalize_to_255(anatomy, hist_percentiles=hist_percentiles)

        return _color_anatomy_rgb(
            rois,
            roi_colors[:, :3],
            anatomy.astype(np.uint8),
            alpha=alpha,
            invert_anatomy=invert_anatomy,
        )
