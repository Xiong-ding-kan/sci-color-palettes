# -*- coding: utf-8 -*-
"""Tests for the palette data, colour maths and auditing.

Run:  python -m pytest tests -q        (or)  python tests/test_palettes.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))

import sci_palettes as sp  # noqa: E402
from sci_palettes.data import PALETTES  # noqa: E402


# --------------------------------------------------------------------------
# data integrity
# --------------------------------------------------------------------------

def test_all_palettes_have_eight_hex_colours():
    for pid in sp.names():
        cols = sp.palette(pid)
        assert len(cols) == 8, pid
        assert len(set(cols)) == 8, f"{pid} has duplicate colours"
        for c in cols:
            assert len(c) == 7 and c.startswith("#"), c
            sp.hex_to_rgb(c)  # raises if malformed


def test_roles_match_colour_count():
    for pid in sp.names():
        assert len(PALETTES[pid]["roles"]) == len(PALETTES[pid]["hex"]), pid


def test_published_hex_values_are_stable():
    """Guard against accidental edits to the transcribed data."""
    expected = {
        "glacier": ["#315C6B", "#538A95", "#8CB9BB", "#C9DEDA",
                    "#607D8B", "#A5BCC7", "#C6B992", "#E5DDC8"],
        "dusk_rose": ["#655675", "#9382A3", "#C0B3CD", "#E4DCEB",
                      "#A96F80", "#CF9CAA", "#E8C9CE", "#A7B6A1"],
        "sage": ["#6F8F7B", "#A7BCA3", "#D9E3D2", "#817799",
                 "#B5A8C6", "#DED6E7", "#D4B77A", "#E9DCC3"],
        "burgundy": ["#713E50", "#A56778", "#C997A3", "#E9D5DB",
                     "#526879", "#8FA4B3", "#C4CFD6", "#D5B78C"],
        "indigo": ["#414A78", "#6978A6", "#A5B4D1", "#DCE3F0",
                   "#8B739F", "#B7A1C8", "#DDD0E6", "#C7B38A"],
        "lilac_garden": ["#947CC4", "#DFD0ED", "#DBC496", "#A4C8AA",
                         "#A4CDDF", "#EEB8C6", "#8992A0", "#F5F3F8"],
    }
    for pid, cols in expected.items():
        assert sp.palette(pid) == cols, pid


def test_aliases_resolve():
    assert sp.resolve("冰川蓝绿") == "glacier"
    assert sp.resolve("Glacier Teal") == "glacier"
    assert sp.resolve("teal") == "glacier"
    assert sp.resolve("勃艮第") == "burgundy"
    assert sp.resolve("lilac") == "lilac_garden"
    assert sp.resolve("dusk_rose") == "dusk_rose"


# --------------------------------------------------------------------------
# colour maths
# --------------------------------------------------------------------------

def test_hex_roundtrip():
    for pid in sp.names():
        for c in sp.palette(pid):
            assert sp.rgb_to_hex(sp.hex_to_rgb(c)) == c


def test_short_hex_expands():
    assert sp.hex_to_rgb("#4AF") == (0x44, 0xAA, 0xFF)
    assert sp.hex_to_rgb("4af") == (0x44, 0xAA, 0xFF)


def test_luminance_bounds():
    assert sp.luminance("#000000") == 0.0
    assert abs(sp.luminance("#FFFFFF") - 1.0) < 1e-9
    # ordering must follow lightness
    assert sp.luminance("#315C6B") < sp.luminance("#8CB9BB") < sp.luminance("#C9DEDA")


def test_contrast_ratio_known_values():
    assert abs(sp.contrast_ratio("#FFFFFF", "#000000") - 21.0) < 1e-6
    assert abs(sp.contrast_ratio("#000000", "#000000") - 1.0) < 1e-9
    assert sp.contrast_ratio("#315C6B", "#FFFFFF") > 4.5  # dark enough for text
    assert sp.contrast_ratio("#C9DEDA", "#FFFFFF") < 3.0  # fill only


def test_wcag_levels():
    assert sp.wcag_level("#000000", "#FFFFFF") == "AAA"
    assert sp.wcag_level("#FFFFFF", "#FFFFFF") == "fail"


def test_delta_e_identity_and_ordering():
    assert sp.delta_e("#315C6B", "#315C6B") == 0.0
    # a near-identical pair must be closer than an obviously different pair
    near = sp.delta_e("#315C6B", "#325D6C")
    far = sp.delta_e("#315C6B", "#E5DDC8")
    assert near < 3 < far


def test_mix_endpoints_and_midpoint():
    assert sp.mix("#000000", "#FFFFFF", 0.0) == "#000000"
    assert sp.mix("#000000", "#FFFFFF", 1.0) == "#FFFFFF"
    mid = sp.mix("#000000", "#FFFFFF", 0.5)
    assert mid == "#777777", mid  # Lab midpoint, not sRGB 0x80


def test_lighten_darken_direction():
    assert sp.luminance(sp.lighten("#538A95", 0.3)) > sp.luminance("#538A95")
    assert sp.luminance(sp.darken("#538A95", 0.3)) < sp.luminance("#538A95")


def test_nearest():
    cols = sp.palette("glacier")
    assert sp.nearest("#315C6C", cols) == "#315C6B"


# --------------------------------------------------------------------------
# selection
# --------------------------------------------------------------------------

def test_select_returns_real_palette_colours():
    for pid in sp.names():
        cols = sp.palette(pid)
        for n in range(2, 9):
            chosen = sp.select(cols, n)
            assert len(chosen) == n
            assert len(set(chosen)) == n, (pid, n)
            for c in chosen:
                assert c in cols, f"{pid} n={n}: {c} is not a palette colour"


def test_select_keeps_the_ends_for_even_counts():
    cols = sp.palette("sage")
    assert sp.select(cols, 4)[0] == cols[0]
    assert sp.select(cols, 4)[-1] == cols[-1]


def test_select_is_monotonic_in_index():
    cols = sp.palette("indigo")
    idx = [cols.index(c) for c in sp.select(cols, 5)]
    assert idx == sorted(idx)
    assert len(set(idx)) == 5


def test_select_edges():
    cols = sp.palette("sage")
    assert sp.select(cols, 1) == [cols[4]]
    assert sp.select(cols, 8) == cols
    assert sp.select(cols, 12) == cols  # more than available -> all of them


def test_ramp_length_and_endpoints():
    cols = sp.palette("glacier")
    r = sp.ramp(cols, 5)
    assert len(r) == 5
    assert r[0] == cols[0] and r[-1] == cols[-1]


def test_sub_is_consecutive():
    cols = sp.palette("burgundy")
    assert sp.sub("burgundy", 3) == cols[0:3]
    assert sp.sub("burgundy", 3, start=2) == cols[2:5]


def test_colormap_stops_span_unit_interval():
    stops = sp.to_colormap_stops(sp.palette("sage"))
    assert stops[0][0] == 0.0 and stops[-1][0] == 1.0
    assert all(0.0 <= p <= 1.0 for p, _ in stops)
    assert all(len(rgb) == 3 and all(0.0 <= v <= 1.0 for v in rgb) for _, rgb in stops)


# --------------------------------------------------------------------------
# accessibility
# --------------------------------------------------------------------------

def test_simulate_cvd_preserves_length_and_format():
    for kind in (sp.PROTANOPIA, sp.DEUTERANOPIA, sp.TRITANOPIA, sp.ACHROMATOPSIA):
        sim = sp.simulate_cvd(sp.palette("sage"), kind)
        assert len(sim) == 8
        for c in sim:
            sp.hex_to_rgb(c)


def test_achromatopsia_output_is_grey():
    sim = sp.simulate_cvd(sp.palette("indigo"), sp.ACHROMATOPSIA)
    for c in sim:
        r, g, b = sp.hex_to_rgb(c)
        assert max(r, g, b) - min(r, g, b) <= 1, c


def test_cvd_matrix_rejects_unknown():
    try:
        sp.cvd_matrix("nonsense")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


def test_lightness_step_survives_cvd():
    """The core design promise: dark/light structure survives colour blindness."""
    for pid in sp.names():
        cols = sp.palette(pid)
        for kind in (sp.PROTANOPIA, sp.DEUTERANOPIA, sp.TRITANOPIA, sp.ACHROMATOPSIA):
            sim = sp.simulate_cvd(cols, kind)
            lums = [sp.luminance(c) for c in sim]
            assert max(lums) - min(lums) > 0.25, f"{pid}/{kind} lost its lightness range"


def test_check_structure():
    c = sp.check("sage")
    assert c["palette"] == "sage"
    assert c["n"] == 8
    assert set(c["cvd"]) == {"protanopia", "deuteranopia", "tritanopia", "achromatopsia"}
    assert "on_white_AAA" in c["contrast"]
    assert isinstance(c["notes"], list)


def test_report_mentions_palette_and_colours():
    text = sp.report("glacier")
    assert "glacier" in text
    for c in sp.palette("glacier"):
        assert c in text


# --------------------------------------------------------------------------
# exporters
# --------------------------------------------------------------------------

def test_exports_write_files(tmp_path=None):
    import tempfile
    d = tempfile.mkdtemp(prefix="scipal-")
    checks = {
        "p.json": sp.to_json,
        "p.css": sp.to_css,
        "p.scss": sp.to_scss,
        "p.ase": sp.to_ase,
    }
    for fname, fn in checks.items():
        path = os.path.join(d, fname)
        ret = fn(path)
        assert ret == path, (fname, ret)
        assert os.path.getsize(path) > 100, fname
    for fname, fn in (("g.gpl", sp.to_gpl), ("j.jasc", sp.to_jasc)):
        path = os.path.join(d, fname)
        assert fn(path, "glacier") == path
        assert os.path.getsize(path) > 50
    # CSS returns text when no path is given
    assert "--sci-glacier-1:" in sp.to_css("")


def test_ase_header_and_size():
    import struct, tempfile
    path = os.path.join(tempfile.mkdtemp(), "x.ase")
    sp.to_ase(path)
    data = open(path, "rb").read()
    assert data[:4] == b"ASEF"
    major, minor = struct.unpack(">HH", data[4:8])
    assert (major, minor) == (1, 0)
    n_blocks, = struct.unpack(">I", data[8:12])
    assert n_blocks == 6 * 8 + 2 * 6  # colours + group start/end per palette


def test_export_dispatch():
    import tempfile
    d = tempfile.mkdtemp()
    assert sp.export(os.path.join(d, "a.css")).endswith("a.css")
    try:
        sp.export(os.path.join(d, "a.xyz"))
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for unknown extension")


def test_preview_and_swatches_contain_hex():
    text = sp.preview(["glacier"])
    assert "#315C6B" in text
    assert "冰川蓝绿" in text
    assert "#E5DDC8" in sp.swatches(sp.palette("glacier"))


# --------------------------------------------------------------------------
# matplotlib layer (skipped when matplotlib is absent)
# --------------------------------------------------------------------------

def _has_mpl():
    try:
        import matplotlib  # noqa: F401
        return True
    except ImportError:
        return False


def test_colormap_registers_and_is_reusable():
    if not _has_mpl():
        return
    import matplotlib
    matplotlib.use("Agg")
    cm = sp.colormap("glacier")
    assert cm.name == "sci_glacier"
    assert "sci_glacier" in matplotlib.colormaps
    assert sp.colormap("glacier", reverse=True).name == "sci_glacier_r"
    assert matplotlib.colormaps["sci_glacier"] is not None


def test_set_theme_applies_palette_cycle_and_fonts():
    if not _has_mpl():
        return
    import matplotlib
    matplotlib.use("Agg")
    rc = sp.set_theme("sage")
    cycle = matplotlib.rcParams["axes.prop_cycle"].by_key()["color"]
    assert [c.upper() for c in cycle] == [c.upper() for c in sp.palette("sage")]
    assert isinstance(rc["font.family"], list) and rc["font.family"]
    assert matplotlib.rcParams["image.cmap"] == "sci_sage"
    sp.set_theme("glacier")


def test_select_used_by_theme_is_subset_of_palette():
    if not _has_mpl():
        return
    import matplotlib
    matplotlib.use("Agg")
    sp.set_theme("indigo", n=4)
    cycle = [c.upper() for c in matplotlib.rcParams["axes.prop_cycle"].by_key()["color"]]
    assert len(cycle) == 4
    assert set(cycle) <= {c.upper() for c in sp.palette("indigo")}
    sp.set_theme("glacier")


def test_theme_context_manager_restores():
    if not _has_mpl():
        return
    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams["font.size"] = 11
    with sp.theme("burgundy"):
        assert matplotlib.rcParams["font.size"] == 8
    assert matplotlib.rcParams["font.size"] == 11


def test_style_dict_cjk_toggle():
    if not _has_mpl():
        return
    a = sp.style_dict("glacier", cjk=True)["font.family"]
    b = sp.style_dict("glacier", cjk=False)["font.family"]
    assert "DejaVu Sans" in a and "DejaVu Sans" in b
    assert len(a) >= len(b)


def test_swatch_figure_renders():
    if not _has_mpl():
        return
    import matplotlib
    matplotlib.use("Agg")
    sp.set_theme("glacier")
    fig = sp.swatch_figure(["glacier", "sage"])
    assert fig is not None
    fig.canvas.draw()


def test_all_examples_import_and_run_headless():
    """Smoke-test the shipped example scripts (slow, but catches API drift)."""
    if not _has_mpl():
        return
    import subprocess, tempfile
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    out = tempfile.mkdtemp(prefix="scipal-ex-")
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["MPLBACKEND"] = "Agg"
    # each script takes (palette, outdir), (outdir) or (outdir) depending on
    # how it is written; pass the arguments each one actually declares
    scripts = {
        "01_showcase_grid.py": ["glacier", out],
        "02_colormap_gallery.py": [out],
        "03_materials_figure.py": [out],
        "04_group_comparison.py": [out],
        "05_export_all.py": [out],
    }
    for script, args in scripts.items():
        path = os.path.join(root, "examples", script)
        r = subprocess.run([sys.executable, path] + args,
                           capture_output=True, env=env)
        assert r.returncode == 0, f"{script} failed: {r.stderr.decode('utf-8', 'replace')[-800:]}"


# --------------------------------------------------------------------------
# generated library
# --------------------------------------------------------------------------

def test_derived_library_is_present_and_sized():
    names = sp.derived_names()
    assert len(names) >= 150, len(names)
    assert len(set(names)) == len(names), "duplicate derived ids"


def test_every_derived_palette_is_well_formed():
    for pid in sp.derived_names():
        cols = sp.palette(pid)
        # diverging ramps have 2*n_steps+1 members with the centre in the middle
        expected = 7 if pid.startswith("div-") else 8
        assert len(cols) == expected, f"{pid}: {len(cols)} != {expected}"
        assert len(set(cols)) == len(cols), f"{pid} has duplicate colours"
        for c in cols:
            sp.hex_to_rgb(c)


def test_diverging_centre_is_pale_and_centred():
    for pid in sp.derived_names():
        if not pid.startswith("div-"):
            continue
        cols = sp.palette(pid)
        centre = len(cols) // 2
        lums = [sp.luminance(c) for c in cols]
        # the middle member is the palest, and both arms darken away from it
        assert lums[centre] == max(lums), pid
        assert all(lums[i] <= lums[i + 1] + 0.02 for i in range(centre)), pid
        assert all(lums[i] >= lums[i + 1] - 0.02
                   for i in range(centre, len(cols) - 1)), pid


def test_derived_palettes_clear_the_quality_gate():
    """The gate the generator enforces: separation and a real lightness ramp."""
    for pid in sp.derived_names():
        m = sp.applications(pid)["metrics"]
        gate = 3.5 if m["is_scale"] else 6.0
        assert m["min8"] >= gate, f"{pid}: min deltaE {m['min8']} < {gate}"
        assert m["span8"] >= 0.18, f"{pid}: lightness span {m['span8']}"


def test_derived_ids_encode_their_transform():
    assert sp.palette("glacier-h030") != sp.palette("glacier")
    assert sp.palette("glacier-h000") == sp.palette("glacier")
    assert sp.resolve("glacier-h030").endswith("h030")


def test_alias_resolution_covers_derived():
    assert sp.resolve("glacier-warm") == "glacier-warm"
    assert sp.resolve("GLACIER-WARM") == "glacier-warm"
    assert sp.palette("sage-mono") == sp.palette("sage-mono".upper())


def test_derived_palettes_work_in_the_matplotlib_layer():
    if not _has_mpl():
        return
    import matplotlib
    matplotlib.use("Agg")
    cm = sp.colormap("burgundy-clin-hi")
    assert cm.name == "sci_burgundy-clin-hi"
    assert "sci_burgundy-clin-hi" in matplotlib.colormaps
    sp.set_theme("sage-mono", n=4)
    cycle = [c.upper() for c in matplotlib.rcParams["axes.prop_cycle"].by_key()["color"]]
    assert len(cycle) == 4
    assert set(cycle) <= {c.upper() for c in sp.palette("sage-mono")}
    sp.set_theme("glacier")


def test_family_and_index():
    for fam in sp.families():
        ids = sp.family(fam)
        assert ids, fam
        for pid in ids:
            assert sp.get(pid)["family"] == fam
    # a published palette id works as a "family" too
    assert len(sp.family("glacier")) > 1
    assert all(sp.get(p)["base"] == "glacier" for p in sp.family("glacier"))


def test_family_min_score_filters():
    all_ids = sp.family("hue_rotate")
    high = sp.family("hue_rotate", min_score=60)
    assert len(high) < len(all_ids)
    assert all(sp.get(p)["score"] >= 60 for p in high)


def test_search_finds_the_exact_colour():
    hits = sp.search("#315C6B", limit=8)
    assert hits
    exact = [h for h in hits if h["delta_e"] == 0.0]
    assert exact, "no exact match in the results"
    assert exact[0]["closest"] == "#315C6B"
    # centrality is a tie-breaker, not an override: matching the emphasis colour
    # of another palette is a legitimate near-miss and may rank above an exact
    # match that only occurs as a pale background member
    assert any(h["id"] == "glacier" for h in hits)


def test_search_returns_positions_within_range():
    for h in sp.search("#7A4E7E", limit=6):
        assert 1 <= h["position"] <= 8
        assert h["delta_e"] <= 26.0


def test_stats_adds_up():
    s = sp.stats()
    assert s["published"] == len(sp.names())
    assert s["derived"] == len(sp.derived_names())
    assert s["total"] == s["published"] + s["derived"]
    assert sum(s["families"].values()) == s["derived"]
    assert set(s["families"]) == set(sp.families())


def test_random_palette_is_reproducible():
    a = sp.random_palette(seed=7)
    b = sp.random_palette(seed=7)
    assert a == b
    assert a in set(sp.derived_names())


# --------------------------------------------------------------------------
# application profiles
# --------------------------------------------------------------------------

def test_profiles_exist_with_criteria():
    profs = sp.profiles()
    assert set(profs) == {"clinical", "database", "basic", "general"}
    for name, p in profs.items():
        assert p["label_zh"] and p["label_en"], name
        assert p["criteria"], name
        for metric, t in p["criteria"].items():
            assert len(t) == 3, f"{name}.{metric}"
            lo, hi, weight = t
            assert lo < hi, f"{name}.{metric}: floor must be below ceiling"


def test_applications_cover_every_palette():
    for pid in list(sp.names()) + sp.derived_names():
        a = sp.applications(pid)
        assert set(a["scores"]) == {"clinical", "database", "basic", "general"}
        assert set(a["fit"]) == {"clinical", "database", "basic", "general"}
        for v in a["scores"].values():
            assert 0 <= v <= 100, (pid, v)
        assert a["primary"] in a["scores"]
        assert a["metrics"]["n"] in (7, 8), (pid, a["metrics"]["n"])


def test_derived_palettes_are_all_classified_somewhere():
    """Scores and fit flags exist for every palette.

    Two groups are expected to fit nothing: diverging ramps (excluded from
    categorical fits by design, since they are colour bars) and the low-span
    ramps, which must score below the general profile's floor rather than being
    silently unclassified.
    """
    prof = sp.profiles()["general"]
    for pid in sp.derived_names():
        a = sp.applications(pid)
        assert set(a["scores"]) == {"clinical", "database", "basic", "general"}
        if a["metrics"]["is_scale"]:
            assert not any(a["fit"].values()), pid
            continue
        if not any(a["fit"].values()):
            assert a["scores"]["general"] < prof["score_gate"], pid


def test_suggest_for_ranks_by_score():
    for field in ("clinical", "database", "basic", "general", "临床", "数据库", "基础"):
        rows = sp.suggest_for(field, n=8)
        assert rows, field
        scores = [r["score"] for r in rows]
        assert scores == sorted(scores, reverse=True), field
        for r in rows:
            assert r["id"] in set(sp.names()) | set(sp.derived_names())
            assert isinstance(r["fits"], bool)
            assert r["why"]


def test_suggest_for_require_fit_only_returns_fits():
    for field in ("clinical", "database", "basic"):
        for r in sp.suggest_for(field, n=20, require_fit=True):
            assert r["fits"] is True, (field, r["id"])


def test_suggest_for_rejects_unknown_field():
    try:
        sp.suggest_for("astrology")
    except KeyError as exc:
        assert "unknown field" in str(exc)
    else:
        raise AssertionError("expected KeyError")


def test_clinical_gates_are_actually_met_by_fitting_palettes():
    """A palette marked as fitting clinical work must clear the documented gates.

    The gates are read from profiles() rather than duplicated here, so the test
    cannot drift from the generator's criteria.
    """
    gates = sp.profiles()["clinical"]["gate"]
    checked = 0
    for pid in sp.derived_names():
        a = sp.applications(pid)
        if not a["fit"]["clinical"]:
            continue
        m = a["metrics"]
        for metric, need in gates.items():
            assert m[metric] >= need, f"{pid}: {metric} {m[metric]} < {need}"
        checked += 1
    assert checked > 0, "no palette fits clinical work"


def test_diverging_palettes_are_excluded_from_categorical_fits():
    for pid in sp.derived_names():
        if not pid.startswith("div-"):
            continue
        a = sp.applications(pid)
        assert not any(a["fit"].values()), pid
        assert a["metrics"]["is_scale"] is True
        assert a["metrics"]["arm_monotone"] is True, pid


def test_field_fits_are_not_empty():
    s = sp.stats()
    for field in ("clinical", "database", "basic", "general"):
        assert s["fit_by_field"][field] > 0, field


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except Exception as exc:  # noqa: BLE001
                failures += 1
                print(f"FAIL {name}: {type(exc).__name__}: {exc}")
    print(f"\n{'FAILED' if failures else 'OK'} - {failures} failure(s)")
    raise SystemExit(1 if failures else 0)
