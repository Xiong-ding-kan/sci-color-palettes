# -*- coding: utf-8 -*-
"""Matplotlib / seaborn integration.

matplotlib is a hard dependency of this module only; ``sci_palettes.core``
stays stdlib-only so palette data is usable from plain scripts.
"""

from __future__ import annotations

import contextlib

from .core import (
    as_hex, palette, ramp, resolve, select, sub, to_colormap_stops,
)
from .data import PALETTES

__all__ = [
    "set_theme", "colormap", "listed", "cycle", "style_dict", "save_style",
    "swatch_figure", "theme", "PAPER_RC",
]

# A neutral, publication-ready rc baseline: no top/right spines, serif-free,
# thin ticks, tight fonts. Applied by set_theme().
PAPER_RC: dict = {
    "figure.dpi": 120,
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "font.family": ["DejaVu Sans"],  # replaced by resolve_font() below
    "font.size": 8,
    "axes.titlesize": 9,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "axes.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#222222",
    "axes.labelcolor": "#222222",
    "text.color": "#222222",
    "xtick.color": "#222222",
    "ytick.color": "#222222",
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.major.size": 3,
    "ytick.major.size": 3,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "lines.linewidth": 1.2,
    "lines.markersize": 4,
    "legend.frameon": False,
    "axes.grid": False,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.prop_cycle": None,  # filled per palette by set_theme()
}


def _mpl():
    import matplotlib
    return matplotlib


def available_fonts() -> set[str]:
    """Names of every font matplotlib can actually see."""
    from matplotlib import font_manager
    return {f.name for f in font_manager.fontManager.ttflist}


# Ordered preferences. matplotlib does not fall back per glyph, so exactly one
# of these becomes the family; the first one present on this machine wins.
_LATIN_PREFS = ["Arial", "Helvetica", "Helvetica Neue", "DejaVu Sans"]
_CJK_PREFS = ["Microsoft YaHei", "SimHei", "Source Han Sans SC", "Noto Sans CJK SC",
              "PingFang SC", "Hiragino Sans GB", "WenQuanYi Zen Hei"]
_MATH_OK = {"DejaVu Sans", "DejaVu Sans Condensed"}


def resolve_font(cjk: bool = True) -> list[str]:
    """Concrete font stack for this machine, Latin-first, CJK-capable.

    matplotlib resolves a list in ``font.family`` per glyph, so a real stack
    works: Arial renders the Latin text (what most journals ask for), and the
    CJK face catches Chinese labels. DejaVu Sans is always kept in the stack
    because it is the only common face with the full set of scientific
    glyphs (₂ ⁻¹ µ α β Δ); verified by rendering test strings, not assumed.
    """
    have = available_fonts()
    stack = [f for f in _LATIN_PREFS if f in have]
    if "DejaVu Sans" not in stack:
        stack.append("DejaVu Sans")
    if cjk:
        stack += [f for f in _CJK_PREFS if f in have]
    seen, out = set(), []
    for f in stack:
        if f not in seen:
            out.append(f)
            seen.add(f)
    return out or ["DejaVu Sans"]


# --------------------------------------------------------------------------
# theme
# --------------------------------------------------------------------------

def style_dict(name: str = "glacier", n: int | None = None,
               cjk: bool = True) -> dict:
    """rcParams dict for one palette (colour cycle + default colormap)."""
    pid = resolve(name)
    cols = palette(pid) if n is None else select(palette(pid), n)
    rc = {k: v for k, v in PAPER_RC.items() if v is not None}
    # font.family (a real list) is what gives matplotlib per-glyph fallback;
    # font.sans-serif is ignored while font.family names concrete fonts.
    rc["font.family"] = resolve_font(cjk)
    rc["axes.unicode_minus"] = False  # U+2212 is missing from most CJK faces
    rc["axes.prop_cycle"] = _mpl().cycler(color=cols)
    rc["image.cmap"] = colormap(pid).name
    return rc


def set_theme(name: str = "glacier", n: int | None = None,
              cjk: bool = True, **overrides) -> dict:
    """Apply a complete publication theme; returns the rcParams actually set.

    >>> import sci_palettes as sp
    >>> sp.set_theme("burgundy")          # wine/slate journal look
    >>> sp.set_theme("冰川蓝绿", n=4)      # Chinese alias, 4-colour cycle
    >>> sp.set_theme("sage", cjk=False)   # force a Latin-only font stack
    """
    import matplotlib as mpl
    rc = style_dict(name, n, cjk=cjk)
    rc.update(overrides)
    mpl.rcParams.update(rc)
    return rc


@contextlib.contextmanager
def theme(name: str = "glacier", n: int | None = None, cjk: bool = True,
          **overrides):
    """Context manager form: restores the previous rcParams on exit."""
    import matplotlib as mpl
    old = mpl.rcParams.copy()
    try:
        set_theme(name, n, cjk=cjk, **overrides)
        yield
    finally:
        mpl.rcParams.update(old)


def save_style(path: str, name: str = "glacier", n: int | None = None,
               cjk: bool = True) -> str:
    """Write a stand-alone matplotlib .mplstyle file."""
    pid = resolve(name)
    rc = style_dict(pid, n, cjk=cjk)
    lines = [f"# sci-color-palettes :: {pid} ({PALETTES[pid]['name_zh']})",
             f"# {PALETTES[pid]['subtitle_en']}", ""]
    for k, v in rc.items():
        if v is None or k == "axes.prop_cycle":
            continue
        if isinstance(v, (list, tuple)):
            v = ", ".join(str(x) for x in v)
        lines.append(f"{k}: {v}")
    cols = palette(pid) if n is None else select(palette(pid), n)
    quoted = ", ".join(f"'{c}'" for c in cols)
    lines.append(f"axes.prop_cycle: cycler(color=[{quoted}])")
    lines.append(f"image.cmap: sci_{pid}")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return path


# --------------------------------------------------------------------------
# colormaps
# --------------------------------------------------------------------------

def colormap(name: str = "glacier", reverse: bool = False,
             n: int | None = None, continuous: bool = True,
             register: bool = True):
    """A matplotlib colormap for the palette.

    continuous=True  -> smooth LinearSegmentedColormap (heatmaps, surfaces)
    continuous=False -> discrete ListedColormap (categories, contour bands)

    The colormap is registered under ``sci_<palette>`` so it can also be
    referenced by name, e.g. ``plt.imshow(z, cmap="sci_glacier")`` or via the
    ``image.cmap`` rcParam that :func:`set_theme` installs.
    """
    import matplotlib as mpl
    from matplotlib.colors import LinearSegmentedColormap, ListedColormap
    pid = resolve(name)
    cols = as_hex(palette(pid))
    if n:
        cols = ramp(cols, n)
    if reverse:
        cols = cols[::-1]
    suffix = "_r" if reverse else ""
    cmap_name = f"sci_{pid}{suffix}"
    if continuous:
        cmap = LinearSegmentedColormap.from_list(cmap_name,
                                                 to_colormap_stops(cols))
    else:
        cmap = ListedColormap(cols, name=cmap_name)
    cmap._sci_palette = pid  # type: ignore[attr-defined]
    if register:
        try:
            if cmap_name in mpl.colormaps:
                mpl.colormaps.unregister(cmap_name)
            mpl.colormaps.register(cmap, force=True)
        except Exception:  # pragma: no cover - older matplotlib
            pass
    return cmap


def listed(name: str = "glacier", n: int | None = None, reverse: bool = False):
    """Discrete colormap, optionally resampled to ``n`` bands."""
    return colormap(name, reverse=reverse, n=n, continuous=False)


def cycle(name: str = "glacier", n: int | None = None) -> list[str]:
    """Colour list for ``axes.prop_cycle`` / seaborn, keeping original hues."""
    pid = resolve(name)
    cols = palette(pid)
    return select(cols, n) if n else cols


# --------------------------------------------------------------------------
# swatch sheet (for README images and visual QA)
# --------------------------------------------------------------------------

def swatch_figure(palettes=None, per_row: int = 1, show_hex: bool = True,
                  figsize_per: tuple[float, float] = (7.2, 0.95), cjk: bool = True):
    """Build a labelled swatch sheet figure for one or more palettes.

    The font stack is applied to this figure explicitly, so the Chinese names
    render even when the caller never called :func:`set_theme`.
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    names = [resolve(p) for p in (palettes or PALETTES.keys())]
    fig, axes = plt.subplots(len(names), 1,
                             figsize=(figsize_per[0], figsize_per[1] * len(names)))
    if len(names) == 1:
        axes = [axes]
    stack = resolve_font(cjk)
    for ax, pid in zip(axes, names):
        info = PALETTES[pid]
        cols = info["hex"]
        n = len(cols)
        ax.set_xlim(0, n)
        ax.set_ylim(-0.55, 0.75)
        ax.axis("off")
        for i, c in enumerate(cols):
            ax.add_patch(FancyBboxPatch(
                (i + 0.06, 0.06), 0.88, 0.5,
                boxstyle="round,pad=0,rounding_size=0.06",
                linewidth=0, facecolor=c))
            if show_hex:
                ax.text(i + 0.5, -0.10, c, ha="center", va="top",
                        fontsize=7.5, color="#333333", fontfamily=stack)
        ax.text(0.06, 0.66, f"{info['name_zh']}  ·  {info['name_en']}",
                ha="left", va="bottom", fontsize=10, color="#222222",
                fontfamily=stack)
        ax.text(n - 0.06, 0.66, info["subtitle_zh"], ha="right", va="bottom",
                fontsize=7.5, color="#777777", fontfamily=stack)
    fig.subplots_adjust(hspace=0.9)
    return fig
