# -*- coding: utf-8 -*-
r"""P02A plugin / ARMA / TXST / physics migration PLANNER  (STRICT READ-ONLY).

Deliverables (all under reports/P02A/):
  1. P02A_PLUGIN_RECORD_MIGRATION.csv  - every ARMO/ARMA/TXST/COBJ record of the 11
     frozen source plugins -> planned ZLJ_CL_<OUTFIT>_<PART> EDID in ZLJ_CombatLatex.esp
  2. P02A_ARMA_MODEL_REWRITE.csv       - every ARMO.MOD2/MOD4 + ARMA.MOD2..MOD5 model
     reference -> planned meshes\ZLJ\CombatLatex\<OUTFIT_ID>\... target
  3. P02A_PLUGIN_TEXTURE_REWRITE.csv   - every DDS path written by a plugin record
     (TXST.TX00..TX07 hex-decoded) with VFS provider / cross-outfit classification
  4. P02A_PHYSICS_MIGRATION.csv        - HDT-SMP XML + Havok .tri inventory with
     mesh binding, bone dependency and future path plan

Design-stage contract (P02A):
  * Nothing is copied, moved, renamed, built or converted. These CSVs are a
    migration LEDGER only: COPY + REPOINT intent.
  * No new FormID is generated. new_formid_status is always NOT_GENERATED_P02A.
  * No shared material/texture directory is created. Any identical-by-SHA256 asset
    observed across providers is recorded as a proposal, status text
    PROPOSAL_SHARED_NOT_APPROVED (belongs to P05 MATERIAL STANDARDIZATION).
  * No fuzzy matching. Only EXACT_OUTPUT_PATH relations, frozen P00 strong
    relations (P00.parts / P00.plugin_records / VFS winner) and exact-name
    lookups are accepted. Anything else is emitted as UNKNOWN.

READ-ONLY note about MO2 access:
  P00 froze the file index but did not capture the HDT-SMPContainer string that
  lives inside NIF binaries. To bind a physics XML to its mesh *exactly* (and not
  by filename guessing) this script performs a targeted READ-ONLY byte read of
  the individual .nif/.xml files already listed in the frozen P00 index. It never
  writes, moves or enumerates directories inside MO2.

Re-run:  python tools/P02A/p02a_plugin.py
"""
from __future__ import annotations

import binascii
import collections
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

import p02a_common as C  # noqa: E402

P = C.P00.get()
OUT_DIR = C.OUT
MODS_DIR = (P.config_refs.get("scope") or {}).get("mods_dir", "E:\\SkyrimAE\\mo2\\mods")

TARGET_PLUGIN = C.TARGET_PLUGIN
MESH_ROOT = C.MESH_ROOT          # meshes\ZLJ\CombatLatex\
TEX_ROOT = C.TEX_ROOT            # textures\ZLJ\CombatLatex\
NEW_FORMID_STATUS = "NOT_GENERATED_P02A"
FORMKEY_MASTER = "000000"        # plugins.txt is not rebuilt until P03

# ---------------------------------------------------------------------------
# frozen registries derived from P00 (no MO2 re-scan)
# ---------------------------------------------------------------------------
OWN_PLUGIN = {oid: C.OUTFITS[oid]["plugin"] for oid in C.OUTFIT_IDS}
PLUGIN_TO_OWNER = {v: k for k, v in OWN_PLUGIN.items()}

MOD_TO_OWNER = {}
for _oid in C.OUTFIT_IDS:
    for _m in P.mods_of_outfit(_oid):
        MOD_TO_OWNER[_m] = _oid

# historical cross-outfit / cross-mod vocabularies called out by the P02A brief
HISTORIC_PATTERNS = {
    "LATEX_KITTY": re.compile(r"(?i)(kitty)"),
    "SOURYO": re.compile(r"(?i)(souryo|sse_vrc_syo|\\\\syo\\\\)"),
    "ST": re.compile(r"(?i)(^|[\\\\/])st([\\\\/])"),
    "BUNNY": re.compile(r"(?i)bunny"),
    "ANGELI": re.compile(r"(?i)angeli"),
    "DEVIOS_DEVICES": re.compile(r"(?i)devious\\\\devices"),
    "NYES": re.compile(r"(?i)(nye)"),
    "GHOST": re.compile(r"(?i)(^|[\\\\/])ghost([\\\\/])"),
    "AOKILI": re.compile(r"(?i)(^|[\\\\/])aokili([\\\\/])"),
    "PREDATOR": re.compile(r"(?i)(^|[\\\\/])predator([\\\\/])"),
}


def hit_patterns(text):
    return [n for n, rx in HISTORIC_PATTERNS.items() if rx.search(text or "")]


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def bs(s):
    return str(s or "").replace("/", "\\").strip().strip('"')


def v_mesh(model_ref):
    s = bs(model_ref)
    if not s:
        return ""
    return s if s.lower().startswith("meshes\\") else "meshes\\" + s


def v_tex(dds_ref):
    s = bs(dds_ref)
    if not s:
        return ""
    low = s.lower()
    if low.startswith("textures\\") or low.startswith("meshes\\"):
        return s
    return "textures\\" + s


def provider_of(vp):
    if not vp:
        return "", "", ""
    lst = P.providers(vp)
    if not lst:
        return "", "", ""
    return lst[0]["mod"], lst[0].get("sha256", ""), "; ".join(f["mod"] for f in lst[1:])


def mod_owner(mod):
    return MOD_TO_OWNER.get(mod, "")


def abspath_of(f):
    return os.path.join(MODS_DIR, f["mod"], f["rel"].replace("/", os.sep))


# frozen ARMA/ARMO slot vocabulary (recorded as-is; see CSV notes column)
ARMA_SLOT = {"MOD2": "WORLD_DROP", "MOD3": "WORN_ADDON",
             "MOD4": "WORLD_DROP_ALT", "MOD5": "FIRSTPERSON"}
ARMO_SLOT = {"MOD2": "WORLD_DROP", "MOD4": "FIRSTPERSON"}
BBP_VARIANT_RE = re.compile(r"(?i)(_1|_0|_go)\.nif$")


def bbp_variant(model_ref):
    m = BBP_VARIANT_RE.search(str(model_ref or ""))
    if not m:
        return "UNSPECIFIED"
    return {"_1": "PHYSICS_1", "_0": "PHYSICS_0", "_go": "STATIC_GO"}[m.group(1).lower()]


def model_role(model_ref):
    r"""Evidence-driven model_role.

    GROUND   : 'gnd' path segment or basename token
    WORLD    : vanilla Skyrim.esm drop mesh (armor\studded\...) - P00.parts note:
               "ARMO.MOD2..MOD5 are world/inventory drop models ... NOT the worn mesh"
    WEARABLE : mod-owned mesh reachable in the frozen VFS index
    UNKNOWN  : mod-owned mesh the frozen VFS index cannot resolve
    """
    s = bs(model_ref).lower()
    if not s:
        return "UNKNOWN", "EMPTY_MODEL_REF"
    if "\\gnd\\" in s or re.search(r"(?:^|[\\_\-])gnd(?:[\\_\-\.]|$)", s):
        return "GROUND", "GND_PATH_TOKEN"
    if s.startswith("armor\\") or s.startswith("meshes\\armor\\"):
        return "WORLD", "VANILLA_SKYRIMESM_DROP_SLOT"
    if not P.exists(v_mesh(s)):
        return "UNKNOWN", "NOT_IN_FROZEN_VFS_INDEX"
    return "WEARABLE", "MOD_OWNED_REACHABLE"


def sanitise_edid_token(tok):
    t = re.sub(r"[^0-9A-Za-z]+", "_", str(tok or "")).strip("_")
    return t.upper() or "UNKNOWN"


BITSLOT_RE = re.compile(r"(?i)^bit\d+$")
# colour / variant / numbering tokens that describe a colourway, not a body part
VARIANT_STOP = {
    "white", "wet", "red", "blue", "pink", "yellow", "purple", "green", "black",
    "orange", "brown", "grey", "gray", "silver", "gold", "plain", "dirty", "blood",
    "aa", "alt", "alt2", "dup", "duplicate", "copy", "bak", "old", "new", "go",
    "main", "v1", "v2", "0", "1", "2", "3", "01", "02", "03", "04",
}
OUTFIT_STEM = {}   # outfit_id -> set of EDID tokens shared by most of its ARMO EDIDs


def _stem_tokens():
    for oid in C.OUTFIT_IDS:
        pf = OWN_PLUGIN[oid]
        eds = [((r.get("subrecords") or {}).get("EDID") or [""])[0]
               for r in P.records_of_plugin.get(pf, []) if r["record_type"] == "ARMO"]
        eds = [e for e in eds if e]
        if not eds:
            OUTFIT_STEM[oid] = set()
            continue
        counts = collections.Counter()
        for e in eds:
            counts.update(set(t.lower() for t in re.split(r"[_\s]", e) if t))
        thresh = max(2, int(round(0.6 * len(eds))))
        OUTFIT_STEM[oid] = {t for t, c in counts.items() if c >= thresh}


def part_label(oid, edid, part):
    """Deterministic <PART> token for the new EDID namespace."""
    slot = ""
    if part and part.get("slot_names"):
        slot = part["slot_names"].split(";")[0].strip()
    if slot and not BITSLOT_RE.match(slot):
        return sanitise_edid_token(slot), "P00_PARTS_ARMA_BOD2_SLOT"
    # unnamed Skyrim bit slots have no CK name; fall back to the author's own EDID
    # wording with the outfit stem and colourway/variant tokens removed.
    stem = OUTFIT_STEM.get(oid, set())
    for t in re.split(r"[_\s]", str(edid or "")):
        tl = t.lower()
        if t and tl not in VARIANT_STOP and tl not in stem:
            return sanitise_edid_token(t), "P00_SLOT_%s_UNNAMED_EDID_TOKEN" % (
                slot.upper() if slot else "NOSLOT")
    if slot:
        return sanitise_edid_token(slot), "P00_PARTS_ARMA_BOD2_SLOT_BITSLOT"
    return "PART", "UNKNOWN"


# ---------------------------------------------------------------------------
# frozen indices
# ---------------------------------------------------------------------------
PARTS = {}
ARMA_TO_PART = {}
for _pt in P.parts:
    if _pt["plugin_file"] not in PLUGIN_TO_OWNER:
        continue
    PARTS[(_pt["plugin_file"], _pt["ARMO_formid"].upper())] = _pt
    for _tok in str(_pt.get("ARMA_formids") or "").split(";"):
        _tok = _tok.strip()
        if ":" not in _tok:
            continue
        _pl, _fid = _tok.rsplit(":", 1)
        if _pl.lower() == _pt["plugin_file"].lower():
            ARMA_TO_PART.setdefault((_pt["plugin_file"], _fid.upper()), _pt)

REC_BY_ID = {r["formid"].upper(): r for r in P.plugin_records}

_stem_tokens()

EDID_INDEX = collections.defaultdict(list)
for _r in P.plugin_records:
    _e = (_r.get("subrecords") or {}).get("EDID") or [""]
    if _e and _e[0]:
        EDID_INDEX[(_r["record_type"], _e[0].strip().lower())].append(_r)


# ---------------------------------------------------------------------------
# read-only NIF scan -> exact HDT-SMPContainer XML binding
# ---------------------------------------------------------------------------
SMP_STR_RE = re.compile(rb"(?:Meshes|Data)\\+[A-Za-z0-9_\.\\\- ()]{1,200}?\.xml", re.IGNORECASE)
_SMP_CACHE = {}


def smp_xml_of_nif(vp):
    """EXACT SMPContainer path stored inside the NIF, or ''. Read-only byte read."""
    key = C.norm(vp)
    if key in _SMP_CACHE:
        return _SMP_CACHE[key]
    out = ""
    f = P.winner(vp)
    if f and f.get("ext") == ".nif":
        try:
            with open(abspath_of(f), "rb") as fh:
                blob = fh.read()
            m = SMP_STR_RE.search(blob)
            if m:
                raw = m.group(0).decode("utf-8", "ignore").replace("\\", "\\")
                raw = re.sub(r"\\+", r"\\", raw).replace("/", "\\")
                low = raw.lower()
                if low.startswith("data\\meshes\\"):
                    raw = raw[5:]
                if low.startswith("meshes\\"):
                    out = raw
        except OSError:
            out = ""
    _SMP_CACHE[key] = out
    return out


# ===========================================================================
# 1. P02A_PLUGIN_RECORD_MIGRATION.csv
# ===========================================================================
REC_HEADER = [
    "OUTFIT_ID", "source_plugin", "source_mod", "mod_priority", "formid", "formkey",
    "edid", "record_type", "full_name", "part_category", "slot_names", "target_plugin",
    "new_edid", "new_edid_status", "new_formid_status", "relationship", "formid_status",
    "master_index", "edid_collision", "notes",
]


def build_record_rows():
    rows = []
    used = collections.defaultdict(set)
    for oid in C.OUTFIT_IDS:
        pf = OWN_PLUGIN[oid]
        short = C.short_name(oid)
        recs = sorted(P.records_of_plugin.get(pf, []),
                      key=lambda r: (r["record_type"], r["formid"]))
        noncanon = "NON_CANONICAL_BODY" in C.OUTFITS[oid].get("support", {})
        for r in recs:
            fid = r["formid"].upper()
            sub = r.get("subrecords") or {}
            edid = (sub.get("EDID") or [""])[0]
            rt = r["record_type"]
            part = PARTS.get((pf, fid)) if rt == "ARMO" else None

            if rt in ("ARMO", "ARMA"):
                if rt == "ARMO":
                    plabel, psrc = part_label(oid, edid, part)
                    rel = "ARMOR_ITEM"
                else:
                    op = ARMA_TO_PART.get((pf, fid))
                    if op:
                        plabel, psrc = part_label(oid, op["EDID"], op)
                        rel = "ARMOR_ADDON_OF:" + op["EDID"]
                    else:
                        plabel, psrc = part_label(edid, None)
                        rel = "ARMOR_ADDON_UNLINKED"
                rel += ";CARRIES_WEARABLE_MODEL"
            elif rt == "TXST":
                plabel, psrc, rel = "TX", "RECORD_TYPE_TXST", "TEXTURE_SET_STANDALONE"
            elif rt == "COBJ":
                # COBJ.CNAM is the alias override: resolve it inside the source plugin
                cn = sub.get("CNAM", [None])[0]
                tgt = REC_BY_ID.get("%08X" % (cn & 0xFFFFFFFF)) if isinstance(cn, int) else None
                if tgt is not None and tgt["record_type"] == "ARMO":
                    op = PARTS.get((tgt["plugin_file"], tgt["formid"].upper()))
                    plabel, psrc = part_label(oid, tgt["subrecords"].get("EDID", [""])[0], op)
                    rel = "ARMOR_OBJECT_ALIAS_OVERRIDE->" + tgt["subrecords"]["EDID"][0]
                    bn = sub.get("BNAM", [None])[0]
                    if isinstance(bn, int) and not (0 <= bn <= 0x800):
                        rel += ";BNAM_FORMID_OUT_OF_ESP_RANGE=0x%06X_UNRESOLVED" % bn
                else:
                    plabel, psrc, rel = "COBJ", "RECORD_TYPE_COBJ", \
                        "ARMOR_OBJECT_ALIAS_OVERRIDE_TARGET_UNRESOLVED"
            else:
                plabel, psrc = sanitise_edid_token(rt), "RECORD_TYPE_" + rt
                rel = "RECORD_TYPE_" + rt

            base = ("ZLJ_CL_%s_%s_AA" % (short, plabel)) if rt == "ARMA" \
                else ("ZLJ_CL_%s_%s" % (short, plabel))
            new_edid, n = base, 2
            while new_edid.lower() in used[oid]:
                new_edid = "%s_%d" % (base, n)
                n += 1
            used[oid].add(new_edid.lower())

            coll = EDID_INDEX.get((rt, edid.strip().lower()), [])
            collide = ""
            if len(coll) > 1:
                others = sorted({c["plugin_file"] for c in coll if c["plugin_file"] != pf})
                if others:
                    collide = "EDID_SHARED_WITH:" + ";".join(others)

            notes = ["PART_TOKEN_SOURCE=" + psrc]
            if part:
                notes.append("P00_PART_CATEGORY=" + str(part.get("part_category", "")))
                notes.append("P00_BODY_CANDIDATE=" + str(part.get("body_candidate", "")))
                notes.append("P00_BODYSLIDE_MATCH=" + str(part.get("bodyslide_match_method", "")))
                notes.append("P00_PHYSICS=" + str(part.get("physics", "")))
                if part.get("game_nif_resolution_status") == "PENDING_BODYSLIDE":
                    notes.append("WEARABLE_MESH_PENDING_BODYSLIDE_BUILD")
            if collide:
                notes.append("COLLISION_REVIEW_REQUIRED")
            if noncanon:
                notes.append("NON_CANONICAL_BODY=BHUNP_3BBB (labelled only, P02A deletes nothing)")

            rows.append([
                oid, pf, r.get("source_mod", ""), r.get("priority", ""),
                fid, "0x%s:%s" % (FORMKEY_MASTER, fid),
                edid, rt, (sub.get("FULL") or [""])[0],
                (part or {}).get("part_category", ""), (part or {}).get("slot_names", ""),
                TARGET_PLUGIN, new_edid, "PLANNED_NOT_WRITTEN", NEW_FORMID_STATUS,
                rel, NEW_FORMID_STATUS, FORMKEY_MASTER, collide, " | ".join(notes),
            ])
    return rows


# ===========================================================================
# 2. P02A_ARMA_MODEL_REWRITE.csv
# ===========================================================================
ARMA_HEADER = [
    "OUTFIT_ID", "source_plugin", "formid", "edid", "record_type", "subrecord",
    "model_role", "old_path", "new_path", "mesh_role", "target_outfit_match",
    "status", "old_vpath", "new_vpath", "file_exists", "winning_provider",
    "provider_priority", "shadowed_providers", "sha256", "notes",
]


def build_arma_rows():
    rows = []
    for oid in C.OUTFIT_IDS:
        pf = OWN_PLUGIN[oid]
        noncanon = "NON_CANONICAL_BODY" in C.OUTFITS[oid].get("support", {})
        recs = sorted(P.records_of_plugin.get(pf, []),
                      key=lambda x: (x["record_type"], x["formid"]))
        for r in recs:
            if r["record_type"] not in ("ARMO", "ARMA"):
                continue
            sub = r["subrecords"]
            fid = r["formid"].upper()
            edid = (sub.get("EDID") or [""])[0]
            slots = ARMA_SLOT if r["record_type"] == "ARMA" else ARMO_SLOT
            for sk in ("MOD2", "MOD3", "MOD4", "MOD5"):
                for mref in sub.get(sk) or []:
                    if not str(mref).strip():
                        continue
                    role, why = model_role(mref)
                    vp = v_mesh(mref)
                    mod, sha, shadow = provider_of(vp)
                    exists = P.exists(vp)
                    om = mod_owner(mod)
                    if om == oid:
                        match = "SELF_OWN_MOD"
                    elif om:
                        match = "CROSS_OUTFIT:" + om
                    elif mod:
                        match = "EXTERNAL_MOD"
                    else:
                        match = "NO_PROVIDER"

                    base = os.path.basename(bs(mref))
                    if not base:
                        continue
                    sub_dir = {"GROUND": "\\gnd\\", "WORLD": "\\world\\"}.get(role, "\\")
                    np_vp = MESH_ROOT + oid + sub_dir + base

                    notes = ["ROLE_EVIDENCE=" + why, "SLOT=" + slots.get(sk, "UNKNOWN")]
                    pat = hit_patterns(str(mref))
                    if pat:
                        notes.append("HISTORIC_NAME_PATTERN=" + "+".join(pat))
                    if om and om != oid:
                        notes.append("CROSS_OUTFIT_DEPENDENCY_MUST_BE_VENDORED")
                    if not exists:
                        notes.append("MISSING_IN_FROZEN_VFS_INDEX")

                    if noncanon:
                        status = "NON_CANONICAL_SOURCE"
                    elif role == "UNKNOWN":
                        status = "UNRESOLVED"
                    elif role == "WORLD":
                        status = "REPOINT"
                        np_vp = vp
                        notes.append("WORLD_DROP_SLOT_STAYS_VANILLA; recorded separately from "
                                     "the wearable; no copy into the ZLJ namespace")
                        notes.append("NOT_IN_P00_FILE_INDEX (P00 indexes MO2 mods only; "
                                     "Skyrim.esm existence UNVERIFIED in P02A)")
                    elif exists:
                        status = "COPY_AND_REPOINT"
                    else:
                        status = "UNRESOLVED"
                    if noncanon:
                        notes.append("NON_CANONICAL_BODY=BHUNP_3BBB")

                    rows.append([
                        oid, pf, fid, edid, r["record_type"], sk, role,
                        str(mref), np_vp, "%s_%s" % (sk, bbp_variant(mref)),
                        match, status, vp, np_vp, "yes" if exists else "no",
                        mod, P.priority.get(mod, ""), shadow, sha, " | ".join(notes),
                    ])
    return rows


# ===========================================================================
# 3. P02A_PLUGIN_TEXTURE_REWRITE.csv
# ===========================================================================
TEX_HEADER = [
    "OUTFIT_ID", "source_plugin", "formid", "edid", "record_type", "subrecord",
    "old_dds", "new_dds", "source_provider", "owning_outfit_of_source", "dependency_type",
    "status", "file_exists", "sha256", "shadowed_providers", "historic_pattern",
    "notes",
]

# Skyrim.esm content roots. P00 indexes MO2 mods only, so base-game files never
# resolve; only roots that are unambiguously vanilla are labelled VANILLA.
VANILLA_TEX_PREFIXES = ("textures\\actors\\", "textures\\interface\\", "textures\\language\\")


def hex_to_ascii(h):
    try:
        raw = binascii.unhexlify(str(h).strip())
    except (binascii.Error, ValueError):
        return None
    return raw.split(b"\x00")[0].decode("utf-8", "replace")


def build_texture_rows():
    rows = []
    # frozen strong relation: which of the outfit's own NIFs use each DDS
    dds_to_nifs = collections.defaultdict(set)
    for _pt in P.parts:
        if _pt["plugin_file"] not in PLUGIN_TO_OWNER:
            continue
        for _nsh in _pt.get("nif_shapes") or []:
            _nid = C.norm(_nsh.get("nif_id", ""))
            for _sh in _nsh.get("shapes") or []:
                for _slot, _dds in (_sh.get("textures") or {}).items():
                    if _dds and str(_dds).strip():
                        dds_to_nifs[C.norm(_dds)].add(_nid)

    for oid in C.OUTFIT_IDS:
        pf = OWN_PLUGIN[oid]
        noncanon = "NON_CANONICAL_BODY" in C.OUTFITS[oid].get("support", {})
        for r in sorted(P.records_of_plugin.get(pf, []), key=lambda x: x["formid"]):
            if r["record_type"] != "TXST":
                continue
            fid = r["formid"].upper()
            sub = r["subrecords"]
            edid = (sub.get("EDID") or [""])[0]
            for sk in sorted(k for k in sub if k.startswith("TX")):
                for hv in sub.get(sk) or []:
                    dds = hex_to_ascii(hv)
                    if dds is None:
                        rows.append([oid, pf, fid, edid, "TXST", sk, "<<UNDECODABLE>>",
                                     "", "", "", "UNRESOLVED", "no", "", "", "",
                                     "HEX_DECODE_FAILED - no guessing allowed"])
                        continue
                    vp = v_tex(dds)
                    mod, sha, shadow = provider_of(vp)
                    exists = P.exists(vp)
                    om = mod_owner(mod)
                    if om == oid:
                        dep = "SELF"
                    elif om:
                        dep = "CROSS_OUTFIT"
                    elif mod:
                        dep = "EXTERNAL_MOD"
                    elif vp.lower().startswith(VANILLA_TEX_PREFIXES):
                        dep = "VANILLA"
                    else:
                        dep = "UNRESOLVED"
                    pat = hit_patterns(dds)
                    users = sorted(dds_to_nifs.get(C.norm(vp), []))

                    notes = ["PLANNED_TARGET=" + TEX_ROOT + oid + "\\" +
                             os.path.basename(bs(dds))]
                    if users:
                        notes.append("BOUND_MESH=" + ";".join(users))
                    if pat:
                        notes.append("HISTORIC_CROSS_OUTFIT_NAME_PATTERN=" + "+".join(pat))
                    if noncanon:
                        notes.append("NON_CANONICAL_BODY=BHUNP_3BBB")
                    if exists and sha:
                        same = [f["mod"] for f in P.providers(vp)[1:]
                                if f.get("sha256") == sha]
                        if same:
                            notes.append("IDENTICAL_SHA_OTHER_PROVIDERS=" + ";".join(same) +
                                         " PROPOSAL_SHARED_NOT_APPROVED; P02A keeps an independent copy")

                    if not exists:
                        notes.append("NOT_IN_P00_FILE_INDEX (P00 indexes MO2 mods only; "
                                     "Skyrim.esm / CC / DLC existence is UNVERIFIED in P02A)")
                        status = "UNRESOLVED"
                    elif noncanon:
                        status = "NON_CANONICAL_SOURCE"
                    elif dep == "SELF":
                        status = "REPOINT"
                    else:
                        status = "COPY_AND_REPOINT"

                    rows.append([
                        oid, pf, fid, edid, "TXST", sk, dds,
                        TEX_ROOT + oid + "\\" + os.path.basename(bs(dds)),
                        mod, om, dep, status, "yes" if exists else "no", sha, shadow,
                        "+".join(pat), " | ".join(notes),
                    ])
    return rows


# ===========================================================================
# 4. P02A_PHYSICS_MIGRATION.csv
# ===========================================================================
PHYS_HEADER = [
    "OUTFIT_ID", "physics_file", "config_type", "current_provider", "provider_priority",
    "shadowed_providers", "sha256", "mesh_references", "bone_dependencies",
    "config_paths", "old_path_refs", "new_path_refs", "rewrite_required",
    "bone_check_status", "missing_bones", "status", "notes",
]


def xml_bones(path):
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError, ValueError):
        return None, None
    if root.tag != "system":
        return None, None
    bones = [e.get("name") for e in root.iter("bone") if e.get("name")]
    adds = [e.get("name") for e in root.iter("addBone") if e.get("name")]
    return bones, adds


def nif_bones(vp):
    n = P.nif(vp)
    if not n:
        return set(), True
    shapes = n.get("shapes", []) or []
    bones = set()
    for sh in shapes:
        bones.update(sh.get("bones") or [])
    # the bone list is incomplete when ANY shape was truncated by P00
    trunc = bool(shapes) and all(sh.get("n_bones_truncated") for sh in shapes)
    return bones, trunc


def build_physics_rows():
    rows = []
    for oid in C.OUTFIT_IDS:
        pf = OWN_PLUGIN[oid]
        shipped = set()
        for m in P.mods_of_outfit(oid):
            for f in P.files_of_mod[m]:
                if f["ext"] in (".xml", ".tri") and f["vpath"].lower().startswith("meshes/"):
                    shipped.add(bs(f["vpath"]))

        own_nifs = set()
        for pt in P.parts:
            if pt["plugin_file"] != pf:
                continue
            for tok in str(pt.get("nif_ids") or "").split(";"):
                tok = tok.strip()
                if tok.lower().startswith("meshes\\"):
                    own_nifs.add(tok)

        bindings = []
        for vp in sorted(own_nifs):
            x = smp_xml_of_nif(vp)
            if x:
                bindings.append((vp, x))

        # merge shipped files and NIF-bound SMP strings by normalised path so a
        # single physical config never produces two rows that differ only by case
        canonical = {}
        for v in shipped:
            canonical.setdefault(C.norm(v), v)
        for _, v in bindings:
            canonical.setdefault(C.norm(v), v)

        for xml_vp in (canonical[k] for k in sorted(canonical)):
            f = P.winner(xml_vp)
            prov = f["mod"] if f else ""
            sha = f.get("sha256", "") if f else ""
            shadow = "; ".join(P.shadowed(xml_vp)) if f else ""
            is_tri = xml_vp.lower().endswith(".tri")
            meshes = sorted(vp for vp, x in bindings if C.norm(x) == C.norm(xml_vp))
            bind_evidence = "HDT_SMPCONTAINER_STRING_IN_NIF"
            if is_tri and not meshes:
                # Havok .tri: frozen P00.parts relation "same-mod .tri physics mesh stem match"
                tdir, tstem = os.path.split(bs(xml_vp))
                tstem_l = os.path.splitext(tstem)[0].lower()
                meshes = sorted(
                    vp for vp in own_nifs
                    if os.path.dirname(bs(vp)).lower() == tdir.lower()
                    and os.path.splitext(os.path.basename(bs(vp)))[0].lower().startswith(tstem_l))
                bind_evidence = "SAME_DIR_SAME_STEM_TRI_MESH_MATCH" if meshes else ""

            if is_tri:
                bones, adds, cfg_type = [], [], "HAVOK_TRI"
            else:
                bones, adds = xml_bones(abspath_of(f)) if f else (None, None)
                cfg_type = "HDT_SMP_XML" if bones is not None else "XML_UNKNOWN_ROOT"

            if meshes:
                all_b, any_trunc = set(), False
                for mv in meshes:
                    b, tr = nif_bones(mv)
                    all_b |= b
                    any_trunc = any_trunc or tr
                missing = [b for b in (bones or []) if b not in all_b]
                if not all_b:
                    bstat = "UNKNOWN"
                elif not missing:
                    bstat = "OK"
                elif any_trunc:
                    bstat = "UNKNOWN"
                else:
                    bstat = "MISSING_BONE"
                if any_trunc and missing:
                    bstat = "UNKNOWN"
                bdep = "xml_bones=%d" % len(bones or [])
            else:
                all_b, missing, bstat = set(), [], "UNKNOWN"
                bdep = "xml_bones=%s" % (len(bones) if bones is not None else "UNKNOWN")
            if adds:
                bdep += ";addBone=%d" % len(adds)
            if meshes:
                bdep += ";mesh_bones=%d;mesh_bones_truncated=%s" % (
                    len(all_b), "yes" if any_trunc else "no")

            base = os.path.basename(bs(xml_vp))
            new_cfg = MESH_ROOT + oid + "\\physics\\" + base
            old_refs = [xml_vp] + meshes
            new_refs = [new_cfg] + [MESH_ROOT + oid + "\\" +
                                     os.path.basename(bs(m)) for m in meshes]
            rewrite = "YES" if xml_vp != new_cfg else "NO"

            notes = []
            if not meshes:
                notes.append("SHIPPED_BUT_NOT_BOUND_TO_ANY_IN_SCOPE_MESH")
            om = mod_owner(prov)
            if om and om != oid:
                notes.append("CROSS_OUTFIT_DEPENDENCY:" + om)
            elif not om and prov:
                notes.append("EXTERNAL_MOD_DEPENDENCY:" + prov)
            if f and len(P.providers(xml_vp)) > 1:
                same = [x["mod"] for x in P.providers(xml_vp)[1:] if x.get("sha256") == sha]
                if same:
                    notes.append("IDENTICAL_SHA_PROVIDERS=" + ";".join(same) +
                                 " PROPOSAL_SHARED_NOT_APPROVED; P02A keeps an independent copy")
            if bstat == "MISSING_BONE":
                notes.append("MISSING_BONES=" + ",".join(missing[:12]))
            if bstat == "UNKNOWN":
                notes.append("BONE_CHECK_INCONCLUSIVE (mesh bone list truncated in P00, or unbound)")
            pat = hit_patterns(xml_vp)
            if pat:
                notes.append("HISTORIC_NAME_PATTERN=" + "+".join(pat))
            if bind_evidence:
                notes.append("MESH_BINDING_EVIDENCE=" + bind_evidence)

            if is_tri:
                status = "REPOINT"
            elif om and om != oid:
                status = "CROSS_OUTFIT_DEPENDENCY"
            elif not om and prov:
                status = "EXTERNAL_MOD_DEPENDENCY"
            elif not meshes:
                status = "UNRESOLVED"
            else:
                status = "COPY_AND_REPOINT"

            rows.append([
                oid, xml_vp, cfg_type, prov, P.priority.get(prov, ""), shadow, sha,
                ";".join(meshes), bdep, xml_vp,
                ";".join(old_refs), ";".join(new_refs), rewrite, bstat,
                ",".join(missing[:12]), status, " | ".join(notes),
            ])
    return rows

# ===========================================================================
# main
# ===========================================================================
def cnt(rows, col, val):
    return sum(1 for r in rows if r[col] == val)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    rec_rows = build_record_rows()
    arma_rows = build_arma_rows()
    tex_rows = build_texture_rows()
    phys_rows = build_physics_rows()

    C.write_csv(os.path.join(OUT_DIR, "P02A_PLUGIN_RECORD_MIGRATION.csv"), REC_HEADER, rec_rows)
    C.write_csv(os.path.join(OUT_DIR, "P02A_ARMA_MODEL_REWRITE.csv"), ARMA_HEADER, arma_rows)
    C.write_csv(os.path.join(OUT_DIR, "P02A_PLUGIN_TEXTURE_REWRITE.csv"), TEX_HEADER, tex_rows)
    C.write_csv(os.path.join(OUT_DIR, "P02A_PHYSICS_MIGRATION.csv"), PHYS_HEADER, phys_rows)

    print("=" * 100)
    print("P02A PLUGIN / ARMA / TXST / PHYSICS MIGRATION PLAN  (READ-ONLY design stage, nothing executed)")
    print("target_plugin = %s   canonical body = %s" % (TARGET_PLUGIN, C.CANONICAL_BODY))
    print("rows: RECORD=%d  ARMA=%d  TEXTURE=%d  PHYSICS=%d"
          % (len(rec_rows), len(arma_rows), len(tex_rows), len(phys_rows)))
    print("=" * 100)

    hdr = ("%-20s %6s %6s %6s %6s | %6s %6s %6s | %6s %6s %6s | %6s %6s %6s" % (
        "OUTFIT_ID", "REC", "ARMA", "TEX", "PHYS",
        "aREPT", "aCOPY", "aUNKN",
        "tSELF", "tCROSS", "tEXTR",
        "bnOK", "bnMISS", "bnUNK"))
    print(hdr)
    print("-" * len(hdr))
    tot = collections.Counter()
    for oid in C.OUTFIT_IDS:
        a = [r for r in arma_rows if r[0] == oid]
        t = [r for r in tex_rows if r[0] == oid]
        ph = [r for r in phys_rows if r[0] == oid]
        rc = [r for r in rec_rows if r[0] == oid]
        cells = [
            oid, len(rc), len(a), len(t), len(ph),
            cnt(a, 11, "REPOINT"), cnt(a, 11, "COPY_AND_REPOINT"),
            cnt(a, 11, "UNRESOLVED") + cnt(a, 11, "NON_CANONICAL_SOURCE"),
            cnt(t, 10, "SELF"), cnt(t, 10, "CROSS_OUTFIT"),
            cnt(t, 10, "EXTERNAL_MOD") + cnt(t, 10, "VANILLA"),
            cnt(ph, 13, "OK"), cnt(ph, 13, "MISSING_BONE"), cnt(ph, 13, "UNKNOWN"),
        ]
        print("%-20s %6d %6d %6d %6d | %6d %6d %6d | %6d %6d %6d | %6d %6d %6d" % tuple(cells))
        tot["REC"] += len(rc); tot["ARMA"] += len(a)
        tot["TEX"] += len(t); tot["PHYS"] += len(ph)
        tot["UNKN"] += cells[7]; tot["BNDMISS"] += cells[12]
    print("-" * len(hdr))
    print("%-20s %6d %6d %6d %6d" % ("TOTAL", tot["REC"], tot["ARMA"], tot["TEX"], tot["PHYS"]))

    print()
    print("== record_type census per outfit ==")
    per = collections.defaultdict(collections.Counter)
    for x in rec_rows:
        per[x[0]][x[7]] += 1
    for oid in C.OUTFIT_IDS:
        print("   %-20s %s" % (oid, dict(per[oid])))
    alltypes = sorted({x[7] for x in rec_rows})
    print("   record types present : %s" % alltypes)
    for absent in ("ENCH", "KYWD", "OTFT"):
        if absent not in alltypes:
            print("   record type %-4s     : ABSENT in all 11 frozen source plugins" % absent)

    print()
    print("== model_role census (ARMA/ARMO model refs) ==")
    print("   %s" % dict(collections.Counter(x[6] for x in arma_rows)))

    print()
    print("== CROSS_OUTFIT dependencies (Outfit A runtime dependency on Outfit B) ==")
    n = 0
    for x in arma_rows:
        if str(x[10]).startswith("CROSS_OUTFIT"):
            print("   ARMA  %-20s %-8s %-5s %-46s -> %s" % (x[0], x[2], x[5], x[7], x[10])); n += 1
    for x in tex_rows:
        if x[10] == "CROSS_OUTFIT":
            print("   TEX   %-20s %-8s %-5s %-46s -> %s" % (x[0], x[2], x[5], x[6], x[9])); n += 1
    for x in phys_rows:
        if x[16] == "CROSS_OUTFIT_DEPENDENCY":
            print("   PHYS  %-20s %-46s -> %s" % (x[0], x[1], x[3])); n += 1
    if not n:
        print("   NONE - the 11 frozen outfits do not reference each other's plugin assets")
    print("   total = %d" % n)

    print()
    print("== EXTERNAL_MOD dependencies ==")
    ext = collections.Counter()
    for x in arma_rows:
        if str(x[10]).startswith("EXTERNAL_MOD"):
            ext[(x[0], x[15])] += 1
    for x in tex_rows:
        if x[10] == "EXTERNAL_MOD":
            ext[(x[0], x[8])] += 1
    for x in phys_rows:
        if x[16] == "EXTERNAL_MOD_DEPENDENCY":
            ext[(x[0], x[3])] += 1
    for (o, m), c in sorted(ext.items()):
        print("   %-20s %3d x  %s" % (o, c, m))
    if not ext:
        print("   NONE")

    print()
    print("== historic cross-outfit name patterns (KITTY / SOURYO / ST / BUNNY / ANGELI ...) ==")
    hp = collections.Counter()
    for x in arma_rows:
        s = str(x[-1])
        if "HISTORIC_NAME_PATTERN=" in s:
            tok = s.split("HISTORIC_NAME_PATTERN=")[1].split(" |")[0]
            hp[tok] += 1
    for x in tex_rows:
        if x[15]:
            hp["TXST:" + x[15]] += 1
    for k, c in sorted(hp.items()):
        print("   %-46s %d" % (k, c))
    if not hp:
        print("   NONE")

    print()
    print("== collisions ==")
    coll = [x for x in rec_rows if x[18]]
    print("   records whose source EDID is shared with another parsed plugin: %d" % len(coll))
    seen = set()
    for x in coll:
        k = (x[0], x[7], x[6])
        if k in seen:
            continue
        seen.add(k)
        print("      %-20s %-5s %-40s %s" % (x[0], x[7], x[6], x[18]))
    dup = [k for k, v in collections.Counter((x[0], x[12]) for x in rec_rows).items() if v > 1]
    print("   duplicate planned new_edid inside a single outfit: %d" % len(dup))
    for k in dup:
        print("      %s" % (k,))
    vc = sum(1 for x in arma_rows + tex_rows + phys_rows if "IDENTICAL_SHA" in str(x[-1]))
    print("   identical-SHA multi-provider rows (PROPOSAL_SHARED_NOT_APPROVED): %d" % vc)

    print()
    print("== UNRESOLVED ==")
    n = 0
    for x in arma_rows:
        if x[11] == "UNRESOLVED":
            print("   ARMA  %-20s %-8s %-5s %s" % (x[0], x[2], x[5], x[7])); n += 1
    for x in tex_rows:
        if x[11] == "UNRESOLVED":
            print("   TEX   %-20s %-8s %-5s %s" % (x[0], x[2], x[5], x[6])); n += 1
    for x in phys_rows:
        if x[16] == "UNRESOLVED":
            print("   PHYS  %-20s %s" % (x[0], x[1])); n += 1
    print("   total UNRESOLVED = %d" % n)

    print()
    print("== BLOCKERS ==")
    b = 0
    for x in phys_rows:
        if x[13] == "MISSING_BONE":
            print("   PHYS_BONE  %-20s %-48s missing=%s" % (x[0], x[1], x[14][:60])); b += 1
    for x in arma_rows:
        if str(x[10]).startswith("CROSS_OUTFIT"):
            print("   ARMA_CROSS %-20s %s -> %s" % (x[0], x[7], x[10])); b += 1
    for x in tex_rows:
        if x[10] == "CROSS_OUTFIT":
            print("   TEX_CROSS  %-20s %s -> %s" % (x[0], x[6], x[9])); b += 1
    print("   total blockers = %d" % b)
    print()
    print("NOTE: no FormID generated, no file copied, no plugin written, no NIF/DDS/OSP/OSD")
    print("      touched. All rows are P02A design-stage intent only.")
    print("      master_index is 000000 because plugins.txt is not rebuilt until P03.")


if __name__ == "__main__":
    main()
