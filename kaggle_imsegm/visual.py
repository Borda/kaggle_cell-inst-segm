import os
from typing import Sequence

import numpy as np
import pandas as pd

from matplotlib import patches, pyplot as plt
from matplotlib.path import Path
from skimage import color

from kaggle_imsegm.data import create_cells_instances_mask


def show_cells_image_annot(img_name: str, df_train: pd.DataFrame, img_folder: str):
    df_img = df_train[df_train["id"] == img_name]
    path_img = os.path.join(img_folder, f"{img_name}.png")
    img = plt.imread(path_img)
    mask = create_cells_instances_mask(df_img)
    fig, axarr = plt.subplots(ncols=3, figsize=(14, 6))
    axarr[0].imshow(img)
    axarr[1].imshow(img)
    axarr[1].contour(mask, levels=np.unique(mask).tolist(), cmap="inferno", linewidths=0.5)
    axarr[2].imshow(mask, cmap="inferno", interpolation="antialiased")
    return fig


def _draw_line(ax, coords: Sequence[tuple], clr: str = "g") -> None:
    line = Path(coords, [Path.MOVETO, Path.LINETO])
    pp = patches.PathPatch(line, linewidth=3, edgecolor=clr, facecolor="none")
    ax.add_patch(pp)


def _set_axes_labels(ax, axes_x: str, axes_y: str) -> None:
    ax.set_xlabel(axes_x)
    ax.set_ylabel(axes_y)
    ax.set_aspect("equal", "box")


def show_tract_volume(vol: np.ndarray, segm: np.ndarray, z: int, y: int, x: int, fig_size=(9, 9)) -> None:
    fig, axarr = plt.subplots(nrows=2, ncols=2, figsize=fig_size)
    v_z, v_y, v_x = vol.shape
    # axarr[0, 0].imshow(vol[x, :, :], cmap="gray", vmin=0, vmax=255)
    # axarr[0, 1].imshow(vol[:, :, z], cmap="gray", vmin=0, vmax=255)
    # axarr[1, 0].imshow(vol[:, y, :], cmap="gray", vmin=0, vmax=255)
    axarr[0, 0].imshow(color.label2rgb(segm[z, :, :], vol[z, :, :]))
    axarr[0, 0].add_patch(patches.Rectangle((-1, -1), v_x, v_y, linewidth=5, edgecolor="r", facecolor="none"))
    _draw_line(axarr[0, 0], [(x, 0), (x, v_y)], "g")
    _draw_line(axarr[0, 0], [(0, y), (v_x, y)], "b")
    _set_axes_labels(axarr[0, 0], "X", "Y")
    axarr[0, 1].imshow(color.label2rgb(segm[:, :, x].T, vol[:, :, x].T))
    axarr[0, 1].add_patch(patches.Rectangle((-1, -1), v_z, v_y, linewidth=5, edgecolor="g", facecolor="none"))
    _draw_line(axarr[0, 1], [(z, 0), (z, v_y)], "r")
    _draw_line(axarr[0, 1], [(0, y), (v_x, y)], "b")
    _set_axes_labels(axarr[0, 1], "Z", "Y")
    axarr[1, 0].imshow(color.label2rgb(segm[:, y, :], vol[:, y, :]))
    axarr[1, 0].add_patch(patches.Rectangle((-1, -1), v_x, v_z, linewidth=5, edgecolor="b", facecolor="none"))
    _draw_line(axarr[1, 0], [(0, z), (v_x, z)], "r")
    _draw_line(axarr[1, 0], [(x, 0), (x, v_y)], "g")
    _set_axes_labels(axarr[1, 0], "X", "Z")
    axarr[1, 1].set_axis_off()
    fig.tight_layout()