# -*- coding: utf-8 -*-
"""Colour maths and palette helpers for the sci-color-palettes skill.

Pure stdlib; matplotlib is imported only by :mod:`sci_palettes.mpl`.
"""

from __future__ import annotations

import colorsys
import math
import re

from .data import ALIASES, PALETTE_ORDER, PALETTES

__all__ = [
    "resolve", "info", "lookup", "names", "palette", "as_hex", "as_rgb",
    "as_rgb01", "as_hsl", "luminance", "contrast_ratio", "wcag_level",
    "delta_e", "nearest", "sort_by_luminance", "lighten", "darken", "mix",
    "sub", "select", "ramp", "to_colormap_stops", "check", "report",
    "hex_to_rgb", "rgb_to_hex", "PROTANOPIA", "DEUTERANOPIA", "TRITANOPIA",
    "ACHROMATOPSIA", "simulate_cvd", "cvd_matrix",
]

_HEX_RE = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


# --------------------------------------------------------------------------
# basics
# --------------------------------------------------------------------------

def hex_to_rgb(value: str) -> tuple[int, int, int]:
    """'#538A95' or '538A95' or '#4AF' -> (83, 138, 149)."""
    m = _HEX_RE.match(value.strip() if isinstance(value, str) else "")
    if not m:
        raise ValueError(f"not a hex colour: {value!r}")
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(rgb) -> str:
    r, g, b = (max(0, min(255, int(round(c)))) for c in rgb[:3])
    return f"#{r:02X}{g:02X}{b:02X}"


def names() -> list[str]:
    """Canonical palette ids, in the order of the source series."""
    return list(PALETTE_ORDER)


def resolve(name: str) -> str:
    """Map any alias (Chinese name, English name, shorthand, derived id) to an id.

    Anchor palettes are checked first; the generated variants are consulted
    only if nothing matches, so this stays fast for the common case.
    """
    if not isinstance(name, str):
        raise TypeError("palette name must be a string")
    key = name.strip()
    if key in PALETTES:
        return key
    hit = ALIASES.get(key) or ALIASES.get(key.lower())
    if hit:
        return hit
    # generated variants (hue rotations, temperature drift, blends, ...)
    try:
        from . import derived
        avail = derived._by_id()
        if key in avail:
            return key
        low = {k.lower(): k for k in avail}
        if key.lower() in low:
            return low[key.lower()]
    except (ImportError, FileNotFoundError, KeyError):
        pass
    raise KeyError(
        f"unknown palette {name!r}; {len(PALETTES)} anchor palettes: "
        f"{', '.join(PALETTE_ORDER)} "
        f"(aliases include the Chinese names, e.g. '冰川蓝绿'); "
        f"plus generated variants such as 'glacier-h030' or 'glacier-warm' "
        f"- list them with sci_palettes.derived_names()"
    )


def info(name: str) -> dict:
    """Metadata for any palette, anchor or generated."""
    from . import derived
    return derived.get(name)


def lookup(name: str) -> dict:
    """Registry record for any palette: the one accessor the rest of the
    package uses, so anchor and generated palettes behave identically."""
    pid = resolve(name)
    if pid in PALETTES:
        return PALETTES[pid]
    from . import derived
    return derived.all_palettes()[pid]


def palette(name: str, key: str = "hex") -> list:
    """Colours of one palette as a list of hex strings (or 'rgb'/'roles')."""
    p = lookup(name)
    if key == "roles":
        return list(p["roles"])
    if key == "rgb":
        return [hex_to_rgb(h) for h in p["hex"]]
    if key == "info":
        return dict(p)
    return list(p["hex"])


def as_hex(colours) -> list[str]:
    return [c if isinstance(c, str) else rgb_to_hex(c) for c in colours]


def as_rgb(colours) -> list[tuple[int, int, int]]:
    return [hex_to_rgb(c) if isinstance(c, str) else tuple(c) for c in colours]


def as_rgb01(colours) -> list[tuple[float, float, float]]:
    return [(r / 255, g / 255, b / 255) for r, g, b in as_rgb(colours)]


def as_hsl(colours) -> list[tuple[float, float, float]]:
    """(hue 0-360, saturation 0-1, lightness 0-1)."""
    out = []
    for r, g, b in as_rgb01(colours):
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        out.append((h * 360.0, s, l))
    return out


def sub(name: str, n: int, start: int = 0) -> list[str]:
    """``n`` consecutive colours from a palette.

    Consecutive members of a ramp always stay harmonious, so this is the
    correct way to shrink a palette for a 3-group figure.
    """
    cols = palette(name)
    if n > len(cols):
        raise ValueError(f"{name} has only {len(cols)} colours, asked for {n}")
    end = start + n
    if end > len(cols):
        start, end = len(cols) - n, len(cols)
    return cols[start:end]


# --------------------------------------------------------------------------
# luminance / contrast
# --------------------------------------------------------------------------

def _lin(c: float) -> float:
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(colour) -> float:
    """WCAG relative luminance, 0 (black) .. 1 (white)."""
    r, g, b = hex_to_rgb(colour) if isinstance(colour, str) else tuple(colour)
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast_ratio(a, b) -> float:
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def wcag_level(a, b) -> str:
    """WCAG 2.x verdict for a colour pair."""
    r = contrast_ratio(a, b)
    if r >= 7:
        return "AAA"
    if r >= 4.5:
        return "AA"
    if r >= 3:
        return "AA-large"
    return "fail"


def sort_by_luminance(colours) -> list[str]:
    return sorted(as_hex(colours), key=luminance)


# --------------------------------------------------------------------------
# perceptual distance (CIE Lab / CIE76) - good enough for palette work
# --------------------------------------------------------------------------

def _srgb_to_lab(colour) -> tuple[float, float, float]:
    r, g, b = (hex_to_rgb(colour) if isinstance(colour, str) else tuple(colour))
    r, g, b = _lin(r), _lin(g), _lin(b)
    # sRGB -> XYZ (D65)
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047
    y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b) / 1.00000
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else (7.787 * t + 16 / 116)

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e(a, b) -> float:
    """CIE76 colour difference; < 10 means "hard to tell apart"."""
    la, aa, ba = _srgb_to_lab(a)
    lb, ab, bb = _srgb_to_lab(b)
    return math.sqrt((la - lb) ** 2 + (aa - ab) ** 2 + (ba - bb) ** 2)


def nearest(colour, candidates) -> str:
    """Closest candidate by CIE76 distance."""
    return min(as_hex(candidates), key=lambda c: delta_e(colour, c))


# --------------------------------------------------------------------------
# manipulation (interpolation happens in Lab space for smooth ramps)
# --------------------------------------------------------------------------

def _lab_to_srgb(L, a, b) -> tuple[int, int, int]:
    fy = (L + 16) / 116
    fx = fy + a / 500
    fz = fy - b / 200

    def finv(t):
        return t ** 3 if t ** 3 > 0.008856 else (t - 16 / 116) / 7.787

    x = 0.95047 * finv(fx)
    y = 1.00000 * finv(fy)
    z = 1.08883 * finv(fz)

    r = 3.2404542 * x - 1.5371385 * y - 0.4985314 * z
    g = -0.9692660 * x + 1.8760108 * y + 0.0415560 * z
    bb = 0.0556434 * x - 0.2040259 * y + 1.0572252 * z

    def gam(t):
        t = max(0.0, min(1.0, t))
        return 12.92 * t if t <= 0.0031308 else 1.055 * t ** (1 / 2.4) - 0.055

    return tuple(int(round(gam(c) * 255)) for c in (r, g, bb))


def mix(a, b, t: float = 0.5) -> str:
    """Perceptual blend; ``t``=0 gives ``a``, ``t``=1 gives ``b``."""
    t = max(0.0, min(1.0, float(t)))
    la, aa, ba = _srgb_to_lab(a)
    lb, ab, bb = _srgb_to_lab(b)
    return rgb_to_hex(_lab_to_srgb(la + (lb - la) * t, aa + (ab - aa) * t, ba + (bb - ba) * t))


def lighten(colour, amount: float = 0.2) -> str:
    return mix(colour, "#FFFFFF", amount)


def darken(colour, amount: float = 0.2) -> str:
    return mix(colour, "#000000", amount)


def ramp(colours, n: int, keep_ends: bool = True) -> list[str]:
    """Resample to exactly ``n`` perceptually-even colours by *blending*.

    Use this for continuous work (colormaps, gradient fills). For discrete
    categories prefer :func:`select`, which keeps the original hues instead of
    inventing in-between ones.
    """
    cols = as_hex(colours)
    if n <= 0:
        raise ValueError("n must be positive")
    if n == 1:
        return [cols[len(cols) // 2]]
    if len(cols) == 1:
        return cols * n
    out = []
    for i in range(n):
        pos = i / (n - 1) * (len(cols) - 1)
        lo = int(math.floor(pos))
        hi = min(lo + 1, len(cols) - 1)
        out.append(mix(cols[lo], cols[hi], pos - lo))
    if keep_ends:
        out[0], out[-1] = cols[0], cols[-1]
    return out


def select(colours, n: int) -> list[str]:
    """Choose ``n`` colours from a ramp, keeping the original hues.

    Picks the ``n``-of-``len(colours)`` subsequence that stays closest to a
    perfectly even spread (exact dynamic program, so no greedy artefacts).
    This is what categorical plots should use: ``select(palette('sage'), 4)``
    returns four real palette colours, whereas :func:`ramp` would blend the
    green/violet/sand families together into mud.
    """
    cols = as_hex(colours)
    m = len(cols)
    if n <= 0:
        raise ValueError("n must be positive")
    if n >= m:
        return list(cols)
    if n == 1:
        return [cols[m // 2]]
    # ideal positions of the chosen indices on the 0..m-1 axis
    ideal = [i * (m - 1) / (n - 1) for i in range(n)]
    INF = float("inf")
    # cost[j] = best cost of a solution whose last chosen index is j
    cost = [INF] * m
    back = [[-1] * m for _ in range(n)]
    for j in range(m):
        cost[j] = (j - ideal[0]) ** 2
    for i in range(1, n):
        new = [INF] * m
        for j in range(i, m):
            best, arg = INF, -1
            for k in range(i - 1, j):
                if cost[k] < best:
                    best, arg = cost[k], k
            new[j] = best + (j - ideal[i]) ** 2
            back[i][j] = arg
        cost = new
    j = min(range(n - 1, m), key=lambda x: cost[x])
    idx = [j]
    for i in range(n - 1, 0, -1):
        j = back[i][j]
        idx.append(j)
    return [cols[i] for i in reversed(idx)]


def to_colormap_stops(colours) -> list[tuple[float, tuple[float, float, float]]]:
    """(position, (r,g,b) in 0-1) pairs for matplotlib LinearSegmentedColormap."""
    cols = as_hex(colours)
    n = len(cols)
    if n == 1:
        return [(0.0, as_rgb01(cols)[0]), (1.0, as_rgb01(cols)[0])]
    return [(i / (n - 1), c) for i, c in enumerate(as_rgb01(cols))]


# --------------------------------------------------------------------------
# colour-vision-deficiency simulation (Brettel/Vienot-style matrices, sRGB)
# --------------------------------------------------------------------------

def cvd_matrix(kind: str) -> list[list[float]]:
    kind = kind.lower()
    if kind in ("protan", "protanopia", "protanomaly", "red"):
        return [[0.152286, 1.052583, -0.204868],
                [0.114503, 0.786281, 0.099216],
                [-0.003882, -0.048116, 1.051998]]
    if kind in ("deutan", "deuteranopia", "deuteranomaly", "green"):
        return [[0.367322, 0.860646, -0.227968],
                [0.280085, 0.672501, 0.047413],
                [-0.011820, 0.042940, 0.968881]]
    if kind in ("tritan", "tritanopia", "tritanomaly", "blue"):
        return [[1.255528, -0.076749, -0.178779],
                [-0.078411, 0.930809, 0.147602],
                [0.004733, 0.691367, 0.303900]]
    if kind in ("achromat", "achromatopsia", "mono", "grey", "gray"):
        return [[0.2126, 0.7152, 0.0722]] * 3
    raise ValueError(f"unknown CVD type {kind!r}; use protan/deutan/tritan/achromat")

PROTANOPIA = DEUTERANOPIA = TRITANOPIA = ACHROMATOPSIA = None
PROTANOPIA, DEUTERANOPIA, TRITANOPIA, ACHROMATOPSIA = (
    "protanopia", "deuteranopia", "tritanopia", "achromatopsia")


def simulate_cvd(colours, kind: str = "deuteranopia") -> list[str]:
    """Approximate how a palette looks with a colour-vision deficiency."""
    m = cvd_matrix(kind)
    out = []
    for r, g, b in as_rgb01(colours):
        rr = m[0][0] * r + m[0][1] * g + m[0][2] * b
        gg = m[1][0] * r + m[1][1] * g + m[1][2] * b
        bb = m[2][0] * r + m[2][1] * g + m[2][2] * b
        out.append(rgb_to_hex((rr * 255, gg * 255, bb * 255)))
    return out


# --------------------------------------------------------------------------
# palette quality report
# --------------------------------------------------------------------------

def check(name: str, min_delta_e: float = 12.0) -> dict:
    """Audit one palette: distinctness, CVD safety, contrast on white/black.

    ``min_delta_e`` is the CIE76 distance a neighbouring pair must clear to be
    considered distinguishable in print.
    """
    cols = palette(name)
    pairs = []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            d = delta_e(cols[i], cols[j])
            if d < min_delta_e:
                pairs.append({"a": cols[i], "b": cols[j], "delta_e": round(d, 1)})

    cvd = {}
    for kind in (PROTANOPIA, DEUTERANOPIA, TRITANOPIA, ACHROMATOPSIA):
        sim = simulate_cvd(cols, kind)
        worst = min(
            (delta_e(sim[i], sim[j]), cols[i], cols[j])
            for i in range(len(sim)) for j in range(i + 1, len(sim))
        )
        cvd[kind] = {"min_delta_e": round(worst[0], 1),
                     "closest_pair": [worst[1], worst[2]]}

    contrasts = {
        "on_white_AAA": [c for c in cols if contrast_ratio(c, "#FFFFFF") >= 7],
        "on_white_AA": [c for c in cols if 4.5 <= contrast_ratio(c, "#FFFFFF") < 7],
        "on_white_low": [c for c in cols if contrast_ratio(c, "#FFFFFF") < 3],
        "on_black_AA+": [c for c in cols if contrast_ratio(c, "#000000") >= 4.5],
    }
    notes = []
    if contrasts["on_white_low"]:
        notes.append(
            "pale members (" + ", ".join(contrasts["on_white_low"]) + ") are below "
            "3:1 on white: use them for fills/bands only, put labels and data "
            "points on white, or outline them with a darker member of the same ramp")
    if pairs:
        notes.append(
            "some members sit below CIE76 " + str(int(min_delta_e)) +
            ": do not place them side by side without a second cue "
            "(marker shape, linestyle, direct label)")
    return {
        "palette": resolve(name),
        "name_zh": lookup(name)["name_zh"],
        "n": len(cols),
        "hard_pairs": pairs,
        "cvd": cvd,
        "contrast": contrasts,
        "notes": notes,
        "luminance_sorted": sort_by_luminance(cols),
    }


def report(name: str) -> str:
    """Human-readable audit built on :func:`check`."""
    c = check(name)
    L = [f"palette      {c['palette']}  ({c['name_zh']}, {c['n']} colours)"]
    L.append("ramp         " + " ".join(palette(name)))
    L.append("luminance    " + " ".join(c["luminance_sorted"]))
    if c["hard_pairs"]:
        L.append("close pairs  " + ", ".join(
            f"{p['a']}~{p['b']} ({p['delta_e']})" for p in c["hard_pairs"]))
    else:
        L.append("close pairs  none - all pairs clear CIE76 >= 12")
    for k, v in c["cvd"].items():
        L.append(f"{k:<12} min deltaE {v['min_delta_e']:<5} "
                 f"closest {v['closest_pair'][0]}/{v['closest_pair'][1]}")
    con = c["contrast"]
    L.append(f"on white     AAA {len(con['on_white_AAA'])}, AA {len(con['on_white_AA'])}, "
             f"low-contrast {len(con['on_white_low'])}")
    for note in c.get("notes", []):
        L.append("note         " + note)
    return "\n".join(L)
