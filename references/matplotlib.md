# API reference

```python
import sci_palettes as sp      # works after `pip install -e .`
```

Without installing, add the scripts directory to the path:

```python
import sys; sys.path.insert(0, "path/to/sci-color-palettes/scripts")
import sci_palettes as sp
```

Only the matplotlib helpers need matplotlib. Data, colour maths, auditing and
exporting are pure standard library.

## Names and lookup

| Call | Result |
|---|---|
| `sp.names()` | `['glacier', 'dusk_rose', 'sage', 'burgundy', 'indigo', 'lilac_garden']` |
| `sp.resolve("冰川蓝绿")` | `'glacier'` |
| `sp.PALETTE_ORDER` | same order as `names()` |
| `sp.PALETTES` | the full dict: hex, roles, Chinese/English names, mood |

Every function that takes a palette accepts an id, a Chinese name, an English
name, or a shorthand such as `"teal"`, `"wine"`, `"lilac"`.

## Getting colours

| Call | Result |
|---|---|
| `sp.palette("sage")` | all 8 hex strings, dark -> light |
| `sp.palette("sage", key="rgb")` | list of `(r, g, b)` 0-255 tuples |
| `sp.palette("sage", key="roles")` | the role label of each colour |
| `sp.palette("sage", key="info")` | the full metadata dict |
| `sp.sub("sage", 4)` | 4 *consecutive* ramp members |
| `sp.select(sp.palette("sage"), 4)` | 4 colours spread across the ramp, hues preserved |
| `sp.ramp(sp.palette("sage"), 6)` | 6 *blended* steps for continuous scales |
| `sp.sort_by_luminance(cols)` | colours ordered light -> dark |

**`select` vs `ramp`.** `select` returns colours that actually exist in the
palette, so it is correct for categories. `ramp` interpolates in CIE Lab and
returns new colours, so it is correct for gradients and colour bars.

## Colour maths

| Call | Result |
|---|---|
| `sp.hex_to_rgb("#538A95")` | `(83, 138, 149)` |
| `sp.rgb_to_hex((83, 138, 149))` | `'#538A95'` |
| `sp.as_hsl([...])` | `(hue 0-360, saturation, lightness)` |
| `sp.luminance(c)` | WCAG relative luminance, 0-1 |
| `sp.contrast_ratio(a, b)` | e.g. `7.31` |
| `sp.wcag_level(a, b)` | `'AAA'`, `'AA'`, `'AA-large'`, `'fail'` |
| `sp.delta_e(a, b)` | CIE76 perceptual distance |
| `sp.nearest(c, candidates)` | closest candidate colour |
| `sp.mix(a, b, t)` | perceptually even blend |
| `sp.lighten(c, 0.2)` / `sp.darken(c, 0.2)` | blend toward white / black |

## Themes and colormaps (needs matplotlib)

```python
sp.set_theme("burgundy")                 # global rcParams
sp.set_theme("冰川蓝绿", n=4)             # 4-colour cycle instead of 8
sp.set_theme("indigo", cjk=False)        # Latin-only font stack

with sp.theme("sage"):                   # temporary, restores rcParams after
    fig, ax = plt.subplots()
    ax.plot(x, y)

sp.colormap("glacier")                   # continuous LinearSegmentedColormap
sp.colormap("glacier", reverse=True)     # reversed
sp.colormap("glacier", n=6, continuous=False)   # 6 discrete bands
sp.listed("indigo")                      # discrete colormap
sp.cycle("sage", n=5)                    # list for prop_cycle / seaborn
sp.style_dict("burgundy")                # the rcParams dict, without applying
sp.save_style("sci.mplstyle", "sage")    # stand-alone style file
```

`colormap()` registers the result, so it also works by name anywhere matplotlib
accepts a colormap string:

```python
ax.imshow(z, cmap="sci_glacier")     # equivalent to sp.colormap("glacier")
plt.colorbar(im, cmap="sci_burgundy_r")
```

`set_theme` applies a paper baseline in addition to the palette: 600 dpi
saving, top/right spines off, 8 pt base font, embedded fonts
(`pdf.fonttype 42`), a resolved font stack, and `image.cmap` set to the
palette. See `PAPER_RC` in `sci_palettes/mpl.py` to inspect or override it:

```python
sp.set_theme("sage", **{"axes.linewidth": 1.0, "font.size": 9})
```

### Fonts

`resolve_font()` returns the stack actually used, for example
`['Arial', 'DejaVu Sans', 'Microsoft YaHei', 'SimHei']`. The order matters:
Arial first for journal-mandated Latin metrics, DejaVu Sans for scientific
glyphs, then a CJK face for Chinese labels. `font.family` is set to this list
because matplotlib resolves a concrete list per glyph - with the generic
`'sans-serif'` family it does not, and missing glyphs become empty boxes.

## Accessibility

| Call | Result |
|---|---|
| `sp.report("indigo")` | formatted audit: closeness, CVD, contrast |
| `sp.check("indigo")` | the same as a dict, for programmatic use |
| `sp.simulate_cvd(cols, sp.DEUTERANOPIA)` | how that reader sees the colours |
| `sp.PROTANOPIA` `DEUTERANOPIA` `TRITANOPIA` `ACHROMATOPSIA` | names |
| `sp.cvd_matrix("deutan")` | the transform matrix itself |

See `accessibility.md` for how to act on the results.

## Exports

```python
sp.to_json("sci-palettes.json")     # data + metadata
sp.to_css("sci-palettes.css")       # --sci-glacier-1 ... CSS variables
sp.to_scss("sci-palettes.scss")     # $glacier map and list
sp.to_ase("sci-palettes.ase")       # Adobe Swatch Exchange
sp.to_gpl("glacier.gpl", "glacier") # GIMP / Inkscape / Aseprite
sp.to_jasc("glacier.jasc", "glacier")  # JASC-PAL
sp.export("out.ase")                # dispatch on extension
sp.preview(["glacier"])             # ANSI swatches for the terminal
sp.swatches(cols)                   # the ANSI swatch strip alone
```

`.gpl` and `.jasc` hold one palette and default to `glacier`; pass the id as
the second argument.

## Command line

```bash
python -m sci_palettes list                 # all palettes with swatches
python -m sci_palettes show 冰川蓝绿          # detail + audit
python -m sci_palettes check                # audit every palette
python -m sci_palettes export indigo out.css
python -m sci_palettes sheet gallery/sheet.png
```

Installed as a console script, the same commands are available as
`sci-palettes <command>`.

## Typical figure recipe

```python
import numpy as np, matplotlib.pyplot as plt
import sci_palettes as sp

sp.set_theme("burgundy")
C = sp.palette("burgundy")
groups = sp.select(C, 4)                 # four categorical colours
cmap = sp.colormap("burgundy")           # matching continuous map

fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.4))
for i, (ax, g) in enumerate(zip(axes, groups)):
    ...
fig.savefig("figure1.png")               # 600 dpi, tight bbox, fonts embedded
```
