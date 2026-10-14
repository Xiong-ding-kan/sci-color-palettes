# tools

Regeneration scripts. Run them from the repository root; they all write into
the repository, so review the diff before committing.

| Script | Regenerates | When to run |
|---|---|---|
| `measure_distribution.py` | nothing; prints the library's metric distribution | before changing any threshold in `gen_applications.py` |
| `gen_derived_palettes.py` | `scripts/sci_palettes/derived.json` | after editing `_color_ops.py` or the family list |
| `gen_applications.py` | `scripts/sci_palettes/applications.json` | after regenerating the derived palettes or editing a profile |
| `gen_derived_docs.py` | `references/derived-palettes.md` | after regenerating either JSON file |
| `gen_palette_reference.py` | `references/palettes.md` | after editing hex values, role labels or the audit logic |
| `gen_swatch_strips.py` | `gallery/swatch-*.png` | after editing hex values (README table images) |

`_color_ops.py` is a shared helper (CIELCh conversion and the transforms), not a
script to run. The generators depend on it, so the order above matters:
`_color_ops.py` -> `derived.json` -> `applications.json` -> docs.

The full regeneration order, from a change to the transforms:

```bash
python tools/gen_derived_palettes.py     # 1. rebuild derived.json
python tools/measure_distribution.py     # 2. check the thresholds still fit
python tools/gen_applications.py         # 3. rebuild applications.json
python tools/gen_derived_docs.py         # 4. rebuild the palette reference
python tools/gen_palette_reference.py    #    (anchor palettes, unchanged)
python tools/gen_swatch_strips.py        #    README swatch images
python -m sci_palettes sheet gallery/palette_sheet.png   # README hero image
python tests/test_palettes.py            # 5. verify
```

`references/palettes.md` and `references/derived-palettes.md` are generated from
the JSON data, so the documentation cannot drift from the code. Never hand-edit
those two files.

The example figures in `gallery/` are produced by the scripts in `examples/`:

```bash
python examples/01_showcase_grid.py glacier
python examples/02_colormap_gallery.py
python examples/03_materials_figure.py
python examples/04_group_comparison.py
python examples/05_export_all.py
python examples/06_clinical_figures.py burgundy-clin-hi
```
