# -*- coding: utf-8 -*-
"""Nine-panel showcase: one palette applied across the figure types that
dominate SCI manuscripts (time series, bars, clustering, profiles, violin,
contour map, regression, heatmap, surface response).

Run:  python examples/01_showcase_grid.py [palette] [outdir]
"""

import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import sci_palettes as sp  # noqa: E402

PALETTE = sys.argv[1] if len(sys.argv) > 1 else "glacier"
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "..", "gallery")
os.makedirs(OUTDIR, exist_ok=True)

sp.set_theme(PALETTE)
C = sp.palette(PALETTE)
dark, mid, light, pale = C[0], C[1], C[2], C[3]
c5, c6, c7, c8 = C[4], C[5], C[6], C[7]
cmap = sp.colormap(PALETTE)

rng = np.random.default_rng(42)
fig = plt.figure(figsize=(7.2, 9.0))
gs = fig.add_gridspec(3, 3, hspace=0.55, wspace=0.45)


def tag(ax, letter, title):
    ax.set_title(f"{letter}  {title}", loc="left", fontweight="bold", pad=6)


# a - time series with confidence bands ------------------------------------
ax = fig.add_subplot(gs[0, 0])
years = np.arange(2015, 2024)
for i, (col, lab) in enumerate(zip([dark, mid, c7], ["Site A", "Site B", "Site C"])):
    base = [22, 13, 5][i]
    y = base + 6 * np.exp(-((years - 2018) ** 2) / 12) + rng.normal(0, 0.5, len(years))
    ax.plot(years, y, "-o", color=col, label=lab, ms=2.5)
    ax.fill_between(years, y - 2.5, y + 2.5, color=col, alpha=0.18, lw=0)
ax.set_xlabel("Year"); ax.set_ylabel("Concentration (mg/L)")
ax.set_xticks([2015, 2017, 2019, 2021, 2023])
ax.legend(loc="center right")
tag(ax, "a", "Time series")

# b - grouped bars with error bars -----------------------------------------
ax = fig.add_subplot(gs[0, 1])
cats = ["TN", "TP", "COD", "Chl-a"]
x = np.arange(len(cats)); w = 0.2
for i, col in enumerate([dark, mid, light, c7]):
    v = rng.uniform(2, 20, len(cats))
    ax.bar(x + (i - 1.5) * w, v, w, color=col, label=f"Site {'ABCD'[i]}",
           yerr=v * 0.12, capsize=1.5, error_kw={"lw": 0.7, "ecolor": "#444444"})
ax.set_xticks(x); ax.set_xticklabels(cats)
ax.set_ylabel("Concentration (mg/L)")
ax.legend(ncol=2, fontsize=6)
tag(ax, "b", "Water quality")

# c - PCA clusters ---------------------------------------------------------
ax = fig.add_subplot(gs[0, 2])
for i, (col, mk) in enumerate(zip([dark, mid, c7], ["o", "s", "^"])):
    cx, cy = [(0, 1), (2, -1), (-1.5, -1.5)][i]
    pts = rng.normal([cx, cy], 0.55, (22, 2))
    ax.scatter(pts[:, 0], pts[:, 1], s=9, color=col, marker=mk,
               edgecolor="white", linewidth=0.3, label=f"Cluster {i+1}")
ax.set_xlabel("PC1 (46.2%)"); ax.set_ylabel("PC2 (28.1%)")
ax.legend(fontsize=6)
tag(ax, "c", "PCA clusters")

# d - depth profiles -------------------------------------------------------
ax = fig.add_subplot(gs[1, 0])
depth = np.linspace(0, 100, 20)
for i, col in enumerate([dark, mid, light, c7]):
    ax.plot(8 + 6 * np.exp(-depth / (20 + 15 * i)) + rng.normal(0, 0.1, 20),
            depth, "-o", color=col, ms=2, label=["Temp.", "DO", "Chl-a", "Turbidity"][i])
ax.invert_yaxis()
ax.set_xlabel("Parameter (a.u.)"); ax.set_ylabel("Depth (m)")
ax.legend(fontsize=6)
tag(ax, "d", "Depth profile")

# e - violin + box ---------------------------------------------------------
ax = fig.add_subplot(gs[1, 1])
data = [rng.normal(m, 3, 120) for m in (22, 24, 19, 15)]
parts = ax.violinplot(data, showextrema=False, widths=0.8)
for pc, col in zip(parts["bodies"], [dark, mid, light, c7]):
    pc.set_facecolor(col); pc.set_alpha(0.75); pc.set_edgecolor(col)
bp = ax.boxplot(data, widths=0.18, patch_artist=True, showfliers=False,
                medianprops={"color": "white", "lw": 0.9})
for patch in bp["boxes"]:
    patch.set_facecolor("#333333"); patch.set_edgecolor("#333333")
ax.set_xticks(range(1, 5)); ax.set_xticklabels(["Spr", "Sum", "Aut", "Win"])
ax.set_ylabel("Value (a.u.)")
tag(ax, "e", "Seasonal variation")

# f - filled contour map ---------------------------------------------------
ax = fig.add_subplot(gs[1, 2])
lon = np.linspace(100, 108, 60); lat = np.linspace(20, 28, 60)
LON, LAT = np.meshgrid(lon, lat)
Z = 12 * np.exp(-((LON - 106) ** 2 + (LAT - 24) ** 2) / 6) + 3 * np.sin(LON / 2)
cf = ax.contourf(LON, LAT, Z, levels=10, cmap=cmap)
ax.contour(LON, LAT, Z, levels=10, colors="white", linewidths=0.25, alpha=0.6)
plt.colorbar(cf, ax=ax, label="Value (a.u.)", fraction=0.046)
ax.set_xlabel("Longitude (°)"); ax.set_ylabel("Latitude (°)")
tag(ax, "f", "Spatial gradient")

# g - regression scatter ---------------------------------------------------
ax = fig.add_subplot(gs[2, 0])
n = 90
x = rng.uniform(0, 30, n)
y = 6 + 1.7 * x + rng.normal(0, 6, n)
ax.scatter(x, y, s=10, color=mid, alpha=0.75, edgecolor="white", linewidth=0.3)
k, b = np.polyfit(x, y, 1)
xs = np.linspace(0, 30, 10)
ax.plot(xs, k * xs + b, color=dark, lw=1.4)
ax.text(0.04, 0.93, r"$R$ = 0.72" + "\n" + r"$p$ < 0.001", transform=ax.transAxes,
        va="top", ha="left", fontsize=6.5)
ax.set_xlabel("Temperature (°C)"); ax.set_ylabel("Chl-a (µg/L)")
tag(ax, "g", "Correlation")

# h - clustered heatmap ----------------------------------------------------
ax = fig.add_subplot(gs[2, 1])
M = rng.normal(0, 1, (8, 8))
M = (M + M.T) / 2
im = ax.imshow(M, cmap=cmap, aspect="auto", vmin=-2, vmax=2)
plt.colorbar(im, ax=ax, fraction=0.046)
ax.set_xticks(range(8)); ax.set_xticklabels([f"S{i+1}" for i in range(8)], fontsize=5.5)
ax.set_yticks(range(8))
ax.set_yticklabels(["NO₃⁻", "PO₄³⁻", "SiO₂", "NH₄⁺", "Chl-a", "DOC", "Sal", "pH"], fontsize=5.5)
tag(ax, "h", "Heatmap")

# i - 3D response surface --------------------------------------------------
ax = fig.add_subplot(gs[2, 2], projection="3d")
X = np.linspace(0, 30, 40); Y = np.linspace(0, 15, 40)
XX, YY = np.meshgrid(X, Y)
ZZ = 30 * np.exp(-((XX - 20) ** 2) / 200 - ((YY - 8) ** 2) / 40)
surf = ax.plot_surface(XX, YY, ZZ, cmap=cmap, linewidth=0, antialiased=True, alpha=0.95)
ax.contour(XX, YY, ZZ, zdir="z", offset=0, cmap=cmap, levels=8, linewidths=0.4)
ax.set_xlabel("Temp. (°C)", labelpad=-6)
ax.set_ylabel("Nutrient", labelpad=-6)
ax.set_zlabel("Rate", labelpad=-8)
ax.tick_params(labelsize=5, pad=-2)
ax.view_init(28, -128)
tag(ax, "i", "Response surface")

name = sp.PALETTES[sp.resolve(PALETTE)]["name_en"].replace(" ", "_").lower()
out = os.path.join(OUTDIR, f"showcase_{name}.png")
fig.savefig(out, dpi=300)
print("wrote", out)
