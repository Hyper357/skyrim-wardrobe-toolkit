# CL05_Valby - P02A migration manifest

> Pack: `ZLJ_COMBAT_LATEX` (ZLJ Combat Latex Pack) - canonical body `CBBE_3BA` - target plugin `ZLJ_CombatLatex.esp`
> Phase: **P02A design ledger (STRICT READ-ONLY)** - nothing has been copied, moved, renamed or rewritten.

| field | value |
|---|---|
| Outfit ID (frozen) | `CL05_Valby` |
| Source mod(s) | `makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】` |
| Plugin (current) | `AE_TFD_Valby_Nano_Suit.esp` |
| Support mods | NONE |
| Target mesh ns | `meshes\ZLJ\CombatLatex\CL05_Valby\` |
| Target texture ns | `textures\ZLJ\CombatLatex\CL05_Valby\` |
| Target ShapeData ns | `CalienteTools\BodySlide\ShapeData\ZLJ_CombatLatex\CL05_Valby\` |
| Target SliderSet | `CalienteTools\BodySlide\SliderSets\ZLJ_CL05_Valby.osp` |

## 1. Source Mods

| MOD_ID | MO2 priority (low = wins) | role | file_count | plugin |
|---|---|---|---|---|
| makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | 920 | BASE | 41 | AE_TFD_Valby_Nano_Suit.esp |


## 2. Winning Providers

| winning_provider | VFS paths won |
|---|---|
| makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | 40 |
|  | 21 |
| Nyes Latex Pack AiO 1.3 (ReducedSize) | 1 |


## 3. Plugin Records

Counts by record type: `ARMA`=5, `ARMO`=5  
Target plugin: `ZLJ_CombatLatex.esp` - new EDID namespace: `ZLJ_CL_Valby_<PART>` - **no FormID generated in P02A**

| record_type | formid | edid | new_edid | notes |
|---|---|---|---|---|
| ARMA | 01000001 | AE_TFD_Valby_Nano_SuitAltAA | ZLJ_CL_Valby_BODY_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D62 | AE_TFD_Valby_Nano_Suit_FeetAA | ZLJ_CL_Valby_LOWERLEG_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D63 | AE_TFD_Valby_Nano_SuitAA | ZLJ_CL_Valby_BODY_AA_2 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D64 | AE_TFD_Valby_Nano_Suit_HandAA | ZLJ_CL_Valby_HANDS_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D65 | AE_TFD_Valby_Nano_Suit_HelmetAA | ZLJ_CL_Valby_HAIR_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMO | 01000002 | AE_TFD_Valby_Nano_Suit_Alt | ZLJ_CL_Valby_BODY | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=CBBE_3BA / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 01000D66 | AE_TFD_Valby_Nano_Suit_Feet | ZLJ_CL_Valby_LOWERLEG | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 01000D67 | AE_TFD_Valby_Nano_Suit | ZLJ_CL_Valby_BODY_2 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=CBBE_3BA / P00_BODYSLIDE_MATCH=EXACT_OUTPUT_PATH / P00_PHYSICS=no |
| ARMO | 01000D68 | AE_TFD_Valby_Nano_Suit_Hand | ZLJ_CL_Valby_HANDS | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 01000D69 | AE_TFD_Valby_Nano_Suit_Helmet | ZLJ_CL_Valby_HAIR | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |


## 4. Game Mesh

| mesh_role | source_virtual_path | source_provider | target_virtual_path | retain |
|---|---|---|---|---|
| PHYSICS_1 | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL05_Valby\AE_TFD_Valby_Nano_Suit_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1st_1.nif | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL05_Valby\1p\AE_TFD_Valby_Nano_Suit_1st_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_Alt_1.nif | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL05_Valby\AE_TFD_Valby_Nano_Suit_Alt_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_Feet_1.nif | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL05_Valby\AE_TFD_Valby_Nano_Suit_Feet_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_Hand_1.nif | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL05_Valby\1p\AE_TFD_Valby_Nano_Suit_Hand_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_Hand_1.nif | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL05_Valby\AE_TFD_Valby_Nano_Suit_Hand_1.nif | KEEP |
| PLAIN_NIF | meshes\AE_TFD_Valby_Nano_Suit\Helmet.nif | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL05_Valby\Helmet.nif | KEEP |
| PLAIN_NIF | meshes\AE_TFD_Valby_Nano_Suit\Helmet.nif | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL05_Valby\male\Helmet.nif | KEEP |
| PHYSICS_1 | meshes\Armor\Studded\Male\1stPersonbody_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL05_Valby\male\1p\1stPersonbody_1.nif | REVIEW |
| PHYSICS_1 | meshes\Armor\Studded\Male\1stPersongloves_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL05_Valby\male\1p\1stPersongloves_1.nif | REVIEW |
| PHYSICS_1 | meshes\Armor\Studded\Male\body_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL05_Valby\male\body_1.nif | REVIEW |
| STATIC_GO | meshes\Armor\Studded\Male\body_GO.nif | Static Mesh Improvement Mod - SMIM — 【网格·环境】 | meshes\ZLJ\CombatLatex\CL05_Valby\world\male\body_GO.nif | KEEP |
| PHYSICS_1 | meshes\Armor\Studded\Male\boots_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL05_Valby\male\boots_1.nif | REVIEW |
| STATIC_GO | meshes\Armor\Studded\Male\boots_GO.nif | UNKNOWN | meshes\ZLJ\CombatLatex\CL05_Valby\world\male\boots_GO.nif | KEEP |
| PHYSICS_1 | meshes\Armor\Studded\Male\gloves_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL05_Valby\male\gloves_1.nif | REVIEW |
| STATIC_GO | meshes\Armor\Studded\Male\gloves_GO.nif | UNKNOWN | meshes\ZLJ\CombatLatex\CL05_Valby\world\male\gloves_GO.nif | KEEP |
| STATIC_GO | meshes\Armor\Studded\Male\helmet_GO.nif | UNKNOWN | meshes\ZLJ\CombatLatex\CL05_Valby\world\male\helmet_GO.nif | KEEP |


## 5. ShapeData / OSP / OSD

| old_ui_name | new_ui_name | old_osp | new_osp | new_shape_data | new_input_nif | new_osd | new_output_path | new_output_file | basis |
|---|---|---|---|---|---|---|---|---|---|
| AE_TFD_Valby_Nano_Suit | [ZLJ Combat Latex] Valby - AE TFD Valby Nano Suit | CalienteTools\BodySlide\SliderSets\AE_TFD_Valby_Nano_Suit.osp | CalienteTools\BodySlide\SliderSets\ZLJ_CL05_Valby.osp | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL05_Valby\AE_TFD_Valby_Nano_Suit\ | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL05_Valby\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit.nif | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL05_Valby\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit.osd | meshes\ZLJ\CombatLatex\CL05_Valby\ | AE_TFD_Valby_Nano_Suit | EXACT_OUTPUT_PATH |


## 6. DDS actually in use

Distinct source DDS in the closure: **22**

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
| Textures\devious\devices\YokeFront_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_tfd_valby_nano_suit\pc_010_u_cmn_001_body_partb_n.dds | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | CL05_Valby | textures\ZLJ\CombatLatex\CL05_Valby\pc_010_u_cmn_001_body_partb_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_tfd_valby_nano_suit\pc_010_u_cmn_001_body_partb_s.dds | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | CL05_Valby | textures\ZLJ\CombatLatex\CL05_Valby\pc_010_u_cmn_001_body_partb_s.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_tfd_valby_nano_suit\macro_matcap_1.dds | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | CL05_Valby | textures\ZLJ\CombatLatex\CL05_Valby\macro_matcap_1.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_tfd_valby_nano_suit\pc_010_u_cmn_001_body_parta_c.dds | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | CL05_Valby | textures\ZLJ\CombatLatex\CL05_Valby\pc_010_u_cmn_001_body_parta_c.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_tfd_valby_nano_suit\pc_010_u_cmn_001_body_parta_n.dds | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | CL05_Valby | textures\ZLJ\CombatLatex\CL05_Valby\pc_010_u_cmn_001_body_parta_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_tfd_valby_nano_suit\pc_010_u_cmn_001_body_parta_s.dds | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | CL05_Valby | textures\ZLJ\CombatLatex\CL05_Valby\pc_010_u_cmn_001_body_parta_s.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_tfd_valby_nano_suit\macro_matcap_1.dds | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | CL05_Valby | textures\ZLJ\CombatLatex\CL05_Valby\macro_matcap_1.dds | COPY_INTO_OUTFIT_NAMESPACE |
| Textures\devious\devices\YokeFront_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_tfd_valby_nano_suit\pc_010_u_cmn_001_body_parta_n.dds | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | CL05_Valby | textures\ZLJ\CombatLatex\CL05_Valby\pc_010_u_cmn_001_body_parta_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_tfd_valby_nano_suit\pc_010_u_cmn_001_body_parta_s.dds | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | CL05_Valby | textures\ZLJ\CombatLatex\CL05_Valby\pc_010_u_cmn_001_body_parta_s.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_tfd_valby_nano_suit\macro_matcap_1.dds | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | CL05_Valby | textures\ZLJ\CombatLatex\CL05_Valby\macro_matcap_1.dds | COPY_INTO_OUTFIT_NAMESPACE |
| Textures\devious\devices\YokeFront_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_tfd_valby_nano_suit\pc_010_u_cmn_001_body_parta_n.dds | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | CL05_Valby | textures\ZLJ\CombatLatex\CL05_Valby\pc_010_u_cmn_001_body_parta_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_tfd_valby_nano_suit\pc_010_u_cmn_001_body_parta_s.dds | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | CL05_Valby | textures\ZLJ\CombatLatex\CL05_Valby\pc_010_u_cmn_001_body_parta_s.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_tfd_valby_nano_suit\macro_matcap_1.dds | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | CL05_Valby | textures\ZLJ\CombatLatex\CL05_Valby\macro_matcap_1.dds | COPY_INTO_OUTFIT_NAMESPACE |
| Textures\devious\devices\YokeFront_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_tfd_valby_nano_suit\pc_010_u_cmn_001_body_parta_n.dds | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | CL05_Valby | textures\ZLJ\CombatLatex\CL05_Valby\pc_010_u_cmn_001_body_parta_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_tfd_valby_nano_suit\pc_010_u_cmn_001_body_parta_s.dds | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | CL05_Valby | textures\ZLJ\CombatLatex\CL05_Valby\pc_010_u_cmn_001_body_parta_s.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_tfd_valby_nano_suit\macro_matcap_1.dds | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 | CL05_Valby | textures\ZLJ\CombatLatex\CL05_Valby\macro_matcap_1.dds | COPY_INTO_OUTFIT_NAMESPACE |
| Textures\devious\devices\YokeFront_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| `... 214 more rows in the CSV` | | | | |


## 6b. Body morph TRI (not a physics config)

_`none`_


## 6c. Model role (ARMA/ARMO slot semantics)

| model_role | canonical_runtime | body_relevance | old_path | new_path | status |
|---|---|---|---|---|---|
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_Alt_1.nif | meshes\ZLJ\CombatLatex\CL05_Valby\AE_TFD_Valby_Nano_Suit_Alt_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_Feet_1.nif | meshes\ZLJ\CombatLatex\CL05_Valby\AE_TFD_Valby_Nano_Suit_Feet_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | meshes\ZLJ\CombatLatex\CL05_Valby\AE_TFD_Valby_Nano_Suit_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_Hand_1.nif | meshes\ZLJ\CombatLatex\CL05_Valby\AE_TFD_Valby_Nano_Suit_Hand_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_TFD_Valby_Nano_Suit\Helmet.nif | meshes\ZLJ\CombatLatex\CL05_Valby\Helmet.nif | COPY_AND_REPOINT |


Non-canonical roles kept separate: WEARABLE_MALE_3P=5, WORLD_MALE=5, FIRSTPERSON_MALE=3, FIRSTPERSON_FEMALE=3

## 7. Physics

_`none`_


## 8. Existing PBR (provenance only)

No PBR patch mod is registered for this outfit in the P02A registry.

## 9. Cross dependencies (current -> planned)

- cross-outfit texture dependencies: **2** (open after plan: 2)
- external-mod texture dependencies: **55** (open after plan: 27)
- audit counters: cross-outfit open **0** / external-mod-missing **0** / hard-unresolved **3** / vanilla-allowed **0** / shared proposals **0**
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
| CROSS_PACK_CANDIDATE | CL02_OnceMedic;CL03_Tachy;CL04_Haley;CL08_SpearHead;CL11_SkimpyAssassin | textures\devious\devices\catsuitLatex_n.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_Glove_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 6 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL05_Valby\catsuitLatex_n.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL04_Haley | Textures\devious\devices\YokeFront_d.dds | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 2 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds | CLOSED_BY_DUPLICATION |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1_msn.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1_s.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_msn.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_s.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_msn.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_s.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | Textures\devious\devices\YokeFront_d.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor YokeFront_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds and repoint meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif / PC_010_U_CMN_BODY_001_LOD0.006_PC_010_U_CMN_BODY_001_LOD0.231 / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | Textures\devious\devices\YokeFront_d.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor YokeFront_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds and repoint meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif / PC_010_U_CMN_BODY_001_LOD0.012_PC_010_U_CMN_BODY_001_LOD0.195 / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | Textures\devious\devices\YokeFront_d.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor YokeFront_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds and repoint meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif / PC_010_U_CMN_BODY_001_LOD0.023_PC_010_U_CMN_BODY_001_LOD0.206 / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | Textures\devious\devices\YokeFront_d.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor YokeFront_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds and repoint meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif / PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220 / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | Textures\devious\devices\YokeFront_d.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor YokeFront_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds and repoint meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif / PC_010_U_CMN_BODY_001_LOD0.035_PC_010_U_CMN_BODY_001_LOD0.218 / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | Textures\devious\devices\YokeFront_d.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor YokeFront_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds and repoint meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif / PC_010_U_CMN_BODY_001_LOD0.011_PC_010_U_CMN_BODY_001_LOD0.194 / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds | CLOSED |
| UNRESOLVED | UNKNOWN | textures\PC_010_U_CMN_001_Body_PartA_N.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | BLOCKED: PATH-MISMATCH, not fuzzy-resolvable: the referenced folder does not exist, only same-basename files elsewhere were found. Those are NOT treated as the same asset. Candidate locations are recorded in P02A_GLOBAL_PROVIDER_LOOKUP.csv: input reference_class=UNKNOWN; probed forms: textures/pc_010_u_cmn_001_body_parta_n.dds; loose game Data hit: none; PATH MISMATCH: the referenced folder does not exist, but 1 mod(s) in this instance ship a file with the same basename elsewhere: makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】 :: Textures/AE_TFD_Valby_Nano_Suit/PC_010_U_CMN_001_Body_PartA_N.dds; NOT upgraded to EXTERNAL_PROVIDER_FOUND: no provider exists at the referenced path, and a same-basename file elsewhere is NOT proof of the same asset -- identity would be a fuzzy match, which this stage forbids. Left UNKNOWN for human confirmation; winning provider is a PATH-MISMATCH provider, not a provider of the referenced path; winning provider is in the frozen P00 TARGET09 scope; game Data root has no loose 'textures' folder and holds 93 .bsa archives. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| EXTERNAL_MOD | EXTERNAL_MOD | Textures\devious\devices\YokeFront_d.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor YokeFront_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds and repoint meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif / PC_010_U_CMN_BODY_001_LOD0.002_PC_010_U_CMN_BODY_001_LOD0.186 / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL05_Valby\YokeFront_d.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatex_n.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatex_n.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL05_Valby\catsuitLatex_n.dds and repoint meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif / PC_010_U_CMN_BODY_001_LOD0 / Normal so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL05_Valby\catsuitLatex_n.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatex_n.dds | meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatex_n.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL05_Valby\catsuitLatex_n.dds and repoint meshes\AE_TFD_Valby_Nano_Suit\AE_TFD_Valby_Nano_Suit_1.nif / PC_010_U_CMN_BODY_001_LOD0.003_PC_010_U_CMN_BODY_001_LOD0.227 / Normal so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL05_Valby\catsuitLatex_n.dds | CLOSED |
| `... 47 more rows in the CSV` | | | | | | |


## 10. Self-containment audit (simulated post-migration)

| gate | result | metric | evidence |
|---|---|---|---|
| GAME_MESH_SELF_CONTAINED | PASS | 17 | game mesh rows=17, target off-namespace=0, collisions=0 |
| TEXTURE_SELF_CONTAINED | REVIEW | 409 | slots(nif=244 shapedata=168) / off-namespace=0 / provider-found=0 / true-missing=0 / path-mismatch-unknown=3 / no-lookup=0 / vanilla=0 / global-body-skin=0 / proposals=28 / open cross-outfit=0 |
| BODYSLIDE_SELF_CONTAINED | PASS | 1 | projects=1 chain-incomplete=0 OSP-off-ns=0 ShapeData-off-ns=0 Output-off-ns=0 UNKNOWN-basis=0 shapedata-tex-off-ns=0 |
| PLUGIN_PATHS_PLANNED | REVIEW | 10 | records=10 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=5 flagged-canonical=5 world-models=5 plugin-DDS-cross-outfit-open=0 / model refs: source-asset-absent=0 foreign-body-decision=7 |
| MODEL_ROLE_SCHEMA | PASS | 21 | role enum violations (legacy WORLD/WEARABLE/GROUND)=0, unknown-enum=0 / distribution: WEARABLE_MALE_3P=5, WEARABLE_FEMALE_3P=5, WORLD_MALE=5, FIRSTPERSON_MALE=3, FIRSTPERSON_FEMALE=3 |
| PHYSICS_PATHS_PLANNED | PASS | 0 | physics configs=0 types= / without-new-path=0 bone-unknown=0 |
| TRI_MORPH_SEPARATION | PASS | 0 | morph rows=0 (.tri sources=0) / TRI rows wrongly present in physics table=0 / physics types= |
| TARGET_OSP_NAMESPACE | PASS | 1 | distinct target OSP for this outfit=1 expected=1 -> ['calientetools/bodyslide/slidersets/zlj_cl05_valby.osp'] |
| UNRESOLVED_REFERENCE_PROVENANCE | REVIEW | 1 | distinct unresolved DDS=1, without a global provider-lookup verdict=0, rows whose texture set is not derivable at all (BSA-resident stock mesh, no path to look up)=9 |
| OUTFIT_SELF_CONTAINMENT | REVIEW | 9 | C1..C9 = C1:PASS, C2:REVIEW, C3:PASS, C4:REVIEW, C6:PASS, C5:PASS, G7:PASS, C8:PASS, C9:REVIEW |


## 11. BLOCKERS

- `C2` TEXTURE_SELF_CONTAINED = **REVIEW** - slots(nif=244 shapedata=168) | off-namespace=0 | provider-found=0 | true-missing=0 | path-mismatch-unknown=3 | no-lookup=0 | vanilla=0 | global-body-skin=0 | proposals=28 | open cross-outfit=0
- `C4` PLUGIN_PATHS_PLANNED = **REVIEW** - records=10 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=5 flagged-canonical=5 world-models=5 plugin-DDS-cross-outfit-open=0 | model refs: source-asset-absent=0 foreign-body-decision=7
- `C9` UNRESOLVED_REFERENCE_PROVENANCE = **REVIEW** - distinct unresolved DDS=1, without a global provider-lookup verdict=0, rows whose texture set is not derivable at all (BSA-resident stock mesh, no path to look up)=9
- `TOTAL` OUTFIT_SELF_CONTAINMENT = **REVIEW** - C1..C9 = C1:PASS, C2:REVIEW, C3:PASS, C4:REVIEW, C6:PASS, C5:PASS, G7:PASS, C8:PASS, C9:REVIEW

---

P02A stops here. No COPY / MOVE / DELETE / NIF / ESP / OSP / DDS write was performed and none is authorised until this design is reviewed by a human.
