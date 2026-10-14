# tools

Regeneration scripts. Run them from the repository root; they all write into
the repository, so review the diff before committing.

| Script | Regenerates | When to run |
|---|---|---|
| `gen_palette_reference.py` | `references/palettes.md` | after editing hex values, role labels or the audit logic |
| `gen_swatch_strips.py` | `gallery/swatch-*.png` | after editing hex values (README table images) |

```bash
python tools/gen_palette_reference.py
python tools/gen_swatch_strips.py
python -m sci_palettes sheet gallery/palette_sheet.png   # the README hero image
python tests/test_palettes.py                            # then verify
```

`references/palettes.md` is generated from `scripts/sci_palettes/data.py`, so the
documentation cannot drift from the code. Never hand-edit that file.

The example figures in `gallery/` are produced by the scripts in `examples/`:

```bash
python examples/01_showcase_grid.py glacier
python examples/02_colormap_gallery.py
python examples/03_materials_figure.py
python examples/04_group_comparison.py
python examples/05_export_all.py
```
