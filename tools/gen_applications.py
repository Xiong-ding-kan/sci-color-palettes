# -*- coding: utf-8 -*-
"""Recommend palettes for basic research vs clinical research.

Clinical and database work has requirements that basic-research figures do not,
so the groups are scored on different criteria rather than on overall palette
quality:

* **clinical / database** - medical journals expect colour-blind-safe figures,
  and clinical panels (survival curves, forest plots, adverse-event stacks,
  subgroup tables) must survive greyscale printing. Colour-vision separation,
  pairwise distinctness and having dark members to label with dominate.
* **basic research** - panels get photocopied and read in greyscale, and
  omics/materials figures carry meaning in sequential scales, so the lightness
  span dominates while chroma is held back.

Thresholds are calibrated against the measured distribution of this library
(see ``tools/_probe_metrics.py``), not guessed. Figures rarely use all eight
members of a ramp, so separation is also measured on the best 5-colour subset
- the way the palette is actually used.

The classifier is metric-based, so every palette is judged by the same rules and
the output is reproducible.

Run:  python tools/gen_applications.py
"""

import io
import json
import math
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, HERE)

from _color_ops import to_lch  # noqa: E402
import sci_palettes as sp  # noqa: E402
from sci_palettes.data import PALETTES  # noqa: E402

DERIVED = os.path.join(ROOT, "scripts", "sci_palettes", "derived.json")

# Measured medians for this library: min5 14.8, cvd5 7.0, span8 0.60, dark 1.
# "worst" is the level below which a palette should not be recommended for that
# job; "best" is where it stops earning more credit.
# Every metric is (floor, ceiling, weight): satisfaction is 0 at the floor and
# 1 at the ceiling. Floors and ceilings are set from the measured distribution
# of this library (tools/_probe_metrics.py), not guessed. A weight may be
# negative, for a trait the field explicitly does not want.
#
# "gate" is the pass/fail test applied on top of the score: a palette can score
# well and still be refused for a job whose hard requirement it misses.
PROFILES = {
    "clinical": {
        "label_zh": "临床研究",
        "label_en": "Clinical research",
        "criteria": {
            "cvd5": (5.0, 14.0, 0.30),
            "min5": (9.0, 22.0, 0.25),
            "dark": (2, 5, 0.25),
            "span8": (0.45, 0.80, 0.20),
            # clinical panels overlay text on colour: high-saturation ramps
            # vibrate and make annotations harder to read
            "hue_spread": (40.0, 170.0, -0.10),
        },
        "score_gate": 50,
        "gate": {"cvd5": 5.0, "min5": 9.0, "dark": 2, "span8": 0.40},
    },
    "database": {
        "label_zh": "数据库 / 队列研究",
        "label_en": "Database / registry research",
        "criteria": {
            "min5": (10.0, 26.0, 0.30),
            "hue_spread": (60.0, 150.0, 0.25),
            "cvd5": (4.0, 13.0, 0.20),
            "dark": (1, 5, 0.15),
            "span8": (0.38, 0.72, 0.10),
        },
        "score_gate": 50,
        "gate": {"min5": 10.0, "hue_spread": 60.0},
    },
    "basic": {
        "label_zh": "基础科研",
        "label_en": "Basic research",
        "criteria": {
            "span8": (0.45, 0.80, 0.35),
            "min5": (8.0, 22.0, 0.25),
            "cvd5": (4.0, 13.0, 0.25),
            "dark": (1, 5, 0.15),
        },
        "score_gate": 50,
        "gate": {"span8": 0.45, "cvd5": 4.0},
    },
    # A permissive profile so the library is fully covered: these schemes suit
    # a mixed figure or a field we do not specialise for, rather than being
    # unusable. No gate of its own - the score already combines span,
    # separation and dark-member count.
    "general": {
        "label_zh": "通用 / 跨学科",
        "label_en": "General / cross-disciplinary",
        "criteria": {
            "span8": (0.40, 0.75, 0.35),
            "min5": (7.0, 20.0, 0.35),
            "dark": (0, 4, 0.30),
        },
        "score_gate": 40,
        "gate": {},
    },
}


_DERIVED_CACHE: dict | None = None


def derived_data() -> dict:
    """The derived.json payload, loaded once, with an id -> hex shortcut added."""
    global _DERIVED_CACHE
    if _DERIVED_CACHE is None:
        with open(DERIVED, encoding="utf-8") as fh:
            _DERIVED_CACHE = json.load(fh)
        _DERIVED_CACHE["_by_id"] = {r["id"]: r["hex"]
                                    for r in _DERIVED_CACHE["palettes"]}
    return _DERIVED_CACHE


def _cols(pid: str) -> list[str]:
    if pid in PALETTES:
        return PALETTES[pid]["hex"]
    return derived_data()["_by_id"][pid]


def _min_pair(cols) -> float:
    return min(sp.delta_e(a, b) for i, a in enumerate(cols) for b in cols[i + 1:])


def _cvd_min(cols, kind) -> float:
    sim = sp.simulate_cvd(cols, kind)
    return min(sp.delta_e(a, b) for i, a in enumerate(sim) for b in sim[i + 1:])


def hue_spread(cols) -> float:
    """Circular spread of the chromatic hues, in degrees (0-180).

    High values mean different colour families, which is what lets a reader
    tell a cohort from a centre from a site at a glance.
    """
    lch = [to_lch(c) for c in cols]
    chroma = [C for _, C, _ in lch]
    if sum(chroma) < 1e-6:
        return 0.0
    x = sum(C * math.cos(math.radians(h)) for _, C, h in lch) / sum(chroma)
    y = sum(C * math.sin(math.radians(h)) for _, C, h in lch) / sum(chroma)
    R = min(1.0, math.hypot(x, y))
    return math.degrees(math.sqrt(-2.0 * math.log(max(R, 1e-9))))


def metrics(pid: str) -> dict:
    cols = _cols(pid)
    sub5 = sp.select(cols, min(5, len(cols)))
    lums = [sp.luminance(c) for c in cols]
    lch = [to_lch(c)[0] for c in cols]
    ci = len(cols) // 2
    return {
        "n": len(cols),
        "min8": round(_min_pair(cols), 1),
        "min5": round(_min_pair(sub5), 1),
        "cvd8": round(_cvd_min(cols, sp.DEUTERANOPIA), 1),
        "cvd5": round(_cvd_min(sub5, sp.DEUTERANOPIA), 1),
        "cvd5_pro": round(_cvd_min(sub5, sp.PROTANOPIA), 1),
        "span8": round(max(lums) - min(lums), 3),
        "dark": sum(1 for c in cols if sp.contrast_ratio(c, "#FFFFFF") >= 4.5),
        "hue_spread": round(hue_spread(cols), 1),
        "arm_monotone": (all(lch[i] <= lch[i + 1] + 0.5 for i in range(ci))
                         and all(lch[i] >= lch[i + 1] - 0.5
                                 for i in range(ci, len(lch) - 1))),
        "is_scale": pid.startswith("div-"),
        "best5": sub5,
    }


def sat(value: float, worst: float, best: float) -> float:
    if best == worst:
        return 1.0
    return max(0.0, min(1.0, (value - worst) / (best - worst)))


def classify(pid: str, m: dict | None = None) -> dict:
    m = m or metrics(pid)
    scores = {}
    for name, prof in PROFILES.items():
        s = sum(w * sat(m[k], lo, hi)
                for k, (lo, hi, w) in prof["criteria"].items())
        scores[name] = max(0, round(100 * s))
    # A diverging ramp is a tool for continuous data, not a categorical
    # palette: it serves reference ranges and fold-changes, not group series.
    if m["is_scale"]:
        scores = {k: int(v * 0.55) for k, v in scores.items()}
    fit = {}
    for name, prof in PROFILES.items():
        if m["is_scale"]:
            # a diverging ramp is a colour bar, not a categorical palette: it
            # never satisfies a "pick N series" gate, however well it scores
            fit[name] = False
            continue
        ok = scores[name] >= prof["score_gate"]
        for key, need in prof["gate"].items():
            ok = ok and m[key] >= need
        fit[name] = ok
    return {
        "scores": scores,
        "fit": fit,
        "primary": max(scores, key=lambda k: scores[k]),
        "metrics": {k: v for k, v in m.items() if k != "best5"},
    }


if __name__ == "__main__":
    data = derived_data()
    ids = list(PALETTES) + [r["id"] for r in data["palettes"]]

    out = {}
    for pid in ids:
        m = metrics(pid)
        c = classify(pid, m)
        c["derived"] = pid not in PALETTES
        # best5 is recomputable with sp.select(pid, 5); keep it out of the file
        out[pid] = c

    dest = os.path.join(ROOT, "scripts", "sci_palettes", "applications.json")
    payload = {
        "schema": 1,
        "generated_by": "tools/gen_applications.py",
        "note": "separation is measured on the best 5-colour subset as well as "
                "on all 8 members, because figures rarely use all eight",
        "profiles": {k: {"label_zh": v["label_zh"], "label_en": v["label_en"],
                         "criteria": {c: list(t) for c, t in v["criteria"].items()},
                         "score_gate": v["score_gate"], "gate": v["gate"]}
                     for k, v in PROFILES.items()},
        "palettes": out,
    }
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write("\n")
    print(f"wrote {dest}  ({os.path.getsize(dest)/1024:.1f} KB, {len(out)} palettes)\n")

    for name, prof in PROFILES.items():
        fit = [p for p in ids if out[p]["fit"][name]]
        print(f"{prof['label_zh']} ({name}): {len(fit)} fit "
              f"({sum(1 for p in fit if out[p]['derived'])} generated)")
        for p in sorted(fit, key=lambda p: -out[p]["scores"][name])[:8]:
            print(f"   {out[p]['scores'][name]:>3}  {p:<24} "
                  f"min5={out[p]['metrics']['min5']:>5} cvd5={out[p]['metrics']['cvd5']:>5} "
                  f"span={out[p]['metrics']['span8']:.2f} dark={out[p]['metrics']['dark']}")
        print()

    both = [p for p in ids if out[p]["fit"]["clinical"] and out[p]["fit"]["database"]]
    print(f"fit clinical AND database: {len(both)}: {', '.join(both[:12])}")
    none = [p for p in ids if not any(out[p]["fit"].values())]
    print(f"fit nothing: {len(none)}")
