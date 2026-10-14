# Accessibility: reading the audit, and what to do about it

`sp.report(pid)` and `sp.check(pid)` measure three things that decide whether a
figure survives review, greyscale printing and colour-blind readers.

## 1. Pair distinctness (CIE76 ΔE)

Every pair of colours in a palette is compared in CIE Lab space. Rough guide:

| ΔE | Meaning |
|---|---|
| < 5 | indistinguishable in print; only usable as a fill/background pair |
| 5 - 12 | distinguishable side by side, but easy to confuse across panels |
| > 12 | clearly distinct |

`check()` flags pairs below `min_delta_e` (default 12) under `hard_pairs`.

**What to do:** never place a flagged pair adjacent as two series. Either give
them different marker shapes or linestyles, or pick two members that are not
neighbours in the ramp, e.g. `#315C6B` and `#C6B992` instead of `#315C6B` and
`#607D8B`.

## 2. Colour-vision deficiency

The palette is transformed with published protanopia / deuteranopia /
tritanopia / achromatopsia matrices and the worst remaining pair is reported.

All six palettes are built on lightness steps, so **the darkness ordering
always survives** - a fully colour-blind reader still sees the structure. What
can collapse is hue difference between two members of similar lightness; those
are exactly the pairs reported by `cvd`.

**What to do:**

```python
sim = sp.simulate_cvd(sp.palette("indigo"), sp.DEUTERANOPIA)
# plot the same panel with `sim` to preview what that reader sees
```

Add a second cue whenever a `cvd` minimum falls below ~10 - marker shape,
linestyle, or a direct label on the series. The example
`examples/04_group_comparison.py` renders panels b and c side by side so you
can see the difference.

## 3. Contrast on white (WCAG)

`contrast_ratio(colour, "#FFFFFF")`:

| Ratio | Verdict | Use for |
|---|---|---|
| >= 7 | AAA | axis labels, annotations, text |
| 4.5 - 7 | AA | thin lines, small markers, legend text |
| 3 - 4.5 | AA-large | thick lines, large markers, bar fills |
| < 3 | fail | fills, bands, backgrounds only |

Every palette deliberately contains pale members - they are what makes the
ramp work as a background wash. They are simply not text colours.

**What to do:** keep dark members for anything a reader must decode (points,
lines, labels) and pale members for areas. If a pale series needs to be
readable, outline it with the darkest member of the same ramp:

```python
ax.plot(x, y, color=pale, marker="o", mec=dark, mew=0.6)
```

## Practical checklist before submitting

- [ ] One palette per figure; ramp order preserved.
- [ ] No series relies on colour alone.
- [ ] `sp.report()` shows no unexpected `close pairs`.
- [ ] Pale members are fills/bands, not lines or text.
- [ ] Printed in greyscale, the figure still reads (lightness steps separate).
- [ ] Colour bar uses `sp.colormap(pid)`, not a rainbow map.
