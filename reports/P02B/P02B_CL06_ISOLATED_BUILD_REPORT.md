# P02B_CL06 ISOLATED BUILD REPORT

**Scope:** CL06_ToxicCat only. No plan change, no ESP, no asset re-migration, no other outfit.

---

# Part 1 - P02B2.3 audit outcome

## The isolated build is not on disk

I was asked to audit a completed CL06 isolated build. **No such build exists on this machine.** The gate therefore
stays closed - `BODYSLIDE_WEIGHTED_BUILD_PASS` is **not** declared.

### What I checked, and what I found

| search | result |
|---|---|
| `staging\ZLJ Combat Latex Pack - CL06 Isolated Build\` | exists, **empty** (0 files) |
| MO2 mod named `*Isolated*` | **none** |
| `AE_Toxic_Cat*` under `E:\SkyrimAE\mo2` with mtime after 01:00 | **none** |
| `AE_Toxic_Cat*` under `E:\SkyrimAE` outside mo2 | **none** |
| any `*Toxic*` file under `E:\SkyrimAE` modified after 01:00 | **none** |
| `输出·BodySlide Output\...\CL06_ToxicCat\` | still the 00:47 build, unchanged |
| pilot mod `_1.nif` | still the 00:47 build, unchanged |
| MO2 `overwrite` | nothing recent |

### The five sets

| slider set | `_0` | `_1` | `.tri` |
|---|---|---|---|
| ToxicCat - AE Toxic Cat | MISSING | MISSING | MISSING |
| ToxicCat - Feet | MISSING | MISSING | MISSING |
| ToxicCat - Hands | MISSING | MISSING | MISSING |
| ToxicCat - Top | MISSING | MISSING | MISSING |
| ToxicCat - Stockings | MISSING | MISSING | MISSING |

0 of the 15 expected products are present, so there is nothing to parse: shape counts, skinning, partitions, texture
references and the TRI-to-mesh correspondence cannot be evaluated. Same-physical-tree containment also fails trivially -
not because products landed in separate providers, but because no product was produced at all.

## Why it likely did not run

The tool state at the time of this audit (10:05) is consistent with a session that was opened but never built:

* BodySlide is **running** (PID 12200, started 10:04:49), started through MO2.
* Its log `Log_BS.txt` was recreated at 10:04:49 and contains **no `batch build` line and no `ToxicCat` entry**.
* Its current selection is `AE_Silent_Code_Feet` with the outfit filter `silent` - i.e. another outfit entirely.
* `OutfitStudio.xml` and `Log_OS.txt` were touched at 10:01:45, so Outfit Studio was opened shortly before.

So the isolated build was not executed - possibly because the run focused on Silent Code instead, possibly because the
custom path step was not reached. I am reporting the state rather than guessing the intent.

## One extra note on isolation

Even when it is run, the pilot mod's `_1.nif` files must not be the destination. From the Part 2 provider audit,
BodySlide redirects a write to the physical provider of an existing file. If the isolated tree has no `_1.nif` yet,
the pre-existing pilot copy is a candidate destination and the build could silently split again. Two ways to prevent it:

1. Point Custom Path at the isolated tree **and** remove the pilot mod's CL06 `_1` meshes for the duration of the
   build (they are reproducible from the frozen migration, but this does touch the installed pilot mod), or
2. Accept the risk but verify afterwards - check that the isolated tree holds 15/15 and that no `_1.nif` under any
   other provider changed mtime during the build window. This audit is exactly that verification.

## How to close the gate

1. Run BodySlide through MO2 with the pilot mod enabled.
2. Batch Build -> enable **Custom Path** -> `...\5-latex-wardrobe-collection\staging\ZLJ Combat Latex Pack - CL06 Isolated Build\`.
3. Ensure weight generation is on, so `_1.nif` is written for all five sets. Keep TRI generation on.
4. Build the five `[ZLJ Combat Latex] ToxicCat - *` sets.
5. Re-run `tools/P02B/p02b_isolated_audit.py`. `BODYSLIDE_WEIGHTED_BUILD_PASS` is declared automatically only
   when `_0 = 5/5`, `_1 = 5/5`, `TRI = 5/5` **and** all 15 sit inside the isolated tree.

## Status

    PLUGIN_PLAN_STATIC_GATE      = PASS     (14/14, carried forward, unchanged)
    BODYSLIDE_WEIGHTED_BUILD     = BLOCKED  (products absent)
    CL06_ASSET_AND_BODYSLIDE_PIPELINE_FROZEN = NOT DECLARED
    READY_FOR_PILOT_PLUGIN       = NOT DECLARED

The asset migration and the plugin plan are frozen and verified. Only the isolated weighted build is outstanding.

---

# Part 2 - P02B2.1 background: where the first build's output went

## What the first build actually did (provider audit)

My earlier statement "BodySlide only generated `_0`" was wrong. The physical-provider audit shows the
build wrote **both** variants, into two different physical providers:

| file | physical provider | mtime | content vs pre-build staging | classification |
|---|---|---|---|---|
| AE_Toxic_Cat_1.nif | **PILOT mod** | 2026-10-01 **00:47:19** | **differs** | BUILD_WROTE_TO_PILOT_PROVIDER |
| AE_Toxic_Cat_Feet_1.nif | PILOT mod | 00:47:18 | differs | BUILD_WROTE_TO_PILOT_PROVIDER |
| AE_Toxic_Cat_Hand_1.nif | PILOT mod | 00:47:18 | differs | BUILD_WROTE_TO_PILOT_PROVIDER |
| AE_Toxic_Cat_Top_1.nif | PILOT mod | 00:47:18 | differs | BUILD_WROTE_TO_PILOT_PROVIDER |
| AE_Toxic_Cat_St_1.nif | PILOT mod | 00:47:18 | differs | BUILD_WROTE_TO_PILOT_PROVIDER |
| all five `_0.nif` | 输出·BodySlide Output | 00:47:18-19 | new file | newly created |

**5/5 `_1` were written by BodySlide into the pilot mod.** Their mtimes fall exactly inside the batch window
(00:47:18-00:47:19) and their content differs from the pre-build staging copy (00:31:02), so they are build products,
not the migrated copies. Those rebuilt `_1` meshes were re-verified: 0 old `textures\ae_toxic_cat\` references,
34 references inside the ZLJ namespace, 20 global body skin - i.e. the rewritten ShapeData paths survived the rebuild.

### Mechanism

This is MO2 VFS **write redirection by existing file**:

* `_0.nif` did not exist anywhere in the virtual tree -> BodySlide created it, and the write landed in the
  output mod.
* `_1.nif` already existed in the pilot mod -> BodySlide's write was redirected to that physical provider.

Which is exactly why `Custom Path = False` cannot guarantee a single physical output tree, and why the review
requires an isolated build.

Full evidence: `P02B_CL06_BUILD_PROVIDER_AUDIT.csv`.

## Why I could not run the isolated build myself

I extracted BodySlide's complete command-line option table from the binary. It is:

| option | description |
|---|---|
| `gbuild` / `groupbuild` | builds the specified group on launch |
| `targetdir` | build target directory, defaults to game data path |
| `preset` | preset used for the build, defaults to last used preset |
| `tri` / `trimorphs` | enables tri morph output for the specified build |
| `preview` | open the specified nif files in preview mode |

There is **no batch / target / outfit option**. The only build trigger available from the command line is a *group*
build, and it cannot be used here: the BodySlide log records `No group assigned for set '...'` for every one of our
five sets. Assigning a group would mean editing the installed pilot OSP, i.e. changing a frozen deliverable, and it
still would not set the custom output path.

So the isolated build is a **GUI action**: the batch-build dialog owns both the Custom Path and the weight option.

---

## STOP

No ESP written. No other outfit touched (the Silent Code activity observed is not mine). No PBR, no UBE, no final
`ZLJ_CombatLatex.esp`.
