# CL07_Lupa - P02A migration manifest

> Pack: `ZLJ_COMBAT_LATEX` (ZLJ Combat Latex Pack) - canonical body `CBBE_3BA` - target plugin `ZLJ_CombatLatex.esp`
> Phase: **P02A design ledger (STRICT READ-ONLY)** - nothing has been copied, moved, renamed or rewritten.

| field | value |
|---|---|
| Outfit ID (frozen) | `CL07_Lupa` |
| Source mod(s) | `makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】` |
| Plugin (current) | `AE_Wuthering_Waves_Lupa.esp` |
| Support mods | NONE |
| Target mesh ns | `meshes\ZLJ\CombatLatex\CL07_Lupa\` |
| Target texture ns | `textures\ZLJ\CombatLatex\CL07_Lupa\` |
| Target ShapeData ns | `CalienteTools\BodySlide\ShapeData\ZLJ_CombatLatex\CL07_Lupa\` |
| Target SliderSet | `CalienteTools\BodySlide\SliderSets\ZLJ_CL07_Lupa.osp` |

## 1. Source Mods

| MOD_ID | MO2 priority (low = wins) | role | file_count | plugin |
|---|---|---|---|---|
| makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | 918 | BASE | 44 | AE_Wuthering_Waves_Lupa.esp |


## 2. Winning Providers

| winning_provider | VFS paths won |
|---|---|
| makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | 43 |
|  | 22 |
| makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | 6 |
| Nyes Latex Pack AiO 1.3 (ReducedSize) | 1 |


## 3. Plugin Records

Counts by record type: `ARMA`=7, `ARMO`=7  
Target plugin: `ZLJ_CombatLatex.esp` - new EDID namespace: `ZLJ_CL_Lupa_<PART>` - **no FormID generated in P02A**

| record_type | formid | edid | new_edid | notes |
|---|---|---|---|---|
| ARMA | 01000D62 | AE_Wuthering_Waves_Lupa_FeetAA | ZLJ_CL_Lupa_LOWERLEG_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D63 | AE_Wuthering_Waves_Lupa_BodyAA | ZLJ_CL_Lupa_BODY_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D64 | AE_Wuthering_Waves_Lupa_HandAA | ZLJ_CL_Lupa_HANDS_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D65 | AE_Wuthering_Waves_Lupa_HairAA | ZLJ_CL_Lupa_HAIR_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D6A | AE_Wuthering_Waves_Lupa_MantAA | ZLJ_CL_Lupa_CHEST_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D6B | AE_Wuthering_Waves_Lupa_HairACCAA | ZLJ_CL_Lupa_FRONT_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D6C | AE_Wuthering_Waves_Lupa_TailAA | ZLJ_CL_Lupa_RIGHTSHOULDER_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMO | 01000D66 | AE_Wuthering_Waves_Lupa_Feet | ZLJ_CL_Lupa_LOWERLEG | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 01000D67 | AE_Wuthering_Waves_Lupa_Body | ZLJ_CL_Lupa_BODY | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=BODY / P00_BODY_CANDIDATE=CBBE_3BA / P00_BODYSLIDE_MATCH=EXACT_OUTPUT_PATH / P00_PHYSICS=no |
| ARMO | 01000D68 | AE_Wuthering_Waves_Lupa_Hand | ZLJ_CL_Lupa_HANDS | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 01000D69 | AE_Wuthering_Waves_Lupa_Hair | ZLJ_CL_Lupa_HAIR | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 01000D6D | AE_Wuthering_Waves_Lupa_HairACC | ZLJ_CL_Lupa_FRONT | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 01000D6E | AE_Wuthering_Waves_Lupa_Mant | ZLJ_CL_Lupa_CHEST | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=EXACT_OUTPUT_PATH / P00_PHYSICS=no |
| ARMO | 01000D6F | AE_Wuthering_Waves_Lupa_Tail | ZLJ_CL_Lupa_RIGHTSHOULDER | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=TAIL / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |


## 4. Game Mesh

| mesh_role | source_virtual_path | source_provider | target_virtual_path | retain |
|---|---|---|---|---|
| PHYSICS_1 | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL07_Lupa\1p\AE_Wuthering_Waves_Lupa_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL07_Lupa\AE_Wuthering_Waves_Lupa_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_Feet_1.nif | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL07_Lupa\AE_Wuthering_Waves_Lupa_Feet_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_Hand_1.nif | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL07_Lupa\1p\AE_Wuthering_Waves_Lupa_Hand_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_Hand_1.nif | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL07_Lupa\AE_Wuthering_Waves_Lupa_Hand_1.nif | KEEP |
| PHYSICS_1 | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_Mant_1.nif | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL07_Lupa\AE_Wuthering_Waves_Lupa_Mant_1.nif | KEEP |
| PLAIN_NIF | meshes\AE_Wuthering_Waves_Lupa\Hair.nif | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL07_Lupa\Hair.nif | KEEP |
| PLAIN_NIF | meshes\AE_Wuthering_Waves_Lupa\Hair.nif | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL07_Lupa\male\Hair.nif | KEEP |
| PLAIN_NIF | meshes\AE_Wuthering_Waves_Lupa\HeadACC.nif | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL07_Lupa\HeadACC.nif | KEEP |
| PLAIN_NIF | meshes\AE_Wuthering_Waves_Lupa\HeadACC.nif | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL07_Lupa\male\HeadACC.nif | KEEP |
| PLAIN_NIF | meshes\AE_Wuthering_Waves_Lupa\Tail.nif | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL07_Lupa\Tail.nif | KEEP |
| PLAIN_NIF | meshes\AE_Wuthering_Waves_Lupa\Tail.nif | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL07_Lupa\male\Tail.nif | KEEP |
| PHYSICS_1 | meshes\Armor\Studded\Male\1stPersonbody_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL07_Lupa\male\1p\1stPersonbody_1.nif | REVIEW |
| PHYSICS_1 | meshes\Armor\Studded\Male\1stPersongloves_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL07_Lupa\male\1p\1stPersongloves_1.nif | REVIEW |
| PHYSICS_1 | meshes\Armor\Studded\Male\body_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL07_Lupa\male\body_1.nif | REVIEW |
| STATIC_GO | meshes\Armor\Studded\Male\body_GO.nif | Static Mesh Improvement Mod - SMIM — 【网格·环境】 | meshes\ZLJ\CombatLatex\CL07_Lupa\world\male\body_GO.nif | KEEP |
| PHYSICS_1 | meshes\Armor\Studded\Male\boots_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL07_Lupa\male\boots_1.nif | REVIEW |
| STATIC_GO | meshes\Armor\Studded\Male\boots_GO.nif | UNKNOWN | meshes\ZLJ\CombatLatex\CL07_Lupa\world\male\boots_GO.nif | KEEP |
| PHYSICS_1 | meshes\Armor\Studded\Male\gloves_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL07_Lupa\male\gloves_1.nif | REVIEW |
| STATIC_GO | meshes\Armor\Studded\Male\gloves_GO.nif | UNKNOWN | meshes\ZLJ\CombatLatex\CL07_Lupa\world\male\gloves_GO.nif | KEEP |
| STATIC_GO | meshes\Armor\Studded\Male\helmet_GO.nif | UNKNOWN | meshes\ZLJ\CombatLatex\CL07_Lupa\world\male\helmet_GO.nif | KEEP |


## 5. ShapeData / OSP / OSD

| old_ui_name | new_ui_name | old_osp | new_osp | new_shape_data | new_input_nif | new_osd | new_output_path | new_output_file | basis |
|---|---|---|---|---|---|---|---|---|---|
| AE_Wuthering_Waves_Lupa | [ZLJ Combat Latex] Lupa - AE Wuthering Waves Lupa | CalienteTools\BodySlide\SliderSets\AE_Wuthering_Waves_Lupa.osp | CalienteTools\BodySlide\SliderSets\ZLJ_CL07_Lupa.osp | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL07_Lupa\AE_Wuthering_Waves_Lupa\ | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL07_Lupa\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa.nif | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL07_Lupa\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa.osd | meshes\ZLJ\CombatLatex\CL07_Lupa\ | AE_Wuthering_Waves_Lupa | EXACT_OUTPUT_PATH |
| AE_Wuthering_Waves_Lupa_Mant | [ZLJ Combat Latex] Lupa - AE Wuthering Waves Lupa Mant | CalienteTools\BodySlide\SliderSets\AE_Wuthering_Waves_Lupa_Mant.osp | CalienteTools\BodySlide\SliderSets\ZLJ_CL07_Lupa.osp | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL07_Lupa\AE_Wuthering_Waves_Lupa_Mant\ | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL07_Lupa\AE_Wuthering_Waves_Lupa_Mant\AE_Wuthering_Waves_Lupa_Mant.nif | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL07_Lupa\AE_Wuthering_Waves_Lupa_Mant\AE_Wuthering_Waves_Lupa_Mant.osd | meshes\ZLJ\CombatLatex\CL07_Lupa\ | AE_Wuthering_Waves_Lupa_Mant | EXACT_OUTPUT_PATH |


## 6. DDS actually in use

Distinct source DDS in the closure: **28**

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
| textures\ae_wuthering_waves_lupa\up_cloth.dds | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | CL07_Lupa | textures\ZLJ\CombatLatex\CL07_Lupa\up_cloth.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_wuthering_waves_lupa\up_n.dds | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | CL07_Lupa | textures\ZLJ\CombatLatex\CL07_Lupa\up_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_wuthering_waves_lupa\standardcubemap.dds | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | CL07_Lupa | textures\ZLJ\CombatLatex\CL07_Lupa\standardcubemap.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_latex_kitty\metal.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL07_Lupa\metal.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_wuthering_waves_lupa\up_n.dds | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | CL07_Lupa | textures\ZLJ\CombatLatex\CL07_Lupa\up_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_wuthering_waves_lupa\standardcubemap.dds | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | CL07_Lupa | textures\ZLJ\CombatLatex\CL07_Lupa\standardcubemap.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_latex_kitty\metal.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL07_Lupa\metal.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_wuthering_waves_lupa\up_n.dds | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | CL07_Lupa | textures\ZLJ\CombatLatex\CL07_Lupa\up_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_wuthering_waves_lupa\standardcubemap.dds | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | CL07_Lupa | textures\ZLJ\CombatLatex\CL07_Lupa\standardcubemap.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_curse_bunny\latex\d.dds | UNKNOWN | UNKNOWN |  | UNRESOLVED |
| textures\ae_wuthering_waves_lupa\up_n.dds | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | CL07_Lupa | textures\ZLJ\CombatLatex\CL07_Lupa\up_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_curse_bunny\shkurka_body_mask.dds | UNKNOWN | UNKNOWN |  | UNRESOLVED |
| textures\ae_curse_bunny\pink022.dds | UNKNOWN | UNKNOWN |  | UNRESOLVED |
| textures\ae_latex_kitty\metal.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL07_Lupa\metal.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_wuthering_waves_lupa\up_n.dds | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | CL07_Lupa | textures\ZLJ\CombatLatex\CL07_Lupa\up_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_curse_bunny\pink022.dds | UNKNOWN | UNKNOWN |  | UNRESOLVED |
| textures\ae_latex_kitty\metal.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL07_Lupa\metal.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_wuthering_waves_lupa\up_n.dds | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | CL07_Lupa | textures\ZLJ\CombatLatex\CL07_Lupa\up_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_curse_bunny\pink022.dds | UNKNOWN | UNKNOWN |  | UNRESOLVED |
| textures\ae_latex_kitty\metal.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL07_Lupa\metal.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_wuthering_waves_lupa\down_n.dds | makaron-COSPLAY - AE_Wuthering_Waves_Lupa — 【服装·装备】【来源·本地】 | CL07_Lupa | textures\ZLJ\CombatLatex\CL07_Lupa\down_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| `... 123 more rows in the CSV` | | | | |


## 6b. Body morph TRI (not a physics config)

_`none`_


## 6c. Model role (ARMA/ARMO slot semantics)

| model_role | canonical_runtime | body_relevance | old_path | new_path | status |
|---|---|---|---|---|---|
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_Feet_1.nif | meshes\ZLJ\CombatLatex\CL07_Lupa\AE_Wuthering_Waves_Lupa_Feet_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | meshes\ZLJ\CombatLatex\CL07_Lupa\AE_Wuthering_Waves_Lupa_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_Hand_1.nif | meshes\ZLJ\CombatLatex\CL07_Lupa\AE_Wuthering_Waves_Lupa_Hand_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_Wuthering_Waves_Lupa\Hair.nif | meshes\ZLJ\CombatLatex\CL07_Lupa\Hair.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_Mant_1.nif | meshes\ZLJ\CombatLatex\CL07_Lupa\AE_Wuthering_Waves_Lupa_Mant_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_Wuthering_Waves_Lupa\HeadACC.nif | meshes\ZLJ\CombatLatex\CL07_Lupa\HeadACC.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | AE_Wuthering_Waves_Lupa\Tail.nif | meshes\ZLJ\CombatLatex\CL07_Lupa\Tail.nif | COPY_AND_REPOINT |


Non-canonical roles kept separate: WEARABLE_MALE_3P=7, WORLD_MALE=7, FIRSTPERSON_MALE=2, FIRSTPERSON_FEMALE=2

## 7. Physics

| config_file | config_type | mesh_references | bone_dependencies | rewrite_required | bone_check_status | status |
|---|---|---|---|---|---|---|
| meshes\ae_wuthering_waves_lupa\coat.xml | HDT_SMP_XML | calientetools\bodyslide\shapedata\ae_wuthering_waves_lupa_mant\ae_wuthering_waves_lupa_mant.nif |  | YES | MISSING_BONE | COPY_AND_REPOINT |


## 8. Existing PBR (provenance only)

No PBR patch mod is registered for this outfit in the P02A registry.

## 9. Cross dependencies (current -> planned)

- cross-outfit texture dependencies: **38** (open after plan: 6)
- external-mod texture dependencies: **18** (open after plan: 18)
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
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL10_HoodST | textures\ae_latex_kitty\d1.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256 775d2ba7ba8716eb is consumed by 3 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL07_Lupa\d1.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL04_Haley | textures\ae_latex_kitty\matcap-latex-e.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_Plug_Vag_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256 f69ab01532109731 is consumed by 3 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL07_Lupa\matcap-latex-e.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty | textures\ae_latex_kitty\metal.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256 a62c83ba93427dd6 is consumed by 2 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL07_Lupa\metal.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty | textures\ae_latex_kitty\metal02.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256 07291e75f588ee6d is consumed by 2 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL07_Lupa\metal02.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL09_Corrupted;CL10_HoodST | textures\ae_latex_kitty\n.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256 a49d6de5ccb12de9 is consumed by 4 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL07_Lupa\n.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL04_Haley | textures\ae_latex_kitty\s.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256 9ccbdf82cc9d1284 is consumed by 3 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL07_Lupa\s.dds | CLOSED_BY_DUPLICATION |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1.dds | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1_msn.dds | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_1_s.dds | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1.dds | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_msn.dds | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_s.dds | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1.dds | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_msn.dds | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_msn.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\actors\character\female\femalebody_etc_v2_1_s.dds | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | KEEP_EXTERNAL_REFERENCE: femalebody_etc_v2_1_s.dds belongs to the GLOBAL_BODY_SKIN and is deliberately NOT copied into the pack namespace. The NIF keeps pointing at the original path. |  | CLOSED_KEEP_EXTERNAL_REFERENCE |
| CROSS_OUTFIT | CL01_LatexKitty | textures\ae_latex_kitty\metal.dds | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: copy metal.dds (owner CL01_LatexKitty) into textures\ZLJ\CombatLatex\CL07_Lupa\metal.dds and repoint meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif / ??_mesh.015_??.004 / Diffuse. Cross-outfit DDS are duplicated per outfit, never shared. | textures\ZLJ\CombatLatex\CL07_Lupa\metal.dds | CLOSED |
| CROSS_OUTFIT | CL01_LatexKitty | textures\ae_latex_kitty\metal.dds | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: copy metal.dds (owner CL01_LatexKitty) into textures\ZLJ\CombatLatex\CL07_Lupa\metal.dds and repoint meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif / ??_mesh.015_??.005 / Diffuse. Cross-outfit DDS are duplicated per outfit, never shared. | textures\ZLJ\CombatLatex\CL07_Lupa\metal.dds | CLOSED |
| UNRESOLVED | UNKNOWN | textures\ae_curse_bunny\latex\d.dds | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | BLOCKED: Global provider lookup executed over all MO2 mod directories plus the game Data folder: no provider at this exact path, no loose game Data file, and the basename occurs in no mod of the instance. Lookup evidence: input reference_class=TRUE_MISSING; probed forms: textures/ae_curse_bunny/latex/d.dds; loose game Data hit: none; complete lookup: no provider at this path and no loose game Data file. Same-basename files DO exist elsewhere (8, e.g. 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 :: interface/exported/widgets/iwantDD/library/Controls/d.dds) but the stem 'd' is non-distinctive, so treating one of them as this asset would be a fuzzy match; they are therefore NOT counted as providers; .bsa-packed contents remain unverified and are a known blind spot; game Data root has no loose 'textures' folder and holds 93 .bsa archives. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | textures\ae_curse_bunny\shkurka_body_mask.dds | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | BLOCKED: Global provider lookup executed over all MO2 mod directories plus the game Data folder: no provider at this exact path, no loose game Data file, and the basename occurs in no mod of the instance. Lookup evidence: input reference_class=TRUE_MISSING; probed forms: textures/ae_curse_bunny/shkurka_body_mask.dds; loose game Data hit: none; complete lookup: no provider at this path, no loose game Data file, and the basename occurs in NO mod dir of this instance; .bsa-packed contents remain unverified and are a known blind spot; game Data root has no loose 'textures' folder and holds 93 .bsa archives. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | textures\ae_curse_bunny\pink022.dds | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | BLOCKED: Global provider lookup executed over all MO2 mod directories plus the game Data folder: no provider at this exact path, no loose game Data file, and the basename occurs in no mod of the instance. Lookup evidence: input reference_class=TRUE_MISSING; probed forms: textures/ae_curse_bunny/pink022.dds; loose game Data hit: none; complete lookup: no provider at this path, no loose game Data file, and the basename occurs in NO mod dir of this instance; .bsa-packed contents remain unverified and are a known blind spot; game Data root has no loose 'textures' folder and holds 93 .bsa archives. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| CROSS_OUTFIT | CL01_LatexKitty | textures\ae_latex_kitty\metal.dds | meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: copy metal.dds (owner CL01_LatexKitty) into textures\ZLJ\CombatLatex\CL07_Lupa\metal.dds and repoint meshes\AE_Wuthering_Waves_Lupa\AE_Wuthering_Waves_Lupa_1.nif / ??_mesh.015_??.014 / Diffuse. Cross-outfit DDS are duplicated per outfit, never shared. | textures\ZLJ\CombatLatex\CL07_Lupa\metal.dds | CLOSED |
| `... 67 more rows in the CSV` | | | | | | |


## 10. Self-containment audit (simulated post-migration)

| gate | result | metric | evidence |
|---|---|---|---|
| GAME_MESH_SELF_CONTAINED | PASS | 21 | game mesh rows=21, target off-namespace=0, collisions=0 |
| TEXTURE_SELF_CONTAINED | REVIEW | 199 | slots(nif=153 shapedata=84) / off-namespace=0 / provider-found=0 / true-missing=38 / path-mismatch-unknown=0 / no-lookup=0 / vanilla=0 / global-body-skin=0 / proposals=32 / open cross-outfit=0 |
| BODYSLIDE_SELF_CONTAINED | PASS | 2 | projects=2 chain-incomplete=0 OSP-off-ns=0 ShapeData-off-ns=0 Output-off-ns=0 UNKNOWN-basis=0 shapedata-tex-off-ns=0 |
| PLUGIN_PATHS_PLANNED | REVIEW | 14 | records=14 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=7 flagged-canonical=7 world-models=7 plugin-DDS-cross-outfit-open=0 / model refs: source-asset-absent=0 foreign-body-decision=5 |
| MODEL_ROLE_SCHEMA | PASS | 25 | role enum violations (legacy WORLD/WEARABLE/GROUND)=0, unknown-enum=0 / distribution: WEARABLE_MALE_3P=7, WEARABLE_FEMALE_3P=7, WORLD_MALE=7, FIRSTPERSON_MALE=2, FIRSTPERSON_FEMALE=2 |
| PHYSICS_PATHS_PLANNED | REVIEW | 1 | physics configs=1 types=HDT_SMP_XML=1 / without-new-path=0 bone-unknown=1 |
| TRI_MORPH_SEPARATION | PASS | 0 | morph rows=0 (.tri sources=0) / TRI rows wrongly present in physics table=0 / physics types=HDT_SMP_XML=1 |
| TARGET_OSP_NAMESPACE | PASS | 1 | distinct target OSP for this outfit=1 expected=1 -> ['calientetools/bodyslide/slidersets/zlj_cl07_lupa.osp'] |
| UNRESOLVED_REFERENCE_PROVENANCE | REVIEW | 3 | distinct unresolved DDS=3, without a global provider-lookup verdict=0, rows whose texture set is not derivable at all (BSA-resident stock mesh, no path to look up)=9 |
| OUTFIT_SELF_CONTAINMENT | REVIEW | 9 | C1..C9 = C1:PASS, C2:REVIEW, C3:PASS, C4:REVIEW, C6:PASS, C5:REVIEW, G7:PASS, C8:PASS, C9:REVIEW |


## 11. BLOCKERS

- `C2` TEXTURE_SELF_CONTAINED = **REVIEW** - slots(nif=153 shapedata=84) | off-namespace=0 | provider-found=0 | true-missing=38 | path-mismatch-unknown=0 | no-lookup=0 | vanilla=0 | global-body-skin=0 | proposals=32 | open cross-outfit=0
- `C4` PLUGIN_PATHS_PLANNED = **REVIEW** - records=14 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=7 flagged-canonical=7 world-models=7 plugin-DDS-cross-outfit-open=0 | model refs: source-asset-absent=0 foreign-body-decision=5
- `C5` PHYSICS_PATHS_PLANNED = **REVIEW** - physics configs=1 types=HDT_SMP_XML=1 | without-new-path=0 bone-unknown=1
- `C9` UNRESOLVED_REFERENCE_PROVENANCE = **REVIEW** - distinct unresolved DDS=3, without a global provider-lookup verdict=0, rows whose texture set is not derivable at all (BSA-resident stock mesh, no path to look up)=9
- `TOTAL` OUTFIT_SELF_CONTAINMENT = **REVIEW** - C1..C9 = C1:PASS, C2:REVIEW, C3:PASS, C4:REVIEW, C6:PASS, C5:REVIEW, G7:PASS, C8:PASS, C9:REVIEW

---

P02A stops here. No COPY / MOVE / DELETE / NIF / ESP / OSP / DDS write was performed and none is authorised until this design is reviewed by a human.
