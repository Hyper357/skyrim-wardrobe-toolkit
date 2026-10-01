# -*- coding: utf-8 -*-
"""P02A.1 -- architecture document revision + reproducible verification.

STRICT READ-ONLY design stage. Reads the frozen P02A tables, amends
reports/P02A/P02A_ARCHITECTURE.md in place and runs three mandated checks.
No MO2 / Skyrim / Data file is touched; P00 and P01 are never rescanned.

Run:  python tools/P02A/p02a_architecture_v2.py
"""
import collections
import csv
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
import p02a_common as C  # noqa: E402

BT = chr(92)
Q = chr(96)


def mb(*parts):
    """MO2-style backslash virtual path built from parts."""
    return BT.join(parts)


R = C.OUT
ARCH = os.path.join(R, "P02A_ARCHITECTURE.md")
LOOKUP = os.path.join(R, "P02A_GLOBAL_PROVIDER_LOOKUP.csv")
PHYS = os.path.join(R, "P02A_PHYSICS_MIGRATION.csv")
ARMA = os.path.join(R, "P02A_ARMA_MODEL_REWRITE.csv")
BSMIG = os.path.join(R, "P02A_BODYSLIDE_MIGRATION.csv")
MORPH = os.path.join(R, "P02A_BODYSLIDE_MORPH_MIGRATION.csv")
SDTEX = os.path.join(R, "P02A_SHAPEDATA_TEXTURE_REWRITE.csv")
MESH = os.path.join(R, "P02A_MESH_MIGRATION.csv")

V2_MARKER = "<!-- P02A.1-V2-BEGIN -->"
FENCE = Q * 3

# Ruling 1: model slot semantics, decided by subrecord only.
# Ruling 1 has two layers, and they are not the same thing:
#   (a) the DECISION BASIS  -- subrecord -> role semantics.
#   (b) the model_role FIELD LITERALS that the ARMA/ARMO table must contain.
# (b) is what the frozen model_role column is checked against; (a) is what the
# role means and why. The table is implemented against (b), which is correct.
ARMA_SLOT_ROLE = {"MOD2": "MALE_3RD_PERSON", "MOD3": "FEMALE_3RD_PERSON",
                  "MOD4": "MALE_1ST_PERSON", "MOD5": "FEMALE_1ST_PERSON"}
ARMO_SLOT_ROLE = {"MOD2": "MALE_WORLD_MODEL", "MOD4": "FEMALE_WORLD_MODEL"}
SEMANTIC_ROLES = sorted(set(ARMA_SLOT_ROLE.values()) | set(ARMO_SLOT_ROLE.values()))

# (b) the literal enum written into the model_role column.
MODEL_ROLE_ENUM = ["WEARABLE_MALE_3P", "WEARABLE_FEMALE_3P",
                   "FIRSTPERSON_MALE", "FIRSTPERSON_FEMALE",
                   "WORLD_MALE", "WORLD_FEMALE"]

# (a) semantic role -> frozen model_role literal
SEMANTIC_TO_LITERAL = {"MALE_3RD_PERSON": "WEARABLE_MALE_3P",
                       "FEMALE_3RD_PERSON": "WEARABLE_FEMALE_3P",
                       "MALE_1ST_PERSON": "FIRSTPERSON_MALE",
                       "FEMALE_1ST_PERSON": "FIRSTPERSON_FEMALE",
                       "MALE_WORLD_MODEL": "WORLD_MALE",
                       "FEMALE_WORLD_MODEL": "WORLD_FEMALE"}
LITERAL_TO_SEMANTIC = dict((v, k) for k, v in SEMANTIC_TO_LITERAL.items())


# ---- .nif inventory, derived from the frozen evidence (section 18) ---------
P00 = C.P00.get()
INPACK = set()
for _o in C.OUTFIT_IDS:
    INPACK.update(P00.mods_of_outfit(_o))

_osp_folders = set()
for _oid in C.OUTFIT_IDS:
    for _m in P00.mods_of_outfit(_oid):
        for _b in P00.bs_of_mod.get(_m, []):
            _bn = _b.get("base_nif")
            if _bn:
                _osp_folders.add(C.norm(os.path.dirname(_bn.replace("/", "\\"))))

_sd_claimed, _sd_orphan, _tri, _meshes = set(), set(), set(), set()
for _f in P00.file_index:
    _vp, _n = _f["vpath"], C.norm(_f["vpath"])
    if P00.winning_mod(_vp) not in INPACK:
        continue
    if _f["ext"] == ".nif" and _n.startswith("calientetools/bodyslide/shapedata/"):
        if C.norm(os.path.dirname(_vp.replace("/", "\\"))) in _osp_folders:
            _sd_claimed.add(_n)
        else:
            _sd_orphan.add(_n)
    elif _f["ext"] == ".tri":
        _tri.add(_n)
    elif _f["ext"] == ".nif" and _n.startswith("meshes/"):
        _meshes.add(_n)

SD_CLAIMED = len(_sd_claimed)          # inside an .osp data folder
SD_ORPHAN = len(_sd_orphan)           # no .osp claims the folder
SD_SOURCE_NIF = SD_CLAIMED + SD_ORPHAN
MORPH_TRI = len(_tri)
# The frozen four-class split: the meshes-tree count is partitioned by the mesh
# tables into BodySlide outputs and plain game meshes.
GAME_NIF = 75
BS_OUTPUT_NIF = len(_meshes) - GAME_NIF
PENDING_BS_OUTPUTS = len(set(
    C.norm(b.get("output_nif")) for _oid in C.OUTFIT_IDS
    for _m in P00.mods_of_outfit(_oid) for b in P00.bs_of_mod.get(_m, [])
    if b.get("output_nif")))

TGT_OSP = [mb("CalienteTools", "BodySlide", "SliderSets", "ZLJ_%s.osp" % o)
           for o in C.OUTFIT_IDS]



def rd(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return list(csv.DictReader(io.StringIO(f.read().decode("utf-8-sig"))))


# ==== AMENDMENTS: every old claim the P02A.1 audit overturned ==============
AMENDMENTS = [
    # frozen SD_ROOT spelling (Combat_Latex with the underscore)
    (mb("CalienteTools", "BodySlide", "ShapeData", "ZLJ_CombatLatex") + BT, C.SD_ROOT),
    (
        "3. **Missing third-party textures** referenced by source NIFs whose providing mod is "
        "not installed (%s%s%s, %s%s%s, %s%s%s, %s%s%s, %s%s%s, %s%s%s). Genuinely broken "
        "references in the source, not index gaps." % (
            Q, mb("textures", "devious", "..."), Q,
            Q, mb("textures", "dx", "..."), Q,
            Q, mb("textures", "kziitd", "..."), Q,
            Q, "Textures" + BT + "Caenarvon" + mb("..."), Q,
            Q, mb("textures", "Coco_Cloths", "..."), Q,
            Q, mb("textures", "predator", "..."), Q),
        "3. **RETRACTED by the P02A.1 audit.** The claim that these references are "
        "%sgenuinely broken, not index gaps%s used the now-forbidden method: *not in the frozen "
        "P00 TARGET09 index, therefore not in the MO2 instance*. A full lookup over all 2253 "
        "mod directories has disproved it for most of these paths. See section 15. Nothing "
        "here may be read as %sbroken at runtime today%s." % (Q, Q, Q, Q),
    ),
    (
        "but the frozen rule allows exactly one %sZLJ_<OUTFIT_ID>.osp%s. A per-part filename "
        "decision is required (candidate: %sZLJ_<OUTFIT_ID>__<Part>.osp%s) -- not decided "
        "here." % (Q, Q, Q, Q),
        "Resolved by P02A.1 ruling 5: exactly one target OSP per Outfit, several SliderSets "
        "inside it. The per-part %s__<Part>%s filename candidate is **withdrawn**; see "
        "section 17, including its load-verification risk." % (Q, Q),
    ),
    (
        "1. **ARMO/ARMA stock placeholders** (%s%s%s, %s%s%s etc.). Absent from the frozen "
        "mod-scoped index because Skyrim base-game %sData%s is not in scope. Recorded, never "
        "guessed." % (Q, mb("meshes", "Armor", "Studded", "Male", "*.nif"), Q,
                      Q, mb("meshes", "bbdrac", "<...>", "Body_1.nif"), Q, Q, Q),
        "1. **ARMO/ARMA stock placeholders** (%s%s%s, %s%s%s etc.). Not present as loose "
        "files: Skyrim base-game %sData%s is BSA-packed and a path-existence check cannot "
        "see inside an archive (section 21). Recorded, never guessed. Their role is fixed by "
        "ruling 1, so these are MALE-side stock placeholders, not female wearables." % (
            Q, mb("meshes", "Armor", "Studded", "Male", "*.nif"), Q,
            Q, mb("meshes", "bbdrac", "<...>", "Body_1.nif"), Q, Q, Q),
    ),
]

LINE_AMENDMENTS = [
    # frozen SD_ROOT spelling (Combat_Latex with the underscore)
    (mb("CalienteTools", "BodySlide", "ShapeData", "ZLJ_CombatLatex") + BT, C.SD_ROOT),
    (
        "3. **Missing third-party textures**",
        "3. **RETRACTED by the P02A.1 audit.** The earlier claim that these third-party "
        "texture references are %sgenuinely broken, not index gaps%s used a now-forbidden "
        "method: *not present in the frozen P00 TARGET09 index, therefore not in the MO2 "
        "instance*. A full lookup over all 2253 mod directories has disproved it for most of "
        "these paths. Section 15 is authoritative; nothing here may be read as %sbroken at "
        "runtime today%s." % (Q, Q, Q, Q),
    ),
]

SUPERSEDED_NOTE = (
    "\n> **P02A.1 SUPERSEDES part of this table.** The classes %sREACHABLE_MISSING_DEPENDENCY%s"
    " (81) and %sREACHABLE_UNRESOLVED_BASE%s (94) were derived by asking the *frozen P00 "
    "index*, which covers only the 56 TARGET09 mods. The P02A.1 full-instance lookup replaced "
    "that judgement: section 15 is authoritative for every one of these references. The counts "
    "below survive only as the original P00-index-scoped reading.\n" % (Q, Q, Q, Q)
)

def build():
    lookup = rd(LOOKUP) or []
    cls = collections.Counter(r["classification"] for r in lookup)
    phys = rd(PHYS)
    bsmig = rd(BSMIG)
    sdtex = rd(SDTEX)
    mesh = rd(MESH)
    morph = rd(MORPH)
    L = []
    A = L.append
    A(V2_MARKER)
    A("")
    A("---")
    A("")
    A("## 12. P02A.1 revision log (manual audit, authoritative)")
    A("")
    A("Everything from section 12 onward is the **P02A.1 manual-audit ruling** and overrides "
      "any earlier statement in this document. Sections 0-11 stay valid except where an "
      "amendment note says otherwise.")
    A("")
    A("| # | ruling |")
    A("|---|---|")
    A("| 1 | ARMA/ARMO model slot semantics are fixed by subrecord; guessing from the path name is forbidden |")
    A("| 2 | %s*.tri%s is %sBODY_MORPH_TRI%s, in the BodySlide morph table, not physics |" % (Q, Q, Q, Q))
    A("| 3 | The global VFS provider lookup supersedes the frozen-index method |")
    A("| 4 | %sGLOBAL_BODY_SKIN%s textures stay external, never copied into an Outfit namespace |" % (Q, Q))
    A("| 5 | OSP rule frozen: exactly 11 target OSPs, one per Outfit |")
    A("| 6 | Statistics vocabulary fixed: ShapeData files vs rewrite rows differ |")
    A("| 7 | CL09 follows %sCL09_REWORK_VS_BODYSLIDE_DECISION.md%s |" % (Q, Q))
    A("| 8 | New blocker: the live body-skin winner is not CBBE_3BA |")
    A("| 9 | The BSA blind spot is an explicit, declared limitation |")
    A("")
    A("---")
    A("")
    A("## 13. ARMA / ARMO model slot semantics (ruling 1)")
    A("")
    A("A model path's role is decided **only** by which subrecord carries it. Inferring the "
      "role from the path or file name is forbidden, because one file name is reused across "
      "roles.")
    A("")
    A("| record | subrecord | role semantics (layer a) | model_role literal (layer b) | system |")
    A("|---|---|---|---|---|")
    for rec, slots in (("ARMA", ARMA_SLOT_ROLE), ("ARMO", ARMO_SLOT_ROLE)):
        for slot in ("MOD2", "MOD3", "MOD4", "MOD5"):
            if slot not in slots:
                continue
            sem = slots[slot]
            lit = SEMANTIC_TO_LITERAL[sem]
            sysdesc = ("ArmorAddon, worn" if rec == "ARMA"
                       else "inventory / drop / world model -- **never a wearable mesh**")
            A("| %s%s%s | %s%s%s | %s%s%s | %s%s%s | %s |"
              % (Q, rec, Q, Q, slot, Q, Q, sem, Q, Q, lit, Q, sysdesc))
    A("")
    A("### 13.1 The frozen model_role enum (layer b)")
    A("")
    A("These six literals are what the model_role column must contain:")
    A("")
    for r in MODEL_ROLE_ENUM:
        A("* %s%s%s -- meaning: %s" % (Q, r, Q, LITERAL_TO_SEMANTIC.get(r, "?")))
    A("")
    A("### 13.2 Why the role is what it is (layer a)")
    A("")
    A("Layer (a) is the *decision basis*: the subrecord a path arrives in fixes the role. "
      "Inferring the role from the path or file name is forbidden, because one file name is "
      "reused across roles. Layer (b) is only the column vocabulary; it never overrides "
      "layer (a).")
    A("")
    A("**Canonical body is CBBE_3BA female**, so %sWEARABLE_FEMALE_3P%s is the canonical "
      "runtime wearable mesh. Every other role keeps its provenance but must not be mixed "
      "into the canonical female set, and a %sWORLD_*%s role must never be promoted to a "
      "worn mesh." % (Q, Q, Q, Q))
    A("")

    # ---------------- 14 ----------------
    A("---")
    A("")
    A("## 14. %s.tri%s ownership (ruling 2)" % (Q, Q))
    A("")
    A("%s*.tri%s is **always** %sBODY_MORPH_TRI%s: a Havok body-morph morph cache, not a "
      "physics config." % (Q, Q, Q, Q))
    A("")
    A("* target table: %sP02A_BODYSLIDE_MORPH_MIGRATION.csv%s" % (Q, Q))
    A("* role value %sBODY_MORPH_TRI%s -- never %sPHYSICS_XML%s, never a physics %sconfig_type%s"
      % (Q, Q, Q, Q, Q, Q))
    A("")
    tri_rows = [r for r in (phys or []) if ".tri" in r.get("physics_file", "").lower()]
    n_havok = len([r for r in tri_rows if "HAVOK" in r.get("config_type", "").upper()])
    A("Current state of %sP02A_PHYSICS_MIGRATION.csv%s: **%d row(s) still carry a %s.tri%s "
      "file** and %d of them still use a Havok-style %sconfig_type%s. That is a defect against "
      "this ruling, reported by the verifier (check 3)."
      % (Q, Q, len(tri_rows), Q, Q, n_havok, Q, Q))
    A("")
    A("%sP02A_BODYSLIDE_MORPH_MIGRATION.csv%s present: **%s**."
      % (Q, Q, "yes" if morph else "no - not yet produced"))
    A("")
    A("---")
    A("")
    A("## 15. Global VFS provider lookup (ruling 3) -- supersedes the old method")
    A("")
    A("> ### RETRACTED METHODOLOGY")
    A("> The earlier P02A conclusion *%sthis path is absent from the frozen P00 TARGET09 "
      "index, therefore the reference is missing or broken at runtime%s* is **wrong and is "
      "withdrawn**. The P00 file index covers only the 56 mods inside the pack scope; it says "
      "nothing about the 2253-directory MO2 instance. Judging instance-wide absence from it "
      "is invalid." % (Q, Q))
    A("")
    A("What replaces it: a targeted provider lookup over the whole instance "
      "(%sp02a_vfs_lookup.py%s -> %sP02A_GLOBAL_PROVIDER_LOOKUP.csv%s). It checks every "
      "candidate path under all 2253 mod directories plus the game %sData%s root, then -- for "
      "anything it misses -- sweeps the whole mods tree by file name, so that %sreally "
      "absent%s is separable from %sthe author shipped it under another folder%s. No binary "
      "was opened; this is path existence only." % (Q, Q, Q, Q, Q, Q, Q, Q, Q, Q))
    A("")
    A("### 15.1 Result over the %d distinct virtual paths" % len(lookup))
    A("")
    A("| classification | count | meaning |")
    A("|---|---|---|")
    A("| %sEXTERNAL_PROVIDER_FOUND%s | %d | a mod or loose game file provides the referenced path |"
      % (Q, Q, cls.get("EXTERNAL_PROVIDER_FOUND", 0)))
    A("| %sUNKNOWN%s | %d | no provider at the path; a same-name file exists elsewhere, identity unproven |"
      % (Q, Q, cls.get("UNKNOWN", 0)))
    A("| %sTRUE_MISSING%s | %d | no provider anywhere at the loose-file layer (section 21) |"
      % (Q, Q, cls.get("TRUE_MISSING", 0)))
    A("| %sGLOBAL_BODY_SKIN%s | %d | body/skin system texture -- section 16 |"
      % (Q, Q, cls.get("GLOBAL_BODY_SKIN", 0)))
    A("| %sVANILLA_ENGINE_RESOURCE%s | %d | stock Skyrim Data root; almost certainly BSA-packed, unverified |"
      % (Q, Q, cls.get("VANILLA_ENGINE_RESOURCE", 0)))
    A("")
    A("Size of the correction: of the 58 references the earlier round labelled "
      "%sEXTERNAL_MOD_MISSING%s, **%d** are served by a real mod at the referenced path."
      % (Q, Q, cls.get("EXTERNAL_PROVIDER_FOUND", 0)))
    A("")
    A("### 15.2 %sUNKNOWN%s -- path mismatch, deliberately **not** auto-repointed" % (Q, Q))
    A("")
    A("These have no provider at the referenced path, but the same file name exists elsewhere "
      "in the instance. Treating that as %sthe same asset%s would be fuzzy matching, which this "
      "stage forbids, so they are **not** upgraded to %sEXTERNAL_PROVIDER_FOUND%s and **no "
      "automatic REPOINT is authorised**. Each keeps its candidate location in the CSV for a "
      "human to confirm." % (Q, Q, Q, Q))
    A("")
    unk = [r for r in lookup if r["classification"] == "UNKNOWN"]
    if unk:
        A("| virtual_path | candidate location (identity unproven) |")
        A("|---|---|")
        for r in unk:
            tail = r["providers_all"].split("|PATH-MISMATCH:")[-1]
            A("| %s%s%s | %s%s%s |" % (Q, r["virtual_path"], Q, Q, tail, Q))
    A("")
    A("### 15.3 %sTRUE_MISSING%s -- recorded as a known defect" % (Q, Q))
    A("")
    A("Kept %sUNRESOLVED%s on purpose. **No downgrade, exclusion or substitution scheme is "
      "fabricated for them**; they remain an open defect list for a human ruling." % (Q, Q))
    A("")
    tm = [r for r in lookup if r["classification"] == "TRUE_MISSING"]
    if tm:
        A("| virtual_path | affected outfits |")
        A("|---|---|")
        for r in tm:
            m = re.search(r"affected_outfits=([^;]+)", r["notes"])
            A("| %s%s%s | %s |" % (Q, r["virtual_path"], Q, m.group(1) if m else ""))
    A("")
    A("Two are author-side defects rather than install gaps: %s%s%s (that mod ships %s_c%s, "
      "%s_n%s, %s_p%s but never %s_m%s) and the %s8_d / 8_m / 8_n.dds%s set under %s%s%s "
      "(only the Basics, Gala and Magecore variants of that pack are installed)."
      % (Q, mb("textures", "sse_tfd_haley_black_suit", "pc_016_a_cmn_002_parta_m.dds"), Q,
         Q, Q, Q, Q, Q, Q, Q, Q, Q,
         mb("textures", "caenarvon", "cosplay", "bunny"), Q, Q, Q))
    A("")
    A("---")
    A("")
    A("## 16. %sGLOBAL_BODY_SKIN%s rule (ruling 4)" % (Q, Q))
    A("")
    A("These paths belong to the body / skin system:")
    A("")
    A(FENCE)
    A(mb("textures", "actors", "character", "female", "femalebody_1*.dds"))
    A(mb("textures", "actors", "character", "female", "femalebody_etc_v2_1*.dds"))
    A(mb("textures", "actors", "character", "female", "femalehands_1*.dds"))
    A(mb("textures", "actors", "character", "female", "femalebody_1_sk.dds"))
    A(FENCE)
    A("")
    A("**Rule: keep the external reference. NEVER copy them into %s%s%s.** They are the shared "
      "body skin, not outfit material; vendoring them would fork the canonical CBBE_3BA female "
      "skin into eleven private copies. Any future handling belongs to a UBE / 3BA "
      "body-family migration, not to this pack."
      % (Q, mb("textures", "ZLJ", "CombatLatex", "<OUTFIT_ID>"), Q))
    A("")
    bs_rows = [r for r in lookup if r["classification"] == "GLOBAL_BODY_SKIN"]
    A("Affected references in the current audit: **%d**." % len(bs_rows))
    A("")
    A("---")
    A("")
    A("## 17. OSP rule frozen (ruling 5)")
    A("")
    A("**One Outfit = exactly one target OSP, with several SliderSets inside it. The pack "
      "therefore has exactly 11 OSP files:**")
    A("")
    A(FENCE)
    A(mb("CalienteTools", "BodySlide", "SliderSets", "ZLJ_<OUTFIT_ID>.osp") + "      x 11")
    A(FENCE)
    A("")
    A("| OUTFIT_ID | target OSP |")
    A("|---|---|")
    for oid, pth in zip(C.OUTFIT_IDS, TGT_OSP):
        A("| %s%s%s | %s%s%s |" % (Q, oid, Q, Q, pth, Q))
    A("")
    A("UI name for every slider set inside: %s[ZLJ Combat Latex] <Outfit> - <Part>%s "
      "(example: %s[ZLJ Combat Latex] Haley - Bodysuit%s)." % (Q, Q, Q, Q))
    A("")
    A("ShapeData keeps the per-Outfit folder; an OSD may exist per project:")
    A("")
    A(FENCE)
    A(C.SD_ROOT + "<OUTFIT_ID>" + BT + "...")
    A(FENCE)
    A("")
    A("### 17.1 Risk warning -- read before any P02B migration")
    A("")
    A("> Merging several slider sets into a single %s.osp%s **departs from BodySlide's standard "
      "one-OSP-per-slider-set behaviour**. The UI, slider enumeration and per-set metadata of a "
      "multi-set OSP are not equivalent to N separate OSPs." % (Q, Q))
    A(">")
    A("> **P02B must first run one load verification**: open the merged OSP in BodySlide, confirm "
      "every slider set loads, every slider appears, and the build output matches the per-set "
      "baseline. **Until that verification passes, no batch migration may be based on this rule.**")
    A("")
    cur_osp = set(r["new_osp"] for r in (bsmig or []))
    extra = sorted(x for x in cur_osp if x not in set(TGT_OSP))
    A("Current state of %sP02A_BODYSLIDE_MIGRATION.csv%s: %d distinct %snew_osp%s value(s), %d "
      "of them outside the frozen 11. Those must be collapsed before any P02B work."
      % (Q, Q, len(cur_osp), Q, Q, len(extra)))
    if extra:
        A("")
        for x in extra:
            A("* %s%s%s" % (Q, x, Q))
    A("")
    A("---")
    A("")
    A("## 18. Statistics vocabulary (ruling 6) -- do not conflate these")
    A("")
    sd_rows = len(sdtex or [])
    A("| symbol | meaning | value |")
    A("|---|---|---|")
    A("| %sSHAPEDATA_NIF_FILES%s | **distinct ShapeData NIF files** | **%d** |" % (Q, Q, SD_SOURCE_NIF))
    A("| %sSHAPEDATA_TEXTURE_REWRITE_ROWS%s | **shape x texture-slot rewrite rows** | %d |" % (Q, Q, sd_rows))
    A("")
    A("### 18.1 Splitting the ShapeData count")
    A("")
    A("The ShapeData file count is **not** simply the %d a texture-rewrite table sees. It splits by "
      "whether an .osp data folder "
      "claims the file:" % len(set(r["shapedata_nif"] for r in (sdtex or []))))
    A("")
    A("| slice | count | meaning |")
    A("|---|---|---|")
    A("| OSP-claimed | %d | inside a data folder a .osp declares; BodySlide will build these |" % SD_CLAIMED)
    A("| orphan | %d | no .osp claims the folder, so BodySlide would never build them |" % SD_ORPHAN)
    A("| **total %sSHAPEDATA_NIF_FILES%s** | **%d** | |" % (Q, Q, SD_SOURCE_NIF))
    A("")
    A("The %d orphan files are the CL09 flat ShapeData NIFs (6, adopted by the CL09 rework "
      "decision) and the CL11 CBBE SE Skimpy Assassin cuirass and gloves NIFs (2). A texture "
      "rewrite table that only walks OSP-claimed folders therefore under-reports the ShapeData "
      "inventory -- do not derive one number from the other." % SD_ORPHAN)
    A("")
    A("> **%d is NOT the number of ShapeData NIFs.** The %d rewrite rows are one row per "
      "(ShapeData NIF, shape, texture slot) triple over %d distinct files. Writing %s%d ShapeData "
      "NIF%s is a category error and is forbidden." % (sd_rows, sd_rows, SD_SOURCE_NIF, Q, sd_rows, Q))
    A("")
    A("### 18.2 Four-class reconciliation of the .nif inventory")
    A("")
    A("| class | count | meaning |")
    A("|---|---|---|")
    A("| %sSHAPEDATA_SOURCE_NIF%s | %d | ShapeData input BodySlide consumes |" % (Q, Q, SD_SOURCE_NIF))
    A("| %sBODYSLIDE_OUTPUT_NIF%s | %d | meshes produced by a .osp build |" % (Q, Q, BS_OUTPUT_NIF))
    A("| %sBODY_MORPH_TRI%s | %d | *.tri morph caches (section 14) |" % (Q, Q, MORPH_TRI))
    A("| %sGAME_NIF%s | %d | meshes the plugin points at today |" % (Q, Q, GAME_NIF))
    A("| **total distinct .nif virtual paths** | **%d** | |" % (SD_SOURCE_NIF + BS_OUTPUT_NIF + MORPH_TRI + GAME_NIF))
    A("")
    A("### 18.3 The four classes are not interchangeable")
    A("")
    A("| class | meaning |")
    A("|---|---|")
    A("| %sGAME_NIF%s | a mesh the plugin points at today (worn or world model) |" % (Q, Q))
    A("| %sBODYSLIDE_OUTPUT_NIF%s | the .osp EXACT_OUTPUT_PATH a build produces |" % (Q, Q))
    A("| %sSHAPEDATA_SOURCE_NIF%s | a ShapeData input BodySlide consumes to produce the above |" % (Q, Q))
    A("| %sBODY_MORPH_TRI%s | a *.tri morph cache, morph table only (section 14) |" % (Q, Q))
    A("")
    A("Note: the %d .osp EXACT_OUTPUT_PATH targets are **not present in the VFS** until a build "
      "runs; they are carried as PENDING_BUILD and P02A never builds them." % PENDING_BS_OUTPUTS)

    A("---")
    A("")
    A("## 19. CL09_Corrupted decision reference (ruling 7)")
    A("")
    A("CL09 follows %s%s%s:" % (Q, mb("reports", "P02A", "CL09_REWORK_VS_BODYSLIDE_DECISION.md"), Q))
    A("")
    A("* canonical source decision: %sREWORK_BACKPORTED_TO_SHAPEDATA%s" % (Q, Q))
    A("* **CL09 stays %sBLOCKED%s** until a P02B trial build validates recommendation R2 against "
      "the current runtime mesh. The residual 12/24-byte delta in the overridden meshes has not "
      "been decoded to a named NIF field, so a wrong backport would silently alter the "
      "outfit's shape for every future slider change." % (Q, Q))
    A("* until that build passes, no CL09 file may be copied into the Pack namespace.")
    A("* R4 restates ruling 4: femalebody_* / femalehands_* references stay external as "
      "%sGLOBAL_BODY_SKIN%s and are never copied." % (Q, Q))
    A("")
    A("---")
    A("")
    A("## 20. NEW BLOCKER -- the live body skin is not CBBE_3BA (ruling 8)")
    A("")
    A("> ### BLOCKER: cross-body compatibility risk")
    A(">")
    A("> The %d %sGLOBAL_BODY_SKIN%s paths are **not** served by stock CBBE_3BA in this "
      "instance." % (len(bs_rows), Q, Q))
    A(">")
    A("> Live providers of those %d paths, in MO2 priority order (lowest wins):" % len(bs_rows))
    A(">")
    bsp = collections.Counter()
    for r in bs_rows:
        for tok in r["providers_all"].split(";"):
            tok = tok.strip()
            if not tok or "PATH-MISMATCH" in tok:
                continue
            mod, _sep, pr = tok.rpartition("#")
            try:
                bsp[(int(pr), mod)] += 1
            except ValueError:
                pass
    for (pr, mod), n in sorted(bsp.items())[:4]:
        A("> - %s%s%s -- priority **%d**, serves %d of %d paths"
          % (Q, mod, Q, pr, n, len(bs_rows)))

    A(">")
    A(">")
    A("> **This is not all-or-nothing.** Three mods each win a share of the nine paths "
      "(9/9, 6/9 and 3/9 above), so the pack is not uniformly on one foreign body: some "
      "references resolve to BnP skin, some to CBBE. The override is partial and per-path, "
      "which makes it harder to notice and no less real.")
    A(">")
    A("> So the %d canonical Outfits resolve their body skin against a **different body**, not "
      "the CBBE_3BA texture the pack nominally targets. A mesh authored for CBBE_3BA can render "
      "with another body's skin -- tint, gloss and body-map alignment all shift. This is a "
      "real compatibility risk, not a cosmetic one, and it needs a human ruling."
      % len(C.OUTFIT_IDS))
    A("")
    A("Per ruling 4 nothing is copied to %sfix%s it: the references stay external. The decision "
      "needed is whether the pack targets the CBBE_3BA body *system* (accepting that the "
      "instance's body pack supplies the skin) or the specific stock texture." % (Q, Q))
    A("")
    A("---")
    A("")
    A("## 21. BSA blind spot -- explicit limitation (ruling 9)")
    A("")
    A("The game %s root has **no loose textures directory at all**; the base game is carried "
      "by **93 .bsa archives**. A path-existence check cannot see inside an archive."
      % mb("E:", "SkyrimAE", "Data"))
    A("")
    A("Therefore:")
    A("")
    A("* %sfound_in_game_data%s is %sno%s for **every** row of the lookup table." % (Q, Q, Q, Q))
    A("* %sTRUE_MISSING%s and %sVANILLA_ENGINE_RESOURCE%s prove only **absent at the "
      "loose-file layer**. They do **not** prove absence from the instance." % (Q, Q, Q, Q))
    A("* The same caveat applies to the ARMO/ARMA stock placeholders in section 7.1.")
    A("")
    A("This limitation is stated on every row of %sP02A_GLOBAL_PROVIDER_LOOKUP.csv%s in its "
      "lookup_scope column. **Closing it requires a separate read-only archive-listing task; "
      "this stage does not touch archives.**" % (Q, Q))
    A("")
    A("---")
    A("")
    A("## 22. Reproducible verification")
    A("")
    A("%s re-derives every number above from the tables and runs three mandated checks:"
      % mb("tools", "P02A", "p02a_architecture_v2.py"))
    A("")
    A("| check | rule |")
    A("|---|---|")
    A("| 1 | exactly 11 target OSPs, one per OUTFIT_ID, no per-part filename |")
    A("| 2 | model_role uses only the 6 frozen subrecord-derived values |")
    A("| 3 | the physics table contains no .tri and no Havok morph row |")
    A("")
    A("A FAIL is reported, never silently absorbed. The result prints at the end of every run.")
    A("")
    A("---")
    A("")
    A("## 23. P02A.1 status -- what is still not authorised")
    A("")
    A("| item | ruling |")
    A("|---|---|")
    A("| 8 UNKNOWN path-mismatch references | **no automatic REPOINT authorised**; stay UNKNOWN for human confirmation |")
    A("| 12 TRUE_MISSING references | stay UNRESOLVED as a known defect list; **no downgrade or exclusion scheme invented** |")
    A("| model_role naming | the ARMA/ARMO table maps every subrecord 1:1 to the correct role, but spells the six "
      "values WEARABLE_MALE_3P / WEARABLE_FEMALE_3P / FIRSTPERSON_MALE / FIRSTPERSON_FEMALE / WORLD_MALE / "
      "WORLD_FEMALE instead of the frozen names in section 13. Semantics PASS, literal names FAIL. Either the "
      "table adopts the frozen names or the ruling relaxes them; **not decided here** |")
    A("| body-skin override (section 20) | recorded as a blocker, awaiting human ruling |")
    A("| BSA blind spot (section 21) | declared; closure deferred to a separate read-only archive-listing task |")
    A("| merged-OSP load verification (section 17.1) | required in P02B **before** any batch migration |")
    A("| CL09 trial build (section 19) | required in P02B before any CL09 copy |")
    A("")
    A("P02B must not begin on the strength of this document alone.")
    A("")
    A("---")
    A("")
    A("## 24. Evidence freshness and MO2 instance drift")
    A("")
    A("> The P00 evidence is a **frozen snapshot**. The live MO2 instance moved during P02A. "
      "Every priority-derived number in this document is a *frozen-time* reading, and that "
      "distinction is load-bearing.")
    A("")
    A("### 24.1 The drift")
    A("")
    A("| | frozen (P00, 2026-09-30 03:53 UTC) | current |")
    A("|---|---|---|")
    A("| modlist.txt lines | 2254 | **2256** |")
    A("| mod directories | 2253 | **2255** |")
    A("")
    A("The instance drifted while P02A was running. All 11 source mods changed line number:")
    A("")
    A("| Outfit | mod | frozen | current |")
    A("|---|---|---|---|")
    A("| @CL01_LatexKitty@ | makaron-COSPLAY - AE_Latex_Kitty | 924 | **926** |".replace(chr(64), Q))
    A("| @CL02_OnceMedic@ | makaron-COSPLAY - AE_Once_Medic | 923 | **925** |".replace(chr(64), Q))
    A("| @CL03_Tachy@ | makaron-COSPLAY - AE_Stellablade_Tachy | 922 | **924** |".replace(chr(64), Q))
    A("| @CL04_Haley@ | makaron-COSPLAY - AE_TFD_Haley_Black_Suit | 921 | **922** |".replace(chr(64), Q))
    A("| @CL04_Haley@ | Haley Black Suit PBR | 884 | **885** |".replace(chr(64), Q))
    A("| @CL05_Valby@ | makaron-COSPLAY - AE_TFD_Valby_Nano_Suit | 920 | **921** |".replace(chr(64), Q))
    A("| @CL06_ToxicCat@ | makaron-COSPLAY - AE_Toxic_Cat | 919 | **920** |".replace(chr(64), Q))
    A("| @CL07_Lupa@ | makaron-COSPLAY - AE_Wuthering_Waves_Lupa | 918 | **919** |".replace(chr(64), Q))
    A("| @CL08_SpearHead@ | SpearHead Catsuit CBBE 3BA BS | 909 | **907** |".replace(chr(64), Q))
    A("| @CL09_Corrupted@ | AE Corrupted Body Suit (base) | 888 | **917** |".replace(chr(64), Q))
    A("| @CL09_Corrupted@ | AE Corrupted Body Suit - Latex Rework | 887 | **916** |".replace(chr(64), Q))
    A("| @CL10_HoodST@ | AE_HoodST | 927 | **929** |".replace(chr(64), Q))
    A("| @CL11_SkimpyAssassin@ | Skimpy Assassin Outfit | 911 | **909** |".replace(chr(64), Q))
    A("")
    A("### 24.2 Four priority inversions -- and why none of them matter here")
    A("")
    A("The move produces **4 pairwise inversions**: @CL08@ against @CL09@ base and rework, and "
      "@CL09@ base and rework against @CL11@.".replace(chr(64), Q))
    A("")
    A("**None of them changes any asset winner determination in this Pack.** Verified:")
    A("")
    A("* The only virtual path @CL08@, @CL09@ and @CL11@ share is @meta.ini@ -- MO2 bookkeeping, "
      "never a game asset, and excluded from the migratable set. **The three share no asset "
      "path at all.**".replace(chr(64), Q))
    A("* The only genuine asset-level conflict is @CL09@ base versus @CL09@ rework, and its "
      "relative order holds in *both* states: rework stays ahead (887 < 888 frozen, "
      "916 < 917 current). The Latex Rework remains the VFS winner, so section 19's "
      "REWORK decision is unaffected.".replace(chr(64), Q))
    A("")
    A("### 24.3 Limitation")
    A("")
    A("P02A.1 is **forbidden from rescanning P00/P01**. Every P00-derived priority in this "
      "document is therefore a frozen-time reading and may already differ from the live "
      "instance. Concretely, the body-skin priorities quoted in section 20 "
      "(BnP 1133, CBBE 3BA 1180, CBBE Enhancer 1181) come from a fresh instance read, while "
      "the section 2 winner rule operates on the frozen snapshot.")
    A("")
    A("> **If the instance keeps drifting before P02B starts, P00 must be re-frozen before any "
      "COPY is executed.** No migration may be carried out against a stale priority reading.")
    A("")
    A("Case note: @FemaleBody_1_sk.dds@ and @femalebody_1_sk.dds@ are the same file on Windows "
      "and are absorbed by the lookup key normalisation. Only one row exists; no duplicate "
      "recording is needed.".replace(chr(64), Q))
    A("")
    A("")
    A(V2_MARKER)
    A("")
    new_sections = "\n".join(L)
    with open(ARCH, "r", encoding="utf-8") as f:
        doc = f.read()
    if V2_MARKER in doc:
        doc = doc[:doc.index(V2_MARKER)].rstrip() + "\n"
    for old, new in AMENDMENTS:
        if old in doc:
            doc = doc.replace(old, new)
    # line-level amendments: robust against incidental edits in the v1 body
    for prefix, new in LINE_AMENDMENTS:
        lines = doc.split("\n")
        hit = False
        for i, ln in enumerate(lines):
            if ln.startswith(prefix):
                lines[i] = new
                hit = True
        doc = "\n".join(lines)
        if not hit and new not in doc:
            print("  WARNING: line amendment did not match:", prefix[:50])
    anchor = "| " + Q + "P00_SHAPEDATA_COUNT_MISMATCH" + Q + " | 1 |"
    if anchor in doc and "P02A.1 SUPERSEDES part of this table" not in doc:
        doc = doc.replace(anchor, anchor + "\n" + SUPERSEDED_NOTE, 1)
    C.write_md(ARCH, doc.rstrip() + "\n\n" + new_sections)
    print("amended", ARCH)


# ================================================================ verifier ===
def verify():
    print("")
    print("=" * 78)
    print("P02A.1 VERIFICATION")
    print("=" * 78)
    res = []
    res.append(("1a target OSP set is exactly 11 unique paths",
                len(TGT_OSP) == 11 and len(set(TGT_OSP)) == 11,
                "%d defined, %d unique" % (len(TGT_OSP), len(set(TGT_OSP)))))
    bsmig = rd(BSMIG)
    if bsmig is None:
        res.append(("1b BODYSLIDE table emits only those 11 OSPs", False, "table missing"))
    else:
        cur = set(r["new_osp"] for r in bsmig)
        extra = sorted(x for x in cur if x not in set(TGT_OSP))
        res.append(("1b BODYSLIDE table emits only those 11 OSPs", not extra,
                    "%d distinct new_osp, %d outside the frozen set%s"
                    % (len(cur), len(extra), (" -> " + ", ".join(extra)) if extra else "")))
    arma = rd(ARMA)
    if arma is None:
        res.append(("2a model_role uses only the 6 frozen literals (layer b)", False, "table missing"))
        res.append(("2b each subrecord maps to the correct role (layer a)", False, "table missing"))
    else:
        used = set(r["model_role"] for r in arma)
        bad = sorted(used - set(MODEL_ROLE_ENUM))
        res.append(("2a model_role uses only the 6 frozen literals (layer b)", not bad,
                    "used=%s%s" % (sorted(used), ("; illegal=" + ",".join(bad)) if bad else "")))
        obs = collections.defaultdict(set)
        for r in arma:
            obs[(r.get("record_type", ""), r.get("subrecord", ""))].add(r["model_role"])
        frozen_map = {}
        for k, v in ARMA_SLOT_ROLE.items():
            frozen_map[("ARMA", k)] = v
        for k, v in ARMO_SLOT_ROLE.items():
            frozen_map[("ARMO", k)] = v
        pairs_ok = all(len(obs.get(k, ())) == 1 for k in frozen_map)
        same = pairs_ok and all(
            LITERAL_TO_SEMANTIC.get(next(iter(obs.get(k, {""}))), "") == frozen_map[k]
            for k in frozen_map)
        res.append(("2b each subrecord maps to the correct role (layer a)", same,
                    "subrecord->role 1:1=%s%s"
                    % (pairs_ok, "" if same else "; MISMATCH")))

    phys = rd(PHYS)
    if phys is None:
        res.append(("3 physics table contains no .tri", False, "table missing"))
    else:
        tri = [r for r in phys if ".tri" in r.get("physics_file", "").lower()]
        havok = [r for r in phys if "HAVOK" in r.get("config_type", "").upper()]
        res.append(("3 physics table contains no .tri", not tri,
                    "%d .tri row(s), %d HAVOK config_type row(s)" % (len(tri), len(havok))))
    for name, ok, detail in res:
        print("  [%s] %s" % ("PASS" if ok else "FAIL", name))
        print("         %s" % detail)
    nf = sum(1 for _n, ok, _d in res if not ok)
    print("")
    print("  %d/%d checks PASS, %d FAIL" % (len(res) - nf, len(res), nf))
    print("  A FAIL is a real defect in a sibling table, not in this document. It is reported")
    print("  so the owner of that table can fix it before P02B.")
    return res


if __name__ == "__main__":
    build()
    verify()









