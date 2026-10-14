---
name: sci-color-palettes
description: Six publication-ready colour schemes for SCI journal figures, transcribed from the "科研配色" series. Use when choosing colours for matplotlib/seaborn/Origin/R/GraphPad figures, when a user asks for 科研配色 / SCI 配色 / 论文配色, when harmonising multi-panel figures, or when checking a colour choice for colour-blind safety and print contrast.
---

# SCI colour palettes (科研配色)

Six curated 8-colour ramps, each designed for a different scientific domain.
Every hex value was transcribed from the source figures and verified by
re-sampling the published swatches.

| id | 中文名 | English | Best for |
|---|---|---|---|
| `glacier` | 冰川蓝绿 | Glacier Teal | environment, ecology, water, climate |
| `dusk_rose` | 暮紫玫瑰 | Dusk Purple Rose | biology, omics, dose-response, group comparison |
| `sage` | 鼠尾草紫 | Sage & Violet | general data visualisation, most colour-blind safe |
| `burgundy` | 勃艮第灰 | Burgundy Slate | materials, chemistry, characterisation, XRD/XPS/TGA |
| `indigo` | 靛蓝丁香 | Indigo Lilac | statistics, modelling, PCA/regression, dense plots |
| `lilac_garden` | 熏紫春庭 | Smoked Lilac Garden | catalysis, pastel multi-hue panels, wide-category plots |

Full hex values, roles and per-palette audits: `references/palettes.md`.

## Workflow

### 1. Pick the palette from the domain, not from taste

Match the table above. If the figure mixes domains, use one palette for the
whole figure - consistency across panels is what makes a multi-panel figure
look designed.

### 2. Apply it

```python
import sci_palettes as sp

sp.set_theme("burgundy")            # rcParams: cycle + colormap + paper styling
C = sp.palette("burgundy")          # the 8 hex strings, dark -> light order
cmap = sp.colormap("burgundy")      # continuous, for heatmaps/surfaces
bands = sp.listed("burgundy")       # discrete, for contour bands
```

Chinese names work as aliases: `sp.set_theme("冰川蓝绿")`.
`sp.set_theme` also fixes top/right spines, 600 dpi saving, and font stacks -
see `references/matplotlib.md`.

### 3. Choose how many colours the figure needs

```python
sp.select(sp.palette("sage"), 4)    # 4 real palette colours, hues preserved
sp.ramp(sp.palette("sage"), 6)      # 6 blended steps, for continuous scales
sp.sub("sage", 4)                   # 4 consecutive ramp members
```

- **Categorical** (groups, treatments, sites) -> `select`: keeps the original
  hues, evenly spaced along the ramp.
- **Continuous** (colour bars, gradients) -> `ramp`: blends in Lab space so the
  scale reads smoothly.
- Never stride a ramp (`C[::2]`) and never put two pale members side by side.

### 4. Check before submitting

```python
print(sp.report("indigo"))
```

Reports the closeness of every pair (CIE76), how the palette survives
protanopia/deuteranopia/tritanopia/achromatopsia, and which members fall below
3:1 contrast on white. Read `references/accessibility.md` before ignoring a
warning: pale members are for fills and bands, not for thin lines or text.

### 5. Export to whatever the co-authors use

```python
sp.to_css("palette.css")       # web / presentation
sp.to_ase("palette.ase")       # Adobe, Affinity, Inkscape
sp.to_gpl("palette.gpl")       # GIMP, Inkscape, Aseprite
sp.save_style("sci.mplstyle")  # reusable matplotlib style
```

`sp.export("out.json")` dispatches on the extension. Origin and GraphPad Prism
have no import format - paste the hex values from `references/palettes.md`.

## Non-negotiable rules

1. **Take colours from one palette per figure.** Do not mix a teal ramp with a
   rose ramp just to get more colours; shrink the ramp instead.
2. **Never encode meaning in colour alone.** Add marker shape, linestyle, or a
   direct label - required by most journals and by the accessibility report.
3. **Keep the ramp order.** The published order is dark -> light so that
   `C[0]` is always the emphasis colour and `C[-1]` the neutral background.
4. **Reserve the pale members** (contrast < 3:1 on white) for fills, bands and
   backgrounds; put data points and labels in the darker members.
5. **Grey is a colour.** `#8992A0` in `lilac_garden` and `#8FA4B3` in
   `burgundy` are the intended neutrals - do not swap in pure black.

## Files

- `scripts/sci_palettes/` - the importable package (`data.py` holds the hex
  values; `core.py` colour maths; `mpl.py` matplotlib; `exporters.py` formats).
- `examples/01_showcase_grid.py` - nine-panel figure types, any palette.
- `examples/02_colormap_gallery.py` - every palette as ramp / bands / contour.
- `examples/03_materials_figure.py` - XRD, adsorption, TGA, XPS, mechanical.
- `examples/04_group_comparison.py` - colour-blind-safe group encoding.
- `examples/05_export_all.py` - every export format at once.
- `references/palettes.md` - copy-paste hex tables and roles.
- `references/accessibility.md` - how to read the audit, and what to do.
- `references/matplotlib.md` - full API and rcParam reference.
- `references/sources.md` - the six source articles.
- `gallery/` - rendered example figures.

## Install

```bash
pip install -e .                     # from the repo root
# or just add to the path
export PYTHONPATH="$PYTHONPATH:$(pwd)/scripts"     # Windows: $env:PYTHONPATH
```

The palette data and colour maths need no dependencies; only the matplotlib
helpers require `matplotlib`.
