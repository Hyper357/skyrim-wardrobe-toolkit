# P02B1 CL06_ToxicCat MIGRATION REPORT

**Phase:** P02B0 pre-flight + P02B1 pilot. **Status: staging + automated validation complete - STOP.**

P02A is APPROVED and was not redone. Only `CL06_ToxicCat` was built. Every output lives under
`staging\ZLJ Combat Latex Pack - P02B Pilot\`; no original mod was modified.

## 1. Rulings applied

| ruling | application in this pilot |
|---|---|
| RULING-01 female canonical only | 5 external male-body meshes (`Armor\Studded\Male\*`) marked NON_CANONICAL_MALE / DO_NOT_VENDOR and **not copied**; the outfit's own gender-neutral HeadACC.nif and Mask.nif are **kept** and shared with the male slots |
| RULING-02 global body skin | 40 references to `textures\actors\character\female\*` left external, never copied, never rewritten into the ZLJ tree |
| RULING-03 world model | 4 vanilla world/drop models (`*_GO.nif`) left external; no vendoring for self-containment |
| RULING-04 one OSP per outfit | one target OSP `ZLJ_CL06_ToxicCat.osp` holding all 5 source SliderSets; not treated as a blocker |

## 2. What was produced (31 files in staging)

| subtree | files |
|---|---|
| `meshes\ZLJ\CombatLatex\CL06_ToxicCat\` | 9 runtime NIF: 5 canonical 3rd-person, 2 canonical 1st-person under `1p\`, 2 shared gender-neutral |
| `textures\ZLJ\CombatLatex\CL06_ToxicCat\` | 11 DDS |
| `CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\CL06_ToxicCat\AE_Toxic_Cat\` | 5 ShapeData NIF + 5 OSD |
| `CalienteTools\BodySlide\SliderSets\ZLJ_CL06_ToxicCat.osp` | 1 target OSP (5 sets, 247 sliders) |

## 3. NIF texture rewriting

The rewrite is done with the **vendored PyNifly** at `E:\SkyrimAE\Tools\pynifly` - the same library the P00
pipeline used to parse NIFs - so the header, block table and string storage are handled by the library rather than by
hand-rolled byte arithmetic.

| metric | value |
|---|---|
| NIFs rewritten | 12 (7 runtime + 5 ShapeData) |
| references now inside the outfit namespace | 61 |
| old `textures\ae_toxic_cat\*` references remaining | **0** |
| global body-skin references preserved | 40 |
| foreign/other references | 0 |

## 4. Automated validation

Ten of eleven checks pass and one is explicitly NOT_RUN; see `P02B_CL06_VALIDATION.csv`.

| # | check | result |
|---|---|---|
| 1 | all files exist | PASS (0 of 28 missing) |
| 2 | target collision = 0 | PASS |
| 3 | NIF broken texture | PASS (0 missing inside the namespace) |
| 4 | ShapeData broken texture | PASS |
| 5 | old AE_Toxic_Cat clothing refs = 0 | PASS |
| 6 | cross-outfit DDS = 0 | PASS |
| 7 | male external assets copied = 0 | PASS |
| 8 | BodySlide output path correct | PASS (5 of 5) |
| 9 | generated output resolves | **NOT_RUN** (no build performed) |
| 11 | ARMA target coverage | PASS (0 of 21 missing) |
| 10 | source mods untouched | PASS (0 of 47 changed) |

Phase status: **STATIC_MIGRATION_PASS / FUNCTIONAL_VALIDATION_PENDING**. No CL06 pilot PASS is claimed.

## 5. Source drift (P02B0)

See `P02B_SOURCE_DRIFT_CHECK.csv` and `P02B_SOURCE_DRIFT_SUMMARY.md`.

* modlist.txt **CHANGED** (2254 to 2256 lines).
* `CL06_ToxicCat` and its effective providers: **all 47 files UNCHANGED** - **CL06_PILOT_GATE = PASS**.
* `CL03_Tachy` is **CHANGED** (an external BodySlide / Outfit Studio session wrote its ShapeData and mesh files
  at 23:01, 23:38 and 23:42). Recorded, **not** allowed to block CL06, and to be refreshed locally when CL03's turn comes.

## 6. Not done in P02B1 (deliberately)

| item | reason |
|---|---|
| `ZLJ_CombatLatex_CL06_Pilot.esp` | **not built.** The review permits it for game testing, but no xEdit is installed and writing a plugin by hand would mean re-serialising records, groups, master indices and FormIDs with no way to validate the result here. Shipping an unvalidated binary plugin into a live load order is the one thing that could actually damage the instance, so it is deferred to a dedicated step with a real ESP tool. |
| pilot batch build | requires the staged OSP to be visible through MO2; see the load-test document. |
| other ten outfits | out of scope for P02B1. |
| merge / PBR / UBE / numeric rework / slot remap / enchant / SPID | forbidden by the phase. |

## 7. Errors made and corrected in this phase

Reported for the record. Each was caught by measurement or by the reviewer, not by luck:

1. **A path-construction bug wrote 28 files to `E:\meshes`, `E:\textures` and `E:\CalienteTools`**
   instead of staging, because the workspace helper returns a `data\\` prefix with a double separator.
   The stray trees were verified to contain only our CL06 namespace, then deleted; the path builder was rewritten and
   the migration re-run. Nothing was written into any mod or game folder.
2. **ShapeData landed one folder too high** because a ledger key carried a trailing separator. Caught by comparing the
   staged tree against the OSP's DataFolder; fixed and re-run.
3. **A source NIF referenced by two ARMA slots was copied to only one of its two required targets.**
   `AE_Toxic_Cat_1.nif` and `AE_Toxic_Cat_Hand_1.nif` serve BOTH the 3rd-person (MOD3) and the 1st-person
   (MOD5) female slots, but the copy loop wrote only `sorted(targets)[0]` - the `1p\` variant - so the 3rd-person
   runtime meshes were missing. Found during the P02B1.1 pre-build review of the 1P/3P question; the migration now writes
   every canonical target and was re-run. Check 11 (ARMA target coverage) was added so this class of defect cannot pass
   silently again. See `P02B1_PRE_BUILD_GATE.md` section 3.
4. An initial NIF rewrite attempt used a hand-rolled string-table patch and silently rewrote only one of two
   occurrences of each path. It was discarded in favour of PyNifly after measurement showed the defect.

## 8. Next human actions

1. Run the BodySlide load test per `P02B_CL06_BODYSLIDE_LOAD_TEST.md` section 2.
2. Confirm the four derived part labels (Feet / Hands / Top / Stockings).
3. Confirm whether a pilot ESP is still wanted in P02B1, and if so authorise an ESP-capable tool for it.
4. Note that an external BodySlide/Outfit Studio session is **currently active** on this machine and keeps changing
   `CL03_Tachy`; freeze that activity before any copy is executed.
