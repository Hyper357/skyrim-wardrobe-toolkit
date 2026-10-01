# -*- coding: utf-8 -*-
r"""P02A.1 - rebuild P02A_ARMA_MODEL_REWRITE.csv with AUTHORITATIVE ARMA/ARMO slot semantics.

Why this file exists
--------------------
The P02A.1 human review overturned the slot semantics that P02A derived from
path-name guessing. The review ruling is authoritative and is encoded verbatim
below (SLOT_RULING). No role is ever inferred from a file name again.

    ARMA.MOD2 = MALE_3RD_PERSON    ARMA.MOD3 = FEMALE_3RD_PERSON
    ARMA.MOD4 = MALE_1ST_PERSON   ARMA.MOD5 = FEMALE_1ST_PERSON      -> ArmorAddon wearable system
    ARMO.MOD2 = MALE_WORLD_MODEL  ARMO.MOD4 = FEMALE_WORLD_MODEL    -> inventory/drop, NEVER wearable

model_role is a closed enum:
    WEARABLE_MALE_3P, WEARABLE_FEMALE_3P, FIRSTPERSON_MALE, FIRSTPERSON_FEMALE,
    WORLD_MALE, WORLD_FEMALE, and the sentinel UNKNOWN_SLOT.

Canonical rule (frozen): canonical body = CBBE_3BA **female**, therefore
WEARABLE_FEMALE_3P is the canonical runtime wearable mesh and is the only role
with canonical_runtime=YES. Every other role is kept with provenance but is kept
in its own sub-directory inside the pack namespace so it can never be confused
with the canonical female mesh.

STRICT READ-ONLY. This script only:
  * reads the frozen P00 evidence through tools/P02A/p02a_common.py
  * performs targeted os.path.exists probes (never opens a .nif/.dds/.esp binary,
    never enumerates asset contents, never copies/moves/writes anything in MO2)
  * writes reports/P02A/P02A_ARMA_MODEL_REWRITE.csv and prints a summary

Re-run:  python tools/P02A/p02a_arma_v2.py
"""
from __future__ import annotations

import collections
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

import p02a_common as C  # noqa: E402

P = C.P00.get()
OUT_CSV = os.path.join(C.OUT, "P02A_ARMA_MODEL_REWRITE.csv")

PLUGIN_SET = {C.OUTFITS[o]["plugin"] for o in C.OUTFIT_IDS}
MODS_ROOT = r"E:\SkyrimAE\mo2\mods"
DATA_ROOT = r"E:\SkyrimAE\Data"

CANONICAL_BODY = "CBBE_3BA"
CANONICAL_GENDER = "FEMALE"
TARGET_PLUGIN = C.TARGET_PLUGIN

# ---------------------------------------------------------------------------
# authoritative slot ruling (human review, P02A.1) - DO NOT derive from paths
# ---------------------------------------------------------------------------
SLOT_RULING = {
    ("ARMA", "MOD2"): ("WEARABLE_MALE_3P",   r"male",  "ARMA.MOD2=MALE_3RD_PERSON (review ruling; ArmorAddon wearable system)"),
    ("ARMA", "MOD3"): ("WEARABLE_FEMALE_3P", "",      "ARMA.MOD3=FEMALE_3RD_PERSON (review ruling; = canonical CBBE_3BA female wearable)"),
    ("ARMA", "MOD4"): ("FIRSTPERSON_MALE",   r"male\1p", "ARMA.MOD4=MALE_1ST_PERSON (review ruling)"),
    ("ARMA", "MOD5"): ("FIRSTPERSON_FEMALE", r"1p",   "ARMA.MOD5=FEMALE_1ST_PERSON (review ruling)"),
    ("ARMO", "MOD2"): ("WORLD_MALE",         r"world\male",   "ARMO.MOD2=MALE_WORLD_MODEL (review ruling; inventory/drop model, NEVER wearable)"),
    ("ARMO", "MOD4"): ("WORLD_FEMALE",       r"world\female", "ARMO.MOD4=FEMALE_WORLD_MODEL (review ruling; inventory/drop model, NEVER wearable)"),
}
CANONICAL_ROLE = "WEARABLE_FEMALE_3P"

HEADER = [
    "OUTFIT_ID", "source_plugin", "formid", "edid", "record_type", "subrecord",
    "model_role", "slot_evidence", "old_path", "new_path", "mesh_role",
    "canonical_runtime", "canonical_reason", "body_relevance",
    "target_outfit_match", "status", "unresolved_class", "collision_check", "notes",
    # traceability extras (review allows extra columns)
    "old_vpath", "existence", "provider_mod", "provider_priority",
    "provider_in_p00_scope", "shadowed_providers", "sha256",
]

BBP_VARIANT_RE = re.compile(r"(?i)(_1|_0|_go)\.nif$")
STOCK_SLOT_RE = re.compile(r"(?i)^armor\\studded\\")


def bs(s):
    return str(s or "").replace("/", "\\").strip().strip('"')


def v_mesh(model_ref):
    s = bs(model_ref)
    if not s:
        return ""
    return s if s.lower().startswith("meshes\\") else "meshes\\" + s


def mesh_role_token(model_ref):
    m = BBP_VARIANT_RE.search(bs(model_ref))
    if not m:
        return "PLAIN_NIF"
    return {"_1": "PHYSICS_1", "_0": "PHYSICS_0", "_go": "STATIC_GO"}[m.group(1).lower()]


def own_mods(oid):
    return set(P.mods_of_outfit(oid))


# ---------------------------------------------------------------------------
# targeted existence probe - bounded to the vpaths the frozen P00 VFS cannot
# resolve, plus every stock-slot vpath (which P00 never indexes because P00 only
# indexes the 56 in-scope MO2 mods, not Skyrim.esm/BSA or out-of-scope mods).
# ---------------------------------------------------------------------------
_PROBED = {}


def probe(vp):
    """Return (state, provider_mod) with state in FOUND_GAME_DATA / FOUND_MOD / NOT_PROBEABLE_BSA / NOT_FOUND."""
    if vp in _PROBED:
        return _PROBED[vp]
    res = ("NOT_FOUND", "")
    if os.path.exists(os.path.join(DATA_ROOT, *vp.split("\\"))):
        res = ("FOUND_GAME_DATA", "Skyrim.esm/Data")
    else:
        try:
            dirs = os.listdir(MODS_ROOT)
        except OSError:
            dirs = []
        for d in dirs:
            if os.path.exists(os.path.join(MODS_ROOT, d, *vp.split("\\"))):
                res = ("FOUND_MOD", d)
                break
    _PROBED[vp] = res
    return res


PROBE_ROOTS = "E:\\SkyrimAE\\Data + all %d MO2 mod directories" % len(os.listdir(MODS_ROOT))


# ---------------------------------------------------------------------------
# build rows
# ---------------------------------------------------------------------------
def build():
    rows = []
    for oid in C.OUTFIT_IDS:
        pf = C.OUTFITS[oid]["plugin"]
        own = own_mods(oid)
        noncanon = "NON_CANONICAL_BODY" in C.OUTFITS[oid].get("support", {})
        noncanon_val = C.OUTFITS[oid]["support"].get("NON_CANONICAL_BODY", "")
        for rec in sorted(P.records_of_plugin.get(pf, []),
                          key=lambda r: (r["record_type"], r["formid"])):
            rt = rec["record_type"]
            if rt not in ("ARMO", "ARMA"):
                continue
            fid = rec["formid"].upper()
            edid = ((rec["subrecords"].get("EDID") or [""])[0])
            for sk in ("MOD2", "MOD3", "MOD4", "MOD5"):
                for mref in rec["subrecords"].get(sk) or []:
                    if not str(mref).strip():
                        continue
                    key = (rt, sk)
                    role, sub_dir, evidence = SLOT_RULING[key]
                    vp = v_mesh(mref)
                    base = os.path.basename(bs(mref))
                    if not base:
                        continue

                    # ---- provider resolution: frozen P00 first, then targeted probe
                    p00win = P.winner(vp)
                    if p00win:
                        prov = p00win["mod"]
                        prov_prio = P.priority.get(prov, "")
                        in_scope = "yes" if prov in P.priority else "no"
                        existence = "RESOLVED_FROZEN_P00_VFS"
                        sha = p00win.get("sha256", "")
                        shadow = "; ".join(P.shadowed(vp))
                    else:
                        prov = ""
                        prov_prio = ""
                        in_scope = ""
                        sha = ""
                        shadow = ""
                        state, found = probe(vp)
                        if state == "FOUND_MOD":
                            prov = found
                            in_scope = "no" if found not in P.priority else "yes"
                            prov_prio = str(P.priority.get(found, "UNKNOWN"))
                            existence = "RESOLVED_BY_TARGETED_PROBE"
                        elif state == "FOUND_GAME_DATA":
                            prov = "Skyrim.esm / Data"
                            in_scope = "no"
                            existence = "RESOLVED_BY_TARGETED_PROBE_GAME_DATA"
                        else:
                            prov = ""
                            # Skyrim.esm stock meshes ship inside Data\*.bsa; the Data root has no
                            # meshes\ folder at all, so a stock-slot path can never be proven by
                            # os.path.exists. Record that honestly instead of calling it absent.
                            existence = ("NOT_PROBEABLE_SKYRIMESM_BSA_RESIDENT"
                                         if STOCK_SLOT_RE.match(bs(mref))
                                         else "NOT_FOUND_IN_DATA_OR_ANY_MOD")

                    prov_owned_by_us = prov in own
                    stock_slot = bool(STOCK_SLOT_RE.match(bs(mref)))
                    # foreign provider that overrides a stock armor slot
                    foreign_body = bool(stock_slot and not prov_owned_by_us and prov
                                        and "HIMBO" in prov)

                    # ---- body relevance
                    if stock_slot:
                        body_rel = "VANILLA_STOCK"
                    elif noncanon:
                        body_rel = "BHUNP_3BBB"
                    else:
                        body_rel = "CBBE_3BA"

                    # ---- target namespace path (role-separated on purpose)
                    new_vp = C.MESH_ROOT + oid + ("\\" + sub_dir if sub_dir else "") + "\\" + base
                    np_vp, _ = new_vp, new_vp

                    # ---- canonical runtime
                    if noncanon:
                        canon, why = "NO", ("NON_CANONICAL_BODY=%s; frozen pack canonical body is "
                                            "%s %s" % (noncanon_val, CANONICAL_BODY, CANONICAL_GENDER))
                    elif role != CANONICAL_ROLE:
                        canon, why = "NO", ("slot=%s.%s is not the canonical female wearable slot"
                                            % (rt, sk))
                    elif existence == "NOT_FOUND_IN_DATA_OR_ANY_MOD":
                        canon, why = "NO", ("canonical slot but the FEMALE_3RD_PERSON mesh cannot be "
                                            "resolved -> nothing canonical to ship")
                    else:
                        canon, why = "YES", ("ARMA.MOD3=FEMALE_3RD_PERSON == canonical %s %s wearable"
                                            % (CANONICAL_BODY, CANONICAL_GENDER))

                    # ---- target_outfit_match
                    if prov_owned_by_us:
                        match = "SELF_OWN_MOD"
                    elif stock_slot and prov and "HIMBO" in prov:
                        match = "FOREIGN_MOD_OVERRIDE_OF_STOCK_SLOT"
                    elif stock_slot:
                        match = "VANILLA_STOCK_SLOT"
                    elif prov:
                        match = "EXTERNAL_MOD"
                    else:
                        match = "NO_PROVIDER"

                    # ---- status
                    notes = ["PROBE_SCOPE=" + PROBE_ROOTS]
                    uclass = ""
                    if noncanon:
                        status = "NON_CANONICAL_SOURCE"
                        notes.append("NON_CANONICAL_BODY=" + str(noncanon_val))
                    elif existence == "NOT_FOUND_IN_DATA_OR_ANY_MOD":
                        status = "UNRESOLVED"
                        uclass = "SOURCE_ASSET_ABSENT"
                        notes.append("EXISTENCE_CHECK=os.path.exists FAILED for this exact vpath in "
                                     "E:\\SkyrimAE\\Data and in all %d MO2 mod directories"
                                     % len(os.listdir(MODS_ROOT)))
                        notes.append("SOURCE_ASSET_ABSENT_IN_INSTALLATION - needs author asset or "
                                     "P03 decision (drop slot / re-author)")
                    elif foreign_body:
                        status = "UNRESOLVED"
                        uclass = "FOREIGN_BODY_DECISION_REQUIRED"
                        notes.append("DECISION_REQUIRED: this %s slot points at a mesh provided by "
                                     "foreign male-body mod '%s', which is not %s %s"
                                     % (role, prov, CANONICAL_BODY, CANONICAL_GENDER))
                        notes.append("recommend P03: unassign the male slot or vendor a neutral mesh; "
                                     "do NOT vendor a male-body mesh into a female canonical pack")
                    else:
                        status = "COPY_AND_REPOINT"
                        if existence == "NOT_PROBEABLE_SKYRIMESM_BSA_RESIDENT":
                            notes.append("EXISTENCE=NOT PROBEABLE: E:\\SkyrimAE\\Data contains no "
                                         "meshes\\ folder at all, Skyrim stock meshes are packed "
                                         "inside Data\\*.bsa, so os.path.exists can never prove "
                                         "this vpath. Treated as Skyrim.esm stock; P03 must "
                                         "confirm the entry exists in the BSA.")
                        if in_scope == "no":
                            notes.append("PROVIDER_OUTSIDE_P00_FROZEN_SCOPE (priority UNKNOWN; "
                                         "VFS winner cannot be proven from P00)")
                            if "BodySlide" in prov:
                                notes.append("PROVIDER_IS_BODYSLIDE_BUILD_OUTPUT: this mesh is a "
                                             "generated BodySlide Build artifact, not a source asset")
                    if stock_slot:
                        notes.append("STOCK_SLOT_FAMILY=armor\\studded\\ (BBP stock armor drop mesh)")
                    if not prov and not stock_slot:
                        notes.append("NO_PROVIDER_KNOWN")

                    rows.append(dict(
                        oid=oid, pf=pf, fid=fid, edid=edid, rt=rt, sk=sk,
                        role=role, evidence=evidence, old=bs(mref), new=new_vp,
                        mesh_role=mesh_role_token(mref),
                        canon=canon, canon_why=why, body_rel=body_rel,
                        match=match, status=status, notes=notes,
                        uclass=uclass,
                        vp=vp, existence=existence, prov=prov, prio=prov_prio,
                        in_scope=in_scope, shadow=shadow, sha=sha,
                        base=base, sub_dir=sub_dir,
                    ))

    # ---- collision detection on the planned namespace path
    by_new = collections.defaultdict(set)
    for r in rows:
        by_new[(r["oid"], r["new"].lower())].add(r["old"].lower())
    used_new = collections.Counter()
    alias = collections.Counter()
    for r in rows:
        k = (r["oid"], r["new"].lower())
        if len(by_new[k]) > 1:
            r["collision"] = ("COLLISION_SAME_NEW_PATH_FROM_%d_DISTINCT_SOURCE_FILES "
                              "(%s)" % (len(by_new[k]), ";".join(sorted(by_new[k]))))
            n = used_new[k] = used_new[k] + 1
            if n > 1:
                r["new"] = r["new"][:-4] + "_DUP%d.nif" % n
                r["notes"].append("new_path DISAMBIGUATED with _DUP%d to keep the pack runnable; "
                                  "review in P03" % n)
                r["collision"] += " | RESOLVED_WITH_DUP_SUFFIX"
        else:
            r["collision"] = "OK"
        r["alias"] = (r["oid"], r["old"].lower())
    acount = collections.Counter(r["alias"] for r in rows)
    for r in rows:
        if acount[r["alias"]] > 1:
            r["notes"].append("SAME_OLD_PATH_REFERENCED_%d_TIMES_IN_THIS_OUTFIT (alias, not a "
                              "collision)" % acount[r["alias"]])

    # author-side anomaly: an ARMO world/drop model that is byte-identical to a mesh
    # its own ArmorAddon also uses as a wearable model. Recorded, never silently repaired.
    arma_of_arma_rec = collections.defaultdict(list)      # ARMA fid -> [row]
    arma_of_armo_rec = collections.defaultdict(list)      # ARMO fid -> [row]
    for r in rows:
        (arma_of_arma_rec if r["rt"] == "ARMA" else arma_of_armo_rec)[r["fid"]].append(r)
    arma_edids_by_arma = {}
    for pt in P.parts:
        if pt["plugin_file"] not in PLUGIN_SET:
            continue
        arma_edids_by_arma[(pt["plugin_file"], pt["ARMO_formid"].upper())] = str(
            pt.get("ARMA_formids") or "")
    for r in rows:
        if r["rt"] != "ARMO":
            continue
        arma_fids = []
        for tok in arma_edids_by_arma.get((r["pf"], r["fid"]), "").split(";"):
            tok = tok.strip()
            if ":" in tok:
                pl, fid = tok.rsplit(":", 1)
                if pl.lower() == r["pf"].lower():
                    arma_fids.append(fid.upper())
        wearable = set()
        for af in arma_fids:
            for ar in arma_of_arma_rec.get(af, []):
                if ar["role"].startswith("WEARABLE") or ar["role"].startswith("FIRSTPERSON"):
                    wearable.add(ar["old"].lower())
        if wearable and r["old"].lower() in wearable:
            r["notes"].append("SOURCE_SLOT_CONTENT_ALIAS: this ARMO world/drop model is the SAME "
                              "mesh its ArmorAddon uses as a wearable model (author-side); there "
                              "is no distinct drop mesh here")
    return rows


HEADER_ROWS = lambda r: [
    r["oid"], r["pf"], r["fid"], r["edid"], r["rt"], r["sk"],
    r["role"], r["evidence"], r["old"], r["new"], r["mesh_role"],
    r["canon"], r["canon_why"], r["body_rel"],
    r["match"], r["status"], r["uclass"], r["collision"], " | ".join(r["notes"]),
    r["vp"], r["existence"], r["prov"], r["prio"], r["in_scope"],
    r["shadow"], r["sha"],
]


# ---------------------------------------------------------------------------
def main():
    rows = build()
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    C.write_csv(OUT_CSV, HEADER, [HEADER_ROWS(r) for r in rows])
    print("=" * 104)
    print("P02A.1 ARMA/ARMO MODEL REWRITE  (authoritative slot semantics, READ-ONLY)")
    print("canonical body = %s %s | target plugin = %s | rows = %d"
          % (CANONICAL_BODY, CANONICAL_GENDER, TARGET_PLUGIN, len(rows)))
    print("targeted existence probe scope: %s" % PROBE_ROOTS)
    print("=" * 104)

    roles = collections.Counter(r["role"] for r in rows)
    print()
    print("== model_role census (from subrecord, never from path) ==")
    for k in sorted(roles):
        print("   %-22s %4d" % (k, roles[k]))
    print("   %-22s %4d" % ("TOTAL", sum(roles.values())))

    print()
    print("== per outfit: role -> count | canonical female set ==")
    print("%-20s %6s %6s %6s %6s %6s %6s | %8s %8s"
          % ("OUTFIT_ID", "W_M3P", "W_F3P", "FP_M", "FP_F", "WD_M", "WD_F",
             "CANON", "ROWS"))
    for oid in C.OUTFIT_IDS:
        sub = [r for r in rows if r["oid"] == oid]
        c = collections.Counter(r["role"] for r in sub)
        canon = [r for r in sub if r["canon"] == "YES"]
        print("%-20s %6d %6d %6d %6d %6d %6d | %8d %8d"
              % (oid, c["WEARABLE_MALE_3P"], c["WEARABLE_FEMALE_3P"],
                 c["FIRSTPERSON_MALE"], c["FIRSTPERSON_FEMALE"],
                 c["WORLD_MALE"], c["WORLD_FEMALE"], len(canon), len(sub)))

    canon = [r for r in rows if r["canon"] == "YES"]
    print()
    print("== canonical_runtime = YES : %d rows (ARMA.MOD3 FEMALE_3RD_PERSON) ==" % len(canon))
    byo = collections.Counter(r["oid"] for r in canon)
    for oid in C.OUTFIT_IDS:
        print("   %-20s %3d" % (oid, byo[oid]))

    print()
    print("== status census ==")
    for k, v in sorted(collections.Counter(r["status"] for r in rows).items()):
        print("   %-24s %4d" % (k, v))

    print()
    print("== body_relevance census ==")
    for k, v in sorted(collections.Counter(r["body_rel"] for r in rows).items()):
        print("   %-24s %4d" % (k, v))

    print()
    print("== target_outfit_match census ==")
    for k, v in sorted(collections.Counter(r["match"] for r in rows).items()):
        print("   %-38s %4d" % (k, v))

    print()
    print("== collisions ==")
    coll = [r for r in rows if r["collision"] != "OK"]
    print("   new_path collisions: %d" % len(coll))
    seen = set()
    for r in coll:
        k = (r["oid"], r["new"])
        if k in seen:
            continue
        seen.add(k)
        print("      %-20s %-64s %s" % (r["oid"], r["new"][:64], r["collision"][:90]))
    if not coll:
        print("      none - every planned new_path is unique inside its outfit namespace")

    # ---------------- CL08 re-classification + existence proof ---------------
    print()
    print("=" * 104)
    print("CL08_SpearHead RE-CLASSIFICATION OF THE 16 PREVIOUSLY-UNRESOLVED WEARABLE REFS")
    print("=" * 104)
    cl08_missing = {
        "catsuita01t01s_1.nif", "spearhead catsuit heel.nif",
        "gaghold for fo4 hood red.nif", "latex hood black.nif", "latex hood red.nif",
    }
    hist = [r for r in rows if r["oid"] == "CL08_SpearHead"
            and os.path.basename(r["old"]).lower() in cl08_missing]
    print("rows affected: %d" % len(hist))
    for r in hist:
        print("   %-8s %-4s %-22s %-52s %-22s %s"
              % (r["fid"], r["sk"], r["role"], os.path.basename(r["old"]), r["existence"],
                 r["status"]))
    still = [r for r in hist if r["status"] == "UNRESOLVED"]
    fixed = [r for r in hist if r["status"] != "UNRESOLVED"]
    print()
    print("   RESOLVED by targeted probe : %d  -> %s"
          % (len(fixed), sorted({os.path.basename(r['old']) for r in fixed})))
    print("   STILL UNRESOLVED            : %d  -> %s"
          % (len(still), sorted({os.path.basename(r['old']) for r in still})))
    print("   proof: os.path.exists(<vpath>) under E:\\SkyrimAE\\Data AND under all %d"
          % len(os.listdir(MODS_ROOT)))
    print("          MO2 mod directories returned False for every STILL-UNRESOLVED vpath.")

    print()
    print("== UNRESOLVED split by reason ==")
    uc = collections.Counter(r["uclass"] for r in rows if r["status"] == "UNRESOLVED")
    for k, v in sorted(uc.items()):
        print("   %-34s %4d" % (k, v))
    print()
    print("-- SOURCE_ASSET_ABSENT (os.path.exists failed everywhere) --")
    for r in rows:
        if r["uclass"] == "SOURCE_ASSET_ABSENT":
            print("   %-20s %-8s %-4s %-22s %s"
                  % (r["oid"], r["fid"], r["sk"], r["role"], os.path.basename(r["old"])))
    print()
    print("-- FOREIGN_BODY_DECISION_REQUIRED: %d rows, providers --"
          % uc.get("FOREIGN_BODY_DECISION_REQUIRED", 0))
    for m, n in collections.Counter(
            r["prov"] for r in rows if r["uclass"] == "FOREIGN_BODY_DECISION_REQUIRED").items():
        print("      %3d x %s" % (n, m))

    print()
    print("== FOREIGN PROVIDER OVERRIDES OF STOCK ARMOR SLOTS (the real finding) ==")
    fb = [r for r in rows if r["match"] == "FOREIGN_MOD_OVERRIDE_OF_STOCK_SLOT"]
    print("   rows: %d" % len(fb))
    provs = collections.Counter(r["prov"] for r in fb)
    for m, n in provs.items():
        print("      %3d x  %s" % (n, m))
    print("   -> these are %s slots whose source mesh belongs to a foreign MALE body mod."
          % "/".join(sorted({r["role"] for r in fb})))
    print("      They are NOT CBBE_3BA female content and must not be vendored as such.")

    print()
    print("== NOTE ==")
    print("  * no FormID generated, no file copied or modified, no NIF/DDS/ESP opened.")
    print("  * every existence claim is a targeted os.path.exists on that exact vpath.")
    print("  * Skyrim.esm stock meshes live inside Data\\*.bsa; E:\\SkyrimAE\\Data has no")
    print("    meshes\\ folder, so BSA-resident stock slots can never be proven by os.path.exists.")


if __name__ == "__main__":
    main()
