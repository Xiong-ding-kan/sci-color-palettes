# -*- coding: utf-8 -*-
"""Generate references/palettes.md from the canonical data (no hand-typing)."""
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

import sci_palettes as sp  # noqa: E402
from sci_palettes.data import PALETTES  # noqa: E402

BT = chr(96)  # backtick


def code(s):
    return BT + s + BT


out = []
out.append("# Palette reference\n")
out.append("Copy-paste hex values. Order is dark -> light as anchor, so index 0 is")
out.append("always the emphasis colour. `contrast` is the WCAG ratio against white;")
out.append("below 3:1 the colour is for fills and bands, not for text or thin lines.\n")
out.append("Chinese names, English names and the ids below all work as arguments to")
out.append("every function in the package.\n")

for pid in sp.names():
    i = PALETTES[pid]
    out.append(f"## {i['name_zh']} / {i['name_en']} - {code(pid)}\n")
    out.append(f"*{i['subtitle_zh']} / {i['subtitle_en']}*\n")
    out.append(f"Mood: {i['vibe']}\n")
    out.append("| # | hex | role | on white | luminance |")
    out.append("|---|---|---|---|---|")
    for n, (c, r) in enumerate(zip(i["hex"], i["roles"]), 1):
        cr = sp.contrast_ratio(c, "#FFFFFF")
        out.append(f"| {n} | {code(c)} | {r} | {cr:.2f}:1 {sp.wcag_level(c, '#FFFFFF')} "
                   f"| {sp.luminance(c):.3f} |")
    out.append("")
    out.append("```python")
    out.append(f"sp.palette({repr(pid)})")
    out.append("  " + " ".join(i["hex"]))
    out.append("```\n")
    out.append("Audit:")
    out.append("```")
    out.append(sp.report(pid))
    out.append("```\n")

text = "\n".join(out) + "\n"
dest = os.path.join(HERE, "..", "references", "palettes.md")
os.makedirs(os.path.dirname(dest), exist_ok=True)
with open(dest, "w", encoding="utf-8") as fh:
    fh.write(text)
print("wrote", os.path.abspath(dest), len(text), "bytes")
