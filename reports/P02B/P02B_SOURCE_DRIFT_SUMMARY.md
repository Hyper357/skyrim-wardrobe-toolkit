# P02B0 source-drift summary

Incremental check only - P00 was **not** rescanned. The live tree is stat-ed and hashed, never written.

## Modlist

| field | frozen P00 | current |
|---|---|---|
| lines | 2254 | 2256 |
| sha256 | `5f03db69574ba916` | `c590c89233ba772a` |
| verdict | | **CHANGED** |

## CL06 pilot gate

Effective provider set for CL06_ToxicCat: 4 mod(s).

* `BnP - 女性皮肤 — BnP - Female Skin — 【NPC·脸部】` - no files compared
* `Static Mesh Improvement Mod - SMIM — 【网格·环境】` - no files compared
* `makaron-COSPLAY - AE_Toxic_Cat — 【服装·装备】【来源·本地】` - UNCHANGED=47
* `男性身体大修 HIMBO·02) HIMBO V5 — 02) HIMBO V5 - BG-DG-DB Refits — 【身体·物理】【体型·HIMBO】【HIMBO】` - no files compared

**CL06_PILOT_GATE = PASS** (CHANGED=0, REMOVED=0)

## Per-outfit drift

| outfit | UNCHANGED | CHANGED | NEW | REMOVED |
|---|---|---|---|---|
| `CL01_LatexKitty` | 62 | 0 | 0 | 0 |
| `CL02_OnceMedic` | 80 | 0 | 0 | 0 |
| `CL03_Tachy` | 29 | 10 | 1 | 0 |
| `CL04_Haley` | 93 | 0 | 0 | 0 |
| `CL05_Valby` | 41 | 0 | 0 | 0 |
| `CL06_ToxicCat` | 47 | 0 | 0 | 0 |
| `CL07_Lupa` | 44 | 0 | 0 | 0 |
| `CL08_SpearHead` | 65 | 0 | 0 | 0 |
| `CL09_Corrupted` | 73 | 0 | 0 | 0 |
| `CL10_HoodST` | 52 | 0 | 0 | 0 |
| `CL11_SkimpyAssassin` | 42 | 0 | 0 | 0 |

Outfits other than CL06 are recorded only; their drift is refreshed locally when their turn comes.
