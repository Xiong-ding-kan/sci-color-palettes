# Palette reference

Copy-paste hex values. Order is dark -> light as anchor, so index 0 is
always the emphasis colour. `contrast` is the WCAG ratio against white;
below 3:1 the colour is for fills and bands, not for text or thin lines.

Chinese names, English names and the ids below all work as arguments to
every function in the package.

## 冰川蓝绿 / Glacier Teal - `glacier`

*清透冷调 / 环境与生态 / Clear cool tones / Environment & ecology*

Mood: cool, clean, aquatic; teal-driven with a sand accent

| # | hex | role | on white | luminance |
|---|---|---|---|---|
| 1 | `#315C6B` | primary dark | 7.31:1 AAA | 0.094 |
| 2 | `#538A95` | primary | 3.86:1 AA-large | 0.222 |
| 3 | `#8CB9BB` | primary mid | 2.15:1 fail | 0.439 |
| 4 | `#C9DEDA` | primary pale | 1.41:1 fail | 0.697 |
| 5 | `#607D8B` | secondary dark | 4.37:1 AA-large | 0.190 |
| 6 | `#A5BCC7` | secondary | 1.98:1 fail | 0.481 |
| 7 | `#C6B992` | accent warm | 1.95:1 fail | 0.488 |
| 8 | `#E5DDC8` | accent warm pale | 1.35:1 fail | 0.725 |

```python
sp.palette('glacier')
  #315C6B #538A95 #8CB9BB #C9DEDA #607D8B #A5BCC7 #C6B992 #E5DDC8
```

Audit:
```
palette      glacier  (冰川蓝绿, 8 colours)
ramp         #315C6B #538A95 #8CB9BB #C9DEDA #607D8B #A5BCC7 #C6B992 #E5DDC8
luminance    #315C6B #607D8B #538A95 #8CB9BB #A5BCC7 #C6B992 #C9DEDA #E5DDC8
close pairs  #538A95~#607D8B (9.0), #8CB9BB~#A5BCC7 (9.6)
protanopia   min deltaE 3.9   closest #538A95/#607D8B
deuteranopia min deltaE 3.5   closest #538A95/#607D8B
tritanopia   min deltaE 9.4   closest #8CB9BB/#A5BCC7
achromatopsia min deltaE 0.4   closest #A5BCC7/#C6B992
on white     AAA 1, AA 0, low-contrast 5
note         pale members (#8CB9BB, #C9DEDA, #A5BCC7, #C6B992, #E5DDC8) are below 3:1 on white: use them for fills/bands only, put labels and data points on white, or outline them with a darker member of the same ramp
note         some members sit below CIE76 12: do not place them side by side without a second cue (marker shape, linestyle, direct label)
```

## 暮紫玫瑰 / Dusk Purple Rose - `dusk_rose`

*温柔层次 / 生物与数据 / Gentle layering / Biology & data*

Mood: soft, feminine, layered; two purple steps then rose then sage

| # | hex | role | on white | luminance |
|---|---|---|---|---|
| 1 | `#655675` | primary dark | 6.69:1 AA | 0.107 |
| 2 | `#9382A3` | primary | 3.52:1 AA-large | 0.248 |
| 3 | `#C0B3CD` | primary pale | 1.99:1 fail | 0.479 |
| 4 | `#E4DCEB` | primary mist | 1.33:1 fail | 0.737 |
| 5 | `#A96F80` | accent rose dark | 3.98:1 AA-large | 0.214 |
| 6 | `#CF9CAA` | accent rose | 2.34:1 fail | 0.399 |
| 7 | `#E8C9CE` | accent rose pale | 1.54:1 fail | 0.634 |
| 8 | `#A7B6A1` | contrast sage | 2.13:1 fail | 0.442 |

```python
sp.palette('dusk_rose')
  #655675 #9382A3 #C0B3CD #E4DCEB #A96F80 #CF9CAA #E8C9CE #A7B6A1
```

Audit:
```
palette      dusk_rose  (暮紫玫瑰, 8 colours)
ramp         #655675 #9382A3 #C0B3CD #E4DCEB #A96F80 #CF9CAA #E8C9CE #A7B6A1
luminance    #655675 #A96F80 #9382A3 #CF9CAA #A7B6A1 #C0B3CD #E8C9CE #E4DCEB
close pairs  #E4DCEB~#E8C9CE (11.3)
protanopia   min deltaE 9.2   closest #E4DCEB/#E8C9CE
deuteranopia min deltaE 7.4   closest #CF9CAA/#A7B6A1
tritanopia   min deltaE 9.9   closest #C0B3CD/#A7B6A1
achromatopsia min deltaE 2.6   closest #C0B3CD/#A7B6A1
on white     AAA 0, AA 1, low-contrast 5
note         pale members (#C0B3CD, #E4DCEB, #CF9CAA, #E8C9CE, #A7B6A1) are below 3:1 on white: use them for fills/bands only, put labels and data points on white, or outline them with a darker member of the same ramp
note         some members sit below CIE76 12: do not place them side by side without a second cue (marker shape, linestyle, direct label)
```

## 鼠尾草紫 / Sage & Violet - `sage`

*柔和层次 / 数据可视化 / Soft hierarchy / Data visualisation*

Mood: restful green -> violet -> sand; the most colour-blind safe of the set

| # | hex | role | on white | luminance |
|---|---|---|---|---|
| 1 | `#6F8F7B` | primary sage dark | 3.56:1 AA-large | 0.245 |
| 2 | `#A7BCA3` | primary sage | 2.03:1 fail | 0.468 |
| 3 | `#D9E3D2` | primary sage pale | 1.32:1 fail | 0.743 |
| 4 | `#817799` | secondary violet dark | 4.17:1 AA-large | 0.202 |
| 5 | `#B5A8C6` | secondary violet | 2.24:1 fail | 0.419 |
| 6 | `#DED6E7` | secondary violet pale | 1.41:1 fail | 0.694 |
| 7 | `#D4B77A` | accent sand | 1.93:1 fail | 0.493 |
| 8 | `#E9DCC3` | accent sand pale | 1.36:1 fail | 0.725 |

```python
sp.palette('sage')
  #6F8F7B #A7BCA3 #D9E3D2 #817799 #B5A8C6 #DED6E7 #D4B77A #E9DCC3
```

Audit:
```
palette      sage  (鼠尾草紫, 8 colours)
ramp         #6F8F7B #A7BCA3 #D9E3D2 #817799 #B5A8C6 #DED6E7 #D4B77A #E9DCC3
luminance    #817799 #6F8F7B #B5A8C6 #A7BCA3 #D4B77A #DED6E7 #E9DCC3 #D9E3D2
close pairs  #D9E3D2~#E9DCC3 (9.6)
protanopia   min deltaE 5.6   closest #D9E3D2/#E9DCC3
deuteranopia min deltaE 7.4   closest #D9E3D2/#E9DCC3
tritanopia   min deltaE 6.0   closest #D9E3D2/#DED6E7
achromatopsia min deltaE 1.1   closest #D9E3D2/#E9DCC3
on white     AAA 0, AA 0, low-contrast 6
note         pale members (#A7BCA3, #D9E3D2, #B5A8C6, #DED6E7, #D4B77A, #E9DCC3) are below 3:1 on white: use them for fills/bands only, put labels and data points on white, or outline them with a darker member of the same ramp
note         some members sit below CIE76 12: do not place them side by side without a second cue (marker shape, linestyle, direct label)
```

## 勃艮第灰 / Burgundy Slate - `burgundy`

*克制质感 / 材料与表征 / Restrained texture / Materials & characterisation*

Mood: serious, journal-style; wine reds against slate blue with a gold accent

| # | hex | role | on white | luminance |
|---|---|---|---|---|
| 1 | `#713E50` | primary wine dark | 8.38:1 AAA | 0.075 |
| 2 | `#A56778` | primary wine | 4.36:1 AA-large | 0.191 |
| 3 | `#C997A3` | primary wine pale | 2.49:1 fail | 0.372 |
| 4 | `#E9D5DB` | primary wine mist | 1.40:1 fail | 0.700 |
| 5 | `#526879` | secondary slate dark | 5.81:1 AA | 0.131 |
| 6 | `#8FA4B3` | secondary slate | 2.58:1 fail | 0.356 |
| 7 | `#C4CFD6` | secondary slate pale | 1.59:1 fail | 0.612 |
| 8 | `#D5B78C` | accent gold | 1.91:1 fail | 0.499 |

```python
sp.palette('burgundy')
  #713E50 #A56778 #C997A3 #E9D5DB #526879 #8FA4B3 #C4CFD6 #D5B78C
```

Audit:
```
palette      burgundy  (勃艮第灰, 8 colours)
ramp         #713E50 #A56778 #C997A3 #E9D5DB #526879 #8FA4B3 #C4CFD6 #D5B78C
luminance    #713E50 #526879 #A56778 #8FA4B3 #C997A3 #D5B78C #C4CFD6 #E9D5DB
close pairs  none - all pairs clear CIE76 >= 12
protanopia   min deltaE 4.4   closest #E9D5DB/#C4CFD6
deuteranopia min deltaE 7.6   closest #E9D5DB/#C4CFD6
tritanopia   min deltaE 10.2  closest #C997A3/#D5B78C
achromatopsia min deltaE 0.4   closest #C997A3/#8FA4B3
on white     AAA 1, AA 1, low-contrast 5
note         pale members (#C997A3, #E9D5DB, #8FA4B3, #C4CFD6, #D5B78C) are below 3:1 on white: use them for fills/bands only, put labels and data points on white, or outline them with a darker member of the same ramp
```

## 靛蓝丁香 / Indigo Lilac - `indigo`

*理性柔和 / 统计与建模 / Rational & soft / Statistics & modelling*

Mood: cool indigo -> lilac -> muted gold; high legibility for dense plots

| # | hex | role | on white | luminance |
|---|---|---|---|---|
| 1 | `#414A78` | primary indigo dark | 8.48:1 AAA | 0.074 |
| 2 | `#6978A6` | primary indigo | 4.34:1 AA-large | 0.192 |
| 3 | `#A5B4D1` | primary indigo pale | 2.09:1 fail | 0.452 |
| 4 | `#DCE3F0` | primary indigo mist | 1.29:1 fail | 0.764 |
| 5 | `#8B739F` | secondary lilac dark | 4.16:1 AA-large | 0.203 |
| 6 | `#B7A1C8` | secondary lilac | 2.35:1 fail | 0.397 |
| 7 | `#DDD0E6` | secondary lilac pale | 1.47:1 fail | 0.662 |
| 8 | `#C7B38A` | accent gold | 2.05:1 fail | 0.462 |

```python
sp.palette('indigo')
  #414A78 #6978A6 #A5B4D1 #DCE3F0 #8B739F #B7A1C8 #DDD0E6 #C7B38A
```

Audit:
```
palette      indigo  (靛蓝丁香, 8 colours)
ramp         #414A78 #6978A6 #A5B4D1 #DCE3F0 #8B739F #B7A1C8 #DDD0E6 #C7B38A
luminance    #414A78 #6978A6 #8B739F #B7A1C8 #A5B4D1 #C7B38A #DDD0E6 #DCE3F0
close pairs  #DCE3F0~#DDD0E6 (9.9)
protanopia   min deltaE 3.5   closest #6978A6/#8B739F
deuteranopia min deltaE 3.0   closest #A5B4D1/#B7A1C8
tritanopia   min deltaE 9.7   closest #DCE3F0/#DDD0E6
achromatopsia min deltaE 0.4   closest #A5B4D1/#C7B38A
on white     AAA 1, AA 0, low-contrast 5
note         pale members (#A5B4D1, #DCE3F0, #B7A1C8, #DDD0E6, #C7B38A) are below 3:1 on white: use them for fills/bands only, put labels and data points on white, or outline them with a darker member of the same ramp
note         some members sit below CIE76 12: do not place them side by side without a second cue (marker shape, linestyle, direct label)
```

## 熏紫春庭 / Smoked Lilac Garden - `lilac_garden`

*柔和雅致 / 材料与催化 / Elegant pastels / Materials & catalysis*

Mood: pastel, airy, multi-hue; balances purple with green, blue and pink

| # | hex | role | on white | luminance |
|---|---|---|---|---|
| 1 | `#947CC4` | primary lilac | 3.54:1 AA-large | 0.247 |
| 2 | `#DFD0ED` | primary lilac pale | 1.46:1 fail | 0.669 |
| 3 | `#DBC496` | accent gold | 1.70:1 fail | 0.567 |
| 4 | `#A4C8AA` | contrast green | 1.84:1 fail | 0.521 |
| 5 | `#A4CDDF` | contrast blue | 1.70:1 fail | 0.569 |
| 6 | `#EEB8C6` | contrast pink | 1.71:1 fail | 0.565 |
| 7 | `#8992A0` | neutral slate | 3.14:1 AA-large | 0.284 |
| 8 | `#F5F3F8` | paper | 1.10:1 fail | 0.903 |

```python
sp.palette('lilac_garden')
  #947CC4 #DFD0ED #DBC496 #A4C8AA #A4CDDF #EEB8C6 #8992A0 #F5F3F8
```

Audit:
```
palette      lilac_garden  (熏紫春庭, 8 colours)
ramp         #947CC4 #DFD0ED #DBC496 #A4C8AA #A4CDDF #EEB8C6 #8992A0 #F5F3F8
luminance    #947CC4 #8992A0 #A4C8AA #EEB8C6 #DBC496 #A4CDDF #DFD0ED #F5F3F8
close pairs  none - all pairs clear CIE76 >= 12
protanopia   min deltaE 4.2   closest #DFD0ED/#A4CDDF
deuteranopia min deltaE 8.1   closest #DFD0ED/#A4CDDF
tritanopia   min deltaE 8.3   closest #A4C8AA/#A4CDDF
achromatopsia min deltaE 0.0   closest #DBC496/#A4CDDF
on white     AAA 0, AA 0, low-contrast 6
note         pale members (#DFD0ED, #DBC496, #A4C8AA, #A4CDDF, #EEB8C6, #F5F3F8) are below 3:1 on white: use them for fills/bands only, put labels and data points on white, or outline them with a darker member of the same ramp
```

