# 00_SCOPE.md — P00_RERUN 扫描范围定义

**ZLJ Wardrobe Collection · P00_INVENTORY_AND_ARCHITECTURE_AUDIT · CLEAN RE-RUN**

本轮为**全量重扫**，以**当前 MO2 实际状态**为唯一真值。
旧 P00 成果未被覆盖，仅作 `archive / reference only`，对比见 `P00_RERUN_VS_OLD.md`。

## 1. 真值来源

| 项 | 值 |
|---|---|
| MO2 instance | `E:\SkyrimAE\mo2` |
| MO2 profile | `Default` |
| modlist | `E:\SkyrimAE\mo2\profiles\Default\modlist.txt` |
| **modlist SHA256** | `5f03db69574ba916d358f12fff7ec6aff06b212e89e0c0dec982af3b8cc4ab4f` |
| modlist 行数 | 2,254 |
| 目标分隔符 | `09 特殊服装与NSFW 装备_separator` |
| 扫描时刻 (UTC) | 2026-09-30T03:53:02.019188+00:00 |

> **mtime 不作为范围判断依据。** 本机 MO2 每次退出会把 `modlist.txt` 原子替换一次，
> mtime 必然刷新而内容可能一字未改。范围只由 **SHA256 + 分隔符解析**决定。

## 2. MO2 优先级模型

1. `modlist.txt` 是左栏**倒序**：第 1 行 = 最底 = **最高覆盖优先级**。
2. 分隔符是**标题**，成员排在标题**下方**（左栏），即 modlist 行号**更小**。
3. 因此行号 L 的 mod 归属**行号比 L 大且最接近**的分隔符。
4. 分隔符 S 拥有区间 `(最近的更小行号分隔符 + 1) … (S - 1)`。
5. `+` 启用 / `-` 禁用 / `#` 注释。

## 3. 范围解析结果

| 项 | modlist 行 |
|---|---|
| 下界分隔符 `10 SexLab 与 OStim／OSA 框架_separator` | 882 |
| **范围首行** | **883** |
| **范围末行** | **938** |
| **分隔符本身 `09 特殊服装与NSFW 装备_separator`** | **939** |
| 上界分隔符 `07 正常服装、护甲_separator` | 1069 |

**扫描范围 = modlist 第 883–938 行，共 56 个 Mod。**

### 3.1 ⚠ 扫描期间 modlist 发生过变更（已在本次扫描中重新取基线）

| 项 | 上一次扫描 | 本次扫描 |
|---|---|---|
| modlist SHA256 | `fba5d3a373be7f5e…` | `5f03db69574ba916…` |
| modlist 行数 | 2250 | 2254 |
| 09 范围 | L879–934 | L883–938 |
| 新增成员 | 0 | — |
| 移出成员 | 0 | — |

**判定：member set unchanged - only the MO2 ordering coordinates shifted; asset findings remain valid, priority/leftpane_row were re-based**

本机 MO2 每次退出会原子替换 `modlist.txt`。本轮扫描期间 MO2 处于运行状态，
modlist 被改写了数次。**扫描主体（56 个 Mod 及其磁盘内容）没有变化**，
因此所有资产层面的结论依然成立；变化的是 MO2 排序坐标
（`priority` / `leftpane_row`），已按当前 modlist 重新取基线。

> **后续阶段开始前请先关闭 MO2**，否则排序坐标会再次漂移。

## 4. 范围汇总

| 指标 | 值 |
|---|---|
| Mod 总数 | **56** |
| 其中启用 | 56 |
| 其中禁用 | 0 |
| 文件夹缺失 | 0 |
| 合计文件数 | **3,708** |
| 合计体积 | **19,375,174,818 B = 18.04 GiB** |

## 5. 逐 Mod 明细（按 MO2 优先级由高到低）

| # | 行 | Mod | MiB | 文件 | 插件 | NIF | DDS | BS | OSP | 体型(名) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 883 | `Nyes Latex Pack AiO 1.3 (ReducedSize)` | 533.6 | 218 | 1 | 19 | 97 | 97 | 24 | `UNKNOWN` |
| 2 | 884 | `Haley Black Suit PBR` | 80.0 | 20 | 0 | 0 | 15 | 0 | 0 | `UNKNOWN` |
| 3 | 885 | `00 资源·H2135 披风物理补全 — H2135 Cloak SMP Physics` | 0.1 | 4 | 0 | 0 | 0 | 0 | 0 | `UNKNOWN` |
| 4 | 886 | `MiscMods Stilettos Zwei 与 Eins — AnkleCut V2 Tall…` | 4.8 | 7 | 0 | 0 | 0 | 6 | 2 | `CBBE_3BA` |
| 5 | 887 | `堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rewor…` | 72.0 | 29 | 0 | 11 | 12 | 6 | 0 | `CBBE_3BA` |
| 6 | 888 | `堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体…` | 66.1 | 44 | 1 | 11 | 10 | 16 | 4 | `CBBE_3BA` |
| 7 | 889 | `静默代码·乳胶重制 — Silent Code - Latex Rework — 【服装·装备】【…` | 487.4 | 73 | 0 | 0 | 64 | 0 | 0 | `UNKNOWN` |
| 8 | 890 | `静默代码 — SSE Silent Code — 【服装·装备】【身体·物理】【来源·本地】` | 1607.8 | 228 | 1 | 39 | 120 | 44 | 7 | `UNKNOWN` |
| 9 | 891 | `Riley Heels — 【服装·护甲】` | 69.0 | 9 | 1 | 0 | 0 | 3 | 1 | `UNKNOWN` |
| 10 | 892 | `MiscMods Stilettos Zwei 与 Eins — MiscMods Stilett…` | 11.6 | 7 | 0 | 0 | 0 | 6 | 2 | `UNKNOWN` |
| 11 | 893 | `FO4TOAEAngeli_Devices — 【来源·本地】` | 568.7 | 119 | 0 | 39 | 27 | 35 | 1 | `UNKNOWN` |
| 12 | 894 | `EvilFall — 【来源·本地】` | 1495.3 | 191 | 0 | 0 | 79 | 104 | 4 | `UNKNOWN` |
| 13 | 895 | `SEXY 靴子-oneboot - 9DM — SEXY BOOTS-oneboot - 9DM …` | 36.6 | 16 | 1 | 4 | 6 | 3 | 1 | `UNKNOWN` |
| 14 | 896 | `回归之夜高跟鞋 — SEXY BOOTS Returning Night Pumps — 【服装·…` | 113.9 | 52 | 1 | 10 | 19 | 21 | 7 | `UNKNOWN` |
| 15 | 897 | `Latex Lover Corset 增强版 — Latex Lover Corset Plus …` | 1194.7 | 226 | 2 | 59 | 23 | 110 | 1 | `UNKNOWN` |
| 16 | 898 | `DD - Sunset Mystic SET — 【来源·本地】` | 347.2 | 29 | 1 | 0 | 17 | 7 | 1 | `UNKNOWN` |
| 17 | 899 | `Nye的乳胶紧身衣和胸衣 2 — Nye's Latex Pack 2 — 【服装·护甲】【身体·…` | 163.6 | 27 | 1 | 0 | 0 | 22 | 7 | `UNKNOWN` |
| 18 | 900 | `Nye的乳胶紧身衣和胸衣 — Nye's Latex Pack — 【服装·护甲】【身体·物理】【…` | 109.4 | 31 | 1 | 0 | 3 | 23 | 7 | `UNKNOWN` |
| 19 | 901 | `Nye's Latex 服装 2 — Nye's Latex Outfit 2 — 【服装·护甲】…` | 103.1 | 25 | 1 | 0 | 1 | 20 | 6 | `UNKNOWN` |
| 20 | 902 | `SEXY 靴子-2B Wedding 靴子 [3BA] Edited — SEXY BOOTS-2…` | 8.6 | 4 | 0 | 0 | 0 | 3 | 1 | `CBBE_3BA` |
| 21 | 903 | `SEXY 靴子- Knee_Boots 3BA BodySlide — SEXY BOOTS- K…` | 120.8 | 25 | 1 | 4 | 10 | 9 | 1 | `CBBE_3BA` |
| 22 | 904 | `J3 Latex 3BA — 【服装·装备】【体型·CBBE+3BA】【来源·本地】` | 165.5 | 74 | 1 | 26 | 32 | 12 | 1 | `CBBE_3BA` |
| 23 | 905 | `紧身衣 — J3 Bodysuit 3BA — 【服装·装备】【身体·物理】【体型·CBBE+3BA】` | 102.0 | 25 | 1 | 2 | 10 | 11 | 1 | `CBBE_3BA` |
| 24 | 906 | `乳胶安杰莉 — SSEDDAngeli 3BA — 【服装·装备】【身体·物理】【体型·CBBE+…` | 884.7 | 162 | 1 | 58 | 52 | 47 | 3 | `CBBE_3BA` |
| 25 | 907 | `Brastia Catwoman TAS for 3BA — 【服装·装备】【体型·CBBE+3BA】` | 64.5 | 40 | 1 | 10 | 13 | 13 | 1 | `CBBE_3BA` |
| 26 | 908 | `Brastia Battle Princess Spandexer for 3BA — 【战斗·技…` | 543.3 | 179 | 1 | 61 | 35 | 79 | 1 | `CBBE_3BA` |
| 27 | 909 | `矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+…` | 138.1 | 65 | 1 | 40 | 10 | 9 | 1 | `CBBE_3BA` |
| 28 | 910 | `Vertigo Thigh High 靴子 - CBBE 3BA — Vertigo Thigh …` | 159.4 | 30 | 1 | 3 | 21 | 4 | 1 | `CBBE_3BA` |
| 29 | 911 | `Skimpy Assassin 服装 - BHUNP 3BBB - CBBE 3BBB — Ski…` | 200.6 | 42 | 1 | 5 | 26 | 7 | 1 | `BHUNP` |
| 30 | 912 | `SEXY 靴子-[Melodic] 4 Heels CBBE 3BA BodySlide SE —…` | 264.1 | 72 | 1 | 16 | 39 | 15 | 5 | `CBBE_3BA` |
| 31 | 913 | `Jennes Thigh 靴子- -BHUNP 3BBB- -CBBE 3BBB — Jennes…` | 29.1 | 15 | 1 | 3 | 6 | 3 | 1 | `BHUNP` |
| 32 | 914 | `SSE_VRC_SOURYO_fix — 【来源·本地】` | 644.6 | 95 | 1 | 22 | 46 | 23 | 1 | `UNKNOWN` |
| 33 | 915 | `SSE_VRC_Latex_Servant — 【来源·本地】` | 209.6 | 46 | 1 | 15 | 11 | 17 | 3 | `UNKNOWN` |
| 34 | 916 | `SSE_Latex_Nun — 【来源·本地】` | 243.8 | 67 | 1 | 24 | 22 | 15 | 3 | `UNKNOWN` |
| 35 | 917 | `SSE_Kakugo_LatexNun — 【来源·本地】` | 260.3 | 75 | 1 | 26 | 16 | 26 | 2 | `UNKNOWN` |
| 36 | 918 | `makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装…` | 121.2 | 44 | 1 | 14 | 17 | 10 | 2 | `UNKNOWN` |
| 37 | 919 | `makaron-COSPLAY - AE_Toxic_Cat — 【服装·装备】【来源·本地】` | 351.8 | 47 | 1 | 12 | 22 | 11 | 1 | `UNKNOWN` |
| 38 | 920 | `makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备…` | 158.3 | 41 | 1 | 11 | 16 | 11 | 1 | `UNKNOWN` |
| 39 | 921 | `makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装…` | 359.8 | 73 | 1 | 15 | 40 | 11 | 1 | `UNKNOWN` |
| 40 | 922 | `makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【…` | 124.5 | 39 | 1 | 8 | 21 | 7 | 1 | `UNKNOWN` |
| 41 | 923 | `makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】` | 166.5 | 80 | 1 | 19 | 45 | 13 | 2 | `UNKNOWN` |
| 42 | 924 | `makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】` | 199.6 | 62 | 1 | 21 | 19 | 14 | 2 | `UNKNOWN` |
| 43 | 925 | `AE_Vtaw_DarkNurse — 【来源·本地】` | 165.5 | 56 | 1 | 12 | 18 | 17 | 3 | `UNKNOWN` |
| 44 | 926 | `AE_VRC_Bunny_Nurse — 【来源·本地】` | 746.0 | 94 | 1 | 24 | 25 | 22 | 1 | `UNKNOWN` |
| 45 | 927 | `AE_HoodST — 【来源·本地】` | 373.9 | 52 | 1 | 12 | 19 | 13 | 1 | `UNKNOWN` |
| 46 | 928 | `[Zap] Gantz Suit — 【来源·本地】` | 1296.5 | 91 | 1 | 6 | 60 | 17 | 6 | `UNKNOWN` |
| 47 | 929 | `[TRX] LatexWhitch — 【来源·本地】` | 415.7 | 149 | 0 | 0 | 18 | 130 | 43 | `UNKNOWN` |
| 48 | 930 | `[Predator] Premium Laced LatexBodysuit — 【来源·本地】【…` | 242.5 | 25 | 1 | 6 | 11 | 5 | 1 | `UNKNOWN` |
| 49 | 931 | `[Predator] 靴子 Pack 02 CBBE 3BA — [Predator] Boots…` | 182.4 | 57 | 1 | 12 | 33 | 9 | 1 | `CBBE_3BA` |
| 50 | 932 | `[Predator] Gynax Suit + Colors XXX BHUNP SE — 【体型…` | 57.6 | 35 | 1 | 0 | 19 | 9 | 1 | `BHUNP` |
| 51 | 933 | `[Predator] Latex Acessories 3BA SE — 【服装·装备】【体型·C…` | 925.3 | 118 | 1 | 0 | 45 | 61 | 1 | `CBBE_3BA` |
| 52 | 934 | `[Predator] Naughty Slave Harness 3 CBBE 3BA AE — …` | 365.6 | 53 | 1 | 21 | 13 | 15 | 1 | `CBBE_3BA` |
| 53 | 935 | `[Predator] Penitent Warrior CBBE 3BA AE — 【体型·CBB…` | 214.6 | 22 | 1 | 3 | 9 | 3 | 1 | `CBBE_3BA` |
| 54 | 936 | `[Predator] Provocative Bikini Harness + Colors 3B…` | 30.2 | 22 | 1 | 0 | 16 | 2 | 1 | `CBBE_3BA` |
| 55 | 937 | `[Predator] Silicon Acessories CBBE 3BA AE — 【体型·C…` | 635.1 | 151 | 1 | 68 | 30 | 46 | 2 | `CBBE_3BA` |
| 56 | 938 | `[Predator] Slave Harness Chastity CBBE 3BA AE — 【…` | 241.5 | 26 | 1 | 3 | 17 | 3 | 1 | `CBBE_3BA` |

## 6. 只读声明

本轮对 `E:\SkyrimAE\mo2\`、`E:\SkyrimAE\Data\`、modlist、BodySlide、
PGPatcher **零写入**。`p00r_common.assert_write_path()` 在运行时强制所有写操作
只能落在 `tools/P00_RERUN/`、`data/P00_RERUN/`、`reports/P00_RERUN/` 之内，
越界直接 `SystemExit`。

---

**P00_RERUN · STAGE A/B/C/D/E COMPLETE**
