---
name: sci-color-palettes
description: A library of 184 publication-ready colour schemes for SCI journal figures - 6 published palettes from the "科研配色" series plus 178 generated variants - scored and filtered for basic research, clinical research (survival curves, forest plots) and database/registry work. Use when choosing colours for matplotlib/seaborn/Origin/R/GraphPad figures, when a user asks for 科研配色 / SCI 配色 / 论文配色 / 临床配色, when a figure needs many categories, or when checking a colour choice for colour-blind safety and print contrast.
---

# SCI colour palettes (科研配色)

184 eight-colour schemes, every one audited. Six are published designs; the
other 178 are generated from them by hue rotation, temperature drift, chroma and
contrast changes, monochrome collapse and cross-palette blending. All are
scored, and each is ranked for the research fields below.

## Start here: pick the field, then the palette

```python
import sci_palettes as sp

sp.suggest_for("临床", n=5)          # clinical: survival, forest, adverse events
sp.suggest_for("数据库", n=5)        # database/registry: many cohorts or centres
sp.suggest_for("基础", n=5)          # basic research: greyscale-safe panels
sp.suggest_for("general", n=5)
```

Each result carries a `score`, a `fits` flag and a `why` string, so a
recommendation can be checked instead of trusted. `require_fit=True` keeps only
palettes that clear every requirement of that field.

| Field | Gate it must clear | Best first choice |
|---|---|---|
| 临床 clinical | CVD separation >= 5 on the best 5, >= 2 dark members, lightness span >= 0.40 | `burgundy-clin-hi` |
| 数据库 database | pairwise separation >= 10 and hue spread >= 60 deg on the best 5 | `lilac_garden-clin-hi` |
| 基础 basic | lightness span >= 0.45, CVD separation >= 4 | `burgundy-clin` |
| 通用 general | no extra gate; ranked by span, separation, dark members | `glacier+hues` |

Of the 184 schemes, 25 clear the clinical gates, 37 the database gates and 63
the basic gates.

Why the fields differ: clinical and database figures are read by colour-blind
clinicians and printed in greyscale, so colour-vision separation and dark
members dominate. Basic-research panels are photocopied, so a monotone lightness
ramp dominates. Thresholds are calibrated against the library's own measured
distribution, not guessed. Full criteria: `references/applications.md`.

## Then apply it

```python
sp.set_theme("burgundy-clin-hi")     # rcParams: cycle + colormap + paper styling
C = sp.palette("burgundy-clin-hi")   # the 8 hex strings
cmap = sp.colormap("burgundy-clin-hi")

print(sp.applications("burgundy-clin-hi")["scores"])
# {'clinical': 82, 'database': 68, 'basic': 92, 'general': 92}
```

Chinese palette names work as aliases: `sp.palette("冰川蓝绿")`.

## Choosing how many colours the figure needs

```python
sp.select(sp.palette("sage-mono"), 5)   # 5 real palette colours, hues preserved
sp.ramp(sp.palette("sage"), 6)          # 6 blended steps, for continuous scales
sp.sub("sage", 4)                       # 4 consecutive ramp members
```

- **Categorical** (groups, treatments, cohorts, sites) -> `select`. It satisfies
  the separation figures quoted in `suggest_for`, on subsets down to 4.
- **Continuous** (colour bars, gradients, dose-response) -> `ramp`.
- **Diverging** (`div-*`, for reference ranges and log fold change) -> use as
  given; index 3 is the pale centre and must stay at the midpoint of the scale.
- Never stride a ramp (`C[::2]`) and never place two pale members side by side.

## The library

| Family | Count | What it is for |
|---|---|---|
| `hue_rotate` | 76 | the same scheme at another hue angle (30 deg steps, 15 deg for glacier/sage) |
| `temperature` | 24 | warm / cool drift, for a warmer or cooler mood |
| `blend` | 12 | two published palettes mixed (e.g. `glacier+dusk_rose`) |
| `clinical` | 12 | widest practical lightness span; survival and forest panels |
| `contrast` | 12 | a lifted (`-light`) or deepened (`-dark`) ramp |
| `diverging` | 12 | symmetric scales for reference ranges (`div-wine-teal`, ...) |
| `chroma` | 9 | muted / soft / rich saturation |
| `complement` | 6 | every hue moved to its opposite |
| `basic` | 6 | restrained chroma, evenly spaced lightness |
| `database` | 6 | `<base>+hues`: each member a further hue step, for many cohorts |
| `monochrome` | 3 | one hue family, lightness only |

```python
sp.derived_names()                 # all 178 generated ids
sp.family("clinical")              # ids in one family, best score first
sp.family("glacier")               # every variant of one published palette
sp.search("#315C6B")               # palettes containing a colour you must use
sp.recommend(n=10, min_score=70)   # highest scoring overall
sp.stats()                         # counts per family and per field
```

Every generated id encodes its transform, so it is reproducible and readable:
`glacier-h030` is glacier rotated 30 deg, `burgundy-clin` is burgundy tuned for
clinical panels, `sage-mono` is a single-hue sage ramp.

## Non-negotiable rules

1. **One palette per figure.** Do not mix two ramps to get more colours; shrink
   or switch ramps instead.
2. **Never encode meaning in colour alone.** Add marker shape, linestyle or a
   direct label - clinical journals require it and the audit assumes it.
3. **Keep the ramp order.** Index 0 is the emphasis colour, the last index the
   neutral background. `div-*` ramps are the exception: index 3 is the centre.
4. **Reserve the pale members** (contrast < 3:1 on white) for fills, bands and
   backgrounds; labels and data points go in the darker members.
5. **Check the audit before submitting.** `sp.report(pid)` or
   `sp.applications(pid)["metrics"]` - a colour choice that fails `cvd5` will
   fail a reviewer with deuteranopia.
6. **Grey is a colour.** `#8992A0` in `lilac_garden` and `#8FA4B3` in `burgundy`
   are the intended neutrals; do not substitute pure black.

## Files

- `scripts/sci_palettes/` - the package. `data.py` holds the six published hex
  values, `derived.json` the 178 generated ones, `applications.json` the field
  scores, `core.py` colour maths, `mpl.py` matplotlib, `exporters.py` formats.
- `references/palettes.md` - copy-paste hex tables for the six published palettes.
- `references/applications.md` - the field profiles, criteria and top picks.
- `references/derived-palettes.md` - every generated palette grouped by family.
- `references/accessibility.md` - how to read the audit, and what to do.
- `references/matplotlib.md` - full API and rcParam reference.
- `references/sources.md` - the six source articles.
- `examples/` - five runnable figure scripts; `gallery/` - their output.
- `tools/` - regenerates `derived.json`, `applications.json` and the docs.

## Install

```bash
pip install -e .                     # from the repo root
# or just add to the path
export PYTHONPATH="$PYTHONPATH:$(pwd)/scripts"     # Windows: $env:PYTHONPATH
```

Palette data, colour maths, auditing and application scoring need no
dependencies; only the matplotlib helpers require `matplotlib`.
