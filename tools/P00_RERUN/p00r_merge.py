#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p00r_merge.py — rebuild reports/P00_RERUN/18_PLUGIN_MERGE_RISK.csv.

WHY THE PREVIOUS IMPLEMENTATION IS DISCARDED
---------------------------------------------
It rated a plugin MERGE_MODERATE because "N formids collide with other in-scope
plugins", i.e. because the same raw 32-bit FormID value occurs in two different
plugins.  That is not evidence of merge risk.  In Skyrim every plugin allocates
its FormIDs from the same low range, two plugins routinely ship 0x00000019, and
a merge tool *remaps* FormIDs by construction.  The criterion is removed
outright and no column derived from it survives in this module.

WHAT REPLACES IT
----------------
Positive evidence, read only from the frozen stage-B / stage-G output:

  1. record types the plugin actually owns (02_plugin_records.json),
  2. every FormID reference slot it carries and what that slot points at,
     resolved in this order (the route is recorded, never guessed):
         a. the plugin's own records            -> SELF        (exact match)
         b. the n-th declared MAST entry         -> master[n]
         c. 0xFF                                 -> SELF
         d. the plugin's own master byte         -> SELF_HEURISTIC (inference)
         e. anything else                        -> UNRESOLVABLE (dangling)
  3. config-level coupling from 14_config_refs.json, split by what the config
     actually keys on: a hard-coded FormID, a plugin file name, or a NIF path.
  4. the master list, split into official game files vs everything else.

Route (d) exists because of a real, documented property of this install: the
in-scope plugins address their OWN records with a master byte that is neither
0xFF nor a valid index into their MAST list (e.g. AE_HoodST.esp owns
0x01000003 while its MAST list holds exactly one entry, Skyrim.esm).  That is
why step (a) -- an exact lookup in the plugin's own record set -- is tried first.

OTFT IS NOT A SCRIPT TYPE
-------------------------
OTFT (Outfit) is a *reference* record: its INAM subrecord is a list of FormIDs
naming the outfits it relates to, and those FormIDs must be remapped along with
everything else.  The earlier pass folded OTFT into a script bucket together
with SCPT/QUES/PERK, which hid the fact that a script and a remappable
reference list are different problems with different fixes.  OTFT now has its
own reference_class, REFERENCE_REMAP_REQUIRED, and its own columns.

READ-ONLY.  Only data/P00_RERUN/*.json is read; only the one CSV is written,
guarded by p00r_common.assert_write_path.

Usage: python tools/P00_RERUN/p00r_merge.py
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p00r_common as C  # noqa: E402

# ------------------------------------------------------------- classifiers --
# Stage B (p00r_plugins.WANT) decodes exactly these record types.  A type in
# this set that is absent is PROOF of absence.  A type outside it was never
# walked, so its absence proves nothing and is reported as such.
STAGE_B_WANT = ("ARMO", "ARMA", "TXST", "COBJ", "ENCH", "KYWD", "OTFT",
                "LVLI", "FLST", "MGEF", "SPEL", "PERK")

SCRIPT_TYPES = ("SCPT", "QUES", "VMAD", "ACTI")          # record level
MAGIC_GRAPH_TYPES = ("PERK", "MGEF", "SPEL", "ENCH")     # effect graphs
REMAP_CONTAINER_TYPES = ("LVLI", "FLST", "KYWD")        # FormID containers
OTFT_TYPE = "OTFT"
SIMPLE_TYPES = ("ARMO", "ARMA", "TXST", "COBJ")

# Official game files: always present at load, a fixed load-order fact, and not
# an "out of scope hard-coded reference" in any sense that matters.
GAME_FILES = {"skyrim.esm", "update.esm", "dawnguard.esm", "hearthfires.esm",
              "dragonborn.esm"}

# Subrecords that hold FormID references.  ARMO.KSIZ is deliberately excluded
# (8 distinct small scalar values 3..N, it is not a reference); ARMO/ARMA
# OBND is excluded (a bounding-box struct).  ARMA.MODL and ARMA.RNAM ARE
# included -- they are material and armour-material FormIDs -- and are counted
# honestly even though they resolve to Skyrim.esm in practice.
REF_SUBRECORD_TAGS = {
    "RNAM", "MODL", "YNAM", "ZNAM", "EITM", "SNDD", "KWDA", "INAM", "ENAM",
    "NAM1", "BNAM", "CNAM", "CNTO", "COCT",
    "MO2S", "MO3S", "MO4S", "MO5S", "MO2T", "MO3T", "MO4T", "MO5T",
}
NON_FORMID_SUBRECORD_TAGS = {"OBND", "KSIZ", "BOD2", "BODT", "DATA", "DNAM",
                             "EDID", "FULL", "DESC", "ITXT", "VMAD"}

# reference_class values, most severe first.  A plugin gets one primary class
# plus the complete set in reference_classes_all.
REFCLASS_ORDER = (
    "SCRIPT_BEHAVIOUR",
    "MAGIC_GRAPH",
    "MODEL_ANIMATION_VMAD",
    "EXTERNAL_UNRESOLVABLE_REF",
    "PERSISTENT_CROSS_PLUGIN",
    "REFERENCE_REMAP_REQUIRED",
    "CONFIG_INJECTION",
    "PLUGIN_NAME_REFERENCE",
    "EXTERNAL_THIRD_PARTY_MASTER",
    "PATH_KEYED_OVERRIDE",
    "INTERNAL_ONLY",
)

SCAN_GAP_NOTE = (
    "stage-B WANT set = " + ",".join(STAGE_B_WANT) + "; SCPT/QUES/VMAD/ACTI "
    "record types are NOT decoded, so their absence here is NOT proof of "
    "absence (has_script_records=NOT_SCANNED)")

OUT = os.path.join(C.REPORTS, "18_PLUGIN_MERGE_RISK.csv")

COLS = [
    "PLUGIN_ID", "plugin_file", "source_mod", "priority", "enabled", "is_esl",
    "n_records", "record_types", "n_simple", "n_script", "n_magic", "n_remap",
    "n_otft", "masters", "n_masters", "unusual_masters", "n_unusual_masters",
    "has_script_records", "script_evidence",
    "has_behavioural_records", "behavioural_evidence",
    "has_otft", "otft_detail",
    "needs_formid_remap", "n_ref_slots", "n_refs_self",
    "n_refs_to_in_scope_plugins", "n_refs_to_vanilla_external",
    "n_out_of_scope_refs", "out_of_scope_refs",
    "n_refs_unresolvable", "unresolvable_refs", "ref_resolution_routes",
    "n_config_files", "config_evidence", "n_config_formid_coupled",
    "n_config_plugin_name_coupled", "n_config_path_keyed",
    "reference_class", "reference_classes_all", "high_triggers",
    "risk_tier", "risk_reason", "recommended_action", "scan_coverage_note",
]

MAX_DETAIL = 6          # how many distinct "<tag>-><target>" pairs to spell out


# ----------------------------------------------------------------- loading --
def _load(name):
    path = os.path.join(C.DATA, name)
    if not os.path.isfile(path):
        raise SystemExit(f"missing frozen input: {path}")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------- ref extraction --
def subrecord_formids(tag, value):
    """Yield FormIDs (ints) carried by one decoded subrecord value.

    The frozen parser decodes by payload width, so the same logical reference
    arrives in four shapes:
      * plain int              4-byte payload, e.g. ARMO.RNAM, ARMA.RNAM
      * 8-char hex string      ARMO.KWDA, which the parser formatted
      * long hex string        MO*S TextureSet blobs; the FormID is the leading
                               uint32 of the embedded struct
      * {"u32":..,"u32b":..}   COBJ.CNTO, an 8-byte (FormID, count) pair
    """
    if tag in NON_FORMID_SUBRECORD_TAGS or tag not in REF_SUBRECORD_TAGS:
        return
    if isinstance(value, bool):
        return
    if isinstance(value, int):
        yield value
    elif isinstance(value, dict):
        u = value.get("u32")
        if isinstance(u, int) and not isinstance(u, bool):
            yield u
    elif isinstance(value, str):
        h = value.strip()
        if len(h) >= 8 and all(c in "0123456789abcdefABCDEF" for c in h[:8]):
            yield int(h[:8], 16)


class Resolver:
    """FormID -> owning plugin, from the frozen record + index data only."""

    def __init__(self, recs, pidx):
        self.own = defaultdict(set)
        self.masters = {}
        self.self_byte = {}
        for p in pidx:
            self.masters[p["PLUGIN_ID"]] = [m.lower() for m in
                                            (p.get("masters") or [])]
        seen = defaultdict(Counter)
        for r in recs:
            pid = r["PLUGIN_ID"]
            fi = r.get("formid_int")
            if isinstance(fi, int):
                self.own[pid].add(fi)
                seen[pid][(fi >> 24) & 0xFF] += 1
        for pid, cnt in seen.items():
            self.self_byte[pid] = cnt.most_common(1)[0][0] if cnt else None

    def resolve(self, pid, formid):
        """-> (target_key, route). target_key is a lowercase plugin file name,
        the literal "SELF", or None when the slot cannot be attributed."""
        if not formid:
            return None, "null"
        if formid in self.own.get(pid, ()):
            return "SELF", "self_record"
        ms = self.masters.get(pid, [])
        mid = (formid >> 24) & 0xFF
        if mid < len(ms):
            return ms[mid], f"master[{mid}]"
        if mid == 0xFF:
            return "SELF", "self_0xFF"
        if self.self_byte.get(pid) == mid:
            return "SELF", "self_master_byte_inferred"
        return None, f"unresolvable(master_byte=0x{mid:02X})"


# ----------------------------------------------------------- config layer --
# 14_config_refs.json detects configuration that couples to a plugin.  Those
# detections are not all equal and the file's own schema_notes say so: a weak
# content hit is "not proof of behaviour" (it fires on an xml comment, a URL, or
# mod metadata prose).  Three couplings that matter for a merge are kept apart:
#
#   formid-coupled   the config stores a raw FormID (KID injector lines, the
#                    Sound Refinery yaml).  Renumbering the plugin breaks it
#                    silently, so it must be edited in lockstep.
#   plugin-name      the config names the plugin FILE in a directive.  Renaming
#                    or splitting the file breaks it.
#   path-keyed       SKSE NiOverride tint data and PBRNifPatcher configs key on
#                    a NIF/TEX path -- verified by reading them.  They do NOT
#                    follow FormIDs and survive a merge untouched.  They are
#                    recorded as PATH_KEYED_OVERRIDE and are explicitly NOT
#                    counted as a remap risk.
def build_config_index(cfg):
    idx = defaultdict(lambda: {
        "n_files": 0, "kid": 0, "spid": 0, "skse": 0, "pgp": 0,
        "outfit_strong": 0, "outfit_weak": 0, "dist": 0,
        "formid_coupled": 0, "plugin_name_coupled": 0, "path_keyed": 0,
        "notes": [],
    })
    for f in cfg.get("files", []):
        dets = f.get("detections") or []
        pref = f.get("plugin_refs") or []
        fref = f.get("formid_refs") or []
        if not (dets or pref or fref):
            continue
        e = idx[f.get("source_mod", "")]
        e["n_files"] += 1
        kinds = set()
        for d in dets:
            k, s = d.get("kind"), d.get("strength")
            kinds.add(k)
            if k == "KID":
                e["kid"] += 1
            elif k == "SPID":
                e["spid"] += 1
            elif k == "SKSE":
                e["skse"] += 1
            elif k == "PGPATCHER":
                e["pgp"] += 1
            elif k == "OUTFIT":
                e["outfit_weak" if s == "weak" else "outfit_strong"] += 1
        if f.get("has_distribution_layer"):
            e["dist"] += 1
        for r in fref:
            if r.get("in_url_prose") == "yes":
                continue                      # 8-hex token inside a URL
            e["formid_coupled"] += 1
            e["notes"].append(f"FORMID_REF {r.get('value')} in {f.get('rel')}")
        for r in pref:
            if r.get("context_class") == "mod_metadata_prose":
                continue                      # a line of meta.ini prose
            e["plugin_name_coupled"] += 1
            e["notes"].append(f"PLUGIN_REF {r.get('value')} in {f.get('rel')}")
        if "SKSE" in kinds or "PGPATCHER" in kinds:
            e["path_keyed"] += 1
    # A KID injector file is `Keyword = <kw>|<cat>|<formids>+<plugin>.<ext>`,
    # so it names the plugin file even when the extractor missed the token.
    for _mod, e in idx.items():
        if e["kid"] and e["plugin_name_coupled"] == 0:
            e["plugin_name_coupled"] += 1
            e["notes"].append("KID injector lines name the plugin file")
    return idx


EMPTY_CFG = {"n_files": 0, "kid": 0, "spid": 0, "skse": 0, "pgp": 0,
             "outfit_strong": 0, "outfit_weak": 0, "dist": 0,
             "formid_coupled": 0, "plugin_name_coupled": 0, "path_keyed": 0,
             "notes": []}


def cfg_evidence(ce):
    bits = []
    for key, label in (("kid", "KID"), ("spid", "SPID"),
                       ("skse", "SKSE NiOverride tint (path-keyed)"),
                       ("pgp", "PBRNifPatcher (path-keyed)"),
                       ("dist", "distribution layer"),
                       ("outfit_strong", "OUTFIT strong"),
                       ("outfit_weak", "OUTFIT weak-only (not evidence)"),
                       ("formid_coupled", "hard-coded FormID"),
                       ("plugin_name_coupled", "plugin-name reference")):
        if ce.get(key):
            bits.append(f"{label} x{ce[key]}")
    if not bits:
        return "none"
    s = "; ".join(bits)
    if ce["notes"]:
        s += " | " + "; ".join(ce["notes"][:4])
    return s


# ------------------------------------------------------------- VMAD decode --
def vmad_names(raw):
    """Pull the contour / morph names out of an ARMO.VMAD blob.

    Layout, verified against this corpus (128-byte payload, version 5):
        u16 version | u16 unk | u16 n_blocks | then per block
        u16 subver | u16 size | <size bytes of name> | <block payload>
    The names are the animation channels -- a contour group and the morphs it
    drives.  They are what makes the block a behavioural dependency rather than
    opaque padding, so they are surfaced by name in risk_reason.
    """
    if not isinstance(raw, str) or len(raw) < 8:
        return []
    try:
        b = bytes.fromhex(raw)
    except ValueError:
        return []
    if len(b) < 6:
        return []
    n_blocks = int.from_bytes(b[4:6], "little")
    out, pos = [], 6
    for _ in range(min(n_blocks, 16)):
        if pos + 4 > len(b):
            break
        size = int.from_bytes(b[pos + 2:pos + 4], "little")
        pos += 4
        if size <= 0 or size > 64 or pos + size > len(b):
            break
        txt = b[pos:pos + size].decode("ascii", "ignore").strip("\x00 ")
        if txt:
            out.append(txt)
        pos += size
    return out


# ------------------------------------------------------- per-plugin evidence --
def analyse(p, recs, resolver, ce, scope_ids):
    pid = p["PLUGIN_ID"]
    bt = Counter(r["record_type"] for r in recs)

    n_script = sum(bt.get(t, 0) for t in SCRIPT_TYPES)
    n_magic = sum(bt.get(t, 0) for t in MAGIC_GRAPH_TYPES)
    n_otft = bt.get(OTFT_TYPE, 0)
    n_remap = sum(bt.get(t, 0) for t in REMAP_CONTAINER_TYPES) + n_otft
    n_simple = sum(bt.get(t, 0) for t in SIMPLE_TYPES)

    n_vmad = 0
    vnames = Counter()
    n_ctda = 0
    otft_inam = 0
    for r in recs:
        subs = r.get("subrecords") or {}
        for raw in subs.get("VMAD") or []:
            n_vmad += 1
            for nm in vmad_names(raw):
                vnames[nm] += 1
        if r["record_type"] == "COBJ":
            n_ctda += len(subs.get("CTDA") or [])
        if r["record_type"] == OTFT_TYPE:
            otft_inam += len(subs.get("INAM") or [])

    routes = Counter()
    n_slots = n_self = n_scope = n_vanilla = n_out = n_bad = 0
    out_detail, bad_detail = Counter(), Counter()
    cobj_cross = 0
    for r in recs:
        is_cobj = r["record_type"] == "COBJ"
        for tag, values in (r.get("subrecords") or {}).items():
            for v in values or []:
                for fid in subrecord_formids(tag, v):
                    n_slots += 1
                    tgt, route = resolver.resolve(pid, fid)
                    routes[route.split("(")[0].split("[")[0]] += 1
                    if route == "null":
                        continue
                    if tgt == "SELF":
                        n_self += 1
                        continue
                    if tgt is None:
                        n_bad += 1
                        bad_detail[f"{r['record_type']}.{tag} 0x{fid:08X}"] += 1
                        continue
                    if tgt in scope_ids:
                        n_scope += 1
                    elif tgt in GAME_FILES:
                        n_vanilla += 1
                    else:
                        n_out += 1
                        out_detail[f"{r['record_type']}.{tag} -> {tgt}"] += 1
                        if is_cobj:
                            cobj_cross += 1

    masters = resolver.masters.get(pid, [])
    unusual = [m for m in masters if m not in GAME_FILES]

    return dict(
        pid=pid, p=p, bt=bt, n_records=len(recs),
        n_script=n_script, n_magic=n_magic, n_otft=n_otft, n_remap=n_remap,
        n_simple=n_simple, n_vmad=n_vmad, vnames=vnames, n_ctda=n_ctda,
        otft_inam=otft_inam, routes=routes,
        n_slots=n_slots, n_self=n_self, n_scope=n_scope, n_vanilla=n_vanilla,
        n_out=n_out, n_bad=n_bad, out_detail=out_detail, bad_detail=bad_detail,
        cobj_cross=cobj_cross, masters=masters, unusual=unusual,
        ce=ce, cfg_evidence=cfg_evidence(ce),
    )


def _spell(detail, n_total):
    if not detail:
        return ""
    items = [f"{k} x{v}" for k, v in detail.most_common(MAX_DETAIL)]
    s = "; ".join(items)
    if len(detail) > MAX_DETAIL:
        s += f"; +{len(detail) - MAX_DETAIL} more target(s)"
    return f"total {n_total} slots: {s}"


# ------------------------------------------------------------- tiering ------
def classify(a):
    """-> (tier, primary_class, all_classes, high_triggers, reason, action)."""
    classes, highs, reasons = set(), [], []

    # ---- HIGH -------------------------------------------------------------
    if a["n_script"]:
        classes.add("SCRIPT_BEHAVIOUR")
        highs.append(f"script records x{a['n_script']}")
        reasons.append(f"{a['n_script']} script/VMAD/QUES record(s)")
    if a["n_magic"]:
        classes.add("MAGIC_GRAPH")
        highs.append(f"effect graph x{a['n_magic']}")
        reasons.append(f"{a['n_magic']} PERK/MGEF/SPEL/ENCH effect-graph "
                       "record(s)")
    if a["n_vmad"]:
        classes.add("MODEL_ANIMATION_VMAD")
        highs.append(f"ARMO.VMAD x{a['n_vmad']}")
        nm = ", ".join(k for k, _ in a["vnames"].most_common(3))
        reasons.append(
            f"ARMO.VMAD contour-morph animation block on {a['n_vmad']} ARMO "
            f"(channels: {nm or 'unreadable'}) -- must be copied byte-for-byte "
            "and is bound to the addon NIF")
    if a["n_bad"]:
        classes.add("EXTERNAL_UNRESOLVABLE_REF")
        highs.append(f"dangling ref x{a['n_bad']}")
        reasons.append(f"{a['n_bad']} FormID slot(s) whose master byte "
                       "matches neither this plugin's own records nor a "
                       "declared MAST entry, so they cannot be attributed or "
                       f"remapped: {_spell(a['bad_detail'], a['n_bad'])}")
    if a["cobj_cross"]:
        classes.add("PERSISTENT_CROSS_PLUGIN")
        highs.append(f"COBJ->outward x{a['cobj_cross']}")
        reasons.append(f"{a['cobj_cross']} save-persistent COBJ reference "
                       "slot(s) point outside the plugin and must be "
                       "rewritten, not just renumbered")

    # ---- MODERATE ---------------------------------------------------------
    if a["n_otft"]:
        classes.add("REFERENCE_REMAP_REQUIRED")
        reasons.append(
            f"OTFT x{a['n_otft']} carrying {a['otft_inam']} INAM FormID(s) "
            "-- an outfit reference list, needs a FormID remap (NOT a script)")
    if a["n_remap"] - a["n_otft"] > 0:
        classes.add("REFERENCE_REMAP_REQUIRED")
        reasons.append(f"{a['n_remap'] - a['n_otft']} LVLI/FLST/KYWD "
                       "FormID container record(s) need a remap")
    if a["n_scope"]:
        classes.add("REFERENCE_REMAP_REQUIRED")
        reasons.append(
            f"{a['n_scope']} reference slot(s) address other in-scope "
            "plugin(s) and must be remapped: "
            + _spell(Counter(dict(a["_scope_detail"])), a["n_scope"]))
    ce = a["ce"]
    if ce["kid"] or ce["spid"]:
        classes.add("CONFIG_INJECTION")
        reasons.append(f"{ce['kid'] + ce['spid']} KID/SPID injector "
                       "config file(s) keyed to this mod")
    if ce["formid_coupled"]:
        classes.add("CONFIG_INJECTION")
        reasons.append(f"{ce['formid_coupled']} config reference(s) store a "
                       "hard-coded FormID -- breaks silently on a renumber")
    if ce["plugin_name_coupled"]:
        classes.add("PLUGIN_NAME_REFERENCE")
        reasons.append(f"{ce['plugin_name_coupled']} config reference(s) name "
                       "this plugin by file name -- breaks on rename/split")
    if a["unusual"]:
        classes.add("EXTERNAL_THIRD_PARTY_MASTER")
        reasons.append(
            f"declares {len(a['unusual'])} third-party master(s) "
            f"({', '.join(a['unusual'][:4])}); " + (_spell(a["out_detail"],
                                                            a["n_out"])
                                                    if a["n_out"] else
                                                    "no outward slot seen"))
    if a["n_out"] and not a["unusual"]:
        classes.add("EXTERNAL_THIRD_PARTY_MASTER")
        reasons.append(f"{a['n_out']} reference slot(s) target a plugin "
                       "outside the audit scope: "
                       + _spell(a["out_detail"], a["n_out"]))
    if ce["path_keyed"]:
        classes.add("PATH_KEYED_OVERRIDE")
        reasons.append(f"{ce['path_keyed']} SKSE/PBRNifPatcher config(s) key "
                       "on NIF/TEX paths, not FormIDs -- unaffected by a "
                       "renumber (recorded, not a remap risk)")
    if a["n_ctda"]:
        reasons.append(f"{a['n_ctda']} COBJ.CTDA condition(s) evaluated at "
                       "load; they gate item availability after a merge")

    if not classes:
        classes.add("INTERNAL_ONLY")

    if highs:
        tier = "HIGH"
    elif classes - {"PATH_KEYED_OVERRIDE", "INTERNAL_ONLY"}:
        tier = "MODERATE"
    else:
        tier = "LOW_EASY"

    if tier == "HIGH":
        action = ("manual review: behaviour must be translated, not remapped "
                  "-- re-verify every listed high trigger after the merge")
    elif tier == "MODERATE":
        action = ("remap FormIDs and re-point every listed reference in "
                  "lockstep, including the external configs")
    else:
        action = ("straight merge: only ARMO/ARMA/TXST/COBJ, no outward "
                  "reference, remap FormIDs and nothing else")

    primary = next((c for c in REFCLASS_ORDER if c in classes), "INTERNAL_ONLY")
    reason = "; ".join(reasons) or (
        "only ARMO/ARMA/TXST/COBJ records; every FormID reference resolves to "
        "this plugin's own records or to official game files")
    return tier, primary, ";".join(c for c in REFCLASS_ORDER if c in classes), \
        "; ".join(highs), reason, action


# ------------------------------------------------------------------- main ---
def main() -> int:
    C.ensure_dirs()
    recs = _load("02_plugin_records.json")
    pidx = _load("02_plugin_index.json")
    cfg = _load("14_config_refs.json")
    C.log(f"stage-B input: {len(pidx)} plugins, {len(recs)} records")
    C.log("  record types: " + ", ".join(
        f"{k}={v}" for k, v in
        Counter(r["record_type"] for r in recs).most_common()))

    scope_ids = {p["PLUGIN_ID"] for p in pidx}
    by_plugin = defaultdict(list)
    for r in recs:
        by_plugin[r["PLUGIN_ID"]].append(r)
    resolver = Resolver(recs, pidx)
    cfg_idx = build_config_index(cfg)
    C.log(f"config layer: {len(cfg_idx)} source_mod(s) carry references")

    rows = []
    routes_all = Counter()
    for p in sorted(pidx, key=lambda x: (-(x.get("priority") or 0), x["PLUGIN_ID"])):
        pid = p["PLUGIN_ID"]
        ce = cfg_idx.get(p.get("source_mod", ""), EMPTY_CFG)
        a = analyse(p, by_plugin.get(pid, []), resolver, ce, scope_ids)
        # keep the per-target breakdown for in-scope plugins for the reason text
        a["_scope_detail"] = [(k, v) for k, v in a["out_detail"].items()]
        routes_all.update(a["routes"])
        tier, primary, allcls, highs, reason, action = classify(a)
        hdr = p.get("header") or {}
        n_otft = a["n_otft"]
        rows.append({
            "PLUGIN_ID": pid,
            "plugin_file": p.get("plugin_file", ""),
            "source_mod": p.get("source_mod", ""),
            "priority": p.get("priority", ""),
            "enabled": p.get("enabled", ""),
            "is_esl": "yes" if hdr.get("is_esl") else "no",
            "n_records": a["n_records"],
            "record_types": "; ".join(f"{k}={v}"
                                      for k, v in a["bt"].most_common()),
            "n_simple": a["n_simple"],
            "n_script": a["n_script"],
            "n_magic": a["n_magic"],
            "n_remap": a["n_remap"],
            "n_otft": n_otft,
            "masters": "; ".join(a["masters"]),
            "n_masters": len(a["masters"]),
            "unusual_masters": "; ".join(a["unusual"]),
            "n_unusual_masters": len(a["unusual"]),
            "has_script_records": "yes" if a["n_script"] else "NOT_SCANNED",
            "script_evidence": (
                f"SCPT/QUES/VMAD/ACTI records: {a['n_script']} decoded, 0 "
                f"expected (see scan_coverage_note); ARMO.VMAD subrecords: "
                f"{a['n_vmad']}"),
            "has_behavioural_records": "yes" if (
                a["n_magic"] or a["n_vmad"] or a["n_ctda"]) else "no",
            "behavioural_evidence": (
                f"PERK/MGEF/SPEL/ENCH={a['n_magic']}; ARMO.VMAD={a['n_vmad']}; "
                f"COBJ.CTDA={a['n_ctda']}"),
            "has_otft": "yes" if n_otft else "no",
            "otft_detail": (
                f"{n_otft} OTFT, {a['otft_inam']} INAM FormID(s); "
                f"edids=" + ",".join(
                    (r["subrecords"].get("EDID") or [""])[0]
                    for r in by_plugin.get(pid, [])
                    if r["record_type"] == OTFT_TYPE)) if n_otft else "",
            "needs_formid_remap": "yes" if (
                a["n_otft"] or a["n_scope"] or a["n_out"] or
                a["n_remap"] - a["n_otft"] or a["ce"]["formid_coupled"]) else "no",
            "n_ref_slots": a["n_slots"],
            "n_refs_self": a["n_self"],
            "n_refs_to_in_scope_plugins": a["n_scope"],
            "n_refs_to_vanilla_external": a["n_vanilla"],
            "n_out_of_scope_refs": a["n_out"],
            "out_of_scope_refs": _spell(a["out_detail"], a["n_out"]),
            "n_refs_unresolvable": a["n_bad"],
            "unresolvable_refs": _spell(a["bad_detail"], a["n_bad"]),
            "ref_resolution_routes": "; ".join(
                f"{k}={v}" for k, v in a["routes"].most_common()),
            "n_config_files": a["ce"]["n_files"],
            "config_evidence": a["cfg_evidence"],
            "n_config_formid_coupled": a["ce"]["formid_coupled"],
            "n_config_plugin_name_coupled": a["ce"]["plugin_name_coupled"],
            "n_config_path_keyed": a["ce"]["path_keyed"],
            "reference_class": primary,
            "reference_classes_all": allcls,
            "high_triggers": highs,
            "risk_tier": tier,
            "risk_reason": reason,
            "recommended_action": action,
            "scan_coverage_note": SCAN_GAP_NOTE,
        })

    n = C.write_csv(OUT, COLS, rows)
    C.log(f"18_PLUGIN_MERGE_RISK.csv = {n} rows, {len(COLS)} columns")
    C.log("  risk_tier       : " + ", ".join(
        f"{k}={v}" for k, v in
        Counter(r["risk_tier"] for r in rows).most_common()))
    C.log("  reference_class : " + ", ".join(
        f"{k}={v}" for k, v in
        Counter(r["reference_class"] for r in rows).most_common()))
    C.log("  all classes     : " + ", ".join(
        f"{k}={v}" for k, v in
        Counter(c for r in rows for c in r["reference_classes_all"].split(";"))
        .most_common()))
    C.log("  ref routes      : " + ", ".join(
        f"{k}={v}" for k, v in routes_all.most_common()))
    C.log(f"  OTFT plugins    : {sum(1 for r in rows if r['n_otft'])}; "
          f"ARMO.VMAD plugins: "
          f"{sum(1 for r in rows if 'VMAD=' in r['behavioural_evidence'])}")
    C.log("  REMOVED criterion check -- the 'shared raw FormID' signal is not "
          "computed anywhere in this module; 'FormID overlap' columns absent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
