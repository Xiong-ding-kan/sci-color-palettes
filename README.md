# sci-color-palettes · 科研配色

> Six publication-ready colour schemes for SCI journal figures — with
> colour-blind simulation, contrast auditing and one-line matplotlib themes.

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Palettes](https://img.shields.io/badge/palettes-6-6F8F7B.svg)](#the-six-palettes)

Transcribed from the **科研配色** (Scientific Colour Schemes) series, where each
article publishes one 8-colour scheme as images. This repository turns them into
hex data a script can use, plus auditing and export tooling. Every value was
read from the published swatch labels and cross-checked against the swatch
pixels.

![All six palettes](gallery/palette_sheet.png)

## The six palettes

| Palette | 中文名 | English | Designed for |
|---|---|---|---|
| ![](gallery/swatch-glacier.png)<br>`glacier` | 冰川蓝绿 | Glacier Teal | environment, ecology, water quality, climate |
| ![](gallery/swatch-dusk_rose.png)<br>`dusk_rose` | 暮紫玫瑰 | Dusk Purple Rose | biology, omics, dose-response, group comparison |
| ![](gallery/swatch-sage.png)<br>`sage` | 鼠尾草紫 | Sage & Violet | general visualisation; the most colour-blind safe |
| ![](gallery/swatch-burgundy.png)<br>`burgundy` | 勃艮第灰 | Burgundy Slate | materials, chemistry, XRD / XPS / TGA |
| ![](gallery/swatch-indigo.png)<br>`indigo` | 靛蓝丁香 | Indigo Lilac | statistics, modelling, PCA and regression |
| ![](gallery/swatch-lilac_garden.png)<br>`lilac_garden` | 熏紫春庭 | Smoked Lilac Garden | catalysis, pastel multi-hue panels |

Hex values, roles and per-palette audits: **[references/palettes.md](references/palettes.md)**.

## Install

```bash
git clone https://github.com/Xiong-ding-kan/sci-color-palettes.git
cd sci-color-palettes
pip install -e .                      # matplotlib stays optional
```

No install wanted? Add `scripts/` to `PYTHONPATH` and import directly.

## Use

```python
import matplotlib.pyplot as plt
import sci_palettes as sp

sp.set_theme("burgundy")            # palette + paper styling, one line
C  = sp.palette("burgundy")         # the 8 hex strings, dark -> light
cm = sp.colormap("burgundy")        # matching continuous colormap
```

Chinese names work as aliases everywhere:

```python
sp.set_theme("冰川蓝绿")
sp.palette("靛蓝丁香", key="rgb")
```

### Choosing the right number of colours

```python
sp.select(sp.palette("sage"), 4)    # 4 real palette colours, hues preserved
sp.ramp(sp.palette("sage"), 6)      # 6 blended steps, for gradients
sp.sub("sage", 4)                   # 4 consecutive ramp members
```

`select` is for categories (it returns colours that exist in the palette);
`ramp` is for continuous scales (it interpolates in CIE Lab).

### Check it before you submit

```python
print(sp.report("indigo"))
```

```
palette      indigo  (靛蓝丁香, 8 colours)
ramp         #414A78 #6978A6 #A5B4D1 #DCE3F0 #8B739F #B7A1C8 #DDD0E6 #C7B38A
luminance    #414A78 #6978A6 #8B739F #B7A1C8 #A5B4D1 #C7B38A #DDD0E6 #DCE3F0
close pairs  #DCE3F0~#DDD0E6 (9.9)
protanopia   min deltaE 3.5   closest #6978A6/#8B739F
deuteranopia min deltaE 3.0   closest #A5B4D1/#B7A1C8
tritanopia   min deltaE 9.7   closest #DCE3F0/#DDD0E6
achromatopsia min deltaE 0.4   closest #A5B4D1/#C7B38A
on white     AAA 1, AA 0, low-contrast 5
note         pale members (#A5B4D1, ...) are below 3:1 on white: use them for
             fills/bands only, put labels and data points on white, or outline
             them with a darker member of the same ramp
```

Preview what a colour-blind reader sees:

```python
sim = sp.simulate_cvd(sp.palette("indigo"), sp.DEUTERANOPIA)
```

Read **[references/accessibility.md](references/accessibility.md)** for how to
act on each number, and the non-negotiable rules in **[SKILL.md](SKILL.md)**.

### Export to whatever your co-authors use

```python
sp.to_css("palette.css")        # --sci-glacier-1: #315C6B;  ...
sp.to_scss("palette.scss")      # $glacier: (1: #315C6B, ...)
sp.to_ase("palette.ase")        # Adobe, Affinity, Inkscape
sp.to_gpl("palette.gpl")        # GIMP, Inkscape, Aseprite
sp.to_json("palette.json")      # data + metadata
sp.save_style("sci.mplstyle")   # reusable matplotlib style
```

Origin and GraphPad Prism have no palette import format — copy the hex values
from [references/palettes.md](references/palettes.md).

### Command line

```bash
python -m sci_palettes list                  # swatches in the terminal
python -m sci_palettes show 冰川蓝绿          # detail + audit
python -m sci_palettes check                 # audit all six
python -m sci_palettes export indigo out.css
python -m sci_palettes sheet gallery/sheet.png
```

## Gallery

Rendered by the scripts in [`examples/`](examples/), regenerated on every run.

| | |
|---|---|
| [showcase_glacier_teal.png](gallery/showcase_glacier_teal.png) | nine panel types in one figure |
| [colormap_gallery.png](gallery/colormap_gallery.png) | all six as continuous / discrete / contour |
| [materials_burgundy.png](gallery/materials_burgundy.png) | XRD, adsorption, pore, TGA, mechanics, property map |
| [group_comparison_indigo.png](gallery/group_comparison_indigo.png) | group encoding + deuteranopia preview |

```bash
python examples/01_showcase_grid.py burgundy    # any palette id
python examples/05_export_all.py                # every export format
```

## Repository layout

```
SKILL.md                  agent-skill instructions (rules + workflow)
scripts/sci_palettes/     the importable package
  data.py                 canonical hex values, roles, aliases
  core.py                 colour maths, selection, auditing  (stdlib only)
  mpl.py                  themes, colormaps, fonts           (needs matplotlib)
  exporters.py            JSON / CSS / SCSS / ASE / GPL / JASC
  cli.py                  python -m sci_palettes
examples/                 five runnable figure scripts
references/               palettes.md, accessibility.md, matplotlib.md, sources.md
tools/                    regenerates references/palettes.md from data.py
gallery/                  rendered output
```

## Design notes

- **Ramps are ordered dark → light** as published, so `C[0]` is always the
  emphasis colour and `C[-1]` the neutral, and a greyscale print keeps the
  structure even when hue collapses.
- **`select` uses an exact dynamic program** to pick *n* of 8 colours closest to
  an even spread, rather than striding the ramp (which drops whole hue
  families) or blending it (which invents muddy in-between colours).
- **The audit reports distances in CIE Lab**, not RGB, because RGB distance does
  not track what the eye sees.
- **Fonts are resolved at runtime** into a concrete `font.family` list: Arial
  first for journal metrics, DejaVu Sans for scientific glyphs (₂ ⁻¹ µ Δ), then
  a CJK face for Chinese labels. matplotlib only falls back per glyph when the
  family is a concrete list — with `'sans-serif'` missing glyphs become boxes.

## Sources and credit

The palettes come from the six 科研配色 articles listed in
[references/sources.md](references/sources.md); the colour choices are the
original authors' work. This repository adds the machine-readable data,
tooling and documentation. MIT licensed — see [LICENSE](LICENSE).
