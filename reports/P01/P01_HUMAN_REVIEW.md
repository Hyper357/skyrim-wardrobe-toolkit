# P01 人工筛选表 / Human Curation Board

P00 已冻结。以下是把 P00 数据整理成的**人工决策包**。

**这里没有替你做决定。** 所有 `[ ]` 都没有勾选，`USER_DECISION` / `USER_PRIORITY` / `USER_NOTE` 全部留空。P01 不删除任何文件、不合并任何插件、不改任何资产。

## 怎么看这张表

| 字段 | 含义 |
|---|---|
| **大小** | 该 outfit 占用的大小（current = 磁盘，effective = MO2 实际保留）|
| **主要零件** | 折叠后的视觉零件（颜色变体 / 重复记录已合并），不是一条条 ARMO |
| **材质** | 从 11_MATERIAL_CLASSIFICATION 得到的材质候选 |
| **物理** | NONE / SMP / CBPC / MIXED / UNKNOWN |
| **技术成本** | LOW / MEDIUM / HIGH —— 依赖复杂度、body conversion、SMP、未解析引用、BodySlide 状态、跨 Mod 依赖综合而来，**不含审美** |
| **独特零件** | 只此一套有的零件（可单独留下）|
| **重复情况** | 与其它 outfit 重复的资产 |
| **依赖情况** | 跨 Mod 依赖与未解析引用 |

`KEEP` / `PARTIAL` / `DROP` 与 `S/A/B/C` 的含义：
S = 核心主角衣装，A = 强烈保留，B = 有价值，C = 可有可无。
这是你自己的衣柜优先级，工具不会替你填。

---

## 1. Nye的乳胶紧身衣和胸衣 — Nye's Latex Pack

- **Mod**：Nyes Latex Pack AiO 1.3 (ReducedSize)
- **插件**：NyesLatexPackAiO.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：533.6 MiB（MO2 实际保留 533.6 MiB）
- **规模**：ARMO 309　ARMA 309　可穿戴 mesh 24　贴图 97　有效 BodySlide 项目 24
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**HIGH**
- **重复资产**：14.8 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 156　未解析 0

主要零件：
- Nyes Latex Outfit2 Bodysuit　`BODYSUIT`　×15 变体，BodySlide
- Nyes Latex Outfit2 Bodysuit SLOT58　`BODYSUIT`　×15 变体
- Nyes Latex Outfit2 Transparent Bodysuit　`BODYSUIT`　×15 变体
- Nyes Latex Outfit2 Transparent Bodysuit SLOT58　`BODYSUIT`　×15 变体
- Nyes Latex Pack Latex Bodysuit　`BODYSUIT`　×15 变体，BodySlide
- Nyes Latex Pack Latex Boots　`BOOTS`　×15 变体
- Nyes Latex Pack Latex Corset　`CORSET`　×15 变体
- Nyes Latex Pack Latex Corset With Chains　`CORSET`　×15 变体
- …另有 35 个视觉零件
**可能的部分保留**：主体（Nyes Latex Outfit2 Bodysuit） + 独立配件 9 件 —— Nyes Latex Pack Latex 、Nyes Latex Pack Latex 、Nyes Latex Pack Latex 、Nyes Latex Pack2 Short、Nyes Latex Outfit2 Pla

**独特零件**（仅此一套）：Nyes Latex Outfit2 Bodys、Nyes Latex Outfit2 Corse、Nyes Latex Outfit2 Platf、Nyes Latex Outfit2 Trans

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 2. makaron-COSPLAY - AE_TFD_Haley_Black_Suit

- **Mod**：Haley Black Suit PBR,  makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】
- **插件**：SSE_TFD_Haley_Black_Suit.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：439.8 MiB（MO2 实际保留 439.7 MiB）
- **规模**：ARMO 13　ARMA 16　可穿戴 mesh 10　贴图 55　有效 BodySlide 项目 1
- **材质**：LATEX; LEATHER; METAL
- **PBR**：FAKE_METALLIC_LATEX+PBRNIFPATCHER_RULES
- **技术成本**：**N/A（无 ARMO 记录）**
- **重复资产**：68.1 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 181　未解析 0

**该 outfit 在范围内没有任何 ARMO 记录。**P00 已判定这类 Mod 只提供贴图 / mesh / physics / config，不是独立衣装本体。是否保留取决于它是否为其它套装提供素材。

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 3. 00 资源·H2135 披风物理补全 — H2135 Cloak SMP Physics

- **Mod**：00 资源·H2135 披风物理补全 — H2135 Cloak SMP Physics
- **插件**：NONE
- **体型**：UNKNOWN　**物理**：UNKNOWN
- **大小**：85 KiB（MO2 实际保留 85 KiB）
- **规模**：ARMO 0　ARMA 0　可穿戴 mesh 0　贴图 0　有效 BodySlide 项目 0
- **材质**：UNKNOWN
- **PBR**：NONE
- **技术成本**：**N/A（无 ARMO 记录）**
- **重复资产**：0 B　**合并风险**：NONE
- **依赖**：跨 Mod 0　未解析 0

**该 outfit 在范围内没有任何 ARMO 记录。**P00 已判定这类 Mod 只提供贴图 / mesh / physics / config，不是独立衣装本体。是否保留取决于它是否为其它套装提供素材。

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 4. MiscMods Stilettos Zwei 与 Eins — MiscMods Stilettos Zwei and Eins

- **Mod**：MiscMods Stilettos Zwei 与 Eins — AnkleCut V2 Tall 3BA【更高靴筒·脚,  MiscMods Stilettos Zwei 与 Eins — MiscMods Stilettos Zwei an
- **插件**：NONE
- **体型**：UNKNOWN　**物理**：UNKNOWN
- **大小**：16.4 MiB（MO2 实际保留 16.4 MiB）
- **规模**：ARMO 0　ARMA 0　可穿戴 mesh 4　贴图 0　有效 BodySlide 项目 4
- **材质**：UNKNOWN
- **PBR**：NONE
- **技术成本**：**N/A（无 ARMO 记录）**
- **重复资产**：0 B　**合并风险**：NONE
- **依赖**：跨 Mod 12　未解析 0

**该 outfit 在范围内没有任何 ARMO 记录。**P00 已判定这类 Mod 只提供贴图 / mesh / physics / config，不是独立衣装本体。是否保留取决于它是否为其它套装提供素材。

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 5. 堕落紧身衣 — AE Corrupted Body Suit

- **Mod**：堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】,  堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA
- **插件**：AE_CorruptedBodySuit.esp
- **体型**：CBBE_3BA　**物理**：CBPC
- **大小**：138.0 MiB（MO2 实际保留 106.8 MiB）
- **规模**：ARMO 6　ARMA 9　可穿戴 mesh 10　贴图 22　有效 BodySlide 项目 4
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**N/A（无 ARMO 记录）**
- **重复资产**：8.2 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 212　未解析 0

**该 outfit 在范围内没有任何 ARMO 记录。**P00 已判定这类 Mod 只提供贴图 / mesh / physics / config，不是独立衣装本体。是否保留取决于它是否为其它套装提供素材。

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 6. 堕落紧身衣 — AE Corrupted Body Suit

- **Mod**：堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA】
- **插件**：AE_CorruptedBodySuit.esp
- **体型**：CBBE_3BA　**物理**：CBPC
- **大小**：66.1 MiB（MO2 实际保留 34.8 MiB）
- **规模**：ARMO 6　ARMA 9　可穿戴 mesh 10　贴图 10　有效 BodySlide 项目 4
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**HIGH**
- **重复资产**：2.2 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 100　未解析 0

主要零件：
- Corrupted Suit Feet　`BODY`　×2 变体，BodySlide
- Corrupted Suit Glove　`GLOVES`　BodySlide
- Corrupted Suit Head　`BODY`　BodySlide
- Corrupted Suit Mask　`MASK`　BodySlide
- Corrupted Suit Neck　`BODY`　—
**可能的部分保留**：主体（Corrupted Suit Feet） + 独立配件 2 件 —— Corrupted Suit Glove、Corrupted Suit Mask

**独特零件**（仅此一套）：Corrupted Suit Neck

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 7. 静默代码 — SSE Silent Code

- **Mod**：静默代码·乳胶重制 — Silent Code - Latex Rework — 【服装·装备】【身体·物理】【来源·本,  静默代码 — SSE Silent Code — 【服装·装备】【身体·物理】【来源·本地】
- **插件**：SSE_Silent_Code.esp
- **体型**：CBBE_3BA　**物理**：CBPC
- **大小**：2.05 GiB（MO2 实际保留 1.51 GiB）
- **规模**：ARMO 63　ARMA 66　可穿戴 mesh 24　贴图 184　有效 BodySlide 项目 7
- **材质**：TRANSPARENT
- **PBR**：NONE
- **技术成本**：**N/A（无 ARMO 记录）**
- **重复资产**：30.4 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 564　未解析 0

**该 outfit 在范围内没有任何 ARMO 记录。**P00 已判定这类 Mod 只提供贴图 / mesh / physics / config，不是独立衣装本体。是否保留取决于它是否为其它套装提供素材。

**预览图**：E:\SkyrimAE\mo2\mods\静默代码·乳胶重制 — Silent Code - Latex Rework — 【服装·装备】【身体·物理】【来源·本地】\屏幕截图 2026-08-13 

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 8. 静默代码 — SSE Silent Code

- **Mod**：静默代码 — SSE Silent Code — 【服装·装备】【身体·物理】【来源·本地】
- **插件**：SSE_Silent_Code.esp
- **体型**：CBBE_3BA　**物理**：CBPC
- **大小**：1.57 GiB（MO2 实际保留 1.03 GiB）
- **规模**：ARMO 63　ARMA 66　可穿戴 mesh 24　贴图 120　有效 BodySlide 项目 7
- **材质**：TRANSPARENT
- **PBR**：NONE
- **技术成本**：**HIGH**
- **重复资产**：10.9 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 564　未解析 0

主要零件：
- Silent Code Body01 T　`BODY`　×2 变体，BodySlide
- Silent Code Body02　`BODY`　×2 变体，BodySlide
- Silent Code Body03　`BODY`　×2 变体，BodySlide
- Silent Code Body04　`BODY`　×2 变体，BodySlide
- Silent Code Coat01　`COAT`　×2 变体，BodySlide
- Silent Code Coat02　`COAT`　×2 变体，BodySlide
- Silent Code Mask01 Erin　`MASK`　×2 变体，BodySlide
- Silent Code Mask02　`MASK`　×2 变体，BodySlide
- …另有 47 个视觉零件
**可能的部分保留**：主体（Silent Code Body01 T） + 独立配件 15 件 —— Silent Code Mask01 Eri、Silent Code Mask02、Silent Code Glove01、Silent Code Glove02、Silent Code Glove03

**独特零件**（仅此一套）：Silent Code Armor01、Silent Code Armor02、Silent Code Armor03、Silent Code Armor04

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 9. Riley Heels

- **Mod**：Riley Heels — 【服装·护甲】
- **插件**：RileyHeels.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：69.0 MiB（MO2 实际保留 69.0 MiB）
- **规模**：ARMO 10　ARMA 10　可穿戴 mesh 1　贴图 0　有效 BodySlide 项目 1
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**HIGH**
- **重复资产**：0 B　**合并风险**：HIGH
- **依赖**：跨 Mod 11　未解析 0

主要零件：
- rileyheels　`HEELS`　×4 变体，BodySlide
- rileyheels Suede　`HEELS`　×3 变体，BodySlide
- rileyheels Matte　`HEELS`　×2 变体，BodySlide
- rileyheels Violet　`HEELS`　BodySlide
> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 10. MiscMods Stilettos Zwei 与 Eins — MiscMods Stilettos Zwei and Eins

- **Mod**：MiscMods Stilettos Zwei 与 Eins — MiscMods Stilettos Zwei and
- **插件**：NONE
- **体型**：UNKNOWN　**物理**：UNKNOWN
- **大小**：11.6 MiB（MO2 实际保留 11.6 MiB）
- **规模**：ARMO 0　ARMA 0　可穿戴 mesh 2　贴图 0　有效 BodySlide 项目 2
- **材质**：UNKNOWN
- **PBR**：NONE
- **技术成本**：**N/A（无 ARMO 记录）**
- **重复资产**：0 B　**合并风险**：NONE
- **依赖**：跨 Mod 6　未解析 0

**该 outfit 在范围内没有任何 ARMO 记录。**P00 已判定这类 Mod 只提供贴图 / mesh / physics / config，不是独立衣装本体。是否保留取决于它是否为其它套装提供素材。

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 11. FO4TOAEAngeli_Devices

- **Mod**：FO4TOAEAngeli_Devices — 【来源·本地】
- **插件**：NONE
- **体型**：UNKNOWN　**物理**：CBPC
- **大小**：568.7 MiB（MO2 实际保留 568.7 MiB）
- **规模**：ARMO 0　ARMA 0　可穿戴 mesh 1　贴图 27　有效 BodySlide 项目 1
- **材质**：UNKNOWN
- **PBR**：NONE
- **技术成本**：**N/A（无 ARMO 记录）**
- **重复资产**：338 KiB　**合并风险**：NONE
- **依赖**：跨 Mod 0　未解析 0

**该 outfit 在范围内没有任何 ARMO 记录。**P00 已判定这类 Mod 只提供贴图 / mesh / physics / config，不是独立衣装本体。是否保留取决于它是否为其它套装提供素材。

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 12. EvilFall

- **Mod**：EvilFall — 【来源·本地】
- **插件**：NONE
- **体型**：UNKNOWN　**物理**：UNKNOWN
- **大小**：1.46 GiB（MO2 实际保留 1.46 GiB）
- **规模**：ARMO 0　ARMA 0　可穿戴 mesh 4　贴图 79　有效 BodySlide 项目 4
- **材质**：UNKNOWN
- **PBR**：NONE
- **技术成本**：**N/A（无 ARMO 记录）**
- **重复资产**：3.7 MiB　**合并风险**：NONE
- **依赖**：跨 Mod 0　未解析 0

**该 outfit 在范围内没有任何 ARMO 记录。**P00 已判定这类 Mod 只提供贴图 / mesh / physics / config，不是独立衣装本体。是否保留取决于它是否为其它套装提供素材。

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 13. SEXY 靴子-oneboot - 9DM — SEXY BOOTS-oneboot - 9DM

- **Mod**：SEXY 靴子-oneboot - 9DM — SEXY BOOTS-oneboot - 9DM — 【服装·护甲】【来
- **插件**：aboot.esp
- **体型**：UNKNOWN　**物理**：CBPC
- **大小**：36.6 MiB（MO2 实际保留 36.6 MiB）
- **规模**：ARMO 2　ARMA 1　可穿戴 mesh 2　贴图 6　有效 BodySlide 项目 1
- **材质**：METAL
- **PBR**：NONE
- **技术成本**：**MEDIUM**
- **重复资产**：0 B　**合并风险**：LOW_EASY
- **依赖**：跨 Mod 2　未解析 0

主要零件：
- abootam　`OTHER`　BodySlide
- abootam1　`OTHER`　BodySlide
> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 14. 回归之夜高跟鞋 — SEXY BOOTS Returning Night Pumps

- **Mod**：回归之夜高跟鞋 — SEXY BOOTS Returning Night Pumps — 【服装·护甲】【来源·本地】
- **插件**：Returning Night.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：113.9 MiB（MO2 实际保留 113.9 MiB）
- **规模**：ARMO 5　ARMA 5　可穿戴 mesh 10　贴图 19　有效 BodySlide 项目 7
- **材质**：LATEX; METAL
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：3.1 MiB　**合并风险**：MODERATE
- **依赖**：跨 Mod 3　未解析 0

主要零件：
- ex Pumps　`HEELS`　×5 变体，BodySlide
> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 15. Latex Lover Corset 增强版 — Latex Lover Corset Plus

- **Mod**：Latex Lover Corset 增强版 — Latex Lover Corset Plus — 【服装·护甲】【来
- **插件**：Latex Lover Corset Plus - DD.esp; Latex Lover Corset Plus.esp
- **体型**：CBBE_3BA　**物理**：CBPC
- **大小**：1.17 GiB（MO2 实际保留 1.17 GiB）
- **规模**：ARMO 177　ARMA 118　可穿戴 mesh 35　贴图 23　有效 BodySlide 项目 1
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：9.3 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 10　未解析 0

主要零件：
- Latex Lover Corset Plus Harness　`CORSET`　×4 变体
- Latex Lover Corset Plus　`CORSET`　×3 变体
- Latex Lover Corset Plus Arm Manacles　`CORSET`　×3 变体
- Latex Lover Corset Plus Binding Gloves　`CORSET`　×3 变体，BodySlide
- Latex Lover Corset Plus Body2　`CORSET`　×3 变体
- Latex Lover Corset Plus Body3　`CORSET`　×3 变体
- Latex Lover Corset Plus Boots　`CORSET`　×3 变体
- Latex Lover Corset Plus Eye Mask BH　`CORSET`　×3 变体
- …另有 68 个视觉零件
**独特零件**（仅此一套）：Latex Lover Corset Plus 、Latex Lover Corset Plus 、Latex Lover Corset Plus 、Latex Lover Corset Plus 

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 16. DD - Sunset Mystic SET

- **Mod**：DD - Sunset Mystic SET — 【来源·本地】
- **插件**：DD  -  Sunset mystic by Vergi.esp
- **体型**：UNKNOWN　**物理**：UNKNOWN
- **大小**：347.2 MiB（MO2 实际保留 347.2 MiB）
- **规模**：ARMO 3　ARMA 3　可穿戴 mesh 1　贴图 17　有效 BodySlide 项目 1
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：0 B　**合并风险**：LOW_EASY
- **依赖**：跨 Mod 7　未解析 0

主要零件：
- aaa Sunset Mystic Helmet　`OTHER`　BodySlide
- aaa Sunset Mystic Panties　`OTHER`　—
- aaa Sunset Mysticbody　`OTHER`　—
**独特零件**（仅此一套）：aaa Sunset Mystic Pantie、aaa Sunset Mysticbody

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 17. Nye的乳胶紧身衣和胸衣 — Nye's Latex Pack

- **Mod**：Nye的乳胶紧身衣和胸衣 2 — Nye's Latex Pack 2 — 【服装·护甲】【身体·物理】【系列·Nye】
- **插件**：NyesLatexPack2.esp
- **体型**：UNKNOWN　**物理**：UNKNOWN
- **大小**：163.6 MiB（MO2 实际保留 115.0 MiB）
- **规模**：ARMO 11　ARMA 11　可穿戴 mesh 0　贴图 0　有效 BodySlide 项目 0
- **材质**：UNKNOWN
- **PBR**：NONE
- **技术成本**：**MEDIUM**
- **重复资产**：4.7 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 41　未解析 0

主要零件：
- COLOUREDNyes Latex Pack2 Bandeau Leotard　`BODYSUIT`　—
- COLOUREDNyes Latex Pack2 Catsuit Sleeved Leota　`BODYSUIT`　—
- COLOUREDNyes Latex Pack2 Short Latex Gloves　`GLOVES`　—
- COLOUREDNyes Latex Pack2 Short Latex Skirt　`SKIRT`　—
- Nyes Latex Pack2 Bandeau Leotard　`BODYSUIT`　—
- Nyes Latex Pack2 Belt Corset　`CORSET`　—
- Nyes Latex Pack2 Catsuit Sleeved Leotard　`BODYSUIT`　—
- Nyes Latex Pack2 Latex Waist Corset　`CORSET`　—
- …另有 3 个视觉零件
**可能的部分保留**：主体（COLOUREDNyes Latex Pack2 Bande） + 独立配件 2 件 —— COLOUREDNyes Latex Pac、Nyes Latex Pack2 Short

**独特零件**（仅此一套）：COLOUREDNyes Latex Pack2、COLOUREDNyes Latex Pack2、COLOUREDNyes Latex Pack2、COLOUREDNyes Latex Pack2

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 18. Nye的乳胶紧身衣和胸衣 — Nye's Latex Pack

- **Mod**：Nye的乳胶紧身衣和胸衣 — Nye's Latex Pack — 【服装·护甲】【身体·物理】【系列·Nye】
- **插件**：NyesLatexPack.esp
- **体型**：UNKNOWN　**物理**：UNKNOWN
- **大小**：109.4 MiB（MO2 实际保留 65.6 MiB）
- **规模**：ARMO 14　ARMA 14　可穿戴 mesh 0　贴图 3　有效 BodySlide 项目 0
- **材质**：UNKNOWN
- **PBR**：NONE
- **技术成本**：**MEDIUM**
- **重复资产**：2.9 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 42　未解析 0

主要零件：
- COLOUREDNyes Latex Pack Latex Corset　`CORSET`　×2 变体
- Nyes Latex Pack Latex Corset　`CORSET`　×2 变体
- COLOUREDNyes Latex Pack Latex Bodysuit　`BODYSUIT`　—
- COLOUREDNyes Latex Pack Latex Boots　`BOOTS`　—
- COLOUREDNyes Latex Pack Latex Gloves　`GLOVES`　—
- COLOUREDNyes Latex Pack Latex High Heels　`HEELS`　—
- COLOUREDNyes Latex Pack Latex Unitard　`BODYSUIT`　—
- Nyes Latex Pack Latex Bodysuit　`BODYSUIT`　—
- …另有 4 个视觉零件
**可能的部分保留**：主体（COLOUREDNyes Latex Pack Latex ） + 独立配件 6 件 —— COLOUREDNyes Latex Pac、COLOUREDNyes Latex Pac、COLOUREDNyes Latex Pac、Nyes Latex Pack Latex 、Nyes Latex Pack Latex 

**独特零件**（仅此一套）：COLOUREDNyes Latex Pack 、COLOUREDNyes Latex Pack 、COLOUREDNyes Latex Pack 、COLOUREDNyes Latex Pack 

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 19. Nye的乳胶紧身衣和胸衣 — Nye's Latex Pack

- **Mod**：Nye's Latex 服装 2 — Nye's Latex Outfit 2 — 【服装·护甲】【系列·Nye】
- **插件**：NyesLatexOutfit2.esl
- **体型**：UNKNOWN　**物理**：UNKNOWN
- **大小**：103.1 MiB（MO2 实际保留 43.8 MiB）
- **规模**：ARMO 6　ARMA 6　可穿戴 mesh 0　贴图 1　有效 BodySlide 项目 0
- **材质**：UNKNOWN
- **PBR**：NONE
- **技术成本**：**LOW**
- **重复资产**：5.8 MiB　**合并风险**：LOW_EASY
- **依赖**：跨 Mod 28　未解析 0

主要零件：
- Nyes Latex Outfit2 Bodysuit　`BODYSUIT`　×2 变体
- Nyes Latex Outfit2 Transparent Bodysuit　`BODYSUIT`　×2 变体
- Nyes Latex Outfit2 Corset Version2　`CORSET`　—
- Nyes Latex Outfit2 Platform Boots　`BOOTS`　—
**可能的部分保留**：主体（Nyes Latex Outfit2 Bodysuit） + 独立配件 1 件 —— Nyes Latex Outfit2 Pla

**独特零件**（仅此一套）：Nyes Latex Outfit2 Corse、Nyes Latex Outfit2 Platf

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 20. SEXY 靴子-2B Wedding 靴子 [3BA] Edited — SEXY BOOTS-2B Wedding Boots [3BA] Edited

- **Mod**：SEXY 靴子-2B Wedding 靴子 [3BA] Edited — SEXY BOOTS-2B Wedding B
- **插件**：NONE
- **体型**：UNKNOWN　**物理**：UNKNOWN
- **大小**：8.6 MiB（MO2 实际保留 8.6 MiB）
- **规模**：ARMO 0　ARMA 0　可穿戴 mesh 1　贴图 0　有效 BodySlide 项目 1
- **材质**：UNKNOWN
- **PBR**：NONE
- **技术成本**：**N/A（无 ARMO 记录）**
- **重复资产**：0 B　**合并风险**：NONE
- **依赖**：跨 Mod 0　未解析 0

**该 outfit 在范围内没有任何 ARMO 记录。**P00 已判定这类 Mod 只提供贴图 / mesh / physics / config，不是独立衣装本体。是否保留取决于它是否为其它套装提供素材。

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 21. SEXY 靴子- Knee_Boots 3BA BodySlide — SEXY BOOTS- Knee_Boots 3BA BodySlide

- **Mod**：SEXY 靴子- Knee_Boots 3BA BodySlide — SEXY BOOTS- Knee_Boots 3
- **插件**：Knee_Boots.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：120.8 MiB（MO2 实际保留 120.8 MiB）
- **规模**：ARMO 20　ARMA 10　可穿戴 mesh 3　贴图 10　有效 BodySlide 项目 1
- **材质**：LATEX; METAL
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：2.7 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 28　未解析 0

主要零件：
- Knee Boots B　`BOOTS`　×2 变体，BodySlide
- Knee Boots BR　`BOOTS`　×2 变体，BodySlide
- Knee Boots R　`BOOTS`　×2 变体，BodySlide
- Knee Boots W　`BOOTS`　×2 变体，BodySlide
- Knee Boots Y　`BOOTS`　×2 变体，BodySlide
- Knee Boots2 B　`OTHER`　×2 变体
- Knee Boots2 BR　`OTHER`　×2 变体
- Knee Boots2 R　`OTHER`　×2 变体
- …另有 2 个视觉零件
> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 22. J3 Latex 3BA

- **Mod**：J3 Latex 3BA — 【服装·装备】【体型·CBBE+3BA】【来源·本地】
- **插件**：[J3] Latex.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：165.5 MiB（MO2 实际保留 165.5 MiB）
- **规模**：ARMO 27　ARMA 27　可穿戴 mesh 1　贴图 32　有效 BodySlide 项目 1
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**HIGH**
- **重复资产**：2.0 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 8　未解析 0

主要零件：
- J3 LBody　`BODY`　×2 变体
- J3 LBoots　`BOOTS`　×2 变体，BodySlide
- J3 LGloves　`GLOVES`　×2 变体
- J3 LPauldrons　`OTHER`　×2 变体
- J3 LBody Be　`BODY`　—
- J3 LBody Bet　`BODY`　—
- J3 LBody Bt　`BODY`　—
- J3 LBody Gr　`BODY`　—
- …另有 15 个视觉零件
**可能的部分保留**：主体（J3 LBody） + 独立配件 2 件 —— J3 LBoots、J3 LGloves

**独特零件**（仅此一套）：J3 LBody Be、J3 LBody Bet、J3 LBody Bt、J3 LBody Gr

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 23. 紧身衣 — J3 Bodysuit 3BA

- **Mod**：紧身衣 — J3 Bodysuit 3BA — 【服装·装备】【身体·物理】【体型·CBBE+3BA】
- **插件**：[J3] Bodysuit.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：102.0 MiB（MO2 实际保留 102.0 MiB）
- **规模**：ARMO 5　ARMA 5　可穿戴 mesh 1　贴图 10　有效 BodySlide 项目 1
- **材质**：UNKNOWN
- **PBR**：NONE
- **技术成本**：**HIGH**
- **重复资产**：0 B　**合并风险**：HIGH
- **依赖**：跨 Mod 5　未解析 0

主要零件：
- J3 Bodysuit　`BODYSUIT`　×2 变体，BodySlide
- J3 Bodysuit SM　`BODYSUIT`　—
- J3 Bodysuit TR　`BODYSUIT`　—
- J3 Bodysuit Uni　`BODYSUIT`　—
**独特零件**（仅此一套）：J3 Bodysuit SM、J3 Bodysuit TR、J3 Bodysuit Uni

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 24. 乳胶安杰莉 — SSEDDAngeli 3BA

- **Mod**：乳胶安杰莉 — SSEDDAngeli 3BA — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】
- **插件**：DDAngeli.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：884.7 MiB（MO2 实际保留 884.7 MiB）
- **规模**：ARMO 36　ARMA 39　可穿戴 mesh 39　贴图 52　有效 BodySlide 项目 3
- **材质**：LATEX; METAL; RUBBER
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：12.1 MiB　**合并风险**：LOW_EASY
- **依赖**：跨 Mod 5　未解析 0

主要零件：
- DDAngeli body01　`BODY`　BodySlide
- DDAngeli body01 Head　`OTHER`　—
- DDAngeli body01 NEck　`OTHER`　—
- DDAngeli body02　`BODY`　—
- DDAngeli body02 Back　`OTHER`　BodySlide
- DDAngeli body02 Feet　`OTHER`　—
- DDAngeli body02 Hand　`OTHER`　—
- DDAngeli body02 Head　`OTHER`　—
- …另有 28 个视觉零件
**独特零件**（仅此一套）：DDAngeli body01 Head、DDAngeli body01 NEck、DDAngeli body02、DDAngeli body02 Feet

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 25. Brastia Catwoman TAS for 3BA

- **Mod**：Brastia Catwoman TAS for 3BA — 【服装·装备】【体型·CBBE+3BA】
- **插件**：[Brastia] Catwoman 3BA.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：64.5 MiB（MO2 实际保留 64.5 MiB）
- **规模**：ARMO 5　ARMA 5　可穿戴 mesh 6　贴图 13　有效 BodySlide 项目 1
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：0 B　**合并风险**：MODERATE
- **依赖**：跨 Mod 2　未解析 0

主要零件：
- Catwoman Tasbodysuit　`BODYSUIT`　BodySlide
- Catwomantas Gloves　`GLOVES`　—
- Catwomantas Mask　`MASK`　—
- Catwomantasboots　`BOOTS`　—
- Catwomantaswhip　`OTHER`　—
**可能的部分保留**：主体（Catwoman Tasbodysuit） + 独立配件 3 件 —— Catwomantas Gloves、Catwomantas Mask、Catwomantasboots

**独特零件**（仅此一套）：Catwomantas Gloves、Catwomantas Mask、Catwomantasboots、Catwomantaswhip

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 26. Brastia Battle Princess Spandexer for 3BA

- **Mod**：Brastia Battle Princess Spandexer for 3BA — 【战斗·技能】【体型·CBBE+
- **插件**：[Brastia] Battle Princess Spandexer 3BA.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：543.3 MiB（MO2 实际保留 543.3 MiB）
- **规模**：ARMO 33　ARMA 33　可穿戴 mesh 36　贴图 35　有效 BodySlide 项目 1
- **材质**：LATEX; METAL; VINYL_PVC
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：1.9 MiB　**合并风险**：MODERATE
- **依赖**：跨 Mod 26　未解析 0

主要零件：
- SPBodysuit CA01　`BODYSUIT`　×2 变体
- SPBodysuit CA02　`BODYSUIT`　×2 变体
- SPBodysuit MA01　`BODYSUIT`　×2 变体
- SPBodysuit MA02　`BODYSUIT`　×2 变体
- SPBodysuit SA01　`BODYSUIT`　×2 变体
- SPBodysuit SA02　`BODYSUIT`　×2 变体
- SPBodysuitzr　`OTHER`　×2 变体
- SPCCape CA　`CAPE`　—
- …另有 18 个视觉零件
**可能的部分保留**：主体（SPBodysuit CA01） + 独立配件 14 件 —— SPGloves CA、SPGloves MA、SPGloves SA、SPGloveszr、SPboots CA

**独特零件**（仅此一套）：SPCCape CA、SPCCape MA、SPCCape SA、SPCCapezr

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 27. 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS

- **Mod**：矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】
- **插件**：BBD_CatsuitSpearhead.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：138.1 MiB（MO2 实际保留 138.1 MiB）
- **规模**：ARMO 24　ARMA 24　可穿戴 mesh 18　贴图 10　有效 BodySlide 项目 1
- **材质**：FABRIC; LATEX; METAL
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：46 KiB　**合并风险**：HIGH
- **依赖**：跨 Mod 39　未解析 0

主要零件：
- BBDCatsuita01t01 S　`OTHER`　×2 变体，BodySlide
- BBDCatsuita01t02　`OTHER`　×2 变体，BodySlide
- BBDCatsuith01t02　`OTHER`　×2 变体
- BBDCatsuitg01t01　`OTHER`　—
- BBDCatsuitg01t02　`OTHER`　—
- BBDCatsuitg02t01　`OTHER`　—
- BBDCatsuitg02t02　`OTHER`　—
- BBDCatsuitg04t01　`OTHER`　—
- …另有 13 个视觉零件
**独特零件**（仅此一套）：BBDCatsuitg01t01、BBDCatsuitg01t02、BBDCatsuitg02t01、BBDCatsuitg02t02

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 28. Vertigo Thigh High 靴子 - CBBE 3BA — Vertigo Thigh High Boots - CBBE 3BA

- **Mod**：Vertigo Thigh High 靴子 - CBBE 3BA — Vertigo Thigh High Boots 
- **插件**：Vertigo Boots.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：159.4 MiB（MO2 实际保留 159.4 MiB）
- **规模**：ARMO 12　ARMA 6　可穿戴 mesh 2　贴图 21　有效 BodySlide 项目 1
- **材质**：METAL
- **PBR**：NONE
- **技术成本**：**MEDIUM**
- **重复资产**：0 B　**合并风险**：HIGH
- **依赖**：跨 Mod 0　未解析 0

主要零件：
- Vertigo Boots　`BOOTS`　×12 变体，BodySlide
> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 29. Skimpy Assassin 服装 - BHUNP 3BBB - CBBE 3BBB — Skimpy Assassin Outfit - BHUNP 3BBB - CBBE 3BBB

- **Mod**：Skimpy Assassin 服装 - BHUNP 3BBB - CBBE 3BBB — Skimpy Assassi
- **插件**：BBD Skimpy Assassin Outfit.esp
- **体型**：MIXED　**物理**：UNKNOWN
- **大小**：200.6 MiB（MO2 实际保留 200.6 MiB）
- **规模**：ARMO 20　ARMA 23　可穿戴 mesh 2　贴图 26　有效 BodySlide 项目 1
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：0 B　**合并风险**：HIGH
- **依赖**：跨 Mod 0　未解析 0

主要零件：
- SAOBody　`BODY`　×5 变体
- SAOBoots　`BOOTS`　×5 变体，BodySlide
- SAOGloves　`GLOVES`　×5 变体
- SAOMask　`MASK`　×5 变体
**可能的部分保留**：主体（SAOBody） + 独立配件 3 件 —— SAOBoots、SAOGloves、SAOMask

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 30. SEXY 靴子-[Melodic] 4 Heels CBBE 3BA BodySlide SE — SEXY BOOTS-[Melodic] 4 Heels CBBE 3BA BodySlide SE

- **Mod**：SEXY 靴子-[Melodic] 4 Heels CBBE 3BA BodySlide SE — SEXY BOOTS
- **插件**：[Melodic] 4Heels.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：264.1 MiB（MO2 实际保留 264.1 MiB）
- **规模**：ARMO 9　ARMA 9　可穿戴 mesh 10　贴图 39　有效 BodySlide 项目 5
- **材质**：FABRIC; LATEX; METAL
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**LOW**
- **重复资产**：691 KiB　**合并风险**：MODERATE
- **依赖**：跨 Mod 42　未解析 0

主要零件：
- Dolly Heels　`HEELS`　BodySlide
- Dolly Heels2　`HEELS`　BodySlide
- Dolly Heels3　`HEELS`　BodySlide
- Sylvia Heels　`HEELS`　BodySlide
- Sylvia Stockings　`STOCKINGS`　BodySlide
- Tracy Heels　`HEELS`　BodySlide
- Tracy Heels2　`HEELS`　BodySlide
- Tracy Heels3　`HEELS`　BodySlide
- …另有 1 个视觉零件
> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 31. Jennes Thigh 靴子- -BHUNP 3BBB- -CBBE 3BBB — Jennes Thigh Boots- -BHUNP 3BBB- -CBBE 3BBB

- **Mod**：Jennes Thigh 靴子- -BHUNP 3BBB- -CBBE 3BBB — Jennes Thigh Boot
- **插件**：Jennes.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：29.1 MiB（MO2 实际保留 29.1 MiB）
- **规模**：ARMO 1　ARMA 1　可穿戴 mesh 2　贴图 6　有效 BodySlide 项目 1
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：0 B　**合并风险**：HIGH
- **依赖**：跨 Mod 1　未解析 0

主要零件：
- Jennes　`OTHER`　BodySlide
> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 32. SSE_VRC_SOURYO_fix

- **Mod**：SSE_VRC_SOURYO_fix — 【来源·本地】
- **插件**：SSE_VRC_SOURYO.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：644.6 MiB（MO2 实际保留 644.6 MiB）
- **规模**：ARMO 17　ARMA 18　可穿戴 mesh 11　贴图 46　有效 BodySlide 项目 1
- **材质**：LATEX; METAL
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**HIGH**
- **重复资产**：148.2 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 15　未解析 0

主要零件：
- SSE VRC SOURYO　`BODY`　×2 变体，BodySlide
- SSE VRC SOURYO St HS W　`BODY`　×2 变体
- SSE VRC SOURYO St W　`BODY`　×2 变体
- SSE VRC SOURYO Stockings　`STOCKINGS`　×2 变体
- SSE VRC SOURYO Stockings HS　`STOCKINGS`　×2 变体
- SSE VRC SOURYO Stockingst Glove　`GLOVES`　×2 变体
- SSE VRC SOURYO Body02 St　`STOCKINGS`　—
- SSE VRC SOURYO Hand　`OTHER`　—
- …另有 3 个视觉零件
**可能的部分保留**：主体（SSE VRC SOURYO） + 独立配件 6 件 —— SSE VRC SOURYO Stockin、SSE VRC SOURYO Stockin、SSE VRC SOURYO Stockin、SSE VRC SOURYO Body02 、SSE VRC SOURYO Harness

**独特零件**（仅此一套）：SSE VRC SOURYO Body02 St、SSE VRC SOURYO Hand、SSE VRC SOURYO Harness、SSE VRC SOURYO Hat01

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 33. SSE_VRC_Latex_Servant

- **Mod**：SSE_VRC_Latex_Servant — 【来源·本地】
- **插件**：SSE_VRC_Latex_Servant.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：209.6 MiB（MO2 实际保留 209.6 MiB）
- **规模**：ARMO 39　ARMA 42　可穿戴 mesh 11　贴图 11　有效 BodySlide 项目 3
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：683 KiB　**合并风险**：HIGH
- **依赖**：跨 Mod 31　未解析 0

主要零件：
- SSE VRC DEXTA Hair　`OTHER`　×2 变体
- SSE VRC Latex Servant　`BODY`　×2 变体，BodySlide
- SSE VRC DEXTA Body01　`BODY`　—
- SSE VRC DEXTA Body02　`BODY`　—
- SSE VRC DEXTA Body03　`BODY`　—
- SSE VRC DEXTA Coat01　`COAT`　—
- SSE VRC DEXTA Coat02　`COAT`　—
- SSE VRC DEXTA Coat03　`COAT`　—
- …另有 29 个视觉零件
**可能的部分保留**：主体（SSE VRC Latex Servant） + 独立配件 6 件 —— SSE VRC DEXTA Tail01、SSE VRC DEXTA Tail02、SSE VRC Latex Servant 、SSE VRC Latex Servant 、SSE VRC Latex Servant 

**独特零件**（仅此一套）：SSE VRC DEXTA Body01、SSE VRC DEXTA Body02、SSE VRC DEXTA Body03、SSE VRC DEXTA Coat01

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 34. SSE_Latex_Nun

- **Mod**：SSE_Latex_Nun — 【来源·本地】
- **插件**：SSE_Latex_Nun.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：243.8 MiB（MO2 实际保留 243.8 MiB）
- **规模**：ARMO 48　ARMA 51　可穿戴 mesh 12　贴图 22　有效 BodySlide 项目 3
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**HIGH**
- **重复资产**：11.9 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 100　未解析 0

主要零件：
- SSE Latex Nun　`BODY`　×12 变体，BodySlide
- SSE Latex Nun Vail　`OTHER`　×12 变体
- SSE Latex Nun Glove　`GLOVES`　×6 变体
- SSE Latex Nun Mant　`OTHER`　×6 变体，BodySlide
- SSE Latex Nun Mask　`MASK`　×6 变体
- SSE Latex Nun Skirt　`SKIRT`　×6 变体，BodySlide
**可能的部分保留**：主体（SSE Latex Nun） + 独立配件 2 件 —— SSE Latex Nun Glove、SSE Latex Nun Mask

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 35. SSE_Kakugo_LatexNun

- **Mod**：SSE_Kakugo_LatexNun — 【来源·本地】
- **插件**：SSE_Kakugo_LatexNun.esp
- **体型**：CBBE_3BA　**物理**：CBPC
- **大小**：260.3 MiB（MO2 实际保留 260.3 MiB）
- **规模**：ARMO 31　ARMA 34　可穿戴 mesh 13　贴图 16　有效 BodySlide 项目 2
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：13.5 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 28　未解析 0

主要零件：
- SSE Kakugo Latex Nun Body01　`BODY`　BodySlide
- SSE Kakugo Latex Nun Body02　`BODY`　BodySlide
- SSE Kakugo Latex Nun Body03　`BODY`　BodySlide
- SSE Kakugo Latex Nun Body04　`BODY`　BodySlide
- SSE Kakugo Latex Nun Body05　`BODY`　BodySlide
- SSE Kakugo Latex Nun Feet01　`OTHER`　—
- SSE Kakugo Latex Nun Feet02　`OTHER`　—
- SSE Kakugo Latex Nun Feet03　`OTHER`　—
- …另有 23 个视觉零件
**可能的部分保留**：主体（SSE Kakugo Latex Nun Body01） + 独立配件 6 件 —— SSE Kakugo Latex Nun G、SSE Kakugo Latex Nun G、SSE Kakugo Latex Nun G、SSE Kakugo Latex Nun G、SSE Kakugo Latex Nun G

**独特零件**（仅此一套）：SSE Kakugo Latex Nun Fee、SSE Kakugo Latex Nun Fee、SSE Kakugo Latex Nun Fee、SSE Kakugo Latex Nun Fee

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 36. makaron-COSPLAY - AE_Wuthering_Waves_Lupa

- **Mod**：makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】
- **插件**：AE_Wuthering_Waves_Lupa.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：121.2 MiB（MO2 实际保留 121.2 MiB）
- **规模**：ARMO 7　ARMA 10　可穿戴 mesh 9　贴图 17　有效 BodySlide 项目 2
- **材质**：FABRIC; LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**HIGH**
- **重复资产**：0 B　**合并风险**：HIGH
- **依赖**：跨 Mod 85　未解析 0

主要零件：
- Wuthering Waves Lupa Hair　`OTHER`　×2 变体
- Wuthering Waves Lupa　`BODY`　BodySlide
- Wuthering Waves Lupa Feet　`OTHER`　—
- Wuthering Waves Lupa Hand　`OTHER`　—
- Wuthering Waves Lupa Mant　`OTHER`　BodySlide
- Wuthering Waves Lupa Tail　`TAIL`　—
**可能的部分保留**：主体（Wuthering Waves Lupa） + 独立配件 1 件 —— Wuthering Waves Lupa T

**独特零件**（仅此一套）：Wuthering Waves Lupa Fee、Wuthering Waves Lupa Han、Wuthering Waves Lupa Tai

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 37. makaron-COSPLAY - AE_Toxic_Cat

- **Mod**：makaron-COSPLAY - AE_Toxic_Cat — 【服装·装备】【来源·本地】
- **插件**：AE_Toxic_Cat.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：351.8 MiB（MO2 实际保留 351.8 MiB）
- **规模**：ARMO 21　ARMA 24　可穿戴 mesh 8　贴图 22　有效 BodySlide 项目 1
- **材质**：LATEX; METAL
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：607 KiB　**合并风险**：HIGH
- **依赖**：跨 Mod 21　未解析 0

主要零件：
- Toxic Cat A　`BODY`　BodySlide
- Toxic Cat B　`BODY`　BodySlide
- Toxic Cat C　`BODY`　BodySlide
- Toxic Cat Feet A　`OTHER`　—
- Toxic Cat Feet B　`OTHER`　—
- Toxic Cat Feet C　`OTHER`　—
- Toxic Cat Hand A　`OTHER`　—
- Toxic Cat Hand B　`OTHER`　—
- …另有 13 个视觉零件
**可能的部分保留**：主体（Toxic Cat A） + 独立配件 3 件 —— Toxic Cat Mask A、Toxic Cat Mask B、Toxic Cat Mask C

**独特零件**（仅此一套）：Toxic Cat Feet A、Toxic Cat Feet B、Toxic Cat Feet C、Toxic Cat Hand A

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 38. makaron-COSPLAY - AE_TFD_Valby_Nano_Suit

- **Mod**：makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】
- **插件**：AE_TFD_Valby_Nano_Suit.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：158.3 MiB（MO2 实际保留 158.3 MiB）
- **规模**：ARMO 5　ARMA 8　可穿戴 mesh 7　贴图 16　有效 BodySlide 项目 1
- **材质**：UNKNOWN
- **PBR**：NONE
- **技术成本**：**MEDIUM**
- **重复资产**：0 B　**合并风险**：HIGH
- **依赖**：跨 Mod 5　未解析 0

主要零件：
- TFD Valby Nano Suit　`OTHER`　×3 变体，BodySlide
- TFD Valby Nano Suit Hand　`OTHER`　—
- TFD Valby Nano Suit Helmet　`OTHER`　—
**独特零件**（仅此一套）：TFD Valby Nano Suit Hand、TFD Valby Nano Suit Helm

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 39. makaron-COSPLAY - AE_TFD_Haley_Black_Suit

- **Mod**：makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】
- **插件**：SSE_TFD_Haley_Black_Suit.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：359.8 MiB（MO2 实际保留 359.7 MiB）
- **规模**：ARMO 13　ARMA 16　可穿戴 mesh 10　贴图 40　有效 BodySlide 项目 1
- **材质**：LATEX; LEATHER; METAL
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**HIGH**
- **重复资产**：65.4 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 181　未解析 0

主要零件：
- SSE TFD Haley Suit　`OTHER`　×4 变体，BodySlide
- SSE TFD Haley Suit Feet　`OTHER`　×2 变体
- SSE TFD Haley Suit Glove　`GLOVES`　×2 变体
- SSE TFD Haley Suit Mask　`MASK`　×2 变体
- SSE TFD Haley Suit Altpurple　`OTHER`　—
- SSE TFD Haley Suit cape　`CAPE`　—
- SSE TFD Haley Suit capepurple　`OTHER`　—
**独特零件**（仅此一套）：SSE TFD Haley Suit Altpu、SSE TFD Haley Suit cape、SSE TFD Haley Suit capep

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 40. makaron-COSPLAY - AE_Stellablade_Tachy

- **Mod**：makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】
- **插件**：AE Stellablade Tachy.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：124.5 MiB（MO2 实际保留 124.5 MiB）
- **规模**：ARMO 3　ARMA 3　可穿戴 mesh 5　贴图 21　有效 BodySlide 项目 1
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：1.3 MiB　**合并风险**：MODERATE
- **依赖**：跨 Mod 2　未解析 0

主要零件：
- Stellablade Tachy　`BODY`　BodySlide
- Stellablade Tachy Hand　`OTHER`　—
- Stellablade Tachy Mask　`MASK`　—
**可能的部分保留**：主体（Stellablade Tachy） + 独立配件 1 件 —— Stellablade Tachy Mask

**独特零件**（仅此一套）：Stellablade Tachy Hand、Stellablade Tachy Mask

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 41. makaron-COSPLAY - AE_Once_Medic

- **Mod**：makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】
- **插件**：AE_Once_Medic.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：166.5 MiB（MO2 实际保留 166.5 MiB）
- **规模**：ARMO 8　ARMA 11　可穿戴 mesh 10　贴图 45　有效 BodySlide 项目 2
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：1.4 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 5　未解析 0

主要零件：
- Once Combat Medic　`BODY`　BodySlide
- Once Combat Medic Back Pack　`OTHER`　BodySlide
- Once Combat Medic Feet　`OTHER`　—
- Once Combat Medic Glove　`GLOVES`　—
- Once Combat Medic Hair　`OTHER`　—
- Once Combat Medic Mask　`MASK`　—
- Once Combat Medic Stockings　`STOCKINGS`　—
- Once Combat Medic Vail　`OTHER`　BodySlide
**可能的部分保留**：主体（Once Combat Medic） + 独立配件 3 件 —— Once Combat Medic Glov、Once Combat Medic Mask、Once Combat Medic Stoc

**独特零件**（仅此一套）：Once Combat Medic Feet、Once Combat Medic Glove、Once Combat Medic Hair、Once Combat Medic Mask

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 42. makaron-COSPLAY - AE_Latex_Kitty

- **Mod**：makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】
- **插件**：AE_Latex_Kitty.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：199.6 MiB（MO2 实际保留 199.5 MiB）
- **规模**：ARMO 20　ARMA 23　可穿戴 mesh 13　贴图 19　有效 BodySlide 项目 2
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**HIGH**
- **重复资产**：23.5 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 51　未解析 0

主要零件：
- Latex Kitty　`BODY`　×2 变体，BodySlide
- Latex Kitty Butt Tail　`TAIL`　×2 变体，BodySlide
- Latex Kitty Cape　`CAPE`　×2 变体
- Latex Kitty Feet　`OTHER`　×2 变体
- Latex Kitty Full Mask　`MASK`　×2 变体
- Latex Kitty Glove　`GLOVES`　×2 变体
- Latex Kitty Harness　`HARNESS`　×2 变体
- Latex Kitty Mask　`MASK`　×2 变体
- …另有 2 个视觉零件
**可能的部分保留**：主体（Latex Kitty） + 独立配件 6 件 —— Latex Kitty Butt Tail、Latex Kitty Full Mask、Latex Kitty Glove、Latex Kitty Harness、Latex Kitty Mask

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 43. AE_Vtaw_DarkNurse

- **Mod**：AE_Vtaw_DarkNurse — 【来源·本地】
- **插件**：AE_Vtaw_DarkNurse.esp
- **体型**：CBBE_3BA　**物理**：CBPC
- **大小**：165.5 MiB（MO2 实际保留 165.5 MiB）
- **规模**：ARMO 7　ARMA 10　可穿戴 mesh 8　贴图 18　有效 BodySlide 项目 3
- **材质**：METAL
- **PBR**：NONE
- **技术成本**：**MEDIUM**
- **重复资产**：0 B　**合并风险**：HIGH
- **依赖**：跨 Mod 7　未解析 0

主要零件：
- Vtaw Nurse　`BODY`　BodySlide
- Vtaw Nurse Feet　`OTHER`　—
- Vtaw Nurse Hand　`GLOVES`　—
- Vtaw Nurse Hat　`HAT`　BodySlide
- Vtaw Nurse Mask　`MASK`　BodySlide
- Vtaw Nurse St　`STOCKINGS`　—
- Vtaw Nurse Top　`OTHER`　—
**可能的部分保留**：主体（Vtaw Nurse） + 独立配件 4 件 —— Vtaw Nurse Hand、Vtaw Nurse Hat、Vtaw Nurse Mask、Vtaw Nurse St

**独特零件**（仅此一套）：Vtaw Nurse Feet、Vtaw Nurse Hand、Vtaw Nurse St、Vtaw Nurse Top

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 44. AE_VRC_Bunny_Nurse

- **Mod**：AE_VRC_Bunny_Nurse — 【来源·本地】
- **插件**：AE_VRC_BunnyNurse.esp
- **体型**：CBBE_3BA　**物理**：CBPC
- **大小**：746.0 MiB（MO2 实际保留 741.7 MiB）
- **规模**：ARMO 22　ARMA 25　可穿戴 mesh 16　贴图 25　有效 BodySlide 项目 1
- **材质**：LATEX; LEATHER; METAL
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**HIGH**
- **重复资产**：127.0 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 555　未解析 0

主要零件：
- VRC Bunny Nurse Feet B　`OTHER`　—
- VRC Bunny Nurse Glove B　`GLOVES`　—
- VRC Bunny Nurse Hand B　`OTHER`　—
- VRC Bunny Nurse Hat A　`HAT`　—
- VRC Bunny Nurse Hat B　`HAT`　—
- VRC Bunny Nurse Neck B　`OTHER`　—
- VRC Bunny Nurse Skirt B　`SKIRT`　—
- VRC Bunny Nurse Suit A　`BODY`　—
- …另有 14 个视觉零件
**可能的部分保留**：主体（VRC Bunny Nurse Suit A） + 独立配件 5 件 —— VRC Bunny Nurse Glove 、VRC Bunny Nurse Hat A、VRC Bunny Nurse Hat B、VRC Dwarven Bio Enclos、VRC Dwarven Bio Enclos

**独特零件**（仅此一套）：VRC Bunny Nurse Feet B、VRC Bunny Nurse Glove B、VRC Bunny Nurse Hand B、VRC Bunny Nurse Hat A

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 45. AE_HoodST

- **Mod**：AE_HoodST — 【来源·本地】
- **插件**：AE_HoodST.esp
- **体型**：CBBE_3BA　**物理**：CBPC
- **大小**：373.9 MiB（MO2 实际保留 373.9 MiB）
- **规模**：ARMO 16　ARMA 19　可穿戴 mesh 7　贴图 19　有效 BodySlide 项目 1
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：0 B　**合并风险**：HIGH
- **依赖**：跨 Mod 19　未解析 0

主要零件：
- Hood ST Suit01 Wet　`HOOD`　×2 变体，BodySlide
- Hood ST Suit02　`HOOD`　×2 变体，BodySlide
- Hood ST Suit03　`HOOD`　×2 变体，BodySlide
- Hood ST leotard01 Wet　`HOOD`　×2 变体
- Hood ST leotard02　`HOOD`　×2 变体
- Hood ST leotard03　`HOOD`　×2 变体
- Hood ST Feet01　`HOOD`　—
- Hood ST Top01　`HOOD`　—
- …另有 2 个视觉零件
**独特零件**（仅此一套）：Hood ST Feet01、Hood ST Top01、Hood ST Top02、Hood ST Top03

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 46. [Zap] Gantz Suit

- **Mod**：[Zap] Gantz Suit — 【来源·本地】
- **插件**：[Zap] Gantz Suit.esp
- **体型**：UNKNOWN　**物理**：UNKNOWN
- **大小**：1.27 GiB（MO2 实际保留 1.27 GiB）
- **规模**：ARMO 6　ARMA 6　可穿戴 mesh 6　贴图 60　有效 BodySlide 项目 6
- **材质**：LATEX; METAL
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：10.7 MiB　**合并风险**：MODERATE
- **依赖**：跨 Mod 16　未解析 0

主要零件：
- Gantz Suit Bodysuit　`BODYSUIT`　BodySlide
- Gantz Suit Gloves　`GLOVES`　BodySlide
- Gantz Suit Harness　`HARNESS`　BodySlide
- Gantz Suit Heels　`HEELS`　BodySlide
- Gantz Suit Neck Harness　`HARNESS`　BodySlide
- Gantz Suit Pauldron　`OTHER`　BodySlide
**可能的部分保留**：主体（Gantz Suit Bodysuit） + 独立配件 4 件 —— Gantz Suit Gloves、Gantz Suit Harness、Gantz Suit Heels、Gantz Suit Neck Harnes

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 47. [TRX] LatexWhitch

- **Mod**：[TRX] LatexWhitch — 【来源·本地】
- **插件**：NONE
- **体型**：UNKNOWN　**物理**：UNKNOWN
- **大小**：415.7 MiB（MO2 实际保留 415.7 MiB）
- **规模**：ARMO 0　ARMA 0　可穿戴 mesh 43　贴图 18　有效 BodySlide 项目 43
- **材质**：UNKNOWN
- **PBR**：NONE
- **技术成本**：**N/A（无 ARMO 记录）**
- **重复资产**：0 B　**合并风险**：NONE
- **依赖**：跨 Mod 0　未解析 0

**该 outfit 在范围内没有任何 ARMO 记录。**P00 已判定这类 Mod 只提供贴图 / mesh / physics / config，不是独立衣装本体。是否保留取决于它是否为其它套装提供素材。

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 48. [Predator] Premium Laced LatexBodysuit

- **Mod**：[Predator] Premium Laced LatexBodysuit — 【来源·本地】【系列·Predator
- **插件**：[Predator] Premium Laced Latex Bodysuit.esp
- **体型**：BHUNP　**物理**：UNKNOWN
- **大小**：242.5 MiB（MO2 实际保留 242.5 MiB）
- **规模**：ARMO 20　ARMA 20　可穿戴 mesh 3　贴图 11　有效 BodySlide 项目 1
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：133 B　**合并风险**：HIGH
- **依赖**：跨 Mod 13　未解析 0

主要零件：
- LB Bodysuit　`BODYSUIT`　×2 变体，BodySlide
- LB Bodysuit Leather Cro　`BODYSUIT`　×2 变体，BodySlide
- LB Bodysuit Leather Goth　`BODYSUIT`　×2 变体，BodySlide
- LB Bodysuit Leather Simple　`BODYSUIT`　×2 变体，BodySlide
- LB Bodysuit Leather Stich　`BODYSUIT`　×2 变体，BodySlide
- LB Bootst　`BOOTS`　×2 变体
- LB Bootst Leather Cro　`BOOTS`　×2 变体
- LB Bootst Leather Goth　`BOOTS`　×2 变体
- …另有 2 个视觉零件
**可能的部分保留**：主体（LB Bodysuit） + 独立配件 5 件 —— LB Bootst、LB Bootst Leather Cro、LB Bootst Leather Goth、LB Bootst Leather Simp、LB Bootst Leather Stic

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 49. [Predator] 靴子 Pack 02 CBBE 3BA — [Predator] Boots Pack 02 CBBE 3BA

- **Mod**：[Predator] 靴子 Pack 02 CBBE 3BA — [Predator] Boots Pack 02 CB
- **插件**：[Predator] Boots Pack 02.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：182.4 MiB（MO2 实际保留 182.4 MiB）
- **规模**：ARMO 16　ARMA 16　可穿戴 mesh 5　贴图 33　有效 BodySlide 项目 1
- **材质**：METAL
- **PBR**：NONE
- **技术成本**：**MEDIUM**
- **重复资产**：683 KiB　**合并风险**：HIGH
- **依赖**：跨 Mod 16　未解析 0

主要零件：
- BP2 Ankle Latex Dye　`OTHER`　×2 变体
- BP2 Ankle Leather Dye　`OTHER`　×2 变体
- BP2 Knee Latex　`OTHER`　×2 变体
- BP2 Knee Leather Dye　`OTHER`　×2 变体
- BP2 Tigh Kinky Latex　`BOOTS`　×2 变体
- BP2 Tigh Kinky Leather Dye　`BOOTS`　×2 变体
- BP2 Tigh Latex　`OTHER`　×2 变体，BodySlide
- BP2 Tigh Leather Dye　`OTHER`　×2 变体，BodySlide
> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 50. [Predator] Gynax Suit + Colors XXX BHUNP SE

- **Mod**：[Predator] Gynax Suit + Colors XXX BHUNP SE — 【体型·BHUNP】【来源·
- **插件**：[Predator] Gynax Latex Suit.esp
- **体型**：BHUNP　**物理**：UNKNOWN
- **大小**：57.6 MiB（MO2 实际保留 57.6 MiB）
- **规模**：ARMO 19　ARMA 19　可穿戴 mesh 1　贴图 19　有效 BodySlide 项目 1
- **材质**：UNKNOWN
- **PBR**：NONE
- **技术成本**：**HIGH**
- **重复资产**：14.2 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 3　未解析 0

主要零件：
- Gynax Suit Hood　`HOOD`　×7 变体
- Gynax Suit Mask　`MASK`　×6 变体
- Gynax Suit Hair　`OTHER`　BodySlide
- Gynax Suit Hood Neon G　`HOOD`　—
- Gynax Suit Hood Neon P　`HOOD`　—
- Gynax Suit Hood Neon R　`HOOD`　—
- Gynax Suit Hood Neon W　`HOOD`　—
- Gynax Suit Hood Neon Y　`HOOD`　—
**独特零件**（仅此一套）：Gynax Suit Hood Neon G、Gynax Suit Hood Neon P、Gynax Suit Hood Neon R、Gynax Suit Hood Neon W

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 51. [Predator] Latex Acessories 3BA SE

- **Mod**：[Predator] Latex Acessories 3BA SE — 【服装·装备】【体型·CBBE+3BA】【来源
- **插件**：[Predator] Latex Acessories.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：925.3 MiB（MO2 实际保留 925.3 MiB）
- **规模**：ARMO 194　ARMA 194　可穿戴 mesh 1　贴图 45　有效 BodySlide 项目 1
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**HIGH**
- **重复资产**：2.7 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 75　未解析 0

主要零件：
- Latex AC Catsuit　`BODYSUIT`　×16 变体，BodySlide
- Latex AC Catsuit Open A　`BODYSUIT`　×16 变体
- Latex AC Socks　`OTHER`　×16 变体
- Latex AC Mask　`MASK`　×10 变体
- Latex AC Anal Plug　`OTHER`　×8 变体
- Latex AC Bondage　`OTHER`　×8 变体
- Latex AC Corset　`CORSET`　×8 变体
- Latex AC Gag Plug　`OTHER`　×8 变体
- …另有 13 个视觉零件
**可能的部分保留**：主体（Latex AC Catsuit） + 独立配件 10 件 —— Latex AC Mask、Latex AC Gloves、Latex AC Heels M1、Latex AC Heels M2、Latex AC Hood

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 52. [Predator] Naughty Slave Harness 3 CBBE 3BA AE

- **Mod**：[Predator] Naughty Slave Harness 3 CBBE 3BA AE — 【体型·CBBE+3B
- **插件**：[Predator] Naughty Slave Harness 3.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：365.6 MiB（MO2 实际保留 365.6 MiB）
- **规模**：ARMO 14　ARMA 14　可穿戴 mesh 8　贴图 13　有效 BodySlide 项目 1
- **材质**：METAL
- **PBR**：NONE
- **技术成本**：**MEDIUM**
- **重复资产**：133 B　**合并风险**：HIGH
- **依赖**：跨 Mod 9　未解析 0

主要零件：
- NSH Chains Breast　`OTHER`　×2 变体
- NSH Chains Butt　`OTHER`　×2 变体
- NSH Chains Nip　`OTHER`　×2 变体
- NSH Chains Tighs　`OTHER`　×2 变体
- NSH Harness Dye　`HARNESS`　×2 变体，BodySlide
- NSH Heels　`HEELS`　×2 变体
- NSH Nip Pasties　`OTHER`　×2 变体
> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 53. [Predator] Penitent Warrior CBBE 3BA AE

- **Mod**：[Predator] Penitent Warrior CBBE 3BA AE — 【体型·CBBE+3BA】【平台·A
- **插件**：[Predator] Penitent Warrior.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：214.6 MiB（MO2 实际保留 214.6 MiB）
- **规模**：ARMO 2　ARMA 4　可穿戴 mesh 2　贴图 9　有效 BodySlide 项目 1
- **材质**：LATEX; LEATHER; METAL
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**MEDIUM**
- **重复资产**：14.2 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 12　未解析 0

主要零件：
- PW Warrior Base　`OTHER`　BodySlide
- PW Warrior Dye　`OTHER`　BodySlide
> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 54. [Predator] Provocative Bikini Harness + Colors 3BA SE

- **Mod**：[Predator] Provocative Bikini Harness + Colors 3BA SE — 【服装·
- **插件**：[Predator] Provocative Bikini Harness.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：30.2 MiB（MO2 实际保留 30.2 MiB）
- **规模**：ARMO 12　ARMA 12　可穿戴 mesh 1　贴图 16　有效 BodySlide 项目 1
- **材质**：LATEX; METAL
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**HIGH**
- **重复资产**：14.2 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 11　未解析 0

主要零件：
- Provocative Blind Latex　`OTHER`　×12 变体，BodySlide
> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 55. [Predator] Silicon Acessories CBBE 3BA AE

- **Mod**：[Predator] Silicon Acessories CBBE 3BA AE — 【体型·CBBE+3BA】【平台
- **插件**：[Predator] Silicon Acessories.esp
- **体型**：CBBE_3BA　**物理**：SMP
- **大小**：635.1 MiB（MO2 实际保留 635.1 MiB）
- **规模**：ARMO 88　ARMA 48　可穿戴 mesh 25　贴图 30　有效 BodySlide 项目 2
- **材质**：LATEX
- **PBR**：FAKE_METALLIC_LATEX
- **技术成本**：**HIGH**
- **重复资产**：16.7 MiB　**合并风险**：HIGH
- **依赖**：跨 Mod 3　未解析 0

主要零件：
- HL Drone Cat　`OTHER`　×4 变体
- HL Drone Fox　`OTHER`　×4 变体
- HL Drone Puffy Hole　`OTHER`　×4 变体
- HL Drone Puppy　`OTHER`　×4 变体
- HL FCDOLL　`OTHER`　×4 变体
- HL Furry Anims　`OTHER`　×4 变体
- HL Hood Cat　`HOOD`　×4 变体
- HL Pig　`OTHER`　×4 变体
- …另有 16 个视觉零件
**可能的部分保留**：主体（HL Silicon Corset） + 独立配件 5 件 —— HL Hood Cat、HL Silicon Gloves、HL Silicon Pawn Gloves、HL Silicon Pawn Mitten、HL Silicon Pleaser Mit

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---

## 56. [Predator] Slave Harness Chastity CBBE 3BA AE

- **Mod**：[Predator] Slave Harness Chastity CBBE 3BA AE — 【体型·CBBE+3BA
- **插件**：[Predator] Slave Harness Chastity.esp
- **体型**：CBBE_3BA　**物理**：UNKNOWN
- **大小**：241.5 MiB（MO2 实际保留 241.5 MiB）
- **规模**：ARMO 22　ARMA 10　可穿戴 mesh 2　贴图 17　有效 BodySlide 项目 1
- **材质**：METAL
- **PBR**：NONE
- **技术成本**：**HIGH**
- **重复资产**：133 B　**合并风险**：HIGH
- **依赖**：跨 Mod 3　未解析 0

主要零件：
- DD INV Slave Harness Chastity Base Dye　`HARNESS`　×2 变体，BodySlide
- DD INV Slave Harness Chastity Dibella Dye　`HARNESS`　×2 变体，BodySlide
- DD INV Slave Harness Chastity Base01　`HARNESS`　UBE 分类未知
- DD INV Slave Harness Chastity Base02　`HARNESS`　UBE 分类未知
- DD INV Slave Harness Chastity Base03　`HARNESS`　UBE 分类未知
- DD INV Slave Harness Chastity Base04　`HARNESS`　UBE 分类未知
- DD INV Slave Harness Chastity Dibella01　`HARNESS`　UBE 分类未知
- DD INV Slave Harness Chastity Dibella02　`HARNESS`　UBE 分类未知
- …另有 12 个视觉零件
**独特零件**（仅此一套）：DD INV Slave Harness Cha、DD INV Slave Harness Cha、DD INV Slave Harness Cha、DD INV Slave Harness Cha

> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：

- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP
- Priority:　[ ] S　[ ] A　[ ] B　[ ] C

Notes: ______________________________________________

---
