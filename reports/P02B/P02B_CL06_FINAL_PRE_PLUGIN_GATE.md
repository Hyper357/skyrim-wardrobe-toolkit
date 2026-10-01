# P02B_CL06 FINAL PRE-PLUGIN GATE (P02B2.2 canonicalization)

**Scope:** CL06_ToxicCat only. No asset re-migration, no P00/P01/P02A rerun, no other outfit, no ESP.

Every number below is **aggregated from `P02B_CL06_PILOT_PLUGIN_PLAN.csv`**, not from intended logic.

## 1. Two path concepts, kept apart

| concept | example |
|---|---|
| `target_virtual_mesh_path` | `meshes\ZLJ\CombatLatex\CL06_ToxicCat\AE_Toxic_Cat_1.nif` |
| `target_plugin_model_path` | `ZLJ\CombatLatex\CL06_ToxicCat\AE_Toxic_Cat_1.nif` |

An ARMA/ARMO model field is relative to `Data\meshes\`, so the `meshes\` prefix belongs to the disk
path only. TXST is a different field family: texture filenames are relative to `Data\`, so they keep their
`textures\` prefix. The two rules were not crossed.

## 2. Classification, read back from the CSV

| change class | rows |
|---|---|
| MODEL_PATH_REPOINT | 21 |
| GENDER_NEUTRAL_SHARED_REPOINT | 12 |
| MALE_SLOT_EMPTY | 18 |
| ARMO_WORLD_NO_CHANGE | 21 |
| TXST_REPOINT | 22 |
| **total** | **94** |

## 3. Topology, verified inside the CSV

| check | result |
|---|---|
| Body MOD3 and MOD5 byte-identical plugin path | **6/3 ARMA records** |
| HeadACC MOD2 and MOD3 byte-identical plugin path | **3/3** |
| Mask MOD2 and MOD3 byte-identical plugin path | **3/3** |
| distinct canonical female plugin targets | 5 |
| ARMA world-model classes present | **none** |

## 4. Stale-string sweep

| pattern | must be | found |
|---|---|---|
| `\1p\` in a plugin model path | 0 | **0** |
| `\male\` in a neutral/female plugin model path | 0 | **0** |
| plugin model path starting with `meshes\` | 0 | **0** |
| ARMA classed as a world model | 0 | **0** |

## 5. Plan gate

| id | check | expected | actual | result |
|---|---|---|---|---|
| G1 | PLUGIN_MODEL_PATH_STARTS_WITH_MESHES | 0 | 0 | **PASS** |
| G2 | STALE_1P_TARGETS | 0 | 0 | **PASS** |
| G3 | STALE_MALE_NEUTRAL_TARGETS | 0 | 0 | **PASS** |
| G4 | BODY_MOD3_MOD5_TARGET_IDENTICAL | 3/3 | 3/3 | **PASS** |
| G5 | HANDS_MOD3_MOD5_TARGET_IDENTICAL | 3/3 | 3/3 | **PASS** |
| G6 | HEADACC_MOD2_MOD3_TARGET_IDENTICAL | 3/3 | 3/3 | **PASS** |
| G7 | MASK_MOD2_MOD3_TARGET_IDENTICAL | 3/3 | 3/3 | **PASS** |
| G8 | MALE_SLOT_EMPTY | 18 | 18 | **PASS** |
| G9 | ARMO_WORLD_NO_CHANGE | 21 | 21 | **PASS** |
| G10 | TXST_REPOINT | 22 | 22 | **PASS** |
| G11 | VIRTUAL_MESH_PATH_EXISTS | 0 missing | 0 missing | **PASS** |
| G12 | PLUGIN_MODEL_PATH_MAPS_BACK | 0 missing | 0 missing | **PASS** |
| G13 | TXST_TARGET_NAMESPACE | 0 wrong | 0 | **PASS** |
| G14 | NO_ARMA_WORLD_MODEL_CLASS | 0 | 0 | **PASS** |

    PLUGIN_PLAN_STATIC_GATE = PASS

## 6. Still outstanding

    BODYSLIDE_WEIGHTED_BUILD = BLOCKED_PENDING_ISOLATED_BUILD

The isolated weighted build (`_0 = 5/5` and `_1 = 5/5` inside one physical tree) has not been run; see
`P02B_CL06_ISOLATED_BUILD_REPORT.md`. This document therefore certifies the **plan**, not the pipeline.

## STOP

No ESP written. No other outfit touched. No PBR, no UBE, no final `ZLJ_CombatLatex.esp`.
