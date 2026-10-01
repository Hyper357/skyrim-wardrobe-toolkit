# P01_CURATION_SUMMARY.md

统计汇总。**本文件不做任何 KEEP / DROP 决策。**

| 项 | 值 |
|---|---|
| Logical outfits | **56** |
| Visual parts | **645**（由 1448 条 ARMO 折叠）|
| PARTIAL 候选行 | 405（涉及 23 套 outfit）|

## 体型分布

| body_type | outfits |
|---|---|
| CBBE_3BA | 40 |
| UNKNOWN | 13 |
| BHUNP | 2 |
| MIXED | 1 |

## 技术成本分布

| technical_cost | outfits | visual parts |
|---|---|---|
| HIGH | 17 | 195 |
| LOW | 2 | 15 |
| MEDIUM | 27 | 435 |
| N/A（无 ARMO 记录） | 10 | 0 |

## UBE 转换分类（仅分类，未执行任何转换）

| class | visual parts | 含义 |
|---|---|---|
| **B** | 294 | 普通非贴身 mesh |
| **A** | 200 | 紧身贴体 3BA mesh，预计非常适合自动转换 |
| **D** | 117 | SMP / 裙 / 外套 / 物理链 |
| **C** | 23 | 多层 / 复杂配件 |
| **E** | 11 | 未知 / 高风险 |

## 物理分布

| physics | outfits |
|---|---|
| UNKNOWN | 44 |
| CBPC | 11 |
| SMP | 1 |

## 视觉零件分类

| part_category | visual parts | DIY 复用价值 |
|---|---|---|
| OTHER | 209 | MEDIUM |
| CORSET | 93 | LOW |
| BODY | 71 | LOW |
| BODYSUIT | 62 | LOW |
| GLOVES | 46 | HIGH |
| MASK | 26 | HIGH |
| BOOTS | 26 | HIGH |
| HARNESS | 25 | HIGH |
| HEELS | 21 | HIGH |
| HOOD | 19 | HIGH |
| SKIRT | 10 | LOW |
| STOCKINGS | 8 | HIGH |
| COAT | 7 | LOW |
| TAIL | 7 | HIGH |
| CAPE | 6 | LOW |
| HAT | 4 | HIGH |
| CHOKER | 3 | HIGH |
| BELT | 2 | HIGH |

---

## 等待人工决定

请在 `P01_HUMAN_REVIEW.md` 中逐套填写，或直接在以下 CSV 中填写`USER_DECISION` / `USER_PRIORITY` / `USER_NOTE`：

- `P01_OUTFIT_REVIEW.csv`
- `P01_VISUAL_PARTS.csv`
- `P01_PARTIAL_CANDIDATES.csv`

**在人工填写完成之前，不进行任何删除、合并、转换或改写。**
