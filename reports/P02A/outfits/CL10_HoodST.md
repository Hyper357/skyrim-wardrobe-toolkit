# CL10_HoodST - P02A migration manifest

> Pack: `ZLJ_COMBAT_LATEX` (ZLJ Combat Latex Pack) - canonical body `CBBE_3BA` - target plugin `ZLJ_CombatLatex.esp`
> Phase: **P02A design ledger (STRICT READ-ONLY)** - nothing has been copied, moved, renamed or rewritten.

| field | value |
|---|---|
| Outfit ID (frozen) | `CL10_HoodST` |
| Source mod(s) | `AE_HoodST — 【来源·本地】` |
| Plugin (current) | `AE_HoodST.esp` |
| Support mods | NONE |
| Target mesh ns | `meshes\ZLJ\CombatLatex\CL10_HoodST\` |
| Target texture ns | `textures\ZLJ\CombatLatex\CL10_HoodST\` |
| Target ShapeData ns | `CalienteTools\BodySlide\ShapeData\ZLJ_CombatLatex\CL10_HoodST\` |
| Target SliderSet | `CalienteTools\BodySlide\SliderSets\ZLJ_CL10_HoodST.osp` |

## 1. Source Mods

| MOD_ID | MO2 priority (low = wins) | role | file_count | plugin |
|---|---|---|---|---|
| AE_HoodST — 【来源·本地】 | 927 | BASE | 52 | AE_HoodST.esp |


## 2. Winning Providers

| winning_provider | VFS paths won |
|---|---|
| AE_HoodST — 【来源·本地】 | 51 |
|  | 16 |
| makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | 2 |
| Nyes Latex Pack AiO 1.3 (ReducedSize) | 1 |


## 3. Plugin Records

Counts by record type: `ARMA`=16, `ARMO`=16, `TXST`=10  
Target plugin: `ZLJ_CombatLatex.esp` - new EDID namespace: `ZLJ_CL_HoodST_<PART>` - **no FormID generated in P02A**

| record_type | formid | edid | new_edid | notes |
|---|---|---|---|---|
| ARMA | 01000001 | AE_HoodST_Body01_WetAA | ZLJ_CL_HoodST_BODY_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000002 | AE_HoodST_Leotard01_WetAA | ZLJ_CL_HoodST_LEOTARD01_AA | PART_TOKEN_SOURCE=P00_SLOT_BIT26_UNNAMED_EDID_TOKEN |
| ARMA | 01000009 | AE_HoodST_Body02AA | ZLJ_CL_HoodST_BODY_AA_2 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 0100000A | AE_HoodST_Body03AA | ZLJ_CL_HoodST_BODY_AA_3 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 0100000D | AE_HoodST_Leotard02AA | ZLJ_CL_HoodST_LEOTARD02_AA | PART_TOKEN_SOURCE=P00_SLOT_BIT26_UNNAMED_EDID_TOKEN |
| ARMA | 0100000E | AE_HoodST_Leotard03AA | ZLJ_CL_HoodST_LEOTARD03_AA | PART_TOKEN_SOURCE=P00_SLOT_BIT26_UNNAMED_EDID_TOKEN |
| ARMA | 01000013 | AE_HoodST_Body02_WetAA | ZLJ_CL_HoodST_BODY_AA_4 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000014 | AE_HoodST_Body03_WetAA | ZLJ_CL_HoodST_BODY_AA_5 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000019 | AE_HoodST_Leotard02_WetAA | ZLJ_CL_HoodST_LEOTARD02_AA_2 | PART_TOKEN_SOURCE=P00_SLOT_BIT26_UNNAMED_EDID_TOKEN |
| ARMA | 0100001A | AE_HoodST_Leotard03_WetAA | ZLJ_CL_HoodST_LEOTARD03_AA_2 | PART_TOKEN_SOURCE=P00_SLOT_BIT26_UNNAMED_EDID_TOKEN |
| ARMA | 0100001F | AE_HoodST_Top02AA | ZLJ_CL_HoodST_PELVIS_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000020 | AE_HoodST_Top03AA | ZLJ_CL_HoodST_PELVIS_AA_2 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D62 | AE_HoodST_Leotard_Feet01AA | ZLJ_CL_HoodST_LOWERLEG_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D63 | AE_HoodST_Body01AA | ZLJ_CL_HoodST_BODY_AA_6 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D64 | AE_HoodST_Top01AA | ZLJ_CL_HoodST_PELVIS_AA_3 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D65 | AE_HoodST_Leotard01AA | ZLJ_CL_HoodST_LEOTARD01_AA_2 | PART_TOKEN_SOURCE=P00_SLOT_BIT26_UNNAMED_EDID_TOKEN |
| ARMO | 01000003 | AE_HoodST_BodySuit01_Wet | ZLJ_CL_HoodST_BODY | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=HOOD / P00_BODY_CANDIDATE=CBBE_3BA / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=yes:havok_tri |
| ARMO | 01000004 | AE_HoodST_leotard01_Wet | ZLJ_CL_HoodST_LEOTARD01 | PART_TOKEN_SOURCE=P00_SLOT_BIT26_UNNAMED_EDID_TOKEN / P00_PART_CATEGORY=HOOD / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=yes:havok_tri |
| ARMO | 0100000B | AE_HoodST_BodySuit02 | ZLJ_CL_HoodST_BODY_2 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=HOOD / P00_BODY_CANDIDATE=CBBE_3BA / P00_BODYSLIDE_MATCH=EXACT_OUTPUT_PATH / P00_PHYSICS=yes:havok_tri |
| ARMO | 0100000C | AE_HoodST_BodySuit03 | ZLJ_CL_HoodST_BODY_3 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=HOOD / P00_BODY_CANDIDATE=CBBE_3BA / P00_BODYSLIDE_MATCH=EXACT_OUTPUT_PATH / P00_PHYSICS=yes:havok_tri |
| `... 12 more rows in the CSV` | | | | |


## 4. Game Mesh

| mesh_role | source_virtual_path | source_provider | target_virtual_path | retain |
|---|---|---|---|---|
| PHYSICS_1 | meshes\AE_HoodST\AE_HoodST_1.nif | AE_HoodST — 【来源·本地】 | meshes\ZLJ\CombatLatex\CL10_HoodST\1p\AE_HoodST_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_HoodST\AE_HoodST_1.nif | AE_HoodST — 【来源·本地】 | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_HoodST\AE_HoodST_Feet_1.nif | AE_HoodST — 【来源·本地】 | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Feet_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_HoodST\AE_HoodST_Leotard_1.nif | AE_HoodST — 【来源·本地】 | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Leotard_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_HoodST\AE_HoodST_Leotard_Wet_1.nif | AE_HoodST — 【来源·本地】 | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Leotard_Wet_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_HoodST\AE_HoodST_Top_1.nif | AE_HoodST — 【来源·本地】 | meshes\ZLJ\CombatLatex\CL10_HoodST\1p\AE_HoodST_Top_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_HoodST\AE_HoodST_Top_1.nif | AE_HoodST — 【来源·本地】 | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Top_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_HoodST\AE_HoodST_Wet_1.nif | AE_HoodST — 【来源·本地】 | meshes\ZLJ\CombatLatex\CL10_HoodST\1p\AE_HoodST_Wet_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_HoodST\AE_HoodST_Wet_1.nif | AE_HoodST — 【来源·本地】 | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Wet_1.nif | KEEP |
| PHYSICS_1 | meshes\Armor\Studded\Male\1stPersonbody_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL10_HoodST\male\1p\1stPersonbody_1.nif | REVIEW |
| PHYSICS_1 | meshes\Armor\Studded\Male\body_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL10_HoodST\male\body_1.nif | REVIEW |
| STATIC_GO | meshes\Armor\Studded\Male\body_GO.nif | Static Mesh Improvement Mod - SMIM — 【网格·环境】 | meshes\ZLJ\CombatLatex\CL10_HoodST\world\male\body_GO.nif | KEEP |
| PHYSICS_1 | meshes\Armor\Studded\Male\boots_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL10_HoodST\male\boots_1.nif | REVIEW |
| STATIC_GO | meshes\Armor\Studded\Male\boots_GO.nif | UNKNOWN | meshes\ZLJ\CombatLatex\CL10_HoodST\world\male\boots_GO.nif | KEEP |
| STATIC_GO | meshes\Armor\Studded\Male\gloves_GO.nif | UNKNOWN | meshes\ZLJ\CombatLatex\CL10_HoodST\world\male\gloves_GO.nif | KEEP |
| STATIC_GO | meshes\Armor\Studded\Male\helmet_GO.nif | UNKNOWN | meshes\ZLJ\CombatLatex\CL10_HoodST\world\male\helmet_GO.nif | KEEP |


## 5. ShapeData / OSP / OSD

| old_ui_name | new_ui_name | old_osp | new_osp | new_shape_data | new_input_nif | new_osd | new_output_path | new_output_file | basis |
|---|---|---|---|---|---|---|---|---|---|
| AE_HoodST | [ZLJ Combat Latex] HoodST - AE HoodST | CalienteTools\BodySlide\SliderSets\AE_HoodST.osp | CalienteTools\BodySlide\SliderSets\ZLJ_CL10_HoodST.osp | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL10_HoodST\AE_HoodST\ | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL10_HoodST\AE_HoodST\AE_HoodST.nif | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL10_HoodST\AE_HoodST\AE_HoodST.osd | meshes\ZLJ\CombatLatex\CL10_HoodST\ | AE_HoodST | EXACT_OUTPUT_PATH |


## 6. DDS actually in use

Distinct source DDS in the closure: **23**

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
| textures\ae_hoodst\d2.dds | AE_HoodST — 【来源·本地】 | CL10_HoodST | textures\ZLJ\CombatLatex\CL10_HoodST\d2.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_hoodst\bodysuit by n.dds | AE_HoodST — 【来源·本地】 | CL10_HoodST | textures\ZLJ\CombatLatex\CL10_HoodST\bodysuit by n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_hoodst\s.dds | AE_HoodST — 【来源·本地】 | CL10_HoodST | textures\ZLJ\CombatLatex\CL10_HoodST\s.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_hoodst\h_mat_5.dds | AE_HoodST — 【来源·本地】 | CL10_HoodST | textures\ZLJ\CombatLatex\CL10_HoodST\h_mat_5.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_hoodst\d2.dds | AE_HoodST — 【来源·本地】 | CL10_HoodST | textures\ZLJ\CombatLatex\CL10_HoodST\d2.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_hoodst\s.dds | AE_HoodST — 【来源·本地】 | CL10_HoodST | textures\ZLJ\CombatLatex\CL10_HoodST\s.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_hoodst\h_mat_5.dds | AE_HoodST — 【来源·本地】 | CL10_HoodST | textures\ZLJ\CombatLatex\CL10_HoodST\h_mat_5.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_hoodst\d2.dds | AE_HoodST — 【来源·本地】 | CL10_HoodST | textures\ZLJ\CombatLatex\CL10_HoodST\d2.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_hoodst\s.dds | AE_HoodST — 【来源·本地】 | CL10_HoodST | textures\ZLJ\CombatLatex\CL10_HoodST\s.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_hoodst\h_mat_3.dds | AE_HoodST — 【来源·本地】 | CL10_HoodST | textures\ZLJ\CombatLatex\CL10_HoodST\h_mat_3.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_latex_kitty\d1.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL10_HoodST\d1.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_latex_kitty\n.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL10_HoodST\n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_hoodst\s.dds | AE_HoodST — 【来源·本地】 | CL10_HoodST | textures\ZLJ\CombatLatex\CL10_HoodST\s.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_hoodst\h_mat_2.dds | AE_HoodST — 【来源·本地】 | CL10_HoodST | textures\ZLJ\CombatLatex\CL10_HoodST\h_mat_2.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\actors\character\female\FemaleBody_1.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\FemaleBody_1_msn.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\FemaleBody_1_s.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\ae_hoodst\suit.dds | AE_HoodST — 【来源·本地】 | CL10_HoodST | textures\ZLJ\CombatLatex\CL10_HoodST\suit.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_hoodst\bodysuitn.dds | AE_HoodST — 【来源·本地】 | CL10_HoodST | textures\ZLJ\CombatLatex\CL10_HoodST\bodysuitn.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_hoodst\s.dds | AE_HoodST — 【来源·本地】 | CL10_HoodST | textures\ZLJ\CombatLatex\CL10_HoodST\s.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_hoodst\h_mat_2.dds | AE_HoodST — 【来源·本地】 | CL10_HoodST | textures\ZLJ\CombatLatex\CL10_HoodST\h_mat_2.dds | COPY_INTO_OUTFIT_NAMESPACE |
| `... 69 more rows in the CSV` | | | | |


## 6b. Body morph TRI (not a physics config)

| source_tri | associated_output_nif | target_tri | rewrite_required | status |
|---|---|---|---|---|
| meshes\ae_hoodst\ae_hoodst.tri | meshes\ae_hoodst\ae_hoodst_0.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\ae_hoodst.tri | YES | COPY_AND_REPOINT |
| meshes\ae_hoodst\ae_hoodst_feet.tri | meshes\ae_hoodst\ae_hoodst_feet_0.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\ae_hoodst_feet.tri | YES | COPY_AND_REPOINT |
| meshes\ae_hoodst\ae_hoodst_leotard.tri | meshes\ae_hoodst\ae_hoodst_leotard_0.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\ae_hoodst_leotard.tri | YES | COPY_AND_REPOINT |
| meshes\ae_hoodst\ae_hoodst_leotard_wet.tri | meshes\ae_hoodst\ae_hoodst_leotard_wet_0.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\ae_hoodst_leotard_wet.tri | YES | COPY_AND_REPOINT |
| meshes\ae_hoodst\ae_hoodst_top.tri | meshes\ae_hoodst\ae_hoodst_top_0.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\ae_hoodst_top.tri | YES | COPY_AND_REPOINT |
| meshes\ae_hoodst\ae_hoodst_wet.tri | meshes\ae_hoodst\ae_hoodst_wet_0.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\ae_hoodst_wet.tri | YES | COPY_AND_REPOINT |


## 6c. Model role (ARMA/ARMO slot semantics)

| model_role | canonical_runtime | body_relevance | old_path | new_path | status |
|---|---|---|---|---|---|
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_HoodST\AE_HoodST_Wet_1.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Wet_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_HoodST\AE_HoodST_Leotard_Wet_1.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Leotard_Wet_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_HoodST\AE_HoodST_1.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_HoodST\AE_HoodST_1.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_HoodST\AE_HoodST_Leotard_1.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Leotard_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_HoodST\AE_HoodST_Leotard_1.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Leotard_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_HoodST\AE_HoodST_Wet_1.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Wet_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_HoodST\AE_HoodST_Wet_1.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Wet_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_HoodST\AE_HoodST_Leotard_Wet_1.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Leotard_Wet_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_HoodST\AE_HoodST_Leotard_Wet_1.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Leotard_Wet_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_HoodST\AE_HoodST_Top_1.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Top_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_HoodST\AE_HoodST_Top_1.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Top_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_HoodST\AE_HoodST_Feet_1.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Feet_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_HoodST\AE_HoodST_1.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_HoodST\AE_HoodST_Top_1.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Top_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_HoodST\AE_HoodST_Leotard_1.nif | meshes\ZLJ\CombatLatex\CL10_HoodST\AE_HoodST_Leotard_1.nif | COPY_AND_REPOINT |


Non-canonical roles kept separate: WORLD_MALE=16, FIRSTPERSON_FEMALE=9, WEARABLE_MALE_3P=7, FIRSTPERSON_MALE=6

## 7. Physics

_`none`_


## 8. Existing PBR (provenance only)

No PBR patch mod is registered for this outfit in the P02A registry.

## 9. Cross dependencies (current -> planned)

- cross-outfit texture dependencies: **4** (open after plan: 2)
- external-mod texture dependencies: **30** (open after plan: 30)
- audit counters: cross-outfit open **0** / external-mod-missing **0** / hard-unresolved **0** / vanilla-allowed **0** / shared proposals **0**
- unresolvable DDS by class (distinct files): none - a DDS absent from the frozen P00 VFS is already broken at runtime today; it is listed, never guessed

| dependency_type | source_owner | source_virtual_path | referenced_by_nif | resolution_plan | target_virtual_path | post_plan_state |
|---|---|---|---|---|---|---|
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\1stPersonbody_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\body_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\body_GO.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\boots_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\boots_GO.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\gloves_GO.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\helmet_GO.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL07_Lupa | textures\ae_latex_kitty\d1.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256 775d2ba7ba8716eb is consumed by 3 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL10_HoodST\d1.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL07_Lupa;CL09_Corrupted | textures\ae_latex_kitty\n.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256 a49d6de5ccb12de9 is consumed by 4 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL10_HoodST\n.dds | CLOSED_BY_DUPLICATION |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1.dds | meshes\AE_HoodST\AE_HoodST_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1_msn.dds | meshes\AE_HoodST\AE_HoodST_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1_s.dds | meshes\AE_HoodST\AE_HoodST_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1.dds | meshes\AE_HoodST\AE_HoodST_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_msn.dds | meshes\AE_HoodST\AE_HoodST_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_s.dds | meshes\AE_HoodST\AE_HoodST_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1.dds | meshes\AE_HoodST\AE_HoodST_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_msn.dds | meshes\AE_HoodST\AE_HoodST_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_s.dds | meshes\AE_HoodST\AE_HoodST_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| CROSS_OUTFIT | CL01_LatexKitty | textures\ae_latex_kitty\d1.dds | meshes\AE_HoodST\AE_HoodST_Feet_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: copy d1.dds (owner CL01_LatexKitty) into textures\ZLJ\CombatLatex\CL10_HoodST\d1.dds and repoint meshes\AE_HoodST\AE_HoodST_Feet_1.nif / Boots / Diffuse. Cross-outfit DDS are duplicated per outfit, never shared. | textures\ZLJ\CombatLatex\CL10_HoodST\d1.dds | CLOSED |
| CROSS_OUTFIT | CL01_LatexKitty | textures\ae_latex_kitty\n.dds | meshes\AE_HoodST\AE_HoodST_Feet_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: copy n.dds (owner CL01_LatexKitty) into textures\ZLJ\CombatLatex\CL10_HoodST\n.dds and repoint meshes\AE_HoodST\AE_HoodST_Feet_1.nif / Boots / Normal. Cross-outfit DDS are duplicated per outfit, never shared. | textures\ZLJ\CombatLatex\CL10_HoodST\n.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\FemaleBody_1.dds | meshes\AE_HoodST\AE_HoodST_Feet_1.nif | KEEP_EXTERNAL_REFERENCE: FemaleBody_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\FemaleBody_1_msn.dds | meshes\AE_HoodST\AE_HoodST_Feet_1.nif | KEEP_EXTERNAL_REFERENCE: FemaleBody_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\FemaleBody_1_s.dds | meshes\AE_HoodST\AE_HoodST_Feet_1.nif | KEEP_EXTERNAL_REFERENCE: FemaleBody_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1.dds | meshes\AE_HoodST\AE_HoodST_Wet_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1_msn.dds | meshes\AE_HoodST\AE_HoodST_Wet_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1_s.dds | meshes\AE_HoodST\AE_HoodST_Wet_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1.dds | meshes\AE_HoodST\AE_HoodST_Wet_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_msn.dds | meshes\AE_HoodST\AE_HoodST_Wet_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_s.dds | meshes\AE_HoodST\AE_HoodST_Wet_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1.dds | meshes\AE_HoodST\AE_HoodST_Wet_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| `... 18 more rows in the CSV` | | | | | | |


## 10. Self-containment audit (simulated post-migration)

| gate | result | metric | evidence |
|---|---|---|---|
| GAME_MESH_SELF_CONTAINED | PASS | 16 | game mesh rows=16, target off-namespace=0, collisions=0 |
| TEXTURE_SELF_CONTAINED | REVIEW | 179 | slots(nif=99 shapedata=80) / off-namespace=0 / provider-found=0 / true-missing=0 / path-mismatch-unknown=0 / no-lookup=0 / vanilla=0 / global-body-skin=0 / proposals=2 / open cross-outfit=0 |
| BODYSLIDE_SELF_CONTAINED | PASS | 1 | projects=1 chain-incomplete=0 OSP-off-ns=0 ShapeData-off-ns=0 Output-off-ns=0 UNKNOWN-basis=0 shapedata-tex-off-ns=0 |
| PLUGIN_PATHS_PLANNED | REVIEW | 42 | records=42 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=16 flagged-canonical=16 world-models=16 plugin-DDS-cross-outfit-open=0 / model refs: source-asset-absent=0 foreign-body-decision=13 |
| MODEL_ROLE_SCHEMA | PASS | 54 | role enum violations (legacy WORLD/WEARABLE/GROUND)=0, unknown-enum=0 / distribution: WEARABLE_FEMALE_3P=16, WORLD_MALE=16, FIRSTPERSON_FEMALE=9, WEARABLE_MALE_3P=7, FIRSTPERSON_MALE=6 |
| PHYSICS_PATHS_PLANNED | PASS | 0 | physics configs=0 types= / without-new-path=0 bone-unknown=0 |
| TRI_MORPH_SEPARATION | PASS | 6 | morph rows=6 (.tri sources=6) / TRI rows wrongly present in physics table=0 / physics types= |
| TARGET_OSP_NAMESPACE | PASS | 1 | distinct target OSP for this outfit=1 expected=1 -> ['calientetools/bodyslide/slidersets/zlj_cl10_hoodst.osp'] |
| UNRESOLVED_REFERENCE_PROVENANCE | PASS | 0 | distinct unresolved DDS=0, without a global provider-lookup verdict=0, rows whose texture set is not derivable at all (BSA-resident stock mesh, no path to look up)=7 |
| OUTFIT_SELF_CONTAINMENT | REVIEW | 9 | C1..C9 = C1:PASS, C2:REVIEW, C3:PASS, C4:REVIEW, C6:PASS, C5:PASS, G7:PASS, C8:PASS, C9:PASS |


## 11. BLOCKERS

- `C2` TEXTURE_SELF_CONTAINED = **REVIEW** - slots(nif=99 shapedata=80) | off-namespace=0 | provider-found=0 | true-missing=0 | path-mismatch-unknown=0 | no-lookup=0 | vanilla=0 | global-body-skin=0 | proposals=2 | open cross-outfit=0
- `C4` PLUGIN_PATHS_PLANNED = **REVIEW** - records=42 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=16 flagged-canonical=16 world-models=16 plugin-DDS-cross-outfit-open=0 | model refs: source-asset-absent=0 foreign-body-decision=13
- `TOTAL` OUTFIT_SELF_CONTAINMENT = **REVIEW** - C1..C9 = C1:PASS, C2:REVIEW, C3:PASS, C4:REVIEW, C6:PASS, C5:PASS, G7:PASS, C8:PASS, C9:PASS

---

P02A stops here. No COPY / MOVE / DELETE / NIF / ESP / OSP / DDS write was performed and none is authorised until this design is reviewed by a human.
