# -*- coding: utf-8 -*-
"""sci-color-palettes - six publication-ready scientific colour schemes.

Quick start
-----------
>>> import sci_palettes as sp
>>> sp.palette("glacier")
['#315C6B', '#538A95', '#8CB9BB', '#C9DEDA', '#607D8B', '#A5BCC7', '#C6B992', '#E5DDC8']
>>> sp.set_theme("burgundy", n=4)      # matplotlib-wide publication theme
>>> sp.colormap("indigo")              # continuous colormap for heatmaps
>>> sp.report("sage")                  # print a colour-vision audit

Chinese palette names work everywhere an id does: ``sp.palette("冰川蓝绿")``.
"""

from .core import (  # noqa: F401
    ACHROMATOPSIA, DEUTERANOPIA, PROTANOPIA, TRITANOPIA,
    as_hex, as_hsl, as_rgb, as_rgb01, check, contrast_ratio, cvd_matrix,
    darken, delta_e, hex_to_rgb, lighten, luminance, mix, names, nearest,
    palette, ramp, report, resolve, rgb_to_hex, select, simulate_cvd,
    sort_by_luminance, sub, to_colormap_stops, wcag_level,
)
from .data import ALIASES, PALETTES, PALETTE_ORDER  # noqa: F401
from .exporters import export, preview, swatches, to_ase, to_css, to_gpl, to_jasc, to_json, to_scss  # noqa: F401

__version__ = "1.0.0"

# matplotlib helpers are re-exported lazily so importing the package in a
# non-plotting environment never requires matplotlib.
_MPL_NAMES = {"set_theme", "theme", "colormap", "listed", "cycle",
              "style_dict", "save_style", "swatch_figure", "PAPER_RC"}

__all__ = [n for n in dir() if not n.startswith("_")] + sorted(_MPL_NAMES)


def __getattr__(name):  # PEP 562
    if name in _MPL_NAMES:
        from . import mpl
        return getattr(mpl, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(set(globals()) | _MPL_NAMES)
