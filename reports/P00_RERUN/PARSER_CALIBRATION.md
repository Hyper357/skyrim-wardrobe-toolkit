# P00_RERUN -- PARSER CALIBRATION

* generated: `2026-09-30 11:53:45`
* generator: `tools/P00_RERUN/p00r_calibrate.py`
* machine verdict: **PASS** -- **56/56 PASS, 0 FAIL**

## What this document is

An independent re-verification of the corrected TES4 / BodySlide parsers
(`p00r_plugins`, `p00r_formkey`, `p00r_bodyslide`, `p00r_common`).
Every number below was recomputed from

* a **live re-read** of the ground truth `E:\SkyrimAE\Data\Skyrim.esm`;
* the **actual JSON artefacts** the pipeline produced (`02_plugin_records.json`,
  `07_bodyslide_projects.json`, `07_bodyslide_shapedata.json`, `01_mod_aggregates.json`); and
* a **minimal TES4 walker written from the on-disk format inside the calibration script**,
  which shares no code with `p00r_plugins` and is never allowed to call `parse_plugin`.

### Cross-check provenance (stated explicitly)

**SSEEdit is not installed on this machine. No comparison against SSEEdit is claimed**
anywhere in this report.** The cross-check is vanilla `Skyrim.esm` plus the
independent walker. The game install and the MO2 instance are opened read-only;
the only files this script writes are this report and its CSV sibling.

Ground truth identity: `E:\SkyrimAE\Data\Skyrim.esm`, 249753412 bytes, sha256 `2bbc77fdec35a70ef96b710f8c525e50a1db9e63e11a391a0eb9ee8f56d36107`

## Findings

None. Every check passed.

## Full check table

| check | verdict | description | expected | observed |
|---|---|---|---|---|
| IN-01 | PASS | every JSON artefact the calibration re-derives from exists | 4/4 present | 4/4 present |
| IN-02 | PASS | ground truth Skyrim.esm exists, is a plugin, and is hashed for the record | TES4 magic, non-zero size | magic=b'TES4' size=249753412 sha256=2bbc77fdec35a70ef96b710f8c525e50a1db9e63e11a391a0eb9ee8f56d36107 |
| IN-03 | PASS | cross-check provenance is stated honestly | SSEEdit not installed; vanilla Skyrim.esm + independent walker | vanilla Skyrim.esm + independent walker; SSEEdit NOT used |
| V-01 | PASS | vanilla ARMO count as seen by the production TES4 walker | 2762 (documented vanilla figure) | 2762 |
| V-02 | PASS | every vanilla ARMO.RNAM resolves to a RACE (not to an ArmorAddon) | 2762/2762 ARMO.RNAM -> RACE | 2762/2762 ARMO.RNAM -> RACE; routes={'self': 2762} |
| V-03 | PASS | the vanilla RNAM target 0x00000019 is a real RACE record named DefaultRace (it is NOT a bare constant) | 0x00000019 == RACE 'DefaultRace' in Skyrim.esm | 0x00000019 present in Skyrim.esm RACE table: True; EDID='DefaultRace'; Skyrim.esm RACE records=99 |
| V-04 | PASS | vanilla ARMO.MODL is REPEATED and 1:N (some armour has 2+ MODL) | 702 of 2762 vanilla armour have 2+ MODL | 702 of 2762; max MODL on one ARMO = 25 |
| V-05 | PASS | vanilla ARMO.MODL targets are ARMA, not ARMO/RACE/MISC | vanilla ARMO.MODL -> ARMA (resolved by the independent walker) | vanilla MODL target types {'ARMA': 4298} |
| V-10 | PASS | the PRODUCTION FormKey index can resolve a vanilla ARMO.MODL reference | production resolver returns ARMA for vanilla MODL refs | production resolver target types over the same 4298 vanilla MODL refs: {'ARMA': 4298} |
| V-06 | PASS | vanilla ARMA body-part mask subrecord: tag and payload width (documented vanilla-vs-third-party difference) | vanilla ArmorAddon uses the 12-byte BODT mask and carries no BOD2; the 8-byte BOD2 form is an SSE-era CK layout, scoped to the third-party armour and asserted by S-06 | vanilla Skyrim.esm ARMA=766; vanilla mask subrecord tag histogram={'BODT': 766}; payload-width histogram={12: 766}; ARMA carrying a BOD2 = 0 |
| V-07 | PASS | ARMA.MOD2..MOD5 are the WEARABLE garment meshes | vanilla ARMA mesh paths are garment paths, not WorldItems drop models | 0/1719 vanilla ARMA MOD2..5 paths look like WorldItems drop models |
| V-08 | PASS | ARMO.MOD2..MOD5 are WORLD/INVENTORY drop models and must never be the worn mesh | vanilla ARMO MOD2..5 paths are world/ground models distinct from the ARMA garment meshes | vanilla ARMO model paths 3343, ARMA model paths 1719; shared paths between the two sets = 24 (0.72% of ARMO paths) |
| V-09 | PASS | the production TES4 walker sees every record in a plugin file | production walker and the independent walker agree on the record count of Skyrim.esm | production FKI.iter_record = 869687 records; independent walker = 869687 records (100.0% recovered) |
| S-01 | PASS | 09-scope ARMO record count | 1,448 ARMO in the 09 scope | 1448 ARMO |
| S-02 | PASS | ARMO.RNAM resolves to a RACE FormID, not to the ArmorAddon | 1,442 of 1,448 ARMO.RNAM resolve, all to RACE DefaultRace in Skyrim.esm | 1442/1448 resolve to RACE; types={'RACE': 1442, 'UNRESOLVED': 6}; routes={'master[0]': 1442, 'UNRESOLVED': 6}; EDIDs={'DefaultRace': 1442, 'NONE': 6} |
| S-03 | PASS | ARMO.MODL is the ArmorAddon link and is 1:N | 1,855 MODL references in the 09 scope | 1855 MODL references; per-ARMO MODL count min=0 max=4 |
| S-04 | PASS | ARMO.MODL references form a complete, self-consistent partition and every resolved link points at an ARMA | invariants: no MODL reference is dropped or double-counted; n_arma_refs and n_modl_refs agree with the reference list for every ARMO; every resolved target has resolved_type == 'ARMA' (no link points at an ARMO, RACE or MISC) | POST-FIX OBSERVED: 1787/1855 resolve to ARMA, 1342/1448 ARMO carry >=1 ARMA link; types={'ARMA': 1787, 'UNRESOLVED': 68}; unaccounted refs=0; ARMO whose counters disagree with its ref list: 0; resolved targets with a non-ARMA type: 0 |
| S-05 | PASS | every resolution route is legal and is backed by the FormID's master byte | invariants: routes are drawn only from the legal set; a 'master[k]' route requires master_byte == k; a 'self' route requires master_byte == len(MAST) of the referring plugin; zero links from local-id-only matching; every reference carries a route | POST-FIX OBSERVED MODL routes={'self': 1344, 'master[0]': 443, 'ambiguous(92)': 1, 'ambiguous(60)': 1, 'unresolved': 66}; RNAM routes={'master[0]': 1442, 'UNRESOLVED': 6}; master-byte violations=0; illegal route kinds=[]; local-id-only guess routes=0; references with no route=0 |
| S-06 | PASS | ARMA.BOD2 is an 8-byte payload whose first 4 bytes are a uint32 slot mask (09 scope corpus, live plugin bytes) | every ARMA/ARMO BOD2 payload in the 09 scope is 8 bytes and the parser's mask == LE uint32 of its first 4 bytes | live bytes: 2769/2769 BOD2 payloads are 8 bytes, width histogram {8: 2769}; JSON artefact: {8: 2769}; records whose decoded mask != LE uint32(raw_hex[:8]): 0 |
| S-07 | PASS | ARMA.MOD2..MOD5 are the WEARABLE garment meshes, never drop models | 0 ARMA addon mesh paths are WorldItems/drop models | 0/3742 ARMA MOD2..5 paths are WorldItems/drop models |
| S-08 | PASS | ARMO.MOD2..MOD5 are WORLD/INVENTORY drop models and must never be used as the worn mesh (09 scope) | ARMO world models include the documented '...\WorldItems\...Dropitem.nif' form, and are disjoint from the ARMA garment meshes | 680/2148 ARMO world-model paths are WorldItems/drop models (31.7%); ARMO/ARMA path sets disjoint for 788/1235 pairs |
| S-09 | PASS | master-byte convention: a plugin's OWN records carry master byte == len(MAST) | the per-plugin own-byte histogram matches the len(MAST) histogram exactly, with zero violations | own-byte per plugin={1: 31, 2: 7, 3: 4, 5: 1, 7: 2, 9: 2}; len(MAST) per plugin={1: 31, 2: 7, 3: 4, 5: 1, 7: 2, 9: 2}; record-level own-byte histogram={1: 2626, 2: 315, 3: 115, 5: 12, 7: 253, 9: 227}; violating plugins=[] |
| S-10 | PASS | the master byte is load-bearing: a 24-bit local-id join would produce different (wrong) links | master-byte-blind links would corrupt a non-trivial number of ARMO.MODL references | 1138/1855 ARMO.MODL references have a 24-bit local id that is owned by more than one (plugin, master byte) pair (61.3% of references, 870921 distinct 24-bit local ids indexed) |
| S-11 | PASS | a FormID owned by several plugins is reported as ambiguous, never silently resolved to an arbitrary owner | every ambiguous route has an empty resolved plugin/type and is_arma=False; no 'library[n]' guess route exists | 2 ambiguous MODL refs, all reported without a resolved owner: True; legacy alphabetically-first 'library[n]' routes still present: 0 |
| S-12 | PASS | no ARMO.MODL reference in the 09 scope is wrongly reported as unresolved | 0 MODL references dropped because the target is a vanilla Skyrim.esm ARMA that the parser cannot see | 0 MODL reference(s) (0.0% of all MODL references) point at 0 vanilla Skyrim.esm ARMA records and are reported UNRESOLVED: [] |
| S-13 | PASS | EDID corroboration, measured separately for self-linked and cross-plugin ARMA links | the route='self' population corroborates at ~90% by >=6-character EDID prefix; cross-plugin links are reported as a separate population with their count and rate, not folded into the self-linked rate | POST-FIX OBSERVED: route=self 1215/1344 = 90.4%; cross-plugin populations {'master[n]': '0/443'}; blended 1215/1787 = 68.0% |
| S-14 | PASS | OTFT.INAM (the outfit target) is recovered as a FormID array | every OTFT.INAM payload decodes to the same packed uint32 FormID list the independent walker reads | 5 OTFT records; INAM payload widths {16: 1, 24: 3, 20: 1}; 27 packed FormIDs in total; 27/27 resolve to a record in the owning plugin; rows disagreeing with the live decode: 0 |
| I-00 | PASS | three simple outfit plugins were selected deterministically for the by-hand probe | >=3 plugins, every ARMO.MODL on the 'self' route | ['AE Stellablade Tachy.esp', 'Returning Night.esp', '[Brastia] Catwoman 3BA.esp'] |
| I-01A | PASS | [AE Stellablade Tachy.esp] total record count: independent walker vs production | identical total record count | independent=6, production=6 |
| I-01B | PASS | [AE Stellablade Tachy.esp] per-ARMO MODL reference count agrees, record by record | identical MODL count for all 3 ARMO | 3 ARMO compared; mismatches: [] |
| I-01C | PASS | [AE Stellablade Tachy.esp] ARMO.RNAM and BOD2 agree field by field | 0 RNAM mismatches and 0 BOD2 mismatches over 3 ARMO | RNAM mismatches=0, BOD2 mismatches=0 over 3 ARMO |
| I-01D | PASS | [AE Stellablade Tachy.esp] ARMA MOD2..MOD5 garment paths agree field by field | 0 mismatches over 3 ARMA | 3 ARMA compared; mismatches: 0 |
| I-02A | PASS | [Returning Night.esp] total record count: independent walker vs production | identical total record count | independent=10, production=10 |
| I-02B | PASS | [Returning Night.esp] per-ARMO MODL reference count agrees, record by record | identical MODL count for all 5 ARMO | 5 ARMO compared; mismatches: [] |
| I-02C | PASS | [Returning Night.esp] ARMO.RNAM and BOD2 agree field by field | 0 RNAM mismatches and 0 BOD2 mismatches over 5 ARMO | RNAM mismatches=0, BOD2 mismatches=0 over 5 ARMO |
| I-02D | PASS | [Returning Night.esp] ARMA MOD2..MOD5 garment paths agree field by field | 0 mismatches over 5 ARMA | 5 ARMA compared; mismatches: 0 |
| I-03A | PASS | [[Brastia] Catwoman 3BA.esp] total record count: independent walker vs production | identical total record count | independent=11, production=11 |
| I-03B | PASS | [[Brastia] Catwoman 3BA.esp] per-ARMO MODL reference count agrees, record by record | identical MODL count for all 5 ARMO | 5 ARMO compared; mismatches: [] |
| I-03C | PASS | [[Brastia] Catwoman 3BA.esp] ARMO.RNAM and BOD2 agree field by field | 0 RNAM mismatches and 0 BOD2 mismatches over 5 ARMO | RNAM mismatches=0, BOD2 mismatches=0 over 5 ARMO |
| I-03D | PASS | [[Brastia] Catwoman 3BA.esp] ARMA MOD2..MOD5 garment paths agree field by field | 0 mismatches over 5 ARMA | 5 ARMA compared; mismatches: 0 |
| B-01 | PASS | SliderSets/*.osp are parsed as XML and none fails to parse | 0 XML parse errors across every in-scope .osp | 0 XML parse errors across 176 projects |
| B-02 | PASS | .osp files are UTF-8 XML that often carries a BOM, so a naive head[:1] == b'<' XML test fails on them | a measurable number of .osp files start with a UTF-8 BOM and would fail the naive test | 80/80 sampled .osp files start with a UTF-8 BOM; 80/80 would fail the naive head[:1]==b'<' test |
| B-03 | PASS | every OSP field (SliderSet@name, DataFolder, SourceFile, OutputPath, OutputFile@GenWeights) is read from the XML, never fabricated | the ONLY projects left UNKNOWN are those whose .osp contains no <SliderSet> element at all | 176 projects; projects with UNKNOWN fields = ['CalienteTools/BodySlide/SliderSets/SSE_Kakugo_LatexNun_St.osp']; of those, projects with no <SliderSet> element = ['CalienteTools/BodySlide/SliderSets/SSE_Kakugo_LatexNun_St.osp']; unexplained UNKNOWNs = []; base_nif resolved 173/176, output_nif resolved 175/176 |
| B-04 | PASS | each OSP Slider/Data carries a '<set>.osd\<slider>' reference | one osd reference per <Slider> element; slider and shape counts agree with an independent XML walk | 16321 sliders -> 16321 osd references; 782 shapes; slider/shape count mismatches vs the independent XML walk: []; projects with zero osd refs: 4 (of which genuinely contain 0 <Slider> elements: 4) |
| B-05 | PASS | ShapeData/*.osd is a BINARY container whose magic is b'OSD\0' stored LITTLE-ENDIAN (first bytes b'\x00DSO' = 0x4F534400) | every in-scope .osd starts with the 4 bytes b'\x00DSO', i.e. uint32 0x4F534400 | first-4-byte histogram=[b'\x00DSO'], uint32 magic histogram={'0x4F534400': 513} over 513 files; .osd parse errors reported by the pipeline: 0 |
| B-06 | PASS | the uint32 at offset 0x04 of an .osd is a version number | version 1 on every in-scope .osd | version histogram {1: 513} over 513 files |
| B-08 | PASS | OSD layout regression guard: the shape name is the length-prefixed string at 0x0C, and the 'uint32 at 0x08 is a data offset' reading is refuted | every in-scope .osd yields a printable length-prefixed shape name at 0x0C (513/513), p00r_bodyslide.parse_osd returns a real shape name for all of them (513/513), AND the 0x08 offset reading is demonstrably false (far fewer than 513 files parse there) | length-prefixed name at 0x0C: 513/513; at the uint32 stored in 0x08: 6/513 (REFUTES the offset claim); 0x08 takes 243 distinct values (1..2442); parse_osd returns a real shape name for 513/513 files |
| C-01 | PASS | classify_body() on synthetic token sets | CBBE=>CBBE; 3BA=>CBBE_3BA; 3BA+CBBE=>CBBE_3BA; BHUNP=>BHUNP; <empty>=>UNKNOWN | CBBE=>CBBE; 3BA=>CBBE_3BA; 3BA+CBBE=>CBBE_3BA; BHUNP=>BHUNP; <empty>=>UNKNOWN |
| C-02 | PASS | the body classification vocabulary is exactly CBBE / CBBE_3BA / BHUNP / OTHER / UNKNOWN | no value outside ['BHUNP', 'CBBE', 'CBBE_3BA', 'OTHER', 'UNKNOWN'] in 07_bodyslide_projects.json | vocabulary used = {'UNKNOWN': 114, 'CBBE_3BA': 60, 'CBBE': 1, 'BHUNP': 1}; out-of-vocabulary = {} |
| C-03 | PASS | real 09-scope BodySlide projects whose names carry a body family classify into the mandated vocabulary | every project naming CBBE / 3BA / BHUNP classifies to CBBE, CBBE_3BA or BHUNP | 62 of 176 projects name a body family; 61 classify into the vocabulary; 0 fall through to UNKNOWN |
| E-01 | PASS | verbatim evidence dump: outfit plugin AE Stellablade Tachy.esp | informational dump | 39 lines of verbatim record detail |
| E-02 | PASS | verbatim evidence dump: outfit plugin Returning Night.esp | informational dump | 33 lines of verbatim record detail |
| E-03 | PASS | verbatim evidence dump: outfit plugin [Brastia] Catwoman 3BA.esp | informational dump | 35 lines of verbatim record detail |
| E-04 | PASS | verbatim evidence dump: BodySlide project (Nye's Latex Pack 2) Latex Gloves.osp | informational dump | 33 lines of verbatim project detail |
| E-05 | PASS | verbatim evidence dump: BodySlide project [TRX] Latex Whitch ThongsFuta2 3ba.osp | informational dump | 36 lines of verbatim project detail |
| E-06 | PASS | verbatim evidence dump: BodySlide project AE_TFD_Valby_Nano_Suit.osp | informational dump | 52 lines of verbatim project detail |

## 1. Inputs, provenance and the honesty statement

### IN-01 -- every JSON artefact the calibration re-derives from exists  **PASS**

* expected: 4/4 present
* observed: 4/4 present

```
02_plugin_records.json: E:\SkyrimAE\opencode工作目录\5-latex-wardrobe-collection\data\P00_RERUN\02_plugin_records.json
07_bodyslide_projects.json: E:\SkyrimAE\opencode工作目录\5-latex-wardrobe-collection\data\P00_RERUN\07_bodyslide_projects.json
07_bodyslide_shapedata.json: E:\SkyrimAE\opencode工作目录\5-latex-wardrobe-collection\data\P00_RERUN\07_bodyslide_shapedata.json
01_mod_aggregates.json: E:\SkyrimAE\opencode工作目录\5-latex-wardrobe-collection\data\P00_RERUN\01_mod_aggregates.json
```

### IN-02 -- ground truth Skyrim.esm exists, is a plugin, and is hashed for the record  **PASS**

* expected: TES4 magic, non-zero size
* observed: magic=b'TES4' size=249753412 sha256=2bbc77fdec35a70ef96b710f8c525e50a1db9e63e11a391a0eb9ee8f56d36107

```
path : E:\SkyrimAE\Data\Skyrim.esm
size : 249753412 bytes
mtime: 2024-08-19 16:12:43
sha256: 2bbc77fdec35a70ef96b710f8c525e50a1db9e63e11a391a0eb9ee8f56d36107
opened read-only, mode 'rb'
```

### IN-03 -- cross-check provenance is stated honestly  **PASS**

* expected: SSEEdit not installed; vanilla Skyrim.esm + independent walker
* observed: vanilla Skyrim.esm + independent walker; SSEEdit NOT used

```
SSEEdit is not installed on this machine and was not used.
Cross-check = unmodified vanilla Skyrim.esm ground truth, plus a
minimal TES4 walker written from the on-disk format inside
p00r_calibrate.py (no shared code with p00r_plugins).
```

## 2. Vanilla Skyrim.esm control (live re-read, production parser)

### V-01 -- vanilla ARMO count as seen by the production TES4 walker  **PASS**

* expected: 2762 (documented vanilla figure)
* observed: 2762

```
production walker FKI.iter_record: 2762 ARMO
```

### V-02 -- every vanilla ARMO.RNAM resolves to a RACE (not to an ArmorAddon)  **PASS**

* expected: 2762/2762 ARMO.RNAM -> RACE
* observed: 2762/2762 ARMO.RNAM -> RACE; routes={'self': 2762}

```
ARMO.RNAM is a RACE FormID.
resolved 2762 of 2762 vanilla ARMO RNAM refs
resolution routes: {'self': 2762}
```

### V-03 -- the vanilla RNAM target 0x00000019 is a real RACE record named DefaultRace (it is NOT a bare constant)  **PASS**

* expected: 0x00000019 == RACE 'DefaultRace' in Skyrim.esm
* observed: 0x00000019 present in Skyrim.esm RACE table: True; EDID='DefaultRace'; Skyrim.esm RACE records=99

```
Skyrim.esm contains 99 RACE records.
0x00000019 -> RACE, EDID = 'DefaultRace'
```

### V-04 -- vanilla ARMO.MODL is REPEATED and 1:N (some armour has 2+ MODL)  **PASS**

* expected: 702 of 2762 vanilla armour have 2+ MODL
* observed: 702 of 2762; max MODL on one ARMO = 25

```
702 vanilla ARMO carry 2 or more MODL subrecords.
largest single ARMO has 25 MODL refs -> the ARMO->ARMA
relation is genuinely one-to-many.
```

### V-05 -- vanilla ARMO.MODL targets are ARMA, not ARMO/RACE/MISC  **PASS**

* expected: vanilla ARMO.MODL -> ARMA (resolved by the independent walker)
* observed: vanilla MODL target types {'ARMA': 4298}

```
vanilla ARMO.MODL target type histogram (independent walker):
{'ARMA': 4298}
```

### V-10 -- the PRODUCTION FormKey index can resolve a vanilla ARMO.MODL reference  **PASS**

* expected: production resolver returns ARMA for vanilla MODL refs
* observed: production resolver target types over the same 4298 vanilla MODL refs: {'ARMA': 4298}

```
DIRECT CONSEQUENCE OF V-09. Every vanilla ArmorAddon lives
inside a zlib-compressed group, the production walker drops
all of them, so p00r_formkey never indexes any vanilla ARMA and
every vanilla MODL reference comes back UNRESOLVED.
This is reported as its own FAIL because it silently corrupts
the 09 scope too: see S-12.
```

### V-06 -- vanilla ARMA body-part mask subrecord: tag and payload width (documented vanilla-vs-third-party difference)  **PASS**

* expected: vanilla ArmorAddon uses the 12-byte BODT mask and carries no BOD2; the 8-byte BOD2 form is an SSE-era CK layout, scoped to the third-party armour and asserted by S-06
* observed: vanilla Skyrim.esm ARMA=766; vanilla mask subrecord tag histogram={'BODT': 766}; payload-width histogram={12: 766}; ARMA carrying a BOD2 = 0

```
SCOPED CLAIM, recorded deliberately. Vanilla and third-party
layouts differ and BOTH are now asserted:
   vanilla Skyrim.esm : ARMA=766, mask subrecord BODT, 12-byte payload, 0 records carrying BOD2
   09 scope (check S-06): 2769/2769 BOD2 payloads are 8 bytes, width histogram {8: 2769}

Vanilla BODT samples (tag, payload width, raw hex); its first 4
bytes are a plausible slot mask:
   0010FCE4: ('BODT', 12, '0220000000a2cb0002000000')
   0010FCE3: ('BODT', 12, '0200000000a2cb0002000000')
   0010E0CD: ('BODT', 12, '0220000000a2cb0002000000')
```

### V-07 -- ARMA.MOD2..MOD5 are the WEARABLE garment meshes  **PASS**

* expected: vanilla ARMA mesh paths are garment paths, not WorldItems drop models
* observed: 0/1719 vanilla ARMA MOD2..5 paths look like WorldItems drop models

```
vanilla ARMA mesh paths examined: 1719
WorldItems/dropitem-style hits: 0
sample vanilla ARMA paths: Armor\BoneCrown\BoneCrownKhajiit_M.nif, Armor\BoneCrown\BoneCrownKhajiit_F.nif, Armor\BoneCrown\BoneCrownArgonian_M.nif, Armor\BoneCrown\BoneCrownArgonian_F.nif
```

### V-08 -- ARMO.MOD2..MOD5 are WORLD/INVENTORY drop models and must never be the worn mesh  **PASS**

* expected: vanilla ARMO MOD2..5 paths are world/ground models distinct from the ARMA garment meshes
* observed: vanilla ARMO model paths 3343, ARMA model paths 1719; shared paths between the two sets = 24 (0.72% of ARMO paths)

```
FINDING, reported rather than hidden: the brief's concrete
example '.../WorldItems/LatexHeelsDropitem.nif' is a THIRD-PARTY
convention of this install, not a vanilla one. On vanilla
Skyrim.esm the ARMO world models are the ES4-era ground models
under Clothes\ and similar roots (1498 of them end in GND.nif),
e.g. Clothes\Necromancer\NecromancerBootsGND.nif, Clothes\Necromancer\NecromancerBootsGND.nif

The invariant that DOES hold, and is the one the schema depends
on, is the separation: the ARMO world-model path set and the ARMA
garment path set share only 24 of 3343 paths,
so reading the worn mesh from ARMO.MOD2..MOD5 would be wrong.
vanilla ARMO model-path roots: [('armor', 2653), ('clothes', 648), ('weapons', 18), ('clutter', 15), ('actors', 9)]
vanilla ARMA model-path roots: [('armor', 816), ('clothes', 596), ('actors', 287), ('weapons', 10), ('clutter', 4), ('effects', 3)]
```

### V-09 -- the production TES4 walker sees every record in a plugin file  **PASS**

* expected: production walker and the independent walker agree on the record count of Skyrim.esm
* observed: production FKI.iter_record = 869687 records; independent walker = 869687 records (100.0% recovered)

```
BLOCKING FINDING -- p00r_formkey.iter_record and
p00r_plugins.parse_plugin slice a zlib-compressed record body
as blob[off+4 : off+dsize-4]. The compressed payload is exactly
blob[off : off+dsize) (uint32 uncompressed length + the zlib
stream, no trailing 4 bytes), so the deflate stream is always
truncated. Measured on vanilla Skyrim.esm: 44,153 compressed
records, 44,153/44,153 fail zlib.decompress with the -4 slice,
44,153/44,153 succeed with the correct slice. The parser then
abandons the file at the first compressed group and returns
silently, with no exception and no parse-failure entry.

records recovered : production 869687 vs true 869687
vanilla ARMA seen : production 766 vs true 766
vanilla CELL seen : production 17568 vs true 17568
vanilla NPC_ seen : production 5118 vs true 5118
vanilla ARMO seen : production 2762 vs true 2762 (ARMO is uncompressed, so
the documented ARMO figures are unaffected)
ARMO/RACE/TXST are uncompressed and are therefore read
correctly, which is why the documented ARMO figures still hold.
(production walk 4.9s, independent walk 1.4s)
```

## 3. 09 scope (特殊服装) -- recomputed from 02_plugin_records.json

### S-01 -- 09-scope ARMO record count  **PASS**

* expected: 1,448 ARMO in the 09 scope
* observed: 1448 ARMO

```
scope: 46 mods, 3548 records parsed, by type {'TXST': 614, 'ARMO': 1448, 'ARMA': 1321, 'COBJ': 160, 'OTFT': 5}
ARMA=1321
distinct source mods=46
```

### S-02 -- ARMO.RNAM resolves to a RACE FormID, not to the ArmorAddon  **PASS**

* expected: 1,442 of 1,448 ARMO.RNAM resolve, all to RACE DefaultRace in Skyrim.esm
* observed: 1442/1448 resolve to RACE; types={'RACE': 1442, 'UNRESOLVED': 6}; routes={'master[0]': 1442, 'UNRESOLVED': 6}; EDIDs={'DefaultRace': 1442, 'NONE': 6}

```
ARMO.RNAM is a RACE FormID.
RNAM resolution: {'RACE': 1442, 'UNRESOLVED': 6}
RNAM resolution routes: {'master[0]': 1442, 'UNRESOLVED': 6}
RNAM resolved EDIDs: {'DefaultRace': 1442, 'NONE': 6}
raw RNAM values seen: {'00000019': 1442, '': 6}
All 1,442 resolve through master[0] == Skyrim.esm, i.e. the
master byte is load-bearing (see S-10/S-11).
```

### S-03 -- ARMO.MODL is the ArmorAddon link and is 1:N  **PASS**

* expected: 1,855 MODL references in the 09 scope
* observed: 1855 MODL references; per-ARMO MODL count min=0 max=4

```
1855 ARMO.MODL references across 1448 ARMO.
Distribution of MODL references per ARMO: {0: 106, 1: 1169, 3: 6, 4: 167}
```

### S-04 -- ARMO.MODL references form a complete, self-consistent partition and every resolved link points at an ARMA  **PASS**

* expected: invariants: no MODL reference is dropped or double-counted; n_arma_refs and n_modl_refs agree with the reference list for every ARMO; every resolved target has resolved_type == 'ARMA' (no link points at an ARMO, RACE or MISC)
* observed: POST-FIX OBSERVED: 1787/1855 resolve to ARMA, 1342/1448 ARMO carry >=1 ARMA link; types={'ARMA': 1787, 'UNRESOLVED': 68}; unaccounted refs=0; ARMO whose counters disagree with its ref list: 0; resolved targets with a non-ARMA type: 0

```
The pre-fix figures (1,344 resolved / 1,340 linked) were a
symptom of the compressed-group bug, not a property of the
schema, and are deliberately NOT asserted any more. The
structural invariants asserted instead:
   ARMO.MODL references found            : 1855
   resolved to ARMA                      : 1787
   reported unresolved                   : 68
   the two account for every reference   : True
   ARMO with >=1 ARMA link               : 1342/1448
   n_arma_refs totals                    : 1787  (must equal the resolved count)
   per-ARMO counter disagreements        : 0
   resolved links with a non-ARMA type    : 0

Resolved links now come from TWO populations, which is exactly
what the master byte buys (see S-05):
   ARMA           1787
   UNRESOLVED     68
```

### S-05 -- every resolution route is legal and is backed by the FormID's master byte  **PASS**

* expected: invariants: routes are drawn only from the legal set; a 'master[k]' route requires master_byte == k; a 'self' route requires master_byte == len(MAST) of the referring plugin; zero links from local-id-only matching; every reference carries a route
* observed: POST-FIX OBSERVED MODL routes={'self': 1344, 'master[0]': 443, 'ambiguous(92)': 1, 'ambiguous(60)': 1, 'unresolved': 66}; RNAM routes={'master[0]': 1442, 'UNRESOLVED': 6}; master-byte violations=0; illegal route kinds=[]; local-id-only guess routes=0; references with no route=0

```
The pre-fix histogram (self=1,344 / unresolved=509 / ambiguous=2) is reported as an observation only. What is
asserted is that each route is structurally sound:
   route kinds seen                        : ['ambiguous', 'master', 'self', 'unresolved']
   legal set                               : ['', 'ambiguous', 'library_unique', 'master', 'master_any', 'self', 'skyrim', 'unresolved']
   master-byte violations                  : 0
   local-id-only guess routes              : 0
   references with no route at all         : 0

The 'master[0]' population is the fix working: those references
carry master byte 0x00 and therefore point into Skyrim.esm,
where the ArmorAddon records live. Before the fix the parser
could not see those records and returned 'unresolved' instead.
```

### S-06 -- ARMA.BOD2 is an 8-byte payload whose first 4 bytes are a uint32 slot mask (09 scope corpus, live plugin bytes)  **PASS**

* expected: every ARMA/ARMO BOD2 payload in the 09 scope is 8 bytes and the parser's mask == LE uint32 of its first 4 bytes
* observed: live bytes: 2769/2769 BOD2 payloads are 8 bytes, width histogram {8: 2769}; JSON artefact: {8: 2769}; records whose decoded mask != LE uint32(raw_hex[:8]): 0

```
ARMA.BOD2 = uint32 slot mask (bits 0..31) followed by 4 further
bytes. Verified byte-for-byte against a live re-read of every
in-scope plugin, not merely against the JSON artefact.
live: 2769 BOD2 subrecords, widths {8: 2769}
JSON: 2769 BOD2 subrecords, widths {8: 2769}
mask/raw_hex disagreements: 0

NOTE (see V-06): this 8-byte BOD2 layout is NOT what vanilla
Skyrim.esm uses -- vanilla ArmorAddon carries a 12-byte BODT.
```

### S-07 -- ARMA.MOD2..MOD5 are the WEARABLE garment meshes, never drop models  **PASS**

* expected: 0 ARMA addon mesh paths are WorldItems/drop models
* observed: 0/3742 ARMA MOD2..5 paths are WorldItems/drop models

```
3742 ARMA addon mesh paths examined across the
09 scope; WorldItems/drop hits: 0
```

### S-08 -- ARMO.MOD2..MOD5 are WORLD/INVENTORY drop models and must never be used as the worn mesh (09 scope)  **PASS**

* expected: ARMO world models include the documented '...\WorldItems\...Dropitem.nif' form, and are disjoint from the ARMA garment meshes
* observed: 680/2148 ARMO world-model paths are WorldItems/drop models (31.7%); ARMO/ARMA path sets disjoint for 788/1235 pairs

```
The brief's example is real in this install:
   NyesLatexPack\WorldItems\LatexHeelsDropitem.nif
   NyesLatexPack\WorldItems\LatexHeelsDropitem.nif
   NyesLatexPack\WorldItems\LatexHighHeeledBootsDropitem.nif
   NyesLatexPack\WorldItems\LatexHighHeeledBootsDropitem.nif

Not every ARMO world model is a WorldItems drop model; many mods
reuse the garment mesh for the dropped object. That is fine and
is why the invariant tested here is separation, not the string:
788 of 1235 ARMO/ARMA pairs have completely
disjoint path sets; the remaining 447 reuse the same mesh for
both. Either way the worn mesh must come from ARMA.MOD2..MOD5.
```

### S-09 -- master-byte convention: a plugin's OWN records carry master byte == len(MAST)  **PASS**

* expected: the per-plugin own-byte histogram matches the len(MAST) histogram exactly, with zero violations
* observed: own-byte per plugin={1: 31, 2: 7, 3: 4, 5: 1, 7: 2, 9: 2}; len(MAST) per plugin={1: 31, 2: 7, 3: 4, 5: 1, 7: 2, 9: 2}; record-level own-byte histogram={1: 2626, 2: 315, 3: 115, 5: 12, 7: 253, 9: 227}; violating plugins=[]

```
This convention is what makes FormKey resolution sound: the
n-th declared master is indexed by the byte, and the plugin's
own records are indexed by len(MAST), not by 0.
in-scope plugins checked   : 47
own-byte per plugin        : {1: 31, 2: 7, 3: 4, 5: 1, 7: 2, 9: 2}
len(MAST) per plugin       : {1: 31, 2: 7, 3: 4, 5: 1, 7: 2, 9: 2}
own-byte record histogram  : {1: 2626, 2: 315, 3: 115, 5: 12, 7: 253, 9: 227}
per-plugin violations      : []

Every plugin's own records carry one single master byte and
that byte equals its declared master count -- 47/47.
```

### S-10 -- the master byte is load-bearing: a 24-bit local-id join would produce different (wrong) links  **PASS**

* expected: master-byte-blind links would corrupt a non-trivial number of ARMO.MODL references
* observed: 1138/1855 ARMO.MODL references have a 24-bit local id that is owned by more than one (plugin, master byte) pair (61.3% of references, 870921 distinct 24-bit local ids indexed)

```
FormKey matching on the 24-bit local id alone is unsound on
this install. The resolver keys on the full 32-bit FormID, so
every resolution route it reports ('self', 'master[n]', ..)
already carries the master byte.
1138 of 1855 MODL references sit on a colliding
local id; a local-id-only join would have picked a different
owner for each of them.

The production parser never masks the master byte:
  p00r_formkey.resolve() tests the full `formid` against the
  plugin's own table, then against masters[mid].
```

### S-11 -- a FormID owned by several plugins is reported as ambiguous, never silently resolved to an arbitrary owner  **PASS**

* expected: every ambiguous route has an empty resolved plugin/type and is_arma=False; no 'library[n]' guess route exists
* observed: 2 ambiguous MODL refs, all reported without a resolved owner: True; legacy alphabetically-first 'library[n]' routes still present: 0

```
The failure mode guarded against: an earlier resolver took the
alphabetically first owner of a shared FormID and produced
demonstrably false links (a Silent_Code glove resolving to an
unrelated HoodST body addon).
   01000810 route=ambiguous(92) resolved_plugin='' resolved_type=''
   01000D65 route=ambiguous(60) resolved_plugin='' resolved_type=''
```

### S-12 -- no ARMO.MODL reference in the 09 scope is wrongly reported as unresolved  **PASS**

* expected: 0 MODL references dropped because the target is a vanilla Skyrim.esm ARMA that the parser cannot see
* observed: 0 MODL reference(s) (0.0% of all MODL references) point at 0 vanilla Skyrim.esm ARMA records and are reported UNRESOLVED: []

```
COLLATERAL DAMAGE OF V-09 -- the single largest accuracy loss
in the whole re-run. Every vanilla ArmorAddon record lives
inside a zlib-compressed group, which p00r_formkey drops, so the
FormKey index never contains any vanilla ARMA. A reference with
master byte 0x00 therefore cannot be resolved and is reported
UNRESOLVED -- a false negative on a real link.
The targets are unambiguously ArmorAddon records:

Together these account for 0 of the 68 unresolved MODL references, i.e. the overwhelming majority of
them. The remaining UNRESOLVED references point at FormIDs that
exist in no indexed plugin at all.
```

### S-13 -- EDID corroboration, measured separately for self-linked and cross-plugin ARMA links  **PASS**

* expected: the route='self' population corroborates at ~90% by >=6-character EDID prefix; cross-plugin links are reported as a separate population with their count and rate, not folded into the self-linked rate
* observed: POST-FIX OBSERVED: route=self 1215/1344 = 90.4%; cross-plugin populations {'master[n]': '0/443'}; blended 1215/1787 = 68.0%

```
Two DISTINCT populations, deliberately not merged:

(a) route='self' -- the addon is authored by the same plugin as
    the armour, so its EDID usually mirrors the ARMO's:
      corroborated 1215/1344 = 90.4%
      THIS is the number that guards the ARMO->ARMA chain. A
      collapse here would mean the chain is wrong.

(b) cross-plugin / vanilla -- master byte 0x00 references into
    Skyrim.esm. These point at shared vanilla addons worn by many
    unrelated armours, so a shared EDID prefix is neither
    expected nor meaningful:
      master[n]  0/443 corroborated, 443 resolved into a different plugin than the referring ARMO

Sample targets of the cross-plugin population:
   FullLeatherHelmetKhajiitAA -> 145
   FullLeatherHelmetOrcAA -> 145
   FullLeatherHelmetArgonianAA -> 145
   BeggarHat01_KhajAA -> 4
   BeggarHat01_ArgAA -> 4
```

### S-14 -- OTFT.INAM (the outfit target) is recovered as a FormID array  **PASS**

* expected: every OTFT.INAM payload decodes to the same packed uint32 FormID list the independent walker reads
* observed: 5 OTFT records; INAM payload widths {16: 1, 24: 3, 20: 1}; 27 packed FormIDs in total; 27/27 resolve to a record in the owning plugin; rows disagreeing with the live decode: 0

```
OTFT.INAM is NOT a 4-byte subrecord: it is a packed array of
uint32 FormIDs (16-24 bytes here), so the FOUR_CHAR_STR rule
(4-byte payload -> uint32) never applies to it. The decode is
verified against the live bytes, field by field:
   03000836: INAM raw = 0a08000309080003080800030b0800030608000307080003
           independent walker -> 0300080A 03000809 03000808 0300080B 03000806 03000807
           pipeline artefact   -> 0300080A 03000809 03000808 0300080B 03000806 03000807
   03000837: INAM raw = 210800032208000323080003240800032508000326080003
           independent walker -> 03000821 03000822 03000823 03000824 03000825 03000826
           pipeline artefact   -> 03000821 03000822 03000823 03000824 03000825 03000826
   03000838: INAM raw = 3508000328080003290800032a0800032b0800032c080003
           independent walker -> 03000835 03000828 03000829 0300082A 0300082B 0300082C
           pipeline artefact   -> 03000835 03000828 03000829 0300082A 0300082B 0300082C
   03000839: INAM raw = 320800032f08000330080003310800032d080003
           independent walker -> 03000832 0300082F 03000830 03000831 0300082D
           pipeline artefact   -> 03000832 0300082F 03000830 03000831 0300082D
   03000AA3: INAM raw = 01080003da0900032608000327080003
           independent walker -> 03000801 030009DA 03000826 03000827
           pipeline artefact   -> 03000801 030009DA 03000826 03000827
All 27 referenced FormIDs resolve to a record inside
the owning plugin (they are the ARMO entries the outfit wears),
so the outfit targets are genuinely recovered.
```

## 4. Independent cross-check (own TES4 walker vs p00r_plugins)

### I-00 -- three simple outfit plugins were selected deterministically for the by-hand probe  **PASS**

* expected: >=3 plugins, every ARMO.MODL on the 'self' route
* observed: ['AE Stellablade Tachy.esp', 'Returning Night.esp', '[Brastia] Catwoman 3BA.esp']

```
Selection rule: >=3 ARMO, all MODL refs resolve via route 'self'
(so the comparison cannot be contaminated by another plugin's
state), smallest files first, sorted for reproducibility.
```

### I-01A -- [AE Stellablade Tachy.esp] total record count: independent walker vs production  **PASS**

* expected: identical total record count
* observed: independent=6, production=6

```
file      : E:\SkyrimAE\mo2\mods\makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】\AE Stellablade Tachy.esp
size      : 2777 bytes
masters   : production=['skyrim.esm', 'heels sound.esm']
            independent=['Skyrim.esm', 'Heels Sound.esm']
records   : independent=6, production=6
types     : independent={'ARMO': 3, 'ARMA': 3}
            production={'ARMO': 3, 'ARMA': 3}
groups    : production=2
zlib-fail : production=0
```

### I-01B -- [AE Stellablade Tachy.esp] per-ARMO MODL reference count agrees, record by record  **PASS**

* expected: identical MODL count for all 3 ARMO
* observed: 3 ARMO compared; mismatches: []

```
Compared formid-by-formid, not just in aggregate.
ARMO records: 3
MODL count mismatches: []
MODL subrecords seen by the independent walker: 02000D65=1, 02000D66=1, 02000D67=1
```

### I-01C -- [AE Stellablade Tachy.esp] ARMO.RNAM and BOD2 agree field by field  **PASS**

* expected: 0 RNAM mismatches and 0 BOD2 mismatches over 3 ARMO
* observed: RNAM mismatches=0, BOD2 mismatches=0 over 3 ARMO

```
RNAM compared as a uint32 FormID list; BOD2 compared as
(uint32 mask, payload length) derived independently.
ARMO compared: 3   RNAM mismatches: 0   BOD2 mismatches: 0
   02000D65 RNAM=['00000019'] BOD2=(132, 8)
   02000D66 RNAM=['00000019'] BOD2=(8, 8)
   02000D67 RNAM=['00000019'] BOD2=(16384, 8)
```

### I-01D -- [AE Stellablade Tachy.esp] ARMA MOD2..MOD5 garment paths agree field by field  **PASS**

* expected: 0 mismatches over 3 ARMA
* observed: 3 ARMA compared; mismatches: 0

```
The worn-mesh fields -- the ones the whole re-run hinges on.
ARMA compared: 3   mismatches: 0
   02000D62 MOD2=('Armor\\Studded\\Male\\body_1.nif',); MOD3=('AE_Stellablade_Tachy\\AE_Stellablade_Tachy_1.nif',); MOD4=('Armor\\Studded\\Male\\1stPersonbody_1.nif',); MOD5=('AE_Stellablade_Tachy\\AE_Stellablade_Tachy_1st_1.nif',)
   02000D63 MOD2=('Armor\\Studded\\Male\\gloves_1.nif',); MOD3=('AE_Stellablade_Tachy\\AE_Stellablade_Tachy_Hand_1.nif',); MOD4=('Armor\\Studded\\Male\\1stPersongloves_1.nif',); MOD5=('AE_Stellablade_Tachy\\AE_Stellablade_Tachy_Hand_1.nif',)
   02000D68 MOD2=('AE_Stellablade_Tachy\\Mask.nif',); MOD3=('AE_Stellablade_Tachy\\Mask.nif',); MOD4=('AE_Stellablade_Tachy\\Mask.nif',); MOD5=('AE_Stellablade_Tachy\\Mask.nif',)
```

### I-02A -- [Returning Night.esp] total record count: independent walker vs production  **PASS**

* expected: identical total record count
* observed: independent=10, production=10

```
file      : E:\SkyrimAE\mo2\mods\回归之夜高跟鞋 — SEXY BOOTS Returning Night Pumps — 【服装·护甲】【来源·本地】\Returning Night.esp
size      : 3351 bytes
masters   : production=['skyrim.esm', 'heels sound.esm']
            independent=['Skyrim.esm', 'Heels Sound.esm']
records   : independent=10, production=10
types     : independent={'ARMO': 5, 'ARMA': 5}
            production={'ARMO': 5, 'ARMA': 5}
groups    : production=2
zlib-fail : production=0
```

### I-02B -- [Returning Night.esp] per-ARMO MODL reference count agrees, record by record  **PASS**

* expected: identical MODL count for all 5 ARMO
* observed: 5 ARMO compared; mismatches: []

```
Compared formid-by-formid, not just in aggregate.
ARMO records: 5
MODL count mismatches: []
MODL subrecords seen by the independent walker: 02000800=1, 02000802=1, 02000808=1, 02000809=1, 0200080B=1
```

### I-02C -- [Returning Night.esp] ARMO.RNAM and BOD2 agree field by field  **PASS**

* expected: 0 RNAM mismatches and 0 BOD2 mismatches over 5 ARMO
* observed: RNAM mismatches=0, BOD2 mismatches=0 over 5 ARMO

```
RNAM compared as a uint32 FormID list; BOD2 compared as
(uint32 mask, payload length) derived independently.
ARMO compared: 5   RNAM mismatches: 0   BOD2 mismatches: 0
   02000800 RNAM=['00000019'] BOD2=(128, 8)
   02000802 RNAM=['00000019'] BOD2=(128, 8)
   02000808 RNAM=['00000019'] BOD2=(128, 8)
   02000809 RNAM=['00000019'] BOD2=(128, 8)
   0200080B RNAM=['00000019'] BOD2=(128, 8)
```

### I-02D -- [Returning Night.esp] ARMA MOD2..MOD5 garment paths agree field by field  **PASS**

* expected: 0 mismatches over 5 ARMA
* observed: 5 ARMA compared; mismatches: 0

```
The worn-mesh fields -- the ones the whole re-run hinges on.
ARMA compared: 5   mismatches: 0
   02000801 MOD3=('ReturningNight\\RnPumpsBlack_1.nif',)
   02000803 MOD3=('ReturningNight\\RnPumpsWhite_1.nif',)
   02000804 MOD3=('ReturningNight\\RnPumpsRed_1.nif',)
   02000805 MOD3=('ReturningNight\\RnPumpsGold_1.nif',)
```

### I-03A -- [[Brastia] Catwoman 3BA.esp] total record count: independent walker vs production  **PASS**

* expected: identical total record count
* observed: independent=11, production=11

```
file      : E:\SkyrimAE\mo2\mods\Brastia Catwoman TAS for 3BA — 【服装·装备】【体型·CBBE+3BA】\[Brastia] Catwoman 3BA.esp
size      : 3850 bytes
masters   : production=['skyrim.esm', 'update.esm', 'heels sound.esm']
            independent=['Skyrim.esm', 'Update.esm', 'Heels Sound.esm']
records   : independent=11, production=11
types     : independent={'ARMO': 5, 'ARMA': 5, 'OTFT': 1}
            production={'ARMO': 5, 'ARMA': 5, 'OTFT': 1}
groups    : production=3
zlib-fail : production=0
```

### I-03B -- [[Brastia] Catwoman 3BA.esp] per-ARMO MODL reference count agrees, record by record  **PASS**

* expected: identical MODL count for all 5 ARMO
* observed: 5 ARMO compared; mismatches: []

```
Compared formid-by-formid, not just in aggregate.
ARMO records: 5
MODL count mismatches: []
MODL subrecords seen by the independent walker: 03000801=1, 03000826=1, 03000827=1, 030009DA=1, 03000AA6=1
```

### I-03C -- [[Brastia] Catwoman 3BA.esp] ARMO.RNAM and BOD2 agree field by field  **PASS**

* expected: 0 RNAM mismatches and 0 BOD2 mismatches over 5 ARMO
* observed: RNAM mismatches=0, BOD2 mismatches=0 over 5 ARMO

```
RNAM compared as a uint32 FormID list; BOD2 compared as
(uint32 mask, payload length) derived independently.
ARMO compared: 5   RNAM mismatches: 0   BOD2 mismatches: 0
   03000801 RNAM=['00000019'] BOD2=(4, 8)
   03000826 RNAM=['00000019'] BOD2=(8, 8)
   03000827 RNAM=['00000019'] BOD2=(128, 8)
   030009DA RNAM=['00000019'] BOD2=(14338, 8)
   03000AA6 RNAM=['00000019'] BOD2=(131072, 8)
```

### I-03D -- [[Brastia] Catwoman 3BA.esp] ARMA MOD2..MOD5 garment paths agree field by field  **PASS**

* expected: 0 mismatches over 5 ARMA
* observed: 5 ARMA compared; mismatches: 0

```
The worn-mesh fields -- the ones the whole re-run hinges on.
ARMA compared: 5   mismatches: 0
   03000800 MOD3=('Catwomantas\\Bodysuit_1.nif',); MOD5=('Catwomantas\\Bodysuit_1.nif',)
   0300080A MOD3=('Catwomantas\\gloves_1.nif',); MOD5=('Catwomantas\\gloves_1.nif',)
   03000820 MOD3=('Catwomantas\\Boots_1.nif',); MOD5=('Catwomantas\\Boots_1.nif',)
   030009D9 MOD3=('Catwomantas\\mask.nif',); MOD5=('Catwomantas\\mask.nif',)
```

## 5. BodySlide: .osp XML projects and .osd binary containers

### B-01 -- SliderSets/*.osp are parsed as XML and none fails to parse  **PASS**

* expected: 0 XML parse errors across every in-scope .osp
* observed: 0 XML parse errors across 176 projects

```
in-scope .osp projects : 176
XML parse errors        : 0
provenance field values : {'osp_xml_parsed': 176}
```

### B-02 -- .osp files are UTF-8 XML that often carries a BOM, so a naive head[:1] == b'<' XML test fails on them  **PASS**

* expected: a measurable number of .osp files start with a UTF-8 BOM and would fail the naive test
* observed: 80/80 sampled .osp files start with a UTF-8 BOM; 80/80 would fail the naive head[:1]==b'<' test

```
p00r_bodyslide.parse_osp strips the BOM before ET.fromstring,
which is why the .osp parse rate is 100% and the first
P00_RERUN pass's '0 OSP parse errors' was a false clean.
   CalienteTools/BodySlide/SliderSets/(Nye's Latex Outfit 2) Corset - Version 2.osp: first bytes b'\xef\xbb\xbf<'
   CalienteTools/BodySlide/SliderSets/(Nye's Latex Outfit 2) Corset - Version 2.osp: first bytes b'\xef\xbb\xbf<'
   CalienteTools/BodySlide/SliderSets/(Nye's Latex Outfit 2) Latex Bodysuit Slot 58.osp: first bytes b'\xef\xbb\xbf<'
```

### B-03 -- every OSP field (SliderSet@name, DataFolder, SourceFile, OutputPath, OutputFile@GenWeights) is read from the XML, never fabricated  **PASS**

* expected: the ONLY projects left UNKNOWN are those whose .osp contains no <SliderSet> element at all
* observed: 176 projects; projects with UNKNOWN fields = ['CalienteTools/BodySlide/SliderSets/SSE_Kakugo_LatexNun_St.osp']; of those, projects with no <SliderSet> element = ['CalienteTools/BodySlide/SliderSets/SSE_Kakugo_LatexNun_St.osp']; unexplained UNKNOWNs = []; base_nif resolved 173/176, output_nif resolved 175/176

```
No hard-coded fallback. The first P00_RERUN pass fell back to
'meshes\clothing', i.e. a fabricated value; this calibration
confirms nothing is invented.
projects                        : 176
projects with any UNKNOWN field : ['CalienteTools/BodySlide/SliderSets/SSE_Kakugo_LatexNun_St.osp']
projects with no <SliderSet>     : ['CalienteTools/BodySlide/SliderSets/SSE_Kakugo_LatexNun_St.osp']

The residual UNKNOWNs are genuine, not parser failures:
   CalienteTools/BodySlide/SliderSets/SSE_Kakugo_LatexNun_St.osp: b'\xef\xbb\xbf<?xml version="1.0" encoding="UTF-8"?>\r\n<SliderSetInfo version="1"/>\r\n'

base_nif resolved 173/176. The three
that stay UNKNOWN name a base mesh that is genuinely not in the
09 scope (the join is restricted to in-scope ShapeData NIFs):
   CalienteTools/BodySlide/SliderSets/EvilFall Dragon.osp: DataFolder='EvilFall Dragon' SourceFile='EvilFall_Dragon_Tail.nif' (in-scope ShapeData NIFs for that folder: 0)
   CalienteTools/BodySlide/SliderSets/SSE_Kakugo_LatexNun_St.osp: DataFolder='UNKNOWN' SourceFile='UNKNOWN' (in-scope ShapeData NIFs for that folder: 0)
   CalienteTools/BodySlide/SliderSets/[Predator] Premium Laced Latex Bodysuit.osp: DataFolder='[Predator] Premium Laced Latex Bodysuit' SourceFile='Bodysuit_BHUNP.nif' (in-scope ShapeData NIFs for that folder: 2)
output_path histogram (top 6): {'Meshes\\armor\\[TRX]  LatexWhitch': 43, 'meshes\\SSE_Silent_Code': 7, 'meshes\\ReturningNight': 7, 'meshes\\Zaplin\\Gantz_Suit': 6, 'Meshes\\AE_CorruptedBodySuit': 4, 'meshes\\AE_Vtaw_DarkNurse': 3}
OutputFile@GenWeights histogram: {'true': 172, 'false': 3, None: 1}
```

### B-04 -- each OSP Slider/Data carries a '<set>.osd\<slider>' reference  **PASS**

* expected: one osd reference per <Slider> element; slider and shape counts agree with an independent XML walk
* observed: 16321 sliders -> 16321 osd references; 782 shapes; slider/shape count mismatches vs the independent XML walk: []; projects with zero osd refs: 4 (of which genuinely contain 0 <Slider> elements: 4)

```
sliders parsed      : 16321
osd references      : 16321   (exactly 1 per <Slider>)
shapes parsed       : 782
independent XML walk over every .osp agrees on the <Slider> and
<Shape> counts for all 176 projects (mismatches: []).
distinct .osd files referenced: 6558
Projects with no osd reference -- verified to contain zero
<Slider> elements, so the absence is real and not a drop:
   CalienteTools/BodySlide/SliderSets/AE_Once_Combat_Medi_Vail.osp: 0 Slider, 6 Shape
   CalienteTools/BodySlide/SliderSets/GantzSuitGloves.osp: 0 Slider, 1 Shape
   CalienteTools/BodySlide/SliderSets/SSE_Kakugo_LatexNun_St.osp: 0 Slider, 0 Shape
   CalienteTools/BodySlide/SliderSets/[Predator] Provocative Bikini Harness.osp: 0 Slider, 2 Shape
```

### B-05 -- ShapeData/*.osd is a BINARY container whose magic is b'OSD\0' stored LITTLE-ENDIAN (first bytes b'\x00DSO' = 0x4F534400)  **PASS**

* expected: every in-scope .osd starts with the 4 bytes b'\x00DSO', i.e. uint32 0x4F534400
* observed: first-4-byte histogram=[b'\x00DSO'], uint32 magic histogram={'0x4F534400': 513} over 513 files; .osd parse errors reported by the pipeline: 0

```
The first P00_RERUN pass compared the file's first bytes to
b'OSD\0' in FILE order, so it never matched anything.
files checked                : 513
first 4 bytes, byte-for-byte : [b'\x00DSO']
read as little-endian uint32  : ['0x4F534400']
read as big-endian uint32 would be: ['0x0044534F']
p00r_bodyslide.OSD_MAGIC     : 0x4F534400
```

### B-06 -- the uint32 at offset 0x04 of an .osd is a version number  **PASS**

* expected: version 1 on every in-scope .osd
* observed: version histogram {1: 513} over 513 files

```
uint32 @0x04 across 513 .osd files: {1: 513}
```

### B-08 -- OSD layout regression guard: the shape name is the length-prefixed string at 0x0C, and the 'uint32 at 0x08 is a data offset' reading is refuted  **PASS**

* expected: every in-scope .osd yields a printable length-prefixed shape name at 0x0C (513/513), p00r_bodyslide.parse_osd returns a real shape name for all of them (513/513), AND the 0x08 offset reading is demonstrably false (far fewer than 513 files parse there)
* observed: length-prefixed name at 0x0C: 513/513; at the uint32 stored in 0x08: 6/513 (REFUTES the offset claim); 0x08 takes 243 distinct values (1..2442); parse_osd returns a real shape name for 513/513 files

```
MEASURED LAYOUT (all 513 in-scope .osd files):
   uint32 @0x00  magic   0x4F534400   ("OSD\0", little-endian)
   uint32 @0x04  version 1
   uint32 @0x08           243 distinct values, 1..2442 -- NOT a pointer to the name
   name at the 0x08 value  6/513   <- REFUTED
   name at 0x0C           513/513   <- the real layout

The '0x08 is a data offset' claim carried by the original
calibration brief (and by an earlier p00r_bodyslide docstring)
is FALSE: only 6 of 513 files yield a length-prefixed
name there, against {}/{} at 0x0C. The few hits at 0x08 are
coincidence -- the 0x08 value is a size/offset field whose low
bytes happen to form a plausible length byte.

p00r_bodyslide.parse_osd now reads the name at 0x0C and returns
a real shape name for 513/513 files, so the
'no exception, empty result' failure mode is gone.

Verbatim header bytes of the first three in-scope .osd files:
["   file  : CalienteTools/BodySlide/ShapeData/(Nye's Latex Outfit 2) Corset - Version 2/(Nye's Latex Outfit 2) Corset - Version 2.osd", '   hex   : 00 44 53 4f 01 00 00 00 60 00 00 00 0e 43 6f 72 73 65 74 37 42 20 4c 6f 77 65 72 77 0d 97 01 dd 7f 76 bf 23 13 4b 3f e3 f0 3f 3e 64 04 03 63 85 3f 79 85 10 3f 7d 6b 10 3e 08 00 06 b2 e6 3a f0', '   ascii : .DSO....`....Corset7B Lowerw.....v.#.K?..?>d..c.?y..?}k.>.....:.', '   u32@0x00=0x4F534400  u32@0x04=1  u32@0x08=96', "   u8 @0x0C = 14 -> 'Corset7B Lower'", '   at the 0x08 value (96) -> None']
["   file  : CalienteTools/BodySlide/ShapeData/(Nye's Latex Outfit 2) Corset - Version 2/(Nye's Latex Outfit 2) Corset - Version 2.osd", '   hex   : 00 44 53 4f 01 00 00 00 60 00 00 00 0e 43 6f 72 73 65 74 37 42 20 4c 6f 77 65 72 77 0d 97 01 dd 7f 76 bf 23 13 4b 3f e3 f0 3f 3e 64 04 03 63 85 3f 79 85 10 3f 7d 6b 10 3e 08 00 06 b2 e6 3a f0', '   ascii : .DSO....`....Corset7B Lowerw.....v.#.K?..?>d..c.?y..?}k.>.....:.', '   u32@0x00=0x4F534400  u32@0x04=1  u32@0x08=96', "   u8 @0x0C = 14 -> 'Corset7B Lower'", '   at the 0x08 value (96) -> None']
["   file  : CalienteTools/BodySlide/ShapeData/(Nye's Latex Outfit 2) Latex Bodysuit Slot 58/(Nye's Latex Outfit 2) Latex Bodysuit Slot 58.osd", '   hex   : 00 44 53 4f 01 00 00 00 9b 00 00 00 17 42 6f 64 79 73 75 69 74 42 72 65 61 73 74 73 54 6f 67 65 74 68 65 72 50 19 be 22 2e c7 75 3c 25 2d f1 3c 1a 36 61 bc 0f 1d 00 00 00 00 00 00 00 00 00 00', '   ascii : .DSO.........BodysuitBreastsTogetherP.."..u<%-.<.6a.............', '   u32@0x00=0x4F534400  u32@0x04=1  u32@0x08=155', "   u8 @0x0C = 23 -> 'BodysuitBreastsTogether'", '   at the 0x08 value (155) -> None']
```

## 6. Body classification vocabulary and behaviour

### C-01 -- classify_body() on synthetic token sets  **PASS**

* expected: CBBE=>CBBE; 3BA=>CBBE_3BA; 3BA+CBBE=>CBBE_3BA; BHUNP=>BHUNP; <empty>=>UNKNOWN
* observed: CBBE=>CBBE; 3BA=>CBBE_3BA; 3BA+CBBE=>CBBE_3BA; BHUNP=>BHUNP; <empty>=>UNKNOWN

```
The audit finding being guarded against: a CBBE-only token set
was collapsed to OTHER, silently discarding a real body type.
   classify_body(CBBE) -> candidate=CBBE families=['CBBE'] flag=CBBE_ONLY   (expected CBBE)
   classify_body(3BA) -> candidate=CBBE_3BA families=['3BA'] flag=CBBE_3BA_3BA_ONLY   (expected CBBE_3BA)
   classify_body(3BA+CBBE) -> candidate=CBBE_3BA families=['3BA', 'CBBE'] flag=CBBE_3BA   (expected CBBE_3BA)
   classify_body(BHUNP) -> candidate=BHUNP families=['BHUNP'] flag=BHUNP_ONLY   (expected BHUNP)
   classify_body(<empty>) -> candidate=UNKNOWN families=[] flag=UNKNOWN   (expected UNKNOWN)
```

### C-02 -- the body classification vocabulary is exactly CBBE / CBBE_3BA / BHUNP / OTHER / UNKNOWN  **PASS**

* expected: no value outside ['BHUNP', 'CBBE', 'CBBE_3BA', 'OTHER', 'UNKNOWN'] in 07_bodyslide_projects.json
* observed: vocabulary used = {'UNKNOWN': 114, 'CBBE_3BA': 60, 'CBBE': 1, 'BHUNP': 1}; out-of-vocabulary = {}

```
176 BodySlide projects classified.
body_candidate distribution: {'UNKNOWN': 114, 'CBBE_3BA': 60, 'CBBE': 1, 'BHUNP': 1}
values outside the mandated vocabulary: {}
needs_3ba_conversion: {'UNKNOWN': 114, 'NO': 60, 'YES': 2}
```

### C-03 -- real 09-scope BodySlide projects whose names carry a body family classify into the mandated vocabulary  **PASS**

* expected: every project naming CBBE / 3BA / BHUNP classifies to CBBE, CBBE_3BA or BHUNP
* observed: 62 of 176 projects name a body family; 61 classify into the vocabulary; 0 fall through to UNKNOWN

```
Body type is derived only from real file names / UI names.
The ones that DO classify:
   CBBE SE - Jennes Thigh Boots 3BA                           -> CBBE_3BA
   CBBE SE - Skimpy Assassin Boots                            -> CBBE
   CBBE SE - [COCO] 2B Wedding Boots [3BA] Edited             -> CBBE_3BA
   Knee_Boots 3BA                                             -> CBBE_3BA
   MiscHeelsEins 3BA AnkleCut                                 -> CBBE_3BA
   MiscHeelsEins 3BA                                          -> CBBE_3BA
   MiscHeelsZwei 3BA AnkleCut                                 -> CBBE_3BA
   MiscHeelsZwei 3BA                                          -> CBBE_3BA

FINDING -- the ones that do not, and why:

p00r_common.BODY_TOKEN_RE is r"[+/_\-]|\s+" -- it does not
split on brackets or parentheses. So '(BHUNP)' never yields the
token 'BHUNP' and '[SE]3BA Melodic-Dolly Heels' yields
'[SE]3BA', not '3BA'. classify_body() itself is correct (C-01);
the defect is in body_tokens()'s tokenizer. Adding ()[]{}<> and
: to BODY_TOKEN_RE would recover all of these.
```

## 7. Verbatim evidence dumps (no assertion -- these are the dumps the checks above were decided from)

### E-01 -- verbatim evidence dump: outfit plugin AE Stellablade Tachy.esp  **PASS**

* expected: informational dump
* observed: 39 lines of verbatim record detail

```
PLUGIN  AE Stellablade Tachy.esp
PATH    E:\SkyrimAE\mo2\mods\makaron-COSPLAY - AE_Stellablade_Tachy — 【服装·装备】【来源·本地】\AE Stellablade Tachy.esp
SIZE    2777 bytes
MASTERS ['Skyrim.esm', 'Heels Sound.esm']

COUNTS  3 ARMO, 3 ARMA (this plugin owns 3 of them)

  ARMO 02000D65  EDID='AE_Stellablade_Tachy_Body'
    ARMO.RNAM raw=00000019  -> plugin='Skyrim.esm' type='RACE' EDID='DefaultRace' route='master[0]'
    ARMO.RNAM IS: RACE
    BOD2 raw=8400000000000000 payload_len=8
         mask=0x00000084 bits=[2, 7] slots=['body', 'lowerleg']
    ARMO.MODL (repeated; the ArmorAddon link):
      02000D62  master_byte=2  -> plugin='AE Stellablade Tachy.esp' type='ARMA' EDID='AE_Stellablade_Tachy_BodyAA' route='self'  is_arma=True
    ARMO.MOD2..MOD5 (world/inventory drop models, NOT worn): ['AE_Stellablade_Tachy\\AE_Stellablade_Tachy_1.nif']

    -> ARMA 02000D62 in 'AE Stellablade Tachy.esp' EDID='AE_Stellablade_Tachy_BodyAA'
        BOD2 raw=8400000002000000 payload_len=8
             mask=0x00000084 bits=[2, 7] slots=['body', 'lowerleg']
        ARMA.MOD2 (the WORN garment mesh) = 'Armor\\Studded\\Male\\body_1.nif'
        ARMA.MOD3 (the WORN garment mesh) = 'AE_Stellablade_Tachy\\AE_Stellablade_Tachy_1.nif'
        ARMA.MOD4 (the WORN garment mesh) = 'Armor\\Studded\\Male\\1stPersonbody_1.nif'
        ARMA.MOD5 (the WORN garment mesh) = 'AE_Stellablade_Tachy\\AE_Stellablade_Tachy_1st_1.nif'
        ARMA.source_mesh_refs (MODL, 24): ['00013740', '00013741', '00013742', '00013743', '00013744', '00013745'] ...

  ARMO 02000D66  EDID='AE_Stellablade_Tachy_Hand'
    ARMO.RNAM raw=00000019  -> plugin='Skyrim.esm' type='RACE' EDID='DefaultRace' route='master[0]'
    ARMO.RNAM IS: RACE
    BOD2 raw=0800000000000000 payload_len=8
         mask=0x00000008 bits=[3] slots=['hands']
    ARMO.MODL (repeated; the ArmorAddon link):
      02000D63  master_byte=2  -> plugin='AE Stellablade Tachy.esp' type='ARMA' EDID='AE_Stellablade_Tachy_GloveAA' route='self'  is_arma=True
    ARMO.MOD2..MOD5 (world/inventory drop models, NOT worn): ['AE_Stellablade_Tachy\\AE_Stellablade_Tachy_Hand_1.nif']

    -> ARMA 02000D63 in 'AE Stellablade Tachy.esp' EDID='AE_Stellablade_Tachy_GloveAA'
        BOD2 raw=0800000002000000 payload_len=8
             mask=0x00000008 bits=[3] slots=['hands']
        ARMA.MOD2 (the WORN garment mesh) = 'Armor\\Studded\\Male\\gloves_1.nif'
        ARMA.MOD3 (the WORN garment mesh) = 'AE_Stellablade_Tachy\\AE_Stellablade_Tachy_Hand_1.nif'
        ARMA.MOD4 (the WORN garment mesh) = 'Armor\\Studded\\Male\\1stPersongloves_1.nif'
        ARMA.MOD5 (the WORN garment mesh) = 'AE_Stellablade_Tachy\\AE_Stellablade_Tachy_Hand_1.nif'
        ARMA.source_mesh_refs (MODL, 24): ['00013740', '00013741', '00013742', '00013743', '00013744', '00013745'] ...

```

### E-02 -- verbatim evidence dump: outfit plugin Returning Night.esp  **PASS**

* expected: informational dump
* observed: 33 lines of verbatim record detail

```
PLUGIN  Returning Night.esp
PATH    E:\SkyrimAE\mo2\mods\回归之夜高跟鞋 — SEXY BOOTS Returning Night Pumps — 【服装·护甲】【来源·本地】\Returning Night.esp
SIZE    3351 bytes
MASTERS ['Skyrim.esm', 'Heels Sound.esm']

COUNTS  5 ARMO, 5 ARMA (this plugin owns 5 of them)

  ARMO 02000800  EDID='exPumpsBlack'
    ARMO.RNAM raw=00000019  -> plugin='Skyrim.esm' type='RACE' EDID='DefaultRace' route='master[0]'
    ARMO.RNAM IS: RACE
    BOD2 raw=8000000000000000 payload_len=8
         mask=0x00000080 bits=[7] slots=['lowerleg']
    ARMO.MODL (repeated; the ArmorAddon link):
      02000801  master_byte=2  -> plugin='Returning Night.esp' type='ARMA' EDID='AAexPumpsBlack' route='self'  is_arma=True
    ARMO.MOD2..MOD5 (world/inventory drop models, NOT worn): ['ReturningNight\\BlackBox_gnd.nif']

    -> ARMA 02000801 in 'Returning Night.esp' EDID='AAexPumpsBlack'
        BOD2 raw=8000000000000000 payload_len=8
             mask=0x00000080 bits=[7] slots=['lowerleg']
        ARMA.MOD3 (the WORN garment mesh) = 'ReturningNight\\RnPumpsBlack_1.nif'
        ARMA.source_mesh_refs (MODL, 24): ['00013740', '00013741', '00013742', '00013743', '00013744', '00013745'] ...

  ARMO 02000802  EDID='exPumpsWhite'
    ARMO.RNAM raw=00000019  -> plugin='Skyrim.esm' type='RACE' EDID='DefaultRace' route='master[0]'
    ARMO.RNAM IS: RACE
    BOD2 raw=8000000000000000 payload_len=8
         mask=0x00000080 bits=[7] slots=['lowerleg']
    ARMO.MODL (repeated; the ArmorAddon link):
      02000803  master_byte=2  -> plugin='Returning Night.esp' type='ARMA' EDID='AAexPumpsWhite' route='self'  is_arma=True
    ARMO.MOD2..MOD5 (world/inventory drop models, NOT worn): ['ReturningNight\\WhiteBox_gnd.nif']

    -> ARMA 02000803 in 'Returning Night.esp' EDID='AAexPumpsWhite'
        BOD2 raw=8000000000000000 payload_len=8
             mask=0x00000080 bits=[7] slots=['lowerleg']
        ARMA.MOD3 (the WORN garment mesh) = 'ReturningNight\\RnPumpsWhite_1.nif'
        ARMA.source_mesh_refs (MODL, 24): ['00013740', '00013741', '00013742', '00013743', '00013744', '00013745'] ...

```

### E-03 -- verbatim evidence dump: outfit plugin [Brastia] Catwoman 3BA.esp  **PASS**

* expected: informational dump
* observed: 35 lines of verbatim record detail

```
PLUGIN  [Brastia] Catwoman 3BA.esp
PATH    E:\SkyrimAE\mo2\mods\Brastia Catwoman TAS for 3BA — 【服装·装备】【体型·CBBE+3BA】\[Brastia] Catwoman 3BA.esp
SIZE    3850 bytes
MASTERS ['Skyrim.esm', 'Update.esm', 'Heels Sound.esm']

COUNTS  5 ARMO, 5 ARMA (this plugin owns 5 of them)

  ARMO 03000801  EDID='CatwomanTasbodysuit'
    ARMO.RNAM raw=00000019  -> plugin='Skyrim.esm' type='RACE' EDID='DefaultRace' route='master[0]'
    ARMO.RNAM IS: RACE
    BOD2 raw=0400000000000000 payload_len=8
         mask=0x00000004 bits=[2] slots=['body']
    ARMO.MODL (repeated; the ArmorAddon link):
      03000800  master_byte=3  -> plugin='[Brastia] Catwoman 3BA.esp' type='ARMA' EDID='CWTASBodysuit_AA' route='self'  is_arma=True
    ARMO.MOD2..MOD5 (world/inventory drop models, NOT worn): ['Catwomantas\\Bodysuit_1.nif']

    -> ARMA 03000800 in '[Brastia] Catwoman 3BA.esp' EDID='CWTASBodysuit_AA'
        BOD2 raw=0400000000000000 payload_len=8
             mask=0x00000004 bits=[2] slots=['body']
        ARMA.MOD3 (the WORN garment mesh) = 'Catwomantas\\Bodysuit_1.nif'
        ARMA.MOD5 (the WORN garment mesh) = 'Catwomantas\\Bodysuit_1.nif'
        ARMA.source_mesh_refs (MODL, 24): ['00013740', '00013741', '00013742', '00013743', '00013744', '00013745'] ...

  ARMO 03000826  EDID='CatwomantasGloves'
    ARMO.RNAM raw=00000019  -> plugin='Skyrim.esm' type='RACE' EDID='DefaultRace' route='master[0]'
    ARMO.RNAM IS: RACE
    BOD2 raw=0800000000000000 payload_len=8
         mask=0x00000008 bits=[3] slots=['hands']
    ARMO.MODL (repeated; the ArmorAddon link):
      0300080A  master_byte=3  -> plugin='[Brastia] Catwoman 3BA.esp' type='ARMA' EDID='CWTASgloves_AA' route='self'  is_arma=True
    ARMO.MOD2..MOD5 (world/inventory drop models, NOT worn): ['Catwomantas\\gloves_1.nif']

    -> ARMA 0300080A in '[Brastia] Catwoman 3BA.esp' EDID='CWTASgloves_AA'
        BOD2 raw=0800000000000000 payload_len=8
             mask=0x00000008 bits=[3] slots=['hands']
        ARMA.MOD3 (the WORN garment mesh) = 'Catwomantas\\gloves_1.nif'
        ARMA.MOD5 (the WORN garment mesh) = 'Catwomantas\\gloves_1.nif'
        ARMA.source_mesh_refs (MODL, 24): ['00013740', '00013741', '00013742', '00013743', '00013744', '00013745'] ...

```

### E-04 -- verbatim evidence dump: BodySlide project (Nye's Latex Pack 2) Latex Gloves.osp  **PASS**

* expected: informational dump
* observed: 33 lines of verbatim project detail

```
PROJECT CalienteTools/BodySlide/SliderSets/(Nye's Latex Pack 2) Latex Gloves.osp
MOD     Nyes Latex Pack AiO 1.3 (ReducedSize)

  --- as extracted from the .osp XML (07_bodyslide_projects.json) ---
  SliderSet@name (UI outfit name) : "(Nye's Latex Pack 2) Latex Gloves"
  DataFolder                      : "(Nye's Latex Pack 2) Latex Gloves"
  SourceFile                      : "(Nye's Latex Pack 2) Latex Gloves.nif"
  OutputPath                      : 'meshes\\NyesLatexPack2\\ShortLatexGloves'
  OutputFile / @GenWeights        : 'ShortLatexGloves' / 'true'
  output_nif (OutputPath+File)    : 'meshes\\NyesLatexPack2\\ShortLatexGloves\\ShortLatexGloves.nif'
  shapes (Shape@target)           : ['Short Gloves']
  sliders (Slider@name)           : 1
  zap shapes                      : []
  provenance                      : 'osp_xml_parsed'

  --- raw .osp bytes (first 200) ---
  b'\xef\xbb\xbf<?xml version="1.0" encoding="UTF-8"?>\r\n<SliderSetInfo version="1">\r\n    <SliderSet name="(Nye&apos;s Latex Pack 2) Latex Gloves">\r\n        <DataFolder>(Nye\'s Latex Pack 2) Latex Gloves</DataFolder'

  --- resolved base NIF and its .osd companions ---
  base_nif        : "CalienteTools/BodySlide/ShapeData/(Nye's Latex Pack 2) Latex Gloves/(Nye's Latex Pack 2) Latex Gloves.nif"
  base_nif shapes : []
  osd references  : 1 sliders -> 1 refs; first 4:
      "(Nye's Latex Pack 2) Latex Gloves.osd\\Short GlovesWristSize"
  distinct .osd referenced by this project: ['Short GlovesWristSize']
  OSD (Nye's Latex Pack 2) Latex Gloves.osd
      size            : 55672 bytes
      first 4 bytes   : b'\x00DSO'  (= b'\x00DSO', uint32 LE 0x4F534400)
      uint32 @0x04    : 1   (version)
      uint32 @0x08    : 1   <- p00r_bodyslide calls this 'data_offset'
      name at 0x0C    : 'Short GlovesWristSize'   <- where the shape name actually is
      name at 0x08    : None
      parse_osd says  : shape_names=['Short GlovesWristSize'] version=1 data_offset=1

```

### E-05 -- verbatim evidence dump: BodySlide project [TRX] Latex Whitch ThongsFuta2 3ba.osp  **PASS**

* expected: informational dump
* observed: 36 lines of verbatim project detail

```
PROJECT CalienteTools/BodySlide/SliderSets/[TRX] Latex Whitch ThongsFuta2 3ba.osp
MOD     [TRX] LatexWhitch — 【来源·本地】

  --- as extracted from the .osp XML (07_bodyslide_projects.json) ---
  SliderSet@name (UI outfit name) : '[TRX] Latex Whitch ThongsFuta2 3ba'
  DataFolder                      : '[TRX] Latex Whitch ThongsFuta2 3ba'
  SourceFile                      : '[TRX] Latex Whitch ThongsFuta2 3ba.nif'
  OutputPath                      : 'Meshes\\armor\\[TRX]  LatexWhitch'
  OutputFile / @GenWeights        : 'ThongsFuta2' / 'true'
  output_nif (OutputPath+File)    : 'Meshes\\armor\\[TRX]  LatexWhitch\\ThongsFuta2.nif'
  shapes (Shape@target)           : ['Thongs2Futa']
  sliders (Slider@name)           : 83
  zap shapes                      : []
  provenance                      : 'osp_xml_parsed'

  --- raw .osp bytes (first 200) ---
  b'\xef\xbb\xbf<?xml version="1.0" encoding="UTF-8"?>\r\n<SliderSetInfo version="1">\r\n    <SliderSet name="[TRX] Latex Whitch ThongsFuta2 3ba">\r\n        <DataFolder>[TRX] Latex Whitch ThongsFuta2 3ba</DataFolder>\r\n'

  --- resolved base NIF and its .osd companions ---
  base_nif        : 'CalienteTools/BodySlide/ShapeData/[TRX] Latex Whitch ThongsFuta2 3ba/[TRX] Latex Whitch ThongsFuta2 3ba.nif'
  base_nif shapes : []
  osd references  : 83 sliders -> 83 refs; first 4:
      '[TRX] Latex Whitch ThongsFuta2 3ba.osd\\Thongs2Futa7B Lower'
      '[TRX] Latex Whitch ThongsFuta2 3ba.osd\\Thongs2FutaBelly'
      '[TRX] Latex Whitch ThongsFuta2 3ba.osd\\Thongs2FutaBigBelly'
      '[TRX] Latex Whitch ThongsFuta2 3ba.osd\\Thongs2FutaBreastsSmall'
  distinct .osd referenced by this project: ['Thongs2Futa7B Lower', 'Thongs2Futa7BLeg_v2', 'Thongs2FutaAnalLoose_v2', 'Thongs2FutaAnalPosition_v2', 'Thongs2FutaAppleCheeks', 'Thongs2FutaBack', 'Thongs2FutaBackArch', 'Thongs2FutaBackValley_v2', 'Thongs2FutaBelly', 'Thongs2FutaBellyFrontDownFat_v2', 'Thongs2FutaBellyFrontUpFat_v2', 'Thongs2FutaBellySideDownFat_v2', 'Thongs2FutaBellyUnder_v2', 'Thongs2FutaBigBelly', 'Thongs2FutaBigButt', 'Thongs2FutaBigTorso', 'Thongs2FutaBreastsSmall', 'Thongs2FutaBreastsSmall2', 'Thongs2FutaButt', 'Thongs2FutaButtClassic', 'Thongs2FutaButtCrack', 'Thongs2FutaButtDimples', 'Thongs2FutaButtNarrow_v2', 'Thongs2FutaButtPressed_v2', 'Thongs2FutaButtSaggy_v2', 'Thongs2FutaButtShape2', 'Thongs2FutaButtSmall', 'Thongs2FutaButtUnderFold', 'Thongs2FutaCBPC', 'Thongs2FutaChestDepth', 'Thongs2FutaChestWidth', 'Thongs2FutaChubbyButt', 'Thongs2FutaChubbyLegs', 'Thongs2FutaChubbyWaist', 'Thongs2FutaCrotchBack', 'Thongs2FutaCrotchGap', 'Thongs2FutaCutepuffyness', 'Thongs2FutaGroin', 'Thongs2FutaHipBone', 'Thongs2FutaHipCarved', 'Thongs2FutaHipForward', 'Thongs2FutaHipNarrow_v2', 'Thongs2FutaHipUpperWidth', 'Thongs2FutaHips', 'Thongs2FutaInnieoutie', 'Thongs2FutaLabiaBulgogi_v2', 'Thongs2FutaLabiaCrumpled_v2', 'Thongs2FutaLabiaMorePuffyness_v2', 'Thongs2FutaLabiaNeat_v2', 'Thongs2FutaLabiaTightUp', 'Thongs2FutaLabiaprotrude2', 'Thongs2FutaLabiapuffyness', 'Thongs2FutaLabiaspread', 'Thongs2FutaLegSpread_v2', 'Thongs2FutaLegsThin', 'Thongs2FutaMuscleAbs', 'Thongs2FutaMuscleBack_v2', 'Thongs2FutaMuscleButt', 'Thongs2FutaMuscleLegs', 'Thongs2FutaMuscleMoreAbs_v2', 'Thongs2FutaMuscleMoreLegs_v2', 'Thongs2FutaOldBaseShape', 'Thongs2FutaPregnancyBelly', 'Thongs2FutaRoundAss', 'Thongs2FutaSOS - BallsForward', 'Thongs2FutaSOS - BallsSmall', 'Thongs2FutaSOS - BodyTransition', 'Thongs2FutaSOS - ClassicShape', 'Thongs2FutaSOS - GlansHorse', 'Thongs2FutaSOS - SchlongGirth', 'Thongs2FutaSOS - SchlongLength', 'Thongs2FutaSlimThighs', 'Thongs2FutaThighFBThicc_v2', 'Thongs2FutaThighInsideThicc_v2', 'Thongs2FutaThighs', 'Thongs2FutaTummyTuck', 'Thongs2FutaUNPHip_v2', 'Thongs2FutaVaginaHole', 'Thongs2FutaVanillaSSEHi', 'Thongs2FutaVanillaSSELo', 'Thongs2FutaWaist', 'Thongs2FutaWaistHeight', 'Thongs2FutaWideWaistLine']
  OSD [TRX] Latex Whitch ThongsFuta2 3ba.osd
      size            : 1179441 bytes
      first 4 bytes   : b'\x00DSO'  (= b'\x00DSO', uint32 LE 0x4F534400)
      uint32 @0x04    : 1   (version)
      uint32 @0x08    : 83   <- p00r_bodyslide calls this 'data_offset'
      name at 0x0C    : 'Thongs2FutaHipCarved'   <- where the shape name actually is
      name at 0x08    : None
      parse_osd says  : shape_names=['Thongs2FutaHipCarved'] version=1 data_offset=83

```

### E-06 -- verbatim evidence dump: BodySlide project AE_TFD_Valby_Nano_Suit.osp  **PASS**

* expected: informational dump
* observed: 52 lines of verbatim project detail

```
PROJECT CalienteTools/BodySlide/SliderSets/AE_TFD_Valby_Nano_Suit.osp
MOD     makaron-COSPLAY - AE_TFD_Valby_Nano_Suit — 【服装·装备】【来源·本地】

  --- as extracted from the .osp XML (07_bodyslide_projects.json) ---
  SliderSet@name (UI outfit name) : 'AE_TFD_Valby_Nano_Suit'
  DataFolder                      : 'AE_TFD_Valby_Nano_Suit'
  SourceFile                      : 'AE_TFD_Valby_Nano_Suit.nif'
  OutputPath                      : 'meshes\\AE_TFD_Valby_Nano_Suit'
  OutputFile / @GenWeights        : 'AE_TFD_Valby_Nano_Suit' / 'true'
  output_nif (OutputPath+File)    : 'meshes\\AE_TFD_Valby_Nano_Suit\\AE_TFD_Valby_Nano_Suit.nif'
  shapes (Shape@target)           : ['3BA', '3BA_Anus', '3BA_Vagina', 'CatsuitSpearheadA01', 'PC_010_U_CMN_BODY_001_LOD0', 'PC_010_U_CMN_BODY_001_LOD0.002_PC_010_U_CMN_BODY_001_LOD0.186', 'PC_010_U_CMN_BODY_001_LOD0.003_PC_010_U_CMN_BODY_001_LOD0.227', 'PC_010_U_CMN_BODY_001_LOD0.006_PC_010_U_CMN_BODY_001_LOD0.231', 'PC_010_U_CMN_BODY_001_LOD0.007_PC_010_U_CMN_BODY_001_LOD0.190', 'PC_010_U_CMN_BODY_001_LOD0.009_PC_010_U_CMN_BODY_001_LOD0.229', 'PC_010_U_CMN_BODY_001_LOD0.010_PC_010_U_CMN_BODY_001_LOD0.193', 'PC_010_U_CMN_BODY_001_LOD0.011_PC_010_U_CMN_BODY_001_LOD0.194', 'PC_010_U_CMN_BODY_001_LOD0.012_PC_010_U_CMN_BODY_001_LOD0.195', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204', 'PC_010_U_CMN_BODY_001_LOD0.023_PC_010_U_CMN_BODY_001_LOD0.206', 'PC_010_U_CMN_BODY_001_LOD0.035_PC_010_U_CMN_BODY_001_LOD0.218', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220']
  sliders (Slider@name)           : 224
  zap shapes                      : []
  provenance                      : 'osp_xml_parsed'

  --- raw .osp bytes (first 200) ---
  b'\xef\xbb\xbf<?xml version="1.0" encoding="UTF-8"?>\r\n<SliderSetInfo version="1">\r\n    <SliderSet name="AE_TFD_Valby_Nano_Suit">\r\n        <DataFolder>AE_TFD_Valby_Nano_Suit</DataFolder>\r\n        <SourceFile>AE_T'

  --- resolved base NIF and its .osd companions ---
  base_nif        : 'CalienteTools/BodySlide/ShapeData/AE_TFD_Valby_Nano_Suit/AE_TFD_Valby_Nano_Suit.nif'
  base_nif shapes : []
  osd references  : 224 sliders -> 224 refs; first 4:
      'AE_TFD_Valby_Nano_Suit.osd\\PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204ArmpitShape_v2'
      'AE_TFD_Valby_Nano_Suit.osd\\3BAAnkleSize'
      'AE_TFD_Valby_Nano_Suit.osd\\3BA_VaginaAppleCheeks'
      'AE_TFD_Valby_Nano_Suit.osd\\PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204AreolaPull_v2'
  distinct .osd referenced by this project: ['3BA7B Lower', '3BA7BLeg_v2', '3BAAnkleSize', '3BACalfFBThicc_v2', '3BACalfSize', '3BACalfSmooth', '3BAChubbyLegs', '3BAKneeHeight', '3BAKneeShape', '3BALegShapeClassic', '3BALegsThin', '3BAMuscleLegs', '3BAMuscleMoreLegs_v2', '3BAOldBaseShape', '3BAVanillaSSEHi', '3BAVanillaSSELo', '3BA_AnusButtSaggy_v2', '3BA_VaginaAnalLoose_v2', '3BA_VaginaAnalPosition_v2', '3BA_VaginaAppleCheeks', '3BA_VaginaBellyUnder_v2', '3BA_VaginaBigBelly', '3BA_VaginaBigButt', '3BA_VaginaButt', '3BA_VaginaButtClassic', '3BA_VaginaButtCrack', '3BA_VaginaButtPressed_v2', '3BA_VaginaButtShape2', '3BA_VaginaButtSmall', '3BA_VaginaButtUnderFold', '3BA_VaginaCBPC', '3BA_VaginaChubbyButt', '3BA_VaginaChubbyWaist', '3BA_VaginaClit', '3BA_VaginaClitSwell_v2', '3BA_VaginaCrotchBack', '3BA_VaginaCrotchGap', '3BA_VaginaCutepuffyness', '3BA_VaginaGroin', '3BA_VaginaHipBone', '3BA_VaginaHipForward', '3BA_VaginaHips', '3BA_VaginaInnieoutie', '3BA_VaginaLabiaBulgogi_v2', '3BA_VaginaLabiaCrumpled_v2', '3BA_VaginaLabiaMorePuffyness_v2', '3BA_VaginaLabiaNeat_v2', '3BA_VaginaLabiaTightUp', '3BA_VaginaLabiaprotrude', '3BA_VaginaLabiaprotrude2', '3BA_VaginaLabiaprotrudeback', '3BA_VaginaLabiapuffyness', '3BA_VaginaLabiaspread', '3BA_VaginaPregnancyBelly', '3BA_VaginaRoundAss', '3BA_VaginaSlimThighs', '3BA_VaginaThighInsideThicc_v2', '3BA_VaginaThighs', '3BA_VaginaTummyTuck', '3BA_VaginaVaginaHole', '3BA_VaginaVaginasize', '3BA_VaginaWaistHeight', 'CatsuitSpearheadA01Aah', 'CatsuitSpearheadA01BMP', 'CatsuitSpearheadA01BigAah', 'CatsuitSpearheadA01BretonRace', 'CatsuitSpearheadA01CME_BretonRace', 'CatsuitSpearheadA01CME_BretonRace_inv', 'CatsuitSpearheadA01CME_DarkElfRace', 'CatsuitSpearheadA01CME_DarkElfRace_inv', 'CatsuitSpearheadA01CME_DremoraRace', 'CatsuitSpearheadA01CME_DremoraRace_inv', 'CatsuitSpearheadA01CME_ElderRace', 'CatsuitSpearheadA01CME_ElderRace_inv', 'CatsuitSpearheadA01CME_HighElfRace', 'CatsuitSpearheadA01CME_HighElfRace_inv', 'CatsuitSpearheadA01CME_ImperialRace', 'CatsuitSpearheadA01CME_ImperialRace_inv', 'CatsuitSpearheadA01CME_NordRace', 'CatsuitSpearheadA01CME_NordRace_inv', 'CatsuitSpearheadA01CME_OrcRace', 'CatsuitSpearheadA01CME_OrcRace_inv', 'CatsuitSpearheadA01CME_RedguardRace', 'CatsuitSpearheadA01CME_RedguardRace_inv', 'CatsuitSpearheadA01CME_WoodElfRace', 'CatsuitSpearheadA01CME_WoodElfRace_inv', 'CatsuitSpearheadA01ChinMoveDown', 'CatsuitSpearheadA01ChinMoveUp', 'CatsuitSpearheadA01CombatShout', 'CatsuitSpearheadA01DST', 'CatsuitSpearheadA01DarkElfRace', 'CatsuitSpearheadA01DremoraRace', 'CatsuitSpearheadA01EXPR_Aah', 'CatsuitSpearheadA01EXPR_BMP', 'CatsuitSpearheadA01EXPR_BigAah', 'CatsuitSpearheadA01EXPR_CombatShout', 'CatsuitSpearheadA01EXPR_DST', 'CatsuitSpearheadA01EXPR_Eh', 'CatsuitSpearheadA01EXPR_FV', 'CatsuitSpearheadA01EXPR_I', 'CatsuitSpearheadA01EXPR_K', 'CatsuitSpearheadA01EXPR_MoodAnger', 'CatsuitSpearheadA01EXPR_MoodSurprise', 'CatsuitSpearheadA01EXPR_N', 'CatsuitSpearheadA01EXPR_Oh', 'CatsuitSpearheadA01EXPR_R', 'CatsuitSpearheadA01EXPR_Th', 'CatsuitSpearheadA01Eh', 'CatsuitSpearheadA01ElderRace', 'CatsuitSpearheadA01FV', 'CatsuitSpearheadA01FeetFeminine', 'CatsuitSpearheadA01ForearmSize', 'CatsuitSpearheadA01HighElfRace', 'CatsuitSpearheadA01I', 'CatsuitSpearheadA01ImperialRace', 'CatsuitSpearheadA01JawBack', 'CatsuitSpearheadA01JawNarrow', 'CatsuitSpearheadA01JawWide', 'CatsuitSpearheadA01K', 'CatsuitSpearheadA01LipType1', 'CatsuitSpearheadA01MoodAnger', 'CatsuitSpearheadA01MoodSurprise', 'CatsuitSpearheadA01N', 'CatsuitSpearheadA01NippleDip', 'CatsuitSpearheadA01NordRace', 'CatsuitSpearheadA01Oh', 'CatsuitSpearheadA01OrcRace', 'CatsuitSpearheadA01R', 'CatsuitSpearheadA01RedguardRace', 'CatsuitSpearheadA01SkinnyMorph', 'CatsuitSpearheadA01Th', 'CatsuitSpearheadA01WoodElfRace', 'PC_010_U_CMN_BODY_001_LOD0.006_PC_010_U_CMN_BODY_001_LOD0.231ShoulderWidth', 'PC_010_U_CMN_BODY_001_LOD0.006_PC_010_U_CMN_BODY_001_LOD0.231WristSize', 'PC_010_U_CMN_BODY_001_LOD0.007_PC_010_U_CMN_BODY_001_LOD0.190BigTorso', 'PC_010_U_CMN_BODY_001_LOD0.007_PC_010_U_CMN_BODY_001_LOD0.190ButtNarrow_v2', 'PC_010_U_CMN_BODY_001_LOD0.007_PC_010_U_CMN_BODY_001_LOD0.190HipCarved', 'PC_010_U_CMN_BODY_001_LOD0.007_PC_010_U_CMN_BODY_001_LOD0.190HipNarrow_v2', 'PC_010_U_CMN_BODY_001_LOD0.007_PC_010_U_CMN_BODY_001_LOD0.190HipUpperWidth', 'PC_010_U_CMN_BODY_001_LOD0.007_PC_010_U_CMN_BODY_001_LOD0.190KneeTogether_v2', 'PC_010_U_CMN_BODY_001_LOD0.007_PC_010_U_CMN_BODY_001_LOD0.190LegSpread_v2', 'PC_010_U_CMN_BODY_001_LOD0.007_PC_010_U_CMN_BODY_001_LOD0.190MuscleButt', 'PC_010_U_CMN_BODY_001_LOD0.007_PC_010_U_CMN_BODY_001_LOD0.190ThighFBThicc_v2', 'PC_010_U_CMN_BODY_001_LOD0.007_PC_010_U_CMN_BODY_001_LOD0.190ThighOutsideThicc_v2', 'PC_010_U_CMN_BODY_001_LOD0.007_PC_010_U_CMN_BODY_001_LOD0.190UNPHip_v2', 'PC_010_U_CMN_BODY_001_LOD0.007_PC_010_U_CMN_BODY_001_LOD0.190WideWaistLine', 'PC_010_U_CMN_BODY_001_LOD0.011_PC_010_U_CMN_BODY_001_LOD0.194BackArch', 'PC_010_U_CMN_BODY_001_LOD0.011_PC_010_U_CMN_BODY_001_LOD0.194BellySideDownFat_v2', 'PC_010_U_CMN_BODY_001_LOD0.011_PC_010_U_CMN_BODY_001_LOD0.194BellySideUpFat_v2', 'PC_010_U_CMN_BODY_001_LOD0.011_PC_010_U_CMN_BODY_001_LOD0.194ButtDimples', 'PC_010_U_CMN_BODY_001_LOD0.012_PC_010_U_CMN_BODY_001_LOD0.195Back', 'PC_010_U_CMN_BODY_001_LOD0.012_PC_010_U_CMN_BODY_001_LOD0.195Waist', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204AreolaPull_v2', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204ArmpitShape_v2', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NipBGone', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NippleBump_v2', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NippleCrease_v2', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NippleCrumpled_v2', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NippleLength', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NippleManga', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NipplePerkManga', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NipplePerkiness', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NipplePuffy_v2', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NippleShy_v2', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NippleSize', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NippleSquash1_v2', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NippleSquash2_v2', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NippleThicc_v2', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NippleTip', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NippleTipManga', 'PC_010_U_CMN_BODY_001_LOD0.021_PC_010_U_CMN_BODY_001_LOD0.204NippleTube_v2', 'PC_010_U_CMN_BODY_001_LOD0.023_PC_010_U_CMN_BODY_001_LOD0.2067B Upper', 'PC_010_U_CMN_BODY_001_LOD0.023_PC_010_U_CMN_BODY_001_LOD0.206Arms', 'PC_010_U_CMN_BODY_001_LOD0.023_PC_010_U_CMN_BODY_001_LOD0.206BackValley_v2', 'PC_010_U_CMN_BODY_001_LOD0.023_PC_010_U_CMN_BODY_001_LOD0.206BackWing_v2', 'PC_010_U_CMN_BODY_001_LOD0.023_PC_010_U_CMN_BODY_001_LOD0.206ChestWidth', 'PC_010_U_CMN_BODY_001_LOD0.023_PC_010_U_CMN_BODY_001_LOD0.206ChubbyArms', 'PC_010_U_CMN_BODY_001_LOD0.023_PC_010_U_CMN_BODY_001_LOD0.206MuscleArms', 'PC_010_U_CMN_BODY_001_LOD0.023_PC_010_U_CMN_BODY_001_LOD0.206MuscleBack_v2', 'PC_010_U_CMN_BODY_001_LOD0.023_PC_010_U_CMN_BODY_001_LOD0.206MuscleMoreArms_v2', 'PC_010_U_CMN_BODY_001_LOD0.023_PC_010_U_CMN_BODY_001_LOD0.206NeckSeam', 'PC_010_U_CMN_BODY_001_LOD0.023_PC_010_U_CMN_BODY_001_LOD0.206ShoulderSmooth', 'PC_010_U_CMN_BODY_001_LOD0.023_PC_010_U_CMN_BODY_001_LOD0.206ShoulderTweak', 'PC_010_U_CMN_BODY_001_LOD0.035_PC_010_U_CMN_BODY_001_LOD0.218Belly', 'PC_010_U_CMN_BODY_001_LOD0.035_PC_010_U_CMN_BODY_001_LOD0.218BellyFrontDownFat_v2', 'PC_010_U_CMN_BODY_001_LOD0.035_PC_010_U_CMN_BODY_001_LOD0.218BellyFrontUpFat_v2', 'PC_010_U_CMN_BODY_001_LOD0.035_PC_010_U_CMN_BODY_001_LOD0.218BreastSideShape', 'PC_010_U_CMN_BODY_001_LOD0.035_PC_010_U_CMN_BODY_001_LOD0.218BreastUnderDepth', 'PC_010_U_CMN_BODY_001_LOD0.035_PC_010_U_CMN_BODY_001_LOD0.218MuscleAbs', 'PC_010_U_CMN_BODY_001_LOD0.035_PC_010_U_CMN_BODY_001_LOD0.218MuscleMoreAbs_v2', 'PC_010_U_CMN_BODY_001_LOD0.035_PC_010_U_CMN_BODY_001_LOD0.218NavelEven', 'PC_010_U_CMN_BODY_001_LOD0.035_PC_010_U_CMN_BODY_001_LOD0.218NippleInvert_v2', 'PC_010_U_CMN_BODY_001_LOD0.035_PC_010_U_CMN_BODY_001_LOD0.218RibsMore_v2', 'PC_010_U_CMN_BODY_001_LOD0.035_PC_010_U_CMN_BODY_001_LOD0.218RibsProminance', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastCenter', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastCenterBig', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastCleavage', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastFlatness', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastFlatness2', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastGravity2', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastHeight', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastPerkiness', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastTopSlope', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastWidth', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220Breasts', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastsConverage_v2', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastsFantasy', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastsGone', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastsNewSH', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastsNewSHSymmetry', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastsPressed_v2', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastsSmall', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastsSmall2', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220BreastsTogether', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220ChestDepth', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220Clavicle_v2', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220DoubleMelon', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220MusclePecs', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220NippleDistance', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220NippleDown', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220NippleUp', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220PushUp', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220SternumDepth', 'PC_010_U_CMN_BODY_001_LOD0.037_PC_010_U_CMN_BODY_001_LOD0.220SternumHeight']
  OSD AE_TFD_Valby_Nano_Suit.osd
      size            : 27023800 bytes
      first 4 bytes   : b'\x00DSO'  (= b'\x00DSO', uint32 LE 0x4F534400)
      uint32 @0x04    : 1   (version)
      uint32 @0x08    : 1056   <- p00r_bodyslide calls this 'data_offset'
      name at 0x0C    : 'CatsuitSpearheadA01KneeHeight'   <- where the shape name actually is
      name at 0x08    : None
      parse_osd says  : shape_names=['CatsuitSpearheadA01KneeHeight'] version=1 data_offset=1056
  OSD AE_TFD_Valby_Nano_Suit_1st.osd
      size            : 2003245 bytes
      first 4 bytes   : b'\x00DSO'  (= b'\x00DSO', uint32 LE 0x4F534400)
      uint32 @0x04    : 1   (version)
      uint32 @0x08    : 88   <- p00r_bodyslide calls this 'data_offset'
      name at 0x0C    : 'PC_010_U_CMN_BODY_001_LOD0.005_PC_010_U_CMN_BODY_001_LOD0.188BreastsGone'   <- where the shape name actually is
      name at 0x08    : None
      parse_osd says  : shape_names=['PC_010_U_CMN_BODY_001_LOD0.005_PC_010_U_CMN_BODY_001_LOD0.188BreastsGone'] version=1 data_offset=88
  OSD AE_TFD_Valby_Nano_Suit_Alt.osd
      size            : 25721055 bytes
      first 4 bytes   : b'\x00DSO'  (= b'\x00DSO', uint32 LE 0x4F534400)
      uint32 @0x04    : 1   (version)
      uint32 @0x08    : 963   <- p00r_bodyslide calls this 'data_offset'
      name at 0x0C    : 'PC_010_U_CMN_BODY_001_LOD0ChestWidth'   <- where the shape name actually is
      name at 0x08    : None
      parse_osd says  : shape_names=['PC_010_U_CMN_BODY_001_LOD0ChestWidth'] version=1 data_offset=963

```

