# skyrim-wardrobe-toolkit

> Skyrim AE 服装/装备合集的**只读审计 → 筛选 → 迁移 → 风格一致化**工具链
>
> A read-only audit, curation, migration and style-unification toolchain for
> Skyrim AE outfit &amp; wardrobe mod collections.

面向 **Skyrim mod 玩家与改模者**：当你的 MO2 里堆了几百上千个服装 mod，
想知道"我到底有什么、哪些重复、哪些冲突、哪套能改成统一风格"时用得上。

---

## 这是什么

一个**证据驱动**的脚本工具链 + 操作手册，处理三件事：

| 问题 | 回答方式 |
|---|---|
| **我有什么？** | 扫描 modlist / 插件 / NIF / DDS / BodySlide 工程，产出可核对的 CSV 清单 |
| **哪些能用、哪些冲突？** | ARMOR/ARMA 映射、插槽分区、DIY 零件兼容性矩阵、MO2 冲突图 |
| **怎么改成统一风格？** | NIF 材质逐项对齐 + 贴图重制 + 接缝校验（见 [`docs/服装风格一致化·操作手册.md`](docs/服装风格一致化·操作手册.md)） |

**它不是**：资源整合包、一键安装器、或任何形式的模组分发。
仓库里**不含任何第三方游戏资源**，只有脚本、报告与文档。

---

## 设计原则

### 1. 只读保证（不是靠自觉，是没实现）

所有扫描脚本对游戏目录**零写入**。写入目标被限制在本工程目录内：

```
tools\    <- 脚本
data\     <- 中间 JSON 证据
reports\  <- 交付报告
```

脚本里**没有任何 `open(..., "w")` 指向 `mo2\` 或 `Data\`**。
"改 Mod / 改插件 / 跑 BodySlide / 改 modlist / merge / 删文件" 这些动作
**根本没有被实现** —— 不是约定，是代码里不存在。

复核方式：记录 modlist 的 SHA256，扫描前后比对，并对 mod 文件数做漂移检查。

### 2. 证据驱动，不靠猜

判定不出来就标 `UNKNOWN` 并写清"需要哪个阶段的什么证据才能定论"，
**不填默认值**。例如体型判定：文件夹名没有 `【体型】` 标签、BodySlide 工程名也没有
体型 token 的，一律挂起等 ShapeData/骨架解析，不用启发式蒙一个。

### 3. 幂等 + 可自检

重复运行覆盖同名产物，无累积副作用。每个扫描器都会打印解析结果（范围、命中数），
可当场核对——因为**最容易出错的地方是"规则读反了"**，而不是脚本崩了。

---

## 流水线阶段

```
P00  审计       扫描与盘点，产出证据链             ✅
 ├─ P00_RERUN/  17 份报告（mod/插件/NIF/DDS/       ✅
 │              材质分类/DIY 矩阵/冲突图…）
P01  筛选       人审看板、门禁、漂移检查            ✅
P02A 迁移设计   逐套装迁移清单（CL01–CL11）        ✅
P02B 构建执行   隔离构建、加载测试、预发布门禁      ✅
```

### P00 扫描范围（示例，本机）

MO2 分隔符 `09 特殊服装与NSFW 装备` 之下：

```
56 个 Mod  ·  3,708 文件  ·  18.04 GiB
46 esp + 1 esl  ·  1,316 NIF  ·  1,355 DDS  ·  1,055 BodySlide 文件
```

全盘检索基准：464,093 个文件。

### P00_RERUN 报告

| 报告 | 内容 |
|---|---|
| `01_MOD_INVENTORY` | Mod 级盘点 |
| `02_PLUGIN_RECORDS` | 插件记录 |
| `03_ARMOR_ARMA_MAP` | 护甲 ↔ 模型映射 |
| `04_PARTS_CATALOG` | DIY 零件目录 |
| `05_SLOT_PARTITION_MAP` | 插槽分区 |
| `06_DIY_COMPATIBILITY_MATRIX` | DIY 兼容性矩阵（最大，97 MB） |
| `07_BODYSLIDE_PROJECTS` | BodySlide 工程索引 |
| `08_NIF_INVENTORY` | NIF 清单（含 BSTriShape 名） |
| `09_NIF_TEXTURE_MAP` | NIF ↔ 贴图引用图 |
| `10_TEXTURE_INVENTORY` | 贴图盘点 |
| `11_MATERIAL_CLASSIFICATION` | 材质分类 |
| `12_DUPLICATE_ASSETS` | 重复资源 |
| `13_MO2_CONFLICT_MAP` | MO2 覆盖冲突 |
| `14_CROSS_MOD_DEPENDENCIES` | 跨 mod 依赖 |
| `15_REWORK_RELATIONSHIPS` | 重制关系 |
| `16_PBR_CURRENT_STATE` | PBR 现状 |
| `17a_EXTERNAL_REFERENCES_BY_FILE` | 外部引用 |

---

## 目录结构

```
.
├── README.md                      本文件
├── docs/
│   └── 服装风格一致化·操作手册.md    ★ 手工改造装备的完整流程与避坑指南
├── tools/
│   ├── p00_common.py               路径常量 + MO2 优先级模型 + 体型分类器
│   ├── p00_s1_scope.py             P00 阶段一扫描器
│   ├── P00_RERUN/                  16 个脚本：NIF/DDS/插件/零件/材质/报告生成
│   └── P01/                        7 个脚本：门禁与漂移检查
├── data/                           中间 JSON 证据（含 modlist SHA256）
├── reports/
│   ├── HANDOFF/                    交接审计、可复用工具索引、下一步计划
│   ├── P00/  P00_RERUN/            审计报告
│   ├── P01/                        筛选报告与人审看板
│   ├── P02A/                       迁移清单（CL01–CL11）
│   └── P02B/                       构建与迁移执行报告
└── .gitignore
```

统计：**60 个 Python 脚本 · 101 份报告（59 CSV / 36 MD）**

---

## 快速上手

### 环境

```
Python 3.11+（P00_RERUN 在 3.14 上验证过）
```

依赖见 `tools/requirements.txt`。**扫描阶段只用标准库**；
NIF 几何解析需要 `PyNifly`，DDS 转换需要 `texconv`（可选）。

### 配置

**所有路径集中在两个文件的顶部常量里，换机器只改那一处：**

| 常量 | 本机示例 |
|---|---|
| `MO2_INSTANCE` | `E:\SkyrimAE\mo2` |
| `MO2_PROFILE` | `Default` |
| `MODLIST` | `<MO2>\profiles\Default\modlist.txt` |
| `MODS_DIR` | `<MO2>\mods` |
| `GAME_DATA` | `E:\SkyrimAE\Data` |
| `TARGET_SEPARATOR` | `09 特殊服装与NSFW 装备` |

### 跑一次范围扫描

```powershell
python tools\p00_s1_scope.py
```

幂等，覆盖 `data\p00_scope.json` 与 `reports\P00\` 下两份报告。
运行时会打印解析出的范围与命中数，**先核对再往下走**。

---

## ⚠️ 先读这条：MO2 优先级模型

**这是整个工具链最容易搞反、后果最大的一处。**

```
1. modlist.txt 是 MO2 左栏的【倒序】
   第 1 行 = 左栏最底一行 = 【最高】覆盖优先级
2. 分隔符是【标题】，成员排在标题【下方】
3. 合起来：行号 L 的 mod，归属于行号比 L 大、且最接近的那个分隔符
4. 分隔符 S 拥有的区间 = (下方最近分隔符的行号 + 1) … (S - 1)
5. + 启用   - 禁用   # 注释
6. VFS 冲突：从第 1 行往下扫，同一虚拟路径【第一个命中者胜出】
```

> **第 3 条读反，范围会多出几百个 mod。**
> 实测：正确读法是 56 个，读反了会变成 129 个（历史记录里还出现过 913 的误算）。
> 所以扫描器每次运行都会把解析结果打印出来，让你当场发现读反了。

---

## 风格一致化工作流

把某件装备改造成和"基准件"（比如全身紧身衣）同一个风格 —— 手套、靴子、外套、护甲步骤一样。

完整流程见 **[`docs/服装风格一致化·操作手册.md`](docs/服装风格一致化·操作手册.md)**，含：

- **文件地图**：BodySlide 源工程 / 构建产物 / 滑块文件，到底该改哪个
- **三层改造**：几何接续 → 材质（10 项）→ 贴图
- **14 条避坑速查表**
- **工具能力边界表**（PyNifly 能做什么、不能做什么）
- **命令速查**

### 三条最值钱的经验

1. **先确认"用户在看哪个文件"** —— BodySlide 源工程和构建产物是两个文件，
   改错了就是全部白干（本项目 80% 的返工来自这一条）
2. **先量，再改** —— 不要凭感觉判断"有没有变化"
3. **材质全属性对比，不要挑** —— 只比高光强度会漏掉高光颜色

### 材质对齐的 10 项清单

```
数值 8 项:  Glossiness · Shader_Type · Env_Map_Scale · Spec_Str ·
            Spec_Color · Soft_Lighting · Shader_Flags_1 · Shader_Flags_2
贴图 2 项:  EnvMap · EnvMask
```

> `Shader_Type = 0` 意味着**完全不采样环境贴图** —— 在无动态光源的预览里就是"发哑"。
> 高低光颜色（`Spec_Color`）决定"高级胶质感"还是"廉价银器感"。

---

## 已知限制

- **路径硬编码在本机布局**（`E:\SkyrimAE\...`）。工具本身是通用的，
  但换机器需要改常量；没有做命令行参数化。
- **报告体积大**：`06_DIY_COMPATIBILITY_MATRIX.csv` 单文件 **97.4 MB**，
  逼近 GitHub 100 MB 硬上限。大 CSV 走 `.gitignore`，需要时本地重新生成。
- **`.osd` 滑块文件是二进制**，按"形状名 + 逐顶点权重"绑定。
  换了网格形状必须用 BodySlide / Outfit Studio 重新生成，脚本无法代劳。
- **PyNifly 的写入能力有限**：标量 ✅ / 贴图路径字符串 ❌ / 删除形状 ❌。
  详见操作手册 §7。
- 尚未做命令行参数化与自动化测试。

---

## 免责声明

- 本仓库**不包含任何第三方游戏资源**（模型、贴图、音频、插件）。
- 报告 CSV 中出现的 mod 名称与作者名，**仅用于索引与依赖分析**，
  版权归各自作者所有。
- 使用本工具链修改游戏文件前**请自行备份**。
  脚本本身对游戏目录只读，但**操作手册中描述的手工流程会写入文件**。

---

## License

MIT
