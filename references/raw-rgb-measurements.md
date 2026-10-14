# Raw RGB read from the reference figures

This is the measurement record behind the six anchor palettes. For every swatch it lists what the pixels actually are, next to the hex label printed on the swatch itself.

**Both columns are derived from the same raster image.** There is no earlier, non-image source of these colours: the figures are renders, so the pixels are a rendering of the palette and the printed label is the value the renderer declared. The repository ships the printed labels (see `palettes.md`) because they are explicit, reproducible and free of sampling choices; this file records the pixel readings so the alternative can be checked.

## How the pixels were read

1. The palette overview sheet is located in each article (1086x1448 px).
2. The swatch band is found by scanning for the row range whose pixels are consistently chromatic; the band is 62-83 px tall.
3. The band is split into blocks at the near-white gutters between them. The eight blocks come out 109-123 px wide, within 5% of each other, which is how the layout is validated per figure.
4. Inside each block a central region (half the width and height, to exclude the rounded corners and the anti-aliased edge) is sampled; the modal RGB of that region is reported, with the arithmetic mean beside it as a cross-check.

## What the measurement shows

| Quantity | Median | p90 | Max |
|---|---|---|---|
| printed label vs measured modal RGB (CIE76) | 1.6 | 3.6 | 5.6 |
| gradient *within* a single swatch (CIE76) | 1.3 | 1.7 | 2.1 |

The swatch blocks are soft gradient fills, not flat colours: the same block contains 20-47 distinct RGB values and its own corners differ by up to 2.1 CIE76. The offset between the label and the pixels is the same order of magnitude. Two consequences:

- no single pixel value is *the* colour of a block, so any pixel-reading rule (centre, modal, most-saturated, ...) is a choice, not a fact;
- the measured values sit consistently slightly lighter and less saturated than the printed labels, which is what a gradient overlay does to a flat fill.

## Per-palette readings

### 冰川蓝绿 / glacier

Source: [article](https://mp.weixin.qq.com/s/Icnhan1N37TATjWmT3mHMg), image `Icnhan1N37TATjWmT3mHMg_1.png`, band rows 168-232 (65 px), layout validated: True

| # | printed label | measured RGB | as hex | mean RGB | CIE76 | block interior |
|---|---|---|---|---|---|---|
| 1 | `#315C6B` | 54, 98, 112 | `#366270` | 54, 98, 112 | 2.5 | 38 values, 24% modal |
| 2 | `#538A95` | 85, 135, 146 | `#558792` | 84, 135, 146 | 1.7 | 37 values, 17% modal |
| 3 | `#8CB9BB` | 140, 180, 183 | `#8CB4B7` | 140, 180, 183 | 2.3 | 30 values, 20% modal |
| 4 | `#C9DEDA` | 196, 218, 213 | `#C4DAD5` | 196, 218, 213 | 1.7 | 24 values, 38% modal |
| 5 | `#607D8B` | 110, 135, 147 | `#6E8793` | 110, 135, 147 | 4.5 | 31 values, 22% modal |
| 6 | `#A5BCC7` | 164, 187, 197 | `#A4BBC5` | 164, 187, 197 | 0.7 | 31 values, 32% modal |
| 7 | `#C6B992` | 194, 182, 146 | `#C2B692` | 194, 182, 146 | 2.0 | 31 values, 23% modal |
| 8 | `#E5DDC8` | 226, 217, 196 | `#E2D9C4` | 226, 217, 195 | 1.4 | 28 values, 15% modal |

```python
# what the repository ships (printed labels)
sp.palette('glacier')
  #315C6B #538A95 #8CB9BB #C9DEDA #607D8B #A5BCC7 #C6B992 #E5DDC8
# what the pixels measure (modal interior RGB)
  #366270 #558792 #8CB4B7 #C4DAD5 #6E8793 #A4BBC5 #C2B692 #E2D9C4
```

### 暮紫玫瑰 / dusk_rose

Source: [article](https://mp.weixin.qq.com/s/GxLpRgHBnefPnRxGzDWFsQ), image `GxLpRgHBnefPnRxGzDWFsQ_1.png`, band rows 156-218 (63 px), layout validated: True

| # | printed label | measured RGB | as hex | mean RGB | CIE76 | block interior |
|---|---|---|---|---|---|---|
| 1 | `#655675` | 110, 91, 126 | `#6E5B7E` | 110, 91, 126 | 3.7 | 32 values, 26% modal |
| 2 | `#9382A3` | 151, 135, 166 | `#9787A6` | 150, 134, 166 | 2.2 | 33 values, 23% modal |
| 3 | `#C0B3CD` | 202, 192, 212 | `#CAC0D4` | 202, 192, 212 | 5.6 | 29 values, 20% modal |
| 4 | `#E4DCEB` | 231, 221, 237 | `#E7DDED` | 232, 221, 237 | 1.0 | 21 values, 29% modal |
| 5 | `#A96F80` | 179, 116, 136 | `#B37488` | 180, 116, 136 | 3.5 | 36 values, 18% modal |
| 6 | `#CF9CAA` | 219, 165, 180 | `#DBA5B4` | 220, 165, 180 | 3.8 | 43 values, 16% modal |
| 7 | `#E8C9CE` | 239, 204, 211 | `#EFCCD3` | 239, 204, 211 | 2.3 | 23 values, 31% modal |
| 8 | `#A7B6A1` | 165, 182, 159 | `#A5B69F` | 165, 182, 160 | 1.3 | 24 values, 25% modal |

```python
# what the repository ships (printed labels)
sp.palette('dusk_rose')
  #655675 #9382A3 #C0B3CD #E4DCEB #A96F80 #CF9CAA #E8C9CE #A7B6A1
# what the pixels measure (modal interior RGB)
  #6E5B7E #9787A6 #CAC0D4 #E7DDED #B37488 #DBA5B4 #EFCCD3 #A5B69F
```

### 鼠尾草紫 / sage

Source: [article](https://mp.weixin.qq.com/s/5dRgr23t8nMHd0P0TxO6VA), image `5dRgr23t8nMHd0P0TxO6VA_1.png`, band rows 159-220 (62 px), layout validated: True

| # | printed label | measured RGB | as hex | mean RGB | CIE76 | block interior |
|---|---|---|---|---|---|---|
| 1 | `#6F8F7B` | 111, 141, 121 | `#6F8D79` | 111, 141, 121 | 1.0 | 32 values, 26% modal |
| 2 | `#A7BCA3` | 171, 191, 166 | `#ABBFA6` | 171, 190, 166 | 1.2 | 32 values, 19% modal |
| 3 | `#D9E3D2` | 214, 225, 209 | `#D6E1D1` | 214, 225, 209 | 1.0 | 20 values, 29% modal |
| 4 | `#817799` | 130, 119, 152 | `#827798` | 130, 119, 152 | 0.7 | 31 values, 24% modal |
| 5 | `#B5A8C6` | 183, 171, 199 | `#B7ABC7` | 183, 171, 200 | 1.5 | 20 values, 23% modal |
| 6 | `#DED6E7` | 222, 215, 230 | `#DED7E6` | 221, 215, 230 | 1.1 | 26 values, 23% modal |
| 7 | `#D4B77A` | 210, 181, 127 | `#D2B57F` | 210, 181, 127 | 3.6 | 32 values, 19% modal |
| 8 | `#E9DCC3` | 234, 220, 193 | `#EADCC1` | 234, 220, 194 | 1.1 | 28 values, 21% modal |

```python
# what the repository ships (printed labels)
sp.palette('sage')
  #6F8F7B #A7BCA3 #D9E3D2 #817799 #B5A8C6 #DED6E7 #D4B77A #E9DCC3
# what the pixels measure (modal interior RGB)
  #6F8D79 #ABBFA6 #D6E1D1 #827798 #B7ABC7 #DED7E6 #D2B57F #EADCC1
```

### 勃艮第灰 / burgundy

Source: [article](https://mp.weixin.qq.com/s/mhpHJRSGmbPOXavTyIUIqw), image `mhpHJRSGmbPOXavTyIUIqw_1.png`, band rows 159-229 (71 px), layout validated: True

| # | printed label | measured RGB | as hex | mean RGB | CIE76 | block interior |
|---|---|---|---|---|---|---|
| 1 | `#713E50` | 114, 65, 80 | `#724150` | 114, 64, 80 | 2.1 | 37 values, 18% modal |
| 2 | `#A56778` | 161, 97, 116 | `#A16174` | 161, 97, 116 | 2.5 | 47 values, 21% modal |
| 3 | `#C997A3` | 196, 146, 158 | `#C4929E` | 196, 146, 158 | 1.9 | 33 values, 17% modal |
| 4 | `#E9D5DB` | 233, 213, 218 | `#E9D5DA` | 232, 212, 218 | 0.5 | 26 values, 28% modal |
| 5 | `#526879` | 82, 104, 120 | `#526878` | 82, 103, 119 | 0.6 | 38 values, 21% modal |
| 6 | `#8FA4B3` | 136, 157, 173 | `#889DAD` | 136, 158, 173 | 2.7 | 43 values, 16% modal |
| 7 | `#C4CFD6` | 194, 205, 212 | `#C2CDD4` | 194, 205, 212 | 0.7 | 24 values, 29% modal |
| 8 | `#D5B78C` | 208, 177, 138 | `#D0B18A` | 208, 177, 138 | 2.8 | 29 values, 27% modal |

```python
# what the repository ships (printed labels)
sp.palette('burgundy')
  #713E50 #A56778 #C997A3 #E9D5DB #526879 #8FA4B3 #C4CFD6 #D5B78C
# what the pixels measure (modal interior RGB)
  #724150 #A16174 #C4929E #E9D5DA #526878 #889DAD #C2CDD4 #D0B18A
```

### 靛蓝丁香 / indigo

Source: [article](https://mp.weixin.qq.com/s/Yy1653HbHbJ5SxreHHRBUA), image `Yy1653HbHbJ5SxreHHRBUA_1.png`, band rows 165-231 (67 px), layout validated: True

| # | printed label | measured RGB | as hex | mean RGB | CIE76 | block interior |
|---|---|---|---|---|---|---|
| 1 | `#414A78` | 72, 82, 128 | `#485280` | 72, 82, 128 | 3.4 | 37 values, 20% modal |
| 2 | `#6978A6` | 108, 120, 164 | `#6C78A4` | 108, 120, 164 | 1.4 | 43 values, 13% modal |
| 3 | `#A5B4D1` | 166, 179, 207 | `#A6B3CF` | 166, 179, 207 | 0.9 | 29 values, 22% modal |
| 4 | `#DCE3F0` | 222, 227, 240 | `#DEE3F0` | 222, 227, 240 | 0.7 | 23 values, 29% modal |
| 5 | `#8B739F` | 143, 121, 165 | `#8F79A5` | 143, 121, 165 | 2.3 | 27 values, 26% modal |
| 6 | `#B7A1C8` | 180, 159, 197 | `#B49FC5` | 180, 159, 198 | 1.1 | 33 values, 26% modal |
| 7 | `#DDD0E6` | 220, 208, 228 | `#DCD0E4` | 220, 208, 228 | 1.1 | 26 values, 25% modal |
| 8 | `#C7B38A` | 197, 177, 139 | `#C5B18B` | 197, 176, 139 | 1.7 | 35 values, 18% modal |

```python
# what the repository ships (printed labels)
sp.palette('indigo')
  #414A78 #6978A6 #A5B4D1 #DCE3F0 #8B739F #B7A1C8 #DDD0E6 #C7B38A
# what the pixels measure (modal interior RGB)
  #485280 #6C78A4 #A6B3CF #DEE3F0 #8F79A5 #B49FC5 #DCD0E4 #C5B18B
```

### 熏紫春庭 / lilac_garden

Source: [article](https://mp.weixin.qq.com/s/L4KrYecHM_Afq_2JXTKIpg), image `L4KrYecHM_Afq_2JXTKIpg_1.png`, band rows 157-239 (83 px), layout validated: False

| # | printed label | measured RGB | as hex | mean RGB | CIE76 | block interior |
|---|---|---|---|---|---|---|
| 1 | `#947CC4` | 147, 121, 194 | `#9379C2` | 147, 121, 194 | 1.4 | 38 values, 23% modal |
| 2 | `#DFD0ED` | 217, 201, 234 | `#D9C9EA` | 217, 201, 234 | 3.2 | 23 values, 36% modal |
| 3 | `#DBC496` | 217, 192, 146 | `#D9C092` | 217, 192, 146 | 1.6 | 32 values, 21% modal |
| 4 | `#A4C8AA` | 164, 198, 166 | `#A4C6A6` | 164, 198, 166 | 1.4 | 33 values, 23% modal |
| 5 | `#A4CDDF` | 161, 201, 219 | `#A1C9DB` | 162, 202, 220 | 1.4 | 34 values, 21% modal |
| 6 | `#EEB8C6` | 234, 178, 193 | `#EAB2C1` | 234, 178, 194 | 2.2 | 30 values, 20% modal |
| 7 | `#8992A0` | 136, 145, 159 | `#88919F` | 137, 145, 160 | 0.4 | 33 values, 22% modal |

```python
# what the repository ships (printed labels)
sp.palette('lilac_garden')
  #947CC4 #DFD0ED #DBC496 #A4C8AA #A4CDDF #EEB8C6 #8992A0
# what the pixels measure (modal interior RGB)
  #9379C2 #D9C9EA #D9C092 #A4C6A6 #A1C9DB #EAB2C1 #88919F
```

