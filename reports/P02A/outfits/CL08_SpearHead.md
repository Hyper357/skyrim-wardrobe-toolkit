# CL08_SpearHead - P02A migration manifest

> Pack: `ZLJ_COMBAT_LATEX` (ZLJ Combat Latex Pack) - canonical body `CBBE_3BA` - target plugin `ZLJ_CombatLatex.esp`
> Phase: **P02A design ledger (STRICT READ-ONLY)** - nothing has been copied, moved, renamed or rewritten.

| field | value |
|---|---|
| Outfit ID (frozen) | `CL08_SpearHead` |
| Source mod(s) | `矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】` |
| Plugin (current) | `BBD_CatsuitSpearhead.esp` |
| Support mods | NONE |
| Target mesh ns | `meshes\ZLJ\CombatLatex\CL08_SpearHead\` |
| Target texture ns | `textures\ZLJ\CombatLatex\CL08_SpearHead\` |
| Target ShapeData ns | `CalienteTools\BodySlide\ShapeData\ZLJ_CombatLatex\CL08_SpearHead\` |
| Target SliderSet | `CalienteTools\BodySlide\SliderSets\ZLJ_CL08_SpearHead.osp` |

## 1. Source Mods

| MOD_ID | MO2 priority (low = wins) | role | file_count | plugin |
|---|---|---|---|---|
| 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | 909 | BASE | 65 | BBD_CatsuitSpearhead.esp |


## 2. Winning Providers

| winning_provider | VFS paths won |
|---|---|
| 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | 64 |
|  | 40 |
| [Predator] Latex Acessories 3BA SE — 【服装·装备】【体型·CBBE+3BA】【来源·本地】【系列·Predator】 | 5 |
| Nyes Latex Pack AiO 1.3 (ReducedSize) | 1 |
| [Predator] Gynax Suit + Colors XXX BHUNP SE — 【体型·BHUNP】【来源·本地】【系列·Predator】 | 1 |


## 3. Plugin Records

Counts by record type: `ARMA`=24, `ARMO`=24  
Target plugin: `ZLJ_CombatLatex.esp` - new EDID namespace: `ZLJ_CL_SpearHead_<PART>` - **no FormID generated in P02A**

| record_type | formid | edid | new_edid | notes |
|---|---|---|---|---|
| ARMA | 01000800 | BBDCatsuita01t02AA | ZLJ_CL_SpearHead_BODY_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000806 | BBDCatsuitg01t01AA | ZLJ_CL_SpearHead_CHEST_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000808 | BBDCatsuitg01t02AA | ZLJ_CL_SpearHead_HANDS_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 0100080A | BBDCatsuitg02t01AA | ZLJ_CL_SpearHead_BBDCATSUITG02T01_AA | PART_TOKEN_SOURCE=P00_SLOT_BIT23_UNNAMED_EDID_TOKEN |
| ARMA | 0100080E | BBDCatsuitg02t02AA | ZLJ_CL_SpearHead_BBDCATSUITG02T02_AA | PART_TOKEN_SOURCE=P00_SLOT_BIT23_UNNAMED_EDID_TOKEN |
| ARMA | 01000817 | BBDCatsuith01t01AA | ZLJ_CL_SpearHead_FRONT_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000818 | BBDCatsuith01t02AA | ZLJ_CL_SpearHead_FRONT_AA_2 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 0100081A | BBDCatsuith02t01AA | ZLJ_CL_SpearHead_FRONT_AA_3 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 0100081C | BBDCatsuith02t02AA | ZLJ_CL_SpearHead_FRONT_AA_4 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 0100081E | BBDCatsuith03t01AA | ZLJ_CL_SpearHead_FRONT_AA_5 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000820 | BBDCatsuith03t02AA | ZLJ_CL_SpearHead_FRONT_AA_6 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000823 | BBDCatsuitl01t01AA | ZLJ_CL_SpearHead_LOWERLEG_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000824 | BBDCatsuitl01t02AA | ZLJ_CL_SpearHead_LOWERLEG_AA_2 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000859 | BBDCatsuita01t01SAA | ZLJ_CL_SpearHead_BODY_AA_2 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 0100085A | BBDCatsuita01t02SAA | ZLJ_CL_SpearHead_BODY_AA_3 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000D63 | BBDCatsuita01t01AA | ZLJ_CL_SpearHead_BODY_AA_4 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000DC3 | BBDCatsuitl01t03AA | ZLJ_CL_SpearHead_LOWERLEG_AA_3 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000DC5 | BBDCatsuith01t02TAA | ZLJ_CL_SpearHead_RIGHTWEAPON_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000DC7 | BBDCatsuith01t03TAA | ZLJ_CL_SpearHead_RIGHTWEAPON_AA_2 | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| ARMA | 01000DC9 | BBDCatsuith01t04TAA | ZLJ_CL_SpearHead_HAIR_AA | PART_TOKEN_SOURCE=P00_PARTS_ARMA_BOD2_SLOT |
| `... 28 more rows in the CSV` | | | | |


## 4. Game Mesh

| mesh_role | source_virtual_path | source_provider | target_virtual_path | retain |
|---|---|---|---|---|
| PLAIN_NIF | meshes\bbdrac\(Nye) Latex Corset - red.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\1p\(Nye) Latex Corset - red.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\(Nye) Latex Corset - red.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\(Nye) Latex Corset - red.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\(Nye) Latex Corset - red.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\world\male\(Nye) Latex Corset - red.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\(Nye) Latex Corset.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\1p\(Nye) Latex Corset.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\(Nye) Latex Corset.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\(Nye) Latex Corset.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\(Nye) Latex Corset.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\world\male\(Nye) Latex Corset.nif | KEEP |
| PHYSICS_1 | meshes\bbdrac\Catsuita01t01_1.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\1p\Catsuita01t01_1.nif | KEEP |
| PHYSICS_1 | meshes\bbdrac\Catsuita01t01_1.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuita01t01_1.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuita01t01GND.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\world\female\Catsuita01t01GND.nif | KEEP |
| PHYSICS_1 | meshes\bbdrac\Catsuita01t01S_1.nif | 输出·BodySlide Output | meshes\ZLJ\CombatLatex\CL08_SpearHead\1p\Catsuita01t01S_1.nif | KEEP |
| PHYSICS_1 | meshes\bbdrac\Catsuita01t01S_1.nif | 输出·BodySlide Output | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuita01t01S_1.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuita01t01SGND.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\world\female\Catsuita01t01SGND.nif | KEEP |
| PHYSICS_1 | meshes\bbdrac\Catsuitg01t01_1.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\1p\Catsuitg01t01_1.nif | KEEP |
| PHYSICS_1 | meshes\bbdrac\Catsuitg01t01_1.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuitg01t01_1.nif | KEEP |
| PHYSICS_1 | meshes\bbdrac\Catsuitg01t01_1.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\world\male\Catsuitg01t01_1.nif | KEEP |
| PHYSICS_1 | meshes\bbdrac\Catsuitg01t02_1.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\1p\Catsuitg01t02_1.nif | KEEP |
| PHYSICS_1 | meshes\bbdrac\Catsuitg01t02_1.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuitg01t02_1.nif | KEEP |
| PHYSICS_1 | meshes\bbdrac\Catsuitg01t02_1.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\world\male\Catsuitg01t02_1.nif | KEEP |
| PHYSICS_1 | meshes\bbdrac\Catsuitg02t01_1.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\1p\Catsuitg02t01_1.nif | KEEP |
| PHYSICS_1 | meshes\bbdrac\Catsuitg02t01_1.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuitg02t01_1.nif | KEEP |
| PHYSICS_1 | meshes\bbdrac\Catsuitg02t01_1.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\world\male\Catsuitg02t01_1.nif | KEEP |
| PHYSICS_1 | meshes\bbdrac\Catsuitg02t02_1.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\1p\Catsuitg02t02_1.nif | KEEP |
| PHYSICS_1 | meshes\bbdrac\Catsuitg02t02_1.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuitg02t02_1.nif | KEEP |
| PHYSICS_1 | meshes\bbdrac\Catsuitg02t02_1.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\world\male\Catsuitg02t02_1.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuith01t01.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\1p\Catsuith01t01.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuith01t01.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuith01t01.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuith01t01GND.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\world\female\Catsuith01t01GND.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuith01t02.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\1p\Catsuith01t02.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuith01t02.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuith01t02.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuith01t02GND.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\world\female\Catsuith01t02GND.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuith02t01.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\1p\Catsuith02t01.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuith02t01.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuith02t01.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuith02t01GND.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\world\female\Catsuith02t01GND.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuith02t02.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\1p\Catsuith02t02.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuith02t02.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuith02t02.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuith02t02GND.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\world\female\Catsuith02t02GND.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuith03t01.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\1p\Catsuith03t01.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuith03t01.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuith03t01.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\Catsuith03t01GND.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\world\female\Catsuith03t01GND.nif | KEEP |
| PLAIN_NIF | meshes\bbdrac\catsuith03t02 - red.nif | 矛头紧身衣 — SpearHead Catsuit CBBE 3BA BS — 【体型·CBBE+3BA】【来源·本地】 | meshes\ZLJ\CombatLatex\CL08_SpearHead\1p\catsuith03t02 - red.nif | KEEP |
| `... 25 more rows in the CSV` | | | | |


## 5. ShapeData / OSP / OSD

| old_ui_name | new_ui_name | old_osp | new_osp | new_shape_data | new_input_nif | new_osd | new_output_path | new_output_file | basis |
|---|---|---|---|---|---|---|---|---|---|
| Spearhead Catsuit Armor 3BA | [ZLJ Combat Latex] SpearHead - Spearhead Catsuit Armor 3BA | CalienteTools\bodyslide\SliderSets\Spearhead Catsuit 3BA.osp | CalienteTools\BodySlide\SliderSets\ZLJ_CL08_SpearHead.osp | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL08_SpearHead\Spearhead Catsuit 3BA\ | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL08_SpearHead\Spearhead Catsuit 3BA\Spearhead Catsuit Armor 3BA.nif | CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL08_SpearHead\Spearhead Catsuit 3BA\Spearhead Catsuit Armor 3BA.osd | meshes\ZLJ\CombatLatex\CL08_SpearHead\ | Spearhead_Catsuit_Armor_3BA | EXACT_OUTPUT_PATH |


## 6. DDS actually in use

Distinct source DDS in the closure: **29**

| source_virtual_path | winning_provider | owning_outfit_of_source | target_virtual_path | action |
|---|---|---|---|---|
| Textures\1Nye\Colors\Gray.dds | Nyes Latex Pack AiO 1.3 (ReducedSize) | UNKNOWN |  | UNRESOLVED |
| Textures\1Nye\Cubemaps\FlatNormal.dds | Nyes Latex Pack AiO 1.3 (ReducedSize) | UNKNOWN |  | UNRESOLVED |
| Textures\1Nye\Cubemaps\FlatCubemap.dds | UNKNOWN | UNKNOWN |  | UNRESOLVED |
| Textures\1Nye\Cubemaps\Studio.dds | Sassy Salt 与 Wind 头发材质重制 - 原版与 KS 发型 — Sassy Salt and Wind Hair Retexture - Vanilla and KS Hairdos — 【材质·NPC】【材质·替换】【NPC·脸部】 | UNKNOWN |  | UNRESOLVED |
| textures\devious\devices\catsuitLatexRed_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexRed_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_n.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_em.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_em.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\expansion\zad_Ebonite_e.dds | 私密装置 乳胶材质 — Better DD Latex - Clean — 【材质·替换】【服装·装备】 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\zad_Ebonite_e.dds | COPY_INTO_OUTFIT_NAMESPACE |
| Textures\1Nye\Colors\Gray.dds | Nyes Latex Pack AiO 1.3 (ReducedSize) | UNKNOWN |  | UNRESOLVED |
| Textures\1Nye\Cubemaps\FlatNormal.dds | Nyes Latex Pack AiO 1.3 (ReducedSize) | UNKNOWN |  | UNRESOLVED |
| Textures\1Nye\Cubemaps\FlatCubemap.dds | UNKNOWN | UNKNOWN |  | UNRESOLVED |
| Textures\1Nye\Cubemaps\Studio.dds | Sassy Salt 与 Wind 头发材质重制 - 原版与 KS 发型 — Sassy Salt and Wind Hair Retexture - Vanilla and KS Hairdos — 【材质·NPC】【材质·替换】【NPC·脸部】 | UNKNOWN |  | UNRESOLVED |
| textures\devious\devices\catsuitLatexBlack_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexBlack_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_n.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_em.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_em.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\expansion\zad_Ebonite_e.dds | 私密装置 乳胶材质 — Better DD Latex - Clean — 【材质·替换】【服装·装备】 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\zad_Ebonite_e.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatexBlack_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexBlack_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_n.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\armor\[TRX]  LatexWhitch\zad_ebonite_e.dds | 私密装置 乳胶材质 — Better DD Latex - Clean — 【材质·替换】【服装·装备】 | UNKNOWN |  | UNRESOLVED |
| textures\devious\devices\catsuitLatexBlack_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexBlack_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_n.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\armor\[TRX]  LatexWhitch\zad_ebonite_e.dds | 私密装置 乳胶材质 — Better DD Latex - Clean — 【材质·替换】【服装·装备】 | UNKNOWN |  | UNRESOLVED |
| textures\devious\devices\catsuitLatexBlack_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexBlack_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_n.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\armor\[TRX]  LatexWhitch\zad_ebonite_e.dds | 私密装置 乳胶材质 — Better DD Latex - Clean — 【材质·替换】【服装·装备】 | UNKNOWN |  | UNRESOLVED |
| textures\devious\devices\catsuitLatexBlack_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexBlack_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_n.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\expansion\zad_Ebonite_e.dds | 私密装置 乳胶材质 — Better DD Latex - Clean — 【材质·替换】【服装·装备】 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\zad_Ebonite_e.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatexBlack_d.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexBlack_d.dds | COPY_INTO_OUTFIT_NAMESPACE |
| textures\devious\devices\catsuitLatex_n.dds | 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 | EXTERNAL_MOD | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_n.dds | COPY_INTO_OUTFIT_NAMESPACE |
| `... 141 more rows in the CSV` | | | | |


## 6b. Body morph TRI (not a physics config)

_`none`_


## 6c. Model role (ARMA/ARMO slot semantics)

| model_role | canonical_runtime | body_relevance | old_path | new_path | status |
|---|---|---|---|---|---|
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\Catsuita01t01_1.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuita01t01_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\Catsuitg01t01_1.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuitg01t01_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\Catsuitg01t02_1.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuitg01t02_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\Catsuitg02t01_1.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuitg02t01_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\Catsuitg02t02_1.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuitg02t02_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\Catsuith01t01.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuith01t01.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\Catsuith01t02.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuith01t02.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\Catsuith02t01.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuith02t01.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\Catsuith02t02.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuith02t02.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\Catsuith03t01.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuith03t01.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\Catsuith03t02.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuith03t02.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\Catsuitl01t01_1.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuitl01t01_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\Catsuitl01t02_1.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuitl01t02_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\Catsuita01t01S_1.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuita01t01S_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\Catsuita01t01S_1.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuita01t01S_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\Catsuita01t01_1.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\Catsuita01t01_1.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | NO | CBBE_3BA | bbdrac\spearhead catsuit heel.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\spearhead catsuit heel.nif | UNRESOLVED |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\gaghold for FO4 HOOD.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\gaghold for FO4 HOOD.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | NO | CBBE_3BA | bbdrac\gaghold for FO4 HOOD RED.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\gaghold for FO4 HOOD RED.nif | UNRESOLVED |
| WEARABLE_FEMALE_3P | NO | CBBE_3BA | bbdrac\latex hood black.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\latex hood black.nif | UNRESOLVED |
| WEARABLE_FEMALE_3P | NO | CBBE_3BA | bbdrac\latex hood red.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\latex hood red.nif | UNRESOLVED |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\catsuith03t02 - red.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\catsuith03t02 - red.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\(Nye) Latex Corset.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\(Nye) Latex Corset.nif | COPY_AND_REPOINT |
| WEARABLE_FEMALE_3P | YES | CBBE_3BA | bbdrac\(Nye) Latex Corset - red.nif | meshes\ZLJ\CombatLatex\CL08_SpearHead\(Nye) Latex Corset - red.nif | COPY_AND_REPOINT |


Non-canonical roles kept separate: FIRSTPERSON_FEMALE=21, WORLD_FEMALE=18, WORLD_MALE=6, FIRSTPERSON_MALE=3

## 7. Physics

_`none`_


## 8. Existing PBR (provenance only)

No PBR patch mod is registered for this outfit in the P02A registry.

## 9. Cross dependencies (current -> planned)

- cross-outfit texture dependencies: **5** (open after plan: 5)
- external-mod texture dependencies: **109** (open after plan: 0)
- audit counters: cross-outfit open **0** / external-mod-missing **0** / hard-unresolved **37** / vanilla-allowed **0** / shared proposals **0**
- unresolvable DDS by class (distinct files): none - a DDS absent from the frozen P00 VFS is already broken at runtime today; it is listed, never guessed

| dependency_type | source_owner | source_virtual_path | referenced_by_nif | resolution_plan | target_virtual_path | post_plan_state |
|---|---|---|---|---|---|---|
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\bbdrac\Catsuita01t01S_1.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\bbdrac\gaghold for FO4 HOOD RED.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\bbdrac\latex hood black.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\bbdrac\latex hood red.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | UNKNOWN | meshes\bbdrac\spearhead catsuit heel.nif | BLOCKED: the BSShaderTextureSet of this mesh is absent from the frozen P00 NIF index, so P02A could not derive it. This is an evidence-coverage gap, not a read-only restriction: parsing the binary is permitted. Resolve in P02B by parsing the mesh, or by listing the BSA that contains it. |  | OPEN_BLOCKED |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL02_OnceMedic;CL04_Haley;CL11_SkimpyAssassin | textures\devious\devices\catsuitLatex_em.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_Feet_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 5 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_em.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL02_OnceMedic;CL03_Tachy;CL04_Haley;CL05_Valby;CL11_SkimpyAssassin | textures\devious\devices\catsuitLatex_n.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_Glove_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 6 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_n.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL02_OnceMedic;CL04_Haley;CL11_SkimpyAssassin | textures\devious\devices\catsuitLatexBlack_d.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_Feet_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 5 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexBlack_d.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL02_OnceMedic | textures\devious\devices\catsuitLatexRed_d.dds | meshes\AE Once Human\AM\AE_Once_Combat_Medic_Glove_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 2 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexRed_d.dds | CLOSED_BY_DUPLICATION |
| CROSS_PACK_CANDIDATE | CL01_LatexKitty;CL02_OnceMedic;CL04_Haley;CL11_SkimpyAssassin | textures\devious\expansion\zad_Ebonite_e.dds | meshes\AE_Latex_Kitty\AE_Latex_Kitty_Feet_1.nif | PROPOSAL_SHARED_NOT_APPROVED: identical sha256  is consumed by 5 outfits of this pack. P02A keeps a private copy per outfit and creates NO Shared folder; material sharing is a P05 decision. | textures\ZLJ\CombatLatex\CL08_SpearHead\zad_Ebonite_e.dds | CLOSED_BY_DUPLICATION |
| UNRESOLVED | UNKNOWN | Textures\1Nye\Colors\Gray.dds | meshes\bbdrac\(Nye) Latex Corset - red.nif | BLOCKED: PATH-MISMATCH, not fuzzy-resolvable: the referenced folder does not exist, only same-basename files elsewhere were found. Those are NOT treated as the same asset. Candidate locations are recorded in P02A_GLOBAL_PROVIDER_LOOKUP.csv: input reference_class=UNKNOWN; probed forms: textures/1nye/colors/gray.dds; loose game Data hit: none; PATH MISMATCH: the referenced folder does not exist, but 2 mod(s) in this instance ship a file with the same basename elsewhere: Nyes Latex Pack AiO 1.3 (ReducedSize) :: textures/NyesLatexPack/latex corset with chains/gray.dds; See Through Portals 与 Oblivion Gates - Myrwatch - The Cause - 基础 Object Swapper — See Through Portals and Oblivion Gates - Myrwatch - The Cause - Base Object Swapper — 【系统·性能】【作者·wankingSkeever】 :: textures/Creation Club better cubemaps/gray.dds; NOT upgraded to EXTERNAL_PROVIDER_FOUND: no provider exists at the referenced path, and a same-basename file elsewhere is NOT proof of the same asset -- identity would be a fuzzy match, which this stage forbids. Left UNKNOWN for human confirmation; winning provider is a PATH-MISMATCH provider, not a provider of the referenced path; winning provider is in the frozen P00 TARGET09 scope; game Data root has no loose 'textures' folder and holds 93 .bsa archives. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | Textures\1Nye\Cubemaps\FlatNormal.dds | meshes\bbdrac\(Nye) Latex Corset - red.nif | BLOCKED: PATH-MISMATCH, not fuzzy-resolvable: the referenced folder does not exist, only same-basename files elsewhere were found. Those are NOT treated as the same asset. Candidate locations are recorded in P02A_GLOBAL_PROVIDER_LOOKUP.csv: input reference_class=UNKNOWN; probed forms: textures/1nye/cubemaps/flatnormal.dds; loose game Data hit: none; PATH MISMATCH: the referenced folder does not exist, but 1 mod(s) in this instance ship a file with the same basename elsewhere: Nyes Latex Pack AiO 1.3 (ReducedSize) :: textures/NyesLatexPack/flatnormal.dds; NOT upgraded to EXTERNAL_PROVIDER_FOUND: no provider exists at the referenced path, and a same-basename file elsewhere is NOT proof of the same asset -- identity would be a fuzzy match, which this stage forbids. Left UNKNOWN for human confirmation; winning provider is a PATH-MISMATCH provider, not a provider of the referenced path; winning provider is in the frozen P00 TARGET09 scope; game Data root has no loose 'textures' folder and holds 93 .bsa archives. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | Textures\1Nye\Cubemaps\FlatCubemap.dds | meshes\bbdrac\(Nye) Latex Corset - red.nif | BLOCKED: Global provider lookup executed over all MO2 mod directories plus the game Data folder: no provider at this exact path, no loose game Data file, and the basename occurs in no mod of the instance. Lookup evidence: input reference_class=TRUE_MISSING; probed forms: textures/1nye/cubemaps/flatcubemap.dds; loose game Data hit: none; complete lookup: no provider at this path, no loose game Data file, and the basename occurs in NO mod dir of this instance; .bsa-packed contents remain unverified and are a known blind spot; game Data root has no loose 'textures' folder and holds 93 .bsa archives. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | Textures\1Nye\Cubemaps\Studio.dds | meshes\bbdrac\(Nye) Latex Corset - red.nif | BLOCKED: PATH-MISMATCH, not fuzzy-resolvable: the referenced folder does not exist, only same-basename files elsewhere were found. Those are NOT treated as the same asset. Candidate locations are recorded in P02A_GLOBAL_PROVIDER_LOOKUP.csv: input reference_class=UNKNOWN; probed forms: textures/1nye/cubemaps/studio.dds; loose game Data hit: none; PATH MISMATCH: the referenced folder does not exist, but 3 mod(s) in this instance ship a file with the same basename elsewhere: Sassy Salt 与 Wind 头发材质重制 - 原版与 KS 发型 — Sassy Salt and Wind Hair Retexture - Vanilla and KS Hairdos — 【材质·NPC】【材质·替换】【NPC·脸部】 :: textures/KS Hairdo's/HDT/Studio.dds; KS 发型 1.7 Salt 与 Wind — KS Hairdos 1.7 Salt and Wind — 【外观·角色】 :: Textures/KS Hairdo's/HDT/Studio.dds; KS物理发型 — KS Hairdos - HDT SMP (Physics) — 【外观·角色】【身体·物理】 :: Textures/KS Hairdo's/HDT/Studio.dds; NOT upgraded to EXTERNAL_PROVIDER_FOUND: no provider exists at the referenced path, and a same-basename file elsewhere is NOT proof of the same asset -- identity would be a fuzzy match, which this stage forbids. Left UNKNOWN for human confirmation; winning provider is a PATH-MISMATCH provider, not a provider of the referenced path; winning provider is out the frozen P00 TARGET09 scope; game Data root has no loose 'textures' folder and holds 93 .bsa archives. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatexRed_d.dds | meshes\bbdrac\(Nye) Latex Corset - red.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatexRed_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexRed_d.dds and repoint meshes\bbdrac\(Nye) Latex Corset - red.nif / Corset / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexRed_d.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatex_n.dds | meshes\bbdrac\(Nye) Latex Corset - red.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatex_n.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_n.dds and repoint meshes\bbdrac\(Nye) Latex Corset - red.nif / Corset / Normal so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_n.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatex_em.dds | meshes\bbdrac\(Nye) Latex Corset - red.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatex_em.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_em.dds and repoint meshes\bbdrac\(Nye) Latex Corset - red.nif / Corset / EnvMask so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_em.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\expansion\zad_Ebonite_e.dds | meshes\bbdrac\(Nye) Latex Corset - red.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor zad_Ebonite_e.dds (provider 私密装置 乳胶材质 — Better DD Latex - Clean — 【材质·替换】【服装·装备】, priority 767) into textures\ZLJ\CombatLatex\CL08_SpearHead\zad_Ebonite_e.dds and repoint meshes\bbdrac\(Nye) Latex Corset - red.nif / Corset / EnvMap so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL08_SpearHead\zad_Ebonite_e.dds | CLOSED |
| UNRESOLVED | UNKNOWN | Textures\1Nye\Colors\Gray.dds | meshes\bbdrac\(Nye) Latex Corset.nif | BLOCKED: PATH-MISMATCH, not fuzzy-resolvable: the referenced folder does not exist, only same-basename files elsewhere were found. Those are NOT treated as the same asset. Candidate locations are recorded in P02A_GLOBAL_PROVIDER_LOOKUP.csv: input reference_class=UNKNOWN; probed forms: textures/1nye/colors/gray.dds; loose game Data hit: none; PATH MISMATCH: the referenced folder does not exist, but 2 mod(s) in this instance ship a file with the same basename elsewhere: Nyes Latex Pack AiO 1.3 (ReducedSize) :: textures/NyesLatexPack/latex corset with chains/gray.dds; See Through Portals 与 Oblivion Gates - Myrwatch - The Cause - 基础 Object Swapper — See Through Portals and Oblivion Gates - Myrwatch - The Cause - Base Object Swapper — 【系统·性能】【作者·wankingSkeever】 :: textures/Creation Club better cubemaps/gray.dds; NOT upgraded to EXTERNAL_PROVIDER_FOUND: no provider exists at the referenced path, and a same-basename file elsewhere is NOT proof of the same asset -- identity would be a fuzzy match, which this stage forbids. Left UNKNOWN for human confirmation; winning provider is a PATH-MISMATCH provider, not a provider of the referenced path; winning provider is in the frozen P00 TARGET09 scope; game Data root has no loose 'textures' folder and holds 93 .bsa archives. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | Textures\1Nye\Cubemaps\FlatNormal.dds | meshes\bbdrac\(Nye) Latex Corset.nif | BLOCKED: PATH-MISMATCH, not fuzzy-resolvable: the referenced folder does not exist, only same-basename files elsewhere were found. Those are NOT treated as the same asset. Candidate locations are recorded in P02A_GLOBAL_PROVIDER_LOOKUP.csv: input reference_class=UNKNOWN; probed forms: textures/1nye/cubemaps/flatnormal.dds; loose game Data hit: none; PATH MISMATCH: the referenced folder does not exist, but 1 mod(s) in this instance ship a file with the same basename elsewhere: Nyes Latex Pack AiO 1.3 (ReducedSize) :: textures/NyesLatexPack/flatnormal.dds; NOT upgraded to EXTERNAL_PROVIDER_FOUND: no provider exists at the referenced path, and a same-basename file elsewhere is NOT proof of the same asset -- identity would be a fuzzy match, which this stage forbids. Left UNKNOWN for human confirmation; winning provider is a PATH-MISMATCH provider, not a provider of the referenced path; winning provider is in the frozen P00 TARGET09 scope; game Data root has no loose 'textures' folder and holds 93 .bsa archives. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | Textures\1Nye\Cubemaps\FlatCubemap.dds | meshes\bbdrac\(Nye) Latex Corset.nif | BLOCKED: Global provider lookup executed over all MO2 mod directories plus the game Data folder: no provider at this exact path, no loose game Data file, and the basename occurs in no mod of the instance. Lookup evidence: input reference_class=TRUE_MISSING; probed forms: textures/1nye/cubemaps/flatcubemap.dds; loose game Data hit: none; complete lookup: no provider at this path, no loose game Data file, and the basename occurs in NO mod dir of this instance; .bsa-packed contents remain unverified and are a known blind spot; game Data root has no loose 'textures' folder and holds 93 .bsa archives. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| UNRESOLVED | UNKNOWN | Textures\1Nye\Cubemaps\Studio.dds | meshes\bbdrac\(Nye) Latex Corset.nif | BLOCKED: PATH-MISMATCH, not fuzzy-resolvable: the referenced folder does not exist, only same-basename files elsewhere were found. Those are NOT treated as the same asset. Candidate locations are recorded in P02A_GLOBAL_PROVIDER_LOOKUP.csv: input reference_class=UNKNOWN; probed forms: textures/1nye/cubemaps/studio.dds; loose game Data hit: none; PATH MISMATCH: the referenced folder does not exist, but 3 mod(s) in this instance ship a file with the same basename elsewhere: Sassy Salt 与 Wind 头发材质重制 - 原版与 KS 发型 — Sassy Salt and Wind Hair Retexture - Vanilla and KS Hairdos — 【材质·NPC】【材质·替换】【NPC·脸部】 :: textures/KS Hairdo's/HDT/Studio.dds; KS 发型 1.7 Salt 与 Wind — KS Hairdos 1.7 Salt and Wind — 【外观·角色】 :: Textures/KS Hairdo's/HDT/Studio.dds; KS物理发型 — KS Hairdos - HDT SMP (Physics) — 【外观·角色】【身体·物理】 :: Textures/KS Hairdo's/HDT/Studio.dds; NOT upgraded to EXTERNAL_PROVIDER_FOUND: no provider exists at the referenced path, and a same-basename file elsewhere is NOT proof of the same asset -- identity would be a fuzzy match, which this stage forbids. Left UNKNOWN for human confirmation; winning provider is a PATH-MISMATCH provider, not a provider of the referenced path; winning provider is out the frozen P00 TARGET09 scope; game Data root has no loose 'textures' folder and holds 93 .bsa archives. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatexBlack_d.dds | meshes\bbdrac\(Nye) Latex Corset.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatexBlack_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexBlack_d.dds and repoint meshes\bbdrac\(Nye) Latex Corset.nif / Corset / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexBlack_d.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatex_n.dds | meshes\bbdrac\(Nye) Latex Corset.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatex_n.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_n.dds and repoint meshes\bbdrac\(Nye) Latex Corset.nif / Corset / Normal so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_n.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatex_em.dds | meshes\bbdrac\(Nye) Latex Corset.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatex_em.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_em.dds and repoint meshes\bbdrac\(Nye) Latex Corset.nif / Corset / EnvMask so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_em.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\expansion\zad_Ebonite_e.dds | meshes\bbdrac\(Nye) Latex Corset.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor zad_Ebonite_e.dds (provider 私密装置 乳胶材质 — Better DD Latex - Clean — 【材质·替换】【服装·装备】, priority 767) into textures\ZLJ\CombatLatex\CL08_SpearHead\zad_Ebonite_e.dds and repoint meshes\bbdrac\(Nye) Latex Corset.nif / Corset / EnvMap so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL08_SpearHead\zad_Ebonite_e.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatexBlack_d.dds | meshes\bbdrac\Catsuita01t01_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatexBlack_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexBlack_d.dds and repoint meshes\bbdrac\Catsuita01t01_1.nif / CatT / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexBlack_d.dds | CLOSED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatex_n.dds | meshes\bbdrac\Catsuita01t01_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatex_n.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_n.dds and repoint meshes\bbdrac\Catsuita01t01_1.nif / CatT / Normal so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatex_n.dds | CLOSED |
| UNRESOLVED | UNKNOWN | textures\armor\[TRX]  LatexWhitch\zad_ebonite_e.dds | meshes\bbdrac\Catsuita01t01_1.nif | BLOCKED: PATH-MISMATCH, not fuzzy-resolvable: the referenced folder does not exist, only same-basename files elsewhere were found. Those are NOT treated as the same asset. Candidate locations are recorded in P02A_GLOBAL_PROVIDER_LOOKUP.csv: input reference_class=UNKNOWN; probed forms: textures/armor/[trx]  latexwhitch/zad_ebonite_e.dds; loose game Data hit: none; PATH MISMATCH: the referenced folder does not exist, but 4 mod(s) in this instance ship a file with the same basename elsewhere: 私密装置 乳胶材质 — Better DD Latex - Clean — 【材质·替换】【服装·装备】 :: textures/devious/expansion/zad_Ebonite_e.dds; 私密装置 高清材质 — Devious Devices upscaled 2k — 【材质】 :: textures/devious/expansion/zad_Ebonite_e.dds; 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3 :: textures/devious/expansion/zad_Ebonite_e.dds; 私密装置 核心框架 — Devious Devices for AE — 【NSFW·框架】【平台·AE】【来源·本地】【系列·DD】 :: textures/devious/expansion/zad_Ebonite_e.dds; NOT upgraded to EXTERNAL_PROVIDER_FOUND: no provider exists at the referenced path, and a same-basename file elsewhere is NOT proof of the same asset -- identity would be a fuzzy match, which this stage forbids. Left UNKNOWN for human confirmation; winning provider is a PATH-MISMATCH provider, not a provider of the referenced path; winning provider is out the frozen P00 TARGET09 scope; game Data root has no loose 'textures' folder and holds 93 .bsa archives. Resolution needs a human ruling or a further evidence extension; no fuzzy match is allowed. |  | OPEN_BLOCKED |
| EXTERNAL_MOD | EXTERNAL_MOD | textures\devious\devices\catsuitLatexBlack_d.dds | meshes\bbdrac\Catsuita01t01_1.nif | COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor catsuitLatexBlack_d.dds (provider 私密装置 次世代 — Devious Devices NG — 【技术·框架】【来源·本地】【系列·DD】 v0.4.3, priority 777) into textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexBlack_d.dds and repoint meshes\bbdrac\Catsuita01t01_1.nif / CatB / Diffuse so the outfit is self-contained (shared-asset whitelist = NONE). | textures\ZLJ\CombatLatex\CL08_SpearHead\catsuitLatexBlack_d.dds | CLOSED |
| `... 128 more rows in the CSV` | | | | | | |


## 10. Self-containment audit (simulated post-migration)

| gate | result | metric | evidence |
|---|---|---|---|
| GAME_MESH_SELF_CONTAINED | PASS | 65 | game mesh rows=65, target off-namespace=0, collisions=0 |
| TEXTURE_SELF_CONTAINED | REVIEW | 177 | slots(nif=171 shapedata=53) / off-namespace=0 / provider-found=0 / true-missing=10 / path-mismatch-unknown=37 / no-lookup=0 / vanilla=0 / global-body-skin=0 / proposals=91 / open cross-outfit=0 |
| BODYSLIDE_SELF_CONTAINED | PASS | 1 | projects=1 chain-incomplete=0 OSP-off-ns=0 ShapeData-off-ns=0 Output-off-ns=0 UNKNOWN-basis=0 shapedata-tex-off-ns=0 |
| PLUGIN_PATHS_PLANNED | BLOCKED | 48 | records=48 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=24 flagged-canonical=20 world-models=24 plugin-DDS-cross-outfit-open=0 / model refs: source-asset-absent=12 foreign-body-decision=0 |
| MODEL_ROLE_SCHEMA | PASS | 72 | role enum violations (legacy WORLD/WEARABLE/GROUND)=0, unknown-enum=0 / distribution: WEARABLE_FEMALE_3P=24, FIRSTPERSON_FEMALE=21, WORLD_FEMALE=18, WORLD_MALE=6, FIRSTPERSON_MALE=3 |
| PHYSICS_PATHS_PLANNED | PASS | 0 | physics configs=0 types= / without-new-path=0 bone-unknown=0 |
| TRI_MORPH_SEPARATION | PASS | 0 | morph rows=0 (.tri sources=0) / TRI rows wrongly present in physics table=0 / physics types= |
| TARGET_OSP_NAMESPACE | PASS | 1 | distinct target OSP for this outfit=1 expected=1 -> ['calientetools/bodyslide/slidersets/zlj_cl08_spearhead.osp'] |
| UNRESOLVED_REFERENCE_PROVENANCE | REVIEW | 10 | distinct unresolved DDS=10, without a global provider-lookup verdict=0, rows whose texture set is not derivable at all (BSA-resident stock mesh, no path to look up)=5 |
| OUTFIT_SELF_CONTAINMENT | BLOCKED | 9 | C1..C9 = C1:PASS, C2:REVIEW, C3:PASS, C4:BLOCKED, C6:PASS, C5:PASS, G7:PASS, C8:PASS, C9:REVIEW |


## 11. BLOCKERS

- `C2` TEXTURE_SELF_CONTAINED = **REVIEW** - slots(nif=171 shapedata=53) | off-namespace=0 | provider-found=0 | true-missing=10 | path-mismatch-unknown=37 | no-lookup=0 | vanilla=0 | global-body-skin=0 | proposals=91 | open cross-outfit=0
- `C4` PLUGIN_PATHS_PLANNED = **BLOCKED** - records=48 wrong-target-plugin=0 missing-EDID=0 canonical-female-models=24 flagged-canonical=20 world-models=24 plugin-DDS-cross-outfit-open=0 | model refs: source-asset-absent=12 foreign-body-decision=0
- `C9` UNRESOLVED_REFERENCE_PROVENANCE = **REVIEW** - distinct unresolved DDS=10, without a global provider-lookup verdict=0, rows whose texture set is not derivable at all (BSA-resident stock mesh, no path to look up)=5
- `TOTAL` OUTFIT_SELF_CONTAINMENT = **BLOCKED** - C1..C9 = C1:PASS, C2:REVIEW, C3:PASS, C4:BLOCKED, C6:PASS, C5:PASS, G7:PASS, C8:PASS, C9:REVIEW

---

P02A stops here. No COPY / MOVE / DELETE / NIF / ESP / OSP / DDS write was performed and none is authorised until this design is reviewed by a human.
