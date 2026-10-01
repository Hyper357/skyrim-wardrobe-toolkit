# CL03_Tachy - P02A migration manifest

> Pack: `ZLJ_COMBAT_LATEX` (ZLJ Combat Latex Pack) - canonical body `CBBE_3BA` - target plugin `ZLJ_CombatLatex.esp`
> Phase: **P02A design ledger (STRICT READ-ONLY)** - nothing has been copied, moved, renamed or rewritten.

| field | value |
|---|---|
| Outfit ID (frozen) | `CL03_Tachy` |
| Source mod(s) | `makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】` |
| Plugin (current) | `AE Stellablade Tachy.esp` |
| Support mods | NONE |
| Target mesh ns | `meshes\ZLJ\CombatLatex\CL03_Tachy\` |
| Target texture ns | `textures\ZLJ\CombatLatex\CL03_Tachy\` |
| Target ShapeData ns | `CalienteTools\BodySlide\ShapeData\ZLJ_CombatLatex\CL03_Tachy\` |
| Target SliderSet | `CalienteTools\BodySlide\SliderSets\ZLJ_CL03_Tachy.osp` |

## 1. Source Mods

| MOD_ID | MO2 priority (low = wins) | role | file_count | plugin |
|---|---|---|---|---|
| makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | 922 | BASE | 39 | AE Stellablade Tachy.esp |


## 2. Winning Providers

| winning_provider | VFS paths won |
|---|---|
| makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | 38 |
|  | 16 |
| Nyes Latex Pack AiO 1.3 (ReducedSize) | 1 |


## 3. Plugin Records

Counts by record type: `ARMA`=3, `ARMO`=3  
Target plugin: `ZLJ_CombatLatex.esp` - new EDID namespace: `ZLJ_CL_Tachy_<PART>` - **no FormID generated in P02A**

| record_type | formid | edid | new_edid | notes |
|---|---|---|---|---|
| ARMA | 02000D62 | AE_Stellablade_Tachy_BodyAA | ZLJ_CL_Tachy_BODY_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 02000D63 | AE_Stellablade_Tachy_GloveAA | ZLJ_CL_Tachy_HANDS_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 02000D68 | AE_Stellablade_Tachy_MaskAA | ZLJ_CL_Tachy_RIGHTWEAPON_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMO | 02000D65 | AE_Stellablade_Tachy_Body | ZLJ_CL_Tachy_BODY | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=BODY / P00_BODY_CANDIDATE=CBBE_3BA / P00_BODYSLIDE_MATCH=EXACT_OUTPUT_PATH / P00_PHYSICS=no |
| ARMO | 02000D66 | AE_Stellablade_Tachy_Hand | ZLJ_CL_Tachy_HANDS | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 02000D67 | AE_Stellablade_Tachy_Mask | ZLJ_CL_Tachy_RIGHTWEAPON | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=MASK / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |


## 4. Game Mesh

| mesh_role | source_virtual_path | source_provider | target_virtual_path | retain |
|---|---|---|---|---|
| PHYSICS_1 | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL03_Tachy\AE_Stellablade_Tachy_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL03_Tachy\world\male\AE_Stellablade_Tachy_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1st_1.nif | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL03_Tachy\1p\AE_Stellablade_Tachy_1st_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_Hand_1.nif | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL03_Tachy\1p\AE_Stellablade_Tachy_Hand_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_Hand_1.nif | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL03_Tachy\AE_Stellablade_Tachy_Hand_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_Hand_1.nif | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL03_Tachy\world\male\AE_Stellablade_Tachy_Hand_1.nif | KEEP |
| PLAIN_NIF | meshes\AE_Stellablade_Tachy\Mask.nif | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL03_Tachy\1p\Mask.nif | KEEP |
| PLAIN_NIF | meshes\AE_Stellablade_Tachy\Mask.nif | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL03_Tachy\male\1p\Mask.nif | KEEP |
| PLAIN_NIF | meshes\AE_Stellablade_Tachy\Mask.nif | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL03_Tachy\Mask.nif | KEEP |
| PLAIN_NIF | meshes\AE_Stellablade_Tachy\Mask.nif | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL03_Tachy\male\Mask.nif | KEEP |
| PLAIN_NIF | meshes\AE_Stellablade_Tachy\Mask.nif | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL03_Tachy\world\female\Mask.nif | KEEP |
| PLAIN_NIF | meshes\AE_Stellablade_Tachy\Mask.nif | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL03_Tachy\world\male\Mask.nif | KEEP |
| PHYSICS_1 | meshes\Armor\Studded\Male\1stPersonbody_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL03_Tachy\male\1p\1stPersonbody_1.nif | REVIEW |
| PHYSICS_1 | meshes\Armor\Studded\Male\1stPersongloves_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL03_Tachy\male\1p\1stPersongloves_1.nif | REVIEW |
| PHYSICS_1 | meshes\Armor\Studded\Male\body_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL03_Tachy\male\body_1.nif | REVIEW |
| PHYSICS_1 | meshes\Armor\Studded\Male\gloves_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL03_Tachy\male\gloves_1.nif | REVIEW |


## 5. ShapeData / OSP / OSD

| old_ui_name | new_ui_name | old_osp | new_osp | new_shape_data | new_input_nif | new_osd | new_output_path | new_output_file | basis |
|---|---|---|---|---|---|---|---|---|---|
| AE_Stellablade_Tachy | [ZLJ Combat Latex] Tachy - AE Stellablade Tachy | CalienteTools\BodySlide\SliderSets\AE_Stellablade_Tachy.osp | CalienteTools\BodySlide\SliderSets\ZLJ_CL03_Tachy.osp | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL03_Tachy\AE_Stellablade_Tachy\ | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL03_Tachy\AE_Stellablade_Tachy\AE_Stellablade_Tachy.nif | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL03_Tachy\AE_Stellablade_Tachy\AE_Stellablade_Tachy.osd | meshes\ZLJ\CombatLatex\CL03_Tachy\ | AE_Stellablade_Tachy | EXACT_OUTPUT_PATH |


## 6. DDS actually in use

Distinct source DDS in the closure: **15**

| source_virtual_path | winning_provider | owning_outfit_of_source | target_virtual_path | action |
|---|---|---|---|---|
| textures\actors\character\female\femalebody_1.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\femalebody_1_msn.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\femalebody_1_s.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\femalebody_etc_v2_1.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\femalebody_etc_v2_1_msn.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\femalebody_etc_v2_1_s.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\femalebody_etc_v2_1.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\femalebody_etc_v2_1_msn.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\femalebody_etc_v2_1_s.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\ghost\ghostcolour4.dds | UNKNOWN | VANILLA |  | KEEP_EXTERNAL_REFERENCE |
| textures\devious\devices\catsuitLatex_n.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatex_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_stellablade_tachy\ch_eve_10_body_orm.dds | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | CL03_Tachy | textures\ZLJ\CombatLatex\CL03_Tachy\ch_eve_10_body_orm.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_stellablade_tachy\cubemap_e.dds | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | CL03_Tachy | textures\ZLJ\CombatLatex\CL03_Tachy\cubemap_e.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ghost\ghostcolour4.dds | UNKNOWN | VANILLA |  | KEEP_EXTERNAL_REFERENCE |
| textures\devious\devices\catsuitLatex_n.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatex_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_stellablade_tachy\ch_eve_10_body_orm.dds | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | CL03_Tachy | textures\ZLJ\CombatLatex\CL03_Tachy\ch_eve_10_body_orm.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_stellablade_tachy\standardcubemap00.dds | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | CL03_Tachy | textures\ZLJ\CombatLatex\CL03_Tachy\standardcubemap00.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatexWhite_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatexWhite_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_stellablade_tachy\ch_eve_10_body_n.dds | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | CL03_Tachy | textures\ZLJ\CombatLatex\CL03_Tachy\ch_eve_10_body_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_stellablade_tachy\cubemap_e.dds | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | CL03_Tachy | textures\ZLJ\CombatLatex\CL03_Tachy\cubemap_e.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatexWhite_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatexWhite_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_stellablade_tachy\ch_eve_10_body_n.dds | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | CL03_Tachy | textures\ZLJ\CombatLatex\CL03_Tachy\ch_eve_10_body_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_stellablade_tachy\ch_eve_10_body_orm.dds | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | CL03_Tachy | textures\ZLJ\CombatLatex\CL03_Tachy\ch_eve_10_body_orm.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_stellablade_tachy\cubemap_e.dds | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | CL03_Tachy | textures\ZLJ\CombatLatex\CL03_Tachy\cubemap_e.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ghost\ghostcolour4.dds | UNKNOWN | VANILLA |  | KEEP_EXTERNAL_REFERENCE |
| textures\devious\devices\catsuitLatex_n.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatex_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_stellablade_tachy\ch_eve_10_body_orm.dds | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | CL03_Tachy | textures\ZLJ\CombatLatex\CL03_Tachy\ch_eve_10_body_orm.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_stellablade_tachy\cubemap_e.dds | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | CL03_Tachy | textures\ZLJ\CombatLatex\CL03_Tachy\cubemap_e.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatexWhite_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatexWhite_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_stellablade_tachy\ch_eve_10_body_n.dds | makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】 | CL03_Tachy | textures\ZLJ\CombatLatex\CL03_Tachy\ch_eve_10_body_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| `... 38 more rows in the CSV` | | | | |


## 6b. Body morph TRI (not a physics config)

_`none`_


## 6c. Model role (ARMA/ARMO slot semantics)

| model_role | canonical_runtime | body_relevance | old_path | new_path | status |
|---|---|---|---|---|---|
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | meshes\ZLJ\CombatLatex\CL03_Tachy\AE_Stellablade_Tachy_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_Stellablade_Tachy\AE_Stellablade_Tachy_Hand_1.nif | meshes\ZLJ\CombatLatex\CL03_Tachy\AE_Stellablade_Tachy_Hand_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_Stellablade_Tachy\Mask.nif | meshes\ZLJ\CombatLatex\CL03_Tachy\Mask.nif | COPY_AND_REPOINT |


Non-canonical roles kept separate: WEARABLE_MALE_3P=3, FIRSTPERSON_MALE=3, FIRSTPERSON_FEMALE=3, WORLD_MALE=3, WORLD_FEMALE=1

## 7. Physics

_`none`_


## 8. Existing PBR (provenance only)

No PBR patch mod is registered for this outfit in the P02A registry.

## 9. Cross dependencies (current -> planned)

- cross-outfit texture dependencies: **2** (open after plan: 2)
- external-mod texture dependencies: **37** (open after plan: 25)
- audit counters: cross-outfit open **0** / external-mod-missing **0** / hard-unresolved **0** / vanilla-allowed **0** / shared proposals **0**
- unresolvable DDS by class (distinct files): none - a DDS absent from the frozen P00 VFS is already broken at runtime today; it is listed, never guessed

| dependency_type | source_owner | source_virtual_path | referenced_by_nif | resolution_plan | target_virtual_path | post_plan_state |
|---|---|---|---|---|---|---|
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\1stPersonbody_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\1stPersongloves_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\body_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\gloves_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| CROSS_PACK_CANDIDATE | CL02_OnceMedic;CL04_Haley;CL05_Valby;CL08_SpearHead;CL11_SkimpyAssassin | textures\devious\devices\catsuitLatex_n.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_Glove_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 6 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatex_n.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL02_OnceMedic | textures\devious\devices\catsuitLatexWhite_d.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 2 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatexWhite_d.dds | CLOSED_BY_DUPLICATION |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1_msn.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1_s.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_msn.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_s.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_msn.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_s.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | VANILLA | textures\ghost\ghostcolour4.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | KEEP_EXTERNAL_REFERENCE: ghostcolour4.dds belongs to the VANILLA_ENGINE_RESOURCE and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatex_n.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatex_n.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatex_n.dds and repoint meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif / CH_NPC_TachyNPC_Body.002_CH_NPC_TachyNPC_Body.001 / Normal so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatex_n.dds | CLOSED |
| EXTERNAL_MOD | VANILLA | textures\ghost\ghostcolour4.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | KEEP_EXTERNAL_REFERENCE: ghostcolour4.dds belongs to the VANILLA_ENGINE_RESOURCE and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatex_n.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatex_n.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatex_n.dds and repoint meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif / CH_NPC_TachyNPC_Body.061_CH_NPC_TachyNPC_Body.060 / Normal so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatex_n.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatexWhite_d.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatexWhite_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatexWhite_d.dds and repoint meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif / CH_NPC_TachyNPC_Body.072_CH_NPC_TachyNPC_Body.071 / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatexWhite_d.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatexWhite_d.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatexWhite_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatexWhite_d.dds and repoint meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1.nif / CH_NPC_TachyNPC_Body.036_CH_NPC_TachyNPC_Body.035 / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatexWhite_d.dds | CLOSED |
| EXTERNAL_MOD | VANILLA | textures\ghost\ghostcolour4.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1st_1.nif | KEEP_EXTERNAL_REFERENCE: ghostcolour4.dds belongs to the VANILLA_ENGINE_RESOURCE and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatex_n.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1st_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatex_n.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatex_n.dds and repoint meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1st_1.nif / CH_NPC_TachyNPC_Body.061_CH_NPC_TachyNPC_Body.060 / Normal so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatex_n.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatexWhite_d.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1st_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatexWhite_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatexWhite_d.dds and repoint meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_1st_1.nif / CH_NPC_TachyNPC_Body.036_CH_NPC_TachyNPC_Body.035 / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatexWhite_d.dds | CLOSED |
| EXTERNAL_MOD | VANILLA | textures\ghost\ghostcolour4.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_Hand_1.nif | KEEP_EXTERNAL_REFERENCE: ghostcolour4.dds belongs to the VANILLA_ENGINE_RESOURCE and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatex_n.dds | meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_Hand_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatex_n.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatex_n.dds and repoint meshes\AE_Stellablade_Tachy\AE_Stellablade_Tachy_Hand_1.nif / Gloves / Normal so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatex_n.dds | CLOSED |
| EXTERNAL_MOD | VANILLA | textures\ghost\ghostcolour4.dds | meshes\AE_Stellablade_Tachy\Mask.nif | KEEP_EXTERNAL_REFERENCE: ghostcolour4.dds belongs to the VANILLA_ENGINE_RESOURCE and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatex_n.dds | meshes\AE_Stellablade_Tachy\Mask.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatex_n.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatex_n.dds and repoint meshes\AE_Stellablade_Tachy\Mask.nif / MaskSilenceDust_2 / Normal so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL03_Tachy\catsuitLatex_n.dds | CLOSED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\1stPersonbody_1.nif | BLOCKED: Texture set of this mesh is not derivable from the frozen P00 evidence: the NIF is not in the P00 NIF index (existence=RESOLVED_BY_TARGETED_PROBE). The frozen evidence indexes loose mod files only, so the mesh is either BSA-resident or belongs to a provider outside the P00 scope. READ-ONLY prohibits writing, not reading: P02B is allowed to parse the binary to resolve it.. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\1stPersongloves_1.nif | BLOCKED: Texture set of this mesh is not derivable from the frozen P00 evidence: the NIF is not in the P00 NIF index (existence=RESOLVED_BY_TARGETED_PROBE). The frozen evidence indexes loose mod files only, so the mesh is either BSA-resident or belongs to a provider outside the P00 scope. READ-ONLY prohibits writing, not reading: P02B is allowed to parse the binary to resolve it.. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| `... 17 more rows in the CSV` | | | | | | |


## 10. Self-containment audit (simulated post-migration)

| gate | result | metric | evidence |
|---|---|---|---|
| GAME_MESH_SELF_CONTAINED | PASS | 16 | game mesh rows=16, target off-namespace=0, collisions=0 |
| TEXTURE_SELF_CONTAINED | REVIEW | 107 | slots(nif=68 shapedata=39) / off-namespace=0 / provider-found=0 / true-missing=0 / path-mismatch-unknown=0 / no-lookup=0 / vanilla=0 / global-body-skin=0 / proposals=12 / open cross-outfit=0 |
| BODYSLIDE_SELF_CONTAINED | PASS | 1 | projects=1 chain-incomplete=0 OSP-off-ns=0 ShapeData-off-ns=0 Output-off-ns=0 UNKNOWN-basis=0 shapedata-tex-off-ns=0 |
| PLUGIN_PATHS_PLANNED | REVIEW | 6 | records=6 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=3 flagged-canonical=3 world-models=4 plugin-DDS-cross-outfit-open=0 / model refs: source-asset-absent=0 foreign-body-decision=4 |
| MODEL_ROLE_SCHEMA | PASS | 16 | role enum violations (legacy WORLD/WEARABLE/GROUND)=0, unknown-enum=0 / distribution: WEARABLE_MALE_3P=3, WEARABLE_FEMALE_3P=3, FIRSTPERSON_MALE=3, FIRSTPERSON_FEMALE=3, WORLD_MALE=3, WORLD_FEMALE=1 |
| PHYSICS_PATHS_PLANNED | PASS | 0 | physics configs=0 types= / without-new-path=0 bone-unknown=0 |
| TRI_MORPH_SEPARATION | PASS | 0 | morph rows=0 (.tri sources=0) / TRI rows wrongly present in physics table=0 / physics types= |
| TARGET_OSP_NAMESPACE | PASS | 1 | distinct target OSP for this outfit=1 expected=1 -> ['calientetools/bodyslide/slidersets/zlj_cl03_tachy.osp'] |
| UNRESOLVED_REFERENCE_PROVENANCE | PASS | 0 | distinct unresolved DDS=0, without a global provider-lookup verdict=0, rows whose texture set is not derivable at all (BSA-resident stock mesh, no path to look up)=4 |
| OUTFIT_SELF_CONTAINMENT | REVIEW | 9 | C1..C9 = C1:PASS, C2:REVIEW, C3:PASS, C4:REVIEW, C6:PASS, C5:PASS, G7:PASS, C8:PASS, C9:PASS |


## 11. BLOCKERS

- `C2` TEXTURE_SELF_CONTAINED = **REVIEW** - slots(nif=68 shapedata=39) | off-namespace=0 | provider-found=0 | true-missing=0 | path-mismatch-unknown=0 | no-lookup=0 | vanilla=0 | global-body-skin=0 | proposals=12 | open cross-outfit=0
- `C4` PLUGIN_PATHS_PLANNED = **REVIEW** - records=6 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=3 flagged-canonical=3 world-models=4 plugin-DDS-cross-outfit-open=0 | model refs: source-asset-absent=0 foreign-body-decision=4
- `TOTAL` OUTFIT_SELF_CONTAINMENT = **REVIEW** - C1..C9 = C1:PASS, C2:REVIEW, C3:PASS, C4:REVIEW, C6:PASS, C5:PASS, G7:PASS, C8:PASS, C9:PASS

---

P02A stops here. No COPY / MOVE / DELETE / NIF / ESP / OSP / DDS write was performed and none is authorised until this design is reviewed by a human.
