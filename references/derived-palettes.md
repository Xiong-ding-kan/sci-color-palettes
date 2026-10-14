# Generated palette library

178 variants of the six published palettes, 184 schemes in total. Each id encodes its transform, so it is reproducible and readable: `glacier-h030` is glacier rotated 30 deg, `burgundy-clin` is burgundy tuned for clinical panels, `sage-mono` is a single-hue sage ramp.

Field suitability (C = clinical, D = database, B = basic) is in the last column; see [applications.md](applications.md) for the criteria. Each score is out of 100.

```python
import sci_palettes as sp
sp.suggest_for("临床")          # ranked for clinical work
sp.family("hue_rotate")         # one family, best score first
sp.search("#315C6B")           # palettes containing a colour you must use
```

## Summary

| Family | Count | Median score | Best |
|---|---|---|---|
| `clinical` | 12 | 71 | `lilac_garden-clin` (92) |
| `database` | 6 | 67 | `indigo+hues` (85) |
| `basic` | 6 | 67 | `lilac_garden-basic` (88) |
| `diverging` | 12 | 84 | `div-plum-sage-deep` (100) |
| `contrast` | 12 | 61 | `lilac_garden-light` (92) |
| `chroma` | 9 | 56 | `sage-rich` (68) |
| `complement` | 6 | 60 | `lilac_garden-comp` (73) |
| `monochrome` | 3 | 85 | `sage-mono` (85) |
| `blend` | 12 | 51 | `glacier+burgundy` (69) |
| `temperature` | 24 | 58 | `lilac_garden-warm` (78) |
| `hue_rotate` | 76 | 58 | `lilac_garden-h030` (82) |

Scores are family-relative: a diverging scale is measured against a smooth-scale threshold, not the categorical one, because a smooth scale is *supposed* to have small steps. Full criteria in [applications.md](applications.md).

## clinical (12)

Widest practical lightness span with colour-vision separation held high: survival curves, forest plots, adverse-event panels.

| id | 中文 | hex | score | C / D / B |
|---|---|---|---|---|
| `lilac_garden-clin` | 熏紫春庭·临床 | `#22154d` `#bbacc7` `#a59167` `#6c8d72` `#749aaa` `#b68692` `#272f3a` `#f2f0f5` | 92 | CDB |
| `lilac_garden-clin-hi` | 熏紫春庭·临床 | `#1c104b` `#b9abc7` `#a48f63` `#688a6f` `#6f98a9` `#b68390` `#232c37` `#f2f0f5` | 92 | CDB |
| `burgundy-clin-hi` | 勃艮第灰·临床 | `#38091e` `#824859` `#c08e9a` `#ffecf2` `#293f4f` `#859aa8` `#d3dee5` `#dabc90` | 80 | CDB |
| `dusk_rose-clin-hi` | 暮紫玫瑰·临床 | `#221630` `#695978` `#b6a9c3` `#f6eefd` `#764151` `#ba8896` `#efd0d5` `#99a793` | 79 | C-B |
| `burgundy-clin` | 勃艮第灰·临床 | `#3b1022` `#844c5c` `#c0929d` `#ffecf2` `#2e4352` `#889caa` `#d4dfe6` `#dabd94` | 79 | CDB |
| `dusk_rose-clin` | 暮紫玫瑰·临床 | `#261a34` `#6c5c7b` `#b7aac3` `#f6eefc` `#784555` `#ba8b98` `#efd1d6` `#9ca996` | 76 | C-B |
| `indigo-clin` | 靛蓝丁香·临床 | `#0e1d44` `#4a5983` `#9fadc9` `#eaf1fd` `#6c577e` `#aa95ba` `#e5d8ed` `#bfad86` | 66 | --B |
| `indigo-clin-hi` | 靛蓝丁香·临床 | `#051941` `#465681` `#9cabc8` `#eaf1fe` `#69527c` `#a994ba` `#e4d7ed` `#bfab82` | 66 | --B |
| `sage-clin-hi` | 鼠尾草紫·临床 | `#1a3726` `#839880` `#eaf4e3` `#1d1732` `#867a96` `#e6deef` `#b3985d` `#f7e9d0` | 65 | --B |
| `glacier-clin-hi` | 冰川蓝绿·临床 | `#001f28` `#2a636e` `#82afb1` `#d9efeb` `#35525f` `#a0b7c2` `#c2b58e` `#f8f0db` | 63 | --B |
| `sage-clin` | 鼠尾草紫·临床 | `#1f3b2b` `#879a83` `#eaf4e4` `#221b36` `#887c98` `#e6deee` `#b49a62` `#f5e9d1` | 63 | --B |
| `glacier-clin` | 冰川蓝绿·临床 | `#00232d` `#326670` `#86b1b2` `#dbefeb` `#395561` `#a2b8c2` `#c2b691` `#f8f0dc` | 62 | --- |

*Transforms*:
- `{"lightness_range": [12.0, 95.0], "chroma_scale": 0.95}`: widest practical lightness span for survival curves, forest plots and adverse-event panels; survives greyscale printing
- `{"lightness_range": [10.0, 95.0], "chroma_scale": 1.0}`: widest practical lightness span for survival curves, forest plots and adverse-event panels; survives greyscale printing

## database (6)

Each member stepped a further hue angle so cohort, centre and site categories stay maximally separated - registry and EHR panels.

| id | 中文 | hex | score | C / D / B |
|---|---|---|---|---|
| `indigo+hues` | 靛蓝丁香·队列 | `#0b1d46` `#744d72` `#cba2ab` `#ffede7` `#4c663d` `#6da99b` `#bfe1ec` `#d7a393` | 85 | -DB |
| `glacier+hues` | 冰川蓝绿·队列 | `#00232d` `#4e5f82` `#b8a2ba` `#fde5ea` `#4f5340` `#9fbab3` `#c3b68f` `#dff6e6` | 82 | -D- |
| `burgundy+hues` | 勃艮第灰·队列 | `#3d0e22` `#695c2f` `#6fa89e` `#e8f2ff` `#2d4352` `#a8939f` `#e5dad4` `#edb1cb` | 68 | --- |
| `lilac_garden+hues` | 熏紫春庭·队列 | `#211450` `#d1a8b0` `#4da0a0` `#927da0` `#9c9377` `#8293b9` `#213139` `#f4eff3` | 66 | --- |
| `sage+hues` | 鼠尾草紫·队列 | `#1d3a2a` `#739d97` `#dbf5fd` `#2c1d00` `#788669` `#d0e7e0` `#d785a2` `#ffe6df` | 58 | --B |
| `dusk_rose+hues` | 暮紫玫瑰·队列 | `#261a35` `#805769` `#cca6a2` `#fdeee1` `#295d46` `#63a1a3` `#c3dbed` `#b89f92` | 57 | --- |

*Transforms*:
- `{"incremental_hue": 45.0, "lightness_range": [12.0, 95.0]}`: each member stepped a further 45.0 deg so cohort, centre and site categories stay maximally separated - for registry and EHR panels
- `{"incremental_hue": 60.0, "lightness_range": [12.0, 95.0]}`: each member stepped a further 60.0 deg so cohort, centre and site categories stay maximally separated - for registry and EHR panels
- `{"incremental_hue": 90.0, "lightness_range": [12.0, 95.0]}`: each member stepped a further 90.0 deg so cohort, centre and site categories stay maximally separated - for registry and EHR panels
- `{"incremental_hue": 55.0, "lightness_range": [12.0, 95.0]}`: each member stepped a further 55.0 deg so cohort, centre and site categories stay maximally separated - for registry and EHR panels
- `{"incremental_hue": 40.0, "lightness_range": [12.0, 95.0]}`: each member stepped a further 40.0 deg so cohort, centre and site categories stay maximally separated - for registry and EHR panels

## basic (6)

Evenly spaced lightness ramp with restrained chroma: reads correctly in greyscale and in photocopied supplementary material.

| id | 中文 | hex | score | C / D / B |
|---|---|---|---|---|
| `lilac_garden-basic` | 熏紫春庭·基础科研 | `#271b4a` `#b6abc1` `#a2906e` `#708b74` `#7998a5` `#af8792` `#2d333c` `#eceaee` | 88 | CDB |
| `dusk_rose-basic` | 暮紫玫瑰·基础科研 | `#291f35` `#6c5f78` `#b3a9be` `#efe9f5` `#754a57` `#b48c97` `#e6ced1` `#9aa695` | 72 | --B |
| `burgundy-basic` | 勃艮第灰·基础科研 | `#3c1826` `#80505d` `#ba929b` `#f7e7ec` `#344552` `#8999a5` `#d1dadf` `#d4bb98` | 72 | CDB |
| `indigo-basic` | 靛蓝丁香·基础科研 | `#192242` `#505b7f` `#9fabc2` `#e5ebf5` `#6b597b` `#a796b5` `#ded4e6` `#bbaa8b` | 62 | --B |
| `glacier-basic` | 冰川蓝绿·基础科研 | `#032732` `#3d666f` `#8aacae` `#d7e8e5` `#415661` `#a3b4bd` `#beb394` `#f2ebd9` | 59 | --- |
| `sage-basic` | 鼠尾草紫·基础科研 | `#273e30` `#889885` `#e5ede0` `#262036` `#887e94` `#e1dbe8` `#b19a6b` `#f0e5d1` | 57 | --- |

*Transform*: `{"chroma_scale": 0.8, "lightness_range": [14.0, 93.0]}` - evenly spaced lightness ramp, restrained chroma: reads correctly in greyscale and in photocopied supplementary material

## diverging (12)

Symmetric scales with a pale centre at index 3: reference ranges, log fold change, change from baseline.

| id | 中文 | hex | score | C / D / B |
|---|---|---|---|---|
| `div-plum-sage-deep` | 双向·plum-sage·柔 | `#2c203b` `#6f6479` `#b8b0be` `#f6ead3` `#bdb199` `#828b70` `#476553` | 100 | --- |
| `div-plum-blue-deep` | 双向·plum-blue·柔 | `#2e0115` `#75535e` `#c0aeb4` `#f3e7fc` `#baaec3` `#7e799b` `#394a74` | 94 | --- |
| `div-plum-sage` | 双向·plum-sage | `#655675` `#968aa1` `#c9c1cf` `#f6ead3` `#cfc2aa` `#a0a98d` `#6f8f7b` | 92 | --- |
| `div-rose-teal-deep` | 双向·rose-teal·柔 | `#2c203b` `#6f6479` `#b8b0be` `#f2e7fc` `#a2b7b3` `#658185` `#324e5b` | 91 | --- |
| `div-plum-blue` | 双向·plum-blue | `#713e50` `#a17c88` `#d2bfc5` `#f3e7fc` `#ccbfd5` `#9f9abd` `#6978a6` | 88 | --- |
| `div-plum-sage-soft` | 双向·plum-sage·柔 | `#9a89ab` `#b9acc4` `#d8d0de` `#f6ead3` `#ded1b9` `#bac3a6` `#93b49f` | 84 | --- |
| `div-plum-blue-soft` | 双向·plum-blue·柔 | `#ae7688` `#c8a1ad` `#e1ced4` `#f3e7fc` `#dbcee4` `#bcb7db` `#93a2d2` | 83 | --- |
| `div-rose-teal` | 双向·rose-teal | `#655675` `#968aa1` `#c9c1cf` `#f2e7fc` `#b3c8c4` `#86a2a6` `#607d8b` | 83 | --- |
| `div-wine-teal-deep` | 双向·wine-teal·柔 | `#2f0116` `#75535e` `#c1aeb4` `#ffe4ec` `#a2b7b3` `#668185` `#324e5b` | 81 | --- |
| `div-rose-teal-soft` | 双向·rose-teal·柔 | `#9a89ab` `#b9acc4` `#d8d0de` `#f2e7fc` `#c2d7d3` `#a3bfc3` `#89a7b6` | 77 | --- |
| `div-wine-teal` | 双向·wine-teal | `#713e50` `#a17c88` `#d2bfc5` `#ffe4ec` `#b3c8c4` `#86a2a6` `#607d8b` | 73 | --- |
| `div-wine-teal-soft` | 双向·wine-teal·柔 | `#ae7688` `#c8a1ad` `#e1ced4` `#ffe4ec` `#c2d7d3` `#a2bfc3` `#89a7b6` | 67 | --- |

*Transforms*:
- `{"archetype": "plum-sage", "parents": ["dusk_rose", "sage"], "arm_scale": 1.45}`: symmetric diverging ramp with a pale centre at index 3: colour bars for reference ranges, log fold change or change from baseline
- `{"archetype": "plum-blue", "parents": ["burgundy", "indigo"], "arm_scale": 1.45}`: symmetric diverging ramp with a pale centre at index 3: colour bars for reference ranges, log fold change or change from baseline
- `{"archetype": "plum-sage", "parents": ["dusk_rose", "sage"], "arm_scale": 1.0}`: symmetric diverging ramp with a pale centre at index 3: colour bars for reference ranges, log fold change or change from baseline
- `{"archetype": "rose-teal", "parents": ["dusk_rose", "glacier"], "arm_scale": 1.45}`: symmetric diverging ramp with a pale centre at index 3: colour bars for reference ranges, log fold change or change from baseline
- `{"archetype": "plum-blue", "parents": ["burgundy", "indigo"], "arm_scale": 1.0}`: symmetric diverging ramp with a pale centre at index 3: colour bars for reference ranges, log fold change or change from baseline
- `{"archetype": "plum-sage", "parents": ["dusk_rose", "sage"], "arm_scale": 0.62}`: symmetric diverging ramp with a pale centre at index 3: colour bars for reference ranges, log fold change or change from baseline
- `{"archetype": "plum-blue", "parents": ["burgundy", "indigo"], "arm_scale": 0.62}`: symmetric diverging ramp with a pale centre at index 3: colour bars for reference ranges, log fold change or change from baseline
- `{"archetype": "rose-teal", "parents": ["dusk_rose", "glacier"], "arm_scale": 1.0}`: symmetric diverging ramp with a pale centre at index 3: colour bars for reference ranges, log fold change or change from baseline
- `{"archetype": "wine-teal", "parents": ["burgundy", "glacier"], "arm_scale": 1.45}`: symmetric diverging ramp with a pale centre at index 3: colour bars for reference ranges, log fold change or change from baseline
- `{"archetype": "rose-teal", "parents": ["dusk_rose", "glacier"], "arm_scale": 0.62}`: symmetric diverging ramp with a pale centre at index 3: colour bars for reference ranges, log fold change or change from baseline
- `{"archetype": "wine-teal", "parents": ["burgundy", "glacier"], "arm_scale": 1.0}`: symmetric diverging ramp with a pale centre at index 3: colour bars for reference ranges, log fold change or change from baseline
- `{"archetype": "wine-teal", "parents": ["burgundy", "glacier"], "arm_scale": 0.62}`: symmetric diverging ramp with a pale centre at index 3: colour bars for reference ranges, log fold change or change from baseline

## contrast (12)

The published ramp lifted into a paler range or deepened into a higher-contrast one.

| id | 中文 | hex | score | C / D / B |
|---|---|---|---|---|
| `lilac_garden-light` | 熏紫春庭·浅调 | `#5b4789` `#ccbdda` `#c0aa7d` `#87aa8d` `#8ab3c4` `#d29eac` `#57606d` `#f2f0f5` | 92 | CDB |
| `lilac_garden-dark` | 熏紫春庭·深调 | `#2b1c59` `#8d7f9a` `#837046` `#4f7056` `#507888` `#946471` `#2a333e` `#acaaaf` | 82 | -D- |
| `burgundy-light` | 勃艮第灰·浅调 | `#764355` `#b07182` `#d9a7b3` `#ffecf2` `#5a7081` `#9eb3c3` `#d9e4eb` `#e8ca9e` | 70 | CDB |
| `dusk_rose-light` | 暮紫玫瑰·浅调 | `#5b4c6b` `#9281a2` `#c9bcd6` `#f6eefd` `#a66c7d` `#d5a2b0` `#f7d7dc` `#afbea9` | 66 | --B |
| `sage-light` | 鼠尾草紫·浅调 | `#4c6b58` `#9eb39a` `#eaf4e3` `#564e6d` `#a69ab7` `#ebe3f4` `#cdb074` `#f8ebd2` | 63 | --B |
| `dusk_rose-dark` | 暮紫玫瑰·深调 | `#2f223e` `#5c4d6b` `#8a7e97` `#b0a8b7` `#6f3a4b` `#976775` `#b2959a` `#73816d` | 61 | --- |
| `burgundy-dark` | 勃艮第灰·深调 | `#46172a` `#773e4f` `#9a6b77` `#b9a6ac` `#2a404f` `#637886` `#96a1a7` `#a58a61` | 61 | -D- |
| `sage-dark` | 鼠尾草紫·深调 | `#1f3c2b` `#647861` `#a5ae9e` `#2b2340` `#6d627d` `#a69faf` `#8d753c` `#b2a68f` | 53 | --- |
| `indigo-light` | 靛蓝丁香·浅调 | `#474f7e` `#7180af` `#b0bfdd` `#eaf1fe` `#937ba8` `#c2acd3` `#eaddf3` `#d3be95` | 52 | --- |
| `glacier-light` | 冰川蓝绿·浅调 | `#2d5867` `#568d98` `#97c4c6` `#dbf1ed` `#627f8d` `#b1c9d4` `#d3c69e` `#f8f0db` | 50 | --- |
| `indigo-dark` | 靛蓝丁香·深调 | `#17254f` `#3c4d78` `#73829d` `#a5acb8` `#5e4871` `#857095` `#a79aaf` `#93815a` | 48 | --- |
| `glacier-dark` | 冰川蓝绿·深调 | `#002c38` `#1d5863` `#5b8688` `#97aba8` `#2f4c59` `#748a94` `#938762` `#b2ab97` | 46 | --- |

*Transforms*:
- `{"lightness_range": [35.0, 95.0]}`: lifted: pale, airy, fills and backgrounds
- `{"lightness_range": [16.0, 70.0]}`: deepened: high contrast, reads at small size

## chroma (9)

Saturation changed: muted, softened or intensified.

| id | 中文 | hex | score | C / D / B |
|---|---|---|---|---|
| `sage-rich` | 鼠尾草紫·高饱和 | `#689178` `#a3bd9e` `#d7e4cf` `#8276a0` `#b7a7cc` `#dfd5ea` `#d8b669` `#ecdcbc` | 68 | --- |
| `indigo-soft` | 靛蓝丁香·柔化 | `#141e3c` `#4c5779` `#9ca7bd` `#e3e9f3` `#675575` `#a392b0` `#dbd1e2` `#b7a788` | 63 | --B |
| `glacier-soft` | 冰川蓝绿·柔化 | `#00232d` `#3a626b` `#87a9ab` `#d6e6e3` `#3d525d` `#a0b1ba` `#bbb092` `#eee8d8` | 59 | --- |
| `indigo-muted` | 靛蓝丁香·低饱和 | `#151a32` `#4b526c` `#99a2b2` `#dfe3eb` `#60526b` `#9c8ea5` `#d4ccd9` `#afa28a` | 59 | --- |
| `glacier-rich` | 冰川蓝绿·高饱和 | `#205d70` `#418c9a` `#81bbbe` `#c5dfda` `#587e90` `#a0bdcb` `#c8b988` `#e7ddc3` | 56 | --- |
| `sage-soft` | 鼠尾草紫·柔化 | `#23382c` `#849581` `#e3eadd` `#221c32` `#837990` `#ded8e5` `#ad9768` `#ede1ce` | 56 | --- |
| `indigo-rich` | 靛蓝丁香·高饱和 | `#3b4983` `#6278b1` `#a1b4d8` `#dae3f3` `#8e70a8` `#ba9fd0` `#dfcfea` `#cab37f` | 56 | --- |
| `glacier-muted` | 冰川蓝绿·低饱和 | `#061e26` `#3f5c62` `#89a3a4` `#d3dfdd` `#3d4d55` `#9eacb2` `#b3aa94` `#e7e2d6` | 54 | --- |
| `sage-muted` | 鼠尾草紫·低饱和 | `#233329` `#828e80` `#dee4da` `#1d1929` `#7c7586` `#d6d1db` `#a2906e` `#e4dbcc` | 50 | --- |

*Transforms*:
- `{"chroma_scale": 1.25, "lightness_range": null}`: chroma x1.25: more vivid, for slides and graphical abstracts
- `{"chroma_scale": 0.78, "lightness_range": [12.0, 92.0]}`: gently desaturated: keeps the hue character, calms a busy figure
- `{"chroma_scale": 0.6, "lightness_range": [10.0, 90.0]}`: chroma x0.60 with a wider lightness ramp; for dense multi-panel figures

## complement (6)

Every hue moved to its opposite. Loud by design; poster and graphical-abstract territory.

| id | 中文 | hex | score | C / D / B |
|---|---|---|---|---|
| `lilac_garden-comp` | 熏紫春庭·互补 | `#71924a` `#cbdbbe` `#a6c9f7` `#d7b5d4` `#e2c0ae` `#96d2c6` `#989182` `#f3f5f0` | 73 | -DB |
| `burgundy-comp` | 勃艮第灰·互补 | `#0f584b` `#36857a` `#76afa5` `#caded9` `#736251` `#b09e8f` `#d6cbc5` `#93c0eb` | 68 | CDB |
| `dusk_rose-comp` | 暮紫玫瑰·互补 | `#506143` `#7c8e6e` `#afbca3` `#d9e2d3` `#458b7f` `#7bb4a9` `#b6d7d3` `#bbadc2` | 63 | --- |
| `sage-comp` | 鼠尾草紫·互补 | `#9d7f94` `#c4b0c9` `#e6dced` `#74815f` `#a4b294` `#d4dccb` `#89bffa` `#cedff7` | 57 | --- |
| `indigo-comp` | 靛蓝丁香·互补 | `#4c5020` `#7f7b4c` `#beb396` `#e8e2d5` `#698459` `#99b08a` `#cbd9c3` `#99b8e0` | 55 | --- |
| `glacier-comp` | 冰川蓝绿·互补 | `#6d5042` `#a2786e` `#cfa7a7` `#e9d5d9` `#8b7466` `#c9b4aa` `#a6bae1` `#d4def3` | 49 | --- |

*Transform*: `{"hue_shift": 180}` - each hue moved to its opposite; high separation, poster-friendly

## monochrome (3)

One hue family, lightness only. The safest option for print.

| id | 中文 | hex | score | C / D / B |
|---|---|---|---|---|
| `sage-mono` | 鼠尾草紫·单色 | `#322d14` `#6e674d` `#f4eedb` `#181300` `#50492f` `#aea896` `#94874a` `#d2cab1` | 85 | C-B |
| `indigo-mono` | 靛蓝丁香·单色 | `#110d35` `#2e284f` `#8a839f` `#f0ebfe` `#4c446e` `#6a6288` `#cdc7de` `#aca2cd` | 85 | C-B |
| `glacier-mono` | 冰川蓝绿·单色 | `#001716` `#175151` `#446f6e` `#b4d0cf` `#103232` `#718c8b` `#73b3b2` `#d3f4f3` | 84 | C-B |

*Transform*: `{"monochrome": true}` - single hue family, lightness only: the safest option for print

## blend (12)

Two published palettes mixed in LCh: the lightness ramp of the first, the colour character of the second.

| id | 中文 | hex | score | C / D / B |
|---|---|---|---|---|
| `glacier+burgundy` | 冰川蓝绿×勃艮第灰 | `#504f70` `#777ba2` `#a1aaca` `#d2dae8` `#597282` `#9ab0bd` `#aacabe` `#dccaa9` | 69 | --- |
| `glacier+lilac_garden` | 冰川蓝绿×熏紫春庭 | `#4872a0` `#95adca` `#a3c4a5` `#b2d4c5` `#81a4b4` `#c1bcd9` `#86ada5` `#f8e4e4` | 57 | --- |
| `sage+lilac_garden` | 鼠尾草紫×熏紫春庭 | `#3193af` `#a1cdda` `#d5d5b3` `#6ca5b7` `#aabbd8` `#e5c7dc` `#cb98a8` `#fae3e4` | 57 | --- |
| `burgundy+lilac_garden` | 勃艮第灰×熏紫春庭 | `#8e5885` `#c39ab6` `#ddaa98` `#dfc9b3` `#7a99ab` `#b9afcc` `#a5b0bb` `#f5ced2` | 57 | --- |
| `glacier+dusk_rose` | 冰川蓝绿×暮紫玫瑰 | `#475a77` `#6c88a6` `#9eb8cf` `#cedfea` `#7e7899` `#b3aeca` `#e2bdad` `#c6c9b3` | 54 | --- |
| `burgundy+indigo` | 勃艮第灰×靛蓝丁香 | `#634167` `#916d95` `#bba4c2` `#e4dbe9` `#657091` `#9ba5c3` `#cbd1e1` `#ceb58b` | 53 | --- |
| `sage+burgundy` | 鼠尾草紫×勃艮第灰 | `#7d6648` `#b09173` `#d7bda8` `#bba3b7` `#7f88a2` `#b6bdcf` `#9fceb9` `#dfcaa7` | 49 | --- |
| `glacier+indigo` | 冰川蓝绿×靛蓝丁香 | `#2c5575` `#5283a2` `#92b8ca` `#cee1e8` `#697b9c` `#a3b1ce` `#e9bcbb` `#d6c8a9` | 48 | --- |
| `indigo+lilac_garden` | 靛蓝丁香×熏紫春庭 | `#68639e` `#a7a2c9` `#e4afbd` `#afd8dd` `#8ca2c7` `#d6abc8` `#b0b1c4` `#efcccd` | 48 | --- |
| `dusk_rose+sage` | 暮紫玫瑰×鼠尾草紫 | `#48788a` `#76a7b5` `#b0d2da` `#b2a8c1` `#b18ba7` `#d6b9ce` `#eebaa6` `#c7c9b0` | 47 | --- |
| `dusk_rose+lilac_garden` | 暮紫玫瑰×熏紫春庭 | `#7d689b` `#b8a8c7` `#e7b2b4` `#afd5e3` `#a49ec4` `#deaab8` `#b9acbd` `#c1d6db` | 45 | --- |
| `indigo+sage` | 靛蓝丁香×鼠尾草紫 | `#297383` `#61a1aa` `#abd0d2` `#a9adc6` `#a08db3` `#cabbd8` `#f5b8ba` `#d8c7a6` | 42 | --- |

*Transforms*:
- `{"blend": ["glacier", "burgundy"], "t": 0.5}`: lightness ramp of glacier, hue and chroma halfway to burgundy
- `{"blend": ["glacier", "lilac_garden"], "t": 0.5}`: lightness ramp of glacier, hue and chroma halfway to lilac_garden
- `{"blend": ["sage", "lilac_garden"], "t": 0.5}`: lightness ramp of sage, hue and chroma halfway to lilac_garden
- `{"blend": ["burgundy", "lilac_garden"], "t": 0.5}`: lightness ramp of burgundy, hue and chroma halfway to lilac_garden
- `{"blend": ["glacier", "dusk_rose"], "t": 0.5}`: lightness ramp of glacier, hue and chroma halfway to dusk_rose
- `{"blend": ["burgundy", "indigo"], "t": 0.5}`: lightness ramp of burgundy, hue and chroma halfway to indigo
- `{"blend": ["sage", "burgundy"], "t": 0.5}`: lightness ramp of sage, hue and chroma halfway to burgundy
- `{"blend": ["glacier", "indigo"], "t": 0.5}`: lightness ramp of glacier, hue and chroma halfway to indigo
- `{"blend": ["indigo", "lilac_garden"], "t": 0.5}`: lightness ramp of indigo, hue and chroma halfway to lilac_garden
- `{"blend": ["dusk_rose", "sage"], "t": 0.5}`: lightness ramp of dusk_rose, hue and chroma halfway to sage
- `{"blend": ["dusk_rose", "lilac_garden"], "t": 0.5}`: lightness ramp of dusk_rose, hue and chroma halfway to lilac_garden
- `{"blend": ["indigo", "sage"], "t": 0.5}`: lightness ramp of indigo, hue and chroma halfway to sage

## temperature (24)

The ramp pulled toward orange or cyan, tapered by chroma so near-neutral members stay neutral.

| id | 中文 | hex | score | C / D / B |
|---|---|---|---|---|
| `lilac_garden-warm` | 熏紫春庭·暖调 | `#b372b0` `#e7cee8` `#c8ca98` `#98cab5` `#aacbe3` `#f0b8b9` `#8b91a0` `#f5f3f8` | 78 | --B |
| `lilac_garden-cool` | 熏紫春庭·冷调 | `#6986cf` `#d6d2f1` `#eabe9b` `#b2c5a1` `#a0ceda` `#e7b9d3` `#8793a0` `#f5f3f8` | 74 | -DB |
| `burgundy-warmer` | 勃艮第灰·暖调 | `#714137` `#a36b5b` `#c9998f` `#ead5d8` `#5b667a` `#95a2b4` `#c5cfd7` `#b3c191` | 73 | CDB |
| `burgundy-warm` | 勃艮第灰·暖调 | `#733e42` `#a66867` `#cb9798` `#ead5d9` `#57677a` `#92a3b4` `#c5cfd6` `#c3bd8c` | 71 | CDB |
| `lilac_garden-warmer` | 熏紫春庭·暖调 | `#c36c9c` `#edcde2` `#b8ce9f` `#90cac0` `#b1c9e4` `#efbab0` `#8d91a0` `#f5f3f8` | 71 | --B |
| `dusk_rose-warmer` | 暮紫玫瑰·暖调 | `#765167` `#a57d93` `#cbb0c4` `#e8dbe8` `#a87264` `#d09e95` `#e9c9c7` `#9fb8a8` | 69 | --- |
| `burgundy-cool` | 勃艮第灰·冷调 | `#69405e` `#9d6989` `#c398ae` `#e8d5dd` `#4e6977` `#8ca5b1` `#c3cfd6` `#e3b193` | 67 | --B |
| `dusk_rose-cool` | 暮紫玫瑰·冷调 | `#58597a` `#8685a8` `#b9b5d0` `#e2ddec` `#a07190` `#c99db6` `#e7c9d2` `#acb59e` | 65 | --- |
| `burgundy-cooler` | 勃艮第灰·冷调 | `#5e4468` `#906d96` `#bc9ab7` `#e7d5de` `#4c6a76` `#8ba5b0` `#c3cfd5` `#eaad9d` | 60 | --- |
| `lilac_garden-cooler` | 熏紫春庭·冷调 | `#388ed1` `#ced4f3` `#f3baa4` `#bdc39b` `#9fcfd5` `#debcdc` `#85939f` `#f5f3f8` | 60 | --- |
| `glacier-cooler` | 冰川蓝绿·冷调 | `#2e5e61` `#578b85` `#91b9af` `#cbded7` `#5c7e86` `#a3bdc4` `#dab298` `#ecdbc9` | 59 | --- |
| `dusk_rose-cooler` | 暮紫玫瑰·冷调 | `#4d5c7c` `#7a88ab` `#b2b7d2` `#e0dded` `#94759c` `#c09fbf` `#e5c9d5` `#b0b49c` | 59 | --- |
| `indigo-warmer` | 靛蓝丁香·暖调 | `#683e65` `#916d95` `#b6b0cd` `#dfe2f0` `#a56b84` `#ce9bb2` `#e5cee0` `#a9bb91` | 58 | --B |
| `dusk_rose-warm` | 暮紫玫瑰·暖调 | `#6f536e` `#9e7f9b` `#c7b1c9` `#e6dbea` `#ab7070` `#d19c9e` `#e9c9ca` `#a2b7a5` | 57 | --- |
| `sage-warm` | 鼠尾草紫·暖调 | `#689082` `#a0bda9` `#d6e4d4` `#8d7492` `#bea6c0` `#e1d5e5` `#bcbf7d` `#e3dec3` | 56 | --- |
| `indigo-warm` | 靛蓝丁香·暖调 | `#5a436f` `#81729f` `#aeb2d0` `#dee3f0` `#9c6e91` `#c59dbd` `#e2cfe3` `#b7b88c` | 56 | --- |
| `sage-cool` | 鼠尾草紫·冷调 | `#778e75` `#afba9e` `#dce2d0` `#737b9d` `#ababca` `#dbd7e8` `#e7af81` `#eedac4` | 55 | --- |
| `sage-cooler` | 鼠尾草紫·冷调 | `#7e8c70` `#b5b99c` `#dee2cf` `#677d9e` `#a3adcc` `#d9d7e9` `#f3a98d` `#f2d9c5` | 55 | --- |
| `indigo-cool` | 靛蓝丁香·冷调 | `#1c507a` `#4e7ea6` `#9cb6d0` `#dae3f0` `#7479a8` `#a5a6cf` `#d8d1e9` `#d4ae8e` | 54 | --- |
| `glacier-warmer` | 冰川蓝绿·暖调 | `#3e5970` `#5f87a0` `#8eb7c5` `#c8dedd` `#677b8e` `#a9bbc9` `#adc09a` `#dedfc9` | 50 | --- |
| `glacier-cool` | 冰川蓝绿·冷调 | `#2e5d66` `#538b8d` `#8eb9b5` `#caded8` `#5d7e88` `#a3bdc5` `#d2b594` `#e9dcc8` | 49 | --- |
| `indigo-cooler` | 靛蓝丁香·冷调 | `#005372` `#3881a2` `#96b8cf` `#d9e4f0` `#5f7eaa` `#95aad2` `#d3d3ea` `#dcaa95` | 49 | --- |
| `glacier-warm` | 冰川蓝绿·暖调 | `#375b6f` `#58889c` `#8cb8c1` `#c8dedc` `#647c8d` `#a7bbc8` `#b8bd95` `#e1dec8` | 48 | --- |
| `sage-warmer` | 鼠尾草紫·暖调 | `#639089` `#9bbeae` `#d4e4d6` `#95718b` `#c4a4bb` `#e3d5e4` `#a7c486` `#dedfc4` | 47 | --- |

*Transforms*:
- `{"temperature": "warm", "degrees": 22}`: hue pulled 22 deg toward orange, tapered by chroma so near-neutral members stay neutral
- `{"temperature": "cool", "degrees": 22}`: hue pulled 22 deg toward cyan, tapered by chroma so near-neutral members stay neutral
- `{"temperature": "warmer", "degrees": 40}`: hue pulled 40 deg toward orange, tapered by chroma so near-neutral members stay neutral
- `{"temperature": "cooler", "degrees": 40}`: hue pulled 40 deg toward cyan, tapered by chroma so near-neutral members stay neutral

## hue_rotate (76)

The same scheme at a different hue angle. Use to match a journal cover, a co-author's slide deck, or to separate two figures that would otherwise look identical.

| id | 中文 | hex | score | C / D / B |
|---|---|---|---|---|
| `lilac_garden-h030` | 熏紫春庭·色相+30 | `#bb6fa7` `#eecce0` `#c1cc9b` `#92cabd` `#b3c9e5` `#efb9b2` `#928f9e` `#f8f2f6` | 82 | -DB |
| `burgundy-h030` | 勃艮第灰·色相+30 | `#723f3d` `#a56961` `#ca9991` `#ebd5d3` `#5f657a` `#9aa1b4` `#c9cdd7` `#bcbf8e` | 79 | CDB |
| `burgundy-h240` | 勃艮第灰·色相+240 | `#00556d` `#3681a1` `#7babc5` `#cadde6` `#5d6956` `#9ba492` `#cbcfc5` `#d3b0db` | 79 | CDB |
| `lilac_garden-h270` | 熏紫春庭·色相+270 | `#0096a8` `#afdde9` `#f5b5ca` `#dfb79f` `#b4cdb5` `#b0c8ee` `#819690` `#eef5f7` | 79 | -DB |
| `lilac_garden-h000` | 熏紫春庭·色相+0 | `#947cc4` `#dfd0ed` `#dbc496` `#a4c8aa` `#a4cddf` `#eeb8c6` `#8992a0` `#f5f3f8` | 78 | -DB |
| `lilac_garden-h210` | 熏紫春庭·色相+210 | `#3f9969` `#bbdecb` `#c7c1f2` `#e5b1c1` `#d6c5a9` `#8fd1da` `#909384` `#f0f5f2` | 78 | -DB |
| `burgundy-h210` | 勃艮第灰·色相+210 | `#00575d` `#228591` `#71aeb8` `#c8dee0` `#696651` `#a6a18e` `#d1cdc3` `#b4b8e9` | 76 | CDB |
| `lilac_garden-h090` | 熏紫春庭·色相+90 | `#ca6f60` `#f5cdc2` `#8dd4c3` `#92c7df` `#d8bfd8` `#d5c59e` `#a08c92` `#faf2f1` | 75 | -DB |
| `lilac_garden-h120` | 熏紫春庭·色相+120 | `#b67b46` `#ebd1b9` `#81d4dc` `#a7c1e6` `#e4bcca` `#bfcba3` `#a28d8b` `#f8f3ef` | 73 | --B |
| `lilac_garden-h180` | 熏紫春庭·色相+180 | `#71924a` `#cbdbbe` `#a6c9f7` `#d7b5d4` `#e2c0ae` `#96d2c6` `#989182` `#f3f5f0` | 73 | -DB |
| `burgundy-h060` | 勃艮第灰·色相+60 | `#6a452d` `#9a7050` `#c19d84` `#e8d7ce` `#6d6175` `#a69eb0` `#cfccd6` `#a1c59c` | 72 | --B |
| `burgundy-h120` | 勃艮第灰·色相+120 | `#48522a` `#6e7f51` `#9ca985` `#d9dccc` `#7b5e61` `#b69a9f` `#d8cacd` `#76c9cb` | 72 | CDB |
| `lilac_garden-h060` | 熏紫春庭·色相+60 | `#cc6983` `#f6cbd1` `#a5d1ab` `#8acad1` `#c6c4e2` `#e6bea4` `#9b8d99` `#f9f2f3` | 72 | -DB |
| `burgundy-h090` | 勃艮第灰·色相+90 | `#5b4c26` `#87784a` `#b0a37f` `#e1d9cb` `#775f6c` `#b19ba8` `#d5cbd2` `#87c9b2` | 71 | --B |
| `burgundy-h270` | 勃艮第灰·色相+270 | `#2b5074` `#5b7ba7` `#91a5c9` `#d1dbe9` `#516b5f` `#90a69a` `#c6d0c9` `#e7abc5` | 71 | CDB |
| `lilac_garden-h240` | 熏紫春庭·色相+240 | `#00998d` `#b0dfda` `#e4b9e1` `#e7b2ae` `#c5caab` `#99cde9` `#879589` `#eef5f4` | 71 | -DB |
| `lilac_garden-h300` | 熏紫春庭·色相+300 | `#0093c2` `#badaf2` `#f8b6b1` `#cfbd98` `#a6d0c3` `#cbc1e8` `#7f9698` `#eff5f8` | 71 | -DB |
| `burgundy-h000` | 勃艮第灰·色相+0 | `#713e50` `#a56778` `#c997a3` `#e9d5db` `#526879` `#8fa4b3` `#c4cfd6` `#d5b78c` | 70 | CDB |
| `dusk_rose-h060` | 暮紫玫瑰·色相+60 | `#7c5057` `#ac7c83` `#d5afb4` `#f0dadc` `#a0775a` `#c8a289` `#e2cdbc` `#94b8b7` | 69 | --- |
| `burgundy-h300` | 勃艮第灰·色相+300 | `#4d4970` `#7e72a0` `#aa9fc3` `#dbd8e7` `#4a6b69` `#89a7a4` `#c2d0ce` `#edaaac` | 69 | CDB |
| `dusk_rose-h240` | 暮紫玫瑰·色相+240 | `#2c6561` `#5a928e` `#96c0bc` `#cce4e1` `#4487a5` `#7db1ca` `#bcd4e5` `#cbaaac` | 68 | --- |
| `burgundy-h180` | 勃艮第灰·色相+180 | `#0f584b` `#36857a` `#76afa5` `#caded9` `#736251` `#b09e8f` `#d6cbc5` `#93c0eb` | 68 | CDB |
| `lilac_garden-h150` | 熏紫春庭·色相+150 | `#98883d` `#dcd6b8` `#8ad0ef` `#c1bae1` `#e7bdbb` `#a8d0b2` `#9f8e85` `#f6f4ef` | 66 | -DB |
| `dusk_rose-h150` | 暮紫玫瑰·色相+150 | `#625d3c` `#8f8966` `#beb89d` `#e3dfcf` `#5e8969` `#8db396` `#bed6c8` `#adb0c8` | 65 | --- |
| `lilac_garden-h330` | 熏紫春庭·色相+330 | `#568ad1` `#ccd5f3` `#efbc9e` `#bac39d` `#9fcfd3` `#e1bbda` `#82949e` `#f2f4f9` | 65 | --B |
| `dusk_rose-h000` | 暮紫玫瑰·色相+0 | `#655675` `#9382a3` `#c0b3cd` `#e4dceb` `#a96f80` `#cf9caa` `#e8c9ce` `#a7b6a1` | 64 | --- |
| `dusk_rose-h030` | 暮紫玫瑰·色相+30 | `#755168` `#a47d95` `#ceb0c2` `#ecdae4` `#aa716a` `#d19d97` `#e8cac3` `#9bb8ab` | 64 | --- |
| `dusk_rose-h090` | 暮紫玫瑰·色相+90 | `#7a5248` `#aa7e73` `#d4b0a7` `#f0dbd5` `#8e7e54` `#b8a883` `#d7d1bb` `#96b7c2` | 64 | --B |
| `dusk_rose-h270` | 暮紫玫瑰·色相+270 | `#276470` `#58919e` `#95bfc9` `#cce3e9` `#6381ab` `#93abcf` `#c8d0e6` `#c9aba1` | 64 | --B |
| `dusk_rose-h180` | 暮紫玫瑰·色相+180 | `#506143` `#7c8e6e` `#afbca3` `#d9e2d3` `#458b7f` `#7bb4a9` `#b6d7d3` `#bbadc2` | 63 | --- |
| `dusk_rose-h330` | 暮紫玫瑰·色相+330 | `#4f5c7c` `#7c88aa` `#afb8d3` `#dadfee` `#9b7395` `#c39fbd` `#e2cad9` `#b5b39b` | 63 | --- |
| `dusk_rose-h210` | 暮紫玫瑰·色相+210 | `#3d6450` `#68917c` `#a0bfae` `#d1e3d9` `#368b95` `#74b4bc` `#b5d6de` `#c6aab8` | 62 | --- |
| `indigo-h120` | 靛蓝丁香·色相+120 | `#71402b` `#a36c5b` `#d2aaa3` `#f2dedc` `#987650` `#c4a482` `#e5d1be` `#78c1c8` | 61 | --B |
| `indigo-h240` | 靛蓝丁香·色相+240 | `#015844` `#49856b` `#9cbba6` `#d9e6dc` `#328985` `#71b5b1` `#b8dcd9` `#d0a9cd` | 61 | --- |
| `glacier-h060` | 冰川蓝绿·色相+60 | `#53546f` `#7382a2` `#9db3cd` `#ccdce6` `#7a768c` `#b9b6c9` `#9ac3a8` `#cde3d4` | 60 | --- |
| `burgundy-h330` | 勃艮第灰·色相+330 | `#644263` `#986b8f` `#be99b5` `#e3d6e2` `#4a6a73` `#89a6ad` `#c1d0d3` `#e6af97` | 60 | --- |
| `glacier-h240` | 冰川蓝绿·色相+240 | `#56593d` `#8a8261` `#c0af95` `#e6d7cd` `#767b65` `#b7baa8` `#d6aecb` `#edd7e7` | 59 | --- |
| `dusk_rose-h120` | 暮紫玫瑰·色相+120 | `#71573e` `#a08468` `#ccb49f` `#ebddd0` `#778559` `#a3ae88` `#cad4bf` `#9fb4c8` | 59 | --- |
| `sage-h015` | 鼠尾草紫·色相+15 | `#689082` `#9fbda9` `#d4e4d6` `#8b7493` `#bea6c0` `#e3d5e4` `#c4bc7b` `#e2dec4` | 58 | --- |
| `indigo-h210` | 靛蓝丁香·色相+210 | `#31552e` `#658157` `#adb79a` `#e0e4d7` `#4d886d` `#82b49c` `#bfdbcd` `#b6b0db` | 58 | --B |
| `sage-h180` | 鼠尾草紫·色相+180 | `#9d7f94` `#c4b0c9` `#e6dced` `#74815f` `#a4b294` `#d4dccb` `#89bffa` `#cedff7` | 57 | --- |
| `indigo-h030` | 靛蓝丁香·色相+30 | `#61416b` `#89709b` `#b8afcc` `#e4e1ee` `#a16c8b` `#cb9cb6` `#e8cddc` `#b0ba8e` | 57 | --- |
| `indigo-h090` | 靛蓝丁香·色相+90 | `#783a3f` `#a76870` `#d2a9b2` `#f1dee3` `#a66f5e` `#d19d8e` `#edcec5` `#82c1b3` | 57 | --- |
| `burgundy-h150` | 勃艮第灰·色相+150 | `#305638` `#538362` `#87ad93` `#d0ddd1` `#7a5f57` `#b59b95` `#d8cac8` `#7ac6e0` | 56 | --- |
| `indigo-h270` | 靛蓝丁香·色相+270 | `#005658` `#2d8683` `#8fbcb5` `#d4e7e2` `#2a879b` `#6fb3c4` `#b8dae4` `#dfa6b8` | 56 | --- |
| `sage-h000` | 鼠尾草紫·色相+0 | `#6f8f7b` `#a7bca3` `#d9e3d2` `#817799` `#b5a8c6` `#ded6e7` `#d4b77a` `#e9dcc3` | 55 | --- |
| `indigo-h060` | 靛蓝丁香·色相+60 | `#733a56` `#9e6987` `#c9abc1` `#ecdfe9` `#aa6b74` `#d49aa1` `#eecdd0` `#97bf9d` | 55 | --- |
| `indigo-h180` | 靛蓝丁香·色相+180 | `#4c5020` `#7f7b4c` `#beb396` `#e8e2d5` `#698459` `#99b08a` `#cbd9c3` `#99b8e0` | 55 | --- |
| `indigo-h300` | 靛蓝丁香·色相+300 | `#005467` `#278498` `#8cbbc3` `#d2e6e9` `#4683a8` `#80afd0` `#c1d8eb` `#e1a7a2` | 55 | --B |
| `glacier-h030` | 冰川蓝绿·色相+30 | `#405971` `#5e87a0` `#90b7c7` `#c8dee1` `#6c7a8e` `#aeb9ca` `#b0bf98` `#d9e0cb` | 54 | --- |
| `sage-h090` | 鼠尾草紫·色相+90 | `#688ca2` `#93bdcb` `#cae4ec` `#9e716a` `#cda49b` `#ecd4ce` `#67ccb5` `#c0e5dc` | 54 | --- |
| `indigo-h330` | 靛蓝丁香·色相+330 | `#01527a` `#447fa5` `#94b9ce` `#d5e5ee` `#6b7baa` `#9ca8d1` `#ced4eb` `#d9ac91` | 54 | --- |
| `glacier-h150` | 冰川蓝绿·色相+150 | `#714d4d` `#a3767e` `#cba7b5` `#e4d5e0` `#90726f` `#ccb3b1` `#8ec0dd` `#c9e1f0` | 52 | --- |
| `dusk_rose-h300` | 暮紫玫瑰·色相+300 | `#37617a` `#658da9` `#9fbcd1` `#d1e1ee` `#837aa5` `#ada5ca` `#d6cde2` `#c1af9b` | 52 | --- |
| `sage-h270` | 鼠尾草紫·色相+270 | `#9e836d` `#d1afa1` `#f3dbd4` `#49858e` `#84b5c0` `#c4dee4` `#f6a2bf` `#f8d4de` | 52 | --- |
| `sage-h345` | 鼠尾草紫·色相-15 | `#778e75` `#afba9e` `#dee2cf` `#757a9d` `#ababca` `#d9d7e9` `#e2b17e` `#efdac4` | 52 | --- |
| `glacier-h015` | 冰川蓝绿·色相+15 | `#385b6f` `#57899b` `#8cb8c1` `#c8dede` `#657c8d` `#a9bbc9` `#bbbc94` `#dfdfc9` | 51 | --- |
| `glacier-h210` | 冰川蓝绿·色相+210 | `#63543c` `#997c64` `#cbaa9b` `#ead5d2` `#827863` `#c1b7a6` `#c0b3da` `#e1daef` | 51 | --- |
| `sage-h060` | 鼠尾草紫·色相+60 | `#5f8f98` `#91bfbf` `#cae5e3` `#9e6f7b` `#cda2aa` `#ecd3d7` `#8dc896` `#cbe4cf` | 51 | --- |
| `sage-h210` | 鼠尾草紫·色相+210 | `#a67d85` `#d0adbc` `#efdae6` `#60846c` `#93b5a1` `#caded2` `#b9b3f4` `#dfdaf4` | 51 | --- |
| `sage-h240` | 鼠尾草紫·色相+240 | `#a57f77` `#d5acad` `#f4dadc` `#4f867d` `#87b6b1` `#c4dedb` `#e0a8de` `#eed6eb` | 51 | --- |
| `indigo-h000` | 靛蓝丁香·色相+0 | `#414a78` `#6978a6` `#a5b4d1` `#dce3f0` `#8b739f` `#b7a1c8` `#ddd0e6` `#c7b38a` | 51 | --- |
| `glacier-h000` | 冰川蓝绿·色相+0 | `#315c6b` `#538a95` `#8cb9bb` `#c9deda` `#607d8b` `#a5bcc7` `#c6b992` `#e5ddc8` | 50 | --- |
| `glacier-h330` | 冰川蓝绿·色相+330 | `#2e5e60` `#578b85` `#93b9ad` `#ceddd3` `#5c7f83` `#a2bec0` `#d8b296` `#efdaca` | 50 | --- |
| `glacier-h180` | 冰川蓝绿·色相+180 | `#6d5042` `#a2786e` `#cfa7a7` `#e9d5d9` `#8b7466` `#c9b4aa` `#a6bae1` `#d4def3` | 49 | --- |
| `sage-h150` | 鼠尾草紫·色相+150 | `#8e83a0` `#b2b4d1` `#dbdff2` `#877b5a` `#b6ad8e` `#ded9c8` `#5bc7ef` `#c1e2f3` | 49 | --- |
| `glacier-h270` | 冰川蓝绿·色相+270 | `#465c45` `#788767` `#b1b397` `#dfd9cb` `#6a7e6d` `#adbcae` `#e1abb7` `#f4d6dc` | 48 | --- |
| `glacier-h345` | 冰川蓝绿·色相-15 | `#2e5d66` `#538b8e` `#8eb9b4` `#cbded6` `#5d7e87` `#a3bdc4` `#d0b693` `#eadbc8` | 48 | --- |
| `sage-h030` | 鼠尾草紫·色相+30 | `#62908a` `#99beb0` `#d0e5da` `#94728c` `#c5a4ba` `#e7d4e0` `#b3c180` `#dae0c6` | 48 | --- |
| `indigo-h150` | 靛蓝丁香·色相+150 | `#61491f` `#94734d` `#cbae99` `#efe0d7` `#837e4e` `#b0aa80` `#d9d5be` `#80bdd9` | 48 | --- |
| `glacier-h090` | 冰川蓝绿·色相+90 | `#645067` `#897c9c` `#afaecb` `#d3dae8` `#867385` `#c3b4c3` `#88c5bc` `#c5e4de` | 47 | --- |
| `glacier-h300` | 冰川蓝绿·色相+300 | `#385e52` `#658a75` `#a0b79f` `#d7dccd` `#607f78` `#a5beb7` `#e2ada4` `#f4d7d2` | 47 | --- |
| `sage-h120` | 鼠尾草紫·色相+120 | `#7a88a5` `#a0b9d2` `#d1e2f1` `#96765e` `#c4a891` `#e7d6c9` `#4dcbd6` `#bce5e9` | 47 | --- |
| `glacier-h120` | 冰川蓝绿·色相+120 | `#6e4d5a` `#9a778f` `#c0aac2` `#dcd7e6` `#8e717a` `#cab2ba` `#83c4cf` `#c3e3e9` | 46 | --- |
| `sage-h330` | 鼠尾草紫·色相+330 | `#808c6f` `#b8b89b` `#e4e0ce` `#697d9e` `#a1adcc` `#d3d9ea` `#edac86` `#f4d8c7` | 46 | --- |
| `sage-h300` | 鼠尾草紫·色相+300 | `#90886a` `#c7b39a` `#edddcf` `#53829a` `#8eb2ca` `#c9dce9` `#faa49f` `#fad5d1` | 44 | --- |

*Transforms*:
- `{"hue_shift": 30}`: every hue rotated 30 deg; same lightness and chroma structure
- `{"hue_shift": 240}`: every hue rotated 240 deg; same lightness and chroma structure
- `{"hue_shift": 270}`: every hue rotated 270 deg; same lightness and chroma structure
- `{"hue_shift": 0}`: every hue rotated 0 deg; same lightness and chroma structure
- `{"hue_shift": 210}`: every hue rotated 210 deg; same lightness and chroma structure
- `{"hue_shift": 90}`: every hue rotated 90 deg; same lightness and chroma structure
- `{"hue_shift": 120}`: every hue rotated 120 deg; same lightness and chroma structure
- `{"hue_shift": 180}`: every hue rotated 180 deg; same lightness and chroma structure
- `{"hue_shift": 60}`: every hue rotated 60 deg; same lightness and chroma structure
- `{"hue_shift": 300}`: every hue rotated 300 deg; same lightness and chroma structure
- `{"hue_shift": 150}`: every hue rotated 150 deg; same lightness and chroma structure
- `{"hue_shift": 330}`: every hue rotated 330 deg; same lightness and chroma structure
- `{"hue_shift": 15}`: every hue rotated 15 deg; fine-tune step for this ramp
- `{"hue_shift": 345}`: every hue rotated -15 deg; fine-tune step for this ramp

