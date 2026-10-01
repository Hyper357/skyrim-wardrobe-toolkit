# CL09_Corrupted - P02A migration manifest

> Pack: `ZLJ_COMBAT_LATEX` (ZLJ Combat Latex Pack) - canonical body `CBBE_3BA` - target plugin `ZLJ_CombatLatex.esp`
> Phase: **P02A design ledger (STRICT READ-ONLY)** - nothing has been copied, moved, renamed or rewritten.

| field | value |
|---|---|
| Outfit ID (frozen) | `CL09_Corrupted` |
| Source mod(s) | `堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】`, `堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】` |
| Plugin (current) | `AE_CorruptedBodySuit.esp` |
| Support mods | `堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】` (LATEX_REWORK) |
| Target mesh ns | `meshes\ZLJ\CombatLatex\CL09_Corrupted\` |
| Target texture ns | `textures\ZLJ\CombatLatex\CL09_Corrupted\` |
| Target ShapeData ns | `CalienteTools\BodySlide\ShapeData\ZLJ_CombatLatex\CL09_Corrupted\` |
| Target SliderSet | `CalienteTools\BodySlide\SliderSets\ZLJ_CL09_Corrupted.osp` |

## 1. Source Mods

| MOD_ID | MO2 priority (low = wins) | role | file_count | plugin |
|---|---|---|---|---|
| 堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | 888 | BASE | 44 | AE_CorruptedBodySuit.esp |
| 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | 887 | LATEX_REWORK | 29 |  |


## 2. Winning Providers

| winning_provider | VFS paths won |
|---|---|
| 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | 29 |
| 堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | 25 |
|  | 23 |
| Nyes Latex Pack AiO 1.3 (ReducedSize) | 1 |
| makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | 1 |


## 3. Plugin Records

Counts by record type: `ARMA`=6, `ARMO`=6  
Target plugin: `ZLJ_CombatLatex.esp` - new EDID namespace: `ZLJ_CL_Corrupted_<PART>` - **no FormID generated in P02A**

| record_type | formid | edid | new_edid | notes |
|---|---|---|---|---|
| ARMA | 01000D62 | AE_CorruptedBodySuit_FeetAA | ZLJ_CL_Corrupted_LOWERLEG_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D63 | AE_CorruptedBodySuitAA | ZLJ_CL_Corrupted_BODY_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D64 | AE_CorruptedBodySuit_GloveAA | ZLJ_CL_Corrupted_HANDS_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D65 | AE_CorruptedBodySuit_HeadAA | ZLJ_CL_Corrupted_HEAD_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D6A | AE_CorruptedBodySuit_MaskAA | ZLJ_CL_Corrupted_UPPERARM_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D6B | AE_CorruptedBodySuit_NeckAA | ZLJ_CL_Corrupted_CHEST_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMO | 01000D66 | AE_CorruptedBodySuit_Feet | ZLJ_CL_Corrupted_LOWERLEG | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=BODY / P00_BODY_CANDIDATE=CBBE_3BA / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=yes:havok_tri |
| ARMO | 01000D67 | AE_CorruptedBodySuit | ZLJ_CL_Corrupted_BODY | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=BODY / P00_BODY_CANDIDATE=CBBE_3BA / P00_BODYSLIDE_MATCH=EXACT_OUTPUT_PATH / P00_PHYSICS=yes:havok_tri |
| ARMO | 01000D68 | AE_CorruptedBodySuit_Glove | ZLJ_CL_Corrupted_HANDS | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=GLOVES / P00_BODY_CANDIDATE=CBBE_3BA / P00_BODYSLIDE_MATCH=EXACT_OUTPUT_PATH / P00_PHYSICS=yes:havok_tri |
| ARMO | 01000D69 | AE_CorruptedBodySuit_Head | ZLJ_CL_Corrupted_HEAD | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=BODY / P00_BODY_CANDIDATE=CBBE_3BA / P00_BODYSLIDE_MATCH=EXACT_OUTPUT_PATH / P00_PHYSICS=yes:havok_tri |
| ARMO | 01000D6C | AE_CorruptedBodySuit_Neck | ZLJ_CL_Corrupted_CHEST | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=BODY / P00_BODY_CANDIDATE=CBBE_3BA / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=yes:havok_tri |
| ARMO | 01000D6D | AE_CorruptedBodySuit_Mask | ZLJ_CL_Corrupted_UPPERARM | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=MASK / P00_BODY_CANDIDATE=CBBE_3BA / P00_BODYSLIDE_MATCH=EXACT_OUTPUT_PATH / P00_PHYSICS=yes:havok_tri |


## 4. Game Mesh

| mesh_role | source_virtual_path | source_provider | target_virtual_path | retain |
|---|---|---|---|---|
| PHYSICS_1 | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_1.nif | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\1p\AE_CorruptedBodySuit_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_1.nif | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Feet_1.nif | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_Feet_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Hand_1.nif | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\1p\AE_CorruptedBodySuit_Hand_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Hand_1.nif | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_Hand_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Head_1.nif | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_Head_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Mask_1.nif | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_Mask_1.nif | KEEP |
| PLAIN_NIF | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Neck.nif | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_Neck.nif | KEEP |
| PHYSICS_1 | meshes\Armor\Studded\Male\1stPersongloves_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\male\1p\1stPersongloves_1.nif | REVIEW |
| STATIC_GO | meshes\Armor\Studded\Male\body_GO.nif | Static Mesh Improvement Mod - SMIM — 【网格·环境】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\world\male\body_GO.nif | KEEP |
| STATIC_GO | meshes\Armor\Studded\Male\boots_GO.nif | UNKNOWN | meshes\ZLJ\CombatLatex\CL09_Corrupted\world\male\boots_GO.nif | KEEP |
| PHYSICS_1 | meshes\Armor\Studded\Male\gloves_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\male\gloves_1.nif | REVIEW |
| STATIC_GO | meshes\Armor\Studded\Male\gloves_GO.nif | UNKNOWN | meshes\ZLJ\CombatLatex\CL09_Corrupted\world\male\gloves_GO.nif | KEEP |
| STATIC_GO | meshes\Armor\Studded\Male\helmet_GO.nif | UNKNOWN | meshes\ZLJ\CombatLatex\CL09_Corrupted\world\male\helmet_GO.nif | KEEP |
| PHYSICS_1 | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_1.nif | 堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_1.nif | EXCLUDE_SHADOWED |
| PHYSICS_1 | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_1.nif | 堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\1p\AE_CorruptedBodySuit_1.nif | EXCLUDE_SHADOWED |
| PHYSICS_1 | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Feet_1.nif | 堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_Feet_1.nif | EXCLUDE_SHADOWED |
| PHYSICS_1 | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Hand_1.nif | 堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_Hand_1.nif | EXCLUDE_SHADOWED |
| PHYSICS_1 | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Hand_1.nif | 堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\1p\AE_CorruptedBodySuit_Hand_1.nif | EXCLUDE_SHADOWED |
| PHYSICS_1 | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Head_1.nif | 堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_Head_1.nif | EXCLUDE_SHADOWED |
| PHYSICS_1 | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Mask_1.nif | 堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_Mask_1.nif | EXCLUDE_SHADOWED |
| PLAIN_NIF | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Neck.nif | 堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_Neck.nif | EXCLUDE_SHADOWED |


## 5. ShapeData / OSP / OSD

| old_ui_name | new_ui_name | old_osp | new_osp | new_shape_data | new_input_nif | new_osd | new_output_path | new_output_file | basis |
|---|---|---|---|---|---|---|---|---|---|
| AE_CorruptedBodySuit | [ZLJ Combat Latex] Corrupted - Body | CalienteTools\BodySlide\SliderSets\AE_CorruptedBodySuit.osp | CalienteTools\BodySlide\SliderSets\ZLJ_CL09_Corrupted.osp | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL09_Corrupted\AE_CorruptedBodySuit\ | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL09_Corrupted\AE_CorruptedBodySuit\AE_CorruptedBodySuit.nif | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL09_Corrupted\AE_CorruptedBodySuit\AE_CorruptedBodySuit.osd | meshes\ZLJ\CombatLatex\CL09_Corrupted\ | Body | EXACT_OUTPUT_PATH |
| AE_CorruptedBodySuit_Hand | [ZLJ Combat Latex] Corrupted - Hands | CalienteTools\BodySlide\SliderSets\AE_CorruptedBodySuit_Hand.osp | CalienteTools\BodySlide\SliderSets\ZLJ_CL09_Corrupted.osp | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL09_Corrupted\AE_CorruptedBodySuit_Hand\ | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL09_Corrupted\AE_CorruptedBodySuit_Hand\AE_CorruptedBodySuit_Hand.nif | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL09_Corrupted\AE_CorruptedBodySuit_Hand\AE_CorruptedBodySuit_Hand.osd | meshes\ZLJ\CombatLatex\CL09_Corrupted\ | Hands | EXACT_OUTPUT_PATH |
| AE_CorruptedBodySuit_Head | [ZLJ Combat Latex] Corrupted - Head | CalienteTools\BodySlide\SliderSets\AE_CorruptedBodySuit_Head.osp | CalienteTools\BodySlide\SliderSets\ZLJ_CL09_Corrupted.osp | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL09_Corrupted\AE_CorruptedBodySuit_Head\ | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL09_Corrupted\AE_CorruptedBodySuit_Head\AE_CorruptedBodySuit_Head.nif | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL09_Corrupted\AE_CorruptedBodySuit_Head\AE_CorruptedBodySuit_Head.osd | meshes\ZLJ\CombatLatex\CL09_Corrupted\ | Head | EXACT_OUTPUT_PATH |
| AE_CorruptedBodySuit_Mask | [ZLJ Combat Latex] Corrupted - Mask | CalienteTools\BodySlide\SliderSets\AE_CorruptedBodySuit_Mask.osp | CalienteTools\BodySlide\SliderSets\ZLJ_CL09_Corrupted.osp | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL09_Corrupted\AE_CorruptedBodySuit_Mask\ | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL09_Corrupted\AE_CorruptedBodySuit_Mask\AE_CorruptedBodySuit_Mask.nif | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL09_Corrupted\AE_CorruptedBodySuit_Mask\AE_CorruptedBodySuit_Mask.osd | meshes\ZLJ\CombatLatex\CL09_Corrupted\ | Mask | EXACT_OUTPUT_PATH |
| UNKNOWN | UNKNOWN | UNKNOWN | CalienteTools\BodySlide\SliderSets\ZLJ_CL09_Corrupted.osp | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |


## 6. DDS actually in use

Distinct source DDS in the closure: **26**

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
| textures\ae_corruptedbodysuit\cmilltina_botysuit_texture.dds | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\cmilltina_botysuit_texture.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\cmilltina_botysuit_normal.dds | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\cmilltina_botysuit_normal.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\s.dds | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\s.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\standardcubemap.dds | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\standardcubemap.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\d.dds | 堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\n.dds | 堕落紧身衣 — AE Corrupted Body Suit — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\s.dds | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\s.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\standardcubemap.dds | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\standardcubemap.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\eff01.dds | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\eff01.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\cmilltina_botysuit_normal.dds | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\cmilltina_botysuit_normal.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\eff01.dds | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\eff01.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\bootshoe.dds | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\bootshoe.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_latex_kitty\n.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL09_Corrupted\ae_latex_kitty\n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\standardcubemap.dds | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\standardcubemap.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\bootsole.dds | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\bootsole.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_latex_kitty\n.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL09_Corrupted\ae_latex_kitty\n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\standardcubemap.dds | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\standardcubemap.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\bootsockleather.dds | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\bootsockleather.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\dx\fetishfashion\05_begforit\socks_n.dds | [DeserterX] 恋物风尚第二辑 - 多身形本体 — DX Fetish Fashion Volume 2 SE - CBBE Physics - 3BA - BHUNP — 【服装·装备】 【体型·多体型】 【本体·ESP】 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL09_Corrupted\socks_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\standardcubemap.dds | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\standardcubemap.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_corruptedbodysuit\bootsockmetal.dds | 堕落紧身衣·乳胶重制 — AE Corrupted Body Suit - Latex Rework — 【服装·装备】【身体·物理】【体型·CBBE+3BA】【来源·本地】 | CL09_Corrupted | textures\ZLJ\CombatLatex\CL09_Corrupted\bootsockmetal.dds | COPY_INTO_OUTFIT_NAMESPACE |
| `... 70 more rows in the CSV` | | | | |


## 6b. Body morph TRI (not a physics config)

| source_tri | associated_output_nif | target_tri | rewrite_required | status |
|---|---|---|---|---|
| meshes\ae_corruptedbodysuit\ae_corruptedbodysuit.tri | meshes\ae_corruptedbodysuit\ae_corruptedbodysuit_0.nif | meshes\ZLJ\CombatLatex\CL09_Corrupted\ae_corruptedbodysuit.tri | YES | COPY_AND_REPOINT |
| meshes\ae_corruptedbodysuit\ae_corruptedbodysuit_hand.tri | meshes\ae_corruptedbodysuit\ae_corruptedbodysuit_hand_0.nif | meshes\ZLJ\CombatLatex\CL09_Corrupted\ae_corruptedbodysuit_hand.tri | YES | COPY_AND_REPOINT |
| meshes\ae_corruptedbodysuit\ae_corruptedbodysuit_head.tri | meshes\ae_corruptedbodysuit\ae_corruptedbodysuit_head_0.nif | meshes\ZLJ\CombatLatex\CL09_Corrupted\ae_corruptedbodysuit_head.tri | YES | COPY_AND_REPOINT |
| meshes\ae_corruptedbodysuit\ae_corruptedbodysuit_mask.tri | meshes\ae_corruptedbodysuit\ae_corruptedbodysuit_mask_0.nif | meshes\ZLJ\CombatLatex\CL09_Corrupted\ae_corruptedbodysuit_mask.tri | YES | COPY_AND_REPOINT |
| meshes\ae_corruptedbodysuit\ae_corruptedbodysuit_neck.tri | meshes\ae_corruptedbodysuit\ae_corruptedbodysuit_neck.nif | meshes\ZLJ\CombatLatex\CL09_Corrupted\ae_corruptedbodysuit_neck.tri | YES | COPY_AND_REPOINT |


## 6c. Model role (ARMA/ARMO slot semantics)

| model_role | canonical_runtime | body_relevance | old_path | new_path | status |
|---|---|---|---|---|---|
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_CorruptedBodySuit\AE_CorruptedBodySuit_Feet_1.nif | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_Feet_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_CorruptedBodySuit\AE_CorruptedBodySuit_1.nif | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_CorruptedBodySuit\AE_CorruptedBodySuit_Hand_1.nif | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_Hand_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_CorruptedBodySuit\AE_CorruptedBodySuit_Head_1.nif | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_Head_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_CorruptedBodySuit\AE_CorruptedBodySuit_Mask_1.nif | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_Mask_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_CorruptedBodySuit\AE_CorruptedBodySuit_Neck.nif | meshes\ZLJ\CombatLatex\CL09_Corrupted\AE_CorruptedBodySuit_Neck.nif | COPY_AND_REPOINT |


Non-canonical roles kept separate: WORLD_MALE=6, FIRSTPERSON_FEMALE=2, WEARABLE_MALE_3P=1, FIRSTPERSON_MALE=1

## 7. Physics

_`none`_


## 8. Existing PBR (provenance only)

No PBR patch mod is registered for this outfit in the P02A registry.

## 9. Cross dependencies (current -> planned)

- cross-outfit texture dependencies: **3** (open after plan: 1)
- external-mod texture dependencies: **26** (open after plan: 24)
- audit counters: cross-outfit open **0** / external-mod-missing **0** / hard-unresolved **0** / vanilla-allowed **0** / shared proposals **0**
- unresolvable DDS by class (distinct files): none - a DDS absent from the frozen P00 VFS is already broken at runtime today; it is listed, never guessed

| dependency_type | source_owner | source_virtual_path | referenced_by_nif | resolution_plan | target_virtual_path | post_plan_state |
|---|---|---|---|---|---|---|
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\1stPersongloves_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\body_GO.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\boots_GO.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\gloves_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\gloves_GO.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\helmet_GO.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL07_Lupa;CL10_HoodST | textures\ae_latex_kitty\n.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256 a49d6de5ccb12de9 is consumed by 4 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL09_Corrupted\n.dds | CLOSED_BY_DUPLICATION |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1.dds | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1_msn.dds | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1_s.dds | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1.dds | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_msn.dds | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_s.dds | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1.dds | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_msn.dds | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_s.dds | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| CROSS_OUTFIT | CL01_LatexKitty | textures\ae_latex_kitty\n.dds | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Feet_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: copy n.dds (owner CL01_LatexKitty) into textures\ZLJ\CombatLatex\CL09_Corrupted\n.dds and repoint meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Feet_1.nif / shoe_Plane.005 / Normal. Cross-outfit DDS are duplicated per outfit, never shared. | textures\ZLJ\CombatLatex\CL09_Corrupted\ae_latex_kitty\n.dds | CLOSED |
| CROSS_OUTFIT | CL01_LatexKitty | textures\ae_latex_kitty\n.dds | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Feet_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: copy n.dds (owner CL01_LatexKitty) into textures\ZLJ\CombatLatex\CL09_Corrupted\n.dds and repoint meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Feet_1.nif / sole_Plane.006 / Normal. Cross-outfit DDS are duplicated per outfit, never shared. | textures\ZLJ\CombatLatex\CL09_Corrupted\ae_latex_kitty\n.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\dx\fetishfashion\05_begforit\socks_n.dds | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Feet_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor socks_n.dds (provider [DeserterX] 恋物风尚第二辑 - 多身形本体 — DX Fetish Fashion Volume 2 SE - CBBE Physics - 3BA - BHUNP — 【服装·装备】 【体型·多体型】 【本体·ESP】, priority 1030) into textures\ZLJ\CombatLatex\CL09_Corrupted\socks_n.dds and repoint meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Feet_1.nif / SocksLeather / Normal so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL09_Corrupted\socks_n.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\dx\fetishfashion\05_begforit\socks_n.dds | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Feet_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor socks_n.dds (provider [DeserterX] 恋物风尚第二辑 - 多身形本体 — DX Fetish Fashion Volume 2 SE - CBBE Physics - 3BA - BHUNP — 【服装·装备】 【体型·多体型】 【本体·ESP】, priority 1030) into textures\ZLJ\CombatLatex\CL09_Corrupted\socks_n.dds and repoint meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Feet_1.nif / SocksMetal / Normal so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL09_Corrupted\socks_n.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\FemaleHands_1.dds | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Hand_1.nif | KEEP_EXTERNAL_REFERENCE: FemaleHands_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\FemaleHands_1_msn.dds | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Hand_1.nif | KEEP_EXTERNAL_REFERENCE: FemaleHands_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\FemaleHands_1_s.dds | meshes\AE_CorruptedBodySuit\AE_CorruptedBodySuit_Hand_1.nif | KEEP_EXTERNAL_REFERENCE: FemaleHands_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\1stPersongloves_1.nif | BLOCKED: Texture set of this mesh is not derivable from the frozen P00 evidence: the NIF is not in the P00 NIF index (existence=RESOLVED_BY_TARGETED_PROBE). The frozen evidence indexes loose mod files only, so the mesh is either BSA-resident or belongs to a provider outside the P00 scope. READ-ONLY prohibits writing, not reading: P02B is allowed to parse the binary to resolve it.. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\body_GO.nif | BLOCKED: Texture set of this mesh is not derivable from the frozen P00 evidence: the NIF is not in the P00 NIF index (existence=RESOLVED_BY_TARGETED_PROBE). The frozen evidence indexes loose mod files only, so the mesh is either BSA-resident or belongs to a provider outside the P00 scope. READ-ONLY prohibits writing, not reading: P02B is allowed to parse the binary to resolve it.. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\boots_GO.nif | BLOCKED: Texture set of this mesh is not derivable from the frozen P00 evidence: the NIF is not in the P00 NIF index (existence=NOT_PROBEABLE_SKYRIMESM_BSA_RESIDENT). The frozen evidence indexes loose mod files only, so the mesh is either BSA-resident or belongs to a provider outside the P00 scope. READ-ONLY prohibits writing, not reading: P02B is allowed to parse the binary to resolve it.. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\gloves_1.nif | BLOCKED: Texture set of this mesh is not derivable from the frozen P00 evidence: the NIF is not in the P00 NIF index (existence=RESOLVED_BY_TARGETED_PROBE). The frozen evidence indexes loose mod files only, so the mesh is either BSA-resident or belongs to a provider outside the P00 scope. READ-ONLY prohibits writing, not reading: P02B is allowed to parse the binary to resolve it.. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\gloves_GO.nif | BLOCKED: Texture set of this mesh is not derivable from the frozen P00 evidence: the NIF is not in the P00 NIF index (existence=NOT_PROBEABLE_SKYRIMESM_BSA_RESIDENT). The frozen evidence indexes loose mod files only, so the mesh is either BSA-resident or belongs to a provider outside the P00 scope. READ-ONLY prohibits writing, not reading: P02B is allowed to parse the binary to resolve it.. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\helmet_GO.nif | BLOCKED: Texture set of this mesh is not derivable from the frozen P00 evidence: the NIF is not in the P00 NIF index (existence=NOT_PROBEABLE_SKYRIMESM_BSA_RESIDENT). The frozen evidence indexes loose mod files only, so the mesh is either BSA-resident or belongs to a provider outside the P00 scope. READ-ONLY prohibits writing, not reading: P02B is allowed to parse the binary to resolve it.. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1.dds | meshes\ZLJ\CombatLatex\CL09_Corrupted\Body.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| `... 11 more rows in the CSV` | | | | | | |


## 10. Self-containment audit (simulated post-migration)

| gate | result | metric | evidence |
|---|---|---|---|
| GAME_MESH_SELF_CONTAINED | PASS | 22 | game mesh rows=22, target off-namespace=0, collisions=0 |
| TEXTURE_SELF_CONTAINED | REVIEW | 222 | slots(nif=100 shapedata=122) / off-namespace=0 / provider-found=0 / true-missing=0 / path-mismatch-unknown=0 / no-lookup=0 / vanilla=0 / global-body-skin=0 / proposals=2 / open cross-outfit=0 |
| BODYSLIDE_SELF_CONTAINED | BLOCKED | 4 | projects=5 chain-incomplete=1 OSP-off-ns=0 ShapeData-off-ns=0 Output-off-ns=0 UNKNOWN-basis=1 shapedata-tex-off-ns=0 |
| PLUGIN_PATHS_PLANNED | REVIEW | 12 | records=12 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=6 flagged-canonical=6 world-models=6 plugin-DDS-cross-outfit-open=0 / model refs: source-asset-absent=0 foreign-body-decision=2 |
| MODEL_ROLE_SCHEMA | PASS | 16 | role enum violations (legacy WORLD/WEARABLE/GROUND)=0, unknown-enum=0 / distribution: WEARABLE_FEMALE_3P=6, WORLD_MALE=6, FIRSTPERSON_FEMALE=2, WEARABLE_MALE_3P=1, FIRSTPERSON_MALE=1 |
| PHYSICS_PATHS_PLANNED | PASS | 0 | physics configs=0 types= / without-new-path=0 bone-unknown=0 |
| TRI_MORPH_SEPARATION | PASS | 5 | morph rows=5 (.tri sources=5) / TRI rows wrongly present in physics table=0 / physics types= |
| TARGET_OSP_NAMESPACE | PASS | 1 | distinct target OSP for this outfit=1 expected=1 -> ['calientetools/bodyslide/slidersets/zlj_cl09_corrupted.osp'] |
| UNRESOLVED_REFERENCE_PROVENANCE | PASS | 0 | distinct unresolved DDS=0, without a global provider-lookup verdict=0, rows whose texture set is not derivable at all (BSA-resident stock mesh, no path to look up)=6 |
| OUTFIT_SELF_CONTAINMENT | BLOCKED | 9 | C1..C9 = C1:PASS, C2:REVIEW, C3:BLOCKED, C4:REVIEW, C6:PASS, C5:PASS, G7:PASS, C8:PASS, C9:PASS |


## 11. BLOCKERS

- `C2` TEXTURE_SELF_CONTAINED = **REVIEW** - slots(nif=100 shapedata=122) | off-namespace=0 | provider-found=0 | true-missing=0 | path-mismatch-unknown=0 | no-lookup=0 | vanilla=0 | global-body-skin=0 | proposals=2 | open cross-outfit=0
- `C3` BODYSLIDE_SELF_CONTAINED = **BLOCKED** - projects=5 chain-incomplete=1 OSP-off-ns=0 ShapeData-off-ns=0 Output-off-ns=0 UNKNOWN-basis=1 shapedata-tex-off-ns=0
- `C4` PLUGIN_PATHS_PLANNED = **REVIEW** - records=12 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=6 flagged-canonical=6 world-models=6 plugin-DDS-cross-outfit-open=0 | model refs: source-asset-absent=0 foreign-body-decision=2
- `TOTAL` OUTFIT_SELF_CONTAINMENT = **BLOCKED** - C1..C9 = C1:PASS, C2:REVIEW, C3:BLOCKED, C4:REVIEW, C6:PASS, C5:PASS, G7:PASS, C8:PASS, C9:PASS

---

P02A stops here. No COPY / MOVE / DELETE / NIF / ESP / OSP / DDS write was performed and none is authorised until this design is reviewed by a human.
