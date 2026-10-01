# PROJECT_HANDOFF_AUDIT.md

**工程**：latex Wardrobe Collection（交接指令中称 ZLJ Wardrobe Collection —— 见 §8.1 命名冲突）
**当前阶段**：P00_INVENTORY_AND_ARCHITECTURE_AUDIT
**审计性质**：只读交接审计。**未执行任何 P00 计算，未修改任何既有成果，未触碰任何游戏文件。**
**审计日期**：2026-09-29
**审计范围**：`E:\SkyrimAE\opencode工作目录\5-latex-wardrobe-collection\`（本 packet）
+ 全盘 464,093 个文件的精确文件名检索 + 关联既有归档

---

## 摘要（先看这三条）

1. **本 packet 只完成了 P00 的第 1 阶段**（范围定义 + Mod 级盘点）。22 项预期成果中，
   2 项存在、20 项缺失。**不是"接近完成"，是"刚开题"。**
2. **但是**：同盘上存在一个**已退出队列的兄弟工程**（`3-p02-6-latex-repository`），
   它的扫描管线与数据缓存**大部分还活着**，并且覆盖了冻结 56 个 Mod 中的 52–55 个。
   其中 `nif_parsed` 缓存里存着**真实 NIF 解析出的 BSTriShape 名称**，
   这是决策 3（体型必须靠证据判定）所要求的证据类型。
   **实测：29 个 UNKNOWN 里，21 个现在就有可用的强证据。**
3. **本 packet 有一个必须先修的缺陷**：`bs_slidersets` 恒为 0，
   漏计 176 个 `.osp` / 52 个 Mod。它是决策 3 指定的证据源之一，不是装饰性 bug。

---

## 1. 当前工程目录结构

```
E:\SkyrimAE\opencode工作目录\5-latex-wardrobe-collection\
├─ 交付说明.md                       4,097 B   阶段一交付说明
├─ data\
│  └─ p00_scope.json                10,959 B   modlist SHA256 / 范围边界 / 成员表 / 命中表
├─ reports\
│  ├─ P00\
│  │  ├─ 00_SCOPE.md               17,150 B   范围定义
│  │  └─ 01_MOD_INVENTORY.csv      17,463 B   56 行 × 47 列
│  └─ HANDOFF\                                ← 本次审计新增
│     ├─ PROJECT_HANDOFF_AUDIT.md
│     ├─ P00_COMPLETION_MATRIX.csv
│     ├─ EXISTING_ARTIFACTS_INDEX.csv
│     ├─ REUSABLE_TOOLS.md
│     └─ NEXT_ACTION_PLAN.md
└─ tools\
   ├─ p00_common.py                 11,000 B   路径常量 + MO2 优先级模型 + 体型分类器
   ├─ p00_s1_scope.py               22,722 B   阶段一扫描器
   ├─ README.md                      2,746 B   只读保证 / 配置 / 优先级模型
   └─ requirements.txt                 635 B
```

**用户 brief 中提到但本 packet 并不存在的目录**：
`staging\`、`archive\`、`docs\`、`AGENTS.md` —— 经全盘检索确认**均不存在**。
`staging/` 在本工程从未建立过；`ZLJ Latex Material Repository` 的 staging 属于**已灭失的 3 号工程**。

工程外的一手交付快照：`E:\SkyrimAE\opencode工作目录\5-latex-wardrobe-collection.zip`
（19:27 打包，10 个条目，与工作目录内容一致，现已被工作目录取代）。

---

## 2. 已经完成哪些阶段

| 阶段 | 状态 | 依据 |
|---|---|---|
| P00 阶段一：范围定义 | ✅ 完成 | `00_SCOPE.md` |
| P00 阶段一：Mod 级盘点 | ⚠️ 完成但有缺陷 | `01_MOD_INVENTORY.csv`（`bs_slidersets` 漏计） |
| P00 阶段二 ~ 十一 | ❌ 未开始 | `tools/README.md:65` 自述"未开始（等 P00 范围审核）" |
| P01 及以后 | ❌ 未触及 | 无任何文件 |

**没有任何超出 P00 的动作发生。** modlist 在整个工程生命周期内只被 MO2 自己改写过
（18:29、18:31 两次），P00 脚本零写入。

---

## 3. P00 已有哪些报告

只有两份：

| 文件 | 大小 | 内容 |
|---|---|---|
| `reports/P00/00_SCOPE.md` | 17,150 B | 6 节：环境真值、优先级模型、范围解析、汇总+体型分布+分发层现状+56 Mod 明细、边界声明、写操作清单 |
| `reports/P00/01_MOD_INVENTORY.csv` | 17,463 B | 47 列 × 56 行，UTF-8-BOM |

外加一份中间证据 `data/p00_scope.json`（10,959 B）。

---

## 4. 每份报告是否完整

按"不能只看文件存在"的标准逐项核验。

### 4.1 `00_SCOPE.md` → **COMPLETE**

- 数据量合理：56 行明细表，列出逐 mod 的 MiB / 文件数 / 插件数 / NIF / DDS / BS / 体型 / 证据来源 / 备注
- 可关联：`§3.1` 交叉核对表把任务书 31 个示例关键词全部映射到具体 modlist 行号
- 证据链：记录了 modlist SHA256、mtime、扫描时刻
- 覆盖冻结 56：✅
- **两处文档缺陷（不影响数据）**：
  1. 引用的"读反了会算成 913 个 Mod"在当前盘面**不可复现**。按反向规则（成员归到行号更小的分隔符）实测为 **129** 个（L936–1064）。我另试算了 10 种可能读法，没有一种得出 913。这只是个历史轶事，不承重。
  2. `§4.2` 脚注称"SliderSets / SliderGroups / SliderPresets 的 BodySlide XML 同时计入 `n_xml` 与 `bs_*`"——对 SliderSets **不成立**（见 §5）。

### 4.2 `01_MOD_INVENTORY.csv` → **PARTIAL**

- 表头 **47 列**（不是 `交付说明.md:13` 声称的 49 列 —— 那是文字笔误）
- 56 行数据，每行 47 列，无残行
- 真实枚举：`total_size_bytes` 求和 = 19,375,174,818 B，与磁盘实测逐字节相符
- **缺陷**：`bs_slidersets` 全 56 行为 0
- **死列**：`n_fomod` 在 `p00_s1_scope.py:39` 声明后全文无任何自增语句，恒为 0
- 交叉验证通过的列：`file_count` 3708、`n_nif` 1316、`n_dds` 1355、`n_esp` 46、`n_esl` 1、
  `n_ini` 68、`n_xml` 59、`bs_total` 1055、`smp_config_xml` 4、`pbrnifpatcher_json` 4 —— **全部与 `00_SCOPE.md` 声称一致**

### 4.3 其余 20 项 + `P00_MASTER_REPORT.md` → **MISSING**

全盘精确文件名检索（464,093 个文件）确认：**`02_PLUGIN_RECORDS.csv` … `20_SPACE_OPTIMIZATION.csv`
与 `P00_MASTER_REPORT.md` 在整个 E: 盘上不存在任何副本。**
没有"只有表头"的空壳，没有 superseded 的旧版本，就是没有。

---

## 5. 现有成果里最需要立刻处理的一个缺陷

**`bs_slidersets` 恒为 0，漏计 176 个 `.osp` 文件 / 52 个 Mod。**

根因在 [tools/p00_s1_scope.py:183-187](../../tools/p00_s1_scope.py#L183-L187)：

```python
elif low.startswith("calientetools/bodyslide/slidersets/"):
    if ext == ".xml":          # ← 只认 .xml
        rec["bs_slidersets"] += 1
```

而这批 Mod 用的是**新版 BodySlide 的 `.osp` 格式**。实测：

| BodySlide 子目录 | 实际扩展名 | 文件数 | 被脚本计入 |
|---|---|---|---|
| ShapeData | `.nif` / `.osd` | 542 / 513 | ✅ |
| **SliderSets** | **`.osp`** | **176** | **❌ 0** |
| SliderGroups | `.xml` | 9 | ✅ |
| SliderPresets | `.xml` | 5 | ✅ |

连带影响：

- `.osp` 既不进 `n_xml`（那条链只收 `.xml`），也不进 `bs_slidersets`，
  **只出现在 `file_count` 里，在 BodySlide 统计中彻底隐形**
- `00_SCOPE.md:104` 的"BodySlide 文件 1,055"偏小；磁盘实际 BodySlide 资产 **1,257**
- `00_SCOPE.md:150` 那句"同时计入 `n_xml` 与 `bs_*`"对 SliderSets 不成立

**为什么这条必须修，而且优先级高于其它补做：**
交接指令的决策 3 明确要求体型判定必须依据
`SliderSets / ShapeData / OSP / OSD / bones / partitions / BodySlide project metadata`。
`.osp` 是被点名的证据源之一，而现在它在账本上是 0。

**我已经先替你验过一件事**（避免修完才发现没用）：
把 `.osp` 的文件名补进 `body_type_from_assets` 证据链后重算 ——
**29 个 UNKNOWN 一个都没被救回，5 个 `bodyslide_assets` 判定也全部不变。**
原因是 OSP 文件名是服装名（`Latex Bodysuit`、`Platform Boots`、`Bandeau Leotard`），
里面没有 CBBE / 3BA / BHUNP token。

**所以：`.osp` 缺陷是纯粹的计数 bug，不是分类 bug。**
它必须修（否则决策 3 的证据链少一环、`bs_total` 数字是错的），
但修它**不会**解决 29 个 UNKNOWN —— 那 21 个的答案在别处，见 §6.2。

---

## 6. 哪些数据可以直接复用

### 6.1 本 packet 内部 —— 可无条件继承

| 资产 | 为什么可信 |
|---|---|
| `tools/p00_common.py` | MO2 优先级模型经全表 2250 行逐行独立验证正确；体型分类器设计合理（token 化匹配，避免 `3BA` 误配 `3BBB`） |
| `data/p00_scope.json` | 含 modlist SHA256，可作为后续一切成果的 provenance 锚点 |
| `01_MOD_INVENTORY.csv` 的 `mod_name` / `mo2_priority` | **两者均唯一**，可直接充当 MOD_ID 的天然主键 |
| `modlist.txt` 事实 | SHA256 `fba5d3a3…` / 2250 行 / mtime 18:31:36.911578，三者独立复现 |

### 6.2 兄弟工程的存活缓存 —— 高价值，但必须按名字 join

`E:\SkyrimAE\opencode工作目录\3-p02-6-latex-repository\reports\_data\`
（`WINDOW_BRIEFING.md` 称该工程"已退出队列、1.33 GB 产物灭失"——
**灭失的是胶乳材质库本身，它的报告与数据缓存大部分仍在**。这是本次审计最重要的发现。）

| 缓存 | 规模 | 对应缺失成果 |
|---|---|---|
| `nif_parsed\chunk_*.json.gz` | 6,732 个已解析 NIF | 04 / 05 / 08 |
| `index_loose.pkl.gz` | 417,896 条 VFS 松散文件索引（含 prio/size/mtime） | 10 / 12 / 13 / 20 |
| `armature.json.gz` | 47,791 条 ARMO 记录（含 EDID/FULL/MOD2 子记录） | 02 / 03 / 19 |
| `bodyslide_projects.json.gz` | 4,540 个 BodySlide 工程 | 07 |
| `plugins_index.json.gz` | 1,837 个插件 → prio / mod / sha256 | 02 / 18 |
| `model_graph.json.gz` | ARMO→ARMA→NIF 图 + 覆盖哈希 | 03 / 14 / 18 |
| `bsa_index.pkl.gz` | BSA 成员索引 | 17 |
| `bodyslide_osp_providers.json.gz` | 870 个 `.osp` 的归属与优先级 | 04 / 07 |
| `scope_assets.json.gz` | 233 mod 逐 mod 资产统计 | 01 的增强版 |

以及 `_archive\2026-09\` 下三个旧审计，其中
`BODyslide_AUDIT\02_ALL_PROJECTS.csv`（4,487 行，**`osp` 列 100% 填充**，
覆盖冻结 56 中的 **51** 个）与 `ASSET_OPTIMIZATION_AUDIT\03_MOD_EFFECTIVENESS.csv`
（覆盖 **55**/56）价值最高。

#### ⚠️ 三条硬约束

1. **行号一律失效，只能按 mod 名 join。**
   3 号的 `scope_mods.json` 记录 09 块为 **69 条 / L879–947**，现为 **56 条 / L879–934**。
   69 条中只有 **4 条**在当前 modlist 的同一行号上对得上。3 号扫描发生在 09-29 09:01，
   早于 modlist 的 18:29/18:31 改写。
2. **它扫描的是 233 mod 的旧世界，不是冻结的 56。**
   55/56 在其范围内；唯一不在的是 **`Nyes Latex Pack AiO 1.3 (ReducedSize)`** ——
   它是 18:29 之后才插入 modlist 第 879 行的新 mod，也是本范围最大的单个 mod（533.6 MiB / 218 文件）。
   **它在所有旧缓存里都是零覆盖。**
3. **好消息：没有被已删除的 ZLJ 胶乳材质库污染。**
   四份旧 CSV 中含 `ZLJ` 的行数均为 **0**，`mods_enabled.json` 条目为 0。
   原因自洽：ZLJ 库是 18:29 才被 `_zlj_enable.py` 拉起来的，晚于所有旧审计的运行时间。

### 6.3 对决策 3 的直接影响（本包新发现）

`nif_parsed` 缓存存的是**真实 NIF 解析结果**，每个 shape 带
`name / type / shader / skin / alpha / partitions / n_bones / textures`。
我按"体型 token 出现在**哪类文件**里"对 29 个 UNKNOWN 做了证据分级：

| 证据级别 | 数量 | 含义 |
|---|---|---|
| **强证据** | **21** | 该 Mod **自己的** `CalienteTools/BodySlide/ShapeData/` 下的 BSTriShape 就叫 `3BA` |
| 弱证据 | 0 | — |
| 无证据 | 8 | 旧缓存里零 shape 记录 |

强证据样例：`L893 Latex Lover Corset Plus` 的 ShapeData 目录里有 58 个自带 shape；
`L926 [Predator] Premium Laced Latex Bodysuit` 的自带 shape 直接命名为 `Bodysuit_3BA` / `Boots_3BA`。

交叉验证：已判定的 mod 走同一套规则不产生矛盾 —— CBBE 3BA / 3BA 的 mod 多数也带 `3BA` shape，
3 个 BHUNP mod 一个都没有（正确，BHUNP 是另一套身体）。`n_bones` 分布与 `SBP_32_BODY`
等 partition 也已随缓存落盘。

**这 8 个仍然无证据**（旧缓存零覆盖或零 shape）：
`L879 Nyes Latex Pack`（新增 mod，旧缓存完全没有）、`L880 Haley Black Suit PBR`、
`L881 H2135 披风物理补全`、`L885 静默代码·乳胶重制`、`L891 SEXY 靴子-oneboot`、
`L895/L896 Nye's Latex Pack 2 / Pack`、`L924 [Zap] Gantz Suit`。

**我不对这 21 个下结论。** 按决策 3，它们是"证据已就位"，
仍需按 SliderSets / ShapeData / OSP / OSD / bones / partitions 的完整链条逐项记录后定稿。
这是你的决策，我只负责把证据摆到台面上。

---

## 7. 哪些任务明显尚未完成

02–20 全部缺失（见 §4.3）。按依赖关系排优先级：

- **无前置依赖，可立即做**：02、07、08、09、10
- **依赖 02/08**：03、04、05、09
- **依赖 04/05/11**：06
- **依赖全量数据**：12–20
- **收口**：`P00_MASTER_REPORT.md`

另有 3 项**非编号的欠账**：

1. `bs_slidersets` 漏计 `.osp`（§5）
2. `n_fomod` 死列
3. `交付说明.md:13` 的"49 列"应为 47 列；`00_SCOPE.md:150` 的 SliderSets 注释不成立

---

## 8. 是否存在互相矛盾的旧报告

### 8.1 🔴 命名冲突：ZLJ 是两个不同的东西

交接指令称本工程为 **ZLJ Wardrobe Collection**，但：

- 本 packet 的**目录名、脚本 docstring、报告标题全部**叫 `latex Wardrobe Collection`
- 磁盘上另有一个 **`ZLJ Latex Material Repository`** —— 那是**已灭失的 3 号工程的目标物**
  （229 文件 / 1.33 GB，modlist 条目已删，staging 已清，不可重建）

**风险**：后续任何 Agent 若按 "ZLJ" 去检索，很可能去找那个**已经不存在**的材质库，
或把 3 号工程的历史报告误当成本工程的成果。
**我没有改任何名字**（改名会让现有 SHA 与报告全部对不上），仅在此登记。
建议由你决定：是统一改名，还是在 `交付说明.md` 顶部加一行命名说明。

### 8.2 `WINDOW_BRIEFING.md` 的两处已过期陈述

| 简报原文 | 实况 |
|---|---|
| 3 号"已退出队列，1.33 GB 产物灭失，交接指令已失效" | **胶乳材质库确实灭失；但 3 号的 `_data\` 缓存与 `_scripts\` 管线仍完整存活**，见 §6.2 |
| "28 分隔符" | 全表分隔符实为 **33** 个（5 启用 + 28 禁用）。简报的 1+28+2197+24=2250 加得通，是把 5 个启用分隔符并进了"启用"类。**数字没错，标签不准** |

### 8.3 本 packet 内部

无互相矛盾的报告。`00_SCOPE.md` 与 `01_MOD_INVENTORY.csv` 的每一个可交叉验证的字段都一致
（3708 / 1316 / 1355 / 47 / 68 / 59 / 1055 / 4 / 4 / 1 全部对得上）。
唯一矛盾在**文字层**：`交付说明.md:13` 的"49 列"与实际的 47 列。

---

## 9. 是否存在临时 / 废弃成果

| 路径 | 性质 | 处置建议 |
|---|---|---|
| `5-latex-wardrobe-collection.zip` | 19:27 交付快照，已被工作目录取代 | SUPERSEDED，留档即可 |
| `3-p02-6-latex-repository\reports\LATEX_LIBRARY_*` | 描述已灭失的材质库 | 只能当方法论参考，**不可当当前事实** |
| `3-p02-6-latex-repository\reports\P02_6_FINAL_*` | 同上 | 同上 |
| `3-p02-6-latex-repository\reports\RECYCLE_BIN_INVENTORY.csv` | 同上 | 同上 |
| `_data\mods_enabled.json` | **实测条目数 = 0，不可用** | 废弃 |
| `_data\parse_validation.txt` | 0 字节 | 废弃 |
| `_data\scan_index.log` / `bsa_scan_stats.txt` | 日志碎片 | 废弃 |
| `_data\armature.json.gz` / `plugins_index.json.gz` | **扩展名撒谎，实为 pickle** | 复用时按 pickle 读 |
| 3 号 `_decoupled_build\_work\` | 110+ 个中间脚本与 JSON | 历史；其中 `L4_plan.json.gz`、`L1_refs.json.gz` 等可能有残余价值 |

**本 packet 内无临时文件残留。** 我在上一轮审计中产生的 `scratch\` 与
`tools\__pycache__\` 已清除，目录已恢复到与 `交付说明.md` 清单完全一致的 8 个文件。

---

## 10. 从哪里继续最合理

**结论：不要重跑 56 个 Mod 的枚举。** 那一步已经做对且已被独立验证两次。
真正的缺口不是"扫得不够"，而是"扫得太浅 + 账本里有一条腿是瘸的"。

**推荐的第一条执行任务**（详见 `NEXT_ACTION_PLAN.md`）：

> **A-0：补 `.osp` 记账，产出 `02_PLUGIN_RECORDS.csv` 之前先把 P00 阶段的账本修正。**
> 范围：改 `p00_s1_scope.py` 一处 + 重跑 + 与旧 CSV 逐行 diff。
> 新结果另存为 `01_MOD_INVENTORY.v2.csv`，**不覆盖旧证据**。

理由见 `NEXT_ACTION_PLAN.md`。**我现在停在审计，不执行任何一条。**

---

## 附录 A：本审计的只读自证

- 全程未修改任何既有成果
- 新增文件**全部**位于 `5-latex-wardrobe-collection\reports\HANDOFF\`
- 审计期间对 `mo2\` / `Data\` / `modlist` / BodySlide / PGPatcher **零写入**
- 审计用脚本写在 `scratch\`，交付完成后清除
- 未运行 BodySlide Build、未运行 PGPatcher、未 merge 任何插件、未创建最终合集

## 附录 A-1：🔴 审计期间观察到的 modlist 文件身份变动（接手者必读）

审计跨越 7 小时多。期间 **MO2 被启动并关闭了两次**：

| 时刻 | 现象 |
|---|---|
| 2026-09-30 00:12:07 | `settings.ini` 改写 |
| 2026-09-30 00:12:10 | **`modlist.txt` 被删除重建** |
| 2026-09-30 00:41:01 | `plugins.txt` / `loadorder.txt` / `lockedorder.txt` / `initweaks.ini` 改写 |
| 2026-09-30 07:53:07–13 | 第二次 MO2 会话，**`modlist.txt` 再次被删除重建**；`downloads\` 新增 `OutfitGallery 1.0.4` |

**判定：内容一字未改，只是文件换了身份。**

| 项 | 冻结基线 | 当前实测 | 结论 |
|---|---|---|---|
| SHA256 | `fba5d3a373be7f5e7010a2687d8bfc5abd4a568ab0f39edc6a5a25905df230e1` | **完全相同** | ✅ 内容逐字节未变 |
| 字节数 | 231,843 | 231,843 | ✅ |
| 行数 | 2250 | 2250 | ✅ |
| 范围 | L879–934 / 56 个 | L879–934 / 56 个 | ✅ |
| `01_MOD_INVENTORY.csv` 对齐 | — | 56/56 | ✅ 账本仍有效 |
| **mtime** | 2026-09-29T18:31:36.911578 | **2026-09-30T07:53:13.479206** | ❌ **已失效** |
| **ctime** | — | 与 mtime 相等 | ❌ 证明是**重建**而非原地编辑 |

**给接手者的三条操作规则：**

1. **判断 modlist 是否变化，只能用 SHA256，不能用 mtime。**
   本机 MO2 每次退出会把 `modlist.txt` 原子替换一次，mtime 必然刷新而内容可能一字未改。
   任何以 mtime 作新鲜度信号的逻辑都会误报。
2. **`00_SCOPE.md` §1 记的 mtime 已过期，同一行的 SHA256 仍有效** —— 引用 provenance 请引 SHA256。
3. **MO2 开着时不要读 modlist。** 重建窗口内读到的可能是半写状态。
   `WINDOW_BRIEFING.md` §2 亦要求 MO2 + Skyrim 关闭才准动 loadorder。
   本审计全程未启动 MO2、未写 modlist，上述变动均来自 MO2 自身。

## 附录 B：本审计的证据来源

| 证据 | 位置 |
|---|---|
| 本包事实 | `reports/P00/00_SCOPE.md`、`01_MOD_INVENTORY.csv`、`data/p00_scope.json` |
| modlist 独立复算 | 全表 2250 行逐行重新解析（不复用 `p00_common.py`） |
| 旧缓存结构探查 | `3-p02-6-latex-repository\reports\_data\` |
| 旧审计覆盖面 | `E:\SkyrimAE\_archive\2026-09\` |
| 环境约定 | `E:\SkyrimAE\AGENTS.md`、`CLAUDE.md`、`MO2_排序规则手册.md` |
| 跨窗口事实 | `WINDOW_BRIEFING.md` |
