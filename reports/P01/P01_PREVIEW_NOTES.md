# P01_PREVIEW_NOTES.md — Item 8: shipped preview images, 09 scope (56 mods)

**ZLJ Wardrobe Collection · P01_HUMAN_CURATION_ASSISTANCE · read-only discovery**

| 项 | 值 |
|---|---|
| 扫描时刻 (local) | 2026-09-30 14:21:21 |
| 范围来源（只读） | `reports/P00_RERUN/01_MOD_INVENTORY.csv` (P00 冻结，未修改) |
| Mod 根目录 | `E:\SkyrimAE\mo2\mods` |
| Mod 总数 | 56 |
| 扫描到的候选预览图总数 | **3** |

## 0. 渲染声明（NO RENDERING）

> **本次没有做任何渲染，也没有尝试渲染。**
>
> 未启动 3DSMax、NifSkope、SSCS、任何 render 脚本或任何预览生成器。
> 本工具只做**文件系统只读遍历**（`os.walk` + `os.stat`），
> 记录 mods **已经自带**的图片文件路径。没有转换、没有复制、没有移动、没有改写。
>
> 没有为了补足画面而搭建渲染管线。**"没有预览图"是完全可接受的结果。**

## 1. 结论（先看这里）

| 指标 | 值 |
|---|---|
| 有候选预览图的 mod | **1 / 56** |
| **零预览图**的 mod | **55 / 56** |
| 候选图片文件总数 | 3 |
| 其中 Windows 图片查看器可直接打开（PNG/JPG…） | **3** |
| 其中 DDS（DDS 查看器才能看，OS 默认不显示） | 0 |
| 有 `fomod/` 目录的 mod | 0 |
| 有 `CalienteTools/BodySlide/` 的 mod | 53 |
| 被判为**贴图/源素材**而排除的图片 | 1384 |

**一句话结论：** 仅 **1 / 56** 个 mod 自带预览图，其中 **1 个**有 Windows 查看器可直接打开的 PNG/JPG；**55 个 mod 零预览图**。绝大多数 mod 需要靠文本证据评审。

## 2. 有预览图的 mod（逐条）

| # | MOD_ID | 预览数 | 类型 | 体积 | 最佳候选 | DDS? | 可直接看? |
|---|---|---|---|---|---|---|---|
| 1 | `静默代码·乳胶重制 — Silent Code - Latex Rework — 【服装·装备】【身体·物理】【来源·本地】` | 3 | `png(3)` | 1.99 MiB | `屏幕截图 2026-08-13 141920.png` | no | yes |

### 2.1 全部候选图逐张清单（共 3 张）

尺寸由**文件头解析**得出（PNG IHDR / JPEG SOFn），只读字节，**不解码像素、不渲染**。

| # | MOD_ID | 相对路径 | 像素 | 字节 | 类型 | 来源判定 |
|---|---|---|---|---|---|---|
| 1 | `静默代码·乳胶重制 — Silent Code - Latex Rework — 【服装·装备】【身体·物理】【来源·本地】` | `屏幕截图 2026-08-13 141920.png` | 1285x1137 | 854562 | named_preview | user-screenshot-name (Windows 截图默认命名，疑似使用者自截入游戏画面，非作者随包宣传图) |
| 2 | `静默代码·乳胶重制 — Silent Code - Latex Rework — 【服装·装备】【身体·物理】【来源·本地】` | `屏幕截图 2026-08-13 141748.png` | 1234x1407 | 769110 | named_preview | user-screenshot-name (Windows 截图默认命名，疑似使用者自截入游戏画面，非作者随包宣传图) |
| 3 | `静默代码·乳胶重制 — Silent Code - Latex Rework — 【服装·装备】【身体·物理】【来源·本地】` | `屏幕截图 2026-08-13 141812.png` | 895x1189 | 468166 | named_preview | user-screenshot-name (Windows 截图默认命名，疑似使用者自截入游戏画面，非作者随包宣传图) |

> **来源提示：** 上述 3 张里，文件名为 Windows 截图默认命名（`屏幕截图 …`）。
> 也就是说它们很可能是**使用者自己截的入游戏画面**，被丢在 mod 根目录，
> 而**不是**作者随 mod 附带的宣传图。对评审而言内容依然有效（确实是该服装的画面），
> 但**不能**据此认为该 mod 作者提供了正式 preview 图。

## 3. 零预览图的 mod（55 个）

- `Nyes Latex Pack AiO 1.3 (ReducedSize)`
- `Haley Black Suit PBR`
- `00 资源·H2135 披风物理补全 — H2135 Cloak SMP Physics`
- `MiscMods Stilettos Zwei 与 Eins — AnkleCut V2 Tall 3BA【更高靴筒·脚踝滑块】`
- `堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】`
- `堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】`
- `静默代码 — SSE Silent Code — 【服装·装备】【身体·物理】【来源·本地】`
- `Riley Heels — 【服装·护甲】`
- `MiscMods Stilettos Zwei 与 Eins — MiscMods Stilettos Zwei and Eins — 【来源·本地】`
- `FO4TOAEAngeli_Devices — 【来源·本地】`
- `EvilFall — 【来源·本地】`
- `SEXY 靴子-oneboot - 9DM — SEXY BOOTS-oneboot - 9DM — 【服装·护甲】【来源·本地】`
- `回归之夜高跟鞋 — SEXY BOOTS Returning Night Pumps — 【服装·护甲】【来源·本地】`
- `Latex Lover Corset 增强版 — Latex Lover Corset Plus — 【服装·护甲】【来源·本地】`
- `DD - Sunset Mystic SET — 【来源·本地】`
- `Nye的乳胶紧身衣和胸衣 2 — Nye's Latex Pack 2 — 【服装·护甲】【身体·物理】【系列·Nye】`
- `Nye的乳胶紧身衣和胸衣 — Nye's Latex Pack — 【服装·护甲】【身体·物理】【系列·Nye】`
- `Nye's Latex 服装 2 — Nye's Latex Outfit 2 — 【服装·护甲】【系列·Nye】`
- `SEXY 靴子-2B Wedding 靴子 [3BA] Edited — SEXY BOOTS-2B Wedding Boots [3BA] Edited — 【服装·装备】【体型·CBBE+3BA】【来源·本地】`
- `SEXY 靴子- Knee_Boots 3BA BodySlide — SEXY BOOTS- Knee_Boots 3BA BodySlide — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【预设·BodySlide】`
- `J3 Latex 3BA — 【服装·装备】【体型·CBBE+3BA】【来源·本地】`
- `紧身衣 — J3 Bodysuit 3BA — 【服装·装备】【身体·物理】【体型·CBBE+3BA】`
- `乳胶安杰莉 — SSEDDAngeli 3BA — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】`
- `Brastia Catwoman TAS for 3BA — 【服装·装备】【体型·CBBE+3BA】`
- `Brastia Battle Princess Spandexer for 3BA — 【战斗·技能】【体型·CBBE+3BA】`
- `矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】`
- `Vertigo Thigh High 靴子 - CBBE 3BA — Vertigo Thigh High Boots - CBBE 3BA — 【服装·装备】【体型·CBBE+3BA】`
- `Skimpy Assassin 服装 - BHUNP 3BBB - CBBE 3BBB — Skimpy Assassin Outfit - BHUNP 3BBB - CBBE 3BBB — 【服装·装备】【体型·多体型】`
- `SEXY 靴子-[Melodic] 4 Heels CBBE 3BA BodySlide SE — SEXY BOOTS-[Melodic] 4 Heels CBBE 3BA BodySlide SE — 【服装·装备】【身体·物理】`
- `Jennes Thigh 靴子- -BHUNP 3BBB- -CBBE 3BBB — Jennes Thigh Boots- -BHUNP 3BBB- -CBBE 3BBB — 【服装·装备】【体型·多体型】`
- `SSE_VRC_SOURYO_fix — 【来源·本地】`
- `SSE_VRC_Latex_Servant — 【来源·本地】`
- `SSE_Latex_Nun — 【来源·本地】`
- `SSE_Kakugo_LatexNun — 【来源·本地】`
- `makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】`
- `makaron-COSPLAY - AE_Toxic_Cat — 【服装·装备】【来源·本地】`
- `makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】`
- `makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】`
- `makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】`
- `makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】`
- `makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】`
- `AE_Vtaw_DarkNurse — 【来源·本地】`
- `AE_VRC_Bunny_Nurse — 【来源·本地】`
- `AE_HoodST — 【来源·本地】`
- `[Zap] Gantz Suit — 【来源·本地】`
- `[TRX] LatexWhitch — 【来源·本地】`
- `[Predator] Premium Laced LatexBodysuit — 【来源·本地】【系列·Predator】`
- `[Predator] 靴子 Pack 02 CBBE 3BA — [Predator] Boots Pack 02 CBBE 3BA — 【服装·装备】【体型·CBBE+3BA】【来源·本地】【系列·Predator】`
- `[Predator] Gynax Suit + Colors XXX BHUNP SE — 【体型·BHUNP】【来源·本地】【系列·Predator】`
- `[Predator] Latex Acessories 3BA SE — 【服装·装备】【体型·CBBE+3BA】【来源·本地】【系列·Predator】`
- `[Predator] Naughty Slave Harness 3 CBBE 3BA AE — 【体型·CBBE+3BA】【平台·AE】【系列·Predator】`
- `[Predator] Penitent Warrior CBBE 3BA AE — 【体型·CBBE+3BA】【平台·AE】【系列·Predator】`
- `[Predator] Provocative Bikini Harness + Colors 3BA SE — 【服装·装备】【体型·CBBE+3BA】【来源·本地】【系列·Predator】`
- `[Predator] Silicon Acessories CBBE 3BA AE — 【体型·CBBE+3BA】【平台·AE】【系列·Predator】`
- `[Predator] Slave Harness Chastity CBBE 3BA AE — 【体型·CBBE+3BA】【平台·AE】【系列·Predator】`

## 4. 可直接查看 (PNG/JPG) vs 仅 DDS

> **DDS 说明：** `.dds` 是 DirectDraw Surface，Windows 照片查看器**打不开**。
> 本次把 DDS 记为 `candidate_is_dds=yes`，并在下面单独列出，方便评审时知道哪些需要 DDS 查看器
> （或人工另存为 PNG）才能看。**本次没有做任何格式转换。**

### 4.1 有 PNG/JPG 等可直接查看文件的 mod（1 个）

- `静默代码·乳胶重制 — Silent Code - Latex Rework — 【服装·装备】【身体·物理】【来源·本地】` → `屏幕截图 2026-08-13 141920.png`

### 4.2 只有 DDS 候选的 mod（0 个）

_（无）_

## 5. 扫描方法（可复核）

命中条件（任一）：

1. **文件名命中**：`preview*`（含 `preview-1` / `preview0` / `preview 1`）、`screenshot*` / `screen shot*`、`截图` / `屏幕截图` / `预览` / `宣传图`、`promo*` / `cover` / `thumb*` / `photo` / `picture`。
2. **目录命中**：位于 `screenshots/` / `preview(s)/` / `docs/` / `documentation/` / `images/` / `img/` / `media/` / `gallery/` / `promo/` / `fomod/` 之下。
3. **BodySlide 预览资产**：mod 内存在 `CalienteTools/BodySlide/` 目录。

排除条件：`textures/` / `texture/` / `meshes/` / `materials/` / `shaders/` / `source/` / `src/` / `bak/` / `backup/` / `work/` 路径下的图片一律判为**贴图/源素材**，不计入预览图（本次共排除 1384 个）。

`*.osp / *.osd / *.xml / *.ini` 等文本文件中出现 `preview` 字样的**引用**另行单独统计，不作为图片计入（见第 7 节）。

## 6. FOMOD 情况

**56 个 mod 中没有任何一个带 `fomod/` 目录**——这些 mods 都不带 FOMOD 安装器，因此不存在 FOMOD 自带预览图的情况。

## 7. BodySlide 预览资产

- 56 个 mod 中带 `CalienteTools/BodySlide/` 的：**53** 个。
- 在 mod 的 `.osp / .osd / .xml / .ini / .json / .txt / .md` **文件内容**中出现 `preview` 字样的文件：**0** 个。
- **没有任何一个 `<previewPath>` 指向磁盘上真实存在的预览图**——BodySlide 在本机没有配图。
- 范围外的旁证（只读探查，**未写入任何东西**）：
  - `E:\SkyrimAE\Data\CalienteTools\` **不存在**——本机 BodySlide 数据目录不在游戏 Data 下。
  - MO2 的 `BodySlide 与服装 Studio — BodySlide and Outfit Studio` 工具 mod 里确实有 `CalienteTools/BodySlide/`，但其图片全部是 `res/images/` 下的**软件 UI 图标**（89 个，`AlphaBrush.png`、`greygrid.png` 之类），**没有服装预览图**。
  - 该工具 mod **不属于 09 范围**，仅作旁证记录，未写入本 CSV。
- 结论：**BodySlide 体系在本范围内不提供任何可用于评审的服装预览图。**

## 8. 判为"贴图/源素材"而排除的图片（提示，避免误当预览）

范围内共发现 1387 个 raster 图片文件，其中 1384 个位于贴图/源素材目录，未计入预览图。

典型样例：

- `Nyes Latex Pack AiO 1.3 (ReducedSize) :: textures\NyesLatexOutfit2\bodysuit\nyelatexbodysuit_Auburn_d.dds`
- `Nyes Latex Pack AiO 1.3 (ReducedSize) :: textures\NyesLatexOutfit2\bodysuit\nyelatexbodysuit_Blue_d.dds`
- `Nyes Latex Pack AiO 1.3 (ReducedSize) :: textures\NyesLatexOutfit2\bodysuit\nyelatexbodysuit_Brown_d.dds`
- `Haley Black Suit PBR :: textures\PBR\SSE_TFD_Haley_Black_Suit\PC_016_A_CMN_002_Head.dds`
- `Haley Black Suit PBR :: textures\PBR\SSE_TFD_Haley_Black_Suit\PC_016_A_CMN_002_Head_g.dds`
- `Haley Black Suit PBR :: textures\PBR\SSE_TFD_Haley_Black_Suit\PC_016_A_CMN_002_Head_n.dds`
- `堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 :: Textures\AE_CorruptedBodySuit\BootShoe.dds`
- `堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 :: Textures\AE_CorruptedBodySuit\BootSockLeather.dds`

## 9. 给评审板的使用建议

- 可直接打开的预览图仅集中在 1 个 mod（见 4.1），覆盖不足全范围。
- **不要**为此新建渲染管线。P01 的定位是人工辅助，不是产出图像。
- 若人工评审确实需要图，正确的下一步是**从 Nexus Mods / 作者主页取原图**（属于人工动作），而不是在本地跑渲染。

## 10. 只读合规声明

- 对 `E:\SkyrimAE\mo2\mods`、`E:\SkyrimAE\Data`、modlist、BodySlide 数据：**零写入**。
- P00 成果（`reports/P00/`、`reports/P00_RERUN/`、`data/P00/`、`tools/P00_RERUN/`）**全部保持冻结**，本轮只读取了 `reports/P00_RERUN/01_MOD_INVENTORY.csv`。
- 唯一写入：`reports/P01/P01_PREVIEW_INDEX.csv`、`reports/P01/P01_PREVIEW_NOTES.md`。
- 工具内置写保护 `assert_write_path()`，越界写入直接 `SystemExit`。

---

**P01 · item 8 · preview discovery complete · 1/56 mods carry previews · no rendering performed**
