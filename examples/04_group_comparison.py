# -*- coding: utf-8 -*-
"""Group-comparison figure: how many colours to take from a ramp, and how to
add redundant (non-colour) encoding so the figure survives greyscale printing
and colour-vision deficiency.

Run:  python examples/04_group_comparison.py [outdir]
"""

import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import sci_palettes as sp  # noqa: E402

OUTDIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "gallery")
os.makedirs(OUTDIR, exist_ok=True)

sp.set_theme("indigo")
rng = np.random.default_rng(11)

fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.5))
fig.subplots_adjust(wspace=0.42, bottom=0.28)

# a - shrinking the ramp correctly: consecutive colours, never strided
ax = axes[0]
groups = ["WT", "OE-1", "OE-2", "KO"]
cols4 = sp.select(sp.palette("indigo"), 4)
data = [rng.normal(m, 0.9, 40) for m in (4.0, 6.2, 5.6, 2.4)]
for i, (d, c) in enumerate(zip(data, cols4)):
    jitter = rng.normal(i, 0.07, d.size)
    ax.scatter(jitter, d, s=6, color=c, alpha=0.8, edgecolor="white", linewidth=0.2)
    ax.hlines(d.mean(), i - 0.26, i + 0.26, color="#222222", lw=1.1)
ax.set_xticks(range(4)); ax.set_xticklabels(groups)
ax.set_ylabel("Expression (a.u.)")
ax.set_title("a  4 groups from one ramp", loc="left", fontweight="bold")
ax.text(0.02, 0.98, "use sp.select(sp.palette(pid), 4)", transform=ax.transAxes,
        fontsize=5.5, va="top", color="#666666")

# b - redundant encoding: colour + marker + linestyle
ax = axes[1]
x = np.linspace(0, 10, 50)
styles = [("-", "o"), ("--", "s"), ("-.", "^"), (":", "D")]
cols4b = sp.select(sp.palette("indigo"), 4)
for i, ((ls, mk), c) in enumerate(zip(styles, cols4b)):
    y = 1 + 0.5 * i + np.sin(x - i) * 0.4 + rng.normal(0, 0.06, x.size)
    ax.plot(x, y, ls, color=c, lw=1.0, marker=mk, markevery=7, ms=2.8,
            markerfacecolor=c, label=f"Model {chr(65+i)}")
ax.set_xlabel("Time (h)"); ax.set_ylabel("Response (a.u.)")
ax.legend(fontsize=5.5, ncol=2)
ax.set_title("b  Redundant encoding", loc="left", fontweight="bold")

# c - the same panel as a colour-vision-deficient reader sees it
ax = axes[2]
sim = sp.simulate_cvd(cols4b, sp.DEUTERANOPIA)
for i, ((ls, mk), c) in enumerate(zip(styles, sim)):
    y = 1 + 0.5 * i + np.sin(x - i) * 0.4 + rng.normal(0, 0.06, x.size)
    ax.plot(x, y, ls, color=c, lw=1.0, marker=mk, markevery=7, ms=2.8,
            markerfacecolor=c, label=f"Model {chr(65+i)}")
ax.set_xlabel("Time (h)"); ax.set_ylabel("Response (a.u.)")
ax.legend(fontsize=5.5, ncol=2)
ax.set_title("c  Deuteranopia preview", loc="left", fontweight="bold")

out = os.path.join(OUTDIR, "group_comparison_indigo.png")
fig.savefig(out, dpi=300)
print("wrote", out)
print("\n" + sp.report("indigo"))
