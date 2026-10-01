# p00r_reports.py — schema-fix migration notes (scratch)

Scope: `tools/P00_RERUN/p00r_reports.py` only. No parser was touched.

## New module helpers

| helper | why |
|---|---|
| `UNK` / `NONE` | absent field -> `UNKNOWN`; positively-empty field -> `NONE`. Never conflated. |
| `jval(v)` | raw subrecord payload. int -> 8-hex FormID, bytes -> hex, else str. |
| `jnum(v)` | count / mask. int -> decimal (NOT a FormID). |
| `joinl(v, empty=)` | list field join, explicit empty token. |
| `as_list(v)` | 04 ships `;`-joined **strings** for some fields; `len(str)` counts characters. Normalise first. |
| `arma_pairs(armo)` | 1:N walk pairing `arma_refs` with `modl_refs` on the **8-digit** formid to recover the route. |
| `flat_models(blk)` | MOD2..MOD5 in slot order. |
| `texture_set_text()` / `TSET_KEYS` | MO2S..MO5T. Scanned on **both** ARMO and ARMA — ARMO rows do carry MO2S/MO2T/MO4S for their world model. |
| `parts_table()` | accepts bare list or `{"stats","parts"}`; returns an explicit `upstream stage unavailable` note instead of crashing. |
| `project_source_mod()` | new single `source_mod`, legacy `source_mods` list as fallback. |
| `_num()` | balance field as plain number or `{"u32","f32"}` pair. |
| `calibration_status()` | reads `reports/P00_RERUN/PARSER_CALIBRATION.md` (+ any `data/P00_RERUN/*calib*.json`). Missing -> `not yet generated`. |
| `SUPERSEDED` | single source of truth for the invalidated-output table, used by both markdown reports. |

## 02_PLUGIN_RECORDS.csv (48 cols)

Removed: `arma_link`, `arma_edid` (they read RNAM as the addon).
Added: `slot_bits`, `slot_source`, `slot_confidence`, `race_formid/race_is/
race_plugin/race_type/race_edid/race_route`, `ARMA_formids`, `ARMA_edids`,
`ARMA_plugins`, `ARMA_routes`, `model_path_kind`, `world_model_paths`,
`world_model_note`, `armor_material_raw`, `n_source_mesh_refs`,
`outfit_target_formid/type/edid`.

`model_path_kind` disambiguates: `ARMO_WORLD_MODEL` vs `ARMA_WEARABLE_MODEL`.

## 03_ARMOR_ARMA_MAP.csv (25 cols)

One row per (ARMO, ArmorAddon) pair. An ARMO with no ArmorAddon gets **zero**
rows — measured 108/1448, cross-checked against 04 `n_arma_refs=0` = 108.
Carries `resolution_route` per pair plus the joined ARMA block
(wearable models / texture sets / slots / material / source_mesh_refs).

## 07_BODYSLIDE_PROJECTS.csv (32 cols)

Keyed on `OSP_PATH`, one row per `.osp`. Every column XML-derived. The
hard-coded `meshes\clothing` is gone; `output_path` / `output_nif` come from the
OSP and `output_path_is_guessed` is carried through (all `no`).
Handles `07_bodyslide_shapedata.json` as a dict `{"nif","osd","errors"}`.

## Measured (this run)

- ARMO 1448 | with >=1 ArmorAddon 1340 (92.5%) | without 108
- MODL refs 1855 -> ARMA 1344; unresolved 509, ambiguous(85) 1, ambiguous(57) 1
- links emitted in 03 = 1344
- RNAM -> RACE 1442/1448
- OTFT.INAM still not a FormID in the current evidence file -> reported as
  UNKNOWN, target NOT recovered (honest; needs a stage-B rerun)

## Bugs found and fixed in my own new code during verification

1. `jval()` was rendering counts/masks as 8-hex FormIDs -> added `jnum()`.
2. First 5b pass took `len("a;b;c")` on 04's `;`-joined strings
   (82,585 "NIFs") -> added `as_list()`; now 903 paths / 795 parts.
3. First r02 pass printed `NONE` for ARMO `texture_set_refs`, but ARMO rows do
   carry MO2S/MO2T/MO4S -> now scanned from raw subrecords for both types.

## Not mine / observed upstream

- `04_parts.json::game_nif_resolved` currently emits NIF **paths** (314 distinct)
  or empty, not the `yes|pending_build|no` vocabulary the brief specifies.
  The report transcribes it as-is, caps the table at 12 rows, and flags the
  mismatch. Not rewritten here — p00r_parts.py is another agent's file.
- `reports/P00_RERUN/PARSER_CALIBRATION.md` does not exist yet -> both reports
  say `not yet generated` and issue no verdict.

## Run

`python tools\P00_RERUN\p00r_reports.py` -> exit 0, 21 CSVs + 00_SCOPE.md +
P00_MASTER_REPORT.md + P00_RERUN_VS_OLD.md. Deterministic across reruns.
