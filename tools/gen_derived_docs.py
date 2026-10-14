# -*- coding: utf-8 -*-
"""Generate references/derived-palettes.md from derived.json + applications.json.

Never hand-edit the output: rerun this after changing the generators.

Run:  python tools/gen_derived_docs.py
"""

import io
import json
import os
import statistics
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import sci_palettes as sp  # noqa: E402
from sci_palettes.data import PALETTES  # noqa: E402

BT = chr(96)


def code(s):
    return BT + str(s) + BT


with open(os.path.join(ROOT, "scripts", "sci_palettes", "derived.json"),
          encoding="utf-8") as fh:
    data = json.load(fh)
with open(os.path.join(ROOT, "scripts", "sci_palettes", "applications.json"),
          encoding="utf-8") as fh:
    apps = json.load(fh)

records = data["palettes"]
by_family: dict[str, list] = {}
for r in records:
    by_family.setdefault(r["family"], []).append(r)

ORDER = ["clinical", "database", "basic", "diverging", "contrast", "chroma",
         "complement", "monochrome", "blend", "temperature", "hue_rotate"]

FAMILY_INTRO = {
    "clinical": "Widest practical lightness span with colour-vision separation "
                "held high: survival curves, forest plots, adverse-event panels.",
    "database": "Each member stepped a further hue angle so cohort, centre and "
                "site categories stay maximally separated - registry and EHR panels.",
    "basic": "Evenly spaced lightness ramp with restrained chroma: reads correctly "
             "in greyscale and in photocopied supplementary material.",
    "diverging": "Symmetric scales with a pale centre at index 3: reference ranges, "
                 "log fold change, change from baseline.",
    "contrast": "The anchor ramp lifted into a paler range or deepened into a "
                "higher-contrast one.",
    "chroma": "Saturation changed: muted, softened or intensified.",
    "complement": "Every hue moved to its opposite. Loud by design; poster and "
                  "graphical-abstract territory.",
    "monochrome": "One hue family, lightness only. The safest option for print.",
    "blend": "Two anchor palettes mixed in LCh: the lightness ramp of the first, "
             "the colour character of the second.",
    "temperature": "The ramp pulled toward orange or cyan, tapered by chroma so "
                   "near-neutral members stay neutral.",
    "hue_rotate": "The same scheme at a different hue angle. Use to match a journal "
                  "cover, a co-author's slide deck, or to separate two figures that "
                  "would otherwise look identical.",
}

out = []
out.append("# Generated palette library\n")
out.append(f"{len(records)} variants of the six anchor palettes, "
           f"{len(PALETTES) + len(records)} schemes in total. Each id encodes its "
           "transform, so it is reproducible and readable: "
           f"{code('glacier-h030')} is glacier rotated 30 deg, "
           f"{code('burgundy-clin')} is burgundy tuned for clinical panels, "
           f"{code('sage-mono')} is a single-hue sage ramp.\n")
out.append("Field suitability (C = clinical, D = database, B = basic) is in the "
           "last column; see [applications.md](applications.md) for the criteria. "
           "Each score is out of 100.\n")
out.append("```python")
out.append("import sci_palettes as sp")
out.append('sp.suggest_for("临床")          # ranked for clinical work')
out.append('sp.family("hue_rotate")         # one family, best score first')
out.append('sp.search("#315C6B")           # palettes containing a colour you must use')
out.append("```\n")

out.append("## Summary\n")
out.append("| Family | Count | Median score | Best |")
out.append("|---|---|---|---|")
for fam in ORDER:
    recs = by_family.get(fam, [])
    if not recs:
        continue
    scores = [r["score"] for r in recs]
    best = max(recs, key=lambda r: r["score"])
    out.append(f"| {code(fam)} | {len(recs)} | {statistics.median(scores):.0f} "
               f"| {code(best['id'])} ({best['score']}) |")
out.append("")
out.append("Scores are family-relative: a diverging scale is measured against a "
           "smooth-scale threshold, not the categorical one, because a smooth "
           "scale is *supposed* to have small steps. Full criteria in "
           "[applications.md](applications.md).\n")

for fam in ORDER:
    recs = sorted(by_family.get(fam, []), key=lambda r: -r["score"])
    if not recs:
        continue
    out.append(f"## {fam} ({len(recs)})\n")
    out.append(FAMILY_INTRO.get(fam, "") + "\n")
    out.append("| id | 中文 | hex | score | C / D / B |")
    out.append("|---|---|---|---|---|")
    for r in recs:
        a = apps["palettes"][r["id"]]
        hexes = " ".join(code(h.lower()) for h in r["hex"])
        fits = "".join(("C" if a["fit"]["clinical"] else "-",
                        "D" if a["fit"]["database"] else "-",
                        "B" if a["fit"]["basic"] else "-"))
        out.append(f"| {code(r['id'])} | {r['name_zh']} | {hexes} "
                   f"| {r['score']} | {fits} |")
    out.append("")
    # one transform line per distinct transform, not just the top row's
    seen = []
    for r in recs:
        t = json.dumps(r["transform"], ensure_ascii=False)
        if t not in [s[0] for s in seen]:
            seen.append((t, r))
    if len(seen) == 1:
        t, r = seen[0]
        out.append(f"*Transform*: {code(t)} - {r['note']}\n")
    else:
        out.append("*Transforms*:")
        for t, r in seen:
            out.append(f"- {code(t)}: {r['note']}")
        out.append("")

text = "\n".join(out) + "\n"
dest = os.path.join(ROOT, "references", "derived-palettes.md")
with open(dest, "w", encoding="utf-8") as fh:
    fh.write(text)
print(f"wrote {dest}  ({len(text)} bytes, {len(records)} palettes, "
      f"{len(by_family)} families)")
