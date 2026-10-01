# P02B1 PRE-BUILD GATE (P02B1.2 reference-topology correction)

**Scope:** only `CL06_ToxicCat`. P00 / P01 / P02A were not re-run. No other outfit was touched.
**No BodySlide build was executed.**

## 1. Reference topology corrected

The previous round split one source NIF into two targets merely because two ARMA slots named it. That was wrong.

The source uses a **shared runtime mesh**:

| source NIF | slots that reference it | correct target |
|---|---|---|
| `meshes\AE_Toxic_Cat\AE_Toxic_Cat_1.nif` | MOD3 FEMALE_3P + MOD5 FEMALE_1P | `meshes\ZLJ\CombatLatex\CL06_ToxicCat\AE_Toxic_Cat_1.nif` |
| `meshes\AE_Toxic_Cat\AE_Toxic_Cat_Hand_1.nif` | MOD3 FEMALE_3P + MOD5 FEMALE_1P | `meshes\ZLJ\CombatLatex\CL06_ToxicCat\AE_Toxic_Cat_Hand_1.nif` |

Both slots now resolve to the **same canonical NIF**, which is exactly the file BodySlide writes
(`OutputPath meshes\ZLJ\CombatLatex\CL06_ToxicCat` + `OutputFile AE_Toxic_Cat` produces `AE_Toxic_Cat_0.nif` and `AE_Toxic_Cat_1.nif`).

The artificial copies were removed from staging:

* `...\CL06_ToxicCat\1p\AE_Toxic_Cat_1.nif` - deleted
* `...\CL06_ToxicCat\1p\AE_Toxic_Cat_Hand_1.nif` - deleted
* the now-empty `1p\` directory - removed

**No source mod file was deleted or modified.**

## 2. REFERENCE_TOPOLOGY_RULE - permanent

Recorded in `P02B_RULINGS.md`. When several ARMA model slots reference the same source virtual NIF, the target
keeps that sharing and one canonical NIF is written. Splitting requires evidence (a dedicated source 1P NIF, a dedicated
BodySlide output, an independent geometry/weight requirement, or explicit human approval). **A differing MOD3/MOD5 slot
number is not evidence.** BodySlide only ever updates `OutputPath` + `OutputFile`, so an artificial copy would
silently go stale - which is precisely what the removed files would have done.

## 3. Matrix updated

`P02B_CL06_BODYSLIDE_ARMA_MATRIX.csv` now carries `source_reference_topology`, `canonical_target`,
`p02a_ledger_target` and `corrected_by_p02b12`.

| UI name | topology | slots | canonical target |
|---|---|---|---|
| [ZLJ Combat Latex] ToxicCat - AE Toxic Cat | **SHARED_RUNTIME_MESH** | MOD3 + MOD5 | `...\CL06_ToxicCat\AE_Toxic_Cat_1.nif` |
| [ZLJ Combat Latex] ToxicCat - Hands | **SHARED_RUNTIME_MESH** | MOD3 + MOD5 | `...\CL06_ToxicCat\AE_Toxic_Cat_Hand_1.nif` |
| [ZLJ Combat Latex] ToxicCat - Feet | DEDICATED_3P | MOD3 | `...\AE_Toxic_Cat_Feet_1.nif` |
| [ZLJ Combat Latex] ToxicCat - Top | DEDICATED_3P | MOD3 | `...\AE_Toxic_Cat_Top_1.nif` |
| [ZLJ Combat Latex] ToxicCat - Stockings | DEDICATED_3P | MOD3 | `...\AE_Toxic_Cat_St_1.nif` |

21 ARMA references: FEMALE_3P 15 (MOD3) / FEMALE_1P 6 (MOD5). `corrected_by_p02b12=YES` marks every row whose
P02A ledger target is superseded by this correction.

## 4. GLOBAL_BODYSLIDE_RESOURCE

`CBBE Feet.osd` (referenced by the Feet slider set) is owned by Caliente's Beautiful Bodies Enhancer at
`CalienteTools\BodySlide\ShapeData\CBBE\CBBE Feet.osd`. It is classified **GLOBAL_BODYSLIDE_RESOURCE**, stays an
external dependency, and is **not vendored**.

## 5. One yardstick for staging size

Previously staging reported 31 files while the manifest declared 30 and the validator counted 28. The three now use a
single definition - the file set on disk must equal the manifest's COPY rows:

| measure | count |
|---|---|
| files on disk in staging | **29** |
| staging manifest COPY rows | **29** |
| validator denominator | **29** |
| only on disk / only in manifest | **0 / 0** |

The OSP is now a manifest row too (`CalienteTools\BodySlide\SliderSets\ZLJ_CL06_ToxicCat.osp`), which is what closed
the gap.

## 6. Static gate

| criterion | result |
|---|---|
| broken clothing DDS | **0** |
| old ToxicCat DDS refs | **0** |
| cross-outfit DDS | **0** |
| ARMA canonical targets resolve | **100%** (0 of 21 missing) |
| BodySlide output to MOD3/MOD5 topology | **PASS** (2 shared sets, 0 wrong targets) |
| stale artificial 1p copies | **0** |

    PASS=12  FAIL=0  NOT_RUN=1   (13 checks)
    STATIC_MIGRATION      = PASS
    FUNCTIONAL_VALIDATION = PENDING

The single NOT_RUN is `GENERATED_OUTPUT_RESOLVES`: it asserts something about the output of a real BodySlide build
and cannot be honest before that build happens.

## 7. Verdict

    READY_FOR_BODYSLIDE_TEST

All six required criteria hold. Next step is the human-run load test and pilot build in
`P02B_CL06_BODYSLIDE_LOAD_TEST.md` section 2; it needs staging to be visible through MO2. **No build was run here.**
