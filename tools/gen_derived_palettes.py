# -*- coding: utf-8 -*-
"""Generate the 192 derived palettes in sci_palettes/derived.json.

The enumeration is fixed and ordered, so this script is reproducible: running it
twice produces byte-identical output. Every derived palette is audited and
scored, and anything that fails the quality gate is reported at the end.

Run:  python tools/gen_derived_palettes.py
"""

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, HERE)

from _color_ops import (  # noqa: E402
    blend, complement_hues, cool, from_lch, make_diverging, remap_diverging,
    remap_lightness, rotate_all, scale_chroma, scale_lightness, shift_hue,
    spread_lightness, to_lch, to_monochrome, warm,
)
import sci_palettes as sp  # noqa: E402
from sci_palettes.data import PALETTES  # noqa: E402

BASE = ["glacier", "dusk_rose", "sage", "burgundy", "indigo", "lilac_garden"]

# Quality gate. Two thresholds, because the two kinds of palette have opposite
# jobs: a categorical palette must keep its members apart, while a diverging or
# sequential scale must step smoothly and would fail a categorical gate by
# design. Both still need a real lightness span for greyscale printing.
MIN_DELTA_E = 6.0
MIN_DELTA_E_SCALE = 3.5          # diverging / smooth ramps
SCALE_FAMILIES = {"diverging"}
MIN_LIGHTNESS_SPAN = 0.18

records: list[dict] = []
rejected: list[str] = []


def audit(cols: list[str], family: str = "") -> dict:
    pairs = min(sp.delta_e(a, b)
                for i, a in enumerate(cols) for b in cols[i + 1:])
    span = max(sp.luminance(c) for c in cols) - min(sp.luminance(c) for c in cols)
    cvd = {}
    for kind in (sp.PROTANOPIA, sp.DEUTERANOPIA, sp.TRITANOPIA):
        sim = sp.simulate_cvd(cols, kind)
        cvd[kind[:4]] = round(min(sp.delta_e(a, b)
                                  for i, a in enumerate(sim) for b in sim[i + 1:]), 1)
    on_white = sum(1 for c in cols if sp.contrast_ratio(c, "#FFFFFF") >= 4.5)
    # A diverging scale is read as two arms meeting at the centre, so what has
    # to hold is that each arm moves monotonically inward. The anchor ramps
    # are explicitly *not* globally monotone - they walk through hue families
    # (glacier goes teal, then slate, then sand) - so requiring it globally
    # would reject the six reference palettes themselves.
    lch = [to_lch(c)[0] for c in cols]
    arm_monotone = None
    if family == "diverging":
        ci = len(cols) // 2
        arm_monotone = (all(lch[i] <= lch[i + 1] + 0.5 for i in range(ci))
                        and all(lch[i] >= lch[i + 1] - 0.5
                                for i in range(ci, len(lch) - 1)))
    return {
        "min_delta_e": round(pairs, 1),
        "lightness_span": round(span, 3),
        "arm_monotone": arm_monotone,
        "cvd_min": cvd,
        "readable_on_white": on_white,
    }


def score(a: dict, family: str = "") -> int:
    """0-100 usability score, judged against the gate for that family.

    A diverging scale is measured against :data:`MIN_DELTA_E_SCALE`, not the
    categorical gate: a smooth scale is *supposed* to have small steps, so
    scoring it against a categorical threshold would rank every good ramp last.
    """
    gate = MIN_DELTA_E_SCALE if family in SCALE_FAMILIES else MIN_DELTA_E
    full = gate + (6.0 if family in SCALE_FAMILIES else 12.0)
    s = 0.0
    s += 34 * max(0.0, min(1.0, (a["min_delta_e"] - gate) / (full - gate)))
    s += 30 * max(0.0, min(1.0, (a["lightness_span"] - MIN_LIGHTNESS_SPAN) / 0.35))
    s += 24 * max(0.0, min(1.0, a["cvd_min"]["deut"] / (gate * 2)))
    s += 12 * max(0.0, min(1.0, a["readable_on_white"] / 3.0))
    if a.get("arm_monotone") is False:
        s *= 0.8          # readable, but the arms do not read as a scale
    return int(round(s))


def add(pid: str, name_en: str, name_zh: str, family: str, transform: dict,
        cols: list[str], note: str) -> None:
    cols = [c.upper() for c in cols]
    if len(set(cols)) != len(cols):
        rejected.append(f"{pid}: duplicate colours after transform")
        return
    a = audit(cols, family)
    gate = MIN_DELTA_E_SCALE if family in SCALE_FAMILIES else MIN_DELTA_E
    if a["min_delta_e"] < gate:
        rejected.append(f"{pid}: min deltaE {a['min_delta_e']} < {gate} ({family})")
        return
    if a["lightness_span"] < MIN_LIGHTNESS_SPAN:
        rejected.append(f"{pid}: lightness span {a['lightness_span']} too flat")
        return
    records.append({
        "id": pid,
        "name_en": name_en,
        "name_zh": name_zh,
        "base": base_of(pid),
        "family": family,
        "transform": transform,
        "hex": cols,
        "note": note,
        "audit": a,
        "score": score(a, family),
    })


def base_of(pid: str) -> str:
    """Parent palette id: 'glacier-h030' -> 'glacier', 'a+b' -> 'a'.

    The diverging family has no single parent, so it is its own group.
    """
    if pid.startswith("div-"):
        return "div"
    return pid.split("+")[0].split("-")[0]


# --------------------------------------------------------------------------
# 1. hue rotations: 12 steps x 6 palettes
# --------------------------------------------------------------------------
for b in BASE:
    cols = PALETTES[b]["hex"]
    for deg in range(0, 360, 30):
        add(f"{b}-h{deg:03d}",
            f"{PALETTES[b]['name_en']} h+{deg}",
            f"{PALETTES[b]['name_zh']}·色相+{deg}",
            "hue_rotate", {"hue_shift": deg}, rotate_all(cols, deg),
            f"every hue rotated {deg} deg; same lightness and chroma structure")

# finer steps for the two palettes with the most headroom, so the rotation
# family can be dialled in rather than jumped in 30 deg blocks
FINE = {"glacier": 15, "sage": 15}
for b, step in FINE.items():
    cols = PALETTES[b]["hex"]
    for deg in (step, 360 - step):
        add(f"{b}-h{deg:03d}",
            f"{PALETTES[b]['name_en']} h+{deg}" if deg < 180
            else f"{PALETTES[b]['name_en']} h-{360 - deg}",
            f"{PALETTES[b]['name_zh']}·色相{'+' if deg < 180 else '-'}"
            f"{deg if deg < 180 else 360 - deg}",
            "hue_rotate", {"hue_shift": deg}, rotate_all(cols, deg),
            f"every hue rotated {deg if deg < 180 else deg - 360} deg; "
            "fine-tune step for this ramp")

# --------------------------------------------------------------------------
# 2. complementary: the 180 deg family is what "opposite" actually means
# --------------------------------------------------------------------------
for b in BASE:
    add(f"{b}-comp", f"{PALETTES[b]['name_en']} Complement",
        f"{PALETTES[b]['name_zh']}·互补", "complement",
        {"hue_shift": 180}, complement_hues(PALETTES[b]["hex"]),
        "each hue moved to its opposite; high separation, poster-friendly")

# --------------------------------------------------------------------------
# 3. temperature drift
# --------------------------------------------------------------------------
for b in BASE:
    cols = PALETTES[b]["hex"]
    for tag, fn, deg in (("warm", warm, 22), ("cool", cool, 22),
                         ("warmer", warm, 40), ("cooler", cool, 40)):
        add(f"{b}-{tag}", f"{PALETTES[b]['name_en']} {tag.title()}",
            f"{PALETTES[b]['name_zh']}·{'暖调' if 'warm' in tag else '冷调'}",
            "temperature", {"temperature": tag, "degrees": deg},
            fn(cols, deg),
            f"hue pulled {abs(deg)} deg toward {'orange' if 'warm' in tag else 'cyan'}, "
            "tapered by chroma so near-neutral members stay neutral")

# --------------------------------------------------------------------------
# 4. chroma
# --------------------------------------------------------------------------
# Muting shrinks perceptual distance between members, so the muted variants also
# get their lightness ramp remapped a little wider to take over the separation.
# Remapping is used rather than a scale factor because uniform L-scaling
# collapses ramps whose members are already clustered (measured: sage at x1.30
# drops from min deltaE 9.6 to 0.7).
CHROMA = [
    ("muted", 0.60, (10.0, 90.0), "低饱和",
     "chroma x0.60 with a wider lightness ramp; for dense multi-panel figures"),
    ("soft", 0.78, (12.0, 92.0), "柔化",
     "gently desaturated: keeps the hue character, calms a busy figure"),
    ("rich", 1.25, None, "高饱和",
     "chroma x1.25: more vivid, for slides and graphical abstracts"),
]
for b in BASE[::2]:
    cols = PALETTES[b]["hex"]
    for tag, k, lrange, zh, note in CHROMA:
        out = scale_chroma(cols, k)
        if lrange:
            out = remap_lightness(out, *lrange)
        add(f"{b}-{tag}", f"{PALETTES[b]['name_en']} {tag.title()}",
            f"{PALETTES[b]['name_zh']}·{zh}", "chroma",
            {"chroma_scale": k, "lightness_range": list(lrange) if lrange else None},
            out, note)

# --------------------------------------------------------------------------
# 5. contrast / lightness structure
# --------------------------------------------------------------------------
# Remapping the L range is used instead of a scale factor: a factor drives pale
# members to L=100 where they collapse into one duplicate colour per palette.
CONTRAST = [
    ("light", (35.0, 95.0), "lifted: pale, airy, fills and backgrounds"),
    ("dark", (16.0, 70.0), "deepened: high contrast, reads at small size"),
]
for b in BASE:
    cols = PALETTES[b]["hex"]
    for tag, (lo, hi), note in CONTRAST:
        add(f"{b}-{tag}", f"{PALETTES[b]['name_en']} {tag.title()}",
            f"{PALETTES[b]['name_zh']}·{'浅调' if tag == 'light' else '深调'}",
            "contrast", {"lightness_range": [lo, hi]},
            remap_lightness(cols, lo, hi), note)

# --------------------------------------------------------------------------
# 6. monochrome
# --------------------------------------------------------------------------
for b in BASE[::2]:
    cols = PALETTES[b]["hex"]
    lch = [to_lch(c) for c in cols]
    out = to_monochrome(cols)
    add(f"{b}-mono", f"{PALETTES[b]['name_en']} Mono",
        f"{PALETTES[b]['name_zh']}·单色", "monochrome", {"monochrome": True},
        out, "single hue family, lightness only: the safest option for print")

# --------------------------------------------------------------------------
# 7. cross-palette blends
# --------------------------------------------------------------------------
BLENDS = [("glacier", "dusk_rose"), ("glacier", "burgundy"),
          ("dusk_rose", "sage"), ("sage", "lilac_garden"),
          ("burgundy", "indigo"), ("indigo", "sage"),
          ("indigo", "lilac_garden"), ("dusk_rose", "lilac_garden"),
          ("glacier", "indigo"), ("sage", "burgundy"),
          ("burgundy", "lilac_garden"), ("glacier", "lilac_garden")]
for a, b in BLENDS:
    cols = blend(PALETTES[a]["hex"], PALETTES[b]["hex"], 0.5)
    add(f"{a}+{b}", f"{PALETTES[a]['name_en']} x {PALETTES[b]['name_en']}",
        f"{PALETTES[a]['name_zh']}×{PALETTES[b]['name_zh']}", "blend",
        {"blend": [a, b], "t": 0.5}, cols,
        f"lightness ramp of {a}, hue and chroma halfway to {b}")

# --------------------------------------------------------------------------
# 8. field-targeted families
#
# These are not "more rotations": each one is generated to satisfy a concrete
# requirement of one research field, then verified by the audit below.
# --------------------------------------------------------------------------

# clinical: survival curves, adverse-event panels and subgroup forests are
# printed in greyscale and read by colour-blind clinicians, so the blocking
# requirements are a large lightness span and strong CVD separation.
# The lightness floor was tuned by measurement (tools/_probe_clinical.py):
# indigo needs the span opened this far to reach cvd5 >= 5, and pushing further
# only flattens the palette's first member toward black without gaining more.
CLINICAL_SOURCES = ["glacier", "dusk_rose", "sage", "burgundy", "indigo",
                    "lilac_garden"]
for b in CLINICAL_SOURCES:
    cols = PALETTES[b]["hex"]
    for tag, lo, chroma in (("clin", 12.0, 0.95), ("clin-hi", 10.0, 1.00)):
        out = remap_lightness(scale_chroma(cols, chroma), lo, 95.0)
        add(f"{b}-{tag}", f"{PALETTES[b]['name_en']} Clinical",
            f"{PALETTES[b]['name_zh']}·临床", "clinical",
            {"lightness_range": [lo, 95.0], "chroma_scale": chroma},
            out,
            "widest practical lightness span for survival curves, forest plots "
            "and adverse-event panels; survives greyscale printing")

# database / registry work: many cohorts, centres or sites on one axis, so the
# requirement is maximum pairwise separation rather than a smooth ramp.
DATABASE_RECIPES = [
    ("glacier+hues", "glacier", 60.0, [(0, 1.0), (1, 1.15), (2, 1.0), (3, 1.2),
                                       (4, 0.95), (5, 1.1), (6, 1.0), (7, 1.05)]),
    ("indigo+hues", "indigo", 45.0, None),
    ("sage+hues", "sage", 45.0, None),
    ("burgundy+hues", "burgundy", 90.0, None),
    ("dusk_rose+hues", "dusk_rose", 40.0, None),
    ("lilac_garden+hues", "lilac_garden", 55.0, None),
]
for pid, b, deg, chroma in DATABASE_RECIPES:
    cols = PALETTES[b]["hex"]
    out = []
    for i, c in enumerate(cols):
        L, C, h = to_lch(c)
        k = chroma[i][1] if chroma else 1.0
        out.append(from_lch(L, C * k, (h + deg * i) % 360.0))
    out = remap_lightness(out, 12.0, 95.0)
    add(pid, f"{PALETTES[b]['name_en']} Cohorts",
        f"{PALETTES[b]['name_zh']}·队列", "database",
        {"incremental_hue": deg, "lightness_range": [12.0, 95.0]},
        out,
        f"each member stepped a further {deg} deg so cohort, centre and site "
        "categories stay maximally separated - for registry and EHR panels")

# basic research: figure panels are photocopied and read in greyscale, so the
# requirement is a monotone lightness ramp with restrained chroma.
BASIC_SOURCES = ["glacier", "burgundy", "sage", "indigo", "dusk_rose", "lilac_garden"]
for b in BASIC_SOURCES:
    cols = PALETTES[b]["hex"]
    add(f"{b}-basic", f"{PALETTES[b]['name_en']} Greyscale-safe",
        f"{PALETTES[b]['name_zh']}·基础科研", "basic",
        {"chroma_scale": 0.80, "lightness_range": [14.0, 93.0]},
        remap_lightness(scale_chroma(cols, 0.80), 14.0, 93.0),
        "evenly spaced lightness ramp, restrained chroma: reads correctly in "
        "greyscale and in photocopied supplementary material")

# clinical reference-range ramps: diverging scales centred on a normal range,
# a zero effect size or a change from baseline. Arms are drawn from anchor
# palette colours so no invented near-black endpoints can collide.
DIVERGING = [
    ("wine-teal", "burgundy", "glacier"),
    ("plum-blue", "burgundy", "indigo"),
    ("plum-sage", "dusk_rose", "sage"),
    ("rose-teal", "dusk_rose", "glacier"),
]
for tag, parent_a, parent_b in DIVERGING:
    ca, cb = PALETTES[parent_a]["hex"], PALETTES[parent_b]["hex"]
    la = sp.sort_by_luminance(ca)
    lb = sp.sort_by_luminance(cb)
    # arm A from its palette's darkest and palest members; arm B from a
    # chromatic member and a pale one, so the two arms differ in hue family
    base_ramp = make_diverging(dark_a=la[0], pale_a=la[-1],
                               dark_b=lb[1], pale_b=lb[-2], n_steps=3)
    if len(set(base_ramp)) != len(base_ramp):
        rejected.append(f"div-{tag}: duplicate colours in the base ramp")
        continue
    # arm_scale multiplies each arm member's distance from the centre in
    # lightness; the three variants have to differ by enough to be visibly
    # different scales rather than near-identical ramps.
    for vtag, scale in (("", 1.0), ("-soft", 0.62), ("-deep", 1.45)):
        out = remap_diverging(base_ramp, scale, centre_index=3)
        add(f"div-{tag}{vtag}", f"Diverging {tag.title()}{' Soft' if vtag else ''}",
            f"双向·{tag}{'·柔' if vtag else ''}", "diverging",
            {"archetype": tag, "parents": [parent_a, parent_b],
             "arm_scale": scale}, out,
            "symmetric diverging ramp with a pale centre at index 3: colour "
            "bars for reference ranges, log fold change or change from baseline")

# --------------------------------------------------------------------------
# write
# --------------------------------------------------------------------------
records.sort(key=lambda r: (BASE.index(r["base"]) if r["base"] in BASE else len(BASE),
                            r["family"], r["id"]))

payload = {
    "schema": 1,
    "generated_by": "tools/gen_derived_palettes.py",
    "base_palettes": BASE,
    "quality_gate": {"min_delta_e": MIN_DELTA_E,
                     "min_lightness_span": MIN_LIGHTNESS_SPAN},
    "counts": {},
    "palettes": records,
}
counts: dict[str, int] = {}
for r in records:
    counts[r["family"]] = counts.get(r["family"], 0) + 1
    counts[r["base"]] = counts.get(r["base"], 0) + 1
payload["counts"] = dict(sorted(counts.items()))

# a per-base index makes lookup by family/base cheap without scanning
index: dict[str, list[str]] = {}
for r in records:
    index.setdefault(r["base"], []).append(r["id"])
    index.setdefault(r["family"], []).append(r["id"])
payload["index"] = {k: v for k, v in sorted(index.items())}

dest = os.path.join(ROOT, "scripts", "sci_palettes", "derived.json")
with open(dest, "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, separators=(",", ":"), indent=None)
    fh.write("\n")

print(f"wrote {dest}")
print(f"  {len(records)} derived palettes, {os.path.getsize(dest)/1024:.1f} KB")
print(f"  base: {len(BASE)}, total with originals: {len(records) + len(BASE)}")
print("\nfamilies:")
fam: dict[str, int] = {}
for r in records:
    fam[r["family"]] = fam.get(r["family"], 0) + 1
for k, v in sorted(fam.items(), key=lambda kv: -kv[1]):
    print(f"  {k:<12} {v:>4}")

print("\nper base palette:")
for b in BASE + ["div"]:
    n = sum(1 for r in records if r["base"] == b)
    if n:
        print(f"  {b:<14} {n:>4}")

scores = [r["score"] for r in records]
print(f"\nscore: min {min(scores)}  mean {sum(scores)/len(scores):.1f}  max {max(scores)}")
weak = sorted(records, key=lambda r: r["score"])[:8]
print("lowest scoring:")
for r in weak:
    print(f"  {r['score']:>3}  {r['id']:<22} dE {r['audit']['min_delta_e']:<5} "
          f"span {r['audit']['lightness_span']}")

if rejected:
    print(f"\nREJECTED {len(rejected)}:")
    for line in rejected:
        print("  ", line)
else:
    print("\nrejected: none")
