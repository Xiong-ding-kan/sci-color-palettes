# -*- coding: utf-8 -*-
"""Terminal previews and file exports (JSON / CSS / SCSS / ASE / GPL / JASC)."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone

from .core import as_hex, as_rgb, lookup, palette, resolve
from .data import PALETTES, PALETTE_ORDER

__all__ = [
    "swatches", "preview", "to_json", "to_css", "to_scss", "to_gpl",
    "to_jasc", "to_ase", "export", "resolve_names",
]

# 24-bit ANSI block; falls back to the hex text when colour is unsupported.
_BLOCK = "\u2588\u2588\u2588"


def resolve_names(names=None) -> list[str]:
    """Normalise an export target list.

    ``None`` (default) means the six published palettes, so exports stay small;
    pass ``"all"`` or ``"derived"`` to include the generated variants.
    """
    if names is None:
        return list(PALETTE_ORDER)
    if isinstance(names, str):
        if names in ("all", "everything"):
            from . import derived
            return list(PALETTE_ORDER) + derived.derived_names()
        if names == "derived":
            from . import derived
            return derived.derived_names()
        return [resolve(names)]
    return [resolve(n) for n in names]


def _export_record(pid: str) -> dict:
    """Public metadata only: internal audit scores stay out of export files."""
    info = dict(lookup(pid))
    for k in ("audit", "score", "transform", "family", "base"):
        info.pop(k, None)
    return info


def swatches(colours, per_line: int = 8) -> str:
    """ANSI truecolour swatch strip."""
    cols = as_hex(colours)
    out = []
    for c in cols:
        r, g, b = as_rgb([c])[0]
        out.append(f"\x1b[48;2;{r};{g};{b}m{_BLOCK}\x1b[0m {c}")
    lines = ["  ".join(out[i:i + per_line]) for i in range(0, len(out), per_line)]
    return "\n".join(lines)


def preview(names=None, per_line: int = 8) -> str:
    """Terminal report for one or more palettes."""
    ids = resolve_names(names)
    blocks = []
    for pid in ids:
        info = lookup(pid)
        blocks.append(
            f"{info['name_zh']}  ·  {info['name_en']}   [{pid}]\n"
            f"  {info['subtitle_zh']}\n"
            f"{swatches(info['hex'], per_line)}"
        )
    return "\n\n".join(blocks)


# --------------------------------------------------------------------------
# exporters
# --------------------------------------------------------------------------

def to_json(path: str, names=None) -> str:
    ids = [resolve(n) for n in names] if names else list(PALETTE_ORDER)
    payload = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "科研配色 series, WeChat Official Accounts (see references/sources.md)",
        "palettes": {pid: PALETTES[pid] for pid in ids},
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    return path


def to_css(path: str, prefix: str = "sci", names=None) -> str:
    """Write CSS custom properties. Returns the path, or the text if path is ''. """
    ids = [resolve(n) for n in names] if names else list(PALETTE_ORDER)
    lines = ["/* sci-color-palettes - generated file, do not edit by hand */",
             ":root {"]
    for pid in ids:
        info = PALETTES[pid]
        lines.append(f"  /* {info['name_zh']} / {info['name_en']} - {info['subtitle_en']} */")
        for i, c in enumerate(info["hex"], 1):
            lines.append(f"  --{prefix}-{pid.replace('_', '-')}-{i}: {c};")
    lines.append("}")
    text = "\n".join(lines) + "\n"
    if path:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path
    return text


def to_scss(path: str, names=None) -> str:
    """Write SCSS maps and lists. Returns the path, or the text if path is ''."""
    ids = [resolve(n) for n in names] if names else list(PALETTE_ORDER)
    lines = ["// sci-color-palettes - generated file, do not edit by hand"]
    for pid in ids:
        info = PALETTES[pid]
        lines.append(f"// {info['name_zh']} / {info['name_en']}")
        lines.append(f"${pid}: (")
        for i, c in enumerate(info["hex"], 1):
            lines.append(f"  {i}: {c},")
        lines.append(");")
        lines.append(f"${pid}-list: {' '.join(info['hex'])};")
        lines.append("")
    text = "\n".join(lines)
    if path:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path
    return text


def to_gpl(path: str, name: str = "glacier") -> str:
    """GIMP / Inkscape / Aseprite friendly .gpl palette."""
    pid = resolve(name)
    info = PALETTES[pid]
    lines = ["GIMP Palette", f"Name: {info['name_en']} ({pid})",
             f"Columns: {len(info['hex'])}", "#"]
    for i, h in enumerate(info["hex"], 1):
        r, g, b = as_rgb([h])[0]
        lines.append(f"{r:3d} {g:3d} {b:3d}\t{pid}-{i} {h}")
    text = "\n".join(lines) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def to_jasc(path: str, name: str = "glacier") -> str:
    """JASC-PAL, readable by Paint Shop Pro, Procreate, some CAD tools."""
    pid = resolve(name)
    info = PALETTES[pid]
    lines = ["JASC-PAL", "0100", str(len(info["hex"]))]
    for h in info["hex"]:
        r, g, b = as_rgb([h])[0]
        lines.append(f"{r} {g} {b}")
    text = "\n".join(lines) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def to_ase(path: str, names=None) -> str:
    """Adobe Swatch Exchange (.ase), importable by Adobe/Inkscape/Affinity.

    Supports RGB entries only, which is what these palettes are.
    """
    import struct
    ids = [resolve(n) for n in names] if names else list(PALETTE_ORDER)

    groups = b""
    n_colors = 0
    for pid in ids:
        info = PALETTES[pid]
        label = f"{info['name_en']} {info['name_zh']}"
        name_utf16 = label.encode("utf-16-be") + b"\x00\x00"
        block = b""
        for i, h in enumerate(info["hex"], 1):
            r, g, b = as_rgb([h])[0]
            cname = f"{pid}-{i}".encode("utf-16-be") + b"\x00\x00"
            body = (struct.pack(">H", len(cname)) + cname +
                    b"RGB " + struct.pack(">fff", r / 255, g / 255, b / 255) +
                    struct.pack(">H", 0))
            block += struct.pack(">H", 0x0001) + struct.pack(">I", len(body)) + body
            n_colors += 1
        gbody = (struct.pack(">H", len(name_utf16)) + name_utf16 + block +
                 struct.pack(">H", 0xC002) + struct.pack(">I", 0))
        groups += struct.pack(">H", 0xC001) + struct.pack(">I", len(gbody)) + gbody
    data = (b"ASEF" + struct.pack(">HH", 1, 0) +
            struct.pack(">I", n_colors + 2 * len(ids)) + groups)
    with open(path, "wb") as fh:
        fh.write(data)
    return path


_EXPORTERS = {
    ".json": lambda p, n: to_json(p, n),
    ".css": lambda p, n: to_css(p),
    ".scss": lambda p, n: to_scss(p),
    ".ase": lambda p, n: to_ase(p, n),
}


def export(path: str, names=None) -> str:
    """Dispatch on file extension: .json .css .scss .ase .gpl .jasc/.pal."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".gpl",):
        return to_gpl(path, (names or ["glacier"])[0] if names else "glacier")
    if ext in (".jasc", ".pal"):
        return to_jasc(path, (names or ["glacier"])[0] if names else "glacier")
    fn = _EXPORTERS.get(ext)
    if not fn:
        raise ValueError(f"unsupported export extension {ext!r}; "
                         f"use one of {', '.join(sorted(set(_EXPORTERS) | {'.gpl', '.jasc'}))}")
    return fn(path, names)
