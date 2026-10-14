# -*- coding: utf-8 -*-
"""Measure the library's metric distributions.

The application thresholds in ``gen_applications.py`` are calibrated against the
numbers this prints, so run it before changing any floor or ceiling there -
otherwise the gates drift away from what the palettes actually deliver.

Run:  python tools/measure_distribution.py
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


def quantiles(values, ps=(0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0)):
    v = sorted(values)
    return [v[min(len(v) - 1, int(p * (len(v) - 1)))] for p in ps]


def main() -> int:
    apps = sp.applications if hasattr(sp, "applications") else None
    if apps is None:
        print("sci_palettes.applications is unavailable", file=sys.stderr)
        return 2

    ids = list(PALETTES) + sp.derived_names()
    rows = {pid: apps(pid)["metrics"] for pid in ids}
    metrics = ("min8", "min5", "cvd5", "cvd8", "span8", "dark", "hue_spread")

    print(f"n = {len(rows)} palettes "
          f"({len(PALETTES)} published + {len(sp.derived_names())} generated)\n")
    header = (f"{'metric':<11} {'min':>7} {'p10':>7} {'p25':>7} "
              f"{'median':>7} {'p75':>7} {'p90':>7} {'max':>7}")
    print(header)
    print("-" * len(header))
    for m in metrics:
        q = quantiles([r[m] for r in rows.values()])
        print(f"{m:<11} " + " ".join(f"{x:>7.1f}" for x in q))

    print("\nper family (median, max):")
    fams: dict[str, list[dict]] = {}
    for pid, m in rows.items():
        fams.setdefault(sp.get(pid).get("family", "published"), []).append(m)
    for fam, ms in sorted(fams.items(),
                          key=lambda kv: -statistics.median(x["min5"] for x in kv[1])):
        print(f"  {fam:<12} n={len(ms):>3}  "
              f"min5 med {statistics.median(x['min5'] for x in ms):6.1f}  "
              f"cvd5 med {statistics.median(x['cvd5'] for x in ms):6.1f}  "
              f"span8 med {statistics.median(x['span8'] for x in ms):.2f}")

    gates = sp.profiles()
    print("\nhow many clear each profile's hard gates:")
    for field, prof in gates.items():
        n = sum(1 for pid in ids
                if sp.applications(pid)["fit"][field])
        print(f"  {field:<9} {n:>4}  (score floor {prof['score_gate']}, "
              f"gates {prof['gate'] or 'none'})")

    print("\nsuggested floors if you recalibrate (roughly the 10th percentile):")
    for m in ("min5", "cvd5", "span8", "dark"):
        q = quantiles([r[m] for r in rows.values()])
        print(f"  {m:<8} p10 = {q[1]:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
