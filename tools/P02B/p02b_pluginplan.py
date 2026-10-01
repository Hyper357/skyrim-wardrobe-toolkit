# -*- coding: utf-8 -*-
"""P02B_CL06_PILOT_PLUGIN_PLAN.csv - canonicalized (P02B2.2).

Two path concepts, never mixed:

  target_virtual_mesh_path   physical / virtual file, rooted at Data\\
                             e.g. meshes\\ZLJ\\CombatLatex\\CL06_ToxicCat\\AE_Toxic_Cat_1.nif
  target_plugin_model_path   what the ARMA/ARMO model field actually stores, which is
                             relative to Data\\meshes\\
                             e.g. ZLJ\\CombatLatex\\CL06_ToxicCat\\AE_Toxic_Cat_1.nif

new_value holds the plugin field value: the model filename for ARMA, the texture path for
TXST (texture fields are relative to Data\\, so textures\\... stays as-is), and the old
value for records that must not change.

Classification (no ARMA+WORLD_MODEL class exists):
  MODEL_PATH_REPOINT, GENDER_NEUTRAL_SHARED_REPOINT, MALE_SLOT_EMPTY,
  ARMO_WORLD_NO_CHANGE, TXST_REPOINT
"""
import csv
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "P02A"))
import p02a_common as C

OUTFIT = "CL06_ToxicCat"
REPORTS = os.path.join(C.ROOT, "reports", "P02B")
PLAN = os.path.join(REPORTS, "P02B_CL06_PILOT_PLUGIN_PLAN.csv")
GATE = os.path.join(REPORTS, "P02B_CL06_PLUGIN_PLAN_GATE.csv")
STAGING = os.path.join(C.ROOT, "staging", "ZLJ Combat Latex Pack - P02B Pilot")
HEADER = ["outfit_id", "record_type", "formid", "edid", "source_plugin", "slot_field",
          "old_value", "new_value", "target_virtual_mesh_path", "target_plugin_model_path",
          "change_class", "must_override", "reason"]

NEUTRAL_HINT = ("headacc", "mask")


def R(f):
    with open(os.path.join(C.OUT, f), encoding="utf-8-sig", newline="") as fh:
        return [r for r in csv.DictReader(fh) if (r.get("OUTFIT_ID") or "") == OUTFIT]


def canonical_by_output_file():
    """output_file (lower) -> physical virtual mesh path, from the corrected matrix."""
    p = os.path.join(REPORTS, "P02B_CL06_BODYSLIDE_ARMA_MATRIX.csv")
    m = {}
    if not os.path.exists(p):
        return m
    with open(p, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            op = (r.get("output_path") or "").replace("/", "\\").strip("\\")
            of = (r.get("output_file") or "").strip()
            if not op or not of:
                continue
            if not op.lower().startswith("meshes\\"):
                op = "meshes\\" + op
            m[of.lower()] = op + "\\" + of + "_1.nif"
    return m


def canonical_from_mesh_ledger():
    """source NIF basename -> target virtual path, from the mesh migration ledger.

    Needed for meshes BodySlide does not build (HeadACC, Mask): they never appear in
    the BodySlide matrix. Targets under male\\ or 1p\\ are ignored - those are the
    artificial splits the topology rule forbids.
    """
    p = os.path.join(C.OUT, "P02A_MESH_MIGRATION.csv")
    m = {}
    if not os.path.exists(p):
        return m
    with open(p, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if (r.get("OUTFIT_ID") or "") != OUTFIT:
                continue
            if (r.get("mesh_class") or "").upper() != "GAME_NIF":
                continue
            src = os.path.basename((r.get("source_virtual_path") or "").replace("/", "\\")).lower()
            tgt = (r.get("target_virtual_path") or "").replace("/", "\\")
            if not src or not tgt:
                continue
            if "\\male\\" in tgt.lower() or "\\1p\\" in tgt.lower():
                continue
            m.setdefault(src, tgt)
    return m


def to_plugin_path(virtual_mesh_path):
    """Data\\meshes\\X  ->  X  (the value an ARMA/ARMO model field stores)."""
    v = (virtual_mesh_path or "").replace("/", "\\")
    if v.lower().startswith("meshes\\"):
        return v[len("meshes\\"):]
    if v.lower().startswith("data\\meshes\\"):
        return v[len("data\\meshes\\"):]
    return v


def main():
    rows = []
    cmap = canonical_by_output_file()
    mmap = canonical_from_mesh_ledger()
    print("canonical map entries (bodyslide):", len(cmap), "| mesh-ledger fallback:", len(mmap))
    for k in sorted(cmap)[:6]:
        print("   ", k, "->", cmap[k])
    for k in sorted(mmap)[:8]:
        print("   fallback", k, "->", mmap[k])

    for r in R("P02A_ARMA_MODEL_REWRITE.csv"):
        rtype = (r.get("record_type") or "ARMA").upper()
        slot = r.get("subrecord", "")
        old = (r.get("old_path") or "").replace("/", "\\")
        neutral = any(h in old.lower() for h in NEUTRAL_HINT)
        of = os.path.basename(old).lower()
        of = of.rsplit("_", 1)[0] if of.endswith(("_0.nif", "_1.nif")) else of.replace(".nif", "")
        virt = cmap.get(of, "")
        if not virt:
            virt = mmap.get(os.path.basename(old).lower(), "")

        if rtype == "ARMO":
            rows.append([OUTFIT, "ARMO", r.get("formid", ""), r.get("edid", ""), "AE_Toxic_Cat.esp",
                         slot, old, old, "", "", "ARMO_WORLD_NO_CHANGE", "NO",
                         "RULING-03: ARMO owns the world/inventory model; global vanilla mesh stays external"])
        elif neutral:
            plugin = to_plugin_path(virt)
            rows.append([OUTFIT, "ARMA", r.get("formid", ""), r.get("edid", ""), "AE_Toxic_Cat.esp",
                         slot, old, plugin, virt, plugin, "GENDER_NEUTRAL_SHARED_REPOINT", "YES",
                         "RULING-01 exception: outfit-owned neutral asset; MOD2 and MOD3 share ONE nif"])
        elif slot in ("MOD2", "MOD4"):
            rows.append([OUTFIT, "ARMA", r.get("formid", ""), r.get("edid", ""), "AE_Toxic_Cat.esp",
                         slot, old, "", "", "", "MALE_SLOT_EMPTY", "YES",
                         "RULING-01: external male body branch (Armor\\Studded\\Male) - male field emptied"])
        else:
            plugin = to_plugin_path(virt)
            rows.append([OUTFIT, "ARMA", r.get("formid", ""), r.get("edid", ""), "AE_Toxic_Cat.esp",
                         slot, old, plugin, virt, plugin, "MODEL_PATH_REPOINT", "YES",
                         "canonical female wearable; target topology SHARED_RUNTIME_MESH"])

    for r in R("P02A_PLUGIN_TEXTURE_REWRITE.csv"):
        dep = (r.get("dependency_type") or "").upper()
        old = (r.get("old_dds") or "").replace("/", "\\")
        new = (r.get("new_dds") or "").replace("/", "\\")
        if dep == "VANILLA":
            rows.append([OUTFIT, r.get("record_type", "TXST"), r.get("formid", ""), r.get("edid", ""),
                         "AE_Toxic_Cat.esp", r.get("subrecord", ""), old, old, "", "", "TXST_NO_CHANGE",
                         "NO", "engine/global texture stays external"])
        else:
            rows.append([OUTFIT, r.get("record_type", "TXST"), r.get("formid", ""), r.get("edid", ""),
                         "AE_Toxic_Cat.esp", r.get("subrecord", ""), old, new, "", "", "TXST_REPOINT",
                         "YES", "texture field is relative to Data\\; textures\\ prefix is correct here"])

    C.write_csv(PLAN, HEADER, rows)

    # ------------------------- gate -------------------------
    cls = Counter(r[10] for r in rows)
    mesh_rows = [r for r in rows if r[1] == "ARMA"]
    g = []

    def add(cid, name, expected, actual, ok, detail=""):
        g.append([cid, name, expected, actual, "PASS" if ok else "FAIL", detail])

    bad_prefix = [r for r in mesh_rows if r[8] and r[8].lower().startswith("meshes\\")
                  and r[10] in ("MODEL_PATH_REPOINT", "GENDER_NEUTRAL_SHARED_REPOINT")
                  and (r[9] or "").lower().startswith("meshes\\")]
    add("G1", "PLUGIN_MODEL_PATH_STARTS_WITH_MESHES", "0",
        sum(1 for r in rows if r[10] in ("MODEL_PATH_REPOINT", "GENDER_NEUTRAL_SHARED_REPOINT")
            and (r[9] or "").lower().startswith("meshes\\")),
        all(not (r[9] or "").lower().startswith("meshes\\") for r in rows),
        "plugin model filenames are relative to Data\\meshes\\")

    n1p = [r for r in rows if "\\1p\\" in (r[7] or "").lower()]
    add("G2", "STALE_1P_TARGETS", "0", len(n1p), not n1p,
        "; ".join(r[3] for r in n1p[:3]))

    nmale = [r for r in rows if r[10] in ("MODEL_PATH_REPOINT", "GENDER_NEUTRAL_SHARED_REPOINT")
             and "\\male\\" in (r[7] or "").lower()]
    add("G3", "STALE_MALE_NEUTRAL_TARGETS", "0", len(nmale), not nmale,
        "; ".join(r[3] for r in nmale[:3]))

    def identical(prefix, mods):
        n = 0
        for edid in sorted({r[3] for r in rows if r[3].lower().startswith(prefix)}):
            vals = [r[9] for r in rows if r[3] == edid and r[5] in mods]
            if len(vals) == len(mods) and len(set(vals)) == 1 and vals[0]:
                n += 1
        return n

    for cid, name, prefix, mods, want in (
            ("G4", "BODY_MOD3_MOD5_TARGET_IDENTICAL", "ae_toxic_cat_body", ("MOD3", "MOD5"), 3),
            ("G5", "HANDS_MOD3_MOD5_TARGET_IDENTICAL", "ae_toxic_cat_hand", ("MOD3", "MOD5"), 3),
            ("G6", "HEADACC_MOD2_MOD3_TARGET_IDENTICAL", "ae_toxic_cat_headacc", ("MOD2", "MOD3"), 3),
            ("G7", "MASK_MOD2_MOD3_TARGET_IDENTICAL", "ae_toxic_cat_mask", ("MOD2", "MOD3"), 3)):
        n = identical(prefix, mods)
        add(cid, name, "%d/%d" % (want, want), "%d/%d" % (n, want), n == want,
            "same plugin model filename across the listed slots")

    add("G8", "MALE_SLOT_EMPTY", "18", cls["MALE_SLOT_EMPTY"], cls["MALE_SLOT_EMPTY"] == 18, "")
    add("G9", "ARMO_WORLD_NO_CHANGE", "21", cls["ARMO_WORLD_NO_CHANGE"], cls["ARMO_WORLD_NO_CHANGE"] == 21, "")
    add("G10", "TXST_REPOINT", "22", cls["TXST_REPOINT"], cls["TXST_REPOINT"] == 22, "")

    virt_missing = []
    for r in rows:
        if r[8]:
            p = os.path.join(STAGING, r[8].replace("\\", os.sep))
            if not os.path.isfile(p):
                virt_missing.append(r[8])
    add("G11", "VIRTUAL_MESH_PATH_EXISTS", "0 missing", "%d missing" % len(virt_missing),
        not virt_missing, "; ".join(sorted(set(virt_missing))[:3]))

    plug_missing = []
    for r in rows:
        if r[9] and r[10] in ("MODEL_PATH_REPOINT", "GENDER_NEUTRAL_SHARED_REPOINT"):
            p = os.path.join(STAGING, "meshes", r[9].replace("\\", os.sep))
            if not os.path.isfile(p):
                plug_missing.append(r[9])
    add("G12", "PLUGIN_MODEL_PATH_MAPS_BACK", "0 missing", "%d missing" % len(plug_missing),
        not plug_missing, "; ".join(sorted(set(plug_missing))[:3]))

    txst_bad = [r for r in rows if r[10] == "TXST_REPOINT" and not (r[7] or "").lower()
                .startswith("textures\\zlj\\combatlatex\\cl06_toxiccat\\")]
    add("G13", "TXST_TARGET_NAMESPACE", "0 wrong", len(txst_bad), not txst_bad,
        "; ".join(r[7] for r in txst_bad[:2]))

    arma_world = [r for r in rows if r[1] == "ARMA" and "WORLD" in r[10]]
    add("G14", "NO_ARMA_WORLD_MODEL_CLASS", "0", len(arma_world), not arma_world, "")

    C.write_csv(GATE, ["check_id", "check_name", "expected", "actual", "result", "detail"], g)
    print()
    print("plan rows:", len(rows))
    for k, v in cls.most_common():
        print("   %-32s %d" % (k, v))
    print()
    for row in g:
        print("%-5s %-38s %-10s %s" % (row[0], row[1], row[4], row[3]))
    fails = [r for r in g if r[4] == "FAIL"]
    print()
    print("PLUGIN_PLAN_STATIC_GATE =", "PASS" if not fails else "FAIL")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
