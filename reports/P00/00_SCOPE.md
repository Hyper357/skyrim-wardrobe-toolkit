# 00_SCOPE.md — P00 扫描范围定义

**latex Wardrobe Collection · P00_INVENTORY_AND_ARCHITECTURE_AUDIT**

本文件只做一件事：把「扫描哪些东西」钉死，并给出可复核的证据。
本阶段**全程只读**，没有修改任何 Mod / 插件 / NIF / DDS / 配置。

---

## 1. 运行环境与真值来源

| 项 | 值 |
|---|---|
| MO2 instance | `E:\SkyrimAE\mo2` |
| MO2 profile | `Default` |
| modlist | `E:\SkyrimAE\mo2\profiles\Default\modlist.txt` |
| modlist SHA256 | `fba5d3a373be7f5e7010a2687d8bfc5abd4a568ab0f39edc6a5a25905df230e1` |
| modlist 行数 | 2250 |
| modlist mtime | 2026-09-29T18:31:36.911578 |
| mods 根目录 | `E:\SkyrimAE\mo2\mods` |
| 游戏根目录 | `E:\SkyrimAE`（Data 在 `E:\SkyrimAE\Data`） |
| 扫描时刻 (UTC) | 2026-09-29T15:44:04.422144+00:00 |
| 脚本 | `tools/p00_common.py`, `tools/p00_s1_scope.py` |

> modlist.txt 在本次扫描期间被 MO2 改写过（18:29 与 18:31 两次落盘）。
> 上表的 SHA256 是本报告所依据的那一份快照，可随时复核。

## 2. MO2 优先级模型（本项目的事实，不是推测）

1. `modlist.txt` 是左栏**倒序**：第 1 行 = 左栏最底一行 = **最高覆盖优先级**。
   交叉验证：`-99 工具生成输出（务必置底）` 分隔符在第 36 行，`输出·BodySlide Output` 在第 33 行 —— 33 在 36 之下 = 左栏里排在 36 之下，符合手册「99 生成输出必须真正处于最末端」。
2. 分隔符是**标题**，成员排在标题**下方**。
3. 因此：一条 mod 属于**行号比它大的最近那个分隔符**。
4. `+` = 启用；`-` = 禁用（不进 VFS）；`#` = 注释。

## 3. 范围解析结果

目标分隔符：`09 特殊服装与NSFW 装备_separator`

| 项 | modlist 行 | 左栏行 |
|---|---|---|
| 下界分隔符 `10 SexLab 与 OStim／OSA 框架_separator`（左栏里排在本块**下方**） | 878 | 1373 |
| **范围首行** | **879** | 1372 |
| **范围末行** | **934** | 1317 |
| **分隔符本身 `09 特殊服装与NSFW 装备_separator`**（本块在左栏里排在它**下方**） | **935** | **1316** |
| 上界分隔符 `07 正常服装、护甲_separator` | 1065 | 1186 |

**扫描范围 = modlist 第 879–934 行，共 56 个 Mod（左栏第 1372–1317 行）。**

### 3.1 与任务书示例清单的交叉核对

任务书列出的示例名称中 **31 / 31** 命中本范围：

| 示例关键词 | 命中 | modlist 行 |
|---|---|---|
| `Predator` | ✓ | 926, 927, 928, 929, 930, 931, 932, 933, 934 |
| `TRX` | ✓ | 925 |
| `Zap` | ✓ | 924 |
| `AE_HoodST` | ✓ | 923 |
| `AE_VRC_Bunny_Nurse` | ✓ | 922 |
| `AE_Vtaw_DarkNurse` | ✓ | 921 |
| `AE_Latex_Kitty` | ✓ | 920 |
| `AE_Once_Medic` | ✓ | 919 |
| `AE_Stellablade_Tachy` | ✓ | 918 |
| `AE_TFD_Haley_Black_Suit` | ✓ | 917 |
| `AE_TFD_Valby_Nano` | ✓ | 916 |
| `AE_Toxic_Cat` | ✓ | 915 |
| `AE_Wuthering_Waves_Lupa` | ✓ | 914 |
| `SSE_Kakugo_LatexNun` | ✓ | 913 |
| `SSE_Latex_Nun` | ✓ | 912 |
| `SSE_VRC_Latex_Servant` | ✓ | 911 |
| `SSE_VRC_SOURYO` | ✓ | 910 |
| `SpearHead` | ✓ | 905 |
| `Brastia` | ✓ | 903, 904 |
| `Angeli` | ✓ | 889, 902 |
| `J3 Bodysuit` | ✓ | 901 |
| `J3 Latex` | ✓ | 900 |
| `Nye` | ✓ | 879, 895, 896, 897 |
| `Latex Lover` | ✓ | 893 |
| `EvilFall` | ✓ | 890 |
| `FO4TOAEAngeli` | ✓ | 889 |
| `Silent Code` | ✓ | 885, 886 |
| `Corrupted` | ✓ | 883, 884 |
| `H2135` | ✓ | 881 |
| `Haley` | ✓ | 880, 917 |
| `Nyes Latex` | ✓ | 879 |

**全部命中，无遗漏。** 任务书的范围定义与 MO2 实际内容一致。

## 4. 范围汇总

| 指标 | 值 |
|---|---|
| Mod 总数 | **56** |
| 其中启用 | 56 |
| 其中禁用 | 0 |
| 文件夹缺失 | 0 |
| 合计文件数 | 3,708 |
| 合计体积 | 19,375,174,818 B = 18.04 GiB |
| 插件文件总数 | 47 |
| 其中无插件的 Mod | 10 |
| NIF | 1,316 |
| DDS | 1,355 |
| BodySlide 文件 | 1,055 |

### 4.1 体型体系分布

`body_type_guess` 由三条证据链依次得出，来源记录在 `body_type_source` 列：
`name_tag`（文件夹名的结构化 `【体型·…】` 标签，最可信）→ `name_scan`（文件夹名其余部分）→ `bodyslide_assets`（BodySlide 工程 / ShapeData 名）。`【体型·多体型】` 被视为**无效证据**，会继续向下回退。全部无法判定才记 `unknown`。

| 判定 | Mod 数 |
|---|---|
| `unknown` | 29 |
| `CBBE 3BA` | 20 |
| `3BA` | 4 |
| `BHUNP` | 3 |

| 体型族 | Mod 数 | 说明 |
|---|---|---|
| `UNKNOWN` | 29 | 无法判定 |
| `CBBE_3BA` | 24 | CBBE 或 3BA 系 |
| `BHUNP_ONLY` | 3 | 纯 BHUNP，**无法直接并入统一 3BA 体系** |

- **CBBE/3BA 与 BHUNP 混杂：0 个 Mod**
- 纯 BHUNP：3 个 Mod
- 体型完全无法判定：29 个 Mod —— `Nyes Latex Pack AiO 1.3 (ReducedSize)`, `Haley Black Suit PBR`, `00 资源·H2135 披风物理补全 — H2135 Cloak SMP Physics`, `静默代码·乳胶重制 — Silent Code - Latex Rework — 【服装·装备】【身体·物理】【来源·本地】`, `静默代码 — SSE Silent Code — 【服装·装备】【身体·物理】【来源·本地】`, `FO4TOAEAngeli_Devices — 【来源·本地】`, `EvilFall — 【来源·本地】`, `SEXY 靴子-oneboot - 9DM — SEXY BOOTS-oneboot - 9DM — 【服装·护甲】【来源·本地】`…
- 体型判定只能靠 BodySlide 工程名回推（置信度较低）：5 个 Mod

> **不得默认所有项目都能共用同一套 BodySlide。** 上面 `BHUNP_ONLY` 与
> `MIXED_3BA_BHUNP` 两行就是必须转换的部分；具体清单见阶段 08。

### 4.2 脚本 / 分发 / 物理层现状

| 层 | 本范围计数 |
|---|---|
| SPID 分发 | 0 |
| KID 关键词分发 | 0 |
| BOS 物体替换 | 0 |
| OAR 动画条件 | 0 |
| DAR 动画条件 | 0 |
| Papyrus `.psc` | 0 |
| SKSE 配置 JSON | 0 |
| HDT-SMP 骨架 `.hdt` | 0 |
| HDT-SMP 物理 XML | 4 |
| CBPC 布料 `.hkx` | 0 |
| 其它 `.hkx` | 0 |
| PGPatcher 规则 JSON | 4 |
| `textures\pbr\` 目录 | 1 |

本范围内 `.ini` 共 68 个、`.xml` 共 59 个（其中 SliderSets / SliderGroups / SliderPresets 的 BodySlide XML 同时计入 `n_xml` 与 `bs_*` 两组列，属有意重复，不是错误）。

**这一条对最终架构影响很大：** 本分隔符是**纯资产层**。它没有脚本、没有 SPID/KID 分发、没有 OAR/DAR、几乎没有物理。
—— 也就是说「SPID / Outfit 自然分发到 Skyrim 世界」这一目标所需的整套分发层，目前**不在本范围内**，需要么在 P01 单独立项，要么把范围扩到 `07 正常服装、护甲`（那里有 30+ 个 SPID 补丁 Mod）。

### 4.3 范围内全部 Mod 明细

按 `mo2_priority` 升序（= 覆盖优先级由高到低，与左栏从上到下一致）。

| # | modlist 行 | Mod | MiB | 文件 | 插件 | NIF | DDS | BS | 体型 | 来源 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 879 | `Nyes Latex Pack AiO 1.3 (ReducedSize)` | 533.6 | 218 | 1esp | 53 | 97 | 68 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 2 | 880 | `Haley Black Suit PBR` | 80.0 | 20 | — | 0 | 15 | 0 | `unknown` | none | BODY_TYPE_UNKNOWN;NO_PLUGIN;NO_BODYSLIDE;NO_NIF |
| 3 | 881 | `00 资源·H2135 披风物理补全 — H2135 Cloak SMP Physics` | 0.1 | 4 | — | 0 | 0 | 0 | `unknown` | none | BODY_TYPE_UNKNOWN;NO_PLUGIN;NO_BODYSLIDE;NO_NIF |
| 4 | 882 | `MiscMods Stilettos Zwei 与 Eins — AnkleCut V2 Tall 3BA【更...` | 4.8 | 7 | — | 2 | 0 | 4 | `3BA` | bodyslide_assets | body_type_from_assets;NO_PLUGIN |
| 5 | 883 | `堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服...` | 72.0 | 29 | — | 17 | 12 | 6 | `CBBE 3BA` | name_tag | NO_PLUGIN |
| 6 | 884 | `堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE...` | 66.1 | 44 | 1esp | 17 | 10 | 12 | `CBBE 3BA` | name_tag |  |
| 7 | 885 | `静默代码·乳胶重制 — Silent Code - Latex Rework — 【服装·装备】【身体·物理】...` | 487.4 | 73 | — | 0 | 64 | 0 | `unknown` | none | BODY_TYPE_UNKNOWN;NO_PLUGIN;NO_BODYSLIDE;NO_NIF |
| 8 | 886 | `静默代码 — SSE Silent Code — 【服装·装备】【身体·物理】【来源·本地】` | 1607.8 | 228 | 1esp | 57 | 120 | 36 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 9 | 887 | `Riley Heels — 【服装·护甲】` | 69.0 | 9 | 1esp | 1 | 0 | 2 | `CBBE 3BA` | bodyslide_assets | body_type_from_assets |
| 10 | 888 | `MiscMods Stilettos Zwei 与 Eins — MiscMods Stilettos Zwe...` | 11.6 | 7 | — | 2 | 0 | 4 | `3BA` | bodyslide_assets | body_type_from_assets;NO_PLUGIN |
| 11 | 889 | `FO4TOAEAngeli_Devices — 【来源·本地】` | 568.7 | 119 | — | 56 | 27 | 34 | `unknown` | none | BODY_TYPE_UNKNOWN;NO_PLUGIN |
| 12 | 890 | `EvilFall — 【来源·本地】` | 1495.3 | 191 | — | 50 | 79 | 100 | `unknown` | none | BODY_TYPE_UNKNOWN;NO_PLUGIN |
| 13 | 891 | `SEXY 靴子-oneboot - 9DM — SEXY BOOTS-oneboot - 9DM — 【服装·...` | 36.6 | 16 | 1esp | 5 | 6 | 2 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 14 | 892 | `回归之夜高跟鞋 — SEXY BOOTS Returning Night Pumps — 【服装·护甲】【来源...` | 113.9 | 52 | 1esp | 17 | 19 | 14 | `3BA` | bodyslide_assets | body_type_from_assets |
| 15 | 893 | `Latex Lover Corset 增强版 — Latex Lover Corset Plus — 【服装·...` | 1194.7 | 226 | 2esp | 117 | 23 | 109 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 16 | 894 | `DD - Sunset Mystic SET — 【来源·本地】` | 347.1 | 29 | 1esp | 3 | 17 | 6 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 17 | 895 | `Nye的乳胶紧身衣和胸衣 2 — Nye's Latex Pack 2 — 【服装·护甲】【身体·物理】【系列...` | 163.6 | 27 | 1esp | 7 | 0 | 14 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 18 | 896 | `Nye的乳胶紧身衣和胸衣 — Nye's Latex Pack — 【服装·护甲】【身体·物理】【系列·Nye】` | 109.4 | 31 | 1esp | 7 | 3 | 14 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 19 | 897 | `Nye's Latex 服装 2 — Nye's Latex Outfit 2 — 【服装·护甲】【系列·Nye】` | 103.1 | 25 | 1esl | 6 | 1 | 12 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 20 | 898 | `SEXY 靴子-2B Wedding 靴子 [3BA] Edited — SEXY BOOTS-2B Wedd...` | 8.6 | 4 | — | 1 | 0 | 2 | `CBBE 3BA` | name_tag | NO_PLUGIN |
| 21 | 899 | `SEXY 靴子- Knee_Boots 3BA BodySlide — SEXY BOOTS- Knee_Bo...` | 120.8 | 25 | 1esp | 8 | 10 | 8 | `CBBE 3BA` | name_tag |  |
| 22 | 900 | `J3 Latex 3BA — 【服装·装备】【体型·CBBE+3BA】【来源·本地】` | 165.5 | 74 | 1esp | 31 | 32 | 10 | `CBBE 3BA` | name_tag |  |
| 23 | 901 | `紧身衣 — J3 Bodysuit 3BA — 【服装·装备】【身体·物理】【体型·CBBE+3BA】` | 102.0 | 25 | 1esp | 7 | 10 | 10 | `CBBE 3BA` | name_tag |  |
| 24 | 902 | `乳胶安杰莉 — SSEDDAngeli 3BA — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来...` | 884.7 | 162 | 1esp | 80 | 52 | 44 | `CBBE 3BA` | name_tag |  |
| 25 | 903 | `Brastia Catwoman TAS for 3BA — 【服装·装备】【体型·CBBE+3BA】` | 64.5 | 40 | 1esp | 17 | 13 | 12 | `CBBE 3BA` | name_tag |  |
| 26 | 904 | `Brastia Battle Princess Spandexer for 3BA — 【战斗·技能】【体型·...` | 543.3 | 179 | 1esp | 103 | 35 | 78 | `CBBE 3BA` | name_tag |  |
| 27 | 905 | `矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来...` | 138.1 | 65 | 1esp | 44 | 10 | 8 | `CBBE 3BA` | name_tag |  |
| 28 | 906 | `Vertigo Thigh High 靴子 - CBBE 3BA — Vertigo Thigh High B...` | 159.4 | 30 | 1esp | 4 | 21 | 2 | `CBBE 3BA` | name_tag |  |
| 29 | 907 | `Skimpy Assassin 服装 - BHUNP 3BBB - CBBE 3BBB — Skimpy As...` | 200.6 | 42 | 1esp | 8 | 26 | 6 | `BHUNP` | name_scan |  |
| 30 | 908 | `SEXY 靴子-[Melodic] 4 Heels CBBE 3BA BodySlide SE — SEXY ...` | 264.1 | 72 | 1esp | 21 | 39 | 10 | `CBBE 3BA` | name_scan(notag) |  |
| 31 | 909 | `Jennes Thigh 靴子- -BHUNP 3BBB- -CBBE 3BBB — Jennes Thigh...` | 29.1 | 15 | 1esp | 4 | 6 | 2 | `BHUNP` | name_scan |  |
| 32 | 910 | `SSE_VRC_SOURYO_fix — 【来源·本地】` | 644.6 | 95 | 1esp | 33 | 46 | 22 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 33 | 911 | `SSE_VRC_Latex_Servant — 【来源·本地】` | 209.6 | 46 | 1esp | 22 | 11 | 14 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 34 | 912 | `SSE_Latex_Nun — 【来源·本地】` | 243.8 | 67 | 1esp | 30 | 22 | 12 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 35 | 913 | `SSE_Kakugo_LatexNun — 【来源·本地】` | 260.3 | 75 | 1esp | 38 | 16 | 24 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 36 | 914 | `makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】` | 121.2 | 44 | 1esp | 18 | 17 | 8 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 37 | 915 | `makaron-COSPLAY - AE_Toxic_Cat — 【服装·装备】【来源·本地】` | 351.8 | 47 | 1esp | 17 | 22 | 10 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 38 | 916 | `makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】` | 158.3 | 41 | 1esp | 16 | 16 | 10 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 39 | 917 | `makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】` | 359.8 | 73 | 1esp | 20 | 40 | 10 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 40 | 918 | `makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】` | 124.5 | 39 | 1esp | 11 | 21 | 6 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 41 | 919 | `makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】` | 166.5 | 80 | 1esp | 25 | 45 | 11 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 42 | 920 | `makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】` | 199.6 | 62 | 1esp | 27 | 19 | 12 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 43 | 921 | `AE_Vtaw_DarkNurse — 【来源·本地】` | 165.5 | 56 | 1esp | 19 | 18 | 14 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 44 | 922 | `AE_VRC_Bunny_Nurse — 【来源·本地】` | 746.0 | 94 | 1esp | 36 | 25 | 21 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 45 | 923 | `AE_HoodST — 【来源·本地】` | 373.9 | 52 | 1esp | 18 | 19 | 12 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 46 | 924 | `[Zap] Gantz Suit — 【来源·本地】` | 1296.5 | 91 | 1esp | 12 | 60 | 11 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 47 | 925 | `[TRX] LatexWhitch — 【来源·本地】` | 415.7 | 149 | — | 43 | 18 | 86 | `3BA` | bodyslide_assets | body_type_from_assets;NO_PLUGIN |
| 48 | 926 | `[Predator] Premium Laced LatexBodysuit — 【来源·本地】【系列·Pre...` | 242.5 | 25 | 1esp | 8 | 11 | 4 | `unknown` | none | BODY_TYPE_UNKNOWN |
| 49 | 927 | `[Predator] 靴子 Pack 02 CBBE 3BA — [Predator] Boots Pack ...` | 182.4 | 57 | 1esp | 16 | 33 | 8 | `CBBE 3BA` | name_tag |  |
| 50 | 928 | `[Predator] Gynax Suit + Colors XXX BHUNP SE — 【体型·BHUNP...` | 57.6 | 35 | 1esp | 5 | 19 | 8 | `BHUNP` | name_tag |  |
| 51 | 929 | `[Predator] Latex Acessories 3BA SE — 【服装·装备】【体型·CBBE+3B...` | 925.3 | 118 | 1esp | 30 | 45 | 60 | `CBBE 3BA` | name_tag |  |
| 52 | 930 | `[Predator] Naughty Slave Harness 3 CBBE 3BA AE — 【体型·CB...` | 365.6 | 53 | 1esp | 28 | 13 | 14 | `CBBE 3BA` | name_tag |  |
| 53 | 931 | `[Predator] Penitent Warrior CBBE 3BA AE — 【体型·CBBE+3BA】...` | 214.6 | 22 | 1esp | 4 | 9 | 2 | `CBBE 3BA` | name_tag |  |
| 54 | 932 | `[Predator] Provocative Bikini Harness + Colors 3BA SE —...` | 30.2 | 22 | 1esp | 1 | 16 | 1 | `CBBE 3BA` | name_tag |  |
| 55 | 933 | `[Predator] Silicon Acessories CBBE 3BA AE — 【体型·CBBE+3B...` | 635.1 | 151 | 1esp | 90 | 30 | 44 | `CBBE 3BA` | name_tag |  |
| 56 | 934 | `[Predator] Slave Harness Chastity CBBE 3BA AE — 【体型·CBB...` | 241.5 | 26 | 1esp | 4 | 17 | 2 | `CBBE 3BA` | name_tag |  |


## 5. 范围边界声明

**在范围内**（本轮唯一授权扫描的对象）：
`E:\SkyrimAE\mo2\mods\<本节表格 01_MOD_INVENTORY.csv 所列 56 个 Mod>`

**明确不在范围内**：

- 其余所有 MO2 分隔符（`00`–`08`、`10`–`17`、`98`、`99`）。
- 紧邻上方的 `07 正常服装、护甲` 分隔符下的 115 个护甲/长袍 Mod。
- `Data\` 下的游戏本体文件与 BSA。

范围外资产**只允许被读取用于解析引用关系**（例如某个范围内 Mod 的 NIF 指向了范围外的 DDS，这一事实必须被记录），**不得成为报告主体**。

## 6. 本阶段的写操作清单

本次运行只写入了本工程自己的目录：

```
E:\SkyrimAE\opencode工作目录\5-latex-wardrobe-collection\
├─ tools\p00_common.py, p00_s1_scope.py   # 扫描脚本
├─ data\p00_scope.json                      # 中间证据
└─ reports\P00\00_SCOPE.md, 01_MOD_INVENTORY.csv
```

对 `mo2\mods\`、`Data\`、modlist、BodySlide、PGPatcher **零写入**。

---

*下一步（待人工审核后）：02_PLUGIN_RECORDS.csv / 03_ARMOR_ARMA_MAP.csv / …*

**P00 STAGE 1 COMPLETE — STOPPED FOR REVIEW**
