# P02B_CL06 BODYSLIDE LOAD TEST

**Pilot:** `CL06_ToxicCat` - phase P02B1. Target OSP: `CalienteTools\BodySlide\SliderSets\ZLJ_CL06_ToxicCat.osp`.

## 1. What was verified automatically

`tools/P02B/p02b_osp_check.py` resolves every reference BodySlide would resolve at load time.

| set (UI name) | SourceFile | ShapeData NIF | sliders | shapes | OSD refs |
|---|---|---|---|---|---|
| [ZLJ Combat Latex] ToxicCat - AE Toxic Cat | AE_Toxic_Cat.nif | FOUND | 156 | 5 | all local |
| [ZLJ Combat Latex] ToxicCat - Feet | AE_Toxic_Cat_Feet.nif | FOUND | 2 | 3 | 1 external (CBBE Feet.osd) |
| [ZLJ Combat Latex] ToxicCat - Hands | AE_Toxic_Cat_Hand.nif | FOUND | 2 | 2 | all local |
| [ZLJ Combat Latex] ToxicCat - Top | AE_Toxic_Cat_Top.nif | FOUND | 86 | 1 | all local |
| [ZLJ Combat Latex] ToxicCat - Stockings | AE_Toxic_Cat_St.nif | FOUND | 1 | 1 | all local |

**LOAD_TEST_STATIC = PASS** - 5 sets, 247 sliders, 0 problems.

### 1.1 Finding: the source OSP was already multi-set

The P02A ledger recorded **one** BodySlide project for CL06. The source OSP actually contains
**five** SliderSets (`AE_Toxic_Cat`).

This is direct field evidence for **RULING-04**: a multi-set OSP is a normal, supported structure, and it is what the
original author shipped. All five sets are preserved in the target OSP; the primary one keeps the UI name the review
specified, the other four are named per the frozen convention `[ZLJ Combat Latex] ToxicCat - <Part>`.

**Decision needed:** confirm the part labels (Body / Feet / Hands / Top / Stockings). They are derived from the source
set names, not invented from thin air, but they were not specified by the review.

### 1.2 External OSD

The Feet set references `CBBE Feet.osd`, which is not an outfit asset: it ships with
`Caliente's Beautiful Bodies Enhancer - CBBE` at `CalienteTools\BodySlide\ShapeData\CBBE\CBBE Feet.osd`.
This is a **global body resource**, so per RULING-03 it stays external and is **not** vendored.

## 2. Interactive load test

**RESULT: PENDING_HUMAN - not executable in this phase.**

I was authorised to launch BodySlide and did so, from an isolated copy of the tool placed inside staging. The
attempt is recorded because it produced a conclusive negative result:

    [23:44:23] Working directory: E:\SkyrimAE
    [23:44:23] Executable directory: E:\SkyrimAE\data\CalienteTools\BodySlide
    [23:44:23] Game data path in config: E:\SkyrimAE\Data\

BodySlide resolves its SliderSets from the **game data path**, not from its own folder, so the isolated copy loaded the
production SliderSets and never touched the staged OSP. Confirming the load therefore requires the staged OSP to be
visible through the MO2 virtual filesystem.

Making it visible means installing staging as an MO2 mod and enabling it, which would modify the MO2 instance and is
**not authorised**. So this check is handed to the human.

### Steps for the human reviewer

1. Install `staging\ZLJ Combat Latex Pack - P02B Pilot\` as an MO2 mod (it is already laid out as a mod folder).
2. Enable it and start BodySlide through MO2.
3. Confirm: five projects appear under `[ZLJ Combat Latex] ToxicCat - *`; slider counts read 156 / 2 / 2 / 86 / 1;
   the preview renders without a missing-shape or missing-OSD error.
4. Only then run the pilot build of `[ZLJ Combat Latex] ToxicCat - AE Toxic Cat` with the output redirected to staging.

**No batch build was performed in P02B1.** The acceptance criteria that depend on a running BodySlide session
(UI listing, Preview, Batch Build) remain open and are explicitly listed in the validation CSV as not executed.

## 3. Status

| item | state |
|---|---|
| OSP generated into staging | done |
| all five sets preserved | done |
| static reference resolution | **PASS** |
| multi-set OSP treated as a blocker | **no** (RULING-04) |
| interactive load test | **PENDING_HUMAN** |
| pilot batch build | **not run** |
