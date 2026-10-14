# -*- coding: utf-8 -*-
"""Colormap gallery: every palette as a smooth ramp, a discrete ramp, and a
mounted contour heatmap - the three ways a palette is used as a colormap.

Run:  python examples/02_colormap_gallery.py [outdir]
"""

import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import sci_palettes as sp  # noqa: E402

OUTDIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "gallery")
os.makedirs(OUTDIR, exist_ok=True)
sp.set_theme("glacier")

IDS = sp.names()
n = len(IDS)
grad = np.linspace(0, 1, 512).reshape(1, -1)

fig = plt.figure(figsize=(7.4, 1.05 * n + 0.6))
gs = fig.add_gridspec(n, 3, width_ratios=[1, 1, 1.1], hspace=0.75, wspace=0.28,
                      left=0.16, right=0.97, top=0.94, bottom=0.04)

x = np.linspace(-3, 3, 200)
y = np.linspace(-3, 3, 200)
XX, YY = np.meshgrid(x, y)
ZZ = np.sin(XX) * np.cos(YY) * np.exp(-(XX ** 2 + YY ** 2) / 8)

for i, pid in enumerate(IDS):
    info = sp.PALETTES[pid]

    ax0 = fig.add_subplot(gs[i, 0])
    ax0.imshow(grad, aspect="auto", cmap=sp.colormap(pid))
    ax0.set_xticks([]); ax0.set_yticks([])
    ax0.set_ylabel(f"{info['name_zh']}\n{pid}", fontsize=7, rotation=0,
                   ha="right", va="center", labelpad=10)

    ax1 = fig.add_subplot(gs[i, 1])
    ax1.imshow(grad, aspect="auto", cmap=ListedColormap(sp.palette(pid)))
    ax1.set_xticks([]); ax1.set_yticks([])

    ax2 = fig.add_subplot(gs[i, 2])
    ax2.contourf(XX, YY, ZZ, levels=12, cmap=sp.colormap(pid))
    ax2.set_xticks([]); ax2.set_yticks([])
    for s in ax2.spines.values():
        s.set_visible(True)

fig.text(0.16, 0.975, "continuous", fontsize=7, color="#555555")
fig.text(0.45, 0.975, "discrete (8)", fontsize=7, color="#555555")
fig.text(0.75, 0.975, "applied to a contour map", fontsize=7, color="#555555")

out = os.path.join(OUTDIR, "colormap_gallery.png")
fig.savefig(out, dpi=300)
print("wrote", out)
