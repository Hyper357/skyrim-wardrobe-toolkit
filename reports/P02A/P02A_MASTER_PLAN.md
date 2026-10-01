# P02A.1 MASTER PLAN - ZLJ_COMBAT_LATEX (ZLJ Combat Latex Pack)

**Phase:** P02A.1 final schema + namespace correction. **Status: STRICT READ-ONLY design ledger.**  
Nothing was copied, moved, deleted or rewritten. No MO2 mod, NIF, DDS, ESP, OSP, OSD or TRI was touched. No BodySlide build, no PGPatcher, no UBE conversion, no PBR generation, no plugin merge, no BSA unpacking. Writes are confined to `reports/P02A/` and `tools/P02A/`.

Canonical body `CBBE_3BA female` - target plugin `ZLJ_CombatLatex.esp` - 11 frozen Outfit IDs - one outfit = one independent asset namespace.

## Headline gates (P02A.1)

| gate | required | result |
|---|---|---|
| target path collision | 0 | **0** |
| cross-outfit runtime DDS after plan | 0 | **0** |
| cross-outfit runtime Mesh after plan | 0 | **0** |
| ARMA/ARMO model-role schema | PASS | **PASS** |
| TRI misclassification in physics | 0 | **0** |
| target OSP namespace | 11 | **11** |
| outfits PASS / REVIEW / BLOCKED | - | **0 / 7 / 4** |
| shared-material whitelist | NONE | **NONE** (483 proposal rows only) |

## Strict counting buckets (P02A.1 correction)

| quantity | pack total | meaning |
|---|---|---|
| GAME_NIF | 166 | distinct runtime meshes reachable from ARMO/ARMA |
| BODYSLIDE_OUTPUT_NIF | 17 | distinct meshes a BodySlide build would produce |
| SHAPEDATA_NIF_FILES | 59 | distinct ShapeData source NIF (files, not rows) |
| SHAPEDATA_TEXTURE_REWRITE_ROWS | 1096 | shape x texture-slot rows inside those files |
| BODY_MORPH_TRI | 11 | distinct .tri body morph files (NOT physics configs) |

The previous round reported 1096 as if it were a ShapeData NIF count. It is a row count. Corrected here.

## Per-outfit ledger

| Outfit | GAME_NIF | BS_OUT_NIF | SD files | SD rows | TRI | DDS in use | cross-outfit DDS (now) | after plan | true-missing | path-mismatch | body-skin ext | audit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `CL01_LatexKitty` | 17 | 2 | 6 | 136 | 0 | 45 | 9 | **0** | 0 | 74 | 0 | **REVIEW** |
| `CL02_OnceMedic` | 17 | 2 | 6 | 90 | 0 | 44 | 6 | **0** | 0 | 0 | 0 | **BLOCKED** |
| `CL03_Tachy` | 8 | 1 | 3 | 39 | 0 | 17 | 2 | **0** | 0 | 0 | 0 | **REVIEW** |
| `CL04_Haley` | 14 | 1 | 5 | 197 | 0 | 52 | 82 | **0** | 3 | 5 | 0 | **REVIEW** |
| `CL05_Valby` | 15 | 1 | 5 | 168 | 0 | 24 | 2 | **0** | 0 | 3 | 0 | **REVIEW** |
| `CL06_ToxicCat` | 16 | 1 | 5 | 47 | 0 | 24 | 0 | **0** | 0 | 0 | 0 | **REVIEW** |
| `CL07_Lupa` | 16 | 2 | 4 | 84 | 0 | 30 | 38 | **0** | 38 | 0 | 0 | **REVIEW** |
| `CL08_SpearHead` | 30 | 1 | 4 | 53 | 0 | 29 | 5 | **0** | 10 | 37 | 0 | **BLOCKED** |
| `CL09_Corrupted` | 12 | 4 | 12 | 122 | 5 | 31 | 3 | **0** | 0 | 0 | 0 | **BLOCKED** |
| `CL10_HoodST` | 13 | 1 | 6 | 80 | 6 | 22 | 4 | **0** | 0 | 0 | 0 | **REVIEW** |
| `CL11_SkimpyAssassin` | 8 | 1 | 3 | 80 | 0 | 26 | 4 | **0** | 0 | 1 | 0 | **BLOCKED** |
| **TOTAL** | **166** | **17** | **59** | **1096** | **11** | **344** | **155** | **0** | **51** | **120** | **0** | |

## The 13 mandated answers

### 1. How many Game NIF must each outfit migrate?

**166 GAME_NIF** pack-wide (per outfit in the table above), plus **17 BODYSLIDE_OUTPUT_NIF** that must also live inside the pack namespace. World/drop models are counted apart from wearable models, and the canonical CBBE_3BA female wearable set is **119 model references**.

### 2. How many ShapeData NIF?

**59 SHAPEDATA_NIF_FILES** (distinct files). They carry **1096 SHAPEDATA_TEXTURE_REWRITE_ROWS** (shape x texture-slot). Both numbers are reported separately and must never be added together or interchanged.

### 3. How many OSP / OSD?

- Target OSP: **exactly 11** (`CalienteTools\BodySlide\SliderSets\ZLJ_<OUTFIT_ID>.osp`), one per outfit, each containing one or more slider sets.
- OSD: **17 distinct planned OSD** under `CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\<OUTFIT_ID>\` (per project, not per outfit).
- Relationship basis: EXACT_OUTPUT_PATH=16, UNKNOWN=3, FROZEN_STRONG=1.
- **Risk carried forward:** merging several slider sets into one .osp deviates from BodySlide's standard one-OSP-per-slider-set behaviour. P02B must validate that BodySlide loads a merged OSP before any bulk migration.

### 4. How many DDS are actually in use?

**344 distinct DDS**, derived forwards from the retained NIFs and then classified by the targeted global VFS provider lookup.

Ledger action across all texture rewrite rows (2762 rows):

| rewrite status | rows | meaning |
|---|---|---|
| REPOINT_SELF_NAMESPACE | 1268 | the outfit's own material, already inside its namespace |
| COPY_FROM_EXTERNAL_MOD | 684 | mod outside the pack - copied into the consuming namespace |
| KEEP_EXTERNAL_REFERENCE | 380 | body skin / engine resource - stays outside every outfit namespace |
| UNRESOLVED | 241 | no usable provider, see question 10 |
| COPY_FROM_CROSS_OUTFIT | 189 | borrowed from another outfit in this pack - copied, never shared |

Provider-lookup verdicts over the unresolvable set (75 distinct paths):

| class | distinct paths | action |
|---|---|---|
| EXTERNAL_PROVIDER_FOUND | 40 | COPY into the consuming outfit namespace + REPOINT |
| GLOBAL_BODY_SKIN | 12 | **KEEP EXTERNAL - never copied into an outfit namespace** |
| TRUE_MISSING | 12 | UNRESOLVED, no provider anywhere in the instance |
| UNKNOWN (path mismatch) | 8 | UNRESOLVED, human confirmation required |
| VANILLA_ENGINE_RESOURCE | 3 | KEEP EXTERNAL |

### 5. How many cross-outfit DDS dependencies exist today?

**155** today, **0 remain after the plan**. Each is closed by copying the DDS into the consuming outfit namespace and repointing the references - never by sharing.

### 6. How many cross-outfit mesh dependencies exist today?

**49** retained meshes whose winning provider belongs to a different outfit or mod.

### 7. Which outfit has the most complex asset relationship?

| rank | outfit | complexity | drivers |
|---|---|---|---|
| 1 | `CL04_Haley` | 2476 | 82 cross-outfit DDS; 15 foreign-body model refs; 3 true-missing DDS; 3 physics config(s); support layer: PBR_PATCH |
| 2 | `CL01_LatexKitty` | 1777 | 9 cross-outfit DDS; 8 foreign-body model refs; 4 physics config(s) |
| 3 | `CL08_SpearHead` | 1563 | 5 cross-outfit DDS; 12 model refs confirmed absent; 10 true-missing DDS |
| 4 | `CL07_Lupa` | 1110 | 38 cross-outfit DDS; 5 foreign-body model refs; 38 true-missing DDS; 1 physics config(s) |
| 5 | `CL05_Valby` | 987 | 2 cross-outfit DDS; 7 foreign-body model refs |
| 6 | `CL02_OnceMedic` | 956 | 6 cross-outfit DDS; 6 foreign-body model refs; 1 broken BodySlide chain(s); 1 physics config(s) |
| 7 | `CL10_HoodST` | 588 | 4 cross-outfit DDS; 13 foreign-body model refs |
| 8 | `CL06_ToxicCat` | 573 | 18 foreign-body model refs |
| 9 | `CL09_Corrupted` | 461 | 3 cross-outfit DDS; 2 foreign-body model refs; 1 broken BodySlide chain(s); support layer: LATEX_REWORK |
| 10 | `CL03_Tachy` | 428 | 2 cross-outfit DDS; 4 foreign-body model refs |
| 11 | `CL11_SkimpyAssassin` | 328 | 4 cross-outfit DDS; 2 broken BodySlide chain(s) |

**Most complex: `CL04_Haley`**; runner-up `CL01_LatexKitty`.

### 8. Which outfit is the best first P02B pilot?

**Recommended pilot: `CL06_ToxicCat`** - audit REVIEW, complexity 573, 16 GAME_NIF, 24 DDS, 0 cross-outfit DDS, 0 true-missing, 0 absent model refs, support layers: none.

Outfits that must **not** go first: `CL02_OnceMedic` (BLOCKED), `CL08_SpearHead` (BLOCKED), `CL09_Corrupted` (BLOCKED), `CL11_SkimpyAssassin` (BLOCKED).

### 9. Which target paths collide?

**0.** Collisions are re-derived independently by indexing every planned target path (meshes, BodySlide outputs, OSP names, morph TRI) and comparing owning Outfit IDs.

### 10. Which references are still unresolvable?

Only **20 distinct DDS** lack a usable provider, and each one now carries a global-lookup verdict rather than an assumption:

- **TRUE_MISSING 12** - absent from every mod directory and from the game Data root.
- **UNKNOWN 8** - the referenced folder does not exist, but same-named files exist elsewhere. These are *not* promoted to found, because same-name is not same-asset; each candidate is recorded for human confirmation.
- **VANILLA_ENGINE_RESOURCE** rows are unverified: the game ships no loose `textures` tree, everything lives in 93 .bsa archives, and a path-existence check cannot see inside an archive.

**The previous conclusion that these references are already broken at runtime is withdrawn.** The global lookup showed that most of them have real providers, so that claim was an artefact of the P00 scope, not a fact.

### 11. Which existing PBR / rework need provenance kept?

| outfit | role | mod | handling |
|---|---|---|---|
| `CL04_Haley` | PBR_PATCH | `Haley Black Suit PBR` | provenance only; P05/P06 redesign the material standard |
| `CL09_Corrupted` | LATEX_REWORK | `堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】` | rework is the VFS winner over the base mod; provenance chain must survive migration |

**CL09 Corrupted** additionally has a full decision record in `CL09_REWORK_VS_BODYSLIDE_DECISION.md`: measured byte-level, the rework is a 12/24-byte weight tweak on five parts plus a complete boot replacement; the canonical source is **REWORK_BACKPORTED_TO_SHAPEDATA**, and CL09 stays BLOCKED until a trial build validates it.

### 12. After planning, can each outfit own an independent namespace?

**YES for everything the Pack owns.** All 166 GAME_NIF, 17 BODYSLIDE_OUTPUT_NIF, 59 SHAPEDATA_NIF_FILES, 11 OSP, 11 BODY_MORPH_TRI and 464 model references resolve inside `meshes\ZLJ\CombatLatex\<OUTFIT_ID>` / `textures\ZLJ\CombatLatex\<OUTFIT_ID>` / `CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\<OUTFIT_ID>`.

Three honest caveats: (a) the shared-material whitelist stays **NONE** - 483 rows are proposals only, each still copied per outfit; (b) 0 GLOBAL_BODY_SKIN references deliberately stay outside every outfit namespace; (c) 51 references point at mods that are absent from this instance and cannot be brought into any namespace.

### 13. What blocks P02B?

**Confirmed structural blockers** (kept BLOCKED on purpose, no invented fixes):

| outfit | gate | what is actually wrong |
|---|---|---|
| `CL02_OnceMedic` | C3 | projects=2 chain-incomplete=1 OSP-off-ns=0 ShapeData-off-ns=0 Output-off-ns=0 UNKNOWN-basis=0 shapedata-tex-off-ns=0 |
| `CL08_SpearHead` | C4 | records=48 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=24 flagged-canonical=20 world-models=24 plugin-DDS-cross-outfit-open=0 | model refs: source-asset-absent=12 foreign-bo |
| `CL09_Corrupted` | C3 | projects=5 chain-incomplete=1 OSP-off-ns=0 ShapeData-off-ns=0 Output-off-ns=0 UNKNOWN-basis=1 shapedata-tex-off-ns=0 |
| `CL11_SkimpyAssassin` | C3 | projects=3 chain-incomplete=2 OSP-off-ns=0 ShapeData-off-ns=0 Output-off-ns=0 UNKNOWN-basis=2 shapedata-tex-off-ns=0 |

**Open decisions** (the plan is provisional until a human answers):

1. **Male-slot foreign body** - 78 model references for 9 outfits resolve to a male body overhaul mod, not to these outfits. Vendoring another body's mesh into a CBBE_3BA female pack is unacceptable; decide to drop the male slot or author neutral meshes.
2. **World-model aliasing** - 51 world-model slots point at the same file as their own wearable mesh. Decide whether to author real drop meshes or accept the reuse.
3. **Body-skin override** - the 9 GLOBAL_BODY_SKIN paths are won by a BnP female-skin mod (priority 1131) ahead of CBBE (1179), so the meshes currently sample another body's skin. Cross-body compatibility risk.
4. **CL09 rework vs BodySlide** - see the decision record; needs one trial build before any CL09 copy.
5. **OSP merge behaviour** - one OSP holding several slider sets must be validated in BodySlide first.
6. **51 TRUE_MISSING DDS** and **120 path-mismatch references** - author omissions or wrong paths in the source mods; decide between installing the owning mod, dropping the reference, or accepting the defect.
7. **BSA blind spot** - vanilla meshes and engine resources cannot be verified without a read-only archive listing task, which is out of scope here.
8. **CL11 body branch** - keep only the CBBE/3BBB/3BA compatible branch; BHUNP files stay until P02B decides.
9. **EDID granularity** and **OSP output vs ARMA reference naming** remain open from the previous round.
10. **Physics bone verification** - HDT-SMP bone sets are not part of the frozen evidence.
11. **Re-freeze P00 before P02B - mandatory.** The instance was modified by a separate actor while P02A.1 ran: Outfit Studio / BodySlide working files were written at 22:52, 23:00 and 23:12, and CL03_Tachy's own 3 ShapeData + 7 mesh files were rewritten at 23:01:21, i.e. between the source map and the texture ledgers. This phase did not do it (a static audit of every generator under `tools/P02A/` found 0 write calls against any MO2 path), but the frozen evidence and the live instance can no longer be assumed identical. Stop any build session and re-freeze P00 before executing a single COPY.

## Deliverables

- [x] P02A_EFFECTIVE_SOURCE_MAP.csv (916 rows)
- [x] P02A_MESH_MIGRATION.csv (338 rows)
- [x] P02A_TEXTURE_MIGRATION.csv (1666 rows)
- [x] P02A_CROSS_OUTFIT_TEXTURE_CLOSURE.csv (1019 rows)
- [x] P02A_NIF_TEXTURE_REWRITE.csv (1666 rows)
- [x] P02A_BODYSLIDE_MIGRATION.csv (20 rows)
- [x] P02A_BODYSLIDE_MORPH_MIGRATION.csv (11 rows)
- [x] P02A_SHAPEDATA_TEXTURE_REWRITE.csv (1096 rows)
- [x] P02A_PLUGIN_RECORD_MIGRATION.csv (346 rows)
- [x] P02A_ARMA_MODEL_REWRITE.csv (464 rows)
- [x] P02A_PLUGIN_TEXTURE_REWRITE.csv (126 rows)
- [x] P02A_PHYSICS_MIGRATION.csv (9 rows)
- [x] P02A_GLOBAL_PROVIDER_LOOKUP.csv (75 rows)
- [x] P02A_SELF_CONTAINMENT_AUDIT.csv
- [x] P02A_UNRESOLVED_REFERENCE_CLASSIFICATION.csv
- [x] P02A_ARCHITECTURE.md
- [x] CL09_REWORK_VS_BODYSLIDE_DECISION.md
- [x] P02A_MASTER_PLAN.md
- [x] `reports/P02A/outfits/` - 11 per-outfit manifests

## STOP

P02A.1 ends here. **P02B is not authorised.** No COPY / MOVE / DELETE / NIF / ESP / OSP / OSD / TRI write may happen until a human reviews this design and answers the open decisions above.
