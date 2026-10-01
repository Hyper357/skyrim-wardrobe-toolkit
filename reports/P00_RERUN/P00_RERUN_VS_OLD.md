# P00_RERUN_VS_OLD.md — 新旧 P00 对比

只对比**关键数字与重大差异**。旧 P00 成果未被覆盖，仍在 `reports/P00/`，状态 `archive / reference only`。

## 0. ⚠ SUPERSEDE NOTICE — 上一版 P00_RERUN 已被作废（schema fix）

**本次 schema fix 之前生成的整套 P00_RERUN 结果已整体作废。** 它们不是「旧了一点」，而是**方向错了**：

| # | 缺陷 | 证据 |
|---|---|---|
| 1 | `ARMO.RNAM` 被当成 ArmorAddon 链接 | RNAM 100% 指向 **RACE**（vanilla 全库 2,762 条 ARMO 实测）；ArmorAddon 链接是 `ARMO.MODL`，且 1:N（702/2762 条 ARMO 有多条 MODL） |
| 2 | ARMO 自己的 MOD2..MOD5 被当成 worn mesh | worn mesh 在 **ARMA** 上；ARMO 的 MOD2..MOD5 是 world / inventory 模型 |
| 3 | 链接被单值化 | 一个 ARMO 可以挂多个 ArmorAddon，旧表只有 `ARMA_formid` 一列 |
| 4 | 二进制 OSD 解析器被用在 XML `.osp` 上 | `ShapeData/*.osd` 才是二进制（`OSD\0`）；`SliderSets/*.osp` 是 XML。旧解析器对 `.osp` 静默返回空 → 07 的 shapedata/sliderset 计数全是假空 |
| 5 | `classify_body` 把 CBBE-only 并进 OTHER | 现已单独判为 `CBBE`；任何假定 CBBE 不存在的聚合都需重算 |

### 被作废的输出

| 输出 | 波及层级 | 原因 |
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

### 因此，下面第 1–4 节的数字只能与 `reports/P00/` 的旧 P00 比，**不能**与上一版 P00_RERUN 比。**
上一版 P00_RERUN 的对应数字已作废，不在此列出 —— 列出来只会让它看起来还能用。

### 解析器校准门

- 引用：`reports/P00_RERUN/PARSER_CALIBRATION.md`
- 门状态：**machine verdict: **PASS** -- **56/56 PASS, 0 FAIL****
- 说明：reports/P00_RERUN/PARSER_CALIBRATION.md present (87,080 B)

---

## 1. 范围

| 项 | 旧 P00 | P00_RERUN | 一致 |
|---|---|---|---|
| modlist SHA256 | `fba5d3a3…` | `5f03db69…` | ✅ |
| 范围 | L879–934 | L883–938 | ✅ |
| Mod 数 | 56 | 56 | ✅ |

## 2. 关键数字

| 指标 | 旧 P00 | P00_RERUN | 差异 |
|---|---|---|---|
| Mod 数 | 56 | 56 | ✅ |
| 文件数 | 3,708 | 3,708 | ✅ |
| 总体积 | 18.04 GiB | 18.04 GiB | ✅ |
| 插件 | 47 | 47 | ✅ |
| NIF | 1316 | 1316 | ✅ |
| DDS | 1355 | 1355 | ✅ |
| BodySlide 文件 | 1055 | 1245 | ⚠ +190 |
|   其中 SliderSet (.osp) | 0 | 176 | 🔴 旧版漏计 |
|   其中 ShapeData NIF | 542 | 542 | ✅ |
|   其中 ShapeData OSD | 513 | 513 | ✅ |
| 01_MOD_INVENTORY 列数 | 47（文档写 49） | 47 | ✅ |
| ARMA 记录 | 未解析 | 1321 | 新增 |
| TXST 记录 | 未解析 | 614 | 新增 |
| COBJ 记录 | 未解析 | 160 | 新增 |
| OTFT 记录 | 未解析 | 5 | 新增 |
| ARMO→ArmorAddon 链接 | 未解析 | 1787（ARMO → MODL → ARMA，1:N） | 新增 |

## 3. 重大差异说明

- **⚠ 本文件第 1–4 节不能与「上一版 P00_RERUN」比。** 上一版已被 schema fix 作废（见第 0 节），其数字不再有效。
- **BodySlide 计数口径不同**：旧版 1,055 只统计了 ShapeData 的 NIF+OSD；本轮把 SliderSet(.osp) / SliderGroup / SliderPreset 一并计入，合计 1245。旧脚本的 `bs_slidersets` 恒为 0，根因是只匹配 `.xml`，而本批 176 个 SliderSet 全部是新版 `.osp`。
- **插件层完全新增**：旧 P00 没有任何 ESP/ESL 记录解析，本轮真实解析了 47 个插件、3548 条记录（ARMO/ARMA/TXST/COBJ/OTFT）。
- **🔴 旧 P00 的「KID 关键词分发 = 0」是假阴性。** 本轮全文检测 132 个配置文件，发现 **5 个文件 / 54 行关键词注入**，向护甲注入 SLA_*/ORF_* 关键词。旧审计的三条 KID 正则要求存在`[KeywordInjector]` 类小节头，而这些文件用的是裸行 `Keyword = <kw>|<category>|<formids>` 格式，一条都匹配不到。**结论：09 范围没有 SPID/BOS/OAR/DAR/Papyrus，但确实有一层 KID。**
- **modlist mtime 已失效但 SHA256 未变**：审计期间 MO2 开关两次，`modlist.txt` 被原子替换，mtime 刷新而内容逐字节相同。范围判断因此只用 SHA256。

## 4. 旧成果的处置

- `reports/P00/00_SCOPE.md`、`01_MOD_INVENTORY.csv` —— **保留为 archive**，不删除、不覆盖。
- 旧 `01_MOD_INVENTORY.csv` 的 `bs_slidersets` 列全为 0，根因是脚本只认 `.xml` 而本批 Mod 用新版 `.osp`；P00_RERUN 已按 `.osp` 正确计入。
- 旧报告的「913 个 Mod」轶事在当前盘面不可复现，本轮未沿用。

**P00_RERUN COMPLETE**
