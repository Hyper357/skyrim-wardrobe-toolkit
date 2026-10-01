# CL02_OnceMedic - P02A migration manifest

> Pack: `ZLJ_COMBAT_LATEX` (ZLJ Combat Latex Pack) - canonical body `CBBE_3BA` - target plugin `ZLJ_CombatLatex.esp`
> Phase: **P02A design ledger (STRICT READ-ONLY)** - nothing has been copied, moved, renamed or rewritten.

| field | value |
|---|---|
| Outfit ID (frozen) | `CL02_OnceMedic` |
| Source mod(s) | `makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】` |
| Plugin (current) | `AE_Once_Medic.esp` |
| Support mods | NONE |
| Target mesh ns | `meshes\ZLJ\CombatLatex\CL02_OnceMedic\` |
| Target texture ns | `textures\ZLJ\CombatLatex\CL02_OnceMedic\` |
| Target ShapeData ns | `CalienteTools\BodySlide\ShapeData\ZLJ_CombatLatex\CL02_OnceMedic\` |
| Target SliderSet | `CalienteTools\BodySlide\SliderSets\ZLJ_CL02_OnceMedic.osp` |

## 1. Source Mods

| MOD_ID | MO2 priority (low = wins) | role | file_count | plugin |
|---|---|---|---|---|
| makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | 923 | BASE | 80 | AE_Once_Medic.esp |


## 2. Winning Providers

| winning_provider | VFS paths won |
|---|---|
| makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | 79 |
|  | 29 |
| Nyes Latex Pack AiO 1.3 (ReducedSize) | 1 |


## 3. Plugin Records

Counts by record type: `ARMA`=8, `ARMO`=8  
Target plugin: `ZLJ_CombatLatex.esp` - new EDID namespace: `ZLJ_CL_OnceMedic_<PART>` - **no FormID generated in P02A**

| record_type | formid | edid | new_edid | notes |
|---|---|---|---|---|
| ARMA | 01000007 | AE_Once_Combat_Medic_FeetAA | ZLJ_CL_OnceMedic_LOWERLEG_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000008 | AE_Once_Combat_Medic_BodyAA | ZLJ_CL_OnceMedic_BODY_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000009 | AE_Once_Combat_Medic_GloveAA | ZLJ_CL_OnceMedic_HANDS_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 0100000A | AE_Once_Combat_Medic_HairAA | ZLJ_CL_OnceMedic_HAIR_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 0100000F | AE_Once_Combat_Medic_MaskAA | ZLJ_CL_OnceMedic_LEFTWEAPON_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000010 | AE_Once_Combat_Medic_StockingsAA | ZLJ_CL_OnceMedic_SHIELD_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000013 | AE_Once_Combat_Medic_VailAA | ZLJ_CL_OnceMedic_FRONT_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000015 | AE_Once_Combat_Medic_Back_PackAA | ZLJ_CL_OnceMedic_PELVIS_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMO | 0100000B | AE_Once_Combat_Medic_Feet | ZLJ_CL_OnceMedic_LOWERLEG | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 0100000C | OnceCombatMedic_Body | ZLJ_CL_OnceMedic_BODY | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=BODY / P00_BODY_CANDIDATE=CBBE_3BA / P00_BODYSLIDE_MATCH=EXACT_OUTPUT_PATH / P00_PHYSICS=no |
| ARMO | 0100000D | OnceCombatMedic_Glove | ZLJ_CL_OnceMedic_HANDS | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=GLOVES / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 0100000E | OnceCombatMedic_Hair | ZLJ_CL_OnceMedic_HAIR | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 01000011 | AE_Once_Combat_Medic_Stockings | ZLJ_CL_OnceMedic_SHIELD | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=STOCKINGS / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 01000012 | OnceCombatMedic_Mask | ZLJ_CL_OnceMedic_LEFTWEAPON | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=MASK / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 01000014 | OnceCombatMedic_Vail | ZLJ_CL_OnceMedic_FRONT | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=EXACT_OUTPUT_PATH / P00_PHYSICS=no |
| ARMO | 01000016 | OnceCombatMedic_Back_Pack | ZLJ_CL_OnceMedic_PELVIS | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=EXACT_OUTPUT_PATH / P00_PHYSICS=no |


## 4. Game Mesh

| mesh_role | source_virtual_path | source_provider | target_virtual_path | retain |
|---|---|---|---|---|
| PHYSICS_1 | meshes\AE Once Human\AM\AE_Once_Combat_Medi_Vail_1.nif | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\AE_Once_Combat_Medi_Vail_1.nif | KEEP |
| PHYSICS_1 | meshes\AE Once Human\AM\AE_Once_Combat_Medi_Vail_1.nif | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\male\AE_Once_Combat_Medi_Vail_1.nif | KEEP |
| PHYSICS_1 | meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\1p\AE_Once_Combat_Medic_1.nif | KEEP |
| PHYSICS_1 | meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\AE_Once_Combat_Medic_1.nif | KEEP |
| PHYSICS_1 | meshes\AE Once Human\AM\AE_Once_Combat_Medic_Back_Pack_1.nif | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\AE_Once_Combat_Medic_Back_Pack_1.nif | KEEP |
| PHYSICS_1 | meshes\AE Once Human\AM\AE_Once_Combat_Medic_Feet_1.nif | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\AE_Once_Combat_Medic_Feet_1.nif | KEEP |
| PHYSICS_1 | meshes\AE Once Human\AM\AE_Once_Combat_Medic_Glove_1.nif | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\1p\AE_Once_Combat_Medic_Glove_1.nif | KEEP |
| PHYSICS_1 | meshes\AE Once Human\AM\AE_Once_Combat_Medic_Glove_1.nif | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\AE_Once_Combat_Medic_Glove_1.nif | KEEP |
| PHYSICS_1 | meshes\AE Once Human\AM\AE_Once_Combat_Medic_Stockings_1.nif | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\AE_Once_Combat_Medic_Stockings_1.nif | KEEP |
| PLAIN_NIF | meshes\AE Once Human\AM\Combat_Medic_Hair.nif | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\Combat_Medic_Hair.nif | KEEP |
| PLAIN_NIF | meshes\AE Once Human\AM\Combat_Medic_Hair.nif | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\male\Combat_Medic_Hair.nif | KEEP |
| PLAIN_NIF | meshes\AE Once Human\AM\Combat_Medic_Mask.nif | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\Combat_Medic_Mask.nif | KEEP |
| PLAIN_NIF | meshes\AE Once Human\AM\Combat_Medic_Mask.nif | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\male\Combat_Medic_Mask.nif | KEEP |
| PHYSICS_1 | meshes\Armor\Studded\Male\1stPersonbody_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\male\1p\1stPersonbody_1.nif | REVIEW |
| PHYSICS_1 | meshes\Armor\Studded\Male\1stPersongloves_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\male\1p\1stPersongloves_1.nif | REVIEW |
| PHYSICS_1 | meshes\Armor\Studded\Male\body_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\male\body_1.nif | REVIEW |
| STATIC_GO | meshes\Armor\Studded\Male\body_GO.nif | Static Mesh Improvement Mod - SMIM — 【网格·环境】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\world\male\body_GO.nif | KEEP |
| PHYSICS_1 | meshes\Armor\Studded\Male\boots_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\male\boots_1.nif | REVIEW |
| STATIC_GO | meshes\Armor\Studded\Male\boots_GO.nif | UNKNOWN | meshes\ZLJ\CombatLatex\CL02_OnceMedic\world\male\boots_GO.nif | KEEP |
| PHYSICS_1 | meshes\Armor\Studded\Male\gloves_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL02_OnceMedic\male\gloves_1.nif | REVIEW |
| STATIC_GO | meshes\Armor\Studded\Male\gloves_GO.nif | UNKNOWN | meshes\ZLJ\CombatLatex\CL02_OnceMedic\world\male\gloves_GO.nif | KEEP |
| STATIC_GO | meshes\Armor\Studded\Male\helmet_GO.nif | UNKNOWN | meshes\ZLJ\CombatLatex\CL02_OnceMedic\world\male\helmet_GO.nif | KEEP |


## 5. ShapeData / OSP / OSD

| old_ui_name | new_ui_name | old_osp | new_osp | new_shape_data | new_input_nif | new_osd | new_output_path | new_output_file | basis |
|---|---|---|---|---|---|---|---|---|---|
| AE_Once_Combat_Medi_Vail | [ZLJ Combat Latex] OnceMedic - AE Once Combat Medi Vail | CalienteTools\BodySlide\SliderSets\AE_Once_Combat_Medi_Vail.osp | CalienteTools\BodySlide\SliderSets\ZLJ_CL02_OnceMedic.osp | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL02_OnceMedic\AE_Once_Combat_Medi_Vail\ | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL02_OnceMedic\AE_Once_Combat_Medi_Vail\AE_Once_Combat_Medi_Vail.nif | UNKNOWN | meshes\ZLJ\CombatLatex\CL02_OnceMedic\ | AE_Once_Combat_Medi_Vail | EXACT_OUTPUT_PATH |
| AE_Once_Combat_Medic | [ZLJ Combat Latex] OnceMedic - AE Once Combat Medic | CalienteTools\BodySlide\SliderSets\AE_Once_Combat_Medic.osp | CalienteTools\BodySlide\SliderSets\ZLJ_CL02_OnceMedic.osp | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL02_OnceMedic\AE_Once_Combat_Medic\ | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL02_OnceMedic\AE_Once_Combat_Medic\AE_Once_Combat_Medic.nif | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL02_OnceMedic\AE_Once_Combat_Medic\AE_Once_Combat_Medic.osd | meshes\ZLJ\CombatLatex\CL02_OnceMedic\ | AE_Once_Combat_Medic | EXACT_OUTPUT_PATH |


## 6. DDS actually in use

Distinct source DDS in the closure: **44**

| source_virtual_path | winning_provider | owning_outfit_of_source | target_virtual_path | action |
|---|---|---|---|---|
| textures\ae once human\am\medic\vail_d.dds | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | CL02_OnceMedic | textures\ZLJ\CombatLatex\CL02_OnceMedic\vail_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae once human\am\medic\vail_n.dds | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | CL02_OnceMedic | textures\ZLJ\CombatLatex\CL02_OnceMedic\vail_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatexBlack_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatexBlack_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae once human\am\medic\vail_n.dds | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | CL02_OnceMedic | textures\ZLJ\CombatLatex\CL02_OnceMedic\vail_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_em.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatex_em.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\expansion\zad_Ebonite_e.dds | 私密装置 乳胶材质 — Better DD Latex - Clean — 【材质·替换】【服装·装备】 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL02_OnceMedic\zad_Ebonite_e.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae once human\am\medic\vail_d.dds | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | CL02_OnceMedic | textures\ZLJ\CombatLatex\CL02_OnceMedic\vail_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae once human\am\medic\vail_n.dds | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | CL02_OnceMedic | textures\ZLJ\CombatLatex\CL02_OnceMedic\vail_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae once human\am\medic\vail_s.dds | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | CL02_OnceMedic | textures\ZLJ\CombatLatex\CL02_OnceMedic\vail_s.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae once human\am\medic\mc_enamel3.dds | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | CL02_OnceMedic | textures\ZLJ\CombatLatex\CL02_OnceMedic\mc_enamel3.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\actors\character\female\femalebody_1.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\femalebody_1_msn.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\femalebody_1_s.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\femalebody_etc_v2_1.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\femalebody_etc_v2_1_msn.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\femalebody_etc_v2_1_s.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\femalebody_etc_v2_1.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\femalebody_etc_v2_1_msn.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\actors\character\female\femalebody_etc_v2_1_s.dds | BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】 | EXTERNAL_MOD |  | KEEP_EXTERNAL_REFERENCE |
| textures\devious\devices\catsuitLatexBlack_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatexBlack_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae once human\am\medic\skirt_n.dds | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | CL02_OnceMedic | textures\ZLJ\CombatLatex\CL02_OnceMedic\skirt_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_em.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatex_em.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\expansion\zad_Ebonite_e.dds | 私密装置 乳胶材质 — Better DD Latex - Clean — 【材质·替换】【服装·装备】 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL02_OnceMedic\zad_Ebonite_e.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatexBlack_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatexBlack_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae once human\am\medic\f_coat15_normal.pvr.dds | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | CL02_OnceMedic | textures\ZLJ\CombatLatex\CL02_OnceMedic\f_coat15_normal.pvr.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_em.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatex_em.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\expansion\zad_Ebonite_e.dds | 私密装置 乳胶材质 — Better DD Latex - Clean — 【材质·替换】【服装·装备】 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL02_OnceMedic\zad_Ebonite_e.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatexWhite_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatexWhite_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae once human\am\medic\f_coat15_normal.pvr.dds | makaron-COSPLAY - AE_Once_Medic — 【服装·装备】【来源·本地】 | CL02_OnceMedic | textures\ZLJ\CombatLatex\CL02_OnceMedic\f_coat15_normal.pvr.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_em.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatex_em.dds | COPY_INTO_OUTFIT_NAMESPACE |
| `... 128 more rows in the CSV` | | | | |


## 6b. Body morph TRI (not a physics config)

_`none`_


## 6c. Model role (ARMA/ARMO slot semantics)

| model_role | canonical_runtime | body_relevance | old_path | new_path | status |
|---|---|---|---|---|---|
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE Once Human\AM\AE_Once_Combat_Medic_Feet_1.nif | meshes\ZLJ\CombatLatex\CL02_OnceMedic\AE_Once_Combat_Medic_Feet_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE Once Human\AM\AE_Once_Combat_Medic_1.nif | meshes\ZLJ\CombatLatex\CL02_OnceMedic\AE_Once_Combat_Medic_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE Once Human\AM\AE_Once_Combat_Medic_Glove_1.nif | meshes\ZLJ\CombatLatex\CL02_OnceMedic\AE_Once_Combat_Medic_Glove_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE Once Human\AM\Combat_Medic_Hair.nif | meshes\ZLJ\CombatLatex\CL02_OnceMedic\Combat_Medic_Hair.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE Once Human\AM\Combat_Medic_Mask.nif | meshes\ZLJ\CombatLatex\CL02_OnceMedic\Combat_Medic_Mask.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE Once Human\AM\AE_Once_Combat_Medic_Stockings_1.nif | meshes\ZLJ\CombatLatex\CL02_OnceMedic\AE_Once_Combat_Medic_Stockings_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE Once Human\AM\AE_Once_Combat_Medi_Vail_1.nif | meshes\ZLJ\CombatLatex\CL02_OnceMedic\AE_Once_Combat_Medi_Vail_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE Once Human\AM\AE_Once_Combat_Medic_Back_Pack_1.nif | meshes\ZLJ\CombatLatex\CL02_OnceMedic\AE_Once_Combat_Medic_Back_Pack_1.nif | COPY_AND_REPOINT |


Non-canonical roles kept separate: WEARABLE_MALE_3P=8, WORLD_MALE=8, FIRSTPERSON_MALE=2, FIRSTPERSON_FEMALE=2

## 7. Physics

| config_file | config_type | mesh_references | bone_dependencies | rewrite_required | bone_check_status | status |
|---|---|---|---|---|---|---|
| meshes\ae once human\am\sparklers.xml | HDT_SMP_XML | calientetools\bodyslide\shapedata\ae_once_combat_medi_vail\ae_once_combat_medi_vail.nif |  | YES | MISSING_BONE | COPY_AND_REPOINT |


## 8. Existing PBR (provenance only)

No PBR patch mod is registered for this outfit in the P02A registry.

## 9. Cross dependencies (current -> planned)

- cross-outfit texture dependencies: **6** (open after plan: 6)
- external-mod texture dependencies: **66** (open after plan: 24)
- audit counters: cross-outfit open **0** / external-mod-missing **0** / hard-unresolved **0** / vanilla-allowed **0** / shared proposals **0**
- unresolvable DDS by class (distinct files): none - a DDS absent from the frozen P00 VFS is already broken at runtime today; it is listed, never guessed

| dependency_type | source_owner | source_virtual_path | referenced_by_nif | resolution_plan | target_virtual_path | post_plan_state |
|---|---|---|---|---|---|---|
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\1stPersonbody_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\1stPersongloves_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\body_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\body_GO.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\boots_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\boots_GO.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\gloves_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\gloves_GO.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\helmet_GO.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL04_Haley;CL08_SpearHead;CL11_SkimpyAssassin | textures\devious\devices\catsuitLatex_em.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_Feet_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 5 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatex_em.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL03_Tachy;CL04_Haley;CL05_Valby;CL08_SpearHead;CL11_SkimpyAssassin | textures\devious\devices\catsuitLatex_n.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_Glove_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 6 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatex_n.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL04_Haley;CL08_SpearHead;CL11_SkimpyAssassin | textures\devious\devices\catsuitLatexBlack_d.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_Feet_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 5 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatexBlack_d.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL08_SpearHead | textures\devious\devices\catsuitLatexRed_d.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_Glove_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 2 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatexRed_d.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL03_Tachy | textures\devious\devices\catsuitLatexWhite_d.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 2 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatexWhite_d.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL04_Haley;CL08_SpearHead;CL11_SkimpyAssassin | textures\devious\expansion\zad_Ebonite_e.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_Feet_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 5 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL02_OnceMedic\zad_Ebonite_e.dds | CLOSED_BY_DUPLICATION |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatexBlack_d.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medi_Vail_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatexBlack_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatexBlack_d.dds and repoint meshes\AE Once Human\AM\AE_Once_Combat_Medi_Vail_1.nif / KSSMP_Sparklers 2 / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatexBlack_d.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatex_em.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medi_Vail_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatex_em.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatex_em.dds and repoint meshes\AE Once Human\AM\AE_Once_Combat_Medi_Vail_1.nif / KSSMP_Sparklers 2 / EnvMask so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatex_em.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\expansion\zad_Ebonite_e.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medi_Vail_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor zad_Ebonite_e.dds (provider 私密装置 乳胶材质 — Better DD Latex - Clean — 【材质·替换】【服装·装备】, priority 767) into textures\ZLJ\CombatLatex\CL02_OnceMedic\zad_Ebonite_e.dds and repoint meshes\AE Once Human\AM\AE_Once_Combat_Medi_Vail_1.nif / KSSMP_Sparklers 2 / EnvMap so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL02_OnceMedic\zad_Ebonite_e.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1_msn.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1_s.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_msn.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_s.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_msn.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_s.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatexBlack_d.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatexBlack_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatexBlack_d.dds and repoint meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif / "f_coat15_3".004_"f_coat15_3"_mesh0004.001 / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatexBlack_d.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatex_em.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatex_em.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatex_em.dds and repoint meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif / "f_coat15_3".004_"f_coat15_3"_mesh0004.001 / EnvMask so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL02_OnceMedic\catsuitLatex_em.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\expansion\zad_Ebonite_e.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor zad_Ebonite_e.dds (provider 私密装置 乳胶材质 — Better DD Latex - Clean — 【材质·替换】【服装·装备】, priority 767) into textures\ZLJ\CombatLatex\CL02_OnceMedic\zad_Ebonite_e.dds and repoint meshes\AE Once Human\AM\AE_Once_Combat_Medic_1.nif / "f_coat15_3".004_"f_coat15_3"_mesh0004.001 / EnvMap so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL02_OnceMedic\zad_Ebonite_e.dds | CLOSED |
| `... 60 more rows in the CSV` | | | | | | |


## 10. Self-containment audit (simulated post-migration)

| gate | result | metric | evidence |
|---|---|---|---|
| GAME_MESH_SELF_CONTAINED | PASS | 22 | game mesh rows=22, target off-namespace=0, collisions=0 |
| TEXTURE_SELF_CONTAINED | REVIEW | 248 | slots(nif=158 shapedata=90) / off-namespace=0 / provider-found=0 / true-missing=0 / path-mismatch-unknown=0 / no-lookup=0 / vanilla=0 / global-body-skin=0 / proposals=42 / open cross-outfit=0 |
| BODYSLIDE_SELF_CONTAINED | BLOCKED | 1 | projects=2 chain-incomplete=1 OSP-off-ns=0 ShapeData-off-ns=0 Output-off-ns=0 UNKNOWN-basis=0 shapedata-tex-off-ns=0 |
| PLUGIN_PATHS_PLANNED | REVIEW | 16 | records=16 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=8 flagged-canonical=8 world-models=8 plugin-DDS-cross-outfit-open=0 / model refs: source-asset-absent=0 foreign-body-decision=6 |
| MODEL_ROLE_SCHEMA | PASS | 28 | role enum violations (legacy WORLD/WEARABLE/GROUND)=0, unknown-enum=0 / distribution: WEARABLE_MALE_3P=8, WEARABLE_FEMALE_3P=8, WORLD_MALE=8, FIRSTPERSON_MALE=2, FIRSTPERSON_FEMALE=2 |
| PHYSICS_PATHS_PLANNED | REVIEW | 1 | physics configs=1 types=HDT_SMP_XML=1 / without-new-path=0 bone-unknown=1 |
| TRI_MORPH_SEPARATION | PASS | 0 | morph rows=0 (.tri sources=0) / TRI rows wrongly present in physics table=0 / physics types=HDT_SMP_XML=1 |
| TARGET_OSP_NAMESPACE | PASS | 1 | distinct target OSP for this outfit=1 expected=1 -> ['calientetools/bodyslide/slidersets/zlj_cl02_oncemedic.osp'] |
| UNRESOLVED_REFERENCE_PROVENANCE | PASS | 0 | distinct unresolved DDS=0, without a global provider-lookup verdict=0, rows whose texture set is not derivable at all (BSA-resident stock mesh, no path to look up)=9 |
| OUTFIT_SELF_CONTAINMENT | BLOCKED | 9 | C1..C9 = C1:PASS, C2:REVIEW, C3:BLOCKED, C4:REVIEW, C6:PASS, C5:REVIEW, G7:PASS, C8:PASS, C9:PASS |


## 11. BLOCKERS

- `C2` TEXTURE_SELF_CONTAINED = **REVIEW** - slots(nif=158 shapedata=90) | off-namespace=0 | provider-found=0 | true-missing=0 | path-mismatch-unknown=0 | no-lookup=0 | vanilla=0 | global-body-skin=0 | proposals=42 | open cross-outfit=0
- `C3` BODYSLIDE_SELF_CONTAINED = **BLOCKED** - projects=2 chain-incomplete=1 OSP-off-ns=0 ShapeData-off-ns=0 Output-off-ns=0 UNKNOWN-basis=0 shapedata-tex-off-ns=0
- `C4` PLUGIN_PATHS_PLANNED = **REVIEW** - records=16 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=8 flagged-canonical=8 world-models=8 plugin-DDS-cross-outfit-open=0 | model refs: source-asset-absent=0 foreign-body-decision=6
- `C5` PHYSICS_PATHS_PLANNED = **REVIEW** - physics configs=1 types=HDT_SMP_XML=1 | without-new-path=0 bone-unknown=1
- `TOTAL` OUTFIT_SELF_CONTAINMENT = **BLOCKED** - C1..C9 = C1:PASS, C2:REVIEW, C3:BLOCKED, C4:REVIEW, C6:PASS, C5:REVIEW, G7:PASS, C8:PASS, C9:PASS

---

P02A stops here. No COPY / MOVE / DELETE / NIF / ESP / OSP / DDS write was performed and none is authorised until this design is reviewed by a human.
