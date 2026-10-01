# P02A Architecture & Effective Source Map

**Pack**: `ZLJ_COMBAT_LATEX` / ZLJ Combat Latex Pack  
**Canonical body**: `CBBE_3BA`  
**Target plugin**: `ZLJ_CombatLatex.esp`  
**Stage**: P02A -- namespace & migration *plan only*  
**Generator**: `tools/P02A/p02a_sourcemap.py` (re-runnable, reads only the frozen P00 evidence set)  
**Ledger**: `reports/P02A/P02A_EFFECTIVE_SOURCE_MAP.csv` (916 rows)

---

## 0. STRICT READ-ONLY declaration

This document is a **plan**. Nothing in it has been executed.

* No MO2 mod folder, Skyrim `Data` file or game install file was created, moved, copied, renamed or modified.
* No NIF, DDS, ESP/ESL, OSP, OSD, XML, JSON or INI was rewritten.
* **No BodySlide build, no PGPatcher pass, no UBE conversion, no PBR generation and no plugin merge was run.**
* The only files written by this stage are the two deliverables above and the generator script, all inside this repository.
* Every `COPY + REPOINT` in the CSV is *plan text*. A later stage must re-authorise it.

---

## 1. Namespace rule and target path layout

**One source Outfit == one independent asset namespace.** Each of the 11 frozen `OUTFIT_ID`s owns a private mesh tree, a private texture tree, a private BodySlide ShapeData folder and its own slider set:

```
meshes\ZLJ\CombatLatex\<OUTFIT_ID>\<file>.nif
textures\ZLJ\CombatLatex\<OUTFIT_ID>\<file>.dds
CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\<OUTFIT_ID>\<file>.nif|.osd
CalienteTools\BodySlide\SliderSets\ZLJ_<OUTFIT_ID>.osp
pbrnifpatcher\ZLJ\CombatLatex\<OUTFIT_ID>\<file>.json   (PBR patches only)
```

Derived naming rules:

| Item | Rule | Example |
|---|---|---|
| Plugin | fixed | `ZLJ_CombatLatex.esp` |
| ARMO/ARMA EDID | `ZLJ_CL_<OUTFIT>_<PART>` | `ZLJ_CL_Haley_Body` |
| BodySlide UI name | `[ZLJ Combat Latex] <Outfit> - <Part>` | `[ZLJ Combat Latex] Haley - Bodysuit` |
| Slider set file | `ZLJ_<OUTFIT_ID>.osp` | `ZLJ_CL04_Haley.osp` |

### 1.1 The independence principle (normative)

> **In P02A two different Outfits never share a DDS, NIF, ShapeData NIF or OSD -- even when their SHA256 is byte-for-byte identical.**

Byte-identical content is a *duplication*, not a *shared resource*. Collapsing it is a **P05 MATERIAL STANDARDIZATION** decision, not a P02A one. The P02A ledger therefore records such pairs explicitly with `status=PROPOSAL_SHARED_NOT_APPROVED` so P05 can act on real evidence later, and the public-resource whitelist stays **NONE** for now.

A consequence: an Outfit that today *borrows* a texture owned by another Outfit's mod (section 5) does **not** silently get a private copy either. It keeps an explicit, recorded dependency with `migration_action=UNKNOWN_BLOCKER` until a human decides. Silently copying it would fabricate a source relationship the frozen evidence does not support.

---

## 2. Winner determination rule

For every virtual path the CSV records the **VFS winner**, not "the mod that happens to hold the file":

```
providers(vp)  = every P00.file_index row whose norm(vpath) == norm(vp)
winner(vp)     = argmin  P00.priority[mod]        # LOWER number wins
shadowed(vp)   = providers(vp) minus {winner(vp)}
```

* MO2 priority: **smaller number = higher priority = VFS winner**.
* `winning_provider` is that mod name; `shadowed_providers` lists every loser.
* A path with **no** provider is never silently dropped -- it is written with an empty `winning_provider`, `status=BLOCKER` and `migration_action=UNKNOWN_BLOCKER`.
* Identical SHA256 across providers does **not** create a merge. Each provider stays a separate row; only the winner is a migration source.

---

## 3. Source taxonomy (how `relationship` is decided)

| relationship | Decided by | Notes |
|---|---|---|
| `BASE_MOD` | winning provider == the outfit's `primary` mod | the canonical delivery |
| `REWORK` | reserved: a frozen support mod whose role is a plain rework | **unused in P02A** -- no in-pack mod matches |
| `BODYSLIDE_CONVERSION` | `asset_type` in {SHAPEDATA_NIF, OSP, OSD}, or a GAME_NIF that is a .osp EXACT_OUTPUT_PATH | ShapeData is the 3BA source of truth; OSP is the slider definition |
| `PBR_PATCH` | `asset_type` == PBR_JSON, or path under `textures\pbr\`, or winner is the frozen PBR_PATCH support mod | CL04 only |
| `LATEX_REWORK` | winner is the frozen LATEX_REWORK support mod | CL09 only |
| `PHYSICS_PATCH` | `asset_type` == PHYSICS_XML | judged on the path type; the winner then decides pack membership |
| `NONE` | everything else, including every out-of-pack or unresolvable reference | the honest default |

`asset_type` values used: `PLUGIN`, `GAME_NIF`, `SHAPEDATA_NIF`, `OSP`, `OSD`, `DDS`, `PHYSICS_XML`, `CONFIG`, `PBR_JSON`, `OTHER`.

Non-asset detection (`migration_action=EXCLUDE_NON_ASSET`): `meta.ini` (MO2/FOMOD bookkeeping, reserved name), `.espbak`, `.old000`, `.old001`, timestamped `.esp.YYYY_MM_DD_HH_MM_SS` backups, `- 副本` / `_bak` author copies, `.tri` authoring caches, and the `bbd_catsuitspearhead - 副本.esp11` duplicate plugin.

---

## 4. Per-Outfit summary

`mods` = in-scope mods. `win NIF / DDS / OSP / OSD` = rows the Outfit actually keeps, i.e. the VFS winner is an in-pack mod. `recs` = plugin records. `rework` = has a rework layer. `PBR` = PBR patch present.

| OUTFIT_ID | mods | win NIF | win DDS | win OSP | win OSD | recs | PBR | rework | rows |
|---|---|---|---|---|---|---|---|---|---|
| `CL01_LatexKitty` | 1 | 21 | 19 | 2 | 6 | 44 | - | - | 105 |
| `CL02_OnceMedic` | 1 | 19 | 45 | 2 | 5 | 16 | - | - | 109 |
| `CL03_Tachy` | 1 | 8 | 21 | 1 | 3 | 6 | - | - | 55 |
| `CL04_Haley` | 2 | 15 | 55 | 1 | 5 | 30 | yes | - | 134 |
| `CL05_Valby` | 1 | 11 | 16 | 1 | 5 | 10 | - | - | 62 |
| `CL06_ToxicCat` | 1 | 12 | 22 | 1 | 5 | 48 | - | - | 69 |
| `CL07_Lupa` | 1 | 14 | 17 | 2 | 4 | 14 | - | - | 72 |
| `CL08_SpearHead` | 1 | 40 | 10 | 1 | 4 | 48 | - | - | 111 |
| `CL09_Corrupted` | 2 | 11 | 15 | 4 | 6 | 12 | - | yes | 79 |
| `CL10_HoodST` | 1 | 12 | 19 | 1 | 6 | 42 | - | - | 70 |
| `CL11_SkimpyAssassin` | 1 | 5 | 26 | 1 | 1 | 76 | - | - | 50 |

### 4.1 Source mods per Outfit

| OUTFIT_ID | source plugin | in-scope mods (MO2 priority) |
|---|---|---|
| `CL01_LatexKitty` | `AE_Latex_Kitty.esp` | `makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】` (924) |
| `CL02_OnceMedic` | `AE_Once_Medic.esp` | `makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】` (923) |
| `CL03_Tachy` | `AE Stellablade Tachy.esp` | `makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】` (922) |
| `CL04_Haley` | `SSE_TFD_Haley_Black_Suit.esp` | `makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】` (921), `Haley Black Suit PBR` (884) |
| `CL05_Valby` | `AE_TFD_Valby_Nano_Suit.esp` | `makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】` (920) |
| `CL06_ToxicCat` | `AE_Toxic_Cat.esp` | `makaron-COSPLAY - AE_Toxic_Cat — 【服装·装备】【来源·本地】` (919) |
| `CL07_Lupa` | `AE_Wuthering_Waves_Lupa.esp` | `makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】` (918) |
| `CL08_SpearHead` | `BBD_CatsuitSpearhead.esp` | `矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】` (909) |
| `CL09_Corrupted` | `AE_CorruptedBodySuit.esp` | `堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】` (888), `堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】` (887) |
| `CL10_HoodST` | `AE_HoodST.esp` | `AE_HoodST — 【来源·本地】` (927) |
| `CL11_SkimpyAssassin` | `BBD Skimpy Assassin Outfit.esp` | `Skimpy Assassin 服装 - BHUNP 3BBB - CBBE 3BBB — Skimpy Assassin Outfit - BHUNP 3BBB - CBBE 3BBB — 【服装·装备】【体型·多体型】` (911) |

---

## 5. Cross-Outfit dependencies (BLOCKER class)

**Rule violation to fix before any copy happens.** These are textures whose VFS winner is the mod of a *different* Outfit in this pack. Under the independence rule they must not be silently borrowed.

| OUTFIT_ID | virtual_path | winner belongs to | note |
|---|---|---|---|
| `CL04_Haley` | `textures/ae_latex_kitty/ComplexBase_M.dds` | CL01_LatexKitty | texture won by another in-pack Outfit |
| `CL04_Haley` | `textures/ae_latex_kitty/ComplexBase_Metalic_M.dds` | CL01_LatexKitty | texture won by another in-pack Outfit |
| `CL04_Haley` | `textures/ae_latex_kitty/Dynamic_Cubemap_NULL.dds` | CL01_LatexKitty | texture won by another in-pack Outfit |
| `CL04_Haley` | `textures/ae_latex_kitty/matcap-latex-e.dds` | CL01_LatexKitty | texture won by another in-pack Outfit |
| `CL04_Haley` | `textures/ae_latex_kitty/s.dds` | CL01_LatexKitty | texture won by another in-pack Outfit |
| `CL07_Lupa` | `textures/ae_latex_kitty/d1.dds` | CL01_LatexKitty | texture won by another in-pack Outfit |
| `CL07_Lupa` | `textures/ae_latex_kitty/matcap-latex-e.dds` | CL01_LatexKitty | texture won by another in-pack Outfit |
| `CL07_Lupa` | `textures/ae_latex_kitty/metal.dds` | CL01_LatexKitty | texture won by another in-pack Outfit |
| `CL07_Lupa` | `textures/ae_latex_kitty/metal02.dds` | CL01_LatexKitty | texture won by another in-pack Outfit |
| `CL07_Lupa` | `textures/ae_latex_kitty/n.dds` | CL01_LatexKitty | texture won by another in-pack Outfit |
| `CL07_Lupa` | `textures/ae_latex_kitty/s.dds` | CL01_LatexKitty | texture won by another in-pack Outfit |
| `CL09_Corrupted` | `textures/ae_latex_kitty/n.dds` | CL01_LatexKitty | texture won by another in-pack Outfit |
| `CL10_HoodST` | `textures/ae_latex_kitty/d1.dds` | CL01_LatexKitty | texture won by another in-pack Outfit |
| `CL10_HoodST` | `textures/ae_latex_kitty/n.dds` | CL01_LatexKitty | texture won by another in-pack Outfit |

**Out-of-pack winners shipped inside an in-pack mod folder** (pack-boundary collision):

| OUTFIT_ID | virtual_path | winning mod |
|---|---|---|
| `CL01_LatexKitty` | `meshes/harry2135/fantasyseries6/smpxml/fs6_hoodedcloak_3ba_smp.xml` | 00 资源·H2135 披风物理补全 — H2135 Cloak SMP Physics |
| `CL01_LatexKitty` | `meshes/harry2135/fantasyseries6/smpxml/fs6_hoodedcloak_folded_3ba_smp.xml` | 00 资源·H2135 披风物理补全 — H2135 Cloak SMP Physics |
| `CL01_LatexKitty` | `meshes/harry2135/fantasyseries6/smpxml/fs6_hoodedcloak_hair_3ba_smp.xml` | 00 资源·H2135 披风物理补全 — H2135 Cloak SMP Physics |
| `CL01_LatexKitty` | `meta.ini` | Nyes Latex Pack AiO 1.3 (ReducedSize) |
| `CL02_OnceMedic` | `meta.ini` | Nyes Latex Pack AiO 1.3 (ReducedSize) |
| `CL03_Tachy` | `meta.ini` | Nyes Latex Pack AiO 1.3 (ReducedSize) |
| `CL04_Haley` | `meshes/harry2135/fantasyseries6/smpxml/fs6_hoodedcloak_3ba_smp.xml` | 00 资源·H2135 披风物理补全 — H2135 Cloak SMP Physics |
| `CL04_Haley` | `meshes/harry2135/fantasyseries6/smpxml/fs6_hoodedcloak_folded_3ba_smp.xml` | 00 资源·H2135 披风物理补全 — H2135 Cloak SMP Physics |
| `CL04_Haley` | `meshes/harry2135/fantasyseries6/smpxml/fs6_hoodedcloak_hair_3ba_smp.xml` | 00 资源·H2135 披风物理补全 — H2135 Cloak SMP Physics |
| `CL04_Haley` | `meta.ini` | Nyes Latex Pack AiO 1.3 (ReducedSize) |
| `CL05_Valby` | `meta.ini` | Nyes Latex Pack AiO 1.3 (ReducedSize) |
| `CL06_ToxicCat` | `meta.ini` | Nyes Latex Pack AiO 1.3 (ReducedSize) |
| `CL07_Lupa` | `meta.ini` | Nyes Latex Pack AiO 1.3 (ReducedSize) |
| `CL08_SpearHead` | `meta.ini` | Nyes Latex Pack AiO 1.3 (ReducedSize) |
| `CL09_Corrupted` | `meta.ini` | Nyes Latex Pack AiO 1.3 (ReducedSize) |
| `CL10_HoodST` | `meta.ini` | Nyes Latex Pack AiO 1.3 (ReducedSize) |
| `CL11_SkimpyAssassin` | `meta.ini` | Nyes Latex Pack AiO 1.3 (ReducedSize) |

---

## 6. Collisions

| kind | count |
|---|---|
| `MO2_RESERVED_NAME` | 12 |
| `VFS_OVERRIDE` | 42 |

* `MO2_RESERVED_NAME` -- `meta.ini` is offered by 54 mods at once. It is MO2/FOMOD bookkeeping, never a game asset, and is excluded from the migratable set.
* `VFS_OVERRIDE` -- a real content path is offered by more than one mod. The winner is the lower MO2 priority number; the loser is preserved in `shadowed_providers`.

---

## 7. Unknowns and manual-confirmation list

| UNKNOWN / BLOCKER class | count |
|---|---|
| `REACHABLE_UNRESOLVED_BASE` | 94 |
| `REACHABLE_UNRESOLVED_INSTANCE` | 81 |
| `UNRESOLVED_MODEL_PATH` | 70 |
| `EXTERNAL_TEXTURE_WINNER` | 35 |
| `OUT_OF_PACK_WINNER` | 17 |
| `PENDING_BODYSLIDE_BUILD` | 17 |
| `ORPHAN_SHAPEDATA_NO_OSP` | 10 |
| `PHYSICS_MESH_UNRESOLVED` | 9 |
| `P00_SHAPEDATA_COUNT_MISMATCH` | 1 |

> **P02A.1 SUPERSEDES part of this table.** The classes `REACHABLE_MISSING_DEPENDENCY` (81) and `REACHABLE_UNRESOLVED_BASE` (94) were derived by asking the *frozen P00 index*, which covers only the 56 TARGET09 mods. The P02A.1 full-instance lookup replaced that judgement: section 15 is authoritative for every one of these references. The counts below survive only as the original P00-index-scoped reading.


### 7.1 Items needing a human decision

1. **ARMO/ARMA stock placeholders** (`meshes\Armor\Studded\Male\*.nif`, `meshes\bbdrac\<...>\Body_1.nif` etc.). Not present as loose files: Skyrim base-game `Data` is BSA-packed and a path-existence check cannot see inside an archive (section 21). Recorded, never guessed. Their role is fixed by ruling 1, so these are MALE-side stock placeholders, not female wearables.
2. **Unbound physics XML.** `tailplug.xml`, `sparklers.xml`, `coat.xml` and the three `fs6_hoodedcloak*_smp.xml` carry no mesh element and have no same-folder `<stem>.nif`. The real target cannot be derived without fuzzy matching, which P02A forbids. All are BLOCKER / PHYSICS_MESH_UNRESOLVED.
3. **RETRACTED by the P02A.1 audit.** The earlier claim that these third-party texture references are `genuinely broken, not index gaps` used a now-forbidden method: *not present in the frozen P00 TARGET09 index, therefore not in the MO2 instance*. A full lookup over all 2253 mod directories has disproved it for most of these paths. Section 15 is authoritative; nothing here may be read as `broken at runtime today`.
4. **Malformed NIF texture slot** holding the bare token `textures\` (`fo4boots slided.nif`, CL08). Author bug in the source mesh.
5. **Orphan ShapeData** -- a ShapeData NIF/OSD that wins the VFS for an Outfit but whose folder no .osp claims, so BodySlide would never build it. See section 8.
6. **P00 metadata disagreement** -- `bs_projects.shapedata_nif_count` disagrees with the frozen file index for CL08. This script trusts the frozen file index plus the .osp data folder and records the disagreement.
7. **Unbuilt BodySlide outputs** -- every .osp EXACT_OUTPUT_PATH build target is absent from the VFS because no build has run. Recorded as PENDING_BUILD; P02A does not build.

---

## 8. Per-Outfit structural findings

### `CL01_LatexKitty`

* **2 .osp projects** (calientetools/bodyslide/slidersets/ae_latex_kitty.osp, calientetools/bodyslide/slidersets/ae_latex_kitty_tail.osp) Resolved by P02A.1 ruling 5: exactly one target OSP per Outfit, several SliderSets inside it. The per-part `__<Part>` filename candidate is **withdrawn**; see section 17, including its load-verification risk.

### `CL02_OnceMedic`

* **2 .osp projects** (calientetools/bodyslide/slidersets/ae_once_combat_medi_vail.osp, calientetools/bodyslide/slidersets/ae_once_combat_medic.osp) Resolved by P02A.1 ruling 5: exactly one target OSP per Outfit, several SliderSets inside it. The per-part `__<Part>` filename candidate is **withdrawn**; see section 17, including its load-verification risk.

### `CL03_Tachy`

* no structural exception: single .osp, no orphan ShapeData, no rework layer.

### `CL04_Haley`

* PBR patch mod `Haley Black Suit PBR` (priority 884) beats the base mod (921) and owns `textures\pbr\...` + `pbrnifpatcher\...` with no path collision.

### `CL05_Valby`

* no structural exception: single .osp, no orphan ShapeData, no rework layer.

### `CL06_ToxicCat`

* no structural exception: single .osp, no orphan ShapeData, no rework layer.

### `CL07_Lupa`

* **2 .osp projects** (calientetools/bodyslide/slidersets/ae_wuthering_waves_lupa.osp, calientetools/bodyslide/slidersets/ae_wuthering_waves_lupa_mant.osp) Resolved by P02A.1 ruling 5: exactly one target OSP per Outfit, several SliderSets inside it. The per-part `__<Part>` filename candidate is **withdrawn**; see section 17, including its load-verification risk.

### `CL08_SpearHead`

* P00 `shapedata_nif_count` mismatch on: `CalienteTools/bodyslide/SliderSets/Spearhead Catsuit 3BA.osp`

### `CL09_Corrupted`

* **4 .osp projects** (calientetools/bodyslide/slidersets/ae_corruptedbodysuit.osp, calientetools/bodyslide/slidersets/ae_corruptedbodysuit_hand.osp, calientetools/bodyslide/slidersets/ae_corruptedbodysuit_head.osp, calientetools/bodyslide/slidersets/ae_corruptedbodysuit_mask.osp) Resolved by P02A.1 ruling 5: exactly one target OSP per Outfit, several SliderSets inside it. The per-part `__<Part>` filename candidate is **withdrawn**; see section 17, including its load-verification risk.
* **Orphan ShapeData** (no .osp data folder claims them): `calientetools/bodyslide/shapedata/ae_corruptedbodysuit.nif`, `calientetools/bodyslide/shapedata/ae_corruptedbodysuit_feet.nif`, `calientetools/bodyslide/shapedata/ae_corruptedbodysuit_hand.nif`, `calientetools/bodyslide/shapedata/ae_corruptedbodysuit_head.nif`, `calientetools/bodyslide/shapedata/ae_corruptedbodysuit_mask.nif`, `calientetools/bodyslide/shapedata/ae_corruptedbodysuit_neck.nif`
* **REWORK / BodySlide split**: the rework mod wins 23 game asset(s) from `堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】` but every .osp, ShapeData NIF and OSD still comes from the base mod (16 file(s)). Once BodySlide builds and PGPatcher swaps the worn meshes, the visible shape geometry will be the BASE ShapeData while the rework only contributes its textures. Manual confirmation required before any build.
* Latex Rework mod `堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】` (priority 887) beats the base mod (888) and is the VFS winner for its meshes/textures.

### `CL10_HoodST`

* no structural exception: single .osp, no orphan ShapeData, no rework layer.

### `CL11_SkimpyAssassin`

* **Orphan ShapeData** (no .osp data folder claims them): `calientetools/bodyslide/shapedata/cbbe se - skimpy assassin cuirass/cbbe se - skimpy assassin cuirass.nif`, `calientetools/bodyslide/shapedata/cbbe se - skimpy assassin cuirass/cbbe se - skimpy assassin cuirass.osd`, `calientetools/bodyslide/shapedata/cbbe se - skimpy assassin gloves/cbbe se - skimpy assassin gloves.nif`, `calientetools/bodyslide/shapedata/cbbe se - skimpy assassin gloves/cbbe se - skimpy assassin gloves.osd`
* `NON_CANONICAL_BODY=BHUNP_3BBB` -- annotated only; nothing is deleted in P02A.

---

## 9. Shared-material proposals

Byte-identical assets appearing under more than one Outfit are **not** merged in P02A. They are listed here only so P05 has a verified starting set.

| asset_type | sha256 (12) | Outfits |
|---|---|---|
| DDS | `775d2ba7ba87` | CL01_LatexKitty, CL04_Haley, CL09_Corrupted |
| DDS | `a49d6de5ccb1` | CL01_LatexKitty, CL04_Haley, CL09_Corrupted |
| DDS | `fafc0d9eba56` | CL01_LatexKitty, CL04_Haley |
| DDS | `d51feefc92a5` | CL01_LatexKitty, CL04_Haley |
| DDS | `fe15587e43e3` | CL01_LatexKitty, CL04_Haley |
| DDS | `de37d3199bbd` | CL01_LatexKitty, CL04_Haley |
| DDS | `f69ab0153210` | CL01_LatexKitty, CL04_Haley |
| DDS | `7389606550e4` | CL01_LatexKitty, CL04_Haley |
| DDS | `a62c83ba9342` | CL01_LatexKitty, CL04_Haley |
| DDS | `07291e75f588` | CL01_LatexKitty, CL04_Haley |
| DDS | `9ccbdf82cc9d` | CL01_LatexKitty, CL04_Haley |
| DDS | `fac660d86a71` | CL01_LatexKitty, CL04_Haley |
| DDS | `02ae0ce1873c` | CL01_LatexKitty, CL04_Haley |
| DDS | `9f835c76d705` | CL01_LatexKitty, CL04_Haley |
| DDS | `184b356a6ae6` | CL01_LatexKitty, CL04_Haley |
| DDS | `5918a0b44c85` | CL01_LatexKitty, CL04_Haley |
| DDS | `de2e67ec1898` | CL02_OnceMedic, CL04_Haley |

Shared-resource whitelist: **NONE**. Status of every item above: `PROPOSAL_SHARED_NOT_APPROVED`. No `Shared` directory is created by P02A.

---

## 10. Statistics

| OUTFIT_ID | rows | UNKNOWN | BLOCKER | collisions |
|---|---|---|---|---|
| `CL01_LatexKitty` | 105 | 21 | 27 | 4 |
| `CL02_OnceMedic` | 109 | 15 | 16 | 1 |
| `CL03_Tachy` | 55 | 10 | 7 | 1 |
| `CL04_Haley` | 134 | 19 | 27 | 5 |
| `CL05_Valby` | 62 | 10 | 12 | 1 |
| `CL06_ToxicCat` | 69 | 14 | 9 | 1 |
| `CL07_Lupa` | 72 | 11 | 19 | 1 |
| `CL08_SpearHead` | 111 | 15 | 33 | 1 |
| `CL09_Corrupted` | 79 | 17 | 14 | 37 |
| `CL10_HoodST` | 70 | 10 | 9 | 1 |
| `CL11_SkimpyAssassin` | 50 | 2 | 11 | 1 |
| **TOTAL** | **916** | **144** | **184** | **54** |

`asset_type` distribution:

| asset_type | rows |
|---|---|
| `DDS` | 475 |
| `GAME_NIF` | 255 |
| `SHAPEDATA_NIF` | 59 |
| `OSD` | 52 |
| `OTHER` | 20 |
| `OSP` | 17 |
| `CONFIG` | 13 |
| `PLUGIN` | 12 |
| `PHYSICS_XML` | 9 |
| `PBR_JSON` | 4 |

`relationship` distribution:

| relationship | rows |
|---|---|
| `BASE_MOD` | 404 |
| `NONE` | 316 |
| `BODYSLIDE_CONVERSION` | 139 |
| `LATEX_REWORK` | 29 |
| `PBR_PATCH` | 19 |
| `PHYSICS_PATCH` | 9 |

`status` distribution:

| status | rows |
|---|---|
| `OK` | 588 |
| `BLOCKER` | 184 |
| `UNKNOWN` | 144 |

---

## 11. Re-running

```
python tools\P02A\p02a_sourcemap.py
```

Deterministic: it reads only the frozen P00 evidence set through `tools/P02A/p02a_common.py`, re-derives every winner, and rewrites both deliverables. It never writes outside `reports/P02A/`.

<!-- P02A.1-V2-BEGIN -->

---

## 12. P02A.1 revision log (manual audit, authoritative)

Everything from section 12 onward is the **P02A.1 manual-audit ruling** and overrides any earlier statement in this document. Sections 0-11 stay valid except where an amendment note says otherwise.

| # | ruling |
|---|---|
| 1 | ARMA/ARMO model slot semantics are fixed by subrecord; guessing from the path name is forbidden |
| 2 | `*.tri` is `BODY_MORPH_TRI`, in the BodySlide morph table, not physics |
| 3 | The global VFS provider lookup supersedes the frozen-index method |
| 4 | `GLOBAL_BODY_SKIN` textures stay external, never copied into an Outfit namespace |
| 5 | OSP rule frozen: exactly 11 target OSPs, one per Outfit |
| 6 | Statistics vocabulary fixed: ShapeData files vs rewrite rows differ |
| 7 | CL09 follows `CL09_REWORK_VS_BODYSLIDE_DECISION.md` |
| 8 | New blocker: the live body-skin winner is not CBBE_3BA |
| 9 | The BSA blind spot is an explicit, declared limitation |

---

## 13. ARMA / ARMO model slot semantics (ruling 1)

A model path's role is decided **only** by which subrecord carries it. Inferring the role from the path or file name is forbidden, because one file name is reused across roles.

| record | subrecord | role semantics (layer a) | model_role literal (layer b) | system |
|---|---|---|---|---|
| `ARMA` | `MOD2` | `MALE_3RD_PERSON` | `WEARABLE_MALE_3P` | ArmorAddon, worn |
| `ARMA` | `MOD3` | `FEMALE_3RD_PERSON` | `WEARABLE_FEMALE_3P` | ArmorAddon, worn |
| `ARMA` | `MOD4` | `MALE_1ST_PERSON` | `FIRSTPERSON_MALE` | ArmorAddon, worn |
| `ARMA` | `MOD5` | `FEMALE_1ST_PERSON` | `FIRSTPERSON_FEMALE` | ArmorAddon, worn |
| `ARMO` | `MOD2` | `MALE_WORLD_MODEL` | `WORLD_MALE` | inventory / drop / world model -- **never a wearable mesh** |
| `ARMO` | `MOD4` | `FEMALE_WORLD_MODEL` | `WORLD_FEMALE` | inventory / drop / world model -- **never a wearable mesh** |

### 13.1 The frozen model_role enum (layer b)

These six literals are what the model_role column must contain:

* `WEARABLE_MALE_3P` -- meaning: MALE_3RD_PERSON
* `WEARABLE_FEMALE_3P` -- meaning: FEMALE_3RD_PERSON
* `FIRSTPERSON_MALE` -- meaning: MALE_1ST_PERSON
* `FIRSTPERSON_FEMALE` -- meaning: FEMALE_1ST_PERSON
* `WORLD_MALE` -- meaning: MALE_WORLD_MODEL
* `WORLD_FEMALE` -- meaning: FEMALE_WORLD_MODEL

### 13.2 Why the role is what it is (layer a)

Layer (a) is the *decision basis*: the subrecord a path arrives in fixes the role. Inferring the role from the path or file name is forbidden, because one file name is reused across roles. Layer (b) is only the column vocabulary; it never overrides layer (a).

**Canonical body is CBBE_3BA female**, so `WEARABLE_FEMALE_3P` is the canonical runtime wearable mesh. Every other role keeps its provenance but must not be mixed into the canonical female set, and a `WORLD_*` role must never be promoted to a worn mesh.

---

## 14. `.tri` ownership (ruling 2)

`*.tri` is **always** `BODY_MORPH_TRI`: a Havok body-morph morph cache, not a physics config.

* target table: `P02A_BODYSLIDE_MORPH_MIGRATION.csv`
* role value `BODY_MORPH_TRI` -- never `PHYSICS_XML`, never a physics `config_type`

Current state of `P02A_PHYSICS_MIGRATION.csv`: **0 row(s) still carry a `.tri` file** and 0 of them still use a Havok-style `config_type`. That is a defect against this ruling, reported by the verifier (check 3).

`P02A_BODYSLIDE_MORPH_MIGRATION.csv` present: **yes**.

---

## 15. Global VFS provider lookup (ruling 3) -- supersedes the old method

> ### RETRACTED METHODOLOGY
> The earlier P02A conclusion *`this path is absent from the frozen P00 TARGET09 index, therefore the reference is missing or broken at runtime`* is **wrong and is withdrawn**. The P00 file index covers only the 56 mods inside the pack scope; it says nothing about the 2253-directory MO2 instance. Judging instance-wide absence from it is invalid.

What replaces it: a targeted provider lookup over the whole instance (`p02a_vfs_lookup.py` -> `P02A_GLOBAL_PROVIDER_LOOKUP.csv`). It checks every candidate path under all 2253 mod directories plus the game `Data` root, then -- for anything it misses -- sweeps the whole mods tree by file name, so that `really absent` is separable from `the author shipped it under another folder`. No binary was opened; this is path existence only.

### 15.1 Result over the 75 distinct virtual paths

| classification | count | meaning |
|---|---|---|
| `EXTERNAL_PROVIDER_FOUND` | 40 | a mod or loose game file provides the referenced path |
| `UNKNOWN` | 8 | no provider at the path; a same-name file exists elsewhere, identity unproven |
| `TRUE_MISSING` | 12 | no provider anywhere at the loose-file layer (section 21) |
| `GLOBAL_BODY_SKIN` | 12 | body/skin system texture -- section 16 |
| `VANILLA_ENGINE_RESOURCE` | 3 | stock Skyrim Data root; almost certainly BSA-packed, unverified |

Size of the correction: of the 58 references the earlier round labelled `EXTERNAL_MOD_MISSING`, **40** are served by a real mod at the referenced path.

### 15.2 `UNKNOWN` -- path mismatch, deliberately **not** auto-repointed

These have no provider at the referenced path, but the same file name exists elsewhere in the instance. Treating that as `the same asset` would be fuzzy matching, which this stage forbids, so they are **not** upgraded to `EXTERNAL_PROVIDER_FOUND` and **no automatic REPOINT is authorised**. Each keeps its candidate location in the CSV for a human to confirm.

| virtual_path | candidate location (identity unproven) |
|---|---|
| `textures/1nye/catsuit/leotard_n.dds` | `textures/armor/bdor/poetica/Leotard_n.dds` |
| `textures/1nye/colors/gray.dds` | `textures/Creation Club better cubemaps/gray.dds` |
| `textures/1nye/cubemaps/flatnormal.dds` | `textures/NyesLatexPack/flatnormal.dds` |
| `textures/1nye/cubemaps/studio.dds` | `Textures/KS Hairdo's/HDT/Studio.dds` |
| `textures/armor/[trx]  latexwhitch/zad_ebonite_e.dds` | `textures/devious/expansion/zad_Ebonite_e.dds` |
| `textures/pc_010_u_cmn_001_body_parta_n.dds` | `Textures/AE_TFD_Valby_Nano_Suit/PC_010_U_CMN_001_Body_PartA_N.dds` |
| `textures/predator/latex bodysuits/complexbase_m.dds` | `Textures/AE_Latex_Kitty/ComplexBase_M.dds` |
| `textures/predator/latex bodysuits/dynamic_cubemap_null.dds` | `Textures/Predator/Slave Chastity Harness/Dynamic_Cubemap_NULL.dds` |

### 15.3 `TRUE_MISSING` -- recorded as a known defect

Kept `UNRESOLVED` on purpose. **No downgrade, exclusion or substitution scheme is fabricated for them**; they remain an open defect list for a human ruling.

| virtual_path | affected outfits |
|---|---|
| `textures/1nye/cubemaps/flatcubemap.dds` |  |
| `textures/ae_curse_bunny/latex/d.dds` |  |
| `textures/ae_curse_bunny/pink022.dds` |  |
| `textures/ae_curse_bunny/shkurka_body_mask.dds` |  |
| `textures/caenarvon/cosplay/bunny/8_d.dds` |  |
| `textures/caenarvon/cosplay/bunny/8_m.dds` |  |
| `textures/caenarvon/cosplay/bunny/8_n.dds` |  |
| `textures/harry2135/fantasyseries6/cubemaps/basilica.dds` |  |
| `textures/harry2135/fantasyseries6/fs6_hooded_cloak_ro_m.dds` |  |
| `textures/kziitd/cloth/2.2/suit_ring.dds` |  |
| `textures/kziitd/cloth/2.2/suit_ring_n.dds` |  |
| `textures/sse_tfd_haley_black_suit/pc_016_a_cmn_002_parta_m.dds` |  |

Two are author-side defects rather than install gaps: `textures\sse_tfd_haley_black_suit\pc_016_a_cmn_002_parta_m.dds` (that mod ships `_c`, `_n`, `_p` but never `_m`) and the `8_d / 8_m / 8_n.ddstextures\caenarvon\cosplay\bunny set under ``` (only the Basics, Gala and Magecore variants of that pack are installed).

---

## 16. `GLOBAL_BODY_SKIN` rule (ruling 4)

These paths belong to the body / skin system:

```
textures\actors\character\female\femalebody_1*.dds
textures\actors\character\female\femalebody_etc_v2_1*.dds
textures\actors\character\female\femalehands_1*.dds
textures\actors\character\female\femalebody_1_sk.dds
```

**Rule: keep the external reference. NEVER copy them into `textures\ZLJ\CombatLatex\<OUTFIT_ID>`.** They are the shared body skin, not outfit material; vendoring them would fork the canonical CBBE_3BA female skin into eleven private copies. Any future handling belongs to a UBE / 3BA body-family migration, not to this pack.

Affected references in the current audit: **12**.

---

## 17. OSP rule frozen (ruling 5)

**One Outfit = exactly one target OSP, with several SliderSets inside it. The pack therefore has exactly 11 OSP files:**

```
CalienteTools\BodySlide\SliderSets\ZLJ_<OUTFIT_ID>.osp      x 11
```

| OUTFIT_ID | target OSP |
|---|---|
| `CL01_LatexKitty` | `CalienteTools\BodySlide\SliderSets\ZLJ_CL01_LatexKitty.osp` |
| `CL02_OnceMedic` | `CalienteTools\BodySlide\SliderSets\ZLJ_CL02_OnceMedic.osp` |
| `CL03_Tachy` | `CalienteTools\BodySlide\SliderSets\ZLJ_CL03_Tachy.osp` |
| `CL04_Haley` | `CalienteTools\BodySlide\SliderSets\ZLJ_CL04_Haley.osp` |
| `CL05_Valby` | `CalienteTools\BodySlide\SliderSets\ZLJ_CL05_Valby.osp` |
| `CL06_ToxicCat` | `CalienteTools\BodySlide\SliderSets\ZLJ_CL06_ToxicCat.osp` |
| `CL07_Lupa` | `CalienteTools\BodySlide\SliderSets\ZLJ_CL07_Lupa.osp` |
| `CL08_SpearHead` | `CalienteTools\BodySlide\SliderSets\ZLJ_CL08_SpearHead.osp` |
| `CL09_Corrupted` | `CalienteTools\BodySlide\SliderSets\ZLJ_CL09_Corrupted.osp` |
| `CL10_HoodST` | `CalienteTools\BodySlide\SliderSets\ZLJ_CL10_HoodST.osp` |
| `CL11_SkimpyAssassin` | `CalienteTools\BodySlide\SliderSets\ZLJ_CL11_SkimpyAssassin.osp` |

UI name for every slider set inside: `[ZLJ Combat Latex] <Outfit> - <Part>` (example: `[ZLJ Combat Latex] Haley - Bodysuit`).

ShapeData keeps the per-Outfit folder; an OSD may exist per project:

```
CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\<OUTFIT_ID>\...
```

### 17.1 Risk warning -- read before any P02B migration

> Merging several slider sets into a single `.osp` **departs from BodySlide's standard one-OSP-per-slider-set behaviour**. The UI, slider enumeration and per-set metadata of a multi-set OSP are not equivalent to N separate OSPs.
>
> **P02B must first run one load verification**: open the merged OSP in BodySlide, confirm every slider set loads, every slider appears, and the build output matches the per-set baseline. **Until that verification passes, no batch migration may be based on this rule.**

Current state of `P02A_BODYSLIDE_MIGRATION.csv`: 11 distinct `new_osp` value(s), 0 of them outside the frozen 11. Those must be collapsed before any P02B work.

---

## 18. Statistics vocabulary (ruling 6) -- do not conflate these

| symbol | meaning | value |
|---|---|---|
| `SHAPEDATA_NIF_FILES` | **distinct ShapeData NIF files** | **59** |
| `SHAPEDATA_TEXTURE_REWRITE_ROWS` | **shape x texture-slot rewrite rows** | 1096 |

### 18.1 Splitting the ShapeData count

The ShapeData file count is **not** simply the 59 a texture-rewrite table sees. It splits by whether an .osp data folder claims the file:

| slice | count | meaning |
|---|---|---|
| OSP-claimed | 51 | inside a data folder a .osp declares; BodySlide will build these |
| orphan | 8 | no .osp claims the folder, so BodySlide would never build them |
| **total `SHAPEDATA_NIF_FILES`** | **59** | |

The 8 orphan files are the CL09 flat ShapeData NIFs (6, adopted by the CL09 rework decision) and the CL11 CBBE SE Skimpy Assassin cuirass and gloves NIFs (2). A texture rewrite table that only walks OSP-claimed folders therefore under-reports the ShapeData inventory -- do not derive one number from the other.

> **1096 is NOT the number of ShapeData NIFs.** The 1096 rewrite rows are one row per (ShapeData NIF, shape, texture slot) triple over 59 distinct files. Writing `1096 ShapeData NIF` is a category error and is forbidden.

### 18.2 Four-class reconciliation of the .nif inventory

| class | count | meaning |
|---|---|---|
| `SHAPEDATA_SOURCE_NIF` | 59 | ShapeData input BodySlide consumes |
| `BODYSLIDE_OUTPUT_NIF` | 93 | meshes produced by a .osp build |
| `BODY_MORPH_TRI` | 11 | *.tri morph caches (section 14) |
| `GAME_NIF` | 75 | meshes the plugin points at today |
| **total distinct .nif virtual paths** | **238** | |

### 18.3 The four classes are not interchangeable

| class | meaning |
|---|---|
| `GAME_NIF` | a mesh the plugin points at today (worn or world model) |
| `BODYSLIDE_OUTPUT_NIF` | the .osp EXACT_OUTPUT_PATH a build produces |
| `SHAPEDATA_SOURCE_NIF` | a ShapeData input BodySlide consumes to produce the above |
| `BODY_MORPH_TRI` | a *.tri morph cache, morph table only (section 14) |

Note: the 17 .osp EXACT_OUTPUT_PATH targets are **not present in the VFS** until a build runs; they are carried as PENDING_BUILD and P02A never builds them.
---

## 19. CL09_Corrupted decision reference (ruling 7)

CL09 follows `reports\P02A\CL09_REWORK_VS_BODYSLIDE_DECISION.md`:

* canonical source decision: `REWORK_BACKPORTED_TO_SHAPEDATA`
* **CL09 stays `BLOCKED`** until a P02B trial build validates recommendation R2 against the current runtime mesh. The residual 12/24-byte delta in the overridden meshes has not been decoded to a named NIF field, so a wrong backport would silently alter the outfit's shape for every future slider change.
* until that build passes, no CL09 file may be copied into the Pack namespace.
* R4 restates ruling 4: femalebody_* / femalehands_* references stay external as `GLOBAL_BODY_SKIN` and are never copied.

---

## 20. NEW BLOCKER -- the live body skin is not CBBE_3BA (ruling 8)

> ### BLOCKER: cross-body compatibility risk
>
> The 12 `GLOBAL_BODY_SKIN` paths are **not** served by stock CBBE_3BA in this instance.
>
> Live providers of those 12 paths, in MO2 priority order (lowest wins):
>
> - `BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】` -- priority **1133**, serves 12 of 12 paths
> - `CBBE 3BA (3BBB) — 【体型·CBBE+3BA】【作者·Acro】` -- priority **1180**, serves 4 of 12 paths
> - `Caliente's Beautiful Bodies Enhancer -CBBE — 【体型·CBBE】` -- priority **1181**, serves 8 of 12 paths
>
>
> **This is not all-or-nothing.** Three mods each win a share of the nine paths (9/9, 6/9 and 3/9 above), so the pack is not uniformly on one foreign body: some references resolve to BnP skin, some to CBBE. The override is partial and per-path, which makes it harder to notice and no less real.
>
> So the 11 canonical Outfits resolve their body skin against a **different body**, not the CBBE_3BA texture the pack nominally targets. A mesh authored for CBBE_3BA can render with another body's skin -- tint, gloss and body-map alignment all shift. This is a real compatibility risk, not a cosmetic one, and it needs a human ruling.

Per ruling 4 nothing is copied to `fix` it: the references stay external. The decision needed is whether the pack targets the CBBE_3BA body *system* (accepting that the instance's body pack supplies the skin) or the specific stock texture.

---

## 21. BSA blind spot -- explicit limitation (ruling 9)

The game E:\SkyrimAE\Data root has **no loose textures directory at all**; the base game is carried by **93 .bsa archives**. A path-existence check cannot see inside an archive.

Therefore:

* `found_in_game_data` is `no` for **every** row of the lookup table.
* `TRUE_MISSING` and `VANILLA_ENGINE_RESOURCE` prove only **absent at the loose-file layer**. They do **not** prove absence from the instance.
* The same caveat applies to the ARMO/ARMA stock placeholders in section 7.1.

This limitation is stated on every row of `P02A_GLOBAL_PROVIDER_LOOKUP.csv` in its lookup_scope column. **Closing it requires a separate read-only archive-listing task; this stage does not touch archives.**

---

## 22. Reproducible verification

tools\P02A\p02a_architecture_v2.py re-derives every number above from the tables and runs three mandated checks:

| check | rule |
|---|---|
| 1 | exactly 11 target OSPs, one per OUTFIT_ID, no per-part filename |
| 2 | model_role uses only the 6 frozen subrecord-derived values |
| 3 | the physics table contains no .tri and no Havok morph row |

A FAIL is reported, never silently absorbed. The result prints at the end of every run.

---

## 23. P02A.1 status -- what is still not authorised

| item | ruling |
|---|---|
| 8 UNKNOWN path-mismatch references | **no automatic REPOINT authorised**; stay UNKNOWN for human confirmation |
| 12 TRUE_MISSING references | stay UNRESOLVED as a known defect list; **no downgrade or exclusion scheme invented** |
| model_role naming | the ARMA/ARMO table maps every subrecord 1:1 to the correct role, but spells the six values WEARABLE_MALE_3P / WEARABLE_FEMALE_3P / FIRSTPERSON_MALE / FIRSTPERSON_FEMALE / WORLD_MALE / WORLD_FEMALE instead of the frozen names in section 13. Semantics PASS, literal names FAIL. Either the table adopts the frozen names or the ruling relaxes them; **not decided here** |
| body-skin override (section 20) | recorded as a blocker, awaiting human ruling |
| BSA blind spot (section 21) | declared; closure deferred to a separate read-only archive-listing task |
| merged-OSP load verification (section 17.1) | required in P02B **before** any batch migration |
| CL09 trial build (section 19) | required in P02B before any CL09 copy |

P02B must not begin on the strength of this document alone.

---

## 24. Evidence freshness and MO2 instance drift

> The P00 evidence is a **frozen snapshot**. The live MO2 instance moved during P02A. Every priority-derived number in this document is a *frozen-time* reading, and that distinction is load-bearing.

### 24.1 The drift

| | frozen (P00, 2026-09-30 03:53 UTC) | current |
|---|---|---|
| modlist.txt lines | 2254 | **2256** |
| mod directories | 2253 | **2255** |

The instance drifted while P02A was running. All 11 source mods changed line number:

| Outfit | mod | frozen | current |
|---|---|---|---|
| `CL01_LatexKitty` | makaron-COSPLAY - AE_Latex_Kitty | 924 | **926** |
| `CL02_OnceMedic` | makaron-COSPLAY - AE_Once_Medic | 923 | **925** |
| `CL03_Tachy` | makaron-COSPLAY - AE_Stellablade_Tachy | 922 | **924** |
| `CL04_Haley` | makaron-COSPLAY - AE_TFD_Haley_Black_Suit | 921 | **922** |
| `CL04_Haley` | Haley Black Suit PBR | 884 | **885** |
| `CL05_Valby` | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit | 920 | **921** |
| `CL06_ToxicCat` | makaron-COSPLAY - AE_Toxic_Cat | 919 | **920** |
| `CL07_Lupa` | makaron-COSPLAY - AE_Wuthering_Waves_Lupa | 918 | **919** |
| `CL08_SpearHead` | SpearHead Catsuit CBBE 3BA BS | 909 | **907** |
| `CL09_Corrupted` | AE Corrupted Body Suit (base) | 888 | **917** |
| `CL09_Corrupted` | AE Corrupted Body Suit - Latex Rework | 887 | **916** |
| `CL10_HoodST` | AE_HoodST | 927 | **929** |
| `CL11_SkimpyAssassin` | Skimpy Assassin Outfit | 911 | **909** |

### 24.2 Four priority inversions -- and why none of them matter here

The move produces **4 pairwise inversions**: `CL08` against `CL09` base and rework, and `CL09` base and rework against `CL11`.

**None of them changes any asset winner determination in this Pack.** Verified:

* The only virtual path `CL08`, `CL09` and `CL11` share is `meta.ini` -- MO2 bookkeeping, never a game asset, and excluded from the migratable set. **The three share no asset path at all.**
* The only genuine asset-level conflict is `CL09` base versus `CL09` rework, and its relative order holds in *both* states: rework stays ahead (887 < 888 frozen, 916 < 917 current). The Latex Rework remains the VFS winner, so section 19's REWORK decision is unaffected.

### 24.3 Limitation

P02A.1 is **forbidden from rescanning P00/P01**. Every P00-derived priority in this document is therefore a frozen-time reading and may already differ from the live instance. Concretely, the body-skin priorities quoted in section 20 (BnP 1133, CBBE 3BA 1180, CBBE Enhancer 1181) come from a fresh instance read, while the section 2 winner rule operates on the frozen snapshot.

> **If the instance keeps drifting before P02B starts, P00 must be re-frozen before any COPY is executed.** No migration may be carried out against a stale priority reading.

Case note: `FemaleBody_1_sk.dds` and `femalebody_1_sk.dds` are the same file on Windows and are absorbed by the lookup key normalisation. Only one row exists; no duplicate recording is needed.
### 24.4 Concurrent external modification of the MO2 instance (Lead addendum)

The drift in 24.1 was not an isolated event. While P02A.1 was running, a **separate process or person** was actively
modifying the instance. Measured from timestamps inside `E:\SkyrimAE\mo2\mods`:

| time | mod | what changed |
|---|---|---|
| 21:44 - 22:32 | `OutfitGallery 1.0.4` | mod files, `SKSE\Plugins\OutfitGallery.dll`, `meta.ini` |
| 22:47:39 | `Stellar Blade Tachy PBR` | `meta.ini` |
| 22:52:11 | `输出·BodySlide Output` | `Log_OS.txt`, `OutfitStudio.xml` |
| 22:59:10 | `TFD-combat-suit-ube` | `meta.ini` |
| 23:00:20 | `输出·BodySlide Output` | `BodySlide.xml` |
| **23:01:21** | **`makaron-COSPLAY - AE_Stellablade_Tachy` (CL03_Tachy)** | **10 of its own files: 3 ShapeData + 7 `Meshes\AE_Stellablade_Tachy\*.nif`** |
| 23:12:58 | `输出·BodySlide Output` | `Log_BS.txt` |

`Log_OS.txt` / `OutfitStudio.xml` / `BodySlide.xml` / `Log_BS.txt` are the working files of **Outfit Studio and
BodySlide**, i.e. a GUI build session was in progress on this machine, in parallel with P02A.1.

**This was not this phase's doing.** A static audit of every generator in `tools/P02A/` found **0** `open()` calls
against any `mo2` / `SkyrimAE\Data` path; all write sinks target `reports/P02A/` or the delivery zip. Every teammate
reported the same read-only usage (`os.path.exists` / `os.path.isfile` / `os.scandir` / `os.walk`).

**Consequences that a reviewer must weigh:**

1. `CL03_Tachy` source files changed at 23:01:21 -- after the source map (22:49) but before the provider lookup
   (23:02) and the ShapeData texture ledger (23:04). Its rows may therefore describe a mix of two file generations.
   They were **not** re-derived, because P02A.1 forbids a P00 rescan.
2. The whole frozen evidence base is a moving target. A priority reading, a SHA256 or a ShapeData inventory taken
   at time T cannot be assumed valid at time T+n while another actor edits the instance.
3. **A P00 re-freeze immediately before P02B is mandatory**, and any build session must be stopped first. This
   supersedes the softer wording in 24.3.

> This document certifies the *design*; it does not certify that the live instance still equals the evidence it was
> derived from.



<!-- P02A.1-V2-BEGIN -->
