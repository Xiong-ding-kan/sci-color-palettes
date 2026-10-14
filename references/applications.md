# Application profiles: basic research vs clinical vs database

The library is scored for four fields. A palette can be excellent overall and
still be wrong for a clinical survival curve, so the fields are judged on
different criteria rather than on one quality number.

```python
import sci_palettes as sp

sp.suggest_for("临床", n=8)                  # ranked for clinical work
sp.suggest_for("database", require_fit=True)  # only those clearing every gate
sp.applications("burgundy-clin-hi")           # scores, metrics, why
sp.profiles()                                 # the criteria themselves
```

Chinese and English field names both work: `临床` / `clinical`,
`数据库` / `database`, `基础` / `basic`, `通用` / `general`.

## Why the fields differ

**Clinical and database figures** are read by colour-blind clinicians, printed in
greyscale for case notes, and often reproduced small. Requirements:

- series must stay apart after simulating colour-vision deficiency;
- enough dark members to carry text, symbols and thin lines;
- survival curves, forest plots and adverse-event stacks are *categorical*, so
  pairwise separation matters more than a smooth ramp.

**Basic-research panels** get photocopied and read in greyscale, and
omics/materials figures carry meaning in sequential scales. Requirement: a
monotone lightness ramp with restrained chroma, so the ordering survives when
hue is lost.

## The criteria

Each metric is scored from a floor (no credit) to a ceiling (full credit), then
weighted. Floors and ceilings come from the measured distribution of this
library, not from guesswork.

| Metric | Meaning | Measured median |
|---|---|---|
| `span8` | WCAG lightness range across all 8 members; governs greyscale readability | 0.60 |
| `min8` | smallest CIE76 distance between any two of the 8 | 10.4 |
| `min5` | the same, on the best 5-colour subset - how figures actually use a ramp | 14.8 |
| `cvd5` | smallest distance on the best 5 after simulating deuteranopia | 7.0 |
| `dark` | members with contrast >= 4.5:1 on white, usable for text | 1 |
| `hue_spread` | circular spread of chromatic hues in degrees; high = many colour families | - |

### clinical

| Metric | Floor | Ceiling | Weight |
|---|---|---|---|
| `cvd5` | 5.0 | 14.0 | 0.30 |
| `min5` | 9.0 | 22.0 | 0.25 |
| `dark` | 2 | 5 | 0.25 |
| `span8` | 0.45 | 0.80 | 0.20 |
| `hue_spread` | 40 | 170 | **-0.10** |

The negative weight is deliberate: clinical panels overlay text on colour, and
very saturated multi-hue ramps vibrate and make annotations harder to read.

Hard gates: `cvd5 >= 5`, `min5 >= 9`, `dark >= 2`, `span8 >= 0.40`, score `>= 50`.

### database / registry

| Metric | Floor | Ceiling | Weight |
|---|---|---|---|
| `min5` | 10.0 | 26.0 | 0.30 |
| `hue_spread` | 60 | 150 | 0.25 |
| `cvd5` | 4.0 | 13.0 | 0.20 |
| `dark` | 1 | 5 | 0.15 |
| `span8` | 0.38 | 0.72 | 0.10 |

Hard gates: `min5 >= 10`, `hue_spread >= 60`, score `>= 50`.

### basic

| Metric | Floor | Ceiling | Weight |
|---|---|---|---|
| `span8` | 0.45 | 0.80 | 0.35 |
| `min5` | 8.0 | 22.0 | 0.25 |
| `cvd5` | 4.0 | 13.0 | 0.25 |
| `dark` | 1 | 5 | 0.15 |

Hard gates: `span8 >= 0.45`, `cvd5 >= 4`, score `>= 50`.

### general

| Metric | Floor | Ceiling | Weight |
|---|---|---|---|
| `span8` | 0.40 | 0.75 | 0.35 |
| `min5` | 7.0 | 20.0 | 0.35 |
| `dark` | 0 | 4 | 0.30 |

No extra gate; the score already combines the three. This profile exists so the
library is fully covered - these schemes suit a mixed figure or a field we do
not specialise for, rather than being unusable.

## Hard gates vs score

`fits` is a pass/fail verdict on the hard gates. `score` is a ranking. A palette
can rank 4th for clinical work and still fail a gate, which is why both are
reported:

```python
r = sp.suggest_for("clinical", n=1)[0]
r["score"]   # 82
r["fits"]    # True  - also cleared every hard gate
r["why"]     # 'colour-vision separation 14.1 on the best 5; 3 dark member(s) for labels'
```

Use `require_fit=True` when the figure must satisfy a journal's accessibility
policy; otherwise treat the ranking as a shortlist and read `why`.

## Current fit counts

Of 184 palettes: **25** clear the clinical gates, **37** the database gates and
**63** the basic gates; **124** fit at least the general profile. The palettes
that fit no specialised profile are mostly hue rotations of low-span ramps,
which is visible in their low `span8`; they remain usable for slides and posters.

These counts move whenever a floor in `gen_applications.py` changes, so treat
them as a snapshot and check the live numbers with:

```python
import sci_palettes as sp
sp.stats()["fit_by_field"]
```

## Reproducing the scores

```bash
python tools/measure_distribution.py   # the measured distributions behind the floors
python tools/gen_applications.py       # rewrites applications.json
```

The classifier is metric-based, so two runs produce identical scores and a
palette's field suitability can be recomputed from its hex values alone. Run the
measurement first if you change a floor or ceiling: the gates are calibrated
against what the palettes actually deliver (median `min5` 14.9, `cvd5` 7.1,
`span8` 0.62, `dark` 1), not against round numbers.

## Diverging scales

`div-*` palettes are excluded from all four categorical fits by design (their
scores are scaled by 0.55 and `fit` is forced false), because they are colour
bars rather than a set of series colours. Use them where the data is signed and
has a meaningful midpoint:

```python
cmap = sp.colormap("div-wine-teal", continuous=True)
ax.imshow(z, cmap=cmap, vmin=-3, vmax=3)   # index 3 of the 7 is the centre
```

Four archetypes — `div-wine-teal`, `div-plum-blue`, `div-plum-sage`,
`div-rose-teal` — each in three arm depths: default, `-soft` (shallower scale)
and `-deep` (darker tips). The centre sits at index 3 of 7 and is the palest
member; lightness rises monotonically toward it from both ends, which
`test_diverging_centre_is_pale_and_centred` enforces.

![diverging ramps](../../gallery/diverging_preview.png)
