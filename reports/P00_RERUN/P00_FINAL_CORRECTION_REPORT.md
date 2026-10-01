# P00_FINAL_CORRECTION_REPORT.md

**P00 最终校正报告** — 关系层与报告层修正，未做第三次全量扫描。

---

## 0. 结论

# P00 FINAL FROZEN

- 内部一致性 gate：**39 PASS / 0 FAIL**（`P00_FINAL_CONSISTENCY_GATE.csv`）
- 解析器校准门：**56 PASS / 0 FAIL**（`PARSER_CALIBRATION.md`）

冻结复用的阶段：00 / 01 / 02 / 03 / 08 / 09 / 10 与 MO2 priority 基线。
本轮只修改了**关系层**（BodySlide VFS 有效视图、PART↔项目匹配、ArmorAddon 跨插件关系）与**报告层**（14 / 15 / 18 / 19 / MASTER）。

---

## 1. 逐项对照

| 审计要求 | 状态 | 关键数字 |
|---|---|---|
| A. BodySlide 改 VFS effective view | ✅ | PHYSICAL 176 / EFFECTIVE 156 / shadowed 20 |
| B. 删除 fuzzy BodySlide 匹配 | ✅ | method={'UNKNOWN': 1089, 'EXACT_OUTPUT_PATH': 279, 'UNIQUE_STRONG_MATCH': 80}，每 part 最多 3 个项目 |
| C. 修复 14 跨 Mod 矛盾 | ✅ | {'CROSS_MOD_TEXTURE': 2044, 'CROSS_PLUGIN_ARMA': 466}，已按 same-mod / cross-target-mod / external 分桶 |
| D. 重做 LOGICAL_OUTFIT | ✅ | 56 个 outfit，{'BASE_MOD': 47, 'PATCH_MOD': 7, 'REWORK_MOD': 2} |
| E. 重做 merge risk | ✅ | risk_tier {'HIGH': 36, 'MODERATE': 7, 'LOW_EASY': 4}，OTFT 独立 REFERENCE_REMAP_REQUIRED |
| F. 解码真实数值 | ✅ | 1448/1448 行三字段齐全 |
| G. `game_nif_resolved` 改名 | ✅ | `game_nif_paths` + `game_nif_resolution_status` |
| H. 内部一致性 gate | ✅ | 39/39 |

---

## 2. A — BodySlide 有效 VFS 视图

`07_BODYSLIDE_PROJECTS.csv` 每行现在带 `winning_provider` / `shadowed_provider` / `effective`，并由 `data/P00_RERUN/07_bodyslide_vfs_summary.json` 提供顶层计数。

| 计数 | 值 |
|---|---|
| `PHYSICAL_PROJECT_ROWS` | 176 |
| `EFFECTIVE_VFS_PROJECTS` | 156 |
| `SHADOWED_PROJECT_ROWS` | 20 |
| `SHADOWED_VFS_PATHS` | 20 |
| `CONTENT_CONFLICTING_VFS_PATHS` | 4 |

判定规则沿用既有口径：**modlist 行号最小 = 优先级最高 = VFS 胜者**。20 条被覆盖路径全部由 L883 `Nye Latex Pack AiO 1.3 (ReducedSize)` 取得覆盖权，其中 4 条 sha256 不同（真实内容冲突）。

**下游只使用 effective 项目** —— gate `G-09` 断言没有任何 PART 引用被覆盖的项目，结果 0。

---

## 3. B — 删除 fuzzy 匹配

旧实现用 stem 子串包含（`s in k or k in s`），实测把 `J3Bodysuit` 链到 15 个项目（Nye / Corrupted / Gantz / Catwoman / Predator 各包），并把 Brastia 的 Choker / Gloves / Mask / Cape 全部挂到 Spandexer Boots 项目。那是共用 pack 目录名，不是共用资产。

新规则：

- **LEVEL 1 `EXACT_OUTPUT_PATH`** — ARMA 穿戴 mesh 归一化路径与 effective OSP `output_nif` 落在同一虚拟族（`foo.nif` / `foo_0.nif` / `foo_1.nif` / `foo_1stPerson.nif` 归为一族，目录与族名都必须相同）
- **LEVEL 2 `UNIQUE_STRONG_MATCH`** — 仅在**同一 source mod** 内，按族名匹配，且候选数必须恰为 1
- **LEVEL 3 `UNKNOWN`** — 无法唯一确认

| 指标 | 修正前 | 修正后 |
|---|---|---|
| 有项目关联的 part | 795 | 359 |
| 单个 part 最多项目数 | 15 | 3 |
| 每 part 平均项目数 | 1.14 | 1.02 |

| `bodyslide_match_method` | part 数 |
|---|---|
| `UNKNOWN` | 1089 |
| `EXACT_OUTPUT_PATH` | 279 |
| `UNIQUE_STRONG_MATCH` | 80 |

覆盖率下降是**刻意**的：宁可 UNKNOWN 也不猜。审计点名的 6 个已知假链接全部消失（gate `G-12`，6/6 PASS）。

---

## 4. C — 14 跨 Mod 依赖矛盾

旧 MASTER 写「NIF 引用其它 TARGET Mod DDS = 0」，而 `14_CROSS_MOD_DEPENDENCIES.csv` 实际有 2,510 行非空。根因是旧的计数用了一个永远匹配不到的 `/{mod 名}/` 路径测试。现已改为直接从 14 聚合。

| dep_type | 行数 |
|---|---|
| `CROSS_MOD_TEXTURE` | 2044 |
| `CROSS_PLUGIN_ARMA` | 466 |

分桶（same-mod / cross-target-mod / external-out-of-scope / unresolved）已写入 MASTER 第 17 节。

---

## 5. D — LOGICAL_OUTFIT 重做

旧规则把全部 Predator 折叠成一个 outfit，并按 MO2 显示名里的「物理」/「3BA」字样去判 PHYSICS_PATCH / BODYSLIDE_CONVERSION。两条都是标签，不是证据。

| 指标 | 修正后 |
|---|---|
| logical outfit 数 | 56 |
| role = `BASE_MOD` | 47 |
| role = `PATCH_MOD` | 7 |
| role = `REWORK_MOD` | 2 |

**9 个 Predator Mod → 9 个不同 logical outfit**（审计点名要求）。

非 BASE 的每一条都带 `parent_mod` + `relationship_evidence` + `confidence`，证据是具体的，例如：

- `Haley Black Suit PBR` → parent `makaron-COSPLAY - AE_TFD_Haley_Bla`
  - the folder it introduces, 'sse_tfd_haley_black_suit', is a strict derivation of parent 'SSE_TFD_Haley_Black_Suit' (exact match) | payload is 20 path(s
- `00 资源·H2135 披风物理补全 — H2135 Cloak SMP Physics` → parent `<out-of-scope> harry2135/fantasyse`
  - owns no armor records, no mesh file and no BSA (ARMA=0, ARMO=0, plugins=0, own .nif=0, bsa=0) and no in-scope mod provides the armor it projects, so i
- `MiscMods Stilettos Zwei 与 Eins — AnkleCut V2` → parent `MiscMods Stilettos Zwei 与 Eins — M`
  - the folder it introduces, 'mischeelseins 3ba anklecut', is a strict derivation of parent 'mischeelseins 3ba' (extension 'anklecut') | payload is 7 pat
- `堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex ` → parent `堕落紧身衣 — AE Corrupted Body Suit — 【`
  - shadows 18 of the parent's OUTFIT virtual paths (dds x7, nif x11), MO2 13_MO2_CONFLICT_MAP records 18 VFS_OVERRIDE wins (0 byte-identical); the folder
- `静默代码·乳胶重制 — Silent Code - Latex Rework — 【服装` → parent `静默代码 — SSE Silent Code — 【服装·装备】【身`
  - shadows 64 of the parent's OUTFIT virtual paths (dds x64), MO2 13_MO2_CONFLICT_MAP records 64 VFS_OVERRIDE wins (2 byte-identical); the folder it intr
- `MiscMods Stilettos Zwei 与 Eins — MiscMods St` → parent `<out-of-scope> mischeelseins 3ba /`
  - owns no armor records, no mesh file and no BSA (ARMA=0, ARMO=0, plugins=0, own .nif=0, bsa=0) and no in-scope mod provides the armor it projects, so i
- `EvilFall — 【来源·本地】` → parent `<out-of-scope> evilfall / evilfall`
  - owns no armor records, no mesh file and no BSA (ARMA=0, ARMO=0, plugins=0, own .nif=0, bsa=0) and no in-scope mod provides the armor it projects, so i
- `SEXY 靴子-2B Wedding 靴子 [3BA] Edited — SEXY BO` → parent `<out-of-scope> cbbe se coco 2b wed`
  - owns no armor records, no mesh file and no BSA (ARMA=0, ARMO=0, plugins=0, own .nif=0, bsa=0) and no in-scope mod provides the armor it projects, so i
- `[TRX] LatexWhitch — 【来源·本地】` → parent `<out-of-scope> [trx]  latexwhitch `
  - owns no armor records, no mesh file and no BSA (ARMA=0, ARMO=0, plugins=0, own .nif=0, bsa=0) and no in-scope mod provides the armor it projects, so i

---

## 6. E — merge risk 重做

旧判据「不同 plugin 的 raw/local FormID 数值相同」已**彻底删除** —— 合并时 FormID 本来就要重映射，重叠不构成风险证据。该信息仅以 `formid_overlap_INFO_ONLY` 保留，不参与分级。

| `risk_tier` | plugin 数 |
|---|---|
| `HIGH` | 36 |
| `MODERATE` | 7 |
| `LOW_EASY` | 4 |

| `reference_class` | plugin 数 |
|---|---|
| `EXTERNAL_UNRESOLVABLE_REF` | 33 |
| `EXTERNAL_THIRD_PARTY_MASTER` | 5 |
| `INTERNAL_ONLY` | 4 |
| `MODEL_ANIMATION_VMAD` | 3 |
| `REFERENCE_REMAP_REQUIRED` | 2 |

OTFT 归入 **`REFERENCE_REMAP_REQUIRED`**，与 `SCRIPT_BEHAVIOUR` 分开 —— 「需要重映射引用」和「是脚本」是两种不同的义务。

---

## 7. F — 数值字段解码

按已确认的 Skyrim ARMO schema 解码，原始字节保留为 provenance：

- `ARMO.DATA` 8 字节 = uint32 **value** + float32 **weight**
- `ARMO.DNAM` 4 字节 = uint32 **armor_rating**

- `19_CURRENT_BALANCE_VALUES.csv` **1448** 行，**1448** 行三字段齐全
- `weight_sanity` 分布：{'ok': 1448}

上一版「找不到权威 CK 列名所以不猜」的保留意见已不适用并从 MASTER 移除。

---

## 8. G — 字段改名

`game_nif_resolved`（实际存的是 NIF 路径）已拆为：

- `game_nif_paths` — 实际路径列表
- `game_nif_resolution_status` — `PENDING_BODYSLIDE`=703 / `RESOLVED`=412 / `PARTIAL`=225 / `UNRESOLVED`=108

---

## 9. H — 内部一致性 gate 结果

| check | 结论 | 说明 |
|---|---|---|
| `G-01` | PASS | 04_PARTS_CATALOG.csv present and parseable |
| `G-01` | PASS | 05_SLOT_PARTITION_MAP.csv present and parseable |
| `G-01` | PASS | 06_DIY_COMPATIBILITY_MATRIX.csv present and parseable |
| `G-01` | PASS | 07_BODYSLIDE_PROJECTS.csv present and parseable |
| `G-01` | PASS | 14_CROSS_MOD_DEPENDENCIES.csv present and parseable |
| `G-01` | PASS | 15_REWORK_RELATIONSHIPS.csv present and parseable |
| `G-01` | PASS | 18_PLUGIN_MERGE_RISK.csv present and parseable |
| `G-01` | PASS | 19_CURRENT_BALANCE_VALUES.csv present and parseable |
| `G-01` | PASS | P00_MASTER_REPORT.md present and parseable |
| `G-01` | PASS | P00_RERUN_VS_OLD.md present and parseable |
| `G-01` | PASS | PARSER_CALIBRATION.md present and parseable |
| `G-02` | PASS | 14_CROSS_MOD_DEPENDENCIES is non-empty |
| `G-03` | PASS | master reports CROSS_MOD_TEXTURE consistent with CSV |
| `G-03` | PASS | master reports CROSS_PLUGIN_ARMA consistent with CSV |
| `G-04` | PASS | no master/CSV zero contradiction |
| `G-05` | PASS | 14 exposes from_mod/to_mod for bucketing |
| `G-06` | PASS | 07 physical rows >= effective rows |
| `G-07` | PASS | vfs summary PHYSICAL matches CSV row count |
| `G-08` | PASS | vfs summary EFFECTIVE matches CSV effective count |
| `G-09` | PASS | no PART references a MO2-shadowed project |
| `G-10` | PASS | bodyslide_match_method vocabulary |
| `G-11` | PASS | no part attached to a large project set |
| `G-12` | PASS | known false link gone: J3 Bodysuit |
| `G-12` | PASS | known false link gone: Brastia Gloves |
| `G-12` | PASS | known false link gone: Brastia Choker |
| `G-12` | PASS | known false link gone: Brastia Mask |
| `G-12` | PASS | known false link gone: Corrupted Body |
| `G-12` | PASS | known false link gone: Kitty Tail |
| `G-13` | PASS | random chain spot-check (20 parts) |
| `G-14` | PASS | game_nif_resolved removed (misleading name) |
| `G-15` | PASS | game_nif_paths + status present |
| `G-16` | PASS | status vocabulary and total |
| `G-17` | PASS | 19 decodes value+weight+armor_rating |
| `G-18` | PASS | 19 keeps raw provenance |
| `G-19` | PASS | merge risk does not cite FormID-overlap as a reason |
| `G-20` | PASS | OTFT has its own class, not SCRIPT_TYPES |
| `G-21` | PASS | Predator mods are not one logical outfit |
| `G-22` | PASS | 15 has parent/evidence/confidence |
| `G-23` | PASS | parser calibration gate |

合计 **39 PASS / 0 FAIL**。

---

## 10. 遗留事项（不阻塞 P00 冻结）

1. **68 条 MODL 引用仍未解析** —— 校准确认这些 FormID 在全库 1,770 个插件中都不存在，是**决策问题**（丢弃 / 保留为 dangling）不是 parser 问题。
2. **443 条跨插件 ArmorAddon 链接的 addon 细节为 UNKNOWN** —— 链接本身成立（`ARMA_resolved` 形如 `1/4`，分母是真实引用数），但那些 addon 记录在只解析的 47 个插件之外，其 mesh / slot 明细取不到，故如实标 UNKNOWN 而非编造。
3. **DIY 矩阵状态顺序**照字面执行，UNKNOWN 排在最后；要让 UNKNOWN 短路需重生成。
4. **MO2 仍处于运行状态**，modlist 可能在下次运行时漂移；进入 P01 前请先关闭。
