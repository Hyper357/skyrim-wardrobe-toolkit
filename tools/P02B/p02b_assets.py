# -*- coding: utf-8 -*-
"""P02B1 CL06_ToxicCat asset migration into staging.

Sources of truth (never a folder scan):
  P02A_MESH_MIGRATION.csv, P02A_TEXTURE_MIGRATION.csv, P02A_NIF_TEXTURE_REWRITE.csv,
  P02A_SHAPEDATA_TEXTURE_REWRITE.csv, P02A_BODYSLIDE_MIGRATION.csv.

Rulings applied:
  RULING-01 male / male-firstperson models that reference an external male body system
            are NON_CANONICAL_MALE / DO_NOT_VENDOR, unless the very same outfit-owned
            gender-neutral file is also used by a female slot.
  RULING-02 GLOBAL_BODY_SKIN stays external: never copied, never rewritten.
  RULING-03 vanilla / SMIM world-drop models stay external; an outfit's own world NIF migrates.

Everything is written under staging only. Original mods are read-only.
"""
import csv
import os
import shutil
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "P02A"))
sys.path.insert(0, HERE)
import p02a_common as C
import nif_tex as N

OUTFIT = "CL06_ToxicCat"
MODS = r"E:\SkyrimAE\mo2\mods"
STAGING = os.path.join(C.ROOT, "staging", "ZLJ Combat Latex Pack - P02B Pilot")
REPORTS = os.path.join(C.ROOT, "reports", "P02B")
MANIFEST = os.path.join(REPORTS, "P02B_CL06_STAGING_MANIFEST.csv")

# external male body systems that RULING-01 forbids vendoring
MALE_EXTERNAL_PREFIXES = ("meshes/armor/studded/male/", "meshes/himbo/", "meshes/actors/character/himbo/")
WORLD_GLOBAL_PREFIXES = MALE_EXTERNAL_PREFIXES + ("meshes/smim/", "meshes/clutter/", "meshes/architecture/")
DOMESTIC_PREFIX = "meshes/ae_toxic_cat/"

MAN_HEADER = ["outfit_id", "asset_class", "source_virtual_path", "source_provider", "target_virtual_path",
              "action", "ruling", "bytes_in", "bytes_out", "nif_strings_patched", "status", "notes"]


def rows(name):
    p = os.path.join(C.OUT, name)
    with open(p, encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if (r.get("OUTFIT_ID") or "") == OUTFIT]


def src_path(vp):
    return os.path.join(MODS, C.OUTFITS[OUTFIT]["primary"], C.norm(vp).replace("/", os.sep))


def clean_vpath(vp):
    """Strip any leading data\\ (however it was spelled) without changing case."""
    s = str(vp or "").replace("/", "\\")
    while s.lower().startswith("data\\"):
        s = s[5:]
    return s.lstrip("\\")


def stage_path(vp):
    return os.path.join(STAGING, clean_vpath(vp).replace("\\", os.sep))


def put(vp, data):
    dst = stage_path(vp)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    return dst


def main():
    os.makedirs(REPORTS, exist_ok=True)
    man = []
    mesh_rows = rows("P02A_MESH_MIGRATION.csv")
    tex_rows = rows("P02A_TEXTURE_MIGRATION.csv")
    nif_rows = rows("P02A_NIF_TEXTURE_REWRITE.csv")
    sd_rows = rows("P02A_SHAPEDATA_TEXTURE_REWRITE.csv")

    # ---------- decide the mesh copy set ----------
    src_roles = defaultdict(set)
    for r in mesh_rows:
        if r.get("mesh_class", "").upper() != "GAME_NIF":
            continue          # only runtime meshes are decided by RULING-01/03
        src_roles[C.norm(r["source_virtual_path"])].add(r.get("model_role", "").upper())
    targets = {}
    for r in mesh_rows:
        if r.get("mesh_class", "").upper() != "GAME_NIF":
            continue          # ShapeData / BodySlide output are handled separately
        targets.setdefault(C.norm(r["source_virtual_path"]), set()).add(clean_vpath(r["target_virtual_path"]))

    copy_mesh, skip_mesh = [], []
    for src, roles in sorted(src_roles.items()):
        female = bool(roles & {"WEARABLE_FEMALE_3P", "FIRSTPERSON_FEMALE"})
        male = bool(roles & {"WEARABLE_MALE_3P", "FIRSTPERSON_MALE"})
        world = bool(roles & {"WORLD_MALE", "WORLD_FEMALE"})
        domestic = src.startswith(DOMESTIC_PREFIX)
        external_male = src.startswith(MALE_EXTERNAL_PREFIXES)
        if female and domestic:
            copy_mesh.append((src, "CANONICAL_FEMALE", "RULING-01 canonical CBBE_3BA female"))
        elif male and domestic:
            # gender-neutral outfit-owned asset shared by male and female slots
            copy_mesh.append((src, "GENDER_NEUTRAL_SHARED", "RULING-01 exception: same outfit-owned neutral asset"))
        elif male and external_male:
            skip_mesh.append((src, "NON_CANONICAL_MALE", "RULING-01 DO_NOT_VENDOR external male body"))
        elif world and external_male:
            skip_mesh.append((src, "WORLD_GLOBAL_EXTERNAL", "RULING-03 vanilla world/drop model stays external"))
        else:
            skip_mesh.append((src, "UNCLASSIFIED", "no ruling matched"))

    # texture rewrite maps
    rw_by_nif = defaultdict(dict)
    for r in nif_rows:
        if r["status"] in ("REPOINT_SELF_NAMESPACE", "COPY_FROM_EXTERNAL_MOD", "COPY_FROM_CROSS_OUTFIT"):
            o, n = r["old_dds_path"].strip(), r["new_dds_path"].strip()
            if o and n and o.upper() != "UNKNOWN":
                rw_by_nif[C.norm(r["nif_source"])][o] = n
    sd_rw_by_nif = defaultdict(dict)
    for r in sd_rows:
        if r["status"] in ("REPOINT_SELF_NAMESPACE", "COPY_FROM_EXTERNAL_MOD", "COPY_FROM_CROSS_OUTFIT"):
            o, n = r["old_dds_path"].strip(), r["new_dds_path"].strip()
            if o and n and o.upper() != "UNKNOWN":
                sd_rw_by_nif[C.norm(r["shapedata_nif"])][o] = n

    # ---------- 1. runtime meshes ----------
    for src, klass, why in copy_mesh:
        sp = src_path(src)
        if not os.path.isfile(sp):
            man.append([OUTFIT, "GAME_NIF", src, C.OUTFITS[OUTFIT]["primary"], "", "SKIP", why,
                        0, 0, 0, "SOURCE_MISSING", "not present in the source mod"])
            continue
        # REFERENCE_TOPOLOGY_RULE (frozen in P02B1.2):
        #   when several ARMA model slots reference the SAME source virtual NIF, the target
        #   keeps that sharing. One canonical NIF is written, and every slot points at it.
        #   Splitting is only allowed with evidence (a dedicated source 1P NIF, a dedicated
        #   BodySlide output, an independent geometry/weight requirement, or explicit human
        #   approval). A differing MOD3/MOD5 slot number is NOT evidence.
        #   Targets under male\ are likewise not duplicated (RULING-01 shared neutral asset).
        tset = sorted(targets[src])
        female3p = [t for t in tset if "\\male\\" not in t.lower() and "\\1p\\" not in t.lower()]
        canonical = female3p[0] if female3p else (tset[0] if tset else "")
        wanted = [canonical] if canonical else []
        skipped_male = [t for t in tset if "\\male\\" in t.lower()]
        suppressed_1p = [t for t in tset if "\\1p\\" in t.lower()]
        topology = "SHARED_RUNTIME_MESH" if len(tset) > 1 else "DEDICATED_3P"
        mp = rw_by_nif.get(src, {})
        for tgt in wanted:
            if mp:
                rep = N.rewrite_file(sp, stage_path(tgt), mp)
                ver = N.verify(stage_path(tgt), mp)
                patched = rep["applied"]
                status = "COPIED_TEXTURE_REWRITTEN" if ver["old_remaining"] == 0 else "REWRITE_INCOMPLETE"
                note = "%s | shapes=%d applied=%d old_remaining=%d" % (klass, rep["shapes"], patched, ver["old_remaining"])
            else:
                put(tgt, open(sp, "rb").read())
                patched = 0
                status = "COPIED_VERBATIM"
                note = klass
            man.append([OUTFIT, "GAME_NIF", src, C.OUTFITS[OUTFIT]["primary"], tgt, "COPY",
                        why + " | topology=" + topology,
                        os.path.getsize(sp), os.path.getsize(stage_path(tgt)), patched, status, note])
        for tgt in skipped_male:
            man.append([OUTFIT, "GAME_NIF", src, C.OUTFITS[OUTFIT]["primary"], tgt, "SHARED_NEUTRAL",
                        "RULING-01 | topology=" + topology, 0, 0, 0, "NOT_DUPLICATED",
                        "male slot shares the outfit-owned neutral NIF written at the namespace root"])
        for tgt in suppressed_1p:
            man.append([OUTFIT, "GAME_NIF", src, C.OUTFITS[OUTFIT]["primary"], tgt, "SHARED_RUNTIME_MESH",
                        "REFERENCE_TOPOLOGY_RULE | topology=" + topology, 0, 0, 0, "NOT_DUPLICATED",
                        "1st-person slot shares the same canonical NIF; no artificial 1p copy is created"])
    for src, klass, why in skip_mesh:
        man.append([OUTFIT, "GAME_NIF", src, C.OUTFITS[OUTFIT]["primary"], "", "DO_NOT_COPY", why,
                    0, 0, 0, "SKIPPED", klass])

    # ---------- 2. textures ----------
    copied_tex = set()
    for r in tex_rows:
        act = (r.get("action") or "").upper()
        src = C.norm(r["source_virtual_path"])
        tgt = clean_vpath(r["target_virtual_path"]) if r.get("target_virtual_path") else ""
        if act == "COPY_INTO_OUTFIT_NAMESPACE" and tgt:
            if src in copied_tex:
                continue
            copied_tex.add(src)
            sp = src_path(src)
            if not os.path.isfile(sp):
                man.append([OUTFIT, "DDS", src, r.get("winning_provider", ""), tgt, "COPY", "RULING-02",
                            0, 0, 0, "SOURCE_MISSING", "provider not on disk in this mod folder"])
                continue
            put(tgt, open(sp, "rb").read())
            man.append([OUTFIT, "DDS", src, r.get("winning_provider", ""), tgt, "COPY", "outfit material",
                        os.path.getsize(sp), os.path.getsize(sp), 0, "COPIED",
                        r.get("owning_outfit_of_source", "")])
        elif act == "KEEP_EXTERNAL_REFERENCE":
            man.append([OUTFIT, "DDS", src, r.get("winning_provider", ""), src, "KEEP_EXTERNAL",
                        "RULING-02", 0, 0, 0, "NOT_COPIED", r.get("owning_outfit_of_source", "")])
        elif act == "UNRESOLVED":
            # Whole-mesh rows carry a sentinel instead of a DDS path; record the
            # referencing NIF so the row stays traceable (see the unknown-texture audit).
            ref = (r.get("referencing_nif") or "").strip()
            shown = ref if (not src or src == "unknown") and ref else src
            man.append([OUTFIT, "DDS", shown, r.get("winning_provider", ""), "", "UNRESOLVED", "-",
                        0, 0, 0, "UNRESOLVED",
                        "whole-mesh row (no derivable texture set); classification in P02B_CL06_UNKNOWN_TEXTURE_AUDIT.csv"])

    # ---------- 3. ShapeData (NIF + OSD) ----------
    bs_rows = rows("P02A_BODYSLIDE_MIGRATION.csv")
    sd_targets = {}
    for r in bs_rows:
        if r.get("old_shape_data"):
            sd_targets[C.norm(r["old_shape_data"]).rstrip("/")] = clean_vpath(r["new_shape_data"])
    sd_sources = sorted({C.norm(r["shapedata_nif"]) for r in sd_rows if r.get("shapedata_nif")})
    for src in sd_sources:
        sp = src_path(src)
        if not os.path.isfile(sp):
            man.append([OUTFIT, "SHAPEDATA_NIF", src, C.OUTFITS[OUTFIT]["primary"], "", "SKIP", "-",
                        0, 0, 0, "SOURCE_MISSING", ""])
            continue
        old_dir = src.rsplit("/", 1)[0].rstrip("/")
        new_dir = sd_targets.get(old_dir, "")
        if not new_dir:
            new_dir = "CalienteTools\\BodySlide\\ShapeData\\ZLJ_Combat_Latex\\CL06_ToxicCat\\"
        tgt = new_dir.rstrip("\\") + "\\" + src.rsplit("/", 1)[1]
        mp = sd_rw_by_nif.get(src, {})
        if mp:
            rep = N.rewrite_file(sp, stage_path(tgt), mp)
            ver = N.verify(stage_path(tgt), mp)
            patched = rep["applied"]
            st = "COPIED_TEXTURE_REWRITTEN" if ver["old_remaining"] == 0 else "REWRITE_INCOMPLETE"
            note = "shapes=%d applied=%d old_remaining=%d" % (rep["shapes"], patched, ver["old_remaining"])
        else:
            put(tgt, open(sp, "rb").read())
            patched, st, note = 0, "COPIED_VERBATIM", "BodySlide source"
        man.append([OUTFIT, "SHAPEDATA_NIF", src, C.OUTFITS[OUTFIT]["primary"], tgt, "COPY",
                    "BodySlide source", os.path.getsize(sp), os.path.getsize(stage_path(tgt)), patched, st, note])
    # OSD siblings
    for src in sd_sources:
        osd_src = src.rsplit(".", 1)[0] + ".osd"
        sp = src_path(osd_src)
        old_dir = src.rsplit("/", 1)[0].rstrip("/")
        new_dir = sd_targets.get(old_dir, "CalienteTools\\BodySlide\\ShapeData\\ZLJ_Combat_Latex\\CL06_ToxicCat\\")
        tgt = new_dir.rstrip("\\") + "\\" + os.path.basename(osd_src)
        if os.path.isfile(sp):
            put(tgt, open(sp, "rb").read())
            man.append([OUTFIT, "OSD", osd_src, C.OUTFITS[OUTFIT]["primary"], tgt, "COPY", "BodySlide OSD",
                        os.path.getsize(sp), os.path.getsize(sp), 0, "COPIED_VERBATIM", ""])
        else:
            man.append([OUTFIT, "OSD", osd_src, C.OUTFITS[OUTFIT]["primary"], "", "SKIP", "-",
                        0, 0, 0, "SOURCE_MISSING", ""])

    C.write_csv(MANIFEST, MAN_HEADER, man)

    cnt = Counter((r[5], r[10]) for r in man)
    print("staging root:", STAGING)
    print("manifest rows:", len(man))
    print("by action/status:")
    for k, v in sorted(cnt.items()):
        print("   %-16s %-26s %d" % (k[0], k[1], v))
    print()
    print("copied meshes:")
    for src, klass, why in copy_mesh:
        print("   %-46s %s" % (src, klass))
    print("skipped (rulings):")
    for src, klass, why in skip_mesh:
        print("   %-46s %s" % (src, klass))
    print()
    print("files on disk under staging:", sum(len(f) for _, _, f in os.walk(STAGING)))
    print("manifest:", MANIFEST)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
