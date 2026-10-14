# -*- coding: utf-8 -*-
"""Render gallery/swatch-<id>.png strips for the README table.

Run:  python tools/gen_swatch_strips.py
"""

import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

import sci_palettes as sp  # noqa: E402

OUT = os.path.join(ROOT, "gallery")
os.makedirs(OUT, exist_ok=True)

for pid in sp.names():
    cols = sp.palette(pid)
    n = len(cols)
    fig, ax = plt.subplots(figsize=(n * 0.42, 0.30))
    ax.set_xlim(0, n)
    ax.set_ylim(0, 1)
    ax.axis("off")
    for i, c in enumerate(cols):
        ax.add_patch(FancyBboxPatch(
            (i + 0.02, 0.06), 0.96, 0.88,
            boxstyle="round,pad=0,rounding_size=0.10",
            linewidth=0, facecolor=c))
    fig.subplots_adjust(0, 0, 1, 1)
    path = os.path.join(OUT, f"swatch-{pid}.png")
    fig.savefig(path, dpi=200, transparent=False)
    plt.close(fig)
    print("wrote", path)
