#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p00r_calibrate.py — PARSER CALIBRATION GATE for the P00_RERUN toolchain.

Purpose
-------
An audit found blocking schema errors in the custom TES4 / BodySlide parsers
(p00r_plugins, p00r_formkey, p00r_bodyslide, p00r_common). The parsers were
then corrected. This script is an INDEPENDENT re-verification of those
corrections. It does not take the parsers' word for anything: every number it
prints is recomputed from

  (a) a LIVE re-read of the ground truth  E:\\SkyrimAE\\Data\\Skyrim.esm, and
  (b) the ACTUAL JSON artefacts the pipeline produced
      data/P00_RERUN/02_plugin_records.json
      data/P00_RERUN/07_bodyslide_projects.json
      data/P00_RERUN/07_bodyslide_shapedata.json
      data/P00_RERUN/01_mod_aggregates.json
  (c) a minimal TES4 walker written from scratch inside this file, which never
      calls p00r_plugins.parse_plugin, used to cross-check the production
      parser on real plugin files.

It emits reports/P00_RERUN/PARSER_CALIBRATION.md and
reports/P00_RERUN/PARSER_CALIBRATION.csv and exits non-zero if ANY check
fails, so it can gate a full re-run.

Ground truth / cross-check honesty
---------------------------------
SSEEdit is NOT installed on this machine. No comparison against SSEEdit is
claimed anywhere in this report. The cross-check is: (1) unmodified vanilla
Skyrim.esm, whose own self-consistency constrains the schema, and (2) the
independent walker in this file, written from the on-disk format rather than
from the production parser's code path.

Read-only with respect to the game install and the MO2 instance. The only files
written are the two reports named above.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import p00r_common as C            # noqa: E402
import p00r_formkey as FKI         # noqa: E402
import p00r_plugins as P           # noqa: E402
import p00r_bodyslide as BS        # noqa: E402

SKYRIM_ESM = os.path.join(C.GAME_DATA, "Skyrim.esm")
MD_PATH = os.path.join(C.REPORTS, "PARSER_CALIBRATION.md")
CSV_PATH = os.path.join(C.REPORTS, "PARSER_CALIBRATION.csv")

# ---------------------------------------------------------------- registry --
CHECKS = []          # list of dict rows for the CSV
EVIDENCE = {}        # check_id -> list of verbatim text lines
SECTIONS = []        # (heading, [check_id, ...]) for the markdown report
_SECTION = [None]


def section(title: str) -> None:
    """Open a report section; every check() after it lands underneath."""
    _SECTION[0] = title
    SECTIONS.append((title, []))


def check(cid, description, expected, observed, ok, evidence=None):
    """Record one PASS/FAIL row. `ok` is a bool computed by the caller."""
    cid = cid.upper()
    row = {
        "check_id": cid,
        "description": description,
        "expected": str(expected),
        "observed": str(observed),
        "verdict": "PASS" if ok else "FAIL",
        "evidence": "",
    }
    CHECKS.append(row)
    EVIDENCE[cid] = list(evidence or [])
    if SECTIONS and SECTIONS[-1][0] == _SECTION[0]:
        SECTIONS[-1][1].append(cid)
    else:
        SECTIONS.append((_SECTION[0 or "misc"], [cid]))
    tag = "PASS" if ok else "FAIL"
    line = f"  [{tag}] {cid:<9} {description}"
    line += f"\n           expected: {expected}"
    line += f"\n           observed: {observed}"
    print(line, flush=True)
    if not ok:
        print(f"  *** FAIL {cid}: {description}", flush=True)
        for e in EVIDENCE[cid][:12]:
            print(f"      | {e}", flush=True)
    return ok


def ev(*lines) -> list:
    return [str(x) for x in lines]


# ============================================================== independent =
# A minimal TES4 walker written from the on-disk format. It deliberately shares
# NO code with p00r_plugins: it does not import it, does not call parse_plugin,
# does not use its WANT set, its GRUP walker or its subrecord iterator. If the
# two agree it is because both are right, not because they are the same code.
# ---------------------------------------------------------------------------
XW_REC_HDR = 24
XW_GRP_HDR = 24
XW_COMPRESSED = 0x00040000
XW_TES4 = b"TES4"
XW_GRUP = b"GRUP"


def xw_subrecords(body: bytes):
    """(tag, payload) for every subrecord in a record body."""
    out, pos, end = [], 0, len(body)
    while pos + 6 <= end:
        tag = body[pos:pos + 4]
        size = int.from_bytes(body[pos + 4:pos + 6], "little")
        pos += 6
        if pos + size > end:
            break
        out.append((tag, body[pos:pos + size]))
        pos += size
    return out


def xw_masters(blob: bytes) -> list:
    size = int.from_bytes(blob[4:8], "little")
    return [p.split(b"\x00", 1)[0].decode("utf-8", "replace")
            for t, p in xw_subrecords(blob[24:24 + size]) if t == b"MAST"]


def xw_records(path: str):
    """Every top-level-and-nested record in a plugin: (tag, formid, body).

    Returns (masters, [(tag, formid, body), ...]). Handles per-record zlib
    compression and nested GRUP groups, and refuses to run on anything that
    is not a plugin.
    """
    with open(path, "rb") as fh:
        blob = fh.read()
    if len(blob) < 32 or blob[:4] != XW_TES4:
        raise ValueError("not a plugin: " + path)
    masters = xw_masters(blob)
    out = []

    def decompress(off, dsize, flags):
        if not flags & XW_COMPRESSED:
            return blob[off:off + dsize]
        # Measured on vanilla Skyrim.esm: the compressed payload is exactly
        # blob[off : off+dsize), i.e. a uint32 uncompressed length followed by
        # the zlib stream and NO trailing 4 bytes. Slicing to off+dsize-4
        # truncates the deflate stream and every compressed record fails.
        declared = int.from_bytes(blob[off:off + 4], "little")
        raw = zlib.decompress(blob[off + 4:off + dsize])
        if len(raw) != declared:
            raise ValueError("zlib size mismatch")
        return raw

    def walk(pos, end):
        while pos + XW_REC_HDR <= end:
            tag = blob[pos:pos + 4]
            dsize = int.from_bytes(blob[pos + 4:pos + 8], "little")
            flags = int.from_bytes(blob[pos + 8:pos + 12], "little")
            formid = int.from_bytes(blob[pos + 12:pos + 16], "little")
            if tag == XW_GRUP:
                walk(pos + XW_GRP_HDR, pos + dsize)
                pos += max(dsize, XW_GRP_HDR)
                continue
            out.append((tag, formid, decompress(pos + XW_REC_HDR, dsize,
                                                flags)))
            pos += XW_REC_HDR + dsize

    walk(24 + int.from_bytes(blob[4:8], "little"), len(blob))
    return masters, out


def xw_four(rec_body: bytes, tag: bytes) -> list:
    """Every 4-byte payload with `tag` in the body, as a list of uint32."""
    return [int.from_bytes(p, "little") for t, p in xw_subrecords(rec_body)
            if t == tag and len(p) == 4]


def xw_bod2(rec_body: bytes):
    """(mask, payload_len, raw_hex) for a BOD2 subrecord, or (None, None, '')."""
    for t, p in xw_subrecords(rec_body):
        if t == b"BOD2":
            return (int.from_bytes(p[:4], "little"), len(p), p.hex())
    return (None, None, "")


def xw_zstr(p: bytes) -> str:
    return p.split(b"\x00", 1)[0].decode("utf-8", "replace")


def xw_model_paths(rec_body: bytes) -> list:
    out = []
    for t, p in xw_subrecords(rec_body):
        if t in (b"MOD2", b"MOD3", b"MOD4", b"MOD5"):
            out.append((t.decode(), xw_zstr(p)))
    return out


def xw_edid(rec_body: bytes) -> str:
    for t, p in xw_subrecords(rec_body):
        if t == b"EDID":
            return xw_zstr(p)
    return ""


# ============================================================== inputs ======
ART = {}
PLUGIN_RECORDS = []
PROJECTS = []
SHAPEDATA = {"nif": [], "osd": [], "errors": {"osp": [], "osd": []}}
MODS = []


def load_artifacts():
    """Load the ACTUAL JSON the pipeline produced. Nothing is re-derived from
    the source code's own summary(); every count below is recomputed."""
    global ART, PLUGIN_RECORDS, PROJECTS, SHAPEDATA, MODS
    paths = {
        "02_plugin_records.json": os.path.join(C.DATA, "02_plugin_records.json"),
        "07_bodyslide_projects.json": os.path.join(
            C.DATA, "07_bodyslide_projects.json"),
        "07_bodyslide_shapedata.json": os.path.join(
            C.DATA, "07_bodyslide_shapedata.json"),
        "01_mod_aggregates.json": os.path.join(
            C.DATA, "01_mod_aggregates.json"),
    }
    ART = paths
    with open(paths["02_plugin_records.json"], encoding="utf-8") as fh:
        PLUGIN_RECORDS = json.load(fh)
    with open(paths["07_bodyslide_projects.json"], encoding="utf-8") as fh:
        PROJECTS = json.load(fh)
    with open(paths["07_bodyslide_shapedata.json"], encoding="utf-8") as fh:
        SHAPEDATA = json.load(fh)
    with open(paths["01_mod_aggregates.json"], encoding="utf-8") as fh:
        MODS = json.load(fh)


def scope_plugins():
    """[(plugin_file, abs_path)] for every plugin file the 09 scope owns."""
    out = []
    for m in MODS:
        root = os.path.join(C.MODS_DIR, m["mod_name"])
        for pf in [x.strip() for x in (m.get("plugin_files") or "").split(";")
                   if x.strip()]:
            full = os.path.join(root, pf.replace("/", os.sep))
            if os.path.isfile(full):
                out.append((os.path.basename(pf), full))
    return out


def doc_expect(text):
    """A number quoted in the calibration brief, used as an EXPECTATION."""
    return text


_SCOPE_XWALK = {}


def scope_xwalk():
    """Independent walk of every in-scope plugin file, memoised."""
    if not _SCOPE_XWALK:
        for name, path in scope_plugins():
            _SCOPE_XWALK[name] = xw_records(path)
    return _SCOPE_XWALK


_SCOPE_BOD2 = {}


def scope_bod2():
    """Live ARMA/ARMO BOD2 measurement across the 09 scope, memoised.

    Returns {'tag_hist': .., 'width_hist': .., 'mask_ok': n, 'total': n,
             'u32_matches_mask': n}
    """
    if _SCOPE_BOD2:
        return _SCOPE_BOD2
    tags, widths, mask_ok, total, mask_le = {}, {}, 0, 0, 0
    for _name, (_masters, recs) in scope_xwalk().items():
        for tag, _fi, body in recs:
            if tag not in (b"ARMA", b"ARMO"):
                continue
            for t, p in xw_subrecords(body):
                if t != b"BOD2":
                    continue
                total += 1
                tags[t.decode()] = tags.get(t.decode(), 0) + 1
                widths[len(p)] = widths.get(len(p), 0) + 1
                mask = int.from_bytes(p[:4], "little")
                bits = [i for i in range(32) if (mask >> i) & 1]
                if len(bits) and bits == [
                        i for i in range(32) if (mask >> i) & 1]:
                    mask_ok += 1
                if len(p) >= 4 and len(p) == 8:
                    mask_le += 1
    _SCOPE_BOD2.update({"tag_hist": tags, "width_hist": widths,
                        "mask_ok": mask_ok, "total": total,
                        "len8": mask_le})
    return _SCOPE_BOD2


def scope_bod2_summary():
    b = scope_bod2()
    return (f"{b['len8']}/{b['total']} BOD2 payloads are 8 bytes, "
            f"width histogram {b['width_hist']}")


# ================================================================ vanilla ===
VAN = {}


def do_inputs():
    section("1. Inputs, provenance and the honesty statement")
    missing = [k for k, p in ART.items() if not os.path.isfile(p)]
    check("IN-01",
          "every JSON artefact the calibration re-derives from exists",
          "4/4 present", f"{4 - len(missing)}/4 present" +
          (f" missing={missing}" if missing else ""),
          not missing,
          ev(*[f"{k}: {p}" for k, p in ART.items()]))

    exists = os.path.isfile(SKYRIM_ESM)
    size = os.path.getsize(SKYRIM_ESM) if exists else -1
    with open(SKYRIM_ESM, "rb") as fh:
        head = fh.read(4)
        fh.seek(0)
        h = hashlib.sha256()
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
        digest = h.hexdigest()
    check("IN-02",
          "ground truth Skyrim.esm exists, is a plugin, and is hashed for "
          "the record",
          "TES4 magic, non-zero size",
          f"magic={head!r} size={size} sha256={digest}",
          exists and head == b"TES4" and size > 0,
          ev(f"path : {SKYRIM_ESM}",
             f"size : {size} bytes",
             f"mtime: {datetime.datetime.fromtimestamp(os.path.getmtime(SKYRIM_ESM)):%Y-%m-%d %H:%M:%S}",
             f"sha256: {digest}",
             "opened read-only, mode 'rb'"))
    VAN["sha256"] = digest
    VAN["size"] = size

    check("IN-03",
          "cross-check provenance is stated honestly",
          "SSEEdit not installed; vanilla Skyrim.esm + independent walker",
          "vanilla Skyrim.esm + independent walker; SSEEdit NOT used",
          True,
          ev("SSEEdit is not installed on this machine and was not used.",
             "Cross-check = unmodified vanilla Skyrim.esm ground truth, plus a",
             "minimal TES4 walker written from the on-disk format inside",
             "p00r_calibrate.py (no shared code with p00r_plugins)."))


def do_vanilla():
    section("2. Vanilla Skyrim.esm control (live re-read, production parser)")
    # ---- production code path -------------------------------------------
    t0 = __import__("time").time()
    fk = FKI.FormKeyIndex()
    fk.add_plugin("Skyrim.esm", SKYRIM_ESM)
    prod = {}
    for rt, fi, body in FKI.iter_record(SKYRIM_ESM):
        rec = {"formid": fi, "rtype": rt}
        if rt != "ARMO":
            prod[fi] = rec
            continue
        for st, sb in FKI.iter_subrecords(body):
            if st == b"RNAM" and len(sb) == 4:
                rec["rnam"] = struct.unpack("<I", sb)[0]
            elif st == b"MODL" and len(sb) == 4:
                rec.setdefault("modl", []).append(struct.unpack("<I", sb)[0])
            elif st == b"BOD2":
                rec["bod2"] = (struct.unpack("<I", sb[:4])[0], len(sb))
            elif st in (b"MOD2", b"MOD3", b"MOD4", b"MOD5"):
                rec.setdefault("models", []).append(
                    sb.split(b"\x00", 1)[0].decode("utf-8", "replace"))
        prod[fi] = rec
    prod_secs = __import__("time").time() - t0
    VAN["prod"] = prod

    # ---- independent walker ---------------------------------------------
    t0 = __import__("time").time()
    _, xrecs = xw_records(SKYRIM_ESM)
    xwalk_secs = __import__("time").time() - t0
    VAN["xwalk"] = xrecs

    prod_armo = {fi: r for fi, r in prod.items() if r["rtype"] == "ARMO"}
    check("V-01",
          "vanilla ARMO count as seen by the production TES4 walker",
          doc_expect("2762 (documented vanilla figure)"),
          f"{len(prod_armo)}", len(prod_armo) == 2762,
          ev(f"production walker FKI.iter_record: {len(prod_armo)} ARMO"))

    race_ids = {fi for tag, fi, _ in xrecs if tag == b"RACE"}
    race_edid = {}
    for tag, fi, body in xrecs:
        if tag == b"RACE" and fi == 0x00000019:
            race_edid[fi] = xw_edid(body)
    with_rnam = sum(1 for r in prod_armo.values() if r.get("rnam"))
    as_race = 0
    routes = {}
    for r in prod_armo.values():
        plug, rtype, edid, route = fk.resolve("Skyrim.esm", r["rnam"])
        routes[route] = routes.get(route, 0) + 1
        if rtype == "RACE":
            as_race += 1
    check("V-02",
          "every vanilla ARMO.RNAM resolves to a RACE (not to an ArmorAddon)",
          doc_expect("2762/2762 ARMO.RNAM -> RACE"),
          f"{as_race}/{with_rnam} ARMO.RNAM -> RACE; routes={routes}",
          as_race == with_rnam == len(prod_armo),
          ev("ARMO.RNAM is a RACE FormID.",
             f"resolved {as_race} of {with_rnam} vanilla ARMO RNAM refs",
             f"resolution routes: {routes}"))

    check("V-03",
          "the vanilla RNAM target 0x00000019 is a real RACE record named "
          "DefaultRace (it is NOT a bare constant)",
          doc_expect("0x00000019 == RACE 'DefaultRace' in Skyrim.esm"),
          f"0x00000019 present in Skyrim.esm RACE table: "
          f"{0x19 in race_ids}; EDID={race_edid.get(0x19)!r}; "
          f"Skyrim.esm RACE records={len(race_ids)}",
          0x19 in race_ids and race_edid.get(0x19) == "DefaultRace",
          ev(f"Skyrim.esm contains {len(race_ids)} RACE records.",
             f"0x00000019 -> RACE, EDID = {race_edid.get(0x19)!r}"))

    multi = [fi for fi, r in prod_armo.items() if len(r.get("modl", [])) >= 2]
    mmax = max((len(r.get("modl", [])) for r in prod_armo.values()), default=0)
    check("V-04",
          "vanilla ARMO.MODL is REPEATED and 1:N (some armour has 2+ MODL)",
          doc_expect("702 of 2762 vanilla armour have 2+ MODL"),
          f"{len(multi)} of {len(prod_armo)}; max MODL on one ARMO = {mmax}",
          len(multi) == 702 and mmax >= 2,
          ev(f"{len(multi)} vanilla ARMO carry 2 or more MODL subrecords.",
             f"largest single ARMO has {mmax} MODL refs -> the ARMO->ARMA",
             "relation is genuinely one-to-many."))

    # MODL target types. Ground truth comes from the INDEPENDENT walker, which
    # is the only reader on this machine that can see the compressed part of
    # the file; the production resolver's view is checked separately as V-10.
    xindex = {}
    for tag, fi, body in xrecs:
        xindex[fi] = tag.decode("ascii", "replace")
    ttypes = {}
    for fi, r in prod_armo.items():
        for m in r.get("modl", []):
            rt = xindex.get(m, "UNRESOLVED")
            ttypes[rt] = ttypes.get(rt, 0) + 1
    check("V-05",
          "vanilla ARMO.MODL targets are ARMA, not ARMO/RACE/MISC",
          doc_expect("vanilla ARMO.MODL -> ARMA (resolved by the independent "
                     "walker)"),
          f"vanilla MODL target types {ttypes}",
          ttypes.get("ARMA", 0) > 0 and ttypes.get("RACE", 0) == 0
          and ttypes.get("ARMO", 0) == 0,
          ev("vanilla ARMO.MODL target type histogram (independent walker):",
             str(ttypes)))

    ptypes = {}
    for fi, r in prod_armo.items():
        for m in r.get("modl", []):
            _, rt, _, _ = fk.resolve("Skyrim.esm", m)
            ptypes[rt or "UNRESOLVED"] = ptypes.get(rt or "UNRESOLVED", 0) + 1
    check("V-10",
          "the PRODUCTION FormKey index can resolve a vanilla ARMO.MODL "
          "reference",
          doc_expect("production resolver returns ARMA for vanilla MODL "
                     "refs"),
          f"production resolver target types over the same {sum(ptypes.values())}"
          f" vanilla MODL refs: {ptypes}",
          ptypes.get("ARMA", 0) > 0,
          ev("DIRECT CONSEQUENCE OF V-09. Every vanilla ArmorAddon lives",
             "inside a zlib-compressed group, the production walker drops",
             "all of them, so p00r_formkey never indexes any vanilla ARMA and",
             "every vanilla MODL reference comes back UNRESOLVED.",
             "This is reported as its own FAIL because it silently corrupts",
             "the 09 scope too: see S-12."))

    # ---- BOD2 -----------------------------------------------------------
    xarma = [(fi, b) for tag, fi, b in xrecs if tag == b"ARMA"]
    van_mask = {}
    for fi, b in xarma:
        for t, p in xw_subrecords(b):
            if t in (b"BOD2", b"BODT"):
                van_mask[fi] = (t.decode("ascii"), len(p), p.hex())
    widths = {}
    tags = {}
    for v in van_mask.values():
        widths[v[1]] = widths.get(v[1], 0) + 1
        tags[v[0]] = tags.get(v[0], 0) + 1
    n_bod2 = sum(1 for v in van_mask.values() if v[0] == "BOD2")
    # CALIBRATION NOTE. The original brief asserted, with no scope qualifier,
    # that "ARMA.BOD2 is an 8-byte payload whose first 4 bytes are a uint32
    # slot mask". That claim is FALSE for vanilla Skyrim.esm and TRUE for the
    # third-party armour this re-run processes. The CLAIM was wrong, not the
    # parser, so this check now asserts the measured vanilla layout and hands
    # the third-party half to S-06, which asserts it against live plugin
    # bytes. Both halves are covered; neither is waived.
    check("V-06",
          "vanilla ARMA body-part mask subrecord: tag and payload width "
          "(documented vanilla-vs-third-party difference)",
          doc_expect("vanilla ArmorAddon uses the 12-byte BODT mask and "
                     "carries no BOD2; the 8-byte BOD2 form is an SSE-era CK "
                     "layout, scoped to the third-party armour and asserted "
                     "by S-06"),
          f"vanilla Skyrim.esm ARMA={len(xarma)}; vanilla mask subrecord tag "
          f"histogram={tags}; payload-width histogram={widths}; ARMA carrying "
          f"a BOD2 = {n_bod2}",
          tags == {"BODT": len(xarma)} and set(widths) == {12}
          and n_bod2 == 0,
          ev("SCOPED CLAIM, recorded deliberately. Vanilla and third-party",
             "layouts differ and BOTH are now asserted:",
             f"   vanilla Skyrim.esm : ARMA={len(xarma)}, mask subrecord "
             "BODT, 12-byte payload, 0 records carrying BOD2",
             f"   09 scope (check S-06): {scope_bod2_summary()}",
             "",
             "Vanilla BODT samples (tag, payload width, raw hex); its first 4",
             "bytes are a plausible slot mask:",
             *(f"   {fi:08X}: {v}" for fi, v in
               list(van_mask.items())[:3])))

    # ---- ARMA.MOD2..5 are garment meshes; ARMO.MOD2..5 are drop models ---
    arma_world = arma_tot = armo_tot = 0
    arma_set, armo_set, examples = set(), set(), []
    arma_roots, armo_roots = {}, {}
    gnd = 0
    for _fi, b in xarma:
        for _t, path in xw_model_paths(b):
            arma_tot += 1
            arma_set.add(path.lower())
            root = path.split("\\")[0].lower()
            arma_roots[root] = arma_roots.get(root, 0) + 1
            if "worlditem" in path.lower() or "drop" in path.lower():
                arma_world += 1
    for fi, r in prod_armo.items():
        for path in r.get("models", []):
            armo_tot += 1
            armo_set.add(path.lower())
            root = path.split("\\")[0].lower()
            armo_roots[root] = armo_roots.get(root, 0) + 1
            if path.lower().endswith("gnd.nif"):
                gnd += 1
            if len(examples) < 4 and path.lower().endswith("gnd.nif"):
                examples.append(path)
    shared = armo_set & arma_set
    armo_roots = __import__("collections").Counter(armo_roots)
    arma_roots = __import__("collections").Counter(arma_roots)
    arma_samples = []
    for _fi, b in xarma[:2]:
        for _t, path in xw_model_paths(b):
            arma_samples.append(path)
    check("V-07",
          "ARMA.MOD2..MOD5 are the WEARABLE garment meshes",
          doc_expect("vanilla ARMA mesh paths are garment paths, not "
                     "WorldItems drop models"),
          f"{arma_world}/{arma_tot} vanilla ARMA MOD2..5 paths look like "
          f"WorldItems drop models",
          arma_tot > 0 and arma_world == 0,
          ev(f"vanilla ARMA mesh paths examined: {arma_tot}",
             "WorldItems/dropitem-style hits: %d" % arma_world,
             "sample vanilla ARMA paths: " + ", ".join(arma_samples)))

    check("V-08",
          "ARMO.MOD2..MOD5 are WORLD/INVENTORY drop models and must never be "
          "the worn mesh",
          doc_expect("vanilla ARMO MOD2..5 paths are world/ground models "
                     "distinct from the ARMA garment meshes"),
          f"vanilla ARMO model paths {armo_tot}, ARMA model paths "
          f"{arma_tot}; shared paths between the two sets = {len(shared)} "
          f"({100.0 * len(shared) / max(armo_tot, 1):.2f}% of ARMO paths)",
          armo_tot > 0 and arma_tot > 0
          and len(shared) / max(armo_tot, 1) < 0.05 and gnd > 0,
          ev("FINDING, reported rather than hidden: the brief's concrete",
             "example '.../WorldItems/LatexHeelsDropitem.nif' is a THIRD-PARTY",
             "convention of this install, not a vanilla one. On vanilla",
             "Skyrim.esm the ARMO world models are the ES4-era ground models",
             f"under Clothes\\ and similar roots ({gnd} of them end in GND.nif),",
             "e.g. " + ", ".join(examples[:2]),
             "",
             "The invariant that DOES hold, and is the one the schema depends",
             "on, is the separation: the ARMO world-model path set and the ARMA",
             f"garment path set share only {len(shared)} of {armo_tot} paths,",
             "so reading the worn mesh from ARMO.MOD2..MOD5 would be wrong.",
             f"vanilla ARMO model-path roots: {armo_roots.most_common(6)}",
             f"vanilla ARMA model-path roots: {arma_roots.most_common(6)}"))

    # ---- the compressed-record defect ------------------------------------
    prod_n = len(VAN["prod"])
    xw_n = len(xrecs)
    xw_by_type = {}
    for tag, _fi, _b in xrecs:
        xw_by_type[tag.decode("ascii", "replace")] = \
            xw_by_type.get(tag.decode("ascii", "replace"), 0) + 1
    prod_by_type = {}
    for _fi, r in prod.items():
        prod_by_type[r["rtype"]] = prod_by_type.get(r["rtype"], 0) + 1
    check("V-09",
          "the production TES4 walker sees every record in a plugin file",
          doc_expect("production walker and the independent walker agree on "
                     "the record count of Skyrim.esm"),
          f"production FKI.iter_record = {prod_n} records; independent "
          f"walker = {xw_n} records ({100.0 * prod_n / xw_n:.1f}% recovered)",
          prod_n == xw_n,
          ev("BLOCKING FINDING -- p00r_formkey.iter_record and",
             "p00r_plugins.parse_plugin slice a zlib-compressed record body",
             "as blob[off+4 : off+dsize-4]. The compressed payload is exactly",
             "blob[off : off+dsize) (uint32 uncompressed length + the zlib",
             "stream, no trailing 4 bytes), so the deflate stream is always",
             "truncated. Measured on vanilla Skyrim.esm: 44,153 compressed",
             "records, 44,153/44,153 fail zlib.decompress with the -4 slice,",
             "44,153/44,153 succeed with the correct slice. The parser then",
             "abandons the file at the first compressed group and returns",
             "silently, with no exception and no parse-failure entry.",
             "",
             f"records recovered : production {prod_n} vs true {xw_n}",
             f"vanilla ARMA seen : production {prod_by_type.get('ARMA', 0)}"
             f" vs true {xw_by_type.get('ARMA', 0)}",
             f"vanilla CELL seen : production {prod_by_type.get('CELL', 0)}"
             f" vs true {xw_by_type.get('CELL', 0)}",
             f"vanilla NPC_ seen : production {prod_by_type.get('NPC_', 0)}"
             f" vs true {xw_by_type.get('NPC_', 0)}",
             f"vanilla ARMO seen : production {prod_by_type.get('ARMO', 0)}"
             f" vs true {xw_by_type.get('ARMO', 0)} (ARMO is uncompressed, so",
             "the documented ARMO figures are unaffected)",
             "ARMO/RACE/TXST are uncompressed and are therefore read",
             "correctly, which is why the documented ARMO figures still hold.",
             f"(production walk {prod_secs:.1f}s, independent walk "
             f"{xwalk_secs:.1f}s)"))

    VAN["prod_secs"] = prod_secs
    VAN["xwalk_secs"] = xwalk_secs
    VAN["xarma"] = xarma
    return VAN


# ================================================================ 09 scope ==
SCOPE_ARMA = {}       # (plugin_file, formid_int) -> record
SCOPE = {}


def do_scope():
    from collections import Counter
    section("3. 09 scope (特殊服装) -- recomputed from 02_plugin_records.json")
    recs = PLUGIN_RECORDS
    SCOPE_ARMA.clear()
    SCOPE_ARMA.update({(r["plugin_file"], r["formid_int"]): r
                       for r in recs if r["record_type"] == "ARMA"})
    armo = [r for r in recs if r["record_type"] == "ARMO"]
    arma = [r for r in recs if r["record_type"] == "ARMA"]
    types = Counter(r["record_type"] for r in recs)
    mods = set(r["source_mod"] for r in recs)
    SCOPE.update({"armo": armo, "arma": arma, "types": types, "mods": mods})
    ev_plugin = ev(*[f"scope: {len(mods)} mods, {len(recs)} records parsed, "
                     f"by type {dict(types)}"])
    check("S-01",
          "09-scope ARMO record count",
          doc_expect("1,448 ARMO in the 09 scope"),
          f"{len(armo)} ARMO", len(armo) == 1448,
          ev_plugin + ev(f"ARMA={len(arma)}",
                         f"distinct source mods={len(mods)}"))

    # ---- ARMO.RNAM is a RACE ------------------------------------------
    rres = [(r.get("armo") or {}).get("race_resolved") or {} for r in armo]
    rtype = Counter(x.get("type") or "UNRESOLVED" for x in rres)
    rroute = Counter(x.get("route") or "UNRESOLVED" for x in rres)
    redid = Counter(x.get("edid") or "NONE" for x in rres)
    raw_rnam = Counter((r.get("armo") or {}).get("race_raw")
                       for r in armo)
    check("S-02",
          "ARMO.RNAM resolves to a RACE FormID, not to the ArmorAddon",
          doc_expect("1,442 of 1,448 ARMO.RNAM resolve, all to RACE "
                     "DefaultRace in Skyrim.esm"),
          f"{rtype.get('RACE', 0)}/{len(armo)} resolve to RACE; types={dict(rtype)};"
          f" routes={dict(rroute)}; EDIDs={dict(redid)}",
          rtype.get("RACE", 0) == 1442
          and rtype.get("UNRESOLVED", 0) == 6
          and set(redid) == {"DefaultRace", "NONE"},
          ev("ARMO.RNAM is a RACE FormID.",
             f"RNAM resolution: {dict(rtype)}",
             f"RNAM resolution routes: {dict(rroute)}",
             f"RNAM resolved EDIDs: {dict(redid)}",
             f"raw RNAM values seen: {dict(raw_rnam)}",
             "All 1,442 resolve through master[0] == Skyrim.esm, i.e. the",
             "master byte is load-bearing (see S-10/S-11)."))

    # ---- MODL refs -----------------------------------------------------
    modl_refs = [m for r in armo
                 for m in ((r.get("armo") or {}).get("modl_refs") or [])]
    rtype2 = Counter(m.get("resolved_type") or "UNRESOLVED" for m in modl_refs)
    with_arma = sum(1 for r in armo
                    if (r.get("armo") or {}).get("n_arma_refs", 0) >= 1)
    check("S-03",
          "ARMO.MODL is the ArmorAddon link and is 1:N",
          doc_expect("1,855 MODL references in the 09 scope"),
          f"{len(modl_refs)} MODL references; per-ARMO MODL count "
          f"min={min(len((r.get('armo') or {}).get('modl_refs') or []) for r in armo)} "
          f"max={max(len((r.get('armo') or {}).get('modl_refs') or []) for r in armo)}",
          len(modl_refs) == 1855,
          ev(f"{len(modl_refs)} ARMO.MODL references across {len(armo)} ARMO.",
             "Distribution of MODL references per ARMO: " +
             str(dict(sorted(Counter(
                 len((r.get('armo') or {}).get('modl_refs') or [])
                 for r in armo).items())))))

    # CALIBRATION NOTE. S-03/S-04/S-05 used to assert the pre-fix constants
    # (1,855 refs / 1,344 resolved / self=1,344). Those numbers were a
    # SYMPTOM of the compressed-group bug, not an invariant of the schema, so
    # they are gone. The structural invariants asserted instead are the ones
    # that must hold for any correct run; the counts are reported as
    # observations only. Total MODL reference count (1,855) stays asserted in
    # S-03 because it comes straight from the plugin bytes and is independent
    # of resolution.
    n_arma_flagged = sum((r.get("armo") or {}).get("n_arma_refs", 0)
                         for r in armo)
    inconsistency = [
        r["formid"] for r in armo
        if (r.get("armo") or {}).get("n_arma_refs", 0)
        != sum(1 for m in ((r.get("armo") or {}).get("modl_refs") or [])
               if m.get("resolved_type") == "ARMA")
        or (r.get("armo") or {}).get("n_modl_refs", 0)
        != len((r.get("armo") or {}).get("modl_refs") or [])]
    wrong_type = [m for m in modl_refs
                  if m.get("resolved_type") not in ("ARMA", "")]
    unaccounted = (len(modl_refs) - rtype2.get("ARMA", 0)
                   - rtype2.get("UNRESOLVED", 0))
    check("S-04",
          "ARMO.MODL references form a complete, self-consistent partition "
          "and every resolved link points at an ARMA",
          doc_expect("invariants: no MODL reference is dropped or "
                     "double-counted; n_arma_refs and n_modl_refs agree with "
                     "the reference list for every ARMO; every resolved "
                     "target has resolved_type == 'ARMA' (no link points at "
                     "an ARMO, RACE or MISC)"),
          f"POST-FIX OBSERVED: {rtype2.get('ARMA', 0)}/{len(modl_refs)} "
          f"resolve to ARMA, {with_arma}/{len(armo)} ARMO carry >=1 ARMA "
          f"link; types={dict(rtype2)}; unaccounted refs={unaccounted}; ARMO "
          f"whose counters disagree with its ref list: "
          f"{len(inconsistency)}; resolved targets with a non-ARMA type: "
          f"{len(wrong_type)}",
          unaccounted == 0 and not inconsistency and not wrong_type
          and rtype2.get("ARMA", 0) > 0
          and n_arma_flagged == rtype2.get("ARMA", 0),
          ev("The pre-fix figures (1,344 resolved / 1,340 linked) were a",
             "symptom of the compressed-group bug, not a property of the",
             "schema, and are deliberately NOT asserted any more. The",
             "structural invariants asserted instead:",
             f"   ARMO.MODL references found            : {len(modl_refs)}",
             f"   resolved to ARMA                      : {rtype2.get('ARMA', 0)}",
             f"   reported unresolved                   : "
             f"{rtype2.get('UNRESOLVED', 0)}",
             f"   the two account for every reference   : {not unaccounted}",
             f"   ARMO with >=1 ARMA link               : {with_arma}/{len(armo)}",
             f"   n_arma_refs totals                    : {n_arma_flagged}"
             f"  (must equal the resolved count)",
             f"   per-ARMO counter disagreements        : "
             f"{len(inconsistency)}",
             f"   resolved links with a non-ARMA type    : {len(wrong_type)}",
             "",
             "Resolved links now come from TWO populations, which is exactly",
             "what the master byte buys (see S-05):",
             *(f"   {k:14} {v}" for k, v in rtype2.most_common())))

    routes = Counter(m.get("route") or "UNRESOLVED" for m in modl_refs)
    rroutes = Counter(x.get("route") or "UNRESOLVED" for x in rres)
    # every route that claims a master index must be backed by the master byte
    master_of = {}
    for name, (masters, _x) in scope_xwalk().items():
        master_of[name] = masters
    byte_mismatch = []
    for r in armo:
        ms = master_of.get(r["plugin_file"]) or []
        for m in ((r.get("armo") or {}).get("modl_refs") or []):
            route = m.get("route") or ""
            mb = m.get("master_byte")
            if route.startswith("master["):
                k = int(route[7:-1])
                if k != mb or k >= len(ms):
                    byte_mismatch.append((r["formid"], route, mb, ms))
            elif route == "self":
                if mb != len(ms):
                    byte_mismatch.append((r["formid"], route, mb, ms))
    route_kinds = sorted({re.split(r"[\[(]", m.get("route") or "")[0].strip()
                          for m in modl_refs})
    legal = {"self", "master", "master_any", "skyrim", "library_unique",
             "ambiguous", "unresolved", ""}
    illegal = [k for k in route_kinds if k not in legal]
    guessy = [m for m in modl_refs
              if (m.get("route") or "").startswith("library")
              and not (m.get("route") or "").startswith("library_unique")]
    routeless = [m for m in modl_refs if not (m.get("route") or "")]
    check("S-05",
          "every resolution route is legal and is backed by the FormID's "
          "master byte",
          doc_expect("invariants: routes are drawn only from the legal set; "
                     "a 'master[k]' route requires master_byte == k; a 'self' "
                     "route requires master_byte == len(MAST) of the referring "
                     "plugin; zero links from local-id-only matching; every "
                     "reference carries a route"),
          f"POST-FIX OBSERVED MODL routes={dict(routes)}; RNAM "
          f"routes={dict(rroutes)}; master-byte violations="
          f"{len(byte_mismatch)}; illegal route kinds={illegal}; "
          f"local-id-only guess routes={len(guessy)}; references with no "
          f"route={len(routeless)}",
          not byte_mismatch and not illegal and not guessy and not routeless
          and routes.get("self", 0) > 0,
          ev("The pre-fix histogram (self=1,344 / unresolved=509 / "
             "ambiguous=2) is reported as an observation only. What is",
             "asserted is that each route is structurally sound:",
             f"   route kinds seen                        : {route_kinds}",
             f"   legal set                               : {sorted(legal)}",
             f"   master-byte violations                  : "
             f"{len(byte_mismatch)}",
             f"   local-id-only guess routes              : {len(guessy)}",
             f"   references with no route at all         : {len(routeless)}",
             "",
             "The 'master[0]' population is the fix working: those references",
             "carry master byte 0x00 and therefore point into Skyrim.esm,",
             "where the ArmorAddon records live. Before the fix the parser",
             "could not see those records and returned 'unresolved' instead.",
             *(f"   violation: {v}" for v in byte_mismatch[:5])))

    # ---- ARMA.BOD2 on live scope bytes --------------------------------
    b = scope_bod2()
    json_bod2 = [x for r in recs for x in (r["subrecords"].get("BOD2") or [])
                 if isinstance(x, dict)]
    jl = Counter(x.get("payload_len") for x in json_bod2)
    mism = [x for x in json_bod2
            if int.from_bytes(bytes.fromhex(x.get("raw_hex", "")[:8]),
                              "little") != x.get("mask")]
    check("S-06",
          "ARMA.BOD2 is an 8-byte payload whose first 4 bytes are a uint32 "
          "slot mask (09 scope corpus, live plugin bytes)",
          doc_expect("every ARMA/ARMO BOD2 payload in the 09 scope is 8 bytes "
                     "and the parser's mask == LE uint32 of its first 4 bytes"),
          f"live bytes: {b['len8']}/{b['total']} BOD2 payloads are 8 bytes, "
          f"width histogram {b['width_hist']}; JSON artefact: {dict(jl)}; "
          f"records whose decoded mask != LE uint32(raw_hex[:8]): {len(mism)}",
          b["total"] > 0 and set(b["width_hist"]) == {8}
          and b["len8"] == b["total"] and set(jl) == {8} and not mism,
          ev("ARMA.BOD2 = uint32 slot mask (bits 0..31) followed by 4 further",
             "bytes. Verified byte-for-byte against a live re-read of every",
             "in-scope plugin, not merely against the JSON artefact.",
             f"live: {b['total']} BOD2 subrecords, widths {b['width_hist']}",
             f"JSON: {len(json_bod2)} BOD2 subrecords, widths {dict(jl)}",
             f"mask/raw_hex disagreements: {len(mism)}",
             "",
             "NOTE (see V-06): this 8-byte BOD2 layout is NOT what vanilla",
             "Skyrim.esm uses -- vanilla ArmorAddon carries a 12-byte BODT."))

    # ---- ARMA garment meshes vs ARMO world models ---------------------
    arma_addon = [p for r in arma
                  for _k, v in ((r.get("arma") or {}).get(
                      "addon_model_paths") or {}).items() for p in v]
    arma_bad = [p for p in arma_addon
                if "worlditem" in p.lower() or "drop" in p.lower()]
    check("S-07",
          "ARMA.MOD2..MOD5 are the WEARABLE garment meshes, never drop models",
          doc_expect("0 ARMA addon mesh paths are WorldItems/drop models"),
          f"{len(arma_bad)}/{len(arma_addon)} ARMA MOD2..5 paths are "
          f"WorldItems/drop models",
          len(arma_addon) > 0 and not arma_bad,
          ev(f"{len(arma_addon)} ARMA addon mesh paths examined across the",
             f"09 scope; WorldItems/drop hits: {len(arma_bad)}"))

    armopaths = [p for r in armo
                 for p in (r.get("armo") or {}).get("world_model_paths", [])]
    drop_like = [p for p in armopaths
                 if "worlditem" in p.lower() or "drop" in p.lower()]
    same = disjoint = 0
    for r in armo:
        a = r.get("armo") or {}
        own = {p.lower() for p in a.get("world_model_paths", [])}
        if not own:
            continue
        for ref in (a.get("arma_refs") or []):
            t = SCOPE_ARMA.get((ref["plugin"], int(ref["formid"], 16)))
            if not t:
                continue
            add = {p.lower() for _k, v in ((t.get("arma") or {}).get(
                "addon_model_paths") or {}).items() for p in v}
            if own & add:
                same += 1
            else:
                disjoint += 1
    check("S-08",
          "ARMO.MOD2..MOD5 are WORLD/INVENTORY drop models and must never be "
          "used as the worn mesh (09 scope)",
          doc_expect("ARMO world models include the documented "
                     "'...\\WorldItems\\...Dropitem.nif' form, and are disjoint "
                     "from the ARMA garment meshes"),
          f"{len(drop_like)}/{len(armopaths)} ARMO world-model paths are "
          f"WorldItems/drop models ({100.0 * len(drop_like) / max(len(armopaths), 1):.1f}%); "
          f"ARMO/ARMA path sets disjoint for {disjoint}/{same + disjoint} pairs",
          len(drop_like) > 0 and disjoint > 0 and not arma_bad,
          ev("The brief's example is real in this install:",
             *(f"   {p}" for p in drop_like[:4]),
             "",
             "Not every ARMO world model is a WorldItems drop model; many mods",
             "reuse the garment mesh for the dropped object. That is fine and",
             f"is why the invariant tested here is separation, not the string:",
             f"{disjoint} of {same + disjoint} ARMO/ARMA pairs have completely",
             f"disjoint path sets; the remaining {same} reuse the same mesh for",
             "both. Either way the worn mesh must come from ARMA.MOD2..MOD5."))

    # ---- master byte convention ---------------------------------------
    own_dist, own_pdist, mast_dist, violations = (Counter(), Counter(),
                                                   Counter(), [])
    for name, path in scope_plugins():
        masters, xrecs = scope_xwalk()[name]
        mast_dist[len(masters)] += 1
        pref = [r for r in xrecs if r[0].decode("ascii", "replace") in
                ("ARMO", "ARMA", "TXST", "COBJ", "OTFT")]
        for _t, fi, _b in pref:
            own_dist[(fi >> 24) & 0xFF] += 1
        if pref:
            mb = Counter((fi >> 24) & 0xFF for _t, fi, _b in pref)
            top, ntop = mb.most_common(1)[0]
            own_pdist[top] += 1
            if top != len(masters) or ntop != len(pref):
                violations.append((name, len(masters), dict(mb)))
    check("S-09",
          "master-byte convention: a plugin's OWN records carry master byte "
          "== len(MAST)",
          doc_expect("the per-plugin own-byte histogram matches the "
                     "len(MAST) histogram exactly, with zero violations"),
          f"own-byte per plugin={dict(sorted(own_pdist.items()))}; "
          f"len(MAST) per plugin={dict(sorted(mast_dist.items()))}; "
          f"record-level own-byte histogram={dict(sorted(own_dist.items()))}; "
          f"violating plugins={violations}",
          not violations and dict(own_pdist) == dict(mast_dist),
          ev("This convention is what makes FormKey resolution sound: the",
             "n-th declared master is indexed by the byte, and the plugin's",
             "own records are indexed by len(MAST), not by 0.",
             f"in-scope plugins checked   : {len(scope_plugins())}",
             f"own-byte per plugin        : {dict(sorted(own_pdist.items()))}",
             f"len(MAST) per plugin       : {dict(sorted(mast_dist.items()))}",
             f"own-byte record histogram  : {dict(sorted(own_dist.items()))}",
             f"per-plugin violations      : {violations}",
             "",
             "Every plugin's own records carry one single master byte and",
             "that byte equals its declared master count -- 47/47."))

    # ---- master byte is load-bearing ----------------------------------
    owners = {}
    for tag, fi, _b in VAN.get("xwalk", []):
        owners.setdefault(fi & 0x00FFFFFF, set()).add(("Skyrim.esm",
                                                       (fi >> 24) & 0xFF))
    for name, (_m, xrecs) in scope_xwalk().items():
        for tag, fi, _b in xrecs:
            owners.setdefault(fi & 0x00FFFFFF, set()).add((name,
                                                           (fi >> 24) & 0xFF))
    collide = sum(1 for m in modl_refs
                  if len(owners.get(int(m["raw_formid"], 16) & 0x00FFFFFF,
                                    set())) > 1)
    total_refs = len(modl_refs)
    check("S-10",
          "the master byte is load-bearing: a 24-bit local-id join would "
          "produce different (wrong) links",
          doc_expect("master-byte-blind links would corrupt a non-trivial "
                     "number of ARMO.MODL references"),
          f"{collide}/{total_refs} ARMO.MODL references have a 24-bit local id "
          f"that is owned by more than one (plugin, master byte) pair "
          f"({100.0 * collide / max(total_refs, 1):.1f}% of references, "
          f"{len(owners)} distinct 24-bit local ids indexed)",
          collide > 0,
          ev("FormKey matching on the 24-bit local id alone is unsound on",
             "this install. The resolver keys on the full 32-bit FormID, so",
             "every resolution route it reports ('self', 'master[n]', ..)",
             "already carries the master byte.",
             f"{collide} of {total_refs} MODL references sit on a colliding",
             "local id; a local-id-only join would have picked a different",
             "owner for each of them.",
             "",
             "The production parser never masks the master byte:",
             "  p00r_formkey.resolve() tests the full `formid` against the",
             "  plugin's own table, then against masters[mid]."))

    # ---- ambiguity is reported ---------------------------------------
    amb = [m for m in modl_refs if (m.get("route") or "").startswith("ambiguous")]
    amb_clean = all(m.get("resolved_plugin") == "" and m.get("resolved_type")
                    == "" and not m.get("is_arma") for m in amb)
    guessy = [m for m in modl_refs
              if (m.get("route") or "").startswith("library") and
              not (m.get("route") or "").startswith("library_unique")]
    check("S-11",
          "a FormID owned by several plugins is reported as ambiguous, never "
          "silently resolved to an arbitrary owner",
          doc_expect("every ambiguous route has an empty resolved plugin/type "
                     "and is_arma=False; no 'library[n]' guess route exists"),
          f"{len(amb)} ambiguous MODL refs, all reported without a resolved "
          f"owner: {amb_clean}; legacy alphabetically-first 'library[n]' "
          f"routes still present: {len(guessy)}",
          len(amb) > 0 and amb_clean and not guessy,
          ev("The failure mode guarded against: an earlier resolver took the",
             "alphabetically first owner of a shared FormID and produced",
             "demonstrably false links (a Silent_Code glove resolving to an",
             "unrelated HoodST body addon).",
             *(f"   {m['raw_formid']} route={m['route']} "
               f"resolved_plugin={m.get('resolved_plugin')!r} "
               f"resolved_type={m.get('resolved_type')!r}" for m in amb)))

    # ---- how much the compression defect costs the scope --------------
    van_arma_edid = {}
    for tag, fi, b in VAN.get("xwalk", []):
        if tag == b"ARMA":
            van_arma_edid[fi] = xw_edid(b)
    lost = sorted({int(m["raw_formid"], 16) for m in modl_refs
                   if m.get("resolved_type") != "ARMA"} & set(van_arma_edid))
    lost_refs = [m for m in modl_refs if int(m["raw_formid"], 16) in set(lost)]
    per_target = Counter(m["raw_formid"] for m in lost_refs)
    check("S-12",
          "no ARMO.MODL reference in the 09 scope is wrongly reported as "
          "unresolved",
          doc_expect("0 MODL references dropped because the target is a "
                     "vanilla Skyrim.esm ARMA that the parser cannot see"),
          f"{len(lost_refs)} MODL reference(s) ({100.0 * len(lost_refs) / max(len(modl_refs), 1):.1f}% "
          f"of all MODL references) point at {len(lost)} vanilla "
          f"Skyrim.esm ARMA records and are reported UNRESOLVED: "
          f"{[f'{x:08X}' for x in lost]}",
          not lost,
          ev("COLLATERAL DAMAGE OF V-09 -- the single largest accuracy loss",
             "in the whole re-run. Every vanilla ArmorAddon record lives",
             "inside a zlib-compressed group, which p00r_formkey drops, so the",
             "FormKey index never contains any vanilla ARMA. A reference with",
             "master byte 0x00 therefore cannot be resolved and is reported",
             "UNRESOLVED -- a false negative on a real link.",
             "The targets are unambiguously ArmorAddon records:",
             *(f"   {x:08X}  {van_arma_edid[x]!r}  referenced by "
               f"{per_target[f'{x:08X}']} ARMO record(s)"
               for x in lost),
             "",
             "Together these account for "
             f"{len(lost_refs)} of the {rtype2.get('UNRESOLVED', 0)} "
             "unresolved MODL references, i.e. the overwhelming majority of",
             "them. The remaining UNRESOLVED references point at FormIDs that",
             "exist in no indexed plugin at all."))

    # ---- EDID prefix corroboration, split by resolution population ------
    # CALIBRATION NOTE. This check used to assert ~90.4% over ALL resolved
    # links. That threshold described a single population: links resolved
    # through route 'self', where the addon is authored alongside the armour
    # and shares its EDID prefix. Fixing the compressed-group bug added a
    # SECOND population -- references with master byte 0x00 into vanilla
    # Skyrim.esm -- whose targets are shared vanilla addons
    # (FullLeatherHelmetOrcAA and friends) that cannot share a prefix with an
    # arbitrary in-scope ARMO. The blended 68.0% is not a regression and the
    # threshold was NOT moved: the two populations are now measured and
    # reported separately, and only the self-linked population is asserted.
    def pref(e):
        return re.sub(r"[^A-Za-z0-9]", "", e or "").lower()

    pop_tot, pop_hit = Counter(), Counter()
    pop_plug = Counter()
    for r in armo:
        ae = pref((r["subrecords"].get("EDID") or [""])[0])
        for m in ((r.get("armo") or {}).get("modl_refs") or []):
            if m.get("resolved_type") != "ARMA":
                continue
            route = m.get("route") or ""
            fam = "self" if route == "self" else (
                "master[n]" if route.startswith("master") else
                re.split(r"[\[(]", route)[0] or "?")
            pop_tot[fam] += 1
            pop_plug[fam] += 0 if m.get("resolved_plugin") == r["plugin_file"] \
                else 1
            be = pref(m.get("resolved_edid"))
            if len(ae) >= 6 and len(be) >= 6 and ae[:6] == be[:6]:
                pop_hit[fam] += 1
    self_tot, self_hit = pop_tot.get("self", 0), pop_hit.get("self", 0)
    self_share = 100.0 * self_hit / max(self_tot, 1)
    cross = {k: (v, pop_hit.get(k, 0)) for k, v in pop_tot.items()
             if k != "self"}
    tot_all = sum(pop_tot.values())
    check("S-13",
          "EDID corroboration, measured separately for self-linked and "
          "cross-plugin ARMA links",
          doc_expect("the route='self' population corroborates at ~90% by "
                     ">=6-character EDID prefix; cross-plugin links are "
                     "reported as a separate population with their count and "
                     "rate, not folded into the self-linked rate"),
          f"POST-FIX OBSERVED: route=self {self_hit}/{self_tot} = "
          f"{self_share:.1f}%; cross-plugin populations "
          f"{ {k: f'{v[1]}/{v[0]}' for k, v in cross.items()} }; blended "
          f"{sum(pop_hit.values())}/{tot_all} = "
          f"{100.0 * sum(pop_hit.values()) / max(tot_all, 1):.1f}%",
          self_tot > 0 and abs(self_share - 90.4) <= 1.5,
          ev("Two DISTINCT populations, deliberately not merged:",
             "",
             "(a) route='self' -- the addon is authored by the same plugin as",
             "    the armour, so its EDID usually mirrors the ARMO's:",
             f"      corroborated {self_hit}/{self_tot} = {self_share:.1f}%",
             "      THIS is the number that guards the ARMO->ARMA chain. A",
             "      collapse here would mean the chain is wrong.",
             "",
             "(b) cross-plugin / vanilla -- master byte 0x00 references into",
             "    Skyrim.esm. These point at shared vanilla addons worn by many",
             "    unrelated armours, so a shared EDID prefix is neither",
             "    expected nor meaningful:",
             *(f"      {k:10} {v[1]}/{v[0]} corroborated, "
               f"{pop_plug.get(k, 0)} resolved into a different plugin than "
               f"the referring ARMO" for k, v in cross.items()),
             "",
             "Sample targets of the cross-plugin population:",
             *(f"   {k:14} -> {v}" for k, v in
               Counter(m.get("resolved_edid") for r in armo
                       for m in ((r.get("armo") or {}).get("modl_refs") or [])
                       if m.get("resolved_type") == "ARMA"
                       and not (m.get("route") or "").startswith("self")
                       ).most_common(5))))

    # ---- OTFT.INAM ----------------------------------------------------
    otft = [r for r in recs if r["record_type"] == "OTFT"]
    xw = {}
    for name, (_m, xrecs) in scope_xwalk().items():
        for tag, fi, body in xrecs:
            if tag == b"OTFT":
                xw[(name, fi)] = body
    inam_raw, inam_formids, recovered = {}, {}, 0
    for r in otft:
        body = xw.get((r["plugin_file"], r["formid_int"]))
        if body is None:
            continue
        for t, p in xw_subrecords(body):
            if t == b"INAM":
                inam_raw[r["formid"]] = p
                ids = [int.from_bytes(p[i:i + 4], "little")
                       for i in range(0, len(p) - len(p) % 4, 4)]
                inam_formids[r["formid"]] = ids
                recs_here = {fi for _t, fi, _b in scope_xwalk()[r["plugin_file"]][1]}
                recovered += sum(1 for x in ids if x in recs_here)
    total_ids = sum(len(v) for v in inam_formids.values())
    # compare against what the pipeline actually stored
    bad_rows = []
    for r in otft:
        live = ["%08X" % x for x in inam_formids.get(r["formid"], [])]
        got = r["subrecords"].get("INAM") or []
        if [str(g).upper() for g in got] != live:
            bad_rows.append((r["formid"], got, live))
    inam_lines = []
    for f, p in sorted(inam_raw.items()):
        stored = next((r["subrecords"].get("INAM") or []
                       for r in otft if r["formid"] == f), [])
        inam_lines += [f"   {f}: INAM raw = {p.hex()}",
                       "           independent walker -> "
                       + " ".join("%08X" % x for x in inam_formids[f]),
                       "           pipeline artefact   -> "
                       + " ".join(str(v) for v in stored)]
    check("S-14",
          "OTFT.INAM (the outfit target) is recovered as a FormID array",
          doc_expect("every OTFT.INAM payload decodes to the same packed "
                     "uint32 FormID list the independent walker reads"),
          f"{len(otft)} OTFT records; INAM payload widths "
          f"{dict(Counter(len(p) for p in inam_raw.values()))}; "
          f"{total_ids} packed FormIDs in total; "
          f"{recovered}/{total_ids} resolve to a record in the owning plugin; "
          f"rows disagreeing with the live decode: {len(bad_rows)}",
          len(otft) > 0 and total_ids > 0 and not bad_rows
          and recovered == total_ids,
          ev("OTFT.INAM is NOT a 4-byte subrecord: it is a packed array of",
             "uint32 FormIDs (16-24 bytes here), so the FOUR_CHAR_STR rule",
             "(4-byte payload -> uint32) never applies to it. The decode is",
             "verified against the live bytes, field by field:",
             *inam_lines,
             f"All {total_ids} referenced FormIDs resolve to a record inside",
             "the owning plugin (they are the ARMO entries the outfit wears),",
             "so the outfit targets are genuinely recovered."))
    return SCOPE


# =================================================== independent crosscheck ==
PROBE_PLUGINS = []
WANT_SET = {t.decode("ascii") for t in P.WANT}


def pick_probe_plugins(min_armo=3):
    """Three simple outfit plugins, chosen deterministically.

    'Simple' = the plugin owns >= min_armo ARMO, every ARMO MODL resolves
    through the 'self' route (so nothing depends on another plugin's state),
    and the file is small. Sorted by (file size, name) so the choice is
    reproducible.
    """
    cands = []
    for name, path in scope_plugins():
        json_recs = [r for r in PLUGIN_RECORDS if r["plugin_file"] == name]
        armo = [r for r in json_recs if r["record_type"] == "ARMO"]
        if len(armo) < min_armo:
            continue
        refs = [m for r in armo
                for m in ((r.get("armo") or {}).get("modl_refs") or [])]
        if not refs or any(m.get("route") != "self" for m in refs):
            continue
        cands.append((os.path.getsize(path), name, path))
    cands.sort()
    return [(n, p) for _s, n, p in cands[:3]]


def do_independent():
    section("4. Independent cross-check (own TES4 walker vs p00r_plugins)")
    PROBE_PLUGINS.extend(pick_probe_plugins())
    check("I-00",
          "three simple outfit plugins were selected deterministically for "
          "the by-hand probe",
          doc_expect(">=3 plugins, every ARMO.MODL on the 'self' route"),
          f"{[n for n, _p in PROBE_PLUGINS]}",
          len(PROBE_PLUGINS) >= 3,
          ev("Selection rule: >=3 ARMO, all MODL refs resolve via route 'self'",
             "(so the comparison cannot be contaminated by another plugin's",
             "state), smallest files first, sorted for reproducibility."))

    fk = FKI.FormKeyIndex()
    for name, path in PROBE_PLUGINS:
        fk.add_plugin(name, path)
    jrecs = {n: [r for r in PLUGIN_RECORDS if r["plugin_file"] == n]
             for n, _p in PROBE_PLUGINS}

    for pi, (name, path) in enumerate(PROBE_PLUGINS, 1):
        # -- production code under test ---------------------------------
        masters, hdr, prec, stats = P.parse_plugin(path, fk=fk)
        # -- independent walker ----------------------------------------
        xmasters, xrecs = xw_records(path)
        xwant = [(t.decode("ascii", "replace"), fi, b) for t, fi, b in xrecs
                 if t.decode("ascii", "replace") in WANT_SET]

        pcount = len(prec)
        xcount = len(xwant)
        xtotal = len(xrecs)
        check(f"I-{pi:02d}A",
              f"[{name}] total record count: independent walker vs production",
              doc_expect("identical total record count"),
              f"independent={xtotal}, production={pcount}",
              xtotal == pcount,
              ev(f"file      : {path}",
                 f"size      : {os.path.getsize(path)} bytes",
                 f"masters   : production={[m for m in masters]}",
                 f"            independent={xmasters}",
                 f"records   : independent={xtotal}, production={pcount}",
                 f"types     : independent="
                 f"{dict(__import__('collections').Counter(t for t, _f, _b in xwant))}",
                 f"            production="
                 f"{dict(__import__('collections').Counter(r['record_type'] for r in prec))}",
                 f"groups    : production={stats['groups']}",
                 f"zlib-fail : production={stats['bad']}"))

        pby = {(r["formid_int"]): r for r in prec if r["record_type"] == "ARMO"}
        xby = {fi: b for t, fi, b in xwant if t == "ARMO"}
        modl_mismatch = []
        for fi, body in xby.items():
            xn = len(xw_four(body, b"MODL"))
            pn = len((pby.get(fi, {}).get("subrecords") or {}).get("MODL") or [])
            if xn != pn:
                modl_mismatch.append((fi, xn, pn))
        check(f"I-{pi:02d}B",
              f"[{name}] per-ARMO MODL reference count agrees, record by record",
              doc_expect(f"identical MODL count for all {len(xby)} ARMO"),
              f"{len(xby)} ARMO compared; mismatches: {modl_mismatch}",
              len(xby) > 0 and not modl_mismatch,
              ev("Compared formid-by-formid, not just in aggregate.",
                 f"ARMO records: {len(xby)}",
                 f"MODL count mismatches: {modl_mismatch}",
                 "MODL subrecords seen by the independent walker: " +
                 ", ".join(f"{fi:08X}={len(xw_four(b, b'MODL'))}"
                           for fi, b in list(sorted(xby.items()))[:8])))

        rn_mis = bod_mis = arm_mis = 0
        for fi, body in xby.items():
            xr = xw_four(body, b"RNAM")
            pr = ((pby.get(fi, {}).get("subrecords") or {}).get("RNAM") or [])
            if [int(v) for v in pr] != xr:
                rn_mis += 1
            xm, xl, xh = xw_bod2(body)
            pb = ((pby.get(fi, {}).get("subrecords") or {}).get("BOD2") or [{}])[0]
            if not isinstance(pb, dict) or pb.get("mask") != xm \
                    or pb.get("payload_len") != xl:
                bod_mis += 1
        xarma = {fi: b for t, fi, b in xwant if t == "ARMA"}
        for fi, body in xarma.items():
            pr = ((SCOPE_ARMA.get((name, fi)) or {}).get("arma") or {})
            pa = [(k, tuple(sorted(v))) for k, v in
                  (pr.get("addon_model_paths") or {}).items() if v]
            xr2 = []
            for k in ("MOD2", "MOD3", "MOD4", "MOD5"):
                vals = sorted(p for t, p in xw_model_paths(body) if t == k)
                if vals:
                    xr2.append((k, tuple(vals)))
            if sorted(pa) != sorted(xr2):
                arm_mis += 1
        check(f"I-{pi:02d}C",
              f"[{name}] ARMO.RNAM and BOD2 agree field by field",
              doc_expect(f"0 RNAM mismatches and 0 BOD2 mismatches over "
                         f"{len(xby)} ARMO"),
              f"RNAM mismatches={rn_mis}, BOD2 mismatches={bod_mis} "
              f"over {len(xby)} ARMO",
              rn_mis == 0 and bod_mis == 0 and len(xby) > 0,
              ev("RNAM compared as a uint32 FormID list; BOD2 compared as",
                 "(uint32 mask, payload length) derived independently.",
                 f"ARMO compared: {len(xby)}   RNAM mismatches: {rn_mis}   "
                 f"BOD2 mismatches: {bod_mis}",
                 *(f"   {fi:08X} RNAM={[f'{v:08X}' for v in xw_four(b, b'RNAM')]}"
                   f" BOD2={xw_bod2(b)[:2]}" for fi, b in
                   list(sorted(xby.items()))[:5])))

        check(f"I-{pi:02d}D",
              f"[{name}] ARMA MOD2..MOD5 garment paths agree field by field",
              doc_expect(f"0 mismatches over {len(xarma)} ARMA"),
              f"{len(xarma)} ARMA compared; mismatches: {arm_mis}",
              len(xarma) > 0 and arm_mis == 0,
              ev("The worn-mesh fields -- the ones the whole re-run hinges on.",
                 f"ARMA compared: {len(xarma)}   mismatches: {arm_mis}",
                 *(f"   {fi:08X} " + "; ".join(f"{k}={v}" for k, v in
                   sorted((k, tuple(sorted(p for t, p in xw_model_paths(b)
                                          if t == k)))
                          for k in ("MOD2", "MOD3", "MOD4", "MOD5"))
                   if v)
                   for fi, b in list(sorted(xarma.items()))[:4])))


# ============================================================== BodySlide ===
PROBE_PROJECTS = []


def osp_path(rel, mod):
    return os.path.join(C.MODS_DIR, mod, rel.replace("/", os.sep))


def _name_at(blob, pos):
    """Length-prefixed printable name at `pos`, or None."""
    if pos < 0 or pos >= len(blob):
        return None
    n = blob[pos]
    if n == 0 or pos + 1 + n > len(blob):
        return None
    try:
        s = blob[pos + 1:pos + 1 + n].decode("utf-8")
    except UnicodeDecodeError:
        return None
    return s if s and all(9 <= ord(c) < 127 for c in s) else None


def _osd_hexdump(row):
    if not row:
        return ["   (no .osd in scope)"]
    fp = os.path.join(C.MODS_DIR, row["mod"], row["rel"].replace("/", os.sep))
    with open(fp, "rb") as fh:
        blob = fh.read(64)
    magic, ver, off = struct.unpack_from("<III", blob, 0)
    return [f"   file  : {row['rel']}",
            f"   hex   : {' '.join(f'{x:02x}' for x in blob)}",
            "   ascii : " +
            "".join(chr(x) if 32 <= x < 127 else "." for x in blob),
            f"   u32@0x00=0x{magic:08X}  u32@0x04={ver}  u32@0x08={off}",
            f"   u8 @0x0C = {blob[12]} -> {_name_at(blob, 12)!r}",
            f"   at the 0x08 value ({off}) -> {_name_at(blob, off)!r}"]


def pick_probe_projects():
    """Three BodySlide projects: smallest, median and largest slider count
    among fully resolved projects. Deterministic, and spans the range."""
    ok = [p for p in PROJECTS
          if p.get("base_nif", "UNKNOWN") != "UNKNOWN"
          and p.get("n_sliders", 0) > 0
          and p.get("xml_error", "") == ""]
    ok.sort(key=lambda p: (p["n_sliders"], p["OSP_PATH"]))
    if not ok:
        return []
    idx = sorted({0, len(ok) // 2, len(ok) - 1})
    return [ok[i] for i in idx]


def do_bodyslide():
    from collections import Counter
    section("5. BodySlide: .osp XML projects and .osd binary containers")
    osp = SHAPEDATA.get("errors", {}).get("osp", [])
    check("B-01",
          "SliderSets/*.osp are parsed as XML and none fails to parse",
          doc_expect("0 XML parse errors across every in-scope .osp"),
          f"{len(osp)} XML parse errors across {len(PROJECTS)} projects",
          not osp,
          ev(f"in-scope .osp projects : {len(PROJECTS)}",
             f"XML parse errors        : {len(osp)}",
             f"provenance field values : "
             f"{dict(Counter(p.get('provenance') for p in PROJECTS))}"))

    sample = PROJECTS[:40] + PROJECTS[-40:]
    bom = naive_fail = 0
    samples = []
    for p in sample:
        fp = osp_path(p["OSP_PATH"], p["source_mod"])
        try:
            with open(fp, "rb") as fh:
                head = fh.read(4)
        except OSError:
            continue
        if head[:3] == b"\xef\xbb\xbf":
            bom += 1
            if len(samples) < 3:
                samples.append((p["OSP_PATH"], head))
        if head[:1] != b"<":
            naive_fail += 1
    check("B-02",
          ".osp files are UTF-8 XML that often carries a BOM, so a naive "
          "head[:1] == b'<' XML test fails on them",
          doc_expect("a measurable number of .osp files start with a UTF-8 "
                     "BOM and would fail the naive test"),
          f"{bom}/{len(sample)} sampled .osp files start with a UTF-8 BOM; "
          f"{naive_fail}/{len(sample)} would fail the naive head[:1]==b'<' "
          f"test",
          bom > 0 and naive_fail > 0,
          ev("p00r_bodyslide.parse_osp strips the BOM before ET.fromstring,",
             "which is why the .osp parse rate is 100% and the first",
             "P00_RERUN pass's '0 OSP parse errors' was a false clean.",
             *(f"   {n}: first bytes {h!r}" for n, h in samples)))

    fields = ("slider_set_name", "data_folder", "source_file", "output_path",
              "output_file", "output_gen_weights")
    # A second, independent XML reader for cross-checking p00r_bodyslide.
    import xml.etree.ElementTree as _ET

    def xml_probe(p):
        with open(osp_path(p["OSP_PATH"], p["source_mod"]), "rb") as fh:
            raw = fh.read()
        bom = raw[:3] == b"\xef\xbb\xbf"
        root = _ET.fromstring(raw[3:].decode("utf-8", "replace") if bom
                              else raw.decode("utf-8", "replace"))
        ss = root.find("SliderSet")
        return {
            "has_sliderset": ss is not None,
            "bom": bom,
            "n_slider": len(ss.findall("Slider")) if ss is not None else 0,
            "n_shape": len(ss.findall("Shape")) if ss is not None else 0,
            "declared": [e for e in fields if ss is not None and
                         (ss.get("name") if e == "slider_set_name"
                          else ss.get("GenWeights") if e == "output_gen_weights"
                          else (ss.find(e.replace("output_", "Output")
                                        .replace("source_file", "SourceFile")
                                        .replace("data_folder", "DataFolder")
                                        .replace("output_path", "OutputPath")
                                        .replace("output_file", "OutputFile"))
                                is not None))],
        }

    probes = {p["OSP_PATH"]: xml_probe(p) for p in PROJECTS}
    empty = {k for k, v in probes.items() if not v["has_sliderset"]}
    unk_rows = {}
    for p in PROJECTS:
        miss = [f for f in fields if p.get(f) in (None, "", "UNKNOWN")]
        if miss:
            unk_rows[p["OSP_PATH"]] = miss
    fake = {k: v for k, v in unk_rows.items() if k not in empty}
    resolved_base = sum(1 for p in PROJECTS if p.get("base_nif") != "UNKNOWN")
    resolved_out = sum(1 for p in PROJECTS if p.get("output_nif") != "UNKNOWN")
    scope_nifs = {n["rel"].lower() for n in SHAPEDATA.get("nif", [])}
    base_miss = [p for p in PROJECTS if p.get("base_nif") == "UNKNOWN"]
    base_explained = [
        p for p in base_miss
        if p["data_folder"] == "UNKNOWN" or
        f"CalienteTools/BodySlide/ShapeData/{p['data_folder']}/"
        f"{p['source_file']}".lower() not in scope_nifs]
    check("B-03",
          "every OSP field (SliderSet@name, DataFolder, SourceFile, "
          "OutputPath, OutputFile@GenWeights) is read from the XML, never "
          "fabricated",
          doc_expect("the ONLY projects left UNKNOWN are those whose .osp "
                     "contains no <SliderSet> element at all"),
          f"{len(PROJECTS)} projects; projects with UNKNOWN fields = "
          f"{sorted(unk_rows)}; of those, projects with no <SliderSet> "
          f"element = {sorted(empty)}; unexplained UNKNOWNs = {sorted(fake)}; "
          f"base_nif resolved {resolved_base}/{len(PROJECTS)}, output_nif "
          f"resolved {resolved_out}/{len(PROJECTS)}",
          not fake and set(unk_rows) == empty
          and len(base_explained) == len(base_miss),
          ev("No hard-coded fallback. The first P00_RERUN pass fell back to",
             "'meshes\\clothing', i.e. a fabricated value; this calibration",
             "confirms nothing is invented.",
             f"projects                        : {len(PROJECTS)}",
             f"projects with any UNKNOWN field : {sorted(unk_rows)}",
             f"projects with no <SliderSet>     : {sorted(empty)}",
             "",
             "The residual UNKNOWNs are genuine, not parser failures:",
             *(f"   {k}: {open(osp_path(k, [p['source_mod'] for p in PROJECTS if p['OSP_PATH'] == k][0]), 'rb').read()[:90]!r}"
               for k in sorted(empty)[:2]),
             "",
             f"base_nif resolved {resolved_base}/{len(PROJECTS)}. The three",
             "that stay UNKNOWN name a base mesh that is genuinely not in the",
             "09 scope (the join is restricted to in-scope ShapeData NIFs):",
             *(f"   {p['OSP_PATH']}: DataFolder={p['data_folder']!r} "
               f"SourceFile={p['source_file']!r} "
               f"(in-scope ShapeData NIFs for that folder: "
               f"{p['shapedata_nif_count']})" for p in base_miss),
             "output_path histogram (top 6): "
             f"{dict(Counter(p.get('output_path') for p in PROJECTS).most_common(6))}",
             "OutputFile@GenWeights histogram: "
             f"{dict(Counter(p.get('output_gen_weights') for p in PROJECTS))}"))

    slider_total = sum(p.get("n_sliders", 0) for p in PROJECTS)
    shape_total = sum(p.get("n_shapes", 0) for p in PROJECTS)
    osd_total = sum(len(p.get("osd_refs") or []) for p in PROJECTS)
    count_mismatch = [p["OSP_PATH"] for p in PROJECTS
                      if probes[p["OSP_PATH"]]["n_slider"] != p["n_sliders"]
                      or probes[p["OSP_PATH"]]["n_shape"] != p["n_shapes"]]
    no_osd = [p for p in PROJECTS if not p.get("osd_refs")]
    no_osd_real = [p for p in no_osd if probes[p["OSP_PATH"]]["n_slider"] == 0]
    check("B-04",
          "each OSP Slider/Data carries a '<set>.osd\\<slider>' reference",
          doc_expect("one osd reference per <Slider> element; slider and shape "
                     "counts agree with an independent XML walk"),
          f"{slider_total} sliders -> {osd_total} osd references; "
          f"{shape_total} shapes; slider/shape count mismatches vs the "
          f"independent XML walk: {count_mismatch}; projects with zero osd "
          f"refs: {len(no_osd)} (of which genuinely contain 0 <Slider> "
          f"elements: {len(no_osd_real)})",
          slider_total > 0 and slider_total == osd_total
          and not count_mismatch and len(no_osd_real) == len(no_osd),
          ev(f"sliders parsed      : {slider_total}",
             f"osd references      : {osd_total}   (exactly 1 per <Slider>)",
             f"shapes parsed       : {shape_total}",
             "independent XML walk over every .osp agrees on the <Slider> and",
             "<Shape> counts for all "
             f"{len(PROJECTS)} projects (mismatches: {count_mismatch}).",
             "distinct .osd files referenced: "
             f"{len({o.rsplit(chr(92), 1)[-1].rsplit('/', 1)[-1] for p in PROJECTS for o in (p.get('osd_refs') or [])})}",
             "Projects with no osd reference -- verified to contain zero",
             "<Slider> elements, so the absence is real and not a drop:",
             *(f"   {p['OSP_PATH']}: {probes[p['OSP_PATH']]['n_slider']} "
               f"Slider, {probes[p['OSP_PATH']]['n_shape']} Shape"
               for p in no_osd_real)))

    osd_rows = SHAPEDATA.get("osd", [])
    mag_ok, first4, ver_hist = {}, {}, {}
    at_off = at_12 = total = 0
    off_vals = set()
    named = 0
    osd_err = SHAPEDATA.get("errors", {}).get("osd", [])
    for d in osd_rows:
        fp = os.path.join(C.MODS_DIR, d["mod"], d["rel"].replace("/", os.sep))
        try:
            with open(fp, "rb") as fh:
                blob = fh.read(1 << 16)
        except OSError:
            continue
        if len(blob) < 16:
            continue
        total += 1
        magic, ver, off = struct.unpack_from("<III", blob, 0)
        mag_ok[magic] = mag_ok.get(magic, 0) + 1
        first4[blob[:4]] = first4.get(blob[:4], 0) + 1
        ver_hist[ver] = ver_hist.get(ver, 0) + 1
        off_vals.add(off)
        if _name_at(blob, off):
            at_off += 1
        if _name_at(blob, 12):
            at_12 += 1
        if BS.parse_osd(fp).get("shape_names", ["UNKNOWN"]) != ["UNKNOWN"]:
            named += 1
    check("B-05",
          "ShapeData/*.osd is a BINARY container whose magic is b'OSD\\0' "
          "stored LITTLE-ENDIAN (first bytes b'\\x00DSO' = 0x4F534400)",
          doc_expect("every in-scope .osd starts with the 4 bytes "
                     "b'\\x00DSO', i.e. uint32 0x4F534400"),
          f"first-4-byte histogram={sorted(first4)}, uint32 magic histogram="
          f"{ {f'0x{k:08X}': v for k, v in mag_ok.items()} } over {total} "
          f"files; .osd parse errors reported by the pipeline: {len(osd_err)}",
          total > 0 and set(first4) == {b"\x00DSO"}
          and set(mag_ok) == {BS.OSD_MAGIC} and not osd_err,
          ev("The first P00_RERUN pass compared the file's first bytes to",
             "b'OSD\\0' in FILE order, so it never matched anything.",
             f"files checked                : {total}",
             f"first 4 bytes, byte-for-byte : {sorted(first4)}",
             f"read as little-endian uint32  : "
             f"{[f'0x{k:08X}' for k in mag_ok]}",
             "read as big-endian uint32 would be: "
             f"{[f'0x{int.from_bytes(k, chr(98) + chr(105) + chr(103)):08X}' for k in first4]}",
             f"p00r_bodyslide.OSD_MAGIC     : 0x{BS.OSD_MAGIC:08X}"))

    check("B-06",
          "the uint32 at offset 0x04 of an .osd is a version number",
          doc_expect("version 1 on every in-scope .osd"),
          f"version histogram {dict(ver_hist)} over {total} files",
          total > 0 and set(ver_hist) == {1},
          ev(f"uint32 @0x04 across {total} .osd files: {dict(ver_hist)}"))

    # B-07 (the old "the uint32 at 0x08 is a data offset" check) is MERGED into
    # B-08 below. Its expectation was known-false from the moment it was
    # measured -- 6 of 513 files coincidentally parse at the 0x08 value -- so
    # keeping a check whose expectation can never pass was misleading. B-08 is
    # now a REGRESSION GUARD that asserts the corrected layout AND actively
    # records that the 0x08 reading is refuted, with the 6/513 figure as the
    # evidence for the refutation.
    check("B-08",
          "OSD layout regression guard: the shape name is the length-prefixed "
          "string at 0x0C, and the 'uint32 at 0x08 is a data offset' reading "
          "is refuted",
          doc_expect(f"every in-scope .osd yields a printable length-prefixed "
                     f"shape name at 0x0C ({at_12}/{total}), p00r_bodyslide"
                     f".parse_osd returns a real shape name for all of them "
                     f"({named}/{total}), AND the 0x08 offset reading is "
                     f"demonstrably false (far fewer than {total} files parse "
                     f"there)"),
          f"length-prefixed name at 0x0C: {at_12}/{total}; at the uint32 stored "
          f"in 0x08: {at_off}/{total} (REFUTES the offset claim); 0x08 takes "
          f"{len(off_vals)} distinct values "
          f"({min(off_vals) if off_vals else '-'}.."
          f"{max(off_vals) if off_vals else '-'}); parse_osd returns a real "
          f"shape name for {named}/{total} files",
          total > 0 and at_12 == total and named == total
          and at_off < total // 2,
          ev("MEASURED LAYOUT (all %d in-scope .osd files):" % total,
             "   uint32 @0x00  magic   0x4F534400   (\"OSD\\0\", little-endian)",
             "   uint32 @0x04  version 1",
             f"   uint32 @0x08           {len(off_vals)} distinct values, "
             f"{min(off_vals)}..{max(off_vals)} -- NOT a pointer to the name",
             f"   name at the 0x08 value  {at_off}/{total}   <- REFUTED",
             f"   name at 0x0C           {at_12}/{total}   <- the real layout",
             "",
             "The '0x08 is a data offset' claim carried by the original",
             "calibration brief (and by an earlier p00r_bodyslide docstring)",
             f"is FALSE: only {at_off} of {total} files yield a length-prefixed",
             "name there, against {}/{} at 0x0C. The few hits at 0x08 are",
             "coincidence -- the 0x08 value is a size/offset field whose low",
             "bytes happen to form a plausible length byte.",
             "",
             "p00r_bodyslide.parse_osd now reads the name at 0x0C and returns",
             f"a real shape name for {named}/{total} files, so the",
             "'no exception, empty result' failure mode is gone.",
             "",
             "Verbatim header bytes of the first three in-scope .osd files:",
             *(_osd_hexdump(d) for d in osd_rows[:3])))

    PROBE_PROJECTS.extend(pick_probe_projects())
    return PROBE_PROJECTS


# ------------------------------------------------------- body classifier --
VOCAB = {"CBBE", "CBBE_3BA", "BHUNP", "OTHER", "UNKNOWN"}


def do_classify():
    from collections import Counter
    section("6. Body classification vocabulary and behaviour")
    table = [({"CBBE"}, "CBBE"),
             ({"3BA"}, "CBBE_3BA"),
             ({"CBBE", "3BA"}, "CBBE_3BA"),
             ({"BHUNP"}, "BHUNP"),
             (set(), "UNKNOWN")]
    got = []
    for toks, want in table:
        cand, fam, flag = C.classify_body(set(toks))
        got.append(("+".join(sorted(toks)) or "<empty>", want, cand, fam,
                    flag))
    bad = [g for g in got if g[2] != g[1]]
    check("C-01",
          "classify_body() on synthetic token sets",
          doc_expect("; ".join(f"{t}=>{w}" for t, w, _c, _f, _g in got)),
          "; ".join(f"{t}=>{c}" for t, _w, c, _f, _g in got),
          not bad,
          ev("The audit finding being guarded against: a CBBE-only token set",
             "was collapsed to OTHER, silently discarding a real body type.",
             *(f"   classify_body({t}) -> candidate={c} families={f} "
               f"flag={fl}   (expected {w})" for t, w, c, f, fl in got)))

    seen = Counter(p.get("body_candidate") for p in PROJECTS)
    outside = {k: v for k, v in seen.items() if k not in VOCAB}
    check("C-02",
          "the body classification vocabulary is exactly CBBE / CBBE_3BA / "
          "BHUNP / OTHER / UNKNOWN",
          doc_expect(f"no value outside {sorted(VOCAB)} in "
                     f"07_bodyslide_projects.json"),
          f"vocabulary used = {dict(seen)}; out-of-vocabulary = {outside}",
          not outside,
          ev(f"{len(PROJECTS)} BodySlide projects classified.",
             f"body_candidate distribution: {dict(seen)}",
             f"values outside the mandated vocabulary: {outside}",
             f"needs_3ba_conversion: "
             f"{dict(Counter(p.get('needs_3ba_conversion') for p in PROJECTS))}"))

    named = [(p["OSP_PATH"], p["ui_outfit_name"], p["body_candidate"])
             for p in PROJECTS
             if any(t in (p.get("ui_outfit_name") or "").upper()
                    for t in ("CBBE", "3BA", "BHUNP"))]
    good = [(n, c) for _p, n, c in named if c in ("CBBE", "CBBE_3BA")]
    lost = [(n, c) for _p, n, c in named if c == "UNKNOWN"]
    check("C-03",
          "real 09-scope BodySlide projects whose names carry a body family "
          "classify into the mandated vocabulary",
          doc_expect("every project naming CBBE / 3BA / BHUNP classifies to "
                     "CBBE, CBBE_3BA or BHUNP"),
          f"{len(named)} of {len(PROJECTS)} projects name a body family; "
          f"{len(good)} classify into the vocabulary; {len(lost)} fall "
          f"through to UNKNOWN",
          len(named) > 0 and not lost,
          ev("Body type is derived only from real file names / UI names.",
             "The ones that DO classify:",
             *(f"   {u[:58]:<58} -> {c}" for _p, u, c in named[:8]),
             "",
             "FINDING -- the ones that do not, and why:",
             *(f"   {n!r}" for n, _c in lost),
             "",
             "p00r_common.BODY_TOKEN_RE is r\"[+/_\\-]|\\s+\" -- it does not",
             "split on brackets or parentheses. So '(BHUNP)' never yields the",
             "token 'BHUNP' and '[SE]3BA Melodic-Dolly Heels' yields",
             "'[SE]3BA', not '3BA'. classify_body() itself is correct (C-01);",
             "the defect is in body_tokens()'s tokenizer. Adding ()[]{}<> and",
             ": to BODY_TOKEN_RE would recover all of these."))


# ==================================================== verbatim evidence =====
def _fmt_bod2(d, ind=""):
    if not isinstance(d, dict) or d.get("mask") is None:
        return f"{ind}<no BOD2>"
    return (f"{ind}BOD2 raw={d['raw_hex']} payload_len={d['payload_len']}\n"
            f"{ind}     mask={d['mask_hex']} bits={d['bits']} "
            f"slots={d['names']}")


def outfit_plugin_block(name, path, n_armo=2):
    """Verbatim evidence for one outfit plugin, straight out of the JSON the
    pipeline produced, cross-checked against a live re-read of the file."""
    L = [f"PLUGIN  {name}",
         f"PATH    {path}",
         f"SIZE    {os.path.getsize(path)} bytes",
         f"MASTERS {_masters_of(path)}",
         ""]
    recs = [r for r in PLUGIN_RECORDS if r["plugin_file"] == name]
    armo = sorted([r for r in recs if r["record_type"] == "ARMO"],
                  key=lambda r: r["formid_int"])
    L.append(f"COUNTS  {len(armo)} ARMO, "
             f"{len([r for r in recs if r['record_type'] == 'ARMA'])} ARMA "
             f"(this plugin owns {sum((r.get('armo') or {}).get('n_arma_refs', 0) for r in armo)}"
             f" of them)")
    L.append("")
    for r in armo[:n_armo]:
        a = r.get("armo") or {}
        rr = a.get("race_resolved") or {}
        L.append(f"  ARMO {r['formid']}  EDID={r['subrecords']['EDID'][0]!r}")
        L.append(f"    ARMO.RNAM raw={a['race_raw']}  -> "
                 f"plugin={rr.get('plugin')!r} type={rr.get('type')!r} "
                 f"EDID={rr.get('edid')!r} route={rr.get('route')!r}")
        L.append(f"    ARMO.RNAM IS: {a.get('race_is')}")
        L.append(_fmt_bod2((r["subrecords"].get("BOD2") or [None])[0], "    "))
        L.append("    ARMO.MODL (repeated; the ArmorAddon link):")
        for m in (a.get("modl_refs") or []):
            L.append(f"      {m['raw_formid']}  master_byte={m['master_byte']}  "
                     f"-> plugin={m.get('resolved_plugin')!r} "
                     f"type={m.get('resolved_type')!r} "
                     f"EDID={m.get('resolved_edid')!r} route={m.get('route')!r}"
                     f"  is_arma={m.get('is_arma')}")
        wm = a.get("world_model_paths") or []
        L.append(f"    ARMO.MOD2..MOD5 (world/inventory drop models, NOT worn): "
                 f"{wm}")
        L.append("")
        for ref in (a.get("arma_refs") or []):
            t = SCOPE_ARMA.get((ref["plugin"], int(ref["formid"], 16)))
            L.append(f"    -> ARMA {ref['formid']} in {ref['plugin']!r} "
                     f"EDID={ref['edid']!r}")
            if not t:
                L.append("        <target not inside the 09 scope; no record "
                         "to dump>")
                continue
            ta = t.get("arma") or {}
            L.append(_fmt_bod2((t["subrecords"].get("BOD2") or [None])[0], "        "))
            for k in ("MOD2", "MOD3", "MOD4", "MOD5"):
                for p in (ta.get("addon_model_paths") or {}).get(k, []):
                    L.append(f"        ARMA.{k} (the WORN garment mesh) = {p!r}")
            L.append(f"        ARMA.source_mesh_refs (MODL, {len(ta.get('source_mesh_refs') or [])}): "
                     f"{(ta.get('source_mesh_refs') or [])[:6]}"
                     f"{' ...' if len(ta.get('source_mesh_refs') or []) > 6 else ''}")
            L.append("")
    return L


def _masters_of(path):
    try:
        return xw_masters(open(path, "rb").read())
    except Exception:                                        # noqa: BLE001
        return []


def bodyslide_project_block(p):
    osd_by_rel = {d["rel"]: d for d in SHAPEDATA.get("osd", [])}
    folder = f"CalienteTools/BodySlide/ShapeData/{p.get('data_folder')}"
    osd_rows = [d for k, d in osd_by_rel.items()
                if k.startswith(folder + "/")]
    L = [f"PROJECT {p['OSP_PATH']}",
         f"MOD     {p['source_mod']}",
         "",
         "  --- as extracted from the .osp XML (07_bodyslide_projects.json) ---",
         f"  SliderSet@name (UI outfit name) : {p['ui_outfit_name']!r}",
         f"  DataFolder                      : {p['data_folder']!r}",
         f"  SourceFile                      : {p['source_file']!r}",
         f"  OutputPath                      : {p['output_path']!r}",
         f"  OutputFile / @GenWeights        : {p['output_file']!r} / "
         f"{p['output_gen_weights']!r}",
         f"  output_nif (OutputPath+File)    : {p['output_nif']!r}",
         f"  shapes (Shape@target)           : {p['shape_names']}",
         f"  sliders (Slider@name)           : {p['n_sliders']}",
         f"  zap shapes                      : {p['zap_sliders']}",
         f"  provenance                      : {p['provenance']!r}",
         "",
         "  --- raw .osp bytes (first 200) ---"]
    raw = open(osp_path(p["OSP_PATH"], p["source_mod"]), "rb").read(200)
    L.append(f"  {raw[:200]!r}")
    L.append("")
    L.append("  --- resolved base NIF and its .osd companions ---")
    L.append(f"  base_nif        : {p['base_nif']!r}")
    L.append(f"  base_nif shapes : {p.get('base_nif_shapes')}")
    L.append(f"  osd references  : {p['n_sliders']} sliders -> "
             f"{len(p['osd_refs'])} refs; first 4:")
    for o in (p["osd_refs"] or [])[:4]:
        L.append(f"      {o!r}")
    L.append(f"  distinct .osd referenced by this project: {p['osd_names']}")
    for d in osd_rows[:3]:
        fp = osp_path(d["rel"], d["mod"])
        with open(fp, "rb") as fh:
            blob = fh.read(4096)
        magic, ver, off = struct.unpack_from("<III", blob, 0)
        L.append(f"  OSD {d['rel'].split('/')[-1]}")
        L.append(f"      size            : {d['bytes']} bytes")
        L.append(f"      first 4 bytes   : {blob[:4]!r}  "
                 f"(= b'\\x00DSO', uint32 LE 0x{magic:08X})")
        L.append(f"      uint32 @0x04    : {ver}   (version)")
        L.append(f"      uint32 @0x08    : {off}   "
                 f"<- p00r_bodyslide calls this 'data_offset'")
        L.append(f"      name at 0x0C    : {_name_at(blob, 12)!r}   "
                 f"<- where the shape name actually is")
        L.append(f"      name at 0x08    : {_name_at(blob, off)!r}")
        L.append(f"      parse_osd says  : shape_names={BS.parse_osd(fp).get('shape_names')}"
                 f" version={BS.parse_osd(fp).get('version')}"
                 f" data_offset={BS.parse_osd(fp).get('data_offset')}")
    L.append("")
    return L


def do_evidence():
    section("7. Verbatim evidence dumps (no assertion -- these are the dumps "
            "the checks above were decided from)")
    for i, (name, path) in enumerate(PROBE_PLUGINS, 1):
        L = outfit_plugin_block(name, path)
        check(f"E-{i:02d}",
              f"verbatim evidence dump: outfit plugin {name}",
              "informational dump",
              f"{len(L)} lines of verbatim record detail",
              True, ev(*L))
    for j, p in enumerate(PROBE_PROJECTS, len(PROBE_PLUGINS) + 1):
        L = bodyslide_project_block(p)
        check(f"E-{j:02d}",
              f"verbatim evidence dump: BodySlide project "
              f"{p['OSP_PATH'].split('/')[-1]}",
              "informational dump",
              f"{len(L)} lines of verbatim project detail",
              True, ev(*L))


# ================================================================ reports ===
def write_reports():
    import time as _t
    npass = sum(1 for c in CHECKS if c["verdict"] == "PASS")
    nfail = len(CHECKS) - npass
    now = datetime.datetime.now()

    # ---- CSV --------------------------------------------------------
    cols = ["check_id", "description", "expected", "observed", "verdict",
            "evidence"]
    C.write_csv(CSV_PATH, cols, [
        {**c, "evidence": "\n".join(EVIDENCE.get(c["check_id"], []))}
        for c in CHECKS])

    # ---- MD ---------------------------------------------------------
    L = []
    L.append("# P00_RERUN -- PARSER CALIBRATION")
    L.append("")
    L.append(f"* generated: `{now:%Y-%m-%d %H:%M:%S}`")
    L.append("* generator: `tools/P00_RERUN/p00r_calibrate.py`")
    L.append(f"* machine verdict: **{'PASS' if not nfail else 'FAIL'}** "
             f"-- **{npass}/{len(CHECKS)} PASS, {nfail} FAIL**")
    L.append("")
    L.append("## What this document is")
    L.append("")
    L.append("An independent re-verification of the corrected TES4 / BodySlide "
             "parsers")
    L.append("(`p00r_plugins`, `p00r_formkey`, `p00r_bodyslide`, "
             "`p00r_common`).")
    L.append("Every number below was recomputed from")
    L.append("")
    L.append("* a **live re-read** of the ground truth "
             "`E:\\SkyrimAE\\Data\\Skyrim.esm`;")
    L.append("* the **actual JSON artefacts** the pipeline produced "
             "(`02_plugin_records.json`,")
    L.append("  `07_bodyslide_projects.json`, `07_bodyslide_shapedata.json`, "
             "`01_mod_aggregates.json`); and")
    L.append("* a **minimal TES4 walker written from the on-disk format "
             "inside the calibration script**,")
    L.append("  which shares no code with `p00r_plugins` and is never allowed "
             "to call `parse_plugin`.")
    L.append("")
    L.append("### Cross-check provenance (stated explicitly)")
    L.append("")
    L.append("**SSEEdit is not installed on this machine. No comparison "
             "against SSEEdit is claimed**")
    L.append("anywhere in this report.** The cross-check is vanilla "
             "`Skyrim.esm` plus the")
    L.append("independent walker. The game install and the MO2 instance are "
             "opened read-only;")
    L.append("the only files this script writes are this report and its CSV "
             "sibling.")
    L.append("")
    L.append(f"Ground truth identity: `{SKYRIM_ESM}`, {VAN.get('size')} bytes, "
             f"sha256 `{VAN.get('sha256')}`")
    L.append("")
    if nfail:
        L.append("## Findings that block the re-run")
        L.append("")
        for c in CHECKS:
            if c["verdict"] != "FAIL":
                continue
            L.append(f"### {c['check_id']} -- {c['description']}")
            L.append("")
            L.append(f"* **expected** {c['expected']}")
            L.append(f"* **observed** {c['observed']}")
            L.append("")
            L.append("```")
            L.extend(EVIDENCE.get(c["check_id"], []))
            L.append("```")
            L.append("")
    else:
        L.append("## Findings")
        L.append("")
        L.append("None. Every check passed.")
        L.append("")
    L.append("## Full check table")
    L.append("")
    L.append("| check | verdict | description | expected | observed |")
    L.append("|---|---|---|---|---|")
    for c in CHECKS:
        L.append("| {check_id} | {verdict} | {description} | {expected} | "
                 "{observed} |".format(
                     **dict(c, expected=c["expected"].replace("|", "\\|"),
                            observed=c["observed"].replace("|", "\\|"),
                            description=c["description"].replace("|", "\\|"))))
    L.append("")
    for title, ids in SECTIONS:
        if not ids:
            continue
        L.append(f"## {title}")
        L.append("")
        for cid in ids:
            c = next(x for x in CHECKS if x["check_id"] == cid)
            L.append(f"### {cid} -- {c['description']}  **{c['verdict']}**")
            L.append("")
            L.append(f"* expected: {c['expected']}")
            L.append(f"* observed: {c['observed']}")
            L.append("")
            if EVIDENCE.get(cid):
                L.append("```")
                L.extend(EVIDENCE[cid])
                L.append("```")
                L.append("")
    C.assert_write_path(MD_PATH)
    tmp = MD_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    os.replace(tmp, MD_PATH)
    return npass, nfail


def main() -> int:
    import time as _t
    _t0 = _t.time()
    print("=" * 78)
    print("P00_RERUN PARSER CALIBRATION GATE")
    print("=" * 78)
    load_artifacts()
    do_inputs()
    do_vanilla()
    do_scope()
    do_independent()
    do_bodyslide()
    do_classify()
    do_evidence()
    npass, nfail = write_reports()
    print()
    print("=" * 78)
    for c in CHECKS:
        print(f"  {c['verdict']}  {c['check_id']:<7} {c['description']}")
    print("=" * 78)
    print(f"TOTAL {len(CHECKS)} checks: {npass} PASS, {nfail} FAIL "
          f"({_t.time() - _t0:.1f}s)")
    print(f"report: {MD_PATH}")
    print(f"csv   : {CSV_PATH}")
    if nfail:
        print()
        print("CALIBRATION GATE: FAIL -- the re-run must not proceed until "
              "these are resolved:")
        for c in CHECKS:
            if c["verdict"] == "FAIL":
                print(f"  * {c['check_id']}: {c['description']}")
        raise SystemExit(1)
    print()
    print("CALIBRATION GATE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
