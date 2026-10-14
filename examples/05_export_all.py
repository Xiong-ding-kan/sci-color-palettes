# -*- coding: utf-8 -*-
"""End-to-end export demo: JSON / CSS / SCSS / ASE / GPL / JASC plus a
matplotlib .mplstyle file, written into build/.

Run:  python examples/05_export_all.py [outdir]
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import sci_palettes as sp  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "build")
os.makedirs(OUT, exist_ok=True)

written = [
    sp.to_json(os.path.join(OUT, "sci-palettes.json")),
    sp.to_css(os.path.join(OUT, "sci-palettes.css")),
    sp.to_scss(os.path.join(OUT, "sci-palettes.scss")),
    sp.to_ase(os.path.join(OUT, "sci-palettes.ase")),
]
for pid in sp.names():
    written.append(sp.to_gpl(os.path.join(OUT, f"{pid}.gpl"), pid))
    written.append(sp.to_jasc(os.path.join(OUT, f"{pid}.jasc"), pid))
    written.append(sp.save_style(os.path.join(OUT, f"{pid}.mplstyle"), pid))

for w in written:
    print(f"{os.path.getsize(w):>8}  {w}")

print()
print(sp.preview(["glacier", "burgundy"]))
