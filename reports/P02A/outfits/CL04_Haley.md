# CL04_Haley - P02A migration manifest

> Pack: `ZLJ_COMBAT_LATEX` (ZLJ Combat Latex Pack) - canonical body `CBBE_3BA` - target plugin `ZLJ_CombatLatex.esp`
> Phase: **P02A design ledger (STRICT READ-ONLY)** - nothing has been copied, moved, renamed or rewritten.

| field | value |
|---|---|
| Outfit ID (frozen) | `CL04_Haley` |
| Source mod(s) | `makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】`, `Haley Black Suit PBR` |
| Plugin (current) | `SSE_TFD_Haley_Black_Suit.esp` |
| Support mods | `Haley Black Suit PBR` (PBR_PATCH) |
| Target mesh ns | `meshes\ZLJ\CombatLatex\CL04_Haley\` |
| Target texture ns | `textures\ZLJ\CombatLatex\CL04_Haley\` |
| Target ShapeData ns | `CalienteTools\BodySlide\ShapeData\ZLJ_CombatLatex\CL04_Haley\` |
| Target SliderSet | `CalienteTools\BodySlide\SliderSets\ZLJ_CL04_Haley.osp` |

## 1. Source Mods

| MOD_ID | MO2 priority (low = wins) | role | file_count | plugin |
|---|---|---|---|---|
| makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | 921 | BASE | 73 | SSE_TFD_Haley_Black_Suit.esp |
| Haley Black Suit PBR | 884 | PBR_PATCH | 20 |  |


## 2. Winning Providers

| winning_provider | VFS paths won |
|---|---|
| makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | 69 |
|  | 31 |
| Haley Black Suit PBR | 19 |
| makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | 5 |
| AE_VRC_Bunny_Nurse — 【来源·本地】 | 4 |
| 00 资源·H2135 披风物理补全 — H2135 Cloak SMP Physics | 3 |
| [TRX] LatexWhitch — 【来源·本地】 | 2 |
| Nyes Latex Pack AiO 1.3 (ReducedSize) | 1 |


## 3. Plugin Records

Counts by record type: `ARMA`=13, `ARMO`=13, `TXST`=4  
Target plugin: `ZLJ_CombatLatex.esp` - new EDID namespace: `ZLJ_CL_Haley_<PART>` - **no FormID generated in P02A**

| record_type | formid | edid | new_edid | notes |
|---|---|---|---|---|
| ARMA | 01000800 | SSE_TFD_Haley_Black_Suit_Body_AltAA | ZLJ_CL_Haley_BODY_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D62 | SSE_TFD_Haley_Black_Suit_FeetAA | ZLJ_CL_Haley_LOWERLEG_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D63 | SSE_TFD_Haley_Black_Suit_BodyAA | ZLJ_CL_Haley_BODY_AA_2 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D64 | SSE_TFD_Haley_Black_Suit_GloveAA | ZLJ_CL_Haley_HANDS_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D65 | SSE_TFD_Haley_Black_Suit_CapeAA | ZLJ_CL_Haley_PELVIS_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D6A | SSE_TFD_Haley_Black_Suit_MaskAA | ZLJ_CL_Haley_HEAD_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D6B | SSE_TFD_Haley_Black_Suit_StAA | ZLJ_CL_Haley_SHIELD_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D71 | SSE_TFD_Haley_Black_Suit_BodyAA_purple | ZLJ_CL_Haley_BODY_AA_3 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D75 | SSE_TFD_Haley_Black_Suit_FeetAA_purple | ZLJ_CL_Haley_LOWERLEG_AA_2 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D77 | SSE_TFD_Haley_Black_Suit_GloveAA_purple | ZLJ_CL_Haley_HANDS_AA_2 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D78 | SSE_TFD_Haley_Black_Suit_MaskAA_purple | ZLJ_CL_Haley_HEAD_AA_2 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 010012E1 | SSE_TFD_Haley_Black_Suit_CapepAA | ZLJ_CL_Haley_PELVIS_AA_2 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01001DA7 | SSE_TFD_Haley_Black_Suit_Body_Alt_purpleAA | ZLJ_CL_Haley_BODY_AA_4 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMO | 01000801 | SSE_TFD_Haley_Black_SuitAlt | ZLJ_CL_Haley_BODY | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=CBBE_3BA / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 01000D66 | SSE_TFD_Haley_Black_Suit_Feet | ZLJ_CL_Haley_LOWERLEG | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 01000D67 | SSE_TFD_Haley_Black_Suit | ZLJ_CL_Haley_BODY_2 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=EXACT_OUTPUT_PATH / P00_PHYSICS=no |
| ARMO | 01000D68 | SSE_TFD_Haley_Black_Suit_Glove | ZLJ_CL_Haley_HANDS | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=GLOVES / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 01000D69 | SSE_TFD_Haley_Black_Suit_cape | ZLJ_CL_Haley_PELVIS | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=CAPE / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 01000D6C | SSE_TFD_Haley_Black_Suit_Mask | ZLJ_CL_Haley_HEAD | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=MASK / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| ARMO | 01000D6D | SSE_TFD_Haley_Black_Suit_St | ZLJ_CL_Haley_SHIELD | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT / P00_PART_CATEGORY=OTHER / P00_BODY_CANDIDATE=UNKNOWN / P00_BODYSLIDE_MATCH=UNKNOWN / P00_PHYSICS=no |
| `... 6 more rows in the CSV` | | | | |


## 4. Game Mesh

| mesh_role | source_virtual_path | source_provider | target_virtual_path | retain |
|---|---|---|---|---|
| PHYSICS_1 | meshes\Armor\Studded\Male\1stPersonbody_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL04_Haley\male\1p\1stPersonbody_1.nif | REVIEW |
| PHYSICS_1 | meshes\Armor\Studded\Male\1stPersongloves_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL04_Haley\male\1p\1stPersongloves_1.nif | REVIEW |
| PHYSICS_1 | meshes\Armor\Studded\Male\body_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL04_Haley\male\body_1.nif | REVIEW |
| PHYSICS_1 | meshes\Armor\Studded\Male\boots_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL04_Haley\male\boots_1.nif | REVIEW |
| PHYSICS_1 | meshes\Armor\Studded\Male\gloves_1.nif | 男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】 | meshes\ZLJ\CombatLatex\CL04_Haley\male\gloves_1.nif | REVIEW |
| PLAIN_NIF | meshes\SSE_TFD_Haley_Black_Suit\cape.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\cape.nif | KEEP |
| PLAIN_NIF | meshes\SSE_TFD_Haley_Black_Suit\cape.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\world\male\cape.nif | KEEP |
| PLAIN_NIF | meshes\SSE_TFD_Haley_Black_Suit\capePurple.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\capePurple.nif | KEEP |
| PLAIN_NIF | meshes\SSE_TFD_Haley_Black_Suit\capePurple.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\world\female\capePurple.nif | KEEP |
| PLAIN_NIF | meshes\SSE_TFD_Haley_Black_Suit\capePurple.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\world\male\capePurple.nif | KEEP |
| PLAIN_NIF | meshes\SSE_TFD_Haley_Black_Suit\Hair.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\male\Hair.nif | KEEP |
| PLAIN_NIF | meshes\SSE_TFD_Haley_Black_Suit\Mask.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\Mask.nif | KEEP |
| PLAIN_NIF | meshes\SSE_TFD_Haley_Black_Suit\Mask.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\male\Mask.nif | KEEP |
| PLAIN_NIF | meshes\SSE_TFD_Haley_Black_Suit\Mask.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\world\female\Mask.nif | KEEP |
| PLAIN_NIF | meshes\SSE_TFD_Haley_Black_Suit\Mask.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\world\male\Mask.nif | KEEP |
| PHYSICS_1 | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_1.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\1p\SSE_TFD_Haley_Black_Suit_1.nif | KEEP |
| PHYSICS_1 | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_1.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\SSE_TFD_Haley_Black_Suit_1.nif | KEEP |
| PHYSICS_1 | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_1.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\world\female\SSE_TFD_Haley_Black_Suit_1.nif | KEEP |
| PHYSICS_1 | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_1.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\world\male\SSE_TFD_Haley_Black_Suit_1.nif | KEEP |
| PHYSICS_1 | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_Alt_1.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\1p\SSE_TFD_Haley_Black_Suit_Alt_1.nif | KEEP |
| PHYSICS_1 | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_Alt_1.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\SSE_TFD_Haley_Black_Suit_Alt_1.nif | KEEP |
| PHYSICS_1 | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_Alt_1.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\world\male\SSE_TFD_Haley_Black_Suit_Alt_1.nif | KEEP |
| PHYSICS_1 | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_Feet_1.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\SSE_TFD_Haley_Black_Suit_Feet_1.nif | KEEP |
| PHYSICS_1 | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_Feet_1.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\world\female\SSE_TFD_Haley_Black_Suit_Feet_1.nif | KEEP |
| PHYSICS_1 | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_Feet_1.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\world\male\SSE_TFD_Haley_Black_Suit_Feet_1.nif | KEEP |
| PHYSICS_1 | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_Glove_1.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\1p\SSE_TFD_Haley_Black_Suit_Glove_1.nif | KEEP |
| PHYSICS_1 | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_Glove_1.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\SSE_TFD_Haley_Black_Suit_Glove_1.nif | KEEP |
| PHYSICS_1 | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_Glove_1.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\world\female\SSE_TFD_Haley_Black_Suit_Glove_1.nif | KEEP |
| PHYSICS_1 | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_Glove_1.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\world\male\SSE_TFD_Haley_Black_Suit_Glove_1.nif | KEEP |
| PHYSICS_1 | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_St_1.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\SSE_TFD_Haley_Black_Suit_St_1.nif | KEEP |
| PHYSICS_1 | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_St_1.nif | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | meshes\ZLJ\CombatLatex\CL04_Haley\world\male\SSE_TFD_Haley_Black_Suit_St_1.nif | KEEP |


## 5. ShapeData / OSP / OSD

| old_ui_name | new_ui_name | old_osp | new_osp | new_shape_data | new_input_nif | new_osd | new_output_path | new_output_file | basis |
|---|---|---|---|---|---|---|---|---|---|
| SSE_TFD_Haley_Black_Suit | [ZLJ Combat Latex] Haley - Bodysuit | CalienteTools\BodySlide\SliderSets\SSE_TFD_Haley_Black_Suit.osp | CalienteTools\BodySlide\SliderSets\ZLJ_CL04_Haley.osp | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL04_Haley\SSE_TFD_Haley_Black_Suit\ | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL04_Haley\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit.nif | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL04_Haley\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit.osd | meshes\ZLJ\CombatLatex\CL04_Haley\ | Bodysuit | EXACT_OUTPUT_PATH |


## 6. DDS actually in use

Distinct source DDS in the closure: **50**

| source_virtual_path | winning_provider | owning_outfit_of_source | target_virtual_path | action |
|---|---|---|---|---|
| UNKNOWN | UNKNOWN | UNKNOWN |  | UNRESOLVED |
| UNKNOWN | UNKNOWN | UNKNOWN |  | UNRESOLVED |
| UNKNOWN | UNKNOWN | UNKNOWN |  | UNRESOLVED |
| UNKNOWN | UNKNOWN | UNKNOWN |  | UNRESOLVED |
| UNKNOWN | UNKNOWN | UNKNOWN |  | UNRESOLVED |
| textures\devious\devices\catsuitLatexBlack_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatexBlack_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_n.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatex_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_latex_kitty\ComplexBase_M.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL04_Haley\ComplexBase_M.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_latex_kitty\Dynamic_Cubemap_NULL.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL04_Haley\Dynamic_Cubemap_NULL.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\SSE_TFD_Haley_Black_Suit\catsuitLatexPurple_d.dds | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | CL04_Haley | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatexPurple_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_n.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatex_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_latex_kitty\s.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL04_Haley\s.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_latex_kitty\matcap-latex-e.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL04_Haley\matcap-latex-e.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\harry2135\fantasyseries6\fs6_hooded_cloak_ro_m.dds | UNKNOWN | UNKNOWN |  | UNRESOLVED |
| textures\harry2135\fantasyseries6\cubemaps\basilica.dds | UNKNOWN | UNKNOWN |  | UNRESOLVED |
| textures\sse_tfd_haley_black_suit\metal.dds | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | CL04_Haley | textures\ZLJ\CombatLatex\CL04_Haley\metal.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\sse_tfd_haley_black_suit\pc_016_a_cmn_002_head_n.dds | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | CL04_Haley | textures\ZLJ\CombatLatex\CL04_Haley\pc_016_a_cmn_002_head_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\sse_tfd_haley_black_suit\pc_016_a_cmn_002_head_p.dds | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | CL04_Haley | textures\ZLJ\CombatLatex\CL04_Haley\pc_016_a_cmn_002_head_p.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\sse_tfd_haley_black_suit\sample_pbr_e3.dds | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | CL04_Haley | textures\ZLJ\CombatLatex\CL04_Haley\sample_pbr_e3.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatexBlack_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatexBlack_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\sse_tfd_haley_black_suit\pc_016_a_cmn_002_head_n.dds | makaron-COSPLAY - AE_TFD_Haley_Black_Suit — 【服装·装备】【来源·本地】 | CL04_Haley | textures\ZLJ\CombatLatex\CL04_Haley\pc_016_a_cmn_002_head_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_latex_kitty\ComplexBase_M.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL04_Haley\ComplexBase_M.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_latex_kitty\Dynamic_Cubemap_NULL.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL04_Haley\Dynamic_Cubemap_NULL.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatexBlack_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatexBlack_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_n.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatex_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_latex_kitty\ComplexBase_M.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL04_Haley\ComplexBase_M.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_latex_kitty\Dynamic_Cubemap_NULL.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL04_Haley\Dynamic_Cubemap_NULL.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatexBlack_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatexBlack_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_n.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatex_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\ae_latex_kitty\ComplexBase_M.dds | makaron-COSPLAY - AE_Latex_Kitty — 【服装·装备】【来源·本地】 | CL01_LatexKitty | textures\ZLJ\CombatLatex\CL04_Haley\ComplexBase_M.dds | COPY_INTO_OUTFIT_NAMESPACE |
| `... 274 more rows in the CSV` | | | | |


## 6b. Body morph TRI (not a physics config)

_`none`_


## 6c. Model role (ARMA/ARMO slot semantics)

| model_role | canonical_runtime | body_relevance | old_path | new_path | status |
|---|---|---|---|---|---|
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_Alt_1.nif | meshes\ZLJ\CombatLatex\CL04_Haley\SSE_TFD_Haley_Black_Suit_Alt_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_Feet_1.nif | meshes\ZLJ\CombatLatex\CL04_Haley\SSE_TFD_Haley_Black_Suit_Feet_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_1.nif | meshes\ZLJ\CombatLatex\CL04_Haley\SSE_TFD_Haley_Black_Suit_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_Glove_1.nif | meshes\ZLJ\CombatLatex\CL04_Haley\SSE_TFD_Haley_Black_Suit_Glove_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | SSE_TFD_Haley_Black_Suit\cape.nif | meshes\ZLJ\CombatLatex\CL04_Haley\cape.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | SSE_TFD_Haley_Black_Suit\Mask.nif | meshes\ZLJ\CombatLatex\CL04_Haley\Mask.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_St_1.nif | meshes\ZLJ\CombatLatex\CL04_Haley\SSE_TFD_Haley_Black_Suit_St_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_1.nif | meshes\ZLJ\CombatLatex\CL04_Haley\SSE_TFD_Haley_Black_Suit_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_Feet_1.nif | meshes\ZLJ\CombatLatex\CL04_Haley\SSE_TFD_Haley_Black_Suit_Feet_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_Glove_1.nif | meshes\ZLJ\CombatLatex\CL04_Haley\SSE_TFD_Haley_Black_Suit_Glove_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | SSE_TFD_Haley_Black_Suit\Mask.nif | meshes\ZLJ\CombatLatex\CL04_Haley\Mask.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | SSE_TFD_Haley_Black_Suit\capePurple.nif | meshes\ZLJ\CombatLatex\CL04_Haley\capePurple.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_Alt_1.nif | meshes\ZLJ\CombatLatex\CL04_Haley\SSE_TFD_Haley_Black_Suit_Alt_1.nif | COPY_AND_REPOINT |


Non-canonical roles kept separate: WEARABLE_MALE_3P=13, WORLD_MALE=13, FIRSTPERSON_MALE=6, FIRSTPERSON_FEMALE=6, WORLD_FEMALE=5

## 7. Physics

| config_file | config_type | mesh_references | bone_dependencies | rewrite_required | bone_check_status | status |
|---|---|---|---|---|---|---|
| meshes\harry2135\fantasyseries6\smpxml\fs6_hoodedcloak_3ba_smp.xml | HDT_SMP_XML | meshes\sse_tfd_haley_black_suit\cape.nif |  | YES | MISSING_BONE | COPY_AND_REPOINT_EXTERNAL_WINNER |
| meshes\harry2135\fantasyseries6\smpxml\fs6_hoodedcloak_folded_3ba_smp.xml | HDT_SMP_XML | meshes\sse_tfd_haley_black_suit\cape.nif |  | YES | MISSING_BONE | COPY_AND_REPOINT_EXTERNAL_WINNER |
| meshes\harry2135\fantasyseries6\smpxml\fs6_hoodedcloak_hair_3ba_smp.xml | HDT_SMP_XML | UNKNOWN |  | UNKNOWN | UNKNOWN | UNRESOLVED_NO_MESH_BINDING |


## 8. Existing PBR (provenance only)

PBR patch mod: `Haley Black Suit PBR` - recorded as **provenance only**, not adopted as final standard (P05/P06 redesign the material standard).

| virtual_path | winning_provider |
|---|---|
| meta.ini | Haley Black Suit PBR |
| pbrnifpatcher/sse_tfd_haley_black_suit/pc_016_a_cmn_002_head_c.json | Haley Black Suit PBR |
| pbrnifpatcher/sse_tfd_haley_black_suit/pc_016_a_cmn_002_parta_c.json | Haley Black Suit PBR |
| pbrnifpatcher/sse_tfd_haley_black_suit/pc_016_a_cmn_002_partb_c.json | Haley Black Suit PBR |
| pbrnifpatcher/sse_tfd_haley_black_suit/pc_016_a_cmn_002_stockings_c.json | Haley Black Suit PBR |
| textures/pbr/sse_tfd_haley_black_suit/pc_016_a_cmn_002_head.dds | Haley Black Suit PBR |
| textures/pbr/sse_tfd_haley_black_suit/pc_016_a_cmn_002_head_g.dds | Haley Black Suit PBR |
| textures/pbr/sse_tfd_haley_black_suit/pc_016_a_cmn_002_head_n.dds | Haley Black Suit PBR |
| textures/pbr/sse_tfd_haley_black_suit/pc_016_a_cmn_002_head_rmaos.dds | Haley Black Suit PBR |
| textures/pbr/sse_tfd_haley_black_suit/pc_016_a_cmn_002_parta.dds | Haley Black Suit PBR |
| textures/pbr/sse_tfd_haley_black_suit/pc_016_a_cmn_002_parta_g.dds | Haley Black Suit PBR |
| textures/pbr/sse_tfd_haley_black_suit/pc_016_a_cmn_002_parta_n.dds | Haley Black Suit PBR |
| textures/pbr/sse_tfd_haley_black_suit/pc_016_a_cmn_002_parta_rmaos.dds | Haley Black Suit PBR |
| textures/pbr/sse_tfd_haley_black_suit/pc_016_a_cmn_002_partb.dds | Haley Black Suit PBR |
| textures/pbr/sse_tfd_haley_black_suit/pc_016_a_cmn_002_partb_g.dds | Haley Black Suit PBR |
| textures/pbr/sse_tfd_haley_black_suit/pc_016_a_cmn_002_partb_n.dds | Haley Black Suit PBR |
| textures/pbr/sse_tfd_haley_black_suit/pc_016_a_cmn_002_partb_rmaos.dds | Haley Black Suit PBR |
| textures/pbr/sse_tfd_haley_black_suit/pc_016_a_cmn_002_stockings.dds | Haley Black Suit PBR |
| textures/pbr/sse_tfd_haley_black_suit/pc_016_a_cmn_002_stockings_n.dds | Haley Black Suit PBR |
| textures/pbr/sse_tfd_haley_black_suit/pc_016_a_cmn_002_stockings_rmaos.dds | Haley Black Suit PBR |


## 9. Cross dependencies (current -> planned)

- cross-outfit texture dependencies: **82** (open after plan: 7)
- external-mod texture dependencies: **141** (open after plan: 12)
- audit counters: cross-outfit open **0** / external-mod-missing **0** / hard-unresolved **5** / vanilla-allowed **0** / shared proposals **0**
- unresolvable DDS by class (distinct files): none - a DDS absent from the frozen P00 VFS is already broken at runtime today; it is listed, never guessed

| dependency_type | source_owner | source_virtual_path | referenced_by_nif | resolution_plan | target_virtual_path | post_plan_state |
|---|---|---|---|---|---|---|
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\1stPersonbody_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\1stPersongloves_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\body_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\boots_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\gloves_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL07_Lupa | textures\ae_latex_kitty\matcap-latex-e.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_Plug_Vag_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256 f69ab01532109731 is consumed by 3 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL04_Haley\matcap-latex-e.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL07_Lupa | textures\ae_latex_kitty\s.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256 9ccbdf82cc9d1284 is consumed by 3 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL04_Haley\s.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL02_OnceMedic;CL08_SpearHead;CL11_SkimpyAssassin | textures\devious\devices\catsuitLatex_em.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_Feet_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 5 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatex_em.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL02_OnceMedic;CL03_Tachy;CL05_Valby;CL08_SpearHead;CL11_SkimpyAssassin | textures\devious\devices\catsuitLatex_n.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_Glove_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 6 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatex_n.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL02_OnceMedic;CL08_SpearHead;CL11_SkimpyAssassin | textures\devious\devices\catsuitLatexBlack_d.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_Feet_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 5 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatexBlack_d.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL05_Valby | Textures\devious\devices\YokeFront_d.dds | meshes\SSE_TFD_Haley_Black_Suit\SSE_TFD_Haley_Black_Suit_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 2 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL04_Haley\YokeFront_d.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL02_OnceMedic;CL08_SpearHead;CL11_SkimpyAssassin | textures\devious\expansion\zad_Ebonite_e.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_Feet_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 5 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL04_Haley\zad_Ebonite_e.dds | CLOSED_BY_DUPLICATION |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\1stPersonbody_1.nif | BLOCKED: Texture set of this mesh is not derivable from the frozen P00 evidence: the NIF is not in the P00 NIF index (existence=RESOLVED_BY_TARGETED_PROBE). The frozen evidence indexes loose mod files only, so the mesh is either BSA-resident or belongs to a provider outside the P00 scope. READ-ONLY prohibits writing, not reading: P02B is allowed to parse the binary to resolve it.. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\1stPersongloves_1.nif | BLOCKED: Texture set of this mesh is not derivable from the frozen P00 evidence: the NIF is not in the P00 NIF index (existence=RESOLVED_BY_TARGETED_PROBE). The frozen evidence indexes loose mod files only, so the mesh is either BSA-resident or belongs to a provider outside the P00 scope. READ-ONLY prohibits writing, not reading: P02B is allowed to parse the binary to resolve it.. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\body_1.nif | BLOCKED: Texture set of this mesh is not derivable from the frozen P00 evidence: the NIF is not in the P00 NIF index (existence=RESOLVED_BY_TARGETED_PROBE). The frozen evidence indexes loose mod files only, so the mesh is either BSA-resident or belongs to a provider outside the P00 scope. READ-ONLY prohibits writing, not reading: P02B is allowed to parse the binary to resolve it.. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\boots_1.nif | BLOCKED: Texture set of this mesh is not derivable from the frozen P00 evidence: the NIF is not in the P00 NIF index (existence=RESOLVED_BY_TARGETED_PROBE). The frozen evidence indexes loose mod files only, so the mesh is either BSA-resident or belongs to a provider outside the P00 scope. READ-ONLY prohibits writing, not reading: P02B is allowed to parse the binary to resolve it.. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\Armor\Studded\Male\gloves_1.nif | BLOCKED: Texture set of this mesh is not derivable from the frozen P00 evidence: the NIF is not in the P00 NIF index (existence=RESOLVED_BY_TARGETED_PROBE). The frozen evidence indexes loose mod files only, so the mesh is either BSA-resident or belongs to a provider outside the P00 scope. READ-ONLY prohibits writing, not reading: P02B is allowed to parse the binary to resolve it.. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatexBlack_d.dds | meshes\SSE_TFD_Haley_Black_Suit\cape.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatexBlack_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatexBlack_d.dds and repoint meshes\SSE_TFD_Haley_Black_Suit\cape.nif / FS6_Hooded_Cloak / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatexBlack_d.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatex_n.dds | meshes\SSE_TFD_Haley_Black_Suit\cape.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatex_n.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatex_n.dds and repoint meshes\SSE_TFD_Haley_Black_Suit\cape.nif / FS6_Hooded_Cloak / Normal so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatex_n.dds | CLOSED |
| CROSS_OUTFIT | CL01_LatexKitty | textures\ae_latex_kitty\ComplexBase_M.dds | meshes\SSE_TFD_Haley_Black_Suit\cape.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: copy ComplexBase_M.dds (owner CL01_LatexKitty) into textures\ZLJ\CombatLatex\CL04_Haley\ComplexBase_M.dds and repoint meshes\SSE_TFD_Haley_Black_Suit\cape.nif / FS6_Hooded_Cloak / EnvMask. Cross-outfit DDS are duplicated per outfit, never shared. | textures\ZLJ\CombatLatex\CL04_Haley\ComplexBase_M.dds | CLOSED |
| CROSS_OUTFIT | CL01_LatexKitty | textures\ae_latex_kitty\Dynamic_Cubemap_NULL.dds | meshes\SSE_TFD_Haley_Black_Suit\cape.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: copy Dynamic_Cubemap_NULL.dds (owner CL01_LatexKitty) into textures\ZLJ\CombatLatex\CL04_Haley\Dynamic_Cubemap_NULL.dds and repoint meshes\SSE_TFD_Haley_Black_Suit\cape.nif / FS6_Hooded_Cloak / EnvMap. Cross-outfit DDS are duplicated per outfit, never shared. | textures\ZLJ\CombatLatex\CL04_Haley\Dynamic_Cubemap_NULL.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatex_n.dds | meshes\SSE_TFD_Haley_Black_Suit\capePurple.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatex_n.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatex_n.dds and repoint meshes\SSE_TFD_Haley_Black_Suit\capePurple.nif / FS6_Hooded_Cloak / Normal so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatex_n.dds | CLOSED |
| CROSS_OUTFIT | CL01_LatexKitty | textures\ae_latex_kitty\s.dds | meshes\SSE_TFD_Haley_Black_Suit\capePurple.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: copy s.dds (owner CL01_LatexKitty) into textures\ZLJ\CombatLatex\CL04_Haley\s.dds and repoint meshes\SSE_TFD_Haley_Black_Suit\capePurple.nif / FS6_Hooded_Cloak / EnvMask. Cross-outfit DDS are duplicated per outfit, never shared. | textures\ZLJ\CombatLatex\CL04_Haley\s.dds | CLOSED |
| CROSS_OUTFIT | CL01_LatexKitty | textures\ae_latex_kitty\matcap-latex-e.dds | meshes\SSE_TFD_Haley_Black_Suit\capePurple.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: copy matcap-latex-e.dds (owner CL01_LatexKitty) into textures\ZLJ\CombatLatex\CL04_Haley\matcap-latex-e.dds and repoint meshes\SSE_TFD_Haley_Black_Suit\capePurple.nif / FS6_Hooded_Cloak / EnvMap. Cross-outfit DDS are duplicated per outfit, never shared. | textures\ZLJ\CombatLatex\CL04_Haley\matcap-latex-e.dds | CLOSED |
| UNRESOLVED | UNKNOWN | textures\harry2135\fantasyseries6\fs6_hooded_cloak_ro_m.dds | meshes\SSE_TFD_Haley_Black_Suit\Hair.nif | BLOCKED: Global provider lookup executed over all MO2 mod directories plus the game Data folder: no provider at this exact path, no loose game Data file, and the basename occurs in no mod of the instance. Lookup evidence: input reference_class=TRUE_MISSING; probed forms: textures/harry2135/fantasyseries6/fs6_hooded_cloak_ro_m.dds; loose game Data hit: none; complete lookup: no provider at this path, no loose game Data file, and the basename occurs in NO mod dir of this instance; .bsa-packed contents remain unverified and are a known blind spot; game Data root has no loose 'textures' folder and holds 93 .bsa archives. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | textures\harry2135\fantasyseries6\cubemaps\basilica.dds | meshes\SSE_TFD_Haley_Black_Suit\Hair.nif | BLOCKED: Global provider lookup executed over all MO2 mod directories plus the game Data folder: no provider at this exact path, no loose game Data file, and the basename occurs in no mod of the instance. Lookup evidence: input reference_class=TRUE_MISSING; probed forms: textures/harry2135/fantasyseries6/cubemaps/basilica.dds; loose game Data hit: none; complete lookup: no provider at this path, no loose game Data file, and the basename occurs in NO mod dir of this instance; .bsa-packed contents remain unverified and are a known blind spot; game Data root has no loose 'textures' folder and holds 93 .bsa archives. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatexBlack_d.dds | meshes\SSE_TFD_Haley_Black_Suit\Mask.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatexBlack_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatexBlack_d.dds and repoint meshes\SSE_TFD_Haley_Black_Suit\Mask.nif / 06 / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatexBlack_d.dds | CLOSED |
| CROSS_OUTFIT | CL01_LatexKitty | textures\ae_latex_kitty\ComplexBase_M.dds | meshes\SSE_TFD_Haley_Black_Suit\Mask.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: copy ComplexBase_M.dds (owner CL01_LatexKitty) into textures\ZLJ\CombatLatex\CL04_Haley\ComplexBase_M.dds and repoint meshes\SSE_TFD_Haley_Black_Suit\Mask.nif / 06 / EnvMask. Cross-outfit DDS are duplicated per outfit, never shared. | textures\ZLJ\CombatLatex\CL04_Haley\ComplexBase_M.dds | CLOSED |
| CROSS_OUTFIT | CL01_LatexKitty | textures\ae_latex_kitty\Dynamic_Cubemap_NULL.dds | meshes\SSE_TFD_Haley_Black_Suit\Mask.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: copy Dynamic_Cubemap_NULL.dds (owner CL01_LatexKitty) into textures\ZLJ\CombatLatex\CL04_Haley\Dynamic_Cubemap_NULL.dds and repoint meshes\SSE_TFD_Haley_Black_Suit\Mask.nif / 06 / EnvMap. Cross-outfit DDS are duplicated per outfit, never shared. | textures\ZLJ\CombatLatex\CL04_Haley\Dynamic_Cubemap_NULL.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatexBlack_d.dds | meshes\SSE_TFD_Haley_Black_Suit\Mask.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatexBlack_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatexBlack_d.dds and repoint meshes\SSE_TFD_Haley_Black_Suit\Mask.nif / OldLHood:1 / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL04_Haley\catsuitLatexBlack_d.dds | CLOSED |
| `... 209 more rows in the CSV` | | | | | | |


## 10. Self-containment audit (simulated post-migration)

| gate | result | metric | evidence |
|---|---|---|---|
| GAME_MESH_SELF_CONTAINED | PASS | 31 | game mesh rows=31, target off-namespace=0, collisions=0 |
| TEXTURE_SELF_CONTAINED | REVIEW | 493 | slots(nif=304 shapedata=197) / off-namespace=0 / provider-found=0 / true-missing=3 / path-mismatch-unknown=5 / no-lookup=0 / vanilla=0 / global-body-skin=0 / proposals=140 / open cross-outfit=0 |
| BODYSLIDE_SELF_CONTAINED | PASS | 1 | projects=1 chain-incomplete=0 OSP-off-ns=0 ShapeData-off-ns=0 Output-off-ns=0 UNKNOWN-basis=0 shapedata-tex-off-ns=0 |
| PLUGIN_PATHS_PLANNED | REVIEW | 30 | records=30 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=13 flagged-canonical=13 world-models=18 plugin-DDS-cross-outfit-open=0 / model refs: source-asset-absent=0 foreign-body-decision=15 |
| MODEL_ROLE_SCHEMA | PASS | 56 | role enum violations (legacy WORLD/WEARABLE/GROUND)=0, unknown-enum=0 / distribution: WEARABLE_MALE_3P=13, WEARABLE_FEMALE_3P=13, WORLD_MALE=13, FIRSTPERSON_MALE=6, FIRSTPERSON_FEMALE=6, WORLD_FEMALE=5 |
| PHYSICS_PATHS_PLANNED | REVIEW | 3 | physics configs=3 types=HDT_SMP_XML=3 / without-new-path=0 bone-unknown=3 |
| TRI_MORPH_SEPARATION | PASS | 0 | morph rows=0 (.tri sources=0) / TRI rows wrongly present in physics table=0 / physics types=HDT_SMP_XML=3 |
| TARGET_OSP_NAMESPACE | PASS | 1 | distinct target OSP for this outfit=1 expected=1 -> ['calientetools/bodyslide/slidersets/zlj_cl04_haley.osp'] |
| UNRESOLVED_REFERENCE_PROVENANCE | REVIEW | 4 | distinct unresolved DDS=4, without a global provider-lookup verdict=0, rows whose texture set is not derivable at all (BSA-resident stock mesh, no path to look up)=5 |
| OUTFIT_SELF_CONTAINMENT | REVIEW | 9 | C1..C9 = C1:PASS, C2:REVIEW, C3:PASS, C4:REVIEW, C6:PASS, C5:REVIEW, G7:PASS, C8:PASS, C9:REVIEW |


## 11. BLOCKERS

- `C2` TEXTURE_SELF_CONTAINED = **REVIEW** - slots(nif=304 shapedata=197) | off-namespace=0 | provider-found=0 | true-missing=3 | path-mismatch-unknown=5 | no-lookup=0 | vanilla=0 | global-body-skin=0 | proposals=140 | open cross-outfit=0
- `C4` PLUGIN_PATHS_PLANNED = **REVIEW** - records=30 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=13 flagged-canonical=13 world-models=18 plugin-DDS-cross-outfit-open=0 | model refs: source-asset-absent=0 foreign-body-decision=15
- `C5` PHYSICS_PATHS_PLANNED = **REVIEW** - physics configs=3 types=HDT_SMP_XML=3 | without-new-path=0 bone-unknown=3
- `C9` UNRESOLVED_REFERENCE_PROVENANCE = **REVIEW** - distinct unresolved DDS=4, without a global provider-lookup verdict=0, rows whose texture set is not derivable at all (BSA-resident stock mesh, no path to look up)=5
- `TOTAL` OUTFIT_SELF_CONTAINMENT = **REVIEW** - C1..C9 = C1:PASS, C2:REVIEW, C3:PASS, C4:REVIEW, C6:PASS, C5:REVIEW, G7:PASS, C8:PASS, C9:REVIEW

---

P02A stops here. No COPY / MOVE / DELETE / NIF / ESP / OSP / DDS write was performed and none is authorised until this design is reviewed by a human.
