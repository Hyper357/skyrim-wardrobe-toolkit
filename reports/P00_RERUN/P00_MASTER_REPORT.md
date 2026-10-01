# P00_MASTER_REPORT.md — ZLJ Wardrobe Collection

**P00_INVENTORY_AND_ARCHITECTURE_AUDIT · CLEAN RE-RUN**

- 真值来源：当前 MO2 profile `Default`，modlist SHA256 `5f03db69574ba916d358f12fff7ec6aff06b212e89e0c0dec982af3b8cc4ab4f`
- 范围：`09 特殊服装与NSFW 装备_separator`，modlist 第 883–938 行
- 生成时刻 (UTC)：2026-09-30T03:53:02.019188+00:00
- 阶段：P00 全部完成，**未进入 P01**

> ### ⚠ 扫描期间 modlist 变更过，已重新取基线
>
> - 上一次扫描 `fba5d3a373be7f5e…` → 本次 `5f03db69574ba916…`
> - 09 范围 L879–934 → L883–938（成员 2250 → 2254 行）
> - 成员集合：新增 0 / 移出 0
> - **member set unchanged - only the MO2 ordering coordinates shifted; asset findings remain valid, priority/leftpane_row were re-based**
>
> 本轮扫描期间 MO2 处于运行状态并改写了 modlist。资产层面的全部结论
> 依然成立；`priority` / `leftpane_row` 已按当前 modlist 重新取基线。
> **进入 P01 前请先关闭 MO2。**

---

## ⚠ SUPERSEDE NOTICE — 上一版 P00_RERUN 已被作废（schema fix）

**在本次 schema fix 之前生成的整套 P00_RERUN 结果已整体作废，不再作为真值。**
触发作废的两个解析器缺陷：

1. **ARMO→ArmorAddon 关系搞反。** 旧解析把 `ARMO.RNAM` 当成 ArmorAddon 链接，并把 `ARMO.MOD2..MOD5` 当成 worn mesh。实测（`Skyrim.esm` 全库 2,762 条 ARMO）：`RNAM` 100% 指向 **RACE**；ArmorAddon 链接是 **`ARMO.MODL`**，而且是 **1:N**（vanilla 里 702/2762 条 ARMO 有多条 MODL）。
2. **对 XML `.osp` 调用了二进制 OSD 解析器。** `ShapeData/*.osd` 才是二进制（`OSD\0` magic），`SliderSets/*.osp` 是 XML（SliderSet 工程文件）。旧解析器对 `.osp` 静默返回空，于是 07 的 `shapedata_files` / `sliderset_files` / `ui_outfit_names` 全是假空值。

| 被作废的输出 | 波及层级 | 原因 |
|---|---|---|
| `03_ARMOR_ARMA_MAP.csv` | 直接作废 | 旧表把 `ARMO.RNAM` 当成 ArmorAddon 链接，且单值化。RNAM 实际是 **RACE**；ArmorAddon 链接是 `ARMO.MODL`，而且是 **1:N**。worn mesh 在 **ARMA** 上，ARMO 自己的 MOD2..MOD5 是 world / inventory 模型。 |
| `04_PARTS_CATALOG.csv` | 直接作废 | 旧的 `ARMA_formid` / `ARMA_edid` 单值列来自错误的 RNAM 读法，整列语义错误。现改为 `ARMA_formids` / `n_arma_refs` / `ARMA_edids` / `ARMA_resolved` / `ARMA_routes` 的 1:N 形式。 |
| `05_SLOT_PARTITION_MAP.csv` | 直接作废 | 由 04 的 ARMA→NIF 可穿戴链路派生；上游链路错误，下游全部连带作废。 |
| `06_DIY_COMPATIBILITY_MATRIX.csv` | 直接作废 | 由 04 的 part 分类 + 体型判定 + NIF 分区派生；上游链路错误，下游全部连带作废。 |
| `07_BODYSLIDE_PROJECTS.csv` | 直接作废 | 旧表用二进制 OSD 解析器去读 XML `.osp`，解析静默返回空，`shapedata_files` / `sliderset_files` / `ui_outfit_names` 全是假空；`output_path` 还被硬编码成 `meshes\clothing`。现按 `OSP_PATH` 逐 `.osp` 出行，输出路径一律来自 OSP 本身。 |
| `11_MATERIAL_CLASSIFICATION.csv` | 派生作废 | 材质判定消费 04 的 NIF 链路，链路错误导致 NIF 集合错误。 |
| `14_CROSS_MOD_DEPENDENCIES.csv` | 派生作废 | 旧表按 `ARMO.RNAM` 生成 ARMO→ARMA 跨插件依赖，方向与目标都错。 |
| `18_PLUGIN_MERGE_RISK.csv` | 派生作废（merge analysis） | 合并风险统计的 ARMO/ARMA 记录计数来自受影响的解析层。 |
| `15_REWORK_RELATIONSHIPS.csv` | 派生作废（logical outfit analysis） | n_parts 与 BodySlide 计数来自 04 / 07，两者都已作废。 |
| `P00_MASTER_REPORT.md` | 本身作废（已由本次重生成取代） | 本报告的 25 项必答中，第 4/5/11/12/21 项直接建立在上述作废表之上。 |

> 本表中的**每一项都已由本次重跑重新生成**（`04/05/06` 由 `p00r_parts.py` 产出）。如果某个文件不存在或仍是旧内容，以本报告里的「upstream stage unavailable」标记为准，**不要**把旧文件当结论用。

## ARMA 关系校正（schema fix 后的正确说法）

| 子记录 | 挂在谁身上 | 正确含义 |
|---|---|---|
| `RNAM` | **ARMO** | **RACE** 引用 —— 该 armour 供哪个 race 使用。**不是** ArmorAddon 链接。|
| `MODL` | **ARMO** | **1:N** 的 ArmorAddon 引用。0 到多条，解到 ARMA 的那几条才是真链接。|
| `MOD2..MOD5` | **ARMA** | **worn mesh**（角色身上真正渲染的网格）。|
| `MOD2..MOD5` | **ARMO** | **world / inventory 模型**（地面掉落物、物品栏图标），**不是** worn mesh。|
| `BOD2` | ARMO 与 ARMA 各一份 | 8 字节 uint32 slot 位掩码。|

**推论：任何按 ARMO 自己的 MOD2..MOD5 去查贴图 / 材质 / 分区的旧结论都不成立。**
worn mesh 必须从 ARMO → MODL → ARMA → ARMA.MOD2..MOD5 走。`03_ARMOR_ARMA_MAP.csv` 现在是**每个 (ARMO, ArmorAddon) 一行**，并且允许某个 ARMO **一行都没有**（见 4b）。

## 解析器校准门 `P00_RERUN/PARSER_CALIBRATION.md`

- 引用：`reports/P00_RERUN/PARSER_CALIBRATION.md`
- 门状态：**machine verdict: **PASS** -- **56/56 PASS, 0 FAIL****
- 说明：reports/P00_RERUN/PARSER_CALIBRATION.md present (87,080 B)

---

## 25 项必答

### 1. 当前 09 范围实际 Mod 数量

**56** 个（启用 56 / 禁用 0 / 文件夹缺失 0）

### 2. LOGICAL OUTFIT 数量

**56** 个（按 mod 名的系列标记聚合，见 `15_REWORK_RELATIONSHIPS.csv`）

### 3. Patch / Rework 数量

| 角色 | Mod 数 |
|---|---|
| `BASE_MOD` | 47 |
| `PATCH_MOD` | 7 |
| `REWORK_MOD` | 2 |

合计 patch/rework 类（不含 BASE_MOD）= **9**

### 4. 可利用 part 总数

**1448** 个 PART_ID（ARMO 级可穿戴单元）

### 4b. 到达 ArmorAddon 的 armour record 数量

| 指标 | 数量 |
|---|---|
| ARMO 记录总数 | 1448 |
| **至少解析到 1 条 ArmorAddon 的 ARMO** | **1342** |
| **一条 ArmorAddon 都没到的 ARMO** | **106** |
| 覆盖率 | 92.7% |
| ARMA 记录总数（范围内） | 1321 |
| ARMO.MODL 引用总数 | 1855 |
| MODL 中解析到 ARMA 的 | 1787 |
| MODL 未解析 / 有歧义 | 68 |
| ArmorAddon 链接总数（1:N 展开后） | 1787 |

MODL 解析路线分布（`resolution_route`，逐条见 `03_ARMOR_ARMA_MAP.csv`）：

| 路线 | 数量 | 含义 |
|---|---|---|
| `self` | 1344 | 引用所在插件自身的记录（TES4 master byte == len(MAST)） |
| `master[0]` | 443 | UNKNOWN |
| `unresolved` | 66 | 全库范围内找不到任何持有者 |
| `ambiguous(92)` | 1 | UNKNOWN |
| `ambiguous(60)` | 1 | UNKNOWN |

`ambiguous` / `unresolved` 的那部分**没有被强行配对**。在多插件共用 formid 的情况下按字母序取一个，会制造出指向无关 ArmorAddon 的假链接（本轮实测到过：一只 Silent_Code 手套被配到一个不相关的 HoodST body addon）。宁可留 UNKNOWN。

RNAM → RACE：1442 / 1448 条 ARMO 的 `race_is` 确认为 `RACE`；其余 6 条 `race_resolved` 为空，打印 `UNKNOWN`。

### 5. 各部件类别数量

| 类别 | 数量 |
|---|---|
| `OTHER` | 370 |
| `BODYSUIT` | 260 |
| `CORSET` | 241 |
| `GLOVES` | 106 |
| `BODY` | 97 |
| `MASK` | 69 |
| `BOOTS` | 68 |
| `HEELS` | 60 |
| `SKIRT` | 43 |
| `HOOD` | 41 |
| `TAIL` | 29 |
| `HARNESS` | 29 |
| `STOCKINGS` | 10 |
| `COAT` | 9 |
| `CAPE` | 7 |
| `HAT` | 4 |
| `CHOKER` | 3 |
| `BELT` | 2 |

### 5b. ARMO → ArmorAddon 链路实测（来自 `04_PARTS_CATALOG.csv`）

旧版 04 的 `ARMA_formid` / `ARMA_edid` 单值列已删除。新列是 1:N 形式：

| `n_arma_refs` 分布 | part 数 |
|---|---|
| 1 | 1191 |
| 4 | 143 |
| 0 | 106 |
| 3 | 8 |

| `ARMA_resolved` 分布 | part 数 | 含义 |
|---|---|---|
| `1/1` | 1191 | 解析出的 ArmorAddon / 该 part 的 MODL 数 |
| `1/4` | 143 | 解析出的 ArmorAddon / 该 part 的 MODL 数 |
| `0/0` | 106 | 解析出的 ArmorAddon / 该 part 的 MODL 数 |
| `1/3` | 4 | 解析出的 ArmorAddon / 该 part 的 MODL 数 |
| `3/3` | 2 | 解析出的 ArmorAddon / 该 part 的 MODL 数 |
| `0/3` | 2 | 解析出的 ArmorAddon / 该 part 的 MODL 数 |

| `slot_source` | part 数 |
|---|---|
| `ARMA.BOD2 (authoritative addon slots)` | 1340 |
| `ARMO.BOD2` | 108 |

| `model_source` | part 数 |
|---|---|
| `ARMA.MOD2..MOD5 via ARMO.MODL` | 1340 |
| `none:ARMO.MODL resolved to no in-scope ARMA` | 108 |

| `game_nif_resolved` | part 数 | 含义 |
|---|---|---|
| `UNKNOWN` | 1448 | 上游阶段未提供该字段 |

- `ARMA_routes` 分布：`self`=1340, `master[0]`=149
- `race_is` 分布：`RACE`=1448
- `nif_resolved`（= ARMA wearable + BodySlide base NIF）：`yes`=637, `no`=621, `partial`=190
- BodySlide base NIF 来源：349 个 part，共 **357** 条路径 | pending build：928 个 part，共 **1574** 条
- ARMO world model 路径总数：**1612** 条（`world_model_count` 均值 1.11）

### 6. BodySlide project 数量

BodySlide 项目必须按 **MO2 有效视图**计数，不能按磁盘行数计数：同一个虚拟 `.osp` 路径可能由多个 Mod 提供，只有优先级最高的那一份真正进入 VFS。

| 计数 | 值 | 含义 |
|---|---|---|
| `PHYSICAL_PROJECT_ROWS` | **176** | 磁盘上 09 范围内的 `.osp` 行数（含被覆盖的）|
| `EFFECTIVE_VFS_PROJECTS` | **156** | 真正进入 VFS、**下游 PART/DIY 只使用这些** |
| 被覆盖（shadowed） | **20** | 其中内容真正冲突 4 条 |

> 20 个虚拟路径由多个 Mod 提供，全部由 L883 `Nye Latex Pack AiO 1.3 (ReducedSize)` 取得覆盖权（modlist 行号最小 = 优先级最高）。其中 **4 条是真实内容冲突**（sha256 不同），16 条字节相同。被覆盖的项目不得再声明任何 PART。

XML 解析：SliderSet 176 （.osp 176 / .xml 0） | ShapeData 1055（.nif 542 / .osd 513） | SliderGroup 9 | SliderPreset 5

`.osp` XML 解析错误：**0** 条；`.osd` 二进制读取错误：**0** 条。

输出路径分布（全部来自 OSP 自身，**无任何硬编码**）：82 个不同前缀。

### 7. CBBE / CBBE_3BA / BHUNP / OTHER / UNKNOWN 数量

> 口径修正：`classify_body` 现在把**只含 CBBE** 的 token 集合判为 `CBBE`（以前被并进 `OTHER`）。因此下面这张表**必须**包含 `CBBE` 一行；任何假定 CBBE 不会出现的聚合都是错的。

| 判定 | Mod 数 | BodySlide project 数 |
|---|---|---|
| `CBBE_3BA` | 20 | 60 |
| `CBBE` | 0 | 1 |
| `BHUNP` | 3 | 1 |
| `OTHER` | 0 | 0 |
| `UNKNOWN` | 33 | 114 |

Mod 列为**文件名标签 + 文件夹名扫描**；project 列为 **OSP 名称 / dataFolder / sourceFile / outputPath 实测**。两者不一致的地方以 project 列为准（有真实证据）。

### 8. 需要 3BA 转换的项目

| 判定 | project 数 |
|---|---|
| `UNKNOWN` | 114 |
| `NO` | 60 |
| `YES` | 2 |

**明确 YES = 2**。UNKNOWN 未列入 —— 按决策 3，无充分证据不猜。

### 9. DIY 价值最高的 Mod

| Mod | parts | 可分类 part | BodySlide project | 体型 |
|---|---|---|---|---|
| `Nyes Latex Pack AiO 1.3 (ReducedSize)` | 309 | 309 | 24 | `UNKNOWN` |
| `Latex Lover Corset 增强版 — Latex Lover Corset Plus — 【` | 177 | 177 | 1 | `UNKNOWN` |
| `[Predator] Latex Acessories 3BA SE — 【服装·装备】【体型·CBBE` | 194 | 130 | 1 | `CBBE_3BA` |
| `静默代码 — SSE Silent Code — 【服装·装备】【身体·物理】【来源·本地】` | 63 | 44 | 7 | `UNKNOWN` |
| `SSE_Latex_Nun — 【来源·本地】` | 48 | 30 | 3 | `UNKNOWN` |
| `Brastia Battle Princess Spandexer for 3BA — 【战斗·技能】【` | 33 | 30 | 1 | `CBBE_3BA` |
| `[Predator] Silicon Acessories CBBE 3BA AE — 【体型·CBBE` | 88 | 24 | 2 | `CBBE_3BA` |
| `[Predator] Slave Harness Chastity CBBE 3BA AE — 【体型·` | 22 | 22 | 1 | `CBBE_3BA` |
| `J3 Latex 3BA — 【服装·装备】【体型·CBBE+3BA】【来源·本地】` | 27 | 21 | 1 | `CBBE_3BA` |
| `Skimpy Assassin 服装 - BHUNP 3BBB - CBBE 3BBB — Skimpy` | 20 | 20 | 1 | `BHUNP` |
| `[Predator] Premium Laced LatexBodysuit — 【来源·本地】【系列·` | 20 | 20 | 1 | `UNKNOWN` |
| `SSE_VRC_Latex_Servant — 【来源·本地】` | 39 | 19 | 3 | `UNKNOWN` |

### 10. 高度重复的 Mod

- byte-identical 重复组：**70** 组，多余副本 **103** 个
- 同名不同内容（VFS 遮蔽）：**110** 组
- **MO2 虚拟路径冲突组：161**，其中 **93** 组内容不同（失败者被完全遮蔽，永不进入 VFS），被遮蔽字节 **772,549,680 B**

### 11. 只值得保留部分零件的 Mod

| Mod | parts | 空壳 part | 无插件 part | 建议 |
|---|---|---|---|---|
| `[Predator] Latex Acessories 3BA SE — 【服装·装备】【体型·CB` | 194 | 0 | 0 | `PARTIAL` |
| `[Predator] Silicon Acessories CBBE 3BA AE — 【体型·CB` | 88 | 0 | 0 | `PARTIAL` |
| `静默代码 — SSE Silent Code — 【服装·装备】【身体·物理】【来源·本地】` | 63 | 0 | 0 | `PARTIAL` |
| `SSE_Latex_Nun — 【来源·本地】` | 48 | 0 | 0 | `PARTIAL` |
| `SSE_VRC_Latex_Servant — 【来源·本地】` | 39 | 0 | 0 | `PARTIAL` |
| `乳胶安杰莉 — SSEDDAngeli 3BA — 【服装·装备】【身体·物理】【体型·CBBE+3` | 36 | 0 | 0 | `PARTIAL` |
| `Brastia Battle Princess Spandexer for 3BA — 【战斗·技能` | 33 | 0 | 0 | `PARTIAL` |
| `SSE_Kakugo_LatexNun — 【来源·本地】` | 31 | 0 | 0 | `PARTIAL` |
| `J3 Latex 3BA — 【服装·装备】【体型·CBBE+3BA】【来源·本地】` | 27 | 0 | 0 | `PARTIAL` |
| `矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3` | 24 | 0 | 0 | `DROP_CANDIDATE` |
| `AE_VRC_Bunny_Nurse — 【来源·本地】` | 22 | 0 | 0 | `PARTIAL` |
| `makaron-COSPLAY - AE_Toxic_Cat — 【服装·装备】【来源·本地】` | 21 | 0 | 0 | `PARTIAL` |

### 12. DROP 候选

见 `15_REWORK_RELATIONSHIPS.csv` 的 `recommended_keep` 列。本阶段**不执行任何删除**。

### 13. MERGE_EASY 插件

**4** 个 / 共 47 个插件

### 14. 高风险插件

**MERGE_HIGH_RISK = 36**，MERGE_MODERATE = 7

### 15. 外部 FormID 引用

- 范围内插件之间的 formid 冲突组：**437**
- ARMO→ArmorAddon 依赖（**走 `ARMO.MODL`，1:N**，不是 RNAM）：**466** 条，见 `14_CROSS_MOD_DEPENDENCIES.csv`
- 配置层外部引用：见 `17_EXTERNAL_REFERENCES.csv`（逐条） / `17a_EXTERNAL_REFERENCES_BY_FILE.csv`（逐文件）

### 15a. OUTFIT (OTFT) 目标解析

- 范围内 OTFT 记录：**5** 条（`CatwomanTAS`, `CosmoAngel`, `SunAngel`, `MoonAngel`, `Zora`）
- `INAM` 成功恢复成 FormID：**5** 条
- 其中能在 09 范围内解析到目标记录：**5** 条

5 条 `INAM` 已恢复成 FormID，其中 **5** 条在 09 范围内解析到了目标记录。逐条见 `02_PLUGIN_RECORDS.csv` 的 `outfit_target_*` 三列；**解析不到的保持 UNKNOWN，不猜**。

| Outfit EDID | 插件 | INAM (FormID) | 目标 |
|---|---|---|---|
| `CatwomanTAS` | `[Brastia] Catwoman 3BA.esp` | `03000801;030009DA;03000826;03000827` | ARMO `CatwomanTasbodysuit` |
| `CosmoAngel` | `[Brastia] Battle Princess Spandexer 3BA.esp` | `0300080A;03000809;03000808;0300080B;03000806;03000807` | ARMO `SPeyeMaskCA` |
| `SunAngel` | `[Brastia] Battle Princess Spandexer 3BA.esp` | `03000821;03000822;03000823;03000824;03000825;03000826` | ARMO `SPBodysuitSA01` |
| `MoonAngel` | `[Brastia] Battle Princess Spandexer 3BA.esp` | `03000835;03000828;03000829;0300082A;0300082B;0300082C` | ARMO `SPBodysuitMA02` |
| `Zora` | `[Brastia] Battle Princess Spandexer 3BA.esp` | `03000832;0300082F;03000830;03000831;0300082D` | ARMO `SPCCapezr` |

### 15b. 🔴 分发层实测 —— 修正旧 P00 的「全为 0」

对 132 个 ini/xml/json/yaml/txt 配置文件做全文检测，结论与旧 P00 不一致：

| 层 | 旧 P00 | 本轮实测 |
|---|---|---|
| SPID | 0 | **0** ✅ 一致 |
| KID（关键词注入） | 0 | **54 行 / 5 文件** ⚠ **旧结论是假阴性** |
| BOS | 0 | **0** ✅ 一致 |
| OAR | 0 | **0** ✅ 一致 |
| DAR | 0 | **0** ✅ 一致 |
| Papyrus `.psc` | 0 | **0** ✅ 一致 |
| SKSE 配置 | 0 | **6**（NiOverride/TintData/Armor）|
| PGPatcher 规则 | 4 | **4** ✅ 一致 |

**KID 假阴性的根因**：这 5 个文件用的是裸行格式
`Keyword = <kw>|<category>|<formids>[+<plugin>]`，
**没有** `[KeywordInjector]` 这类小节头，因此旧审计的
`[KeywordInjector] / KeywordItemDistribution / KeywordDistribution`
三条正则**一条都匹配不到**。

| 文件 | Mod | 注入行数 |
|---|---|---|
| `nyeslatexpackaio_kid.ini` | `Nyes Latex Pack AiO 1.3 (ReducedSize)` | 22 |
| `rileyheels_kid.ini` | `Riley Heels — 【服装·护甲】` | 10 |
| `sse_tfd_haley_suit_kid.ini` | `makaron-COSPLAY - AE_TFD_Haley_Black_Suit — ` | 9 |
| `ae_vrc_outfits_orf_kid.ini` | `AE_VRC_Bunny_Nurse — 【来源·本地】` | 7 |
| `ae_latex_kitty_kid.ini` | `makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来` | 6 |

它们在运行时把 **SLA_\***（Sexy Latex Apparel）与 **ORF_\*** 关键词注入到护甲上 ——
**这是一层真实存在的分发逻辑，但在插件记录里完全看不见。**
对本项目的意义：ZLJ 统一 Keyword 时必须知道这层依赖，否则合流后会断。

**另有 2 个未解析的外部插件依赖**：

| 插件 | 声明位置 | 性质 |
|---|---|---|
| `Skyrim.esm` | `meta.ini` |  |
| `Heels Sound.esm` | `rileyheels_srd.yaml` |  |

### 16. Slot 冲突

| slot_mask | 次数 | 解释 |
|---|---|---|
| `0x00000004` | 297 | body |
| `0x00000080` | 215 | lowerleg |
| `0x00000000` | 106 |  |
| `0x00000008` | 101 | hands |
| `0x00008000` | 77 | chest |
| `0x00001000` | 71 | front |
| `0x00004000` | 63 | rightweapon |
| `0x00010000` | 58 | pelvis |
| `0x20000000` | 50 | bit29 |
| `0x10000000` | 45 | bit28 |

### 17. 跨 Mod DDS / NIF 依赖

全部数字由 `14_CROSS_MOD_DEPENDENCIES.csv` 聚合而来，**没有手填**。该表当前构成：

| dep_type | 行数 |
|---|---|
| `CROSS_MOD_TEXTURE` | 2044 |
| `CROSS_PLUGIN_ARMA` | 466 |

| 分桶 | 条数 |
|---|---|
| cross-target-mod | 2036 |
| external / out-of-scope | 474 |

- NIF 引用**范围内其它 TARGET Mod** 提供的贴图：**2,044** 条（`CROSS_MOD_TEXTURE`）—— 这不是 0。
- 跨插件 ArmorAddon 引用：**466** 条（`CROSS_PLUGIN_ARMA`）
- NIF 贴图槽总数：**29,880**
- 其中在本范围内找不到提供者的：**15653** 条

### 17b. NIF 分类（重-taxonomy 后）

| nif_class | 数量 |
|---|---|
| `GAME_MESH` | 774 |
| `SHAPEDATA` | 542 |

> 原始扫描器按任务书给定的有序规则执行，在本范围上只有 SHAPEDATA 能命中（没有任何 NIF 位于 /bodyphysics/、/static/、meshes/actors/ 等路径）。本轮在报告层重做了一次分类，**原始扫描输出未被修改**，旧值保留在 `nif_class_raw`。

### 18. 材质分布

| 材质类 | shape 数 |
|---|---|
| `UNKNOWN` | 2770 |
| `LATEX` | 2755 |
| `METAL` | 533 |
| `RUBBER` | 76 |
| `TRANSPARENT` | 51 |
| `LEATHER` | 41 |
| `FABRIC` | 20 |
| `VINYL_PVC` | 12 |
| `POLYESTER` | 9 |
| `SILK` | 1 |

### 19. FAKE_METALLIC_LATEX 清单

**2733** 个 shape 同时满足：材质证据指向 LATEX/RUBBER/VINYL，但 NIF 暴露 EnvMap/specular 槽（legacy 材质把它做成像金属）。

| NIF | shape | material | 证据 |
|---|---|---|---|
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |
| `calientetools\bodyslide\shapedata\(nye's` | `calientetools\bodyslide\` | `LATEX` | material=LATEX (keyword 'latex') but NIF exposes EnvMap/spec |

### 20. 当前已有 PBR

- PGPatcher 规则文件：**4**
- `textures/pbr/` 目录所在 Mod：**0**
- 已含 PBR 通道（NORMAL/RMAOS/METALLIC/ROUGHNESS/AO/COAT）的 Mod：**1**
- 其余 Mod 为 legacy `_d/_n/_s/_e` 四通道：**5**

### 21. 推荐保留哪个 Rework / PBR 版本

本阶段**不做**版本取舍决定 —— 需要 `04_PARTS_CATALOG.csv` 与`15_REWORK_RELATIONSHIPS.csv` 的人工复核。
判定所需的客观输入已齐：同系列 Mod 的 priority、part 数、贴图字节、重复组归属。

### 22. 总资产大小

**19,375,174,818 B = 18.04 GiB**（3,708 个文件）

### 23. Safe byte dedup 可节省空间

**683,110,122 B = 651.46 MiB**（103 个多余副本）

### 24. KEEP / PARTIAL / DROP 后预计合集体积

**本阶段不估算。** KEEP/PARTIAL/DROP 需要逐 part 的人工决定，任何在此给出的数字都是猜测。决策输入见 `04_PARTS_CATALOG.csv`。

### 25. P01 推荐执行顺序

本报告**不进入 P01**。以下仅为 P00 内部遗留工作的建议顺序：

1. 修 `bs_slidersets` 口径（本轮已重扫解决，v1 报告需以本轮为准）
2. 补齐 body_candidate=UNKNOWN 的 Mod 的证据（ShapeData/OSP/NIF shape）
3. 人工复核 `19_CURRENT_BALANCE_VALUES.csv` 的 raw 字段与 CK 字段映射
4. 复核 `13/17` 的外部引用，决定哪些能进大 ESP

---

## 关键诚实声明

1. **ARMO 的 Value / Weight / ArmorRating 已按 Skyrim schema 解码。** `ARMO.DATA` = uint32 value + float32 weight；`ARMO.DNAM` = uint32 armor rating。`19_CURRENT_BALANCE_VALUES.csv` 全部 1,448 行三个字段均已解码，原始字节以 `data_raw_hex` / `dnam_raw_hex` 保留为 provenance，异常 weight 会被 `weight_sanity` 标出而不是丢弃。（上一版曾以「找不到权威 CK 列名」为由只输出 raw，该保留意见现已不适用。）
2. **slot_mask 来自 ARMO.BOD2 的 uint32 位掩码**，槽位名用标准 Skyrim 位表解码，`slot_confidence=MEDIUM`，原始十六进制同时保留。
3. **DDS 的 declared format 与实测存储量分开记录** —— 本轮发现 **0** 张贴图的 header 声明与实际字节数矛盾（多为作者工具把 DXGI 98 标在了 BC 数据上），以 `storage_class_measured` 为准。
4. **body_candidate=UNKNOWN 即无证据**，未做任何推测。
5. **ARMO→ArmorAddon 是 1:N，且带歧义的引用一律不配对。** 68 条 MODL 引用没能唯一解析到 ARMA（`ambiguous(N)` / `unresolved`），这些在 `03_ARMOR_ARMA_MAP.csv` 里**没有行**。按 24 位本地 id 强行配对会制造假链接，因此没有做。
6. **ARMO 自己的 MOD2..MOD5 是 world / inventory 模型，不是 worn mesh。** 任何材质 / 贴图 / 分区结论都必须沿 ARMO → MODL → ARMA → ARMA.MOD2..MOD5 取网格，否则结论无效。
7. **`UNKNOWN` 与 `NONE` 不同。** 证据里没有的字段打印 `UNKNOWN`；证据确证为空的字段（例如某 ARMO 确实没有任何 ArmorAddon）打印 `NONE`。

**P00_RERUN COMPLETE** —— 上一版结果已作废，见 「⚠ SUPERSEDE NOTICE」一节。
