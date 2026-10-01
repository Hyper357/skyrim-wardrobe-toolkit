# REUSABLE_TOOLS.md

**交接审计配套文件** · 审计日期 2026-09-29
**用途**：回答"哪些脚本/数据可以直接拿去用，哪些必须重写，哪些是陷阱"。

本文件**不含任何执行建议**，只做资产定级。执行顺序见 `NEXT_ACTION_PLAN.md`。

---

## 0. 三级定级标准

| 级别 | 含义 | 判定依据 |
|---|---|---|
| **A · 直接继承** | 已独立验证正确，可作为后续一切成果的地基 | 逐行/逐条重算过，数字对得上 |
| **B · 继承并修正** | 主体可靠，有已知且已定位的缺陷，改动范围小 | 缺陷有明确行号与根因 |
| **C · 谨慎复用** | 逻辑成熟但**作用域和时效对不上**，需先做适配层 | 覆盖的是旧世界，不是冻结 56 |
| **D · 陷阱** | 看着能用，实际不能用或极易误用 | 已实测证伪 |

---

## 1. A 级 —— 本 packet 内部，直接继承

### 1.1 `tools/p00_common.py`（11,000 B）★ 本工程最核心资产

| 函数 / 常量 | 作用 | 定级理由 |
|---|---|---|
| `read_modlist()` | 读 modlist，`utf-8-sig` + `newline=""` + 手工剥 CRLF | 正确处理了本机 3 个已知陷阱（无 BOM UTF-8 / CRLF / 中文） |
| `section_of()` | 归属"行号比 L 大的最近分隔符" | 已对全表 2250 行逐行独立复现，**56/56 无例外** |
| `resolve_scope()` | 解析目标分隔符的区间 | 正确。命中不唯一时会直接 `SystemExit` 而非静默取第一个 |
| `ModlistEntry` | 剥离 `+`/`-`/`#` 状态前缀 | 正确 |
| `iter_files()` | 确定性遍历（`dirnames.sort()` + `sorted(filenames)`） | 顺序稳定，是幂等的前提 |
| `body_tokens()` / `classify_body()` | 体型分类器 | **设计上是对的**：token 化匹配，避免 `3BA` 误配进 `3BBB`、避免 `CBBE+3BA` 被读成含 BHUNP |
| `GENERIC_TAGS` | 把 `【体型·多体型】` 当无效证据继续回退 | 符合"不得猜测"的要求 |
| `TARGET_SEPARATOR` | 范围锚点 | 正确（不带 `+`/`-`） |
| 路径常量 | `MODLIST` / `MODS_DIR` / `GAME_DATA` | 换机器只改这一处，设计合理 |

> **一句提醒**：`section_of()` 是 O(n²)（对每行遍历全部分隔符）。全表 2250 行跑一次约
> 百万次比较，0.5 秒内可完成，**当前规模不需要优化**。不要提前重构。

### 1.2 `data/p00_scope.json`（10,959 B）

含 `modlist_sha256` / `modlist_lines` / `modlist_mtime` / 范围边界 / 56 条成员表 / 31 项命中表。
**作用**：后续每一份成果的 provenance 锚点 —— 出问题时要能证明"我是基于哪一份 modlist 算的"。

### 1.3 `01_MOD_INVENTORY.csv` 的两列

`mod_name` 与 `mo2_priority` **均已验证唯一**，可直接充当 `MOD_ID` 的天然主键，
无需另起编号（见 §5）。

---

## 2. B 级 —— 继承并修正

### 2.1 `tools/p00_s1_scope.py`（22,722 B）

| 项 | 状态 |
|---|---|
| 写入隔离 | ✅ 只有 3 处 `open(..., "w")`，全部指向 `data\` 与 `reports\P00\`。**无任何一处指向 `mo2\` 或 `Data\`** |
| 幂等性 | ✅ 已实测：相邻两次运行 `01_MOD_INVENTORY.csv` **SHA256 完全相同**；`00_SCOPE.md` / `p00_scope.json` 仅时间戳 1 行不同 |
| 只读性 | ✅ 实测扫描窗口内 `mo2\profiles` + `mo2\mods` + `Data` + `mo2\plugins` 共 19,262 文件被修改数 = 0 |
| **缺陷 1** | 🔴 `bs_slidersets` 恒为 0（`p00_s1_scope.py:183-187` 只认 `.xml`，实际是 `.osp`，漏 176 文件 / 52 Mod） |
| **缺陷 2** | `n_fomod`（`:39`）声明后无任何自增语句，死列 |
| **缺陷 3** | `scan_mod()` 里 `plugin_files` 先用 `rec.get(...)+` 累加再整体覆盖（`:118` vs `:198`），逻辑冗余但结果正确 |
| **缺陷 4** | `.ini` 的 SPID / KID / BOS 是 `elif` 链（`:147-152`），一个文件同时含 KID 和 SPID 时只记前者 |
| 环境副作用 | 导入会生成 `tools\__pycache__\`。原交付包内没有该目录（原作者应已清理或用了 `-B`），复现时注意 |

### 2.2 建议的最小修正（**尚未执行，等你指令**）

```python
# p00_s1_scope.py:183-187
elif low.startswith("calientetools/bodyslide/slidersets/"):
    if ext in (".xml", ".osp"):              # ← 加 .osp
        set_names.add(os.path.splitext(base)[0])   # ← 原 base[:-4] 对 .osp 会截错
        rec["bs_slidersets"] += 1
        rec["bs_total"] += 1
```

**已验证不会带来的副作用**：29 个 UNKNOWN 的判定结果**一个都不变**，
5 个 `bodyslide_assets` 判定也**全部不变**（OSP 文件名里没有体型 token）。
所以这个修正与"体型怎么判"完全解耦，可以独立推进。

**连带要改的文档**：`00_SCOPE.md:150` 的 SliderSets 注释、`交付说明.md:13` 的"49 列"。

---

## 3. C 级 —— 兄弟工程的存活资产，谨慎复用

来源：`E:\SkyrimAE\opencode工作目录\3-p02-6-latex-repository\reports\`

### 3.1 9 段式扫描管线（`_scripts\`，13 个 .py，共约 138 KB）

比本包的 `p00_s1_scope.py` 成熟得多 —— 它有真正的解析能力，而不只是计数。

| 脚本 | 职责 | 对本工程的价值 |
|---|---|---|
| `audit_common.py` | 共享常量 + **MO2 虚拟 FS 模型** | ★★★ 直接可作 `p00_common.py` 的补充 |
| `stage1_index.py` | MO2 虚拟文件系统只读索引 | ★★★ |
| `stage2_bsa.py` | BSA / BA2 成员索引 | ★★ → 17 |
| `stage3_plugins.py` | 解析每个插件副本的 ARMO / ARMA | ★★★ → 02 / 03 |
| `stage4_inventory.py` | 范围内 mod 资产盘点 | ★★ |
| `stage5_nif.py` + 两个 child | **解析范围内每一个松散 NIF** | ★★★ → 04 / 05 / 08 |
| `stage6_bodyslide.py` | BodySlide 工程 / 输出审计 | ★★★ → 07 |
| `stage7_model.py` | Armor → ArmorAddon → NIF 图 | ★★★ → 03 / 14 |
| `stage8_report.py` | 依赖分类 + 报告写出 | ★★ |
| `stage9_metrics.py` | 叙述性报告写出 | ★★ |

**复用前必须做的一件事**：把它们的 scope 常量从"旧 233 mod / 09 块 69 条"
改成"当前 modlist 解析出的 56 条"，并**全部改成按 mod 名 join**。

### 3.2 数据缓存（`_data\`）

| 文件 | 规模 | 读取方式 | 价值 |
|---|---|---|---|
| `nif_parsed\chunk_0000..0022.json.gz` | 6,732 个已解析 NIF | JSON，键 = `mod名\|\|相对路径` | ★★★ |
| `index_loose.pkl.gz` | **417,896** 条 VFS 索引 | **gzip + pickle** | ★★★ |
| `armature.json.gz` | **47,791** 条 ARMO 记录 | **gzip + pickle（扩展名撒谎）** | ★★★ |
| `bodyslide_projects.json.gz` | 4,540 个 BodySlide 工程 | JSON list | ★★★ |
| `plugins_index.json.gz` | 1,837 插件 → prio/mod/sha256 | **gzip + pickle（扩展名撒谎）** | ★★★ |
| `model_graph.json.gz` | ARMO→ARMA→NIF 图 + 覆盖 sha256 | JSON dict | ★★★ |
| `bsa_index.pkl.gz` | BSA 成员索引 | gzip + pickle | ★★ |
| `bodyslide_osp_providers.json.gz` | **870 个 `.osp` 归属** | JSON dict | ★★★ |
| `scope_assets.json.gz` | 233 mod 逐 mod 资产统计 | JSON dict | ★★ |
| `analysis_summary.json` | 汇总 | JSON | ★★ |

`nif_parsed` 每条 value 的结构（本审计实测）：

```json
{"shapes": [{"name": "3BA", "type": "BSTriShape",
             "shader": "BSLightingShaderProperty",
             "skin": "BSDismemberSkinInstance",
             "alpha": false,
             "partitions": ["SBP_32_BODY"],
             "n_bones": 49,
             "textures": {"Diffuse": "...", "Normal": "...", ...}}]}
```

**这是真解析，不是字符串猜测** —— 决策 3 要求的证据类型在这里是现成的。

### 3.3 `_archive\2026-09\` 下的旧审计

| 文件 | 行数 | 覆盖冻结 56 | 备注 |
|---|---|---|---|
| `BODyslide_AUDIT\02_ALL_PROJECTS.csv` | 4,487 | **51/56** | ★★★ **有 `osp` 列且 100% 填充**，还有 `status`（PREBUILT_ONLY / GENERATED_CONFIRMED / …） |
| `ASSET_OPTIMIZATION_AUDIT\03_MOD_EFFECTIVENESS.csv` | 2,198 | **55/56** | ★★★ 逐 mod 覆盖/遮蔽判定 |
| `OUTFIT_FORENSIC_AUDIT\04_BODyslide_PROJECT_RUNTIME_MAP.csv` | 8,723 | 28/56 | ★★ |
| `OUTFIT_FORENSIC_AUDIT\03_ARMOR_PLUGIN_MODEL_MAP.csv` | 14,513 | 14/56 | ★★ |

### 3.4 ⚠️ C 级的三条硬约束（**复用前必读**）

1. **行号一律失效。** 3 号的 09 块 = 69 条 / L879–947，现为 56 条 / L879–934。
   69 条里只有 **4 条**在当前 modlist 同一行号对得上。
   **任何 join 必须用 mod 名，绝不能用 line。**
2. **作用域是 233 mod 的旧世界。** 55/56 命中；唯一落空的是
   **`Nyes Latex Pack AiO 1.3 (ReducedSize)`** —— 18:29 之后才插入 modlist 第 879 行，
   是本范围最大的单个 mod（533.6 MiB / 218 文件），**在所有旧缓存里零覆盖**。
   它必须由新扫描器亲自处理。
3. **没有 ZLJ 污染。** 四份旧 CSV 中含 `ZLJ` 的行 = **0**；`mods_enabled.json` 条目 = 0。
   原因自洽：ZLJ 材质库 18:29 才被 `_zlj_enable.py` 拉起，晚于所有旧审计的运行时间。
   **旧数据描述的是"胶乳库出现之前"的世界，结构可信。**

---

## 4. D 级 —— 陷阱

| 资产 | 为什么是陷阱 |
|---|---|
| `_data\mods_enabled.json` | **实测条目数 = 0**。名字看着像权威清单，实际是空的。 |
| `_data\parse_validation.txt` | 0 字节。 |
| `_data\scan_index.log`、`bsa_scan_stats.txt` | 日志碎片，无结构。 |
| `LATEX_LIBRARY_*`、`P02_6_FINAL_REPOSITORY_REPORT.md`、`RECYCLE_BIN_INVENTORY.csv` | 描述的是**已灭失**的 ZLJ 材质库。方法论可参考，**事实已失效**。 |
| `armature.json.gz`、`plugins_index.json.gz` | 扩展名是 `.json`，**内容是 pickle**。按 JSON 读会直接 `UnicodeDecodeError`（本审计已实测踩到）。 |
| `交付说明.md:13` 的"49 列" | 实为 47 列。 |
| `交付说明.md:54` 的"913 个 Mod" | 当前盘面不可复现（反向规则实测 = 129）。历史轶事，不承重。 |
| `_decoupled_build\_work\`（110+ 文件） | 3 号工程内部中间产物，与本工程无契约。仅 `L4_plan.json.gz` / `L1_refs.json.gz` 可能有残余价值。 |
| `WINDOW_BRIEFING.md` 对 3 号的判断 | "不可重建"只对**材质库**成立；缓存与管线仍可用（见 §3）。 |

---

## 5. ID 体系：现状与兼容方案

### 5.1 现状

**全盘检索确认：现有成果中不存在任何 `_id` 结尾的列。**
`01_MOD_INVENTORY.csv` 的 47 列里没有 `MOD_ID` / `PLUGIN_ID` / `NIF_ID` 等。

**好消息是这反而降低了迁移成本** —— 没有历史编号需要兼容，
所以**不存在"重新编号导致旧报告失效"的风险**。

### 5.2 现成的稳定锚点

| 层级 | 已有锚点 | 唯一性 |
|---|---|---|
| MOD | `01_MOD_INVENTORY.csv` 的 `mod_name` | ✅ 56/56 唯一 |
| MOD | `mo2_priority`（modlist 行号） | ✅ 56/56 唯一，**但会随 modlist 改动漂移** |
| PLUGIN | 文件名（如 `NyesLatexPack-Devious.esp`） | ✅ 47 个全唯一（已实测） |
| RECORD | `armature.json.gz` 的 `formid` | ✅ 47,791 条，真 formid |
| RECORD | `armature.json.gz` 的 `EDID` 子记录 | 需查重后使用 |
| NIF | `nif_parsed` 的 `mod名\|\|相对路径` | ✅ 天然复合键 |

### 5.3 兼容方案（**提案，未执行**）

不要立刻重写历史数据。建议：

1. **`MOD_ID` 直接取 `mod_name` 原值**，不新造编号。
   理由：它是 MO2 里的真实文件夹名，唯一、稳定、且与旧归档天然可 join。
   若嫌长，可另加 `MOD_KEY` = `modlist 行号`，但**只做辅助列，不做主键**。

2. **`NIF_ID` / `TEXTURE_ID` 取相对虚拟路径原值**（如
   `meshes\actors\...`），不做哈希、不做自增。
   理由：与 `index_loose.pkl.gz`、`NIF_TEXTURE_MAP.csv` 直接兼容。

3. **`PLUGIN_ID` 取小写文件名**（`nyeslatexpack-devious.esp`），大小写归一。

4. **`RECORD_ID` 取 `formid` 十六进制**（`04000801`），与 `model_graph.json.gz`
   的 `armo_formid` 字段同格式，可直接 join。

5. **`LOGICAL_OUTFIT_ID` / `PART_ID` / `BODyslide_PROJECT_ID` 尚无对应物** ——
   这三个是业务概念，需要在 04 / 07 出表时随定义一起产生，**现在不要预造**。

> 一句话：**先复用真实标识符做 ID，不要造序号。** 造序号会在 modlist 一变动时全线失效。

---

## 6. 环境与运行前提

| 项 | 值 |
|---|---|
| Python | 3.14.6（`python`） |
| 阶段一依赖 | 纯标准库 |
| `PyNifly` | **未安装** —— 阶段 05 做 NIF 几何解析前需要装，或改用自写 NIF 头解析器 |
| 本机铁律 | 游戏锁死 1.6.1170 + SKSE 2.2.6 |
| modlist 陷阱 | 无 BOM 合法 UTF-8；PowerShell 直读会乱码，`Test-Path` 会误报 2173 个名字"缺失"。**任何 modlist 结论必须用 Python 复核** |
| 写入边界 | 本 packet 只写自己的 `data\` / `reports\` / `tools\` |

---

## 7. 一句话总结

> `p00_common.py` 是可信地基，`p00_s1_scope.py` 可用但有一条瘸腿（`.osp`），
> 兄弟工程的 9 段管线 + `_data` 缓存是**尚未被本工程接管的宝藏**
> （含决策 3 所需的全部证据类型），但必须先做"按名字 join + 排除 L879 新 mod"的适配层。
> 真正不能信的是 `mods_enabled.json`、所有 `ZLJ 材质库` 相关报告，以及两个撒谎的文件扩展名。
