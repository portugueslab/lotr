import numpy as np


def get_pi_labels(d=1, coefs=None, ax="x", style="notex"):
    """Handy way to generate labels for plots with radiants.
    Ugly numerical keys in dictionary, but should not give troubles.
    """
    coefs_mapping = {2: (-1, 1), 1: (-1, 0, 1), 0.5: (-1, -0.5, 0, 0.5, 1)}

    labels_mappings = {
        "tex": {
            -2: "$-2π$",
            -1: "$-π$",
            -0.75: r"$\dfrac{-3π}{4}$",
            -0.5: r"$\dfrac{-π}{2}$",
            -1 / 3: r"$\dfrac{-π}{3}$",
            -0.25: r"$\dfrac{-π}{4}$",
            0: "0",
            0.25: r"$\dfrac{π}{4}$",
            1 / 3: r"$\dfrac{π}{3}$",
            0.5: r"$\dfrac{π}{2}$",
            0.75: r"$\dfrac{3π}{4}$",
            1: "$π$",
            2: "$2π$",
        },
        "notex": {
            -2: "-2π",
            -1: "-π",
            -0.75: "-3/4π",
            -0.5: "-π/2",
            -1 / 3: "-π/3",
            -0.25: "-π/4",
            0: "0",
            0.25: r"π/4",
            1 / 3: "π/3",
            0.5: "π/2",
            0.75: "3π/4",
            1: "π",
            2: "2π",
        },
    }

    if coefs is None:
        coefs = coefs_mapping[d]

    ticks = []
    tick_labels = []
    for i in coefs:
        ticks.append(i * np.pi)
        tick_labels.append(labels_mappings[style][i])
    tickname = ax + "ticks"
    labname = ax + "ticklabels"
    return {tickname: ticks, labname: tick_labels}
