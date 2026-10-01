# P02B RULINGS - recorded from the P02A.1 human review

**Phase:** P02B0 pre-flight + P02B1 CL06_ToxicCat pilot.
**Status of P02A:** **APPROVED**. P00 / P01 / P02A are not to be redone.

These four rulings are authoritative for the pilot and override any earlier P02A wording that conflicts with them.

---

## RULING-01 - FEMALE CANONICAL ONLY

The canonical runtime of **ZLJ Combat Latex Pack** is **CBBE_3BA FEMALE**.

For ARMA model slots:

* Any **MALE** or **MALE FIRSTPERSON** model that references
  * HIMBO, or
  * a vanilla male body armor mesh, or
  * any other external male body system

  is classified **NON_CANONICAL_MALE**.

* The target plugin must **not** copy those assets into
  `meshes\ZLJ\CombatLatex\<OUTFIT_ID>\`.
  The corresponding male model field in the final ARMA **may be left empty**.

* **Exception - genuinely gender-neutral assets owned by the outfit itself.**
  Where the male and female fields already reference the *same* outfit-owned, gender-neutral asset
  (Mask, HeadACC, Hood, certain accessories), both fields may keep pointing at that one NIF inside the
  outfit namespace. Mechanically deleting genuinely neutral pack assets is **not** allowed.

---

## RULING-02 - GLOBAL BODY SKIN

These continue to be **KEEP_EXTERNAL_REFERENCE** and must **not** be copied into an outfit namespace:

* `femalebody_*.dds`
* `femalehands_*.dds`
* the current **BnP** winning body skin

A future **UBE branch** handles body-family skin compatibility separately.

---

## RULING-03 - WORLD MODEL

* A world / drop model that comes from **Skyrim vanilla**, **SMIM**, or another **global base resource**
  stays an **external reference**. It must **not** be vendored into an outfit namespace merely to achieve
  self-containment.
* A world model that is the **outfit's own dedicated NIF** follows the outfit's migration.

---

## RULING-04 - OSP

Formally adopted: **one Outfit = one target OSP**, e.g. `ZLJ_CL06_ToxicCat.osp`, and that OSP **may contain
multiple SliderSets**. This is a **supported BodySlide capability**, not an anomalous structure.

P02B therefore performs exactly one **BODYSLIDE_OSP_LOAD_SMOKE_TEST** per pilot, verifying:

* every set appears in the UI,
* the slider count matches the source,
* the output path is correct.

**Once that test passes, a multi-set OSP is no longer treated as a blocker.**

---

## Scope of P02B1

Only **CL06_ToxicCat** is built. All output goes to
`staging\ZLJ Combat Latex Pack - P02B Pilot\`. **No original mod may be modified.**

## READ-ONLY semantics (clarified)

READ-ONLY means: **reading and parsing binaries is allowed; writing or mutating is forbidden.**
The earlier P02A phrasing "the read-only rule forbids opening a binary" was wrong and has been removed.
P02B may therefore parse NIF / DDS / ESP binaries freely, and does.

---

## REFERENCE_TOPOLOGY_RULE (frozen in P02B1.2, permanent)

When **several ARMA model slots** reference the **same** source virtual NIF, the migrated target keeps that sharing:
**one canonical NIF** is written, and every one of those slots points at it.

Splitting into separate files is allowed **only** with evidence:

* the source itself ships a dedicated first-person NIF, or
* a dedicated BodySlide output exists for that slot, or
* an independent geometry / weight requirement exists, or
* a human explicitly approves the split.

**A differing MOD3 / MOD5 slot number is not evidence.** Copying one source NIF into several target files merely
because two slots name it is forbidden - BodySlide only ever updates the file named by OutputPath + OutputFile, so an
artificial copy would silently go stale.

Topology is recorded per row in P02B_CL06_BODYSLIDE_ARMA_MATRIX.csv as source_reference_topology in
{SHARED_RUNTIME_MESH, DEDICATED_1P, DEDICATED_3P, UNKNOWN}.

## GLOBAL_BODYSLIDE_RESOURCE (frozen in P02B1.2)

A BodySlide OSD / ShapeData file referenced by an outfit OSP but owned by a body mod (for example CBBE Feet.osd from
Caliente's Beautiful Bodies Enhancer) is classified **GLOBAL_BODYSLIDE_RESOURCE**. It stays an external dependency
and is **never vendored** into an outfit namespace.
