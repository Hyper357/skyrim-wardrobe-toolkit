# CL09_Corrupted — REWORK vs BODYSLIDE DECISION

**Decision record for P02A.1. Read-only analysis. No file was copied, moved or rewritten.**

Evidence collector: `tools/P02A/p02a_cl09_evidence.py` (re-runnable; reads the frozen P00 evidence plus the two
specific NIF pairs from the CL09 source mods).

| | |
|---|---|
| Pack / outfit | `ZLJ_COMBAT_LATEX` / `CL09_Corrupted` |
| Base mod | priority **888** — AE Corrupted Body Suit |
| Latex Rework | priority **887** — AE Corrupted Body Suit - Latex Rework |
| VFS winner | **Latex Rework** (lower priority number = higher MO2 priority) |
| Canonical body | CBBE_3BA female |
| **Gate** | **CL09 stays BLOCKED until the trial build validates recommendation R2** |

---

## 0. What the evidence shows

### 0.1 File-level overlap

| | base | rework |
|---|---|---|
| files | 44 | 29 |
| .nif | 17 | 17 |
| .dds | 10 | 12 |
| .osp / .osd | 4 / 6 | 0 / 0 |
| .tri | 5 | 0 |
| .esp | 1 | 0 |

The rework overrides **18** virtual paths and adds **11** new ones. It ships **no plugin, no OSP, no OSD and no TRI**:
all BodySlide control data still comes from the base mod.

The 11 added files are 6 ShapeData NIF dropped **flat** at the ShapeData root
(`CalienteTools\BodySlide\ShapeData\ae_corruptedbodysuit*.nif`, no data folder) and 5 new DDS
(`bootshoe / bootsole / bootsockleather / bootsockmetal / cmilltina_glossmask`).

### 0.2 Byte-level measurement of the 11 overridden runtime meshes

| mesh | size base -> rework | differing bytes | string table delta |
|---|---|---|---|
| ae_corruptedbodysuit_0/1.nif (body) | 4103974 -> 4103974 | **24** | 0 / 0 |
| ae_corruptedbodysuit_hand_0/1.nif | 1040233 -> 1040233 | **12** | 0 / 0 |
| ae_corruptedbodysuit_head_0/1.nif | 135313 -> 135313 | **12** | 0 / 0 |
| ae_corruptedbodysuit_mask_0/1.nif | 231992 -> 231992 | **12** | 0 / 0 |
| ae_corruptedbodysuit_neck.nif | 120573 -> 120573 | **12** | 0 / 0 |
| ae_corruptedbodysuit_feet_0/1.nif (boots) | 1041134 -> 3809278 | **953034 (91.5%)** | 615 / 6967 |

### 0.3 Byte-level measurement of the ShapeData

| ShapeData NIF | vs base data-folder copy | differing bytes |
|---|---|---|
| ae_corruptedbodysuit.nif | `...\ae_corruptedbodysuit\ae_corruptedbodysuit.nif` | **12** |
| ae_corruptedbodysuit_hand.nif | `...\ae_corruptedbodysuit_hand\...` | **12** |
| ae_corruptedbodysuit_head.nif | `...\ae_corruptedbodysuit_head\...` | **12** |
| ae_corruptedbodysuit_mask.nif | `...\ae_corruptedbodysuit_mask\...` | **12** |
| ae_corruptedbodysuit_neck.nif | `...\ae_corruptedbodysuit\...` | **12** |
| ae_corruptedbodysuit_feet.nif | `...\ae_corruptedbodysuit_feet\...` | **0 — byte identical** |

**This is the decisive fact:** the base mod already contains a ShapeData for the boots that is *byte identical* to the
rework's, and it is the large (3.8 MB) one. The base's own runtime boots are the small 1.0 MB mesh. In other words the
base mod ships the new boot geometry as ShapeData but never shipped a build of it; the rework shipped the build.

---

## 1. What does the Latex Rework actually change?

Measured per category:

| category | body / hand / head / mask / neck | boots (feet) |
|---|---|---|
| **geometry** | **unchanged** — identical shape names, identical shape counts, identical node counts (body 61, hand 44, mask 59, neck 7, head 9) | **replaced** — shapes 2 -> 4 (`CHeels/Eff` -> `shoe_Plane.005 / sole_Plane.006 / SocksLeather / SocksMetal`), nodes 11 -> 52, bone refs 107 -> 71, +2.77 MB |
| **shader** | no evidence of any change — identical material slots and identical texture paths on every shape | changed only through the texture rebinding below |
| **texture path** | **unchanged** — byte-identical string tables | **changed** — `cmilltina_acc_texture / cmilltina_acc_normal / s.dds / eff02.dds` replaced by `bootshoe / bootsole / bootsockleather / bootsockmetal`, plus `textures\ae_latex_kitty\n.dds` and `textures\dx\fetishfashion\05_begforit\socks_n.dds` |
| **weight** | **12 bytes (24 in the body mesh) differ, with no string-table change at all** — consistent with a scalar/weight-level tweak; the exact field is **UNKNOWN** without a block-level decode | n/a (asset replaced) |
| **combination** | none — the rework ships **no .esp**, adds no ARMO/ARMA/COBJ, so no new parts, no new sets, no load-order combination change | none |

**Answer to question 1:** the rework changes *weight-level scalars* on five body parts, and *geometry + texture paths* on
the boots. It changes no shader bindings, no topology, and nothing at the plugin/combination level.

---

## 2. What would a base ShapeData build lose?

A BodySlide build driven by the **base OSPs** reads the base data folders. Per the byte measurements:

| part | base ShapeData build result | rework intent | lost? |
|---|---|---|---|
| body / hand / head / mask / neck | the **base** geometry, i.e. the 12-byte (24-byte) tweak is **not applied** | tweak applied | **YES — the tweak is lost** |
| boots | boots built from the base feet ShapeData, which is byte-identical to the rework's — same 4 shapes, and the **rework's own texture bindings** (`bootshoe / bootsole / bootsockleather / bootsockmetal`, `textures\ae_latex_kitty\n.dds`, `textures\dx\fetishfashion\05_begforit\socks_n.dds`, EnvMask `textures\devious\devices\catsuitLatex_em.dds`) | boots with rework bindings | **NO — the build reproduces it** |

**Answer to question 2:** a base ShapeData build loses the five-part weight tweak and nothing else. It does **not** lose
the boots — it in fact regenerates them.

**Consequence that must not be missed:** building from the base feet ShapeData pulls the rework's external references into
the generated NIF. Those are now CL09 dependencies on

- `textures\ae_latex_kitty\n.dds` — **a cross-outfit reference to CL01_LatexKitty**, already tracked in
  `P02A_CROSS_OUTFIT_TEXTURE_CLOSURE.csv` and planned as COPY into `textures\ZLJ\CombatLatex\CL09_Corrupted\`;
- `textures\dx\fetishfashion\05_begforit\socks_n.dds` and `textures\devious\devices\catsuitLatex_em.dds` —
  out-of-pack references whose providers are resolved in `P02A_GLOBAL_PROVIDER_LOOKUP.csv`.

A base-only build therefore does not merely lose a tweak; it also **creates new external dependencies that did not exist
in the current runtime mesh**. This is the opposite of the usual assumption and is the main reason CL09 needs an
explicit decision.

---

## 3. Which canonical 3BA source should be used?

Candidates: `BASE_SHAPEDATA` / `REWORK_RUNTIME_MESH` / `REWORK_BACKPORTED_TO_SHAPEDATA` / `UNKNOWN`.

| option | verdict | reason |
|---|---|---|
| `BASE_SHAPEDATA` | **REJECTED for the five body parts** | discards the 12/24-byte tweak, and creates the new external boots dependencies described above |
| `REWORK_RUNTIME_MESH` | **REJECTED as canonical** | it is a pre-built static mesh: it cannot be driven by the new `ZLJ_CL09_Corrupted.osp` slider set, so the outfit would silently lose BodySlide functionality |
| `REWORK_BACKPORTED_TO_SHAPEDATA` | **RECOMMENDED (R2)** | adopt the rework's ShapeData NIFs as the ShapeData source for `ZLJ_Combat_Latex\CL09_Corrupted\`. They are the base ShapeData plus the tweak, so a BodySlide build reproduces the rework intent *and* remains slider-driven |
| `UNKNOWN` | not acceptable as a final answer, but **the exact meaning of the 12 bytes is still UNKNOWN** | see the residual risk below |

### Recommended decision

**R1.** Keep **Latex Rework as the provenance of the current runtime winner** — that is a fact of the VFS, not a choice.

**R2.** For the canonical CBBE_3BA female branch, use **`REWORK_BACKPORTED_TO_SHAPEDATA`**:
the ShapeData source for CL09 becomes the rework's ShapeData NIF set, moved into
`CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL09_Corrupted\` and referenced by
`CalienteTools\BodySlide\SliderSets\ZLJ_CL09_Corrupted.osp`.
Note this also repairs a defect in the source mod: the rework shipped its ShapeData flat and with no OSP, so as shipped
those files are unreachable by BodySlide.

**R3.** The boots' external references must be vendored into the CL09 namespace at the same time
(COPY + REPOINT), per the one-outfit-one-namespace rule. A base build must never be used to "clean" them away.

**R4.** `textures\actors\character\female\femalebody_1*.dds` and the other `femalebody_etc_v2_1*` /
`femalehands_1*` / `femalebody_1_sk.dds` references stay **external** as GLOBAL_BODY_SKIN
(they belong to the body/skin system, not to the outfit material, and must never be copied into the outfit namespace).

### Residual risk — why CL09 stays BLOCKED

The 12/24-byte delta has **not** been decoded to a named NIF field. It is consistent with a weight or vertex-scale tweak,
but it could in principle be a bounding-sphere or shader-parameter value. Consequences:

1. P02B must run **one trial BodySlide build** for CL09 from the recommended ShapeData and compare the output against the
   current runtime mesh. If the body silhouette does not match, the tweak was not a weight and R2 must be revisited.
2. Until that build passes, **no CL09 file may be copied into the Pack namespace**, because a wrong backport would
   silently alter the outfit's shape for every future slider change.
3. The 6 flat ShapeData NIF the rework adds are currently **orphans** (no OSP claims them). R2 adopts them, which
   resolves the orphan question for CL09 rather than leaving it UNKNOWN.

---

## 4. Status

| item | state |
|---|---|
| CL09 canonical source decision | **decided: `REWORK_BACKPORTED_TO_SHAPEDATA`** |
| CL09 P02B entry | **BLOCKED** until the trial build validates R2 |
| rework/base provenance | preserved in `P02A_EFFECTIVE_SOURCE_MAP.csv` (18 overridden + 11 added paths) |
| cross-outfit leak `textures\ae_latex_kitty\n.dds` | planned as COPY into the CL09 namespace |
| GLOBAL_BODY_SKIN references | remain external, never copied |
