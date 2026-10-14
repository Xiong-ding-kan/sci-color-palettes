# -*- coding: utf-8 -*-
"""Command line interface: ``python -m sci_palettes <command>``.

Commands
--------
list                          the six published palettes with swatches
show <palette>                detail any palette (published or generated)
check [palette ...]           colour-vision / contrast audit
export <palette> <file>       write .json .css .scss .ase .gpl .jasc
sheet <file.png>              render a swatch sheet for the README
suggest <field>               rank palettes for clinical / database / basic work
search <#hex>                 find palettes containing a colour
"""

from __future__ import annotations

import argparse
import sys

from .core import check, lookup, palette, report, resolve
from .data import PALETTES, PALETTE_ORDER
from .exporters import export, preview, swatches


def _cmd_list(args) -> int:
    print(preview(args.palettes or None, per_line=args.per_line))
    print("\nids: " + ", ".join(PALETTE_ORDER))
    print(f"plus {len(_derived_names())} generated variants "
          f"(e.g. glacier-h030, burgundy-clin-hi, sage-mono)")
    print("Chinese names also work, e.g. sci_palettes show 冰川蓝绿")
    return 0


def _derived_names() -> list[str]:
    from . import derived
    return derived.derived_names()


def _cmd_show(args) -> int:
    pid = resolve(args.palette)
    info = lookup(pid)
    print(f"{info['name_zh']}  ·  {info['name_en']}   [{pid}]")
    print(f"  {info['subtitle_zh']}")
    print()
    print(swatches(info["hex"]))
    if pid in PALETTES:
        print()
        for c, r in zip(info["hex"], info["roles"]):
            print(f"  {c}   {r}")
    print()
    print(report(pid))
    from . import derived
    if pid not in PALETTES:
        a = derived.applications(pid)
        print("scores       " + ", ".join(f"{k} {v}" for k, v in a["scores"].items()))
        print("fits         " + ", ".join(k for k, v in a["fit"].items() if v) or "none")
    return 0


def _cmd_suggest(args) -> int:
    from . import derived
    rows = derived.suggest_for(args.field, n=args.number,
                               require_fit=args.require_fit)
    if not rows:
        print(f"no palette clears the gates for {args.field!r}",
              file=sys.stderr)
        return 2
    print(f"{args.field}: {len(rows)} palettes"
          + (" (all clear the field's hard gates)" if args.require_fit else ""))
    print()
    for r in rows:
        print(f"  {r['score']:>3}  {r['id']:<24} {'fit' if r['fits'] else '   '}  "
              f"{r['name_zh']}")
        print(f"       {swatches(r['hex'])}")
        print(f"       {r['why']}")
    return 0


def _cmd_search(args) -> int:
    from . import derived
    rows = derived.search(args.colour, limit=args.number)
    if not rows:
        print(f"no palette contains a colour within tolerance of {args.colour!r}",
              file=sys.stderr)
        return 2
    for r in rows:
        print(f"  {r['id']:<24} closest {r['closest']} (dE {r['delta_e']}, "
              f"position {r['position']})  score {r['score']}")
        print(f"       {swatches(r['hex'])}")
    return 0


def _cmd_check(args) -> int:
    ids = [resolve(p) for p in args.palettes] if args.palettes else list(PALETTE_ORDER)
    worst = 0
    for pid in ids:
        print(report(pid))
        print()
        c = check(pid, min_delta_e=args.min_delta_e)
        worst = max(worst, len(c["hard_pairs"]))
    if worst:
        print(f"NOTE: {worst} close pair(s) found at CIE76 < {args.min_delta_e}. "
              "Prefer non-adjacent colours or add marker/linestyle coding for those.")
    return 0


def _cmd_export(args) -> int:
    written = export(args.path, [args.palette] if args.palette else None)
    print(f"wrote {written}")
    return 0


def _cmd_sheet(args) -> int:
    try:
        from .mpl import swatch_figure
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("rendering a sheet needs matplotlib: pip install matplotlib", file=sys.stderr)
        return 2
    palettes = args.palettes or None
    fig = swatch_figure(palettes)
    fig.savefig(args.path, dpi=args.dpi)
    print(f"wrote {args.path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="sci_palettes",
        description="科研配色 / scientific colour schemes "
                    "(6 published palettes + 178 generated variants)")
    sub = p.add_subparsers(dest="command")

    s = sub.add_parser("list", help="show the published palettes with swatches")
    s.add_argument("palettes", nargs="*")
    s.add_argument("--per-line", type=int, default=8)
    s.set_defaults(func=_cmd_list)

    s = sub.add_parser("show", help="detail one palette, published or generated")
    s.add_argument("palette")
    s.set_defaults(func=_cmd_show)

    s = sub.add_parser("check", help="colour-vision and contrast audit")
    s.add_argument("palettes", nargs="*")
    s.add_argument("--min-delta-e", type=float, default=12.0)
    s.set_defaults(func=_cmd_check)

    s = sub.add_parser("export", help="write palette files")
    s.add_argument("palette", nargs="?", default=None,
                   help="a palette id, or 'all' for every palette")
    s.add_argument("path")
    s.set_defaults(func=_cmd_export)

    s = sub.add_parser("sheet", help="render a swatch sheet png")
    s.add_argument("path")
    s.add_argument("palettes", nargs="*")
    s.add_argument("--dpi", type=int, default=300)
    s.set_defaults(func=_cmd_sheet)

    s = sub.add_parser("suggest", help="rank palettes for a research field")
    s.add_argument("field",
                   help="clinical / database / basic / general "
                        "(中文也行: 临床 / 数据库 / 基础 / 通用)")
    s.add_argument("-n", "--number", type=int, default=8)
    s.add_argument("--require-fit", action="store_true",
                   help="only palettes that clear every hard gate for the field")
    s.set_defaults(func=_cmd_suggest)

    s = sub.add_parser("search", help="find palettes containing a colour")
    s.add_argument("colour", help="a hex colour, e.g. #315C6B")
    s.add_argument("-n", "--number", type=int, default=6)
    s.set_defaults(func=_cmd_search)
    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 1
    try:
        return args.func(args)
    except KeyError as exc:
        print(exc.args[0], file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
