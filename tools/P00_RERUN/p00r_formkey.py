#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p00r_formkey.py — canonical FormKey resolution for Skyrim SE plugin records.

Why this module exists
----------------------
A TES4 formid is 8 bytes: a 1-byte master index + a 3-byte local id. The master
index does NOT mean "the Nth master in my MAST list" in the naive sense -- the
plugin's own records also carry a master byte, and in this install that byte is
`len(masters)`. Verified against AE_HoodST.esp, whose own ARMO records are
0x01000003 while its MAST list holds exactly one entry (Skyrim.esm).

Naive joins fail here in two ways that were both real bugs in the first
P00_RERUN pass:
  * joining on (plugin, raw_formid) can never see a reference that points at a
    master, a different plugin, or a plugin that is not in scope;
  * ARMO.MODL in this corpus points at ArmorAddon records that live in
    third-party armors-replacer plugins, not in the armour mod itself.

Resolution order (first hit wins, and the route taken is recorded so the
result is auditable rather than silently guessed):
  1. "self"            the referring plugin's own records
  2. "master[n]"       the n-th declared master
  3. "master_any"      any declared master
  4. "skyrim"          Skyrim.esm
  5. "library"         any plugin in the library holding that formid
  6. "unresolved"

Read-only. Nothing outside data/P00_RERUN is written.
"""
from __future__ import annotations

import gzip
import json
import os
import struct
import sys
import time
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p00r_common as C  # noqa: E402

MASTER = 0x00FFFFFF


def read_masters(path: str):
    """MAST list from the TES4 header, which iter_record() deliberately skips."""
    try:
        with open(path, "rb") as fh:
            head = fh.read(1 << 16)
    except OSError:
        return []
    if head[:4] != b"TES4":
        return []
    dsz = struct.unpack_from("<I", head, 4)[0]
    out = []
    for st, sb in iter_subrecords(head[24:24 + dsz]):
        if st == b"MAST":
            out.append(sb.split(b"\x00", 1)[0].decode("utf-8", "replace")
                       .lower())
    return out


def iter_subrecords(data: bytes):
    pos, n = 0, len(data)
    while pos + 6 <= n:
        st, ss = struct.unpack_from("<4sH", data, pos)
        pos += 6
        if pos + ss > n:
            return
        yield st, data[pos:pos + ss]
        pos += ss


def iter_record(path: str):
    """Yield (record_type, formid, raw_body) for every record in a plugin.

    CORRECTED: a GRUP group can itself be COMPRESSED (its flags carry
    0x40000). The previous walker treated a group's dsize as an on-disk extent
    and recursed straight into the deflate stream, so the first compressed
    group in Skyrim.esm desynchronised the walk and the file was truncated to
    3.9% of its records -- which is why no vanilla ArmorAddon was ever indexed
    and 443 in-scope MODL references came back unresolved.

    Compressed payload layout: uint32 uncompressed length + deflate stream,
    running to the end of the record. There is NO trailing 4-byte terminator.

    Because group children may live in a decompressed buffer, the scan works on
    (buffer, start, end) rather than a single shared file offset.
    """
    import zlib
    blob = open(path, "rb").read()
    n = len(blob)
    if n < 32 or blob[:4] != b"TES4":
        return
    start = 24 + struct.unpack_from("<I", blob, 4)[0]
    stats = {"groups": 0, "groups_compressed": 0, "records": 0,
             "records_compressed": 0, "decompress_failed": 0}

    def ok(buf, p):
        # A record/group tag is 4 printable ASCII bytes. Restricting this to
        # A-Z looks right but is wrong: many TES4 types contain '_' (0x5F),
        # e.g. NPC_, and rejecting them desynchronised the walk at the first
        # NPC_ group in Skyrim.esm, truncating the file to 3.9% of its records.
        if p + 24 > len(buf):
            return False
        t = buf[p:p + 4]
        return len(t) == 4 and all(0x20 <= c <= 0x7E for c in t)

    def scan(buf, pos, end, depth=0):
        if depth > 64:
            return
        while pos + 24 <= len(buf) and pos < end:
            if not ok(buf, pos):
                nxt = pos + 1
                while nxt + 24 <= len(buf) and not ok(buf, nxt):
                    nxt += 1
                if nxt >= end:
                    return
                pos = nxt
                continue
            rt, ds, fl, fi = struct.unpack_from("<4sIII", buf, pos)
            if rt == b"GRUP":
                stats["groups"] += 1
                # A GRUP header is: 'GRUP', dsize, groupType(4), label(4).
                # There is NO flags field -- the third DWORD is the group TYPE,
                # and a type like 'ARMO' (0x4F4D5241) happens to have bit
                # 0x40000 set. Treating that as "compressed group" made the
                # inflate fail and the whole group was skipped, which is how
                # all 2,762 vanilla ARMO records went missing. GRUP dsize
                # INCLUDES its own 24-byte header, so children live in
                # [pos+24, pos+ds).
                body = pos + 24
                yield from scan(buf, body, pos + ds, depth + 1)
                pos = pos + ds
                continue
            stats["records"] += 1
            try:
                if fl & 0x40000:
                    # A real compressed record: uint32 uncompressed length,
                    # then the deflate stream running to the end. The length
                    # prefix must be skipped; there is no trailing terminator.
                    stats["records_compressed"] += 1
                    body = zlib.decompress(buf[pos + 28:pos + 24 + ds])
                else:
                    body = buf[pos + 24:pos + 24 + ds]
            except Exception:                            # noqa: BLE001
                stats["decompress_failed"] += 1
                pos += 24 + ds
                continue
            yield rt.decode("ascii", "replace"), fi, body
            pos += 24 + ds

    yield from scan(blob, start, n)


class FormKeyIndex:
    """FormKey -> (plugin, record_type, edid), with route-aware resolution."""

    def __init__(self):
        self.by_plugin = {}          # plugin_name -> {formid: (type, edid)}
        self.masters = {}            # plugin_name -> [master names]
        self.lower_to_name = {}      # lowercase file name -> canonical name
        self.paths = {}              # plugin_name -> abs path
        self.formid_owner = {}       # formid -> [plugin names] (library scan)
        self.stats = defaultdict(int)

    # -- construction -----------------------------------------------------
    def add_plugin(self, name: str, path: str, records=None):
        if name in self.by_plugin:
            return
        self.by_plugin[name] = {}
        self.masters[name] = read_masters(path)
        self.paths[name] = path
        self.lower_to_name.setdefault(name.lower(), name)
        for rt, fi, body in (records if records is not None
                             else iter_record(path)):
            if rt == "TES4":
                continue
            edid = ""
            for st, sb in iter_subrecords(body):
                if st == b"EDID":
                    edid = sb.split(b"\x00", 1)[0].decode("utf-8", "replace")
                    break
            self.by_plugin[name][fi] = (rt, edid)
            self.formid_owner.setdefault(fi, []).append(name)
        self.stats["plugins_indexed"] += 1
        self.stats["records_indexed"] += len(self.by_plugin[name])

    def build(self, paths, log=True):
        t0 = time.time()
        for i, (name, path) in enumerate(paths, 1):
            try:
                self.add_plugin(name, path)
            except Exception as e:                       # noqa: BLE001
                self.stats["plugin_errors"] += 1
                if log and self.stats["plugin_errors"] <= 5:
                    C.log(f"  !! {name}: {e!r}")
            if log and i % 400 == 0:
                C.log(f"  indexed {i}/{len(paths)} plugins "
                      f"({self.stats['records_indexed']:,} records)")
        if log:
            C.log(f"FormKey index: {self.stats['plugins_indexed']:,} plugins, "
                  f"{self.stats['records_indexed']:,} records in "
                  f"{time.time()-t0:.0f}s")
        return self

    # -- resolution -------------------------------------------------------
    def resolve(self, from_plugin: str, formid: int):
        """Return (plugin, record_type, edid, route) or (None,...,route)."""
        self.stats["resolve_calls"] += 1
        if not formid:
            return (None, "", "", "null")
        mid = (formid >> 24) & 0xFF
        ms = self.masters.get(from_plugin, [])
        # route 1: the referring plugin itself. Its own records carry the
        # master byte len(masters); tolerate any byte as a fallback.
        own = self.by_plugin.get(from_plugin, {})
        if formid in own:
            self.stats["route_self"] += 1
            t, e = own[formid]
            return (from_plugin, t, e, "self")
        # route 2: the n-th declared master
        if 0 <= mid < len(ms):
            mname = self.lower_to_name.get(ms[mid])
            if mname and formid in self.by_plugin.get(mname, {}):
                t, e = self.by_plugin[mname][formid]
                self.stats["route_master_n"] += 1
                return (mname, t, e, f"master[{mid}]")
        # route 3: any declared master
        for mn in ms:
            mname = self.lower_to_name.get(mn)
            if mname and formid in self.by_plugin.get(mname, {}):
                t, e = self.by_plugin[mname][formid]
                self.stats["route_master_any"] += 1
                return (mname, t, e, f"master_any[{mn}]")
        # route 4: Skyrim.esm. Resolve the name case-insensitively -- the
        # index is keyed by the on-disk file name, which is capitalised, and
        # a literal ("skyrim.esm",) lookup silently missed every RACE ref.
        sk = self.lower_to_name.get("skyrim.esm")
        if sk and formid in self.by_plugin.get(sk, {}):
            t, e = self.by_plugin[sk][formid]
            self.stats["route_skyrim"] += 1
            return (sk, t, e, "skyrim")
        # route 5: the formid is owned by exactly ONE plugin in the whole
        # library, so ownership is unambiguous even though the master byte
        # did not select it. If two or more plugins hold the same formid we
        # have no evidence of which one is meant, and guessing (e.g. taking
        # the alphabetically first) manufactures false links -- measured
        # here as a Silent_Code glove resolving to an unrelated HoodST body
        # addon. Ambiguity is reported, not resolved.
        owners = self.formid_owner.get(formid)
        if owners and len(owners) == 1:
            pick = owners[0]
            t, e = self.by_plugin[pick][formid]
            self.stats["route_library_unique"] += 1
            return (pick, t, e, "library_unique")
        if owners:
            self.stats["route_ambiguous"] += 1
            return (None, "", "", f"ambiguous({len(owners)})")
        self.stats["route_unresolved"] += 1
        return (None, "", "", "unresolved")

    def summary(self):
        return {
            "plugins": len(self.by_plugin),
            "records": self.stats.get("records_indexed", 0),
            "resolve_calls": self.stats.get("resolve_calls", 0),
            "route_self": self.stats.get("route_self", 0),
            "route_master_n": self.stats.get("route_master_n", 0),
            "route_master_any": self.stats.get("route_master_any", 0),
            "route_skyrim": self.stats.get("route_skyrim", 0),
            "route_library_unique": self.stats.get("route_library_unique", 0),
            "route_ambiguous": self.stats.get("route_ambiguous", 0),
            "route_unresolved": self.stats.get("route_unresolved", 0),
        }


def library_paths(mods_dir=C.MODS_DIR):
    """Every plugin file in the library, plus Skyrim.esm first."""
    out = []
    esm = os.path.join(C.GAME_DATA, "Skyrim.esm")
    if os.path.isfile(esm):
        out.append(("Skyrim.esm", esm))
    for dp, dn, fn in os.walk(mods_dir):
        dn.sort()
        for f in sorted(fn):
            if f.lower().endswith((".esp", ".esm", ".esl")):
                out.append((f, os.path.join(dp, f)))
    return out


if __name__ == "__main__":
    C.ensure_dirs()
    C.log("building full-library FormKey index ...")
    fk = FormKeyIndex().build(library_paths())
    C.write_json(os.path.join(C.DATA, "05_formkey_summary.json"),
                 fk.summary())
    C.log("summary: " + json.dumps(fk.summary(), ensure_ascii=False))
