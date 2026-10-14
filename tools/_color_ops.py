# -*- coding: utf-8 -*-
"""Colour-space transforms used to derive new palettes from the six base ones.

All work happens in CIELCh, so a hue rotation keeps perceived lightness and
chroma, and the result is clipped back into sRGB by reducing chroma instead of
clipping RGB channels (which would shift hue).

Everything here is pure stdlib and deliberately deterministic: the generator
must reproduce the same data file on every run.
"""

from __future__ import annotations

import math

from sci_palettes.core import hex_to_rgb, luminance, rgb_to_hex

__all__ = ["to_lch", "from_lch", "shift_hue", "scale_lightness", "scale_chroma",
           "warm", "cool", "blend", "to_monochrome", "rotate_all",
           "complement_hues", "in_gamut", "spread_lightness", "remap_lightness",
           "make_diverging", "remap_diverging", "delta_e_lch"]


# --------------------------------------------------------------------------
# sRGB <-> CIELCh
# --------------------------------------------------------------------------

def _lin(c: float) -> float:
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _unlin(c: float) -> float:
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def to_lch(colour) -> tuple[float, float, float]:
    """hex or (r,g,b) -> (L 0-100, C, h degrees)."""
    r, g, b = hex_to_rgb(colour) if isinstance(colour, str) else tuple(colour)
    r, g, b = _lin(r), _lin(g), _lin(b)
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047
    y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b) / 1.00000
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else (7.787 * t + 16 / 116)

    fx, fy, fz = f(x), f(y), f(z)
    L = 116 * fy - 16
    a = 500 * (fx - fy)
    bb = 200 * (fy - fz)
    C = math.hypot(a, bb)
    h = math.degrees(math.atan2(bb, a)) % 360.0
    return L, C, h


def _lch_to_rgb01(L: float, C: float, h: float):
    hr = math.radians(h)
    a = C * math.cos(hr)
    bb = C * math.sin(hr)
    fy = (L + 16) / 116
    fx = fy + a / 500
    fz = fy - bb / 200

    def finv(t):
        return t ** 3 if t ** 3 > 0.008856 else (t - 16 / 116) / 7.787

    x = 0.95047 * finv(fx)
    y = 1.00000 * finv(fy)
    z = 1.08883 * finv(fz)

    r = 3.2404542 * x - 1.5371385 * y - 0.4985314 * z
    g = -0.9692660 * x + 1.8760108 * y + 0.0415560 * z
    b = 0.0556434 * x - 0.2040259 * y + 1.0572252 * z
    return _unlin(r), _unlin(g), _unlin(b)


def in_gamut(L: float, C: float, h: float, tol: float = 1e-4) -> bool:
    """True when (L, C, h) maps to sRGB without clipping."""
    L = max(0.0, min(100.0, L))
    hr = math.radians(h)
    a = C * math.cos(hr)
    bb = C * math.sin(hr)
    fy = (L + 16) / 116
    fx = fy + a / 500
    fz = fy - bb / 200

    def finv(t):
        return t ** 3 if t ** 3 > 0.008856 else (t - 16 / 116) / 7.787

    x = 0.95047 * finv(fx)
    y = 1.00000 * finv(fy)
    z = 1.08883 * finv(fz)
    for v in (3.2404542 * x - 1.5371385 * y - 0.4985314 * z,
              -0.9692660 * x + 1.8760108 * y + 0.0415560 * z,
              0.0556434 * x - 0.2040259 * y + 1.0572252 * z):
        if v < -tol or v > 1 + tol:
            return False
    return True


def from_lch(L: float, C: float, h: float, max_steps: int = 40) -> str:
    """(L, C, h) -> hex, reducing chroma until the colour fits in sRGB.

    Reducing chroma rather than clamping RGB keeps the hue intact, which is
    what makes a rotated palette still look like a deliberate scheme.
    """
    L = max(0.0, min(100.0, L))
    if in_gamut(L, C, h):
        return rgb_to_hex(tuple(int(round(c * 255)) for c in _lch_to_rgb01(L, C, h)))
    lo, hi = 0.0, max(0.0, C)
    for _ in range(max_steps):
        mid = (lo + hi) / 2
        if in_gamut(L, mid, h):
            lo = mid
        else:
            hi = mid
    rgb = _lch_to_rgb01(L, lo, h)
    return rgb_to_hex(tuple(int(round(c * 255)) for c in rgb))


# --------------------------------------------------------------------------
# transforms: each takes a list of hex colours and returns a new list
# --------------------------------------------------------------------------

def rotate_all(colours, degrees: float) -> list[str]:
    """Rotate every hue by the same angle - the honest 'different time of day'."""
    out = []
    for c in colours:
        L, C, h = to_lch(c)
        out.append(from_lch(L, C, (h + degrees) % 360.0))
    return out


def shift_hue(colours, degrees: float) -> list[str]:
    """Alias of rotate_all, named for the data-file transform table."""
    return rotate_all(colours, degrees)


def complement_hues(colours) -> list[str]:
    """Move each hue to its opposite, preserving per-colour chroma.

    For a multi-hue palette this produces the complementary scheme, which is
    why the family is kept small: full 180 deg rotations are loud and only
    suit poster figures.
    """
    out = []
    for c in colours:
        L, C, h = to_lch(c)
        out.append(from_lch(L, C, (h + 180.0) % 360.0))
    return out


def scale_lightness(colours, scale: float, pivot: float = 50.0) -> list[str]:
    """Scale the L channel about a pivot: >1 opens the ramp, <1 compresses it."""
    out = []
    for c in colours:
        L, C, h = to_lch(c)
        out.append(from_lch(pivot + (L - pivot) * scale, C, h))
    return out


def scale_chroma(colours, scale: float) -> list[str]:
    """Multiply chroma: <1 mutes toward grey, >1 intensifies toward saturation."""
    out = []
    for c in colours:
        L, C, h = to_lch(c)
        out.append(from_lch(L, C * scale, h))
    return out


def warm(colours, degrees: float = 22.0) -> list[str]:
    """Hue drift toward red/orange, weighted by closeness to the light end.

    Rotating uniformly would break colour harmony in palettes whose members sit
    in different hue families, so the drift tapers with chroma.
    """
    out = []
    for c in colours:
        L, C, h = to_lch(c)
        if C < 3:                      # near-neutral member: leave it alone
            out.append(c)
            continue
        weight = min(1.0, C / 25.0)
        out.append(from_lch(L, C, (h + degrees * weight) % 360.0))
    return out


def cool(colours, degrees: float = 22.0) -> list[str]:
    """Hue drift toward blue/cyan, same taper as :func:`warm`."""
    return warm(colours, -degrees)


def blend(a, b, t: float = 0.5) -> list[str]:
    """Pairwise LCh blend of two equal-length palettes.

    Lightness comes from ``a`` and hue/chroma from ``b`` at weight ``t``, so the
    result keeps the parent ramp's structure but borrows the other palette's
    colour character.
    """
    out = []
    for ca, cb in zip(a, b):
        La, Ca, ha = to_lch(ca)
        Lb, Cb, hb = to_lch(cb)
        # shortest way round the hue circle
        dh = ((hb - ha + 180.0) % 360.0) - 180.0
        out.append(from_lch(La + (Lb - La) * t,
                            Ca + (Cb - Ca) * t,
                            (ha + dh * t) % 360.0))
    return out


def to_monochrome(colours, keep_hue: float | None = None,
                  l_lo: float = 6.0, l_hi: float = 94.0) -> list[str]:
    """Collapse a palette to a single hue family, keeping the lightness order.

    Lightness is redistributed across the full range, because a single-hue
    palette carries all its information in lightness alone: without the spread,
    members of similar luminance become indistinguishable once hue is removed.
    """
    lch = [to_lch(c) for c in colours]
    if keep_hue is None:
        wsum = sum(C for _, C, _ in lch)
        if wsum < 1e-6:
            keep_hue = 0.0
        else:
            x = sum(C * math.cos(math.radians(h)) for _, C, h in lch) / wsum
            y = sum(C * math.sin(math.radians(h)) for _, C, h in lch) / wsum
            keep_hue = math.degrees(math.atan2(y, x)) % 360.0
    n = len(lch)
    order = sorted(range(n), key=lambda i: lch[i][0])
    levels = [0.0] * n
    for rank, i in enumerate(order):
        levels[i] = l_lo + (l_hi - l_lo) * (rank / (n - 1)) if n > 1 else (l_lo + l_hi) / 2
    out = []
    for (_, C, _), L in zip(lch, levels):
        out.append(from_lch(L, max(C, 10.0), keep_hue))
    return out


def spread_lightness(colours, factor: float = 1.15, pivot: float = 50.0) -> list[str]:
    """Open the lightness ramp a little, used after chroma reductions.

    Removing chroma shrinks perceptual distance between members, so the
    lightness axis has to take over some of the separation.
    """
    return scale_lightness(colours, factor, pivot)


def remap_lightness(colours, target_lo: float, target_hi: float) -> list[str]:
    """Linearly remap the palette's L range onto [target_lo, target_hi].

    The rank order is preserved and no channel clipping can occur, because the
    target range is itself inside sRGB's lightness limits. Multiplying L by a
    factor instead (the obvious first attempt) drives pale members to L=100,
    where they collapse into a single duplicate colour.
    """
    lums = [to_lch(c)[0] for c in colours]
    lo, hi = min(lums), max(lums)
    span = hi - lo
    out = []
    for c in colours:
        L, C, h = to_lch(c)
        if span < 1e-6:
            newL = (target_lo + target_hi) / 2
        else:
            newL = target_lo + (L - lo) / span * (target_hi - target_lo)
        out.append(from_lch(newL, C, h))
    return out



def make_diverging(dark_a: str, pale_a: str, dark_b: str, pale_b: str,
                   n_steps: int = 3, centre_gap: float = 9.0) -> list[str]:
    """Build a diverging ramp: dark arm, pale centre, dark arm.

    Returns ``2 * n_steps + 1`` colours with the pale centre at index
    ``n_steps``, so the ramp is symmetric and suits a colour bar centred on a
    reference value: a normal range, a zero effect size, a change from baseline.

    Three failure modes were found by measuring the output rather than by
    reasoning about it, and each shaped the construction:

    1. Colours authored directly at the dark end of LCh collapse to near-black
       duplicates in sRGB, so the arm endpoints are real palette colours.
    2. An arm whose inner end sits at the centre's own lightness leaves only a
       1-3 CIE76 gap - "normal" and "just outside normal" become the same
       colour. Each arm stops ``L_GAP`` below the centre instead.
    3. Ordering is easy to reverse: with the arms running pale -> dark inward,
       the dark ends land next to the centre and the ramp reads inside out. Each
       arm runs dark -> pale, so reversing the first gives
       dark -> pale -> centre -> pale -> dark.
    """
    La, Ca, ha = to_lch(dark_a)
    _, Pca, pha = to_lch(pale_a)
    Lb, Cb, hb = to_lch(dark_b)
    _, Pcb, phb = to_lch(pale_b)

    # 14 L* clears a 9 CIE76 gap in CIELCh; see failure mode 2 above.
    L_GAP = 14.0

    def arm(dark_L, dark_C, dark_h, pale_C, pale_h, centre_L):
        """n_steps colours running dark -> pale, stopping L_GAP below centre."""
        inner_L = max(dark_L + 2.0, centre_L - L_GAP)
        steps = []
        for i in range(n_steps):
            f = i / (n_steps - 1) if n_steps > 1 else 1.0   # 0 dark, 1 inner
            L = dark_L + (inner_L - dark_L) * f
            C = dark_C + (pale_C - dark_C) * f
            dh = ((dark_h - pale_h + 180.0) % 360.0) - 180.0
            steps.append(from_lch(L, max(C, 8.0),
                                  (pale_h + dh * (1.0 - f)) % 360.0))
        return steps

    def build(centre_L):
        """Ramp ordered dark -> pale -> centre -> pale -> dark.

        Each arm runs dark -> pale inward. To read as a V shape the *second* arm
        has to be reversed, so the sequence is armA + centre + reversed(armB):
        dark, mid, pale, CENTRE, pale, mid, dark. Reversing the first arm instead
        - which reads as the natural "mirror it" move - produces
        pale, mid, dark, CENTRE, dark, mid, pale and inverts the whole ramp.
        """
        left = arm(La, Ca, ha, Pca, pha, centre_L)          # dark -> pale
        right = list(reversed(arm(Lb, Cb, hb, Pcb, phb, centre_L)))
        # The centre is a *tint*, not another saturated member: chroma stays near
        # the pale anchors' level with a small floor so it does not read as grey.
        # Driving chroma up here put a violet block in the middle of an
        # otherwise muted ramp.
        centre_C = max(min(Pca, Pcb) * 1.5, 7.0)
        centre = from_lch(centre_L, centre_C, pha if Pca >= Pcb else phb)
        return left + [centre] + right

    def acceptable(ramp):
        """Unique, palest at the centre, monotone rising toward it from both ends."""
        if len(set(ramp)) != len(ramp):
            return False
        L = [to_lch(c)[0] for c in ramp]
        ci = n_steps
        if L[ci] < max(L[:ci] + L[ci + 1:]) - 0.5:
            return False
        if not all(L[i] <= L[i + 1] + 1.0 for i in range(ci)):
            return False
        if not all(L[i] >= L[i + 1] - 1.0 for i in range(ci, len(L) - 1)):
            return False
        return (delta_e_lch(ramp[ci], ramp[ci - 1]) >= centre_gap
                and delta_e_lch(ramp[ci], ramp[ci + 1]) >= centre_gap)

    # A genuinely pale centre first; only come down if that fails, so the centre
    # can never drift into the arms. 93 L* is a pale tint that still reads as a
    # colour rather than as white paper.
    for centre_L in (93.0, 92.0, 91.0, 90.0, 89.0):
        ramp = build(centre_L)
        if acceptable(ramp):
            return ramp
    return build(88.0)

def delta_e_lch(a: str, b: str) -> float:
    """CIE76 distance computed straight from hex, no package dependency."""
    la, aa, ba = _lch_to_ab(a)
    lb, ab, bb = _lch_to_ab(b)
    return math.sqrt((la - lb) ** 2 + (aa - ab) ** 2 + (ba - bb) ** 2)


def _lch_to_ab(colour):
    L, C, h = to_lch(colour)
    return L, C * math.cos(math.radians(h)), C * math.sin(math.radians(h))




def remap_diverging(colours: list[str], arm_scale: float,
                    centre_index: int) -> list[str]:
    """Stretch or compress both arms about the pale centre.

    ``arm_scale`` multiplies each arm member's distance from the centre in
    lightness: 1.0 leaves the ramp alone, <1 gives a shallower scale, >1 pushes
    the tips darker. Scaling rather than targeting an absolute lightness keeps
    the variants distinct whatever the centre's L happens to be - an absolute
    target near the centre's own L silently produced identical palettes.
    """
    lch = [to_lch(c) for c in colours]
    lc = lch[centre_index][0]
    out = []
    for i, (L, C, h) in enumerate(lch):
        if i == centre_index:
            out.append(from_lch(L, C, h))
            continue
        newL = lc + (L - lc) * arm_scale
        out.append(from_lch(max(4.0, min(100.0, newL)), C, h))
    return out


def relative_luminance_span(colours) -> float:
    lums = [luminance(c) for c in colours]
    return max(lums) - min(lums)
