"""
Make wind direction indicator images.

See README.md for info
"""
import math
import os

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow
from matplotlib.collections import PatchCollection
import numpy as np


# Increase for more resolution
NUM_DIRS = 16
# See https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html for more colormaps
CMAP_NAME = "YlOrRd"
OUTPUT_DIR = "pngs"

colormap = plt.get_cmap(CMAP_NAME)


def plot(mag, bearingDeg, fname):
    """Make a single wind direction image."""
    print(f"plotting {mag} {bearingDeg}")
    fig, ax = plt.subplots(figsize=(6, 6))
    for rad in [0.33, 0.66, 1.0]:
        circle = Circle((0, 0), rad, fill=False, ec="black", color="b", alpha=0.1)
        ax.add_patch(circle)

    # Add lines
    for angleI in range(NUM_DIRS):
        theta = angleI * 2 * math.pi / NUM_DIRS
        x = math.cos(theta)
        y = math.sin(theta)
        plt.plot(
            (0, x), (0, y), color="k", alpha=0.1,
        )

    # arrow
    theta = bearingDeg * math.pi / 180.0
    # rotate 90° to have north be up.
    y = math.cos(theta)
    x = math.sin(theta)
    color = colormap(mag)
    # Wind directions are always reported by the bearing of the wind (i.e. where it's
    # coming from)
    # Make a length-2 arrow pointing toward where the wind is coming from.
    # Make bigger and different colors if the wind is extra windy.
    # Tail is specified reflected through the origin
    arrow = FancyArrow(
        -x,
        -y,
        2 * x,
        2 * y,
        color=color,
        width=0.05 + 0.20 * mag,
        length_includes_head=True,
        head_length=2.0,
        ec="black",
        alpha=1.00,
        zorder=100,
    )
    ax.add_patch(arrow)

    plt.axis("equal")
    plt.axis("off")
    # plt.tight_layout()
    plt.margins(0)
    plt.savefig(fname)
    plt.close()


def generate():
    """Generate a series of wind direction images"""
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    for mag, label in [(0.1, "L"), (0.5, "M"), (1.0, "H")]:
        for bearingDeg in np.linspace(0, 360, NUM_DIRS + 1):
            fname = f"{int(bearingDeg)}_{label}"
            plot(mag, bearingDeg, os.path.join(OUTPUT_DIR, fname))


if __name__ == "__main__":
    generate()
