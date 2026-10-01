#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p00r_plugins.py — STAGE B: real TES4 binary parsing of every ESP/ESL/ESM
owned by the 09 scope.

Pure-python, no xEdit, no third-party lib. Handles the GRUP tree, per-record
zlib compression, MAST/HEDR header fields, and the subrecord payloads needed
for the re-run's record table.

Parses the record types the brief mandates:
    ARMO ARMA TXST COBJ ENCH KYWD OTFT LVLI FLST MGEF SPEL PERK

Nothing is written outside data/P00_RERUN/. Game files are opened "rb" only.

Usage: python tools/P00_RERUN/p00r_plugins.py
"""
from __future__ import annotations

import json
import os
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p00r_common as C  # noqa: E402

F_COMPRESSED = 0x00040000
F_ESL = 0x00000200

WANT = {b"ARMO", b"ARMA", b"TXST", b"COBJ", b"ENCH", b"KYWD", b"OTFT",
        b"LVLI", b"FLST", b"MGEF", b"SPEL", b"PERK"}

# Subrecords we decode eagerly as text. Everything else is kept raw so nothing
# is lost.
#
# CORRECTED: the *_NAM family was listed here wholesale, but in TES4 those tags
# are overwhelmingly FormID references. Decoding them as zero-terminated text
# produced junk -- OTFT.INAM came out as '\x01\x08' and '\x08' instead of a
# reference. They are now resolved by payload size in decode_sub() instead, so
# only genuine text tags remain listed here.
ZSTR = {b"EDID", b"FULL", b"DESC", b"ITXT", b"LNAM",
        b"MOD2", b"MOD3", b"MOD4", b"MOD5",
        b"MO3T", b"MO4T", b"MO5T"}
U32_SUB = {b"KSIZ", b"DATA", b"ARAM", b"ACNT", b"FLDR",
           b"SPAT", b"SPET", b"SPFI", b"SPGV", b"SPGO", b"SPTR", b"SPEX",
           b"ETYP", b"BIDS", b"BAMT", b"BODT", b"EITM",
           b"ZNAM", b"ATCK", b"ATIP", b"ATMO", b"ATKW", b"ATOP", b"ATSF"}
U32F32_SUB = {b"DATA"}

# Subrecords whose 4-byte payload is genuinely text rather than a FormID.
# Empty by design: in this corpus every 4-byte subrecord is a reference, which
# is what stopped OTFT.INAM from being read as a string.
FOUR_CHAR_STR: set = set()

# ---- CORRECTED SCHEMA (calibrated against Skyrim.esm, see
# reports/P00_RERUN/PARSER_CALIBRATION.md) --------------------------------
#   ARMO.RNAM   = RACE   FormID   (2762/2762 vanilla ARMO resolve to RACE)
#   ARMO.MODL   = ArmorAddon FormID, REPEATED -> the 1:N ARMO->ARMA link
#   ARMA.BOD2   = 8-byte body-part mask
#   ARMA.MOD2..5= the wearable addon meshes
#   ARMO.MOD2..5= world / inventory drop models, NOT the worn mesh
# The first P00_RERUN pass had RNAM as the ArmorAddon link; that was wrong.
RNAM_IS = "RACE"
MODL_IS = "ArmorAddon (ARMA)"

# Skyrim armour-slot bit table applied to the BOD2 uint32 mask.
SLOT_BITS = {
    0: "head", 1: "hair", 2: "body", 3: "hands", 4: "forearms",
    5: "upperarm", 6: "feet", 7: "lowerleg", 8: "shield",
    9: "leftshoulder", 10: "rightshoulder", 11: "back", 12: "front",
    13: "leftweapon", 14: "rightweapon", 15: "chest", 16: "pelvis",
    17: "shield_back", 18: "misc",
}

SLOT_NAMES = {
    0: "head", 1: "hair", 2: "body", 3: "hands", 4: "forearms", 5: "upperarm",
    6: "feet", 7: "lowerlegs", 8: "thighs", 9: "calves", 10: "shield",
    11: "leftshoulder", 12: "rightshoulder", 13: "back", 14: "front",
    15: "leftweapon", 16: "rightweapon", 17: "chest", 18: "unk18", 19: "unk19",
    20: "pelvis", 21: "unk21", 22: "unk22", 23: "unk23", 24: "unk24",
    25: "unk25", 26: "unk26", 27: "unk27", 28: "unk28", 29: "unk29",
    30: "unk30", 31: "unk31", 32: "face", 33: "unk33", 34: "unk34",
    35: "unk35", 36: "unk36", 37: "unk37", 38: "unk38", 39: "unk39",
    40: "unk40", 41: "unk41", 42: "unk42", 43: "unk43", 44: "unk44",
    45: "unk45", 46: "unk46", 47: "unk47", 48: "unk48", 49: "unk49",
    50: "unk50", 51: "unk51", 52: "unk52", 53: "unk53", 54: "unk54",
    55: "unk55", 56: "unk56", 57: "unk57", 58: "unk58", 59: "unk59",
    60: "unk60", 61: "unk61",
}

ARMOR_TYPE = {
    0: "UNARMORED", 1: "HEAD", 2: "HAIR", 3: "BODY", 4: "HANDS", 5: "FOREARM",
    6: "UPPERARM", 7: "FEET", 8: "LOWERLEG", 9: "THIGH", 10: "CALF",
    11: "SHIELD", 12: "SHOULDER_L", 13: "SHOULDER_R", 14: "BACK",
    15: "FRONT", 16: "WEAPON_L", 17: "WEAPON_R", 18: "CHEST", 19: "PELVIS",
    20: "SKIN", 255: "UNSET",
}

BODYPART = {0: "SKIN", 1: "HEAD", 2: "HAIR", 3: "BODY", 4: "HANDS",
            5: "FOREARM", 6: "UPPERARM", 7: "FEET", 8: "LOWERLEG", 9: "THIGH",
            10: "CALF", 11: "SHIELD", 12: "SHOULDER_L", 13: "SHOULDER_R",
            14: "BACK", 15: "FRONT", 16: "WEAPON_L", 17: "WEAPON_R",
            18: "CHEST", 19: "PELVIS", 20: "RING", 21: "MISC"}

ENCHANTMENT_EFFECTS = {
    0: "STRENGTH", 1: "DEXTERITY", 2: "HEALTH", 3: "STAMINA", 4: "MAGICKA",
    5: "SHOUT", 6: "LUCK", 7: "FORTIFY_*", 8: "RESIST_*", 9: "DAMAGE_*",
    10: "PERSUADE", 11: "MAGIC_RESISTANCE", 12: "MISC", 13: "ABSORB",
    14: "HEAL_RATE", 15: "WEIGHT_REDUCE", 16: "WEAPON_DAMAGE",
    17: "INVALID", 18: "WEAPON_SPEED",
}

TRANSFORM_FLAGS = {0: "NONE", 1: "SCRIPT", 2: "SPELL", 4: "POWER",
                   8: "EFFECT", 16: "DAMAGE"}


def zstr(b: bytes) -> str:
    return b.split(b"\x00", 1)[0].decode("utf-8", "replace").strip()


def iter_subrecords(data: bytes):
    pos, n = 0, len(data)
    while pos + 6 <= n:
        st, ss = struct.unpack_from("<4sH", data, pos)
        pos += 6
        if pos + ss > n:
            return
        yield st, data[pos:pos + ss]
        pos += ss


def decode_sub(stype: bytes, raw: bytes):
    # Payload size decides before the tag table. A 4-byte subrecord is a FormID
    # in essentially every TES4 record, and reading one as text yields garbage
    # (OTFT.INAM was decoding to '\x01\x08' and '\x08'). Listing those tags in
    # ZSTR made the table win, so they are excluded from it below.
    if stype in U32F32_SUB and len(raw) == 8:
        return {"u32": struct.unpack("<I", raw[:4])[0],
                "f32": struct.unpack("<f", raw[4:8])[0]}
    if len(raw) == 4 and stype not in FOUR_CHAR_STR:
        return struct.unpack("<I", raw)[0]
    if stype in ZSTR:
        return zstr(raw)
    if stype in U32_SUB and len(raw) == 4:
        return struct.unpack("<I", raw)[0]
    if len(raw) == 4:
        v = struct.unpack("<I", raw)[0]
        f = struct.unpack("<f", raw)[0]
        return {"u32": v, "f32": f}
    if len(raw) == 2:
        return struct.unpack("<H", raw)[0]
    if len(raw) == 1:
        return raw[0]
    if len(raw) == 8:
        return {"u32": struct.unpack("<I", raw[:4])[0],
                "u32b": struct.unpack("<I", raw[4:])[0]}
    return raw[:64].hex()


def parse_plugin(path: str, want=WANT, fk=None):
    with open(path, "rb") as fh:
        blob = fh.read()
    n = len(blob)
    if n < 24:
        raise ValueError("too small")
    rtype, dsize, flags, formid, _, _, fver, _ = struct.unpack_from(
        "<4sIIIHHHH", blob, 0)
    if rtype != b"TES4":
        raise ValueError("not a plugin (no TES4 header)")

    masters, hdr = [], {}
    for st, sb in iter_subrecords(blob[24:24 + dsize]):
        if st == b"MAST":
            masters.append(zstr(sb).lower())
        elif st == b"HEDR":
            hdr["record_count"] = struct.unpack("<I", sb[4:8])[0] \
                if len(sb) >= 8 else None
            hdr["next_object"] = struct.unpack("<I", sb[8:12])[0] \
                if len(sb) >= 12 else None
    hdr["flags"] = flags
    hdr["is_esl"] = bool(flags & F_ESL)
    hdr["is_master"] = bool(flags & 0x00000001)
    hdr["file_version"] = fver

    pos = 24 + dsize
    records = []
    stats = {"groups": 0, "total": 0, "kept": 0, "bad": 0}

    def body_of(off, dsz, flg):
        if flg & F_COMPRESSED:
            if off + 4 > n:
                stats["bad"] += 1
                return None
            usize = struct.unpack_from("<I", blob, off)[0]
            try:
                # uint32 uncompressed length + deflate stream, running to the
                # end of the record. There is NO trailing 4-byte terminator:
                # the old `off + dsz - 4` failed on 44153/44153 compressed
                # records in Skyrim.esm and silently dropped them, which is why
                # the 09 scope (0 compressed records) never showed it.
                raw = zlib.decompress(blob[off + 4:off + dsz])
            except zlib.error:
                stats["bad"] += 1
                return None
            if len(raw) != usize:
                stats["bad"] += 1
                return None
            return raw
        return blob[off:off + dsz]

    def scan(end):
        nonlocal pos
        while pos + 24 <= n and pos < end:
            rt, ds, fl, fi, _, _, fv, _ = struct.unpack_from(
                "<4sIIIHHHH", blob, pos)
            if rt == b"GRUP":
                stats["groups"] += 1
                gend = pos + ds
                pos += 24
                scan(gend)
                if pos < gend:
                    stats["bad"] += 1
                    pos = gend
                continue
            body_off = pos + 24
            stats["total"] += 1
            if rt in want:
                body = body_of(body_off, ds, fl)
                if body is not None:
                    rec = build_record(rt.decode("ascii"), fi, fv,
                                       blob[body_off:body_off + 4], body, fk,
                                       os.path.basename(path))
                    rec["_plugin_name"] = os.path.basename(path)
                    records.append(rec)
                    stats["kept"] += 1
            pos = body_off + ds

    scan(n)
    return masters, hdr, records, stats


def build_record(rtype, formid, fver, value_bytes, body, fk=None,
                  plugin_name=""):
    """Build one record dict.

    Verified empirically on this install (see PARSER_CALIBRATION.md):
    the body begins directly with the first subrecord -- there is NO leading
    4-byte VALUE. Gameplay numbers therefore come from named subrecords and
    are never invented.
    """
    rec = {
        "record_type": rtype,
        "formid": C.record_id(formid),
        "formid_int": formid,
        "file_version": fver,
        "record_value": None,      # no leading VALUE in these records
        "subrecords": {},
    }
    subs = rec["subrecords"]
    refs = []                       # generic reference capture
    for st, sb in iter_subrecords(body):
        key = st.decode("ascii", "replace")
        if key == "KWDA" and len(sb) % 4 == 0:
            subs.setdefault("KWDA", []).extend(
                C.record_id(x) for x in struct.unpack(
                    "<" + "I" * (len(sb) // 4), sb))
            continue
        if key in ("BOD2",) and len(sb) >= 4:
            mask = struct.unpack("<I", sb[:4])[0]
            bits = [i for i in range(32) if (mask >> i) & 1]
            subs.setdefault("BOD2", []).append({
                "mask": mask, "mask_hex": f"0x{mask:08X}",
                "bits": bits,
                "names": [SLOT_BITS.get(i, f"bit{i}") for i in bits],
                "raw_hex": sb.hex(), "payload_len": len(sb),
            })
            continue
        if key in ("ENAM", "INAM") and len(sb) % 4 == 0 and len(sb) >= 4:
            # ENAM and INAM are FormID LISTS, not single refs and not text.
            # OTFT.INAM measures 12-28 bytes here, i.e. 3-7 consecutive
            # FormIDs: the outfits an outfit is related to. It used to surface
            # as hex soup because no table covered it.
            vals = struct.unpack("<" + "I" * (len(sb) // 4), sb)
            subs.setdefault(key, []).extend(C.record_id(v) for v in vals)
            continue
        if len(sb) == 4 and st in (b"MODL", b"RNAM"):
            v = struct.unpack("<I", sb)[0]
            subs.setdefault(key, []).append(v)
            refs.append((key, v))
            continue
        subs.setdefault(key, []).append(decode_sub(st, sb))

    # ---- ARMO: the corrected relationship --------------------------------
    if rtype == "ARMO":
        bod2 = (subs.get("BOD2") or [{}])[0]
        modl = subs.get("MODL", []) or []
        race = (subs.get("RNAM") or [None])[0]
        arma = []
        modl_refs = []                 # every MODL, resolved or not
        for m in modl:
            if not isinstance(m, int) or not m:
                continue
            entry = {"raw_formid": C.record_id(m), "master_byte": (m >> 24)}
            if fk is not None:
                plug, rtype_t, edid, route = fk.resolve(plugin_name, m)
                entry.update({
                    "resolved_plugin": plug or "",
                    "resolved_type": rtype_t or "",
                    "resolved_edid": edid or "",
                    "route": route,
                    "is_arma": rtype_t == "ARMA",
                })
                if rtype_t == "ARMA":
                    arma.append({"plugin": plug, "formid": C.record_id(m),
                                 "edid": edid})
            modl_refs.append(entry)
        race_res = None
        if fk is not None and isinstance(race, int) and race:
            plug, rtype_t, edid, route = fk.resolve(plugin_name, race)
            race_res = {"plugin": plug, "type": rtype_t, "edid": edid,
                        "route": route}
        world_models = [x for k in ("MOD2", "MOD3", "MOD4", "MOD5")
                        for x in subs.get(k, []) if isinstance(x, str)]
        rec["armo"] = {
            "slot_mask": bod2.get("mask"),
            "slot_mask_hex": bod2.get("mask_hex", ""),
            "slot_bits": bod2.get("bits", []),
            "slot_names": bod2.get("names", []),
            "slot_source": "ARMO.BOD2 uint32 mask (BOD2 payload is 8 bytes)",
            "slot_confidence": "MEDIUM",
            "race_raw": C.record_id(race) if isinstance(race, int) else "",
            "race_is": RNAM_IS,
            "race_resolved": race_res,
            "modl_refs": modl_refs,
            "arma_refs": arma,
            "n_arma_refs": len(arma),
            "n_modl_refs": len(modl_refs),
            "world_model_paths": world_models,
            "world_model_note": "ARMO MOD2..MOD5 are world/inventory drop "
                                "models, NOT the worn mesh",
            "DATA_u32": (subs.get("DATA") or [None])[0]
            if isinstance((subs.get("DATA") or [None])[0], dict) else None,
            "DATA_f32": (subs.get("DATA") or [None])[0].get("f32")
            if isinstance((subs.get("DATA") or [None])[0], dict) else None,
            "DNAM_u32": (subs.get("DNAM") or [None])[0],
            "value_source": "raw_subrecord_unverified_ck_mapping",
        }
    # ---- ARMA: this is where the wearable mesh lives ---------------------
    if rtype == "ARMA":
        bod2 = (subs.get("BOD2") or [{}])[0]
        rec["arma"] = {
            "slot_mask": bod2.get("mask"),
            "slot_mask_hex": bod2.get("mask_hex", ""),
            "slot_bits": bod2.get("bits", []),
            "slot_names": bod2.get("names", []),
            "slot_raw_hex": bod2.get("raw_hex", ""),
            # MOD2..MOD5 on an ArmorAddon are the addon meshes. The first
            # one is conventionally the base/source body, the later ones the
            # actual garment addons; we keep them all and label the roles by
            # whether the path resolves inside the 09 scope.
            "addon_model_paths": {
                k: [x for x in subs.get(k, []) if isinstance(x, str)]
                for k in ("MOD2", "MOD3", "MOD4", "MOD5")},
            "source_mesh_refs": [C.record_id(x) for x in
                                 (subs.get("MODL") or [])
                                 if isinstance(x, int)],
            "armor_material_raw": C.record_id(
                (subs.get("RNAM") or [None])[0])
            if isinstance((subs.get("RNAM") or [None])[0], int) else "",
            "texture_set_refs": {
                k: [v for v in subs.get(k, [])]
                for k in ("MO2S", "MO2T", "MO3S", "MO3T", "MO4S", "MO4T",
                          "MO5S", "MO5T")},
        }
    return rec


def main() -> int:
    C.ensure_dirs()
    with open(os.path.join(C.DATA, "01_mod_aggregates.json"),
              encoding="utf-8") as fh:
        mods = json.load(fh)
    C.log(f"loaded {len(mods)} mods from stage A")

    import p00r_formkey as FKI
    fk = FKI.FormKeyIndex()
    C.log("building full-library FormKey index (needed for cross-master "
          "ARMO->ARMA resolution) ...")
    fk.build(FKI.library_paths())
    C.log("  " + json.dumps(fk.summary(), ensure_ascii=False))

    import gzip
    with gzip.open(os.path.join(C.DATA, "01_file_index.json.gz"), "rt",
                   encoding="utf-8") as fh:
        idx = json.load(fh)
    byrel = {(f["mod"], f["rel"]): f["sha256"] for f in idx}

    out_records, plugin_index, failures = [], [], []
    for m in mods:
        root = os.path.join(C.MODS_DIR, m["mod_name"])
        for pf in [x.strip() for x in (m.get("plugin_files") or "").split(";")
                   if x.strip()]:
            full = os.path.join(root, pf.replace("/", os.sep))
            if not os.path.isfile(full):
                failures.append({"mod": m["mod_name"], "file": pf,
                                 "error": "not found"})
                continue
            try:
                masters, hdr, recs, stats = parse_plugin(full, fk=fk)
            except Exception as e:                       # noqa: BLE001
                failures.append({"mod": m["mod_name"], "file": pf,
                                 "error": repr(e)[:200]})
                C.log(f"  FAIL {pf}: {e}")
                continue
            for r in recs:
                r["plugin_file"] = os.path.basename(pf)
                r["PLUGIN_ID"] = C.plugin_id(os.path.basename(pf))
                r["source_mod"] = m["mod_name"]
                r["MOD_ID"] = m["mod_name"]
                r["priority"] = m["priority"]
                out_records.append(r)
            plugin_index.append({
                "PLUGIN_ID": C.plugin_id(os.path.basename(pf)),
                "plugin_file": os.path.basename(pf),
                "source_mod": m["mod_name"],
                "priority": m["priority"],
                "enabled": m["enabled"],
                "size": m.get("size_bytes"),
                "sha256": byrel.get((m["mod_name"],
                                     os.path.basename(pf)), ""),
                "masters": masters,
                "header": hdr,
                "stats": stats,
                "n_records": len(recs),
                "by_type": {t: sum(1 for r in recs if r["record_type"] == t)
                            for t in sorted({r["record_type"] for r in recs})},
            })
        C.log(f"  {m['mod_name'][:52]:<54} plugins={len(plugin_index):>3} "
              f"records={len(out_records):>5}")

    C.write_json(os.path.join(C.DATA, "02_plugin_records.json"), out_records)
    C.write_json(os.path.join(C.DATA, "02_plugin_index.json"), plugin_index)
    C.write_json(os.path.join(C.DATA, "02_parse_failures.json"), failures)
    C.write_json(os.path.join(C.DATA, "05_formkey_summary.json"),
                 fk.summary())

    from collections import Counter
    tc = Counter(r["record_type"] for r in out_records)
    arma_links = sum(len((r.get("armo") or {}).get("modl_refs", []))
                     for r in out_records if r["record_type"] == "ARMO")
    arma_ok = sum(1 for r in out_records if r["record_type"] == "ARMO"
                  for a_ in (r.get("armo") or {}).get("modl_refs", [])
                  if a_.get("is_arma"))
    rtypes = Counter(a_.get("resolved_type") or "UNRESOLVED"
                     for r in out_records if r["record_type"] == "ARMO"
                     for a_ in (r.get("armo") or {}).get("modl_refs", []))
    C.log("record types: " + ", ".join(f"{k}={v}" for k, v in tc.most_common()))
    C.log(f"ARMO.MODL refs: {arma_links} total, {arma_ok} resolve to ARMA")
    C.log("  MODL target types: " +
          ", ".join(f"{k}={v}" for k, v in rtypes.most_common(8)))
    rr = Counter(((r.get("armo") or {}).get("race_resolved") or {}).get("type")
                 or "UNRESOLVED"
                 for r in out_records if r["record_type"] == "ARMO")
    rr_route = Counter(((r.get("armo") or {}).get("race_resolved") or {}).get(
        "route") or "UNRESOLVED"
        for r in out_records if r["record_type"] == "ARMO")
    C.log("  RNAM target types: " +
          ", ".join(f"{k}={v}" for k, v in rr.most_common(8)))
    C.log("  RNAM routes      : " +
          ", ".join(f"{k}={v}" for k, v in rr_route.most_common(8)))
    C.log("  " + json.dumps(fk.summary(), ensure_ascii=False))
    C.log(f"DONE stage B: {len(plugin_index)} plugins, {len(out_records)} "
          f"records, {len(failures)} failures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
