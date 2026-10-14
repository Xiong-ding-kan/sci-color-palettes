# -*- coding: utf-8 -*-
"""Materials / characterisation style figure (XRD, adsorption, TGA, XPS,
mechanical curves, property map) built on the burgundy palette - the look
most common in materials-science journals.

Run:  python examples/03_materials_figure.py [outdir]
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

sp.set_theme("burgundy")
C = sp.palette("burgundy")
wine, wine_l, slate, slate_l, gold = C[0], C[1], C[4], C[5], C[7]
cmap = sp.colormap("burgundy")

rng = np.random.default_rng(7)
fig, axes = plt.subplots(2, 3, figsize=(7.2, 4.6))
fig.subplots_adjust(hspace=0.55, wspace=0.42)

# a - XRD stacked patterns
ax = axes[0, 0]
tt = np.linspace(10, 80, 1400)
for i, (col, lab) in enumerate(zip([gold, slate, wine_l, wine],
                                   ["Sample A", "Sample B", "Sample C", "Sample D"])):
    peaks = sum(np.exp(-((tt - p) ** 2) / 0.08) for p in
                [18 + i, 27.5, 31.2 + i * 0.4, 45.6, 56.3, 66.1, 75.2])
    noise = rng.normal(0, 0.015, tt.size)
    ax.plot(tt, peaks * 900 + i * 320 + noise * 60, color=col, lw=0.6)
    ax.text(78, i * 320 + 220, lab, fontsize=5.5, ha="right", color="#333333")
ax.set_xlabel("2θ (degree)"); ax.set_ylabel("Intensity (a.u.)")
ax.set_yticks([]); ax.set_title("a  XRD patterns", loc="left", fontweight="bold")

# b - adsorption isotherms
ax = axes[0, 1]
P = np.linspace(0.01, 1, 60)
for col, mk, cap, k in zip([wine, slate, gold], ["o", "s", "^"],
                           ["Material A", "Material B", "Material C"], [22, 14, 7]):
    q = k * 40 * P / (1 + k * P * 0.35)
    ax.plot(P, q, "-", color=col, lw=1.0)
    ax.plot(P[::4], q[::4], mk, color=col, ms=2.2, label=cap)
ax.set_xlabel(r"Relative pressure ($P/P_0$)")
ax.set_ylabel(r"Quantity adsorbed (cm$^3$ g$^{-1}$)")
ax.legend(fontsize=5.5)
ax.set_title("b  Adsorption", loc="left", fontweight="bold")

# c - pore size distribution (filled curves)
ax = axes[0, 2]
d = np.logspace(0, 2, 200)
for col, mu in zip([wine_l, slate, gold], [1.2, 9.0, 32.0]):
    y = np.exp(-((np.log10(d) - np.log10(mu)) ** 2) / 0.09)
    ax.fill_between(d, 0, y, color=col, alpha=0.55, lw=0)
    ax.plot(d, y, color=col, lw=0.8)
ax.set_xscale("log")
ax.set_xlabel("Pore diameter (nm)")
ax.set_ylabel(r"$dV/d\log D$ (cm$^3$ g$^{-1}$)")
ax.set_title("c  Pore distribution", loc="left", fontweight="bold")

# d - TGA
ax = axes[1, 0]
T = np.linspace(25, 800, 300)
for col, lab, drop in zip([wine, slate, gold], ["A", "B", "C"], [0.72, 0.48, 0.24]):
    m = 100 - drop * 100 / (1 + np.exp(-(T - 420) / 70)) - 0.05 * T / 10
    ax.plot(T, m, color=col, lw=1.0, label=f"Sample {lab}")
ax.set_xlabel("Temperature (°C)"); ax.set_ylabel("Mass (%)")
ax.legend(fontsize=5.5)
ax.set_title("d  Thermal analysis", loc="left", fontweight="bold")
# e - mechanical response
ax = axes[1, 1]
strain = np.linspace(0, 16, 200)
for col, lab, E, s_max in zip([wine, wine_l, slate, gold], "ABCD",
                              [150, 110, 55, 30], [12, 11, 15, 18]):
    stress = E * strain * np.exp(-strain / s_max)
    ax.plot(strain, stress, color=col, lw=1.0, label=f"Sample {lab}")
ax.set_xlabel("Strain (%)"); ax.set_ylabel("Stress (MPa)")
ax.legend(fontsize=5.5, ncol=2)
ax.set_title("e  Mechanical response", loc="left", fontweight="bold")

# f - property map
ax = axes[1, 2]
cx = np.linspace(0, 1, 120); cy = np.linspace(200, 800, 120)
CX, CY = np.meshgrid(cx, cy)
Z = np.exp(-((CX - 0.35) ** 2) / 0.05 - ((CY - 350) ** 2) / 40000)
im = ax.imshow(Z, cmap=cmap, origin="lower", aspect="auto",
               extent=[0, 1, 200, 800])
plt.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
ax.set_xlabel("Composition $x$"); ax.set_ylabel("Temperature (°C)")
ax.set_title("f  Property map", loc="left", fontweight="bold")

out = os.path.join(OUTDIR, "materials_burgundy.png")
fig.savefig(out, dpi=300)
print("wrote", out)
