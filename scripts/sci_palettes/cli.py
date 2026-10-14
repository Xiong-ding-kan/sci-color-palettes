# -*- coding: utf-8 -*-
"""Command line interface: ``python -m sci_palettes <command>``.

Commands
--------
list                          show every palette with swatches
show <palette>                detail one palette (ramp, roles, audit)
check [palette ...]           colour-vision / contrast audit
export <palette> <file>       write .json .css .scss .ase .gpl .jasc
sheet <file.png>              render a swatch sheet for the README
"""

from __future__ import annotations

import argparse
import sys

from .core import check, palette, report, resolve
from .data import PALETTES, PALETTE_ORDER
from .exporters import export, preview, swatches


def _cmd_list(args) -> int:
    print(preview(args.palettes or None, per_line=args.per_line))
    print("\nids: " + ", ".join(PALETTE_ORDER))
    print("Chinese names also work, e.g. sci_palettes show 冰川蓝绿")
    return 0


def _cmd_show(args) -> int:
    pid = resolve(args.palette)
    info = PALETTES[pid]
    print(f"{info['name_zh']}  ·  {info['name_en']}   [{pid}]")
    print(f"  {info['subtitle_zh']}  /  {info['subtitle_en']}")
    print(f"  mood: {info['vibe']}")
    print()
    print(swatches(info["hex"]))
    print()
    for c, r in zip(info["hex"], info["roles"]):
        print(f"  {c}   {r}")
    print()
    print(report(pid))
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
    p = argparse.ArgumentParser(prog="sci_palettes",
                                description="六套科研配色 / six scientific colour schemes")
    sub = p.add_subparsers(dest="command")

    s = sub.add_parser("list", help="show every palette with swatches")
    s.add_argument("palettes", nargs="*")
    s.add_argument("--per-line", type=int, default=8)
    s.set_defaults(func=_cmd_list)

    s = sub.add_parser("show", help="detail one palette")
    s.add_argument("palette")
    s.set_defaults(func=_cmd_show)

    s = sub.add_parser("check", help="colour-vision and contrast audit")
    s.add_argument("palettes", nargs="*")
    s.add_argument("--min-delta-e", type=float, default=12.0)
    s.set_defaults(func=_cmd_check)

    s = sub.add_parser("export", help="write palette files")
    s.add_argument("palette", nargs="?", default=None)
    s.add_argument("path")
    s.set_defaults(func=_cmd_export)

    s = sub.add_parser("sheet", help="render a swatch sheet png")
    s.add_argument("path")
    s.add_argument("palettes", nargs="*")
    s.add_argument("--dpi", type=int, default=300)
    s.set_defaults(func=_cmd_sheet)
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
