# -*- coding: utf-8 -*-
"""Clinical / database figure types: Kaplan-Meier curves, forest plot,
subgroup matrix, cohort comparison, CONSORT-style flow, missing-data heatmap.

These are the panels where palette choice is constrained by accessibility
rather than taste, so each one is drawn with a palette that clears the clinical
or database gate.

Run:  python examples/06_clinical_figures.py [palette] [outdir]
"""

import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import sci_palettes as sp  # noqa: E402

PALETTE = sys.argv[1] if len(sys.argv) > 1 else "burgundy-clin-hi"
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "..", "gallery")
os.makedirs(OUTDIR, exist_ok=True)

sp.set_theme(PALETTE)
C = sp.palette(PALETTE)
arm = sp.select(C, 4)                 # four study arms, hues preserved
cmap = sp.colormap(PALETTE)
rng = np.random.default_rng(2024)

fig = plt.figure(figsize=(7.2, 6.6))
gs = fig.add_gridspec(3, 2, hspace=0.62, wspace=0.34)


def tag(ax, letter, title):
    ax.set_title(f"{letter}  {title}", loc="left", fontweight="bold", pad=6)


# a - Kaplan-Meier curves: the canonical clinical panel ---------------------
ax = fig.add_subplot(gs[0, :])
t = np.linspace(0, 60, 400)
for i, (col, ls) in enumerate(zip(arm, ["-", "--", "-.", ":"])):
    rate = [0.010, 0.021, 0.033, 0.052][i]
    surv = np.exp(-rate * t)
    ax.step(t, surv, where="post", color=col, lw=1.3, ls=ls,
            label=f"Arm {chr(65+i)} (n={[210, 186, 154, 98][i]})")
    ax.fill_between(t, np.clip(surv - 0.05, 0, 1), np.clip(surv + 0.05, 0, 1),
                    step="post", color=col, alpha=0.13, lw=0)
ax.set_xlabel("Time since enrolment (months)")
ax.set_ylabel("Overall survival")
ax.set_ylim(0, 1.04)
ax.set_xlim(0, 60)
ax.legend(loc="upper right", fontsize=6)
tag(ax, "a", "Kaplan-Meier survival by treatment arm")

# b - forest plot -----------------------------------------------------------
ax = fig.add_subplot(gs[1, 0])
labels = ["All patients", "Age < 65", "Age >= 65", "Female", "Male", "Stage III", "Stage IV"]
hr = np.array([0.78, 0.71, 0.92, 0.83, 0.74, 0.69, 0.88])
lo = hr - np.array([0.11, 0.14, 0.18, 0.15, 0.13, 0.12, 0.17])
hi = hr + np.array([0.13, 0.17, 0.22, 0.18, 0.15, 0.14, 0.21])
y = np.arange(len(labels))[::-1]
ax.axvline(1.0, color="#888888", lw=0.8, ls="--")
ax.errorbar(hr, y, xerr=[hr - lo, hi - hr], fmt="none", ecolor=arm[0],
            elinewidth=1.0, capsize=2)
ax.plot(hr, y, "o", color=arm[0], ms=3.5)
ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=6)
ax.set_xlabel("Hazard ratio (95% CI)")
ax.set_xscale("log")
# on a log axis the formatter must be told to print plain numbers, otherwise
# 0.5 renders as "6 x 10^-1" and the axis becomes unreadable
ax.set_xticks([0.5, 0.75, 1.0, 1.5])
ax.set_xticklabels(["0.5", "0.75", "1.0", "1.5"])
ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.text(0.02, 0.04, "favours treatment", transform=ax.transAxes,
        fontsize=5, color="#666666")
ax.text(0.70, 0.04, "favours control", transform=ax.transAxes,
        fontsize=5, color="#666666")
tag(ax, "b", "Subgroup forest plot")

# c - adverse events, stacked and colour-blind safe -------------------------
ax = fig.add_subplot(gs[1, 1])
grades = ["G1", "G2", "G3", "G4"]
soc = ["Anaemia", "Fatigue", "Nausea", "Neutropenia", "Rash"]
data = rng.integers(4, 30, (len(soc), len(grades)))
bottom = np.zeros(len(soc))
gcols = sp.select(C, 4)
for j, (g, col) in enumerate(zip(grades, gcols)):
    ax.barh(soc, data[:, j], left=bottom, color=col, label=g, height=0.62)
    bottom += data[:, j]
ax.set_xlabel("Patients (%)")
ax.legend(fontsize=5.5, ncol=4, loc="lower right", title="Grade",
          title_fontsize=5.5)
ax.tick_params(axis="y", labelsize=6)
tag(ax, "c", "Adverse events by grade")

# d - cohort comparison (database work) -------------------------------------
ax = fig.add_subplot(gs[2, 0])
cohorts = sp.select(sp.palette("lilac_garden-clin-hi"), 5)
x = np.arange(4)
w = 0.16
for i, col in enumerate(cohorts):
    v = rng.uniform(10, 45, 4)
    ax.bar(x + (i - 2) * w, v, w, color=col, label=f"Cohort {i+1}")
ax.set_xticks(x)
ax.set_xticklabels(["2019", "2020", "2021", "2022"], fontsize=6)
ax.set_ylabel("Enrolment (n)")
ax.legend(fontsize=5, ncol=5, loc="upper center", columnspacing=0.8)
ax.set_ylim(0, 62)
tag(ax, "d", "Enrolment across five cohorts")

# e - missing-data pattern, the classic database figure ---------------------
ax = fig.add_subplot(gs[2, 1])
M = rng.random((14, 9)) < 0.22
# "present" is the palette's neutral background member and "missing" its
# strongest dark: the eye should be drawn to the gaps, and a dark field would
# read as heavy rather than empty
from matplotlib.colors import ListedColormap
miss_cmap = ListedColormap([C[-1], C[0]])
ax.imshow(M.astype(float), cmap=miss_cmap, aspect="auto", vmin=0, vmax=1)
ax.set_xticks(range(9))
ax.set_xticklabels([f"V{i+1}" for i in range(9)], fontsize=5)
ax.set_yticks(range(0, 14, 2))
ax.set_yticklabels([f"P{i+1}" for i in range(0, 14, 2)], fontsize=5)
ax.set_xlabel("Visit", fontsize=6.5)
ax.set_ylabel("Patient", fontsize=6.5)
ax.text(0.99, 1.06, "dark = missing", transform=ax.transAxes, fontsize=5,
        color="#666666", ha="right")
tag(ax, "e", "Missing data pattern")

name = sp.resolve(PALETTE)
out = os.path.join(OUTDIR, "clinical_figures.png")
fig.savefig(out, dpi=300)
print("wrote", out)
print("palette:", name, "| scores:", sp.applications(name)["scores"])
