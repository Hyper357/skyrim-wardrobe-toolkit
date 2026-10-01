#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p00r_parts.py - STAGE D: PARTS CATALOG + DIY COMPATIBILITY MATRIX.

Consumes the already-computed stage outputs (never recomputes them):
    data/P00_RERUN/02_plugin_records.json     (stage B, binary plugin parse)
    data/P00_RERUN/08_nif_parsed.json.gz      (stage C0, NIF parse)
    data/P00_RERUN/01_file_index.json.gz      (stage A, file index)
    data/P00_RERUN/07_bodyslide_projects.json (stage C1, BodySlide)
    data/P00_RERUN/01_mod_aggregates.json     (stage A, mod aggregates)

Emits:
    reports/P00_RERUN/04_PARTS_CATALOG.csv
    reports/P00_RERUN/05_SLOT_PARTITION_MAP.csv
    reports/P00_RERUN/06_DIY_COMPATIBILITY_MATRIX.csv
    data/P00_RERUN/04_parts.json

A "part" is one ARMO record - that is the in-game wearable unit.  ARMAs, TXSTs,
COBJs and OTFTs are NOT parts; they are used only as enrichment where a
reference actually resolves.

Game files are never opened by this script at all.  Nothing outside
data/P00_RERUN, reports/P00_RERUN and tools/P00_RERUN is written; every write
goes through C.write_csv / C.write_json, which assert the path.

Usage:  python tools/P00_RERUN/p00r_parts.py
"""
from __future__ import annotations

import gzip
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p00r_common as C  # noqa: E402

BS = "\\"

# --------------------------------------------------------------------------- #
# TASK A - part category classifier
# --------------------------------------------------------------------------- #
# Fixed vocabulary. Nothing outside this list is ever emitted; anything that
# does not match is OTHER.
VOCAB = ("BODY", "BODYSUIT", "BRA", "PANTY", "CORSET", "GLOVES", "SLEEVES",
         "BOOTS", "SHOES", "HEELS", "STOCKINGS", "MASK", "HOOD", "HAT", "VEIL",
         "COLLAR", "CHOKER", "BELT", "HARNESS", "STRAPS", "SKIRT", "COAT",
         "CLOAK", "CAPE", "TAIL", "DEVICE", "ACCESSORY", "OTHER")

# Priority order. The brief gives the token families in a specific order and
# says "first match wins"; the two families with no guidance of their own are
# placed so they cannot steal a match from a family the brief did specify:
#   * BODY sits immediately above OTHER, because after camel splitting
#     "AE_CorruptedBodySuit" yields the tokens "corrupted body suit" and BODY
#     must not pre-empt MASK / HOOD / COAT on "AE_..._Mask" / "_Hood" / "_Coat01".
#   * CLOAK sits just after COAT and before CAPE.
#   * STRAPS carries a negative lookahead so "strap-on"/"strapon" reaches DEVICE.
RULE_ORDER = (
    ("BODYSUIT", ("bodysuit", "lingerie", "unitard", "zentai", "catsuit",
                  "leotard", "playsuit", "swimsuit")),
    ("BRA", ("bra", "bralette")),
    ("PANTY", ("panty", "thong", "brief", "knickers")),
    ("CORSET", ("corset", "bustier", "cincher", "stays")),
    ("GLOVES", ("glove", "gauntlet", "mitten", "bracer")),
    ("SLEEVES", ("sleeve", "armwrap", "armband")),
    ("BOOTS", ("boot", "wellington")),
    ("SHOES", ("shoe", "sneaker", "loafer", "ballet shoe", "moccasin")),
    ("HEELS", ("heel", "pump", "stiletto")),
    ("STOCKINGS", ("stocking", "tights", "pantyhose")),
    ("MASK", ("mask",)),
    ("HOOD", ("hood",)),
    ("HAT", ("hat", "cap", "beret")),
    ("VEIL", ("veil",)),
    ("COLLAR", ("collar",)),
    ("CHOKER", ("choker",)),
    ("BELT", ("belt", "girdle")),
    ("HARNESS", ("harness", "bridle", "headharness")),
    ("STRAPS", ("strap",)),
    ("SKIRT", ("skirt",)),
    ("COAT", ("coat", "jacket", "parka", "overcoat")),
    ("CLOAK", ("cloak",)),
    ("CAPE", ("cape",)),
    ("TAIL", ("tail",)),
    ("DEVICE", ("device", "vibrator", "strapon", "strap on")),
    ("ACCESSORY", ("accessory", "jewel", "jewelry", "jewellery", "necklace",
                   "earring", "pendant", "bracelet", "bangle")),
    ("BODY", ("body",)),
)

# "flat" is in the brief's SHOES family, but a bare "flat" is far too loose in
# this corpus ("Flat Chest", "Flat Boots"), so it is matched as a whole word
# only, and without pluralisation.
EXTRA_RULES = (("SHOES", r"\bflats?\b"),)

# RULE_ORDER must cover the fixed vocabulary exactly once each.  Its ORDER is
# deliberately not the vocabulary order: BODY is listed first in the
# vocabulary but evaluated last (see the comment above RULE_ORDER).
assert sorted(list(dict(RULE_ORDER)) + ["OTHER"]) == sorted(VOCAB), \
    "RULE_ORDER must cover the fixed vocabulary exactly, once each"

# camelCase / snake_case / kebab-case all become token separators, otherwise
# "AE_CorruptedBodySuit_Mask" and "NyesLatexPackLatexHighHeels Auburn" would
# never expose "mask" / "heels" as words.
_CAM_A = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
_CAM_B = re.compile(r"(?<=[A-Z])(?=[A-Z][a-z])")
_NONALNUM = re.compile(r"[^0-9A-Za-z]+")
_SUFFIX = r"(?:s|es|ed|ing)?"


def words(text):
    """Lower-cased, space-padded, camel/snake/kebab split token stream."""
    if not text:
        return ""
    t = _CAM_A.sub(" ", text)
    t = _CAM_B.sub(" ", t)
    t = _NONALNUM.sub(" ", t)
    return " " + t.lower() + " "


def _compile_rules():
    out = []
    for cat, stems in RULE_ORDER:
        for stem in stems:
            pat = re.escape(stem).replace(r"\ ", r"\s+")
            out.append((cat, stem, re.compile(r"\b" + pat + _SUFFIX + r"\b")))
    for cat, pat in EXTRA_RULES:
        out.append((cat, pat, re.compile(pat)))
    return out


COMPILED = _compile_rules()
_STRAP_ON = re.compile(r"\bstrap\s*on\b")
_GUARDS = {"STRAPS": lambda w: not _STRAP_ON.search(w)}


def classify_part(edid, full, desc):
    """-> (part_category, category_rule).

    Searches EDID, then FULL, then DESC; inside a field RULE_ORDER decides
    (most specific first), which is what "first match wins" means here.
    category_rule records the token that actually fired and the field it came
    from, e.g. "heel@EDID". Anything unmatched becomes OTHER.
    """
    for field, txt in (("EDID", edid), ("FULL", full), ("DESC", desc)):
        w = words(txt)
        if not w.strip():
            continue
        for cat, stem, rx in COMPILED:
            guard = _GUARDS.get(cat)
            if guard is not None and not guard(w):
                continue
            if rx.search(w):
                return cat, stem + "@" + field
    return "OTHER", "none@-"

# --------------------------------------------------------------------------- #
# NIF path normalisation
# --------------------------------------------------------------------------- #
def norm_nif(path):
    """Forward slashes -> backslashes, lowercase, strip a leading meshes\\.

    Applied to BOTH sides of the join, so an ARMO model path written
    "NyesLatexPack\\WorldItems\\LatexCorsetDropitem.nif" and a stage-C0 row
    whose NIF_ID is "meshes\\nyeslatexpack\\worlditems\\latexcorsetdropitem.nif"
    meet on the same key.  Stripping on only one side links just 84 of 1448
    parts; stripping on both links 821.
    """
    p = (path or "").replace("/", BS).strip().lower()
    if p.startswith("meshes" + BS):
        p = p[len("meshes" + BS):]
    return p


def stem_key(text):
    """Loose alnum-only key used for ShapeData stem matching."""
    return re.sub(r"[^a-z0-9]+", "", (text or "").lower())


def first(rec, key, default=None):
    v = rec.get("subrecords", {}).get(key)
    if isinstance(v, list) and v:
        return v[0]
    if isinstance(v, str):
        return v
    return default


def strlist(rec, key):
    v = rec.get("subrecords", {}).get(key)
    if v is None:
        return []
    vals = v if isinstance(v, list) else [v]
    return [x for x in vals if isinstance(x, str) and x]


def dedup(seq):
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def hexid(v):
    try:
        return C.record_id(int(v))
    except (TypeError, ValueError):
        return None


def arma_nif_id(path):
    """ARMA MOD2..MOD5 path -> a stage-C0 NIF_ID key, or None.

    ARMA model paths are written relative to Data/meshes
    ("NyesLatexPack\\LatexBodysuit\\LatexBodysuit_1.nif"), so "meshes\\" is
    prepended when absent and the whole thing is lower-cased - the same
    normalisation C.nif_id() applies, which is what stage-C0 stored.
    """
    p = (path or "").replace("/", BS).strip().lower()
    if not p.endswith(".nif"):
        return None
    if not p.startswith("meshes" + BS):
        p = "meshes" + BS + p
    return C.nif_id(p)


def build_arma_index(records):
    """-> {"by_key": {(plugin, formid_int): ARMA}, "by_fid": {formid_int: [ARMA]}}.

    Both maps are needed: arma_refs carries the defining plugin, which is
    authoritative, but a cross-master ref may name a plugin that is not in the
    parsed set, and FormIDs are only unique within a master (162 formids in
    this corpus exist in more than one plugin, which is exactly what the old
    global-formid lookup got wrong).
    """
    by_key, by_fid = {}, defaultdict(list)
    for r in records:
        if r.get("record_type") != "ARMA":
            continue
        fid = r.get("formid_int")
        if fid is None:
            continue
        by_key[(r["plugin_file"].lower(), fid)] = r
        by_fid[fid].append(r)
    return {"by_key": by_key, "by_fid": by_fid}


def lookup_arma(arma_index, plugin, formid_hex):
    """Resolve one arma_refs entry to an in-scope ARMA record, or None."""
    m = re.fullmatch(r"[0-9A-Fa-f]{1,8}", (formid_hex or "").strip() or "x")
    if m is None:
        return None
    fid = int(formid_hex, 16)
    rec = arma_index["by_key"].get(((plugin or "").lower(), fid))
    if rec is not None:
        return rec
    cand = arma_index["by_fid"].get(fid) or ()
    return cand[0] if len(cand) == 1 else None


def txst_name(v):
    """Decode one texture_set_refs payload into the embedded TXST name.

    The upstream payload is [u32 formid][u32 name length][name\\0][...], so
    the readable outfit name ("Thigh:0", "Bodysuit") can be recovered.  The
    raw payload is returned unchanged when it does not decode that way.
    """
    if not isinstance(v, str) or not v:
        return None
    b = v.encode("utf-8", "replace")
    if len(b) >= 8 and len(b) % 2 == 0 and re.fullmatch(rb"(?:[0-9A-Fa-f]{2})+", b):
        b = bytes.fromhex(v)
    if len(b) < 8:
        return None
    nlen = int.from_bytes(b[4:8], "little")
    if not 0 < nlen <= 64 or 8 + nlen > len(b):
        return None
    name = b[8:8 + nlen].split(b"\0", 1)[0]
    try:
        return name.decode("ascii")
    except UnicodeDecodeError:
        return None


def clean_text(v, limit=200):
    """CSV/JSON-safe rendering of an arbitrary subrecord payload."""
    if v is None:
        return ""
    if not isinstance(v, str):
        v = str(v)
    if all(32 <= ord(ch) < 127 for ch in v):
        return v[:limit]
    return "0x" + v.encode("utf-8", "replace").hex()[:2 * limit]


# --------------------------------------------------------------------------- #
# loaders (read-only)
# --------------------------------------------------------------------------- #
def load_records():
    with open(os.path.join(C.DATA, "02_plugin_records.json"),
              encoding="utf-8") as fh:
        return json.load(fh)


def load_nifs():
    with gzip.open(os.path.join(C.DATA, "08_nif_parsed.json.gz"), "rt",
                   encoding="utf-8") as fh:
        rows = json.load(fh)
    by_key = defaultdict(list)
    for r in rows:
        by_key[norm_nif(r["NIF_ID"])].append(r)
    return rows, by_key


def load_projects():
    """-> (projects, project_meta, project -> {ShapeData stem keys}).

    Schema-tolerant: stage C1 has been emitted with two different field
    namings (project/shapedata_files/evidence vs
    ui_outfit_name/base_nif/body_evidence), so both are accepted.

    Match keys come from the ShapeData FILE names and their parent folder,
    never from the NIF-internal shape names: those are far too generic here
    ("Gloves", "3BA", "Base") and produced demonstrably false links when tried.
    """
    p = os.path.join(C.DATA, "07_bodyslide_projects.json")
    if not os.path.isfile(p):
        return [], {}, {}
    with open(p, encoding="utf-8") as fh:
        projs = json.load(fh)
    pmeta, stems = {}, defaultdict(set)
    for x in projs:
        name = (x.get("project") or x.get("ui_outfit_name")
                or x.get("slider_set_name") or "")
        if not name:
            continue
        meta = dict(x)
        meta["project"] = name
        if not meta.get("evidence"):
            meta["evidence"] = x.get("body_evidence") or []
        pmeta[name] = meta
        files = list(x.get("shapedata_files") or [])
        for f in (x.get("base_nif"), x.get("OSP_PATH"), x.get("source_file")):
            if f:
                files.append(f)
        for f in files:
            for seg in f.replace("/", BS).split(BS):
                k = stem_key(seg)
                if len(k) >= 8:
                    stems[name].add(k)
    sd_path = os.path.join(C.DATA, "07_bodyslide_shapedata.json")
    if os.path.isfile(sd_path):
        with open(sd_path, encoding="utf-8") as fh:
            sd = json.load(fh)
        for s in sd if isinstance(sd, list) else []:
            name = s.get("project") or s.get("name") or ""
            if name not in pmeta:
                continue
            for seg in str(s.get("file", "")).replace("/", BS).split(BS):
                k = stem_key(seg)
                if len(k) >= 8:
                    stems[name].add(k)
    return projs, pmeta, {k: v for k, v in stems.items() if v}


def load_index():
    """-> (index rows, mod -> {stem keys of that mod's .tri physics meshes})."""
    with gzip.open(os.path.join(C.DATA, "01_file_index.json.gz"), "rt",
                   encoding="utf-8") as fh:
        idx = json.load(fh)
    tri = defaultdict(set)
    for r in idx:
        if r.get("cat") == "physics_mesh":
            stem = r["rel"].replace("/", BS).split(BS)[-1].rsplit(".", 1)[0]
            k = stem_key(stem)
            if k:
                tri[r["mod"]].add(k)
    return idx, tri


def load_mod_body():
    path = os.path.join(C.DATA, "01_mod_aggregates.json")
    out = {}
    if not os.path.isfile(path):
        return out
    with open(path, encoding="utf-8") as fh:
        for m in json.load(fh):
            cand, tag, fams, flag, src = C.body_candidate_from_name(
                m.get("mod_name", ""))
            out[m["mod_name"]] = (cand, tag, flag, src)
    return out


# --------------------------------------------------------------------------- #
# part construction
# --------------------------------------------------------------------------- #
MIN_STEM = 8


def out_family(path):
    """(virtual directory, family stem) for a BodySlide output / ARMA mesh.

    A BodySlide project emits a family of files from one build:
        Corset.nif, Corset_0.nif, Corset_1.nif, Corset_1stPerson.nif
    and the ARMA references one member of that family. Comparing only the
    filename would miss the link; comparing only the directory would collide
    across a whole pack. Both are needed, and the numeric/1st-person suffix
    has to be stripped so the family is recognisable.

    Returns (None, None) for anything unusable rather than a guess.
    """
    if not path:
        return (None, None)
    q = str(path).replace("/", "\\").strip().lower()
    if not q or q in ("unknown", "none", "\\"):
        return (None, None)
    parts = [x for x in q.split("\\") if x]
    # An ARMA model path is mod-relative ('NyesLatexOutfit2\\Corset\\Corset_1.nif')
    # while an OSP OutputPath/OutputFile is already rooted at the VFS
    # ('meshes\\NyesLatexOutfit2\\Corset\\Corset.nif'). Without this the two
    # never compare equal and LEVEL 1 almost never fires.
    if parts and parts[0] != "meshes":
        parts = ["meshes"] + parts
    if len(parts) < 2:
        return (None, None)
    base = parts[-1]
    stem = re.sub(r"\.[a-z0-9]{1,5}$", "", base)
    # strip trailing _0/_1/_23 (BodySlide gender/weight variants)
    stem = re.sub(r"_\d+$", "", stem)
    # strip a 1st-person marker and anything after it
    stem = re.sub(r"(1st|2nd|3rd)person.*$", "", stem)
    stem = stem.strip("_- ")
    if not stem or len(stem) < 3:
        return (None, None)
    return ("\\".join(parts[:-1]), stem)
def build_parts(records, nif_by_key, arma_index, pstems, pmeta, tri_by_mod,
                mod_body):
    armo_recs = sorted((r for r in records if r["record_type"] == "ARMO"),
                       key=lambda r: (r["PLUGIN_ID"], r["formid"]))
    parts, map_rows = [], []
    # Only projects that actually reach the VFS may claim a part. Tolerate the
    # pre-VFS evidence shape (no `effective` key) so this module still runs
    # against an older data file, but never silently use a shadowed project
    # once the flag exists.
    effective_projects = [
        k for k, v in pmeta.items()
        if str(v.get("effective", "yes")).lower() in ("yes", "true", "1")
    ]
    shadowed_projects = [k for k in pmeta if k not in set(effective_projects)]
    unres_examples, zero_shape, no_model = [], [], []
    proj_stem_index = [(proj, s) for proj, s in sorted(pstems.items()) if s]

    for rec in armo_recs:
        subs = rec["subrecords"]
        armo = rec.get("armo") or {}
        edid = first(rec, "EDID", "") or ""
        full = first(rec, "FULL", "") or ""
        desc = first(rec, "DESC", "") or ""
        plugin_id = C.plugin_id(os.path.basename(rec["plugin_file"]))
        part_id = "PART::" + plugin_id + "::" + rec["formid"]
        cat, rule = classify_part(edid, full, desc)

        # ---- ARMA (armor addon) resolution: ARMO -> MODL -> ARMA, 1 : N ----
        # ARMO.RNAM is the RACE, never an ArmorAddon, and is not used as a
        # link at all.  The only link is the repeated ARMO.MODL subrecord,
        # which stage B has already resolved honouring the master byte and
        # reported as armo.arma_refs; a part may carry several addons, so all
        # of them are kept rather than the first hit.
        arma_edids, arma_files, arma_recs = [], [], []
        routes, n_refs, n_hit, n_fallback = [], 0, 0, 0
        for ref in (armo.get("arma_refs") or []):
            n_refs += 1
            fid = (ref.get("formid") or "").strip().upper()
            pl = (ref.get("plugin") or "").lower()
            # arma_refs already carries the master-resolved plugin, so the
            # (plugin, formid) key honours the master byte.  The by-formid
            # fallback only fires for a formid that is unique in scope, and is
            # counted in the note when it does.
            rec_a = lookup_arma(arma_index, pl, fid)
            if rec_a is None and re.fullmatch(r"[0-9A-Fa-f]{1,8}", fid or "x"):
                cand = arma_index["by_fid"].get(int(fid, 16)) or ()
                if len(cand) == 1:
                    rec_a, n_fallback = cand[0], n_fallback + 1
            arma_edids.append(ref.get("edid") or "")
            # Every linked addon is listed, not only the ones whose record we
            # happen to hold. appending inside the `rec_a is not None` branch
            # silently dropped cross-plugin addons (the vanilla
            # FullLeatherHelmet* family), so n_arma_refs said 4 while
            # ARMA_formids showed 1 and the row looked self-contradictory.
            # The owning plugin is known from the FormKey resolution even when
            # the record itself is outside the parsed scope.
            if rec_a is not None:
                n_hit += 1
                arma_recs.append(rec_a)
                arma_files.append(C.plugin_id(
                    os.path.basename(rec_a["plugin_file"])) + ":" + fid)
            else:
                owner = pl or "out_of_scope"
                arma_files.append(C.plugin_id(os.path.basename(owner))
                                  + ":" + fid)
        for m in (armo.get("modl_refs") or []):
            if m.get("is_arma") and m.get("route"):
                routes.append(m["route"])
        routes = dedup(routes)

        # ---- wearable model paths: ARMA MOD2..MOD5 ONLY ------------------
        # ARMO MOD2..MOD5 are world/inventory DROP models ("...DropItem.nif")
        # and are kept in their own column; they must never stand in for the
        # worn garment mesh.  ARMA.MODL is the source-mesh ref list, not a
        # wearable path, so it is not used here either.
        model_paths = []
        for rec_a in arma_recs:
            amp = ((rec_a.get("arma") or {}).get("addon_model_paths") or {})
            for mk in ("MOD2", "MOD3", "MOD4", "MOD5"):
                model_paths.extend(p for p in (amp.get(mk) or [])
                                   if isinstance(p, str) and p)
        model_paths = dedup(model_paths)
        model_source = ("ARMA.MOD2..MOD5 via ARMO.MODL" if arma_recs
                        else "none:ARMO.MODL resolved to no in-scope ARMA")

        # ---- world / inventory drop models, kept strictly separate --------
        world_model_paths = dedup(p for p in (armo.get("world_model_paths") or [])
                                  if isinstance(p, str) and p)
        world_hits = [p for p in world_model_paths
                      if (norm_nif(C.nif_id(p)) in nif_by_key)]

        # ---- slots: the addon's BOD2 is authoritative ---------------------
        # An ArmorAddon overrides the slot mask of the ARMO it belongs to, so
        # once one resolves its BOD2 is used and the source is recorded.
        if arma_recs:
            slots = arma_recs[0].get("arma") or {}
            slot_mask = slots.get("slot_mask", "")
            slot_mask_hex = slots.get("slot_mask_hex", "")
            slot_names = list(slots.get("slot_names") or [])
            slot_source = "ARMA.BOD2 (authoritative addon slots)"
        else:
            slot_mask = armo.get("slot_mask", "")
            slot_mask_hex = armo.get("slot_mask_hex", "")
            slot_names = list(armo.get("slot_names") or [])
            slot_source = "ARMO.BOD2"

        notes = []
        if n_fallback:
            notes.append(str(n_fallback) + " ARMA ref(s) resolved by an "
                         "unambiguous formid fallback (defining plugin absent "
                         "from the parsed set)")
        if n_refs == 0:
            notes.append("ARMO.MODL carries no ArmorAddon ref")
            no_model.append((edid, rec["PLUGIN_ID"]))
        elif n_hit < n_refs:
            notes.append(str(n_refs - n_hit) + " of " + str(n_refs)
                         + " ARMA ref(s) did not resolve in scope")
        if world_model_paths:
            notes.append("ARMO.MOD2..MOD5 are world/inventory drop models ("
                         + str(len(world_hits)) + "/" + str(len(world_model_paths))
                         + " present in the VFS), NOT the worn mesh")

        # ---- game NIFs vs pending build targets vs ShapeData sources ------
        # The ARMA wearable path is frequently a BodySlide BUILD OUTPUT that
        # does not exist on disk because P00 is read-only and never runs
        # Build.  Those are reported as pending, never silently replaced by
        # the ShapeData base mesh, which is reported separately instead.
        game_ids, pending_ids = [], []
        for p in model_paths:
            nid = arma_nif_id(p)
            if not nid:
                continue
            hit = nif_by_key.get(norm_nif(nid))
            if hit:
                game_ids.append(hit[0]["NIF_ID"])
            else:
                pending_ids.append(nid)
        game_ids, pending_ids = dedup(game_ids), dedup(pending_ids)

        # ---- BodySlide project match (ShapeData stem) --------------------
        # Match keys are the part's own names and its ARMA mesh file names.
        # The ARMO drop-model names are deliberately NOT used: measured, they
        # ---- BodySlide project match: EXACT then UNIQUE-STRONG then UNKNOWN ---
        #
        # REPLACED. The previous matcher used substring containment
        # (`s in k or k in s`) over stem keys, which is not evidence of a
        # relationship. Measured damage: J3Bodysuit matched 15 projects across
        # the Nye / Corrupted / Gantz / Catwoman / Predator packs, and Brastia
        # Choker, Gloves, Mask and Cape all attached to the Spandexer Boots
        # project. That is a shared pack folder name, not a shared asset.
        #
        # Only effective (non-MO2-shadowed) OSP projects are eligible, so a
        # project whose .osp is overridden by a higher-priority mod can never
        # claim a part.
        #
        # LEVEL 1 EXACT_OUTPUT_PATH - the ARMA wearable mesh path and the OSP
        #   output_nif resolve to the same virtual family, where
        #   foo.nif / foo_0.nif / foo_1.nif / foo_1stpersonbody_1.nif are one
        #   family. Directory AND family stem must both agree.
        # LEVEL 2 UNIQUE_STRONG_MATCH - only inside the same source mod, on the
        #   family stem alone, and only when exactly one effective project in
        #   that mod is a candidate.
        # LEVEL 3 UNKNOWN - everything else. Coverage is never traded for a
        #   guess.
        matched_projects = set()
        match_method = "UNKNOWN"
        match_confidence = "NONE"
        candidate_count = 0

        part_dirs, part_fams = set(), set()
        for p in model_paths:
            k = out_family(p)
            if not k:
                continue
            part_dirs.add(k[0])
            part_fams.add(k[1])

        cands = {}
        for proj in effective_projects:
            on = (pmeta.get(proj) or {}).get("output_nif") or ""
            if not on or on in ("UNKNOWN", "none"):
                continue
            k = out_family(on)
            if k:
                cands.setdefault(k, []).append(proj)

        exact = []
        for p in model_paths:
            k = out_family(p)
            if k and k in cands:
                exact.extend(cands[k])
        if exact:
            matched_projects = set(exact)
            match_method = "EXACT_OUTPUT_PATH"
            match_confidence = "HIGH"
            candidate_count = len(matched_projects)
        else:
            # LEVEL 2, strictly inside the owning mod
            own = [proj for proj in effective_projects
                   if (pmeta.get(proj) or {}).get("MOD_ID") == rec["MOD_ID"]]
            strong = []
            for proj in own:
                on = (pmeta.get(proj) or {}).get("output_nif") or ""
                k = out_family(on) if on not in ("UNKNOWN", "none", "") else None
                if not k:
                    continue
                if k[1] in part_fams:
                    strong.append(proj)
            if len(strong) == 1:
                matched_projects = {strong[0]}
                match_method = "UNIQUE_STRONG_MATCH"
                match_confidence = "MEDIUM"
                candidate_count = 1
            else:
                candidate_count = len(strong)

        # ShapeData base NIFs: the geometry that IS on disk for a
        # BodySlide-converted outfit.  Only those present in the VFS are
        # claimed as on-disk sources.
        source_ids = []
        for proj in sorted(matched_projects):
            b = ((pmeta.get(proj) or {}).get("base_nif")
                 or "").replace("/", BS).strip().lower()
            if not b.endswith(".nif") or b in ("unknown",):
                continue
            hit = nif_by_key.get(norm_nif(b))
            if hit:
                source_ids.append(hit[0]["NIF_ID"])
        source_ids = dedup(source_ids)

        scan_ids = dedup(game_ids + source_ids)
        nif_rows = [n for k in [norm_nif(i) for i in scan_ids]
                    for n in nif_by_key.get(k, ())]
        nif_ids = dedup([n["NIF_ID"] for n in nif_rows])
        if game_ids:
            nif_resolved, link_src = "yes", "arma_addon"
        elif nif_rows:
            nif_resolved, link_src = "partial", "bodyslide_shapedata"
        else:
            nif_resolved, link_src = "no", "none"
        if pending_ids:
            notes.append(str(len(pending_ids)) + " ARMA wearable model path(s) "
                         "do not exist yet (BodySlide Build output; P00 never "
                         "runs Build)")
            unres_examples.append((edid, rec["MOD_ID"], pending_ids[:2]))
        if source_ids:
            notes.append(str(len(source_ids)) + " BodySlide ShapeData base NIF(s) "
                         "on disk are the geometry actually present")

        # ---- shapes / partitions / textures / physics ---------------------
        shape_names, partitions, textures = [], [], []
        smp_reasons, smp_nifs = [], []
        nif_shape_names = []
        for n in nif_rows:
            for s in n.get("shapes") or []:
                nm = s.get("name") or ""
                if nm:
                    shape_names.append(nm)
                    nif_shape_names.append(nm)
                for p in (s.get("partitions") or []):
                    partitions.append(p)
                for slot, path in (s.get("textures") or {}).items():
                    if path:
                        textures.append(slot + "=" + path)
            if n.get("has_smp"):
                smp_reasons.append(n.get("smp_reason") or "")
                smp_nifs.append(n["NIF_ID"])
        shape_names = dedup(shape_names)
        partitions = dedup(partitions)
        textures = dedup(textures)

        # ---- texture sets: from the ARMOR ADDON, never from the ARMO ------
        # ARMA carries the per-addon MO2S..MO5T weight/texture-set overrides
        # that the part actually wears, so texture_set_paths is built from the
        # resolved addon records.  The payload is a binary subrecord, not a
        # path, so the embedded TXST name is recovered where possible and the
        # raw payload is kept otherwise.
        tset = []
        for rec_a in arma_recs:
            refs = ((rec_a.get("arma") or {}).get("texture_set_refs") or {})
            for tk in ("MO2S", "MO2T", "MO3S", "MO3T",
                       "MO4S", "MO4T", "MO5S", "MO5T"):
                for v in refs.get(tk) or []:
                    nm = txst_name(v)
                    if nm is not None:
                        if nm:
                            tset.append(tk + "=" + nm)
                    else:
                        cv = clean_text(v)
                        if cv:
                            tset.append(tk + "=" + cv)
        tset = dedup(tset)

        # physics: stage-C0 SMP evidence, else a same-mod .tri physics mesh
        # from the stage-A file index whose stem matches this part.
        physics, phys_note = "no", ""
        if smp_nifs:
            physics = "yes:nif_smp"
            phys_note = "NIF SMP " + "|".join(smp_reasons)[:80]
        else:
            ks = {k for k in (stem_key(edid), stem_key(full)) if k}
            ks |= {stem_key(p.replace("/", BS).split(BS)[-1].rsplit(".", 1)[0])
                   for p in model_paths}
            hits = sorted(t for t in tri_by_mod.get(rec["MOD_ID"], ())
                          if any(t == k or (len(t) >= 8 and len(k) >= 8 and
                                            (t.startswith(k) or k.startswith(t)))
                                 for k in ks))
            if hits:
                physics = "yes:havok_tri"
                phys_note = "same-mod .tri physics mesh stem match"

        if nif_rows and all(n.get("shape_count", 0) == 0 for n in nif_rows):
            is_empty = "yes"
            zero_shape.append((edid, rec["PLUGIN_ID"]))
        else:
            is_empty = "no"

        # ---- body candidate: evidence first-match in a fixed chain --------
        body, bnote = "UNKNOWN", ""
        for proj in sorted(matched_projects):
            meta = pmeta.get(proj) or {}
            if (meta.get("body_candidate") or "UNKNOWN") != "UNKNOWN":
                body = meta["body_candidate"]
                _e = meta.get("evidence") or []
                ev = (";".join(_e) if isinstance(_e, list)
                      else str(_e))
                bnote = "bodyslide_project:" + proj + ("|" + ev if ev else "")
                break
        if body == "UNKNOWN":
            cand, tag, fams, flag, src = C.body_candidate_from_name(
                " ".join(x for x in (edid, full, desc) if x))
            if cand != "UNKNOWN":
                body = cand
                bnote = "part_name:" + src + "(" + flag + ")"
        if body == "UNKNOWN" and nif_shape_names:
            cand, fams, flag = C.body_candidate_from_assets(
                (), (), (), nif_shape_names)
            if cand != "UNKNOWN":
                body = cand
                bnote = "nif_shape_name(" + flag + ")"
        if body == "UNKNOWN":
            info = mod_body.get(rec["MOD_ID"])
            if info and info[0] != "UNKNOWN":
                body = info[0]
                bnote = "mod_folder_name:" + info[3] + "(" + info[2] + ")"
        if not bnote:
            bnote = ("no body evidence in EDID/FULL/DESC, linked NIF shape "
                     "names, BodySlide ShapeData or the MO2 mod name")

        kw = [k for k in (subs.get("KWDA") or []) if isinstance(k, str)]

        parts.append({
            "PART_ID": part_id,
            "part_category": cat,
            "category_rule": rule,
            "MOD_ID": rec["MOD_ID"],
            "source_mod": rec["source_mod"],
            "PLUGIN_ID": plugin_id,
            "plugin_file": rec["plugin_file"],
            "ARMO_formid": rec["formid"],
            "ARMA_formids": ";".join(x for x in arma_files if x),
            "n_arma_refs": n_refs,
            "ARMA_edids": ";".join(arma_edids),
            "ARMA_resolved": str(n_hit) + "/" + str(n_refs),
            "ARMA_routes": ";".join(routes),
            "race_formid": armo.get("race_raw", ""),
            "race_is": armo.get("race_is", ""),
            "EDID": edid,
            "FULL": full,
            "DESC": desc,
            "slot_mask": slot_mask,
            "slot_mask_hex": slot_mask_hex,
            "slot_names": ";".join(slot_names),
            "slot_source": slot_source,
            "priority": rec["priority"],
            "model_paths": ";".join(model_paths),
            "model_source": model_source,
            "game_nif_paths": ";".join(game_ids),
        "game_nif_resolution_status": (
            "RESOLVED" if game_ids and not pending_ids else
            ("PARTIAL" if game_ids else
             ("PENDING_BODYSLIDE" if pending_ids else "UNRESOLVED"))),
            "bodyslide_source_nifs": ";".join(source_ids),
            "pending_build_nifs": ";".join(pending_ids),
            "world_model_paths": ";".join(world_model_paths),
            "world_model_count": len(world_model_paths),
            "nif_ids": ";".join(nif_ids),
            "nif_resolved": nif_resolved,
            "shape_names": ";".join(shape_names),
            "partitions": ";".join(partitions),
            "bodyslide_projects": ";".join(sorted(matched_projects)),
            "bodyslide_match_method": match_method,
            "bodyslide_match_confidence": match_confidence,
            "bodyslide_candidate_count": candidate_count,
            "body_candidate": body,
            "body_evidence": bnote,
            "physics": physics,
            "material_class": "PENDING_STAGE_11",
            "texture_set_paths": ";".join(tset),
            "keywords": ";".join(kw),
            "n_keywords": len(kw),
            "is_empty_shell": is_empty,
            "note": "; ".join(notes) + ("; " + phys_note if phys_note else ""),
            "_partitions": partitions,
            "_body": body,
            "_physics": physics != "no",
            "_slots": list(slot_names),
            "_slot_mask": slot_mask,
            "_nif_rows": nif_rows,
            "_link_src": link_src,
            "_nif_textures": textures,
            "_n_arma_refs": n_refs,
            "_n_game_nifs": len(game_ids),
            "_n_pending": len(pending_ids),
            "_n_source": len(source_ids),
            "_n_world_resolved": len(world_hits),
        })

    # ---- TASK C: 05_SLOT_PARTITION_MAP ------------------------------------
    for p in parts:
        for sn in p["_slots"]:
            map_rows.append({
                "PART_ID": p["PART_ID"], "MOD_ID": p["MOD_ID"],
                "part_category": p["part_category"], "slot_name": sn,
                "slot_bit": "", "slot_mask": p["_slot_mask"],
                "partition_name": "", "nif_id": "", "shape_name": "",
                "n_bones": "", "skinned": "",
                "body_candidate": p["body_candidate"],
                "note": p["slot_source"],
            })
        seen = set()
        for n in p["_nif_rows"]:
            for s in n.get("shapes") or []:
                nb = s.get("n_bones") or 0
                skinned = "yes" if (s.get("has_skin_instance") or nb > 0) else "no"
                pos = s.get("partitions") or []
                if not pos:
                    map_rows.append({
                        "PART_ID": p["PART_ID"], "MOD_ID": p["MOD_ID"],
                        "part_category": p["part_category"], "slot_name": "",
                        "slot_bit": "", "slot_mask": p["_slot_mask"],
                        "partition_name": "", "nif_id": n["NIF_ID"],
                        "shape_name": s.get("name") or "", "n_bones": nb,
                        "skinned": skinned,
                        "body_candidate": p["body_candidate"],
                        "note": "shape carries no partition",
                    })
                for pn in pos:
                    sig = (n["NIF_ID"], s.get("name") or "", pn)
                    if sig in seen:
                        continue
                    seen.add(sig)
                    map_rows.append({
                        "PART_ID": p["PART_ID"], "MOD_ID": p["MOD_ID"],
                        "part_category": p["part_category"], "slot_name": "",
                        "slot_bit": "", "slot_mask": p["_slot_mask"],
                        "partition_name": pn, "nif_id": n["NIF_ID"],
                        "shape_name": s.get("name") or "", "n_bones": nb,
                        "skinned": skinned,
                        "body_candidate": p["body_candidate"],
                        "note": "SBP partition from stage C0 shape.partitions",
                    })
    return parts, map_rows, {"unres_examples": unres_examples,
                             "zero_shape": zero_shape,
                             "no_model": no_model}

# --------------------------------------------------------------------------- #
# TASK D - DIY compatibility matrix
# --------------------------------------------------------------------------- #
MAX_MODS_PER_CATEGORY = 40
KNOWN_BODY = {"CBBE", "CBBE_3BA", "BHUNP", "OTHER"}


def short_list(seq, limit=8):
    seq = list(dict.fromkeys(seq))
    if len(seq) <= limit:
        return ";".join(seq)
    return ";".join(seq[:limit]) + (";+" + str(len(seq) - limit) + "more")


def build_matrix(parts):
    by_cat = defaultdict(list)
    for p in parts:
        by_cat[p["part_category"]].append(p)

    rows, caps = [], []
    for cat in sorted(by_cat):
        members = by_cat[cat]
        mods = Counter(p["MOD_ID"] for p in members)
        keep = {m for m, _ in mods.most_common(MAX_MODS_PER_CATEGORY)}
        if len(keep) < len(mods):
            dropped = sorted(set(mods) - keep)
            caps.append({"part_category": cat, "mods_total": len(mods),
                         "mods_kept": len(keep), "mods_dropped": dropped})
            members = [p for p in members if p["MOD_ID"] in keep]
            cap_note = ("capped to the " + str(MAX_MODS_PER_CATEGORY)
                        + " largest mods; " + str(len(dropped))
                        + " mod(s) dropped: " + "|".join(dropped))
        else:
            cap_note = ""
        by_mod = defaultdict(list)
        for p in members:
            by_mod[p["MOD_ID"]].append(p)
        for ma in sorted(by_mod):
            for mb in sorted(by_mod):
                if ma == mb:
                    continue
                for a in by_mod[ma]:
                    for b in by_mod[mb]:
                        sa = set(a["_slots"])
                        sb = set(b["_slots"])
                        pa = set(a["_partitions"])
                        pb = set(b["_partitions"])
                        pinter = sorted(
                            {x for x in pa if "BODY" not in x.upper()}
                            & {x for x in pb if "BODY" not in x.upper()})
                        sinter = sorted(sa & sb)
                        if (a["body_candidate"] in KNOWN_BODY
                                and b["body_candidate"] in KNOWN_BODY
                                and a["body_candidate"] != b["body_candidate"]):
                            status = "BODY_TYPE_MISMATCH"
                        elif pinter:
                            status = "PARTITION_CONFLICT"
                        elif a["_physics"] != b["_physics"]:
                            status = "PHYSICS_CONFLICT"
                        elif sinter:
                            status = "SLOT_CONFLICT"
                        elif ({"body", "chest"} & sa) and ({"body", "chest"} & sb):
                            status = "MESH_OVERLAP_RISK"
                        elif (a["body_candidate"] == "UNKNOWN"
                              or b["body_candidate"] == "UNKNOWN"):
                            status = "UNKNOWN"
                        else:
                            status = "COMPATIBLE"

                        bits = []
                        if cap_note:
                            bits.append(cap_note)
                        if (status == "SLOT_CONFLICT"
                                and ({"body", "chest"} & sa)
                                and ({"body", "chest"} & sb)):
                            bits.append("both cover body/chest, so "
                                        "MESH_OVERLAP_RISK also applies but "
                                        "SLOT_CONFLICT is tested first")
                        if (a["is_empty_shell"] == "yes"
                                or b["is_empty_shell"] == "yes"):
                            bits.append("one side is an empty shell "
                                        "(shape_count 0)")
                        if not a["nif_ids"] or not b["nif_ids"]:
                            bits.append("one side has no linked NIF")
                        if pinter:
                            bits.append("shared non-body partition: "
                                        + "|".join(pinter))
                        rows.append({
                            "pair_id": "PAIR::" + cat + "::"
                                       + a["PLUGIN_ID"] + "::"
                                       + a["ARMO_formid"] + "::"
                                       + b["PLUGIN_ID"] + "::"
                                       + b["ARMO_formid"],
                            "part_a_id": a["PART_ID"],
                            "part_b_id": b["PART_ID"],
                            "mod_a": a["MOD_ID"],
                            "mod_b": b["MOD_ID"],
                            "part_category": cat,
                            "status": status,
                            "slot_a": short_list(sorted(sa)),
                            "slot_b": short_list(sorted(sb)),
                            "partition_a": short_list(sorted(pa)),
                            "partition_b": short_list(sorted(pb)),
                            "body_a": a["body_candidate"],
                            "body_b": b["body_candidate"],
                            "physics_a": a["physics"],
                            "physics_b": b["physics"],
                            "POTENTIAL_SLOT_REMAP": "yes" if status in (
                                "SLOT_CONFLICT", "MESH_OVERLAP_RISK") else "no",
                            "note": "; ".join(bits),
                        })
    rows.sort(key=lambda r: (r["part_category"], r["mod_a"], r["part_a_id"],
                             r["mod_b"], r["part_b_id"]))
    return rows, caps


# --------------------------------------------------------------------------- #
# driver
# --------------------------------------------------------------------------- #
CAT_COLS = ("PART_ID", "part_category", "category_rule", "MOD_ID", "source_mod",
            "PLUGIN_ID", "plugin_file", "ARMO_formid", "ARMA_formids",
            "n_arma_refs", "ARMA_edids", "ARMA_resolved", "ARMA_routes",
            "race_formid", "race_is", "EDID", "FULL", "DESC", "slot_mask",
            "slot_mask_hex", "slot_names", "slot_source", "priority",
            "model_paths", "model_source", "game_nif_paths",
        "game_nif_resolution_status",
            "bodyslide_source_nifs", "pending_build_nifs", "world_model_paths",
            "world_model_count", "nif_ids", "nif_resolved", "shape_names",
            "partitions", "bodyslide_projects", "bodyslide_match_method",
        "bodyslide_match_confidence", "bodyslide_candidate_count",
        "body_candidate", "body_evidence",
            "physics", "material_class", "texture_set_paths", "keywords",
            "n_keywords", "is_empty_shell", "note")
MAP_COLS = ("PART_ID", "MOD_ID", "part_category", "slot_name", "slot_bit",
            "slot_mask", "partition_name", "nif_id", "shape_name", "n_bones",
            "skinned", "body_candidate", "note")
MAT_COLS = ("pair_id", "part_a_id", "part_b_id", "mod_a", "mod_b",
            "part_category", "status", "slot_a", "slot_b", "partition_a",
            "partition_b", "body_a", "body_b", "physics_a", "physics_b",
            "POTENTIAL_SLOT_REMAP", "note")
def main():
    t0 = time.time()
    C.ensure_dirs()
    C.log("stage D: loading stage A/B/C outputs (read-only)")
    records = load_records()
    nif_rows, nif_by_key = load_nifs()
    projs, pmeta, pstems = load_projects()
    idx, tri_by_mod = load_index()
    mod_body = load_mod_body()
    C.log("records=" + str(len(records)) + " nif_rows=" + str(len(nif_rows))
          + " unique_nif_keys=" + str(len(nif_by_key))
          + " bodyslide_projects=" + str(len(projs))
          + " index=" + str(len(idx)))

    arma_index = build_arma_index(records)
    parts, map_rows, diag = build_parts(records, nif_by_key, arma_index,
                                        pstems, pmeta, tri_by_mod, mod_body)
    C.log("parts=" + str(len(parts)) + "  slot/partition map rows="
          + str(len(map_rows)))

    mat_rows, caps = build_matrix(parts)
    C.log("diy matrix rows=" + str(len(mat_rows)))

    ids = [p["PART_ID"] for p in parts]
    assert len(ids) == len(set(ids)), "PART_ID is not unique"
    pair_ids = [r["pair_id"] for r in mat_rows]
    assert len(pair_ids) == len(set(pair_ids)), "pair_id is not unique"

    n_cat = C.write_csv(os.path.join(C.REPORTS, "04_PARTS_CATALOG.csv"),
                        CAT_COLS, parts)
    n_map = C.write_csv(os.path.join(C.REPORTS, "05_SLOT_PARTITION_MAP.csv"),
                        MAP_COLS, map_rows)
    n_mat = C.write_csv(
        os.path.join(C.REPORTS, "06_DIY_COMPATIBILITY_MATRIX.csv"),
        MAT_COLS, mat_rows)
    C.log("wrote 04_PARTS_CATALOG.csv rows=" + str(n_cat))
    C.log("wrote 05_SLOT_PARTITION_MAP.csv rows=" + str(n_map))
    C.log("wrote 06_DIY_COMPATIBILITY_MATRIX.csv rows=" + str(n_mat))

    part_partitions = Counter()
    for p in parts:
        part_partitions.update(set(p["_partitions"]))
    all_partitions = Counter()
    for n in nif_rows:
        for s in n.get("shapes") or []:
            all_partitions.update(s.get("partitions") or [])

    stats = {
        "record_types": dict(Counter(r["record_type"] for r in records)),
        "parts_total": len(parts),
        "part_category": dict(Counter(p["part_category"] for p in parts)),
        "category_rule_top": Counter(
            p["category_rule"] for p in parts).most_common(40),
        "nif_resolved": dict(Counter(p["nif_resolved"] for p in parts)),
        "nif_link_source": dict(Counter(p["_link_src"] for p in parts)),
        "nif_resolved_mods": dict(Counter(
            p["MOD_ID"] for p in parts
            if p["nif_resolved"] != "no").most_common(15)),
        "unresolved_mods": dict(Counter(
            p["MOD_ID"] for p in parts
            if p["nif_resolved"] == "no" and p["model_paths"]).most_common(15)),
        "unresolved_model_path_examples": diag["unres_examples"][:25],
        "slot_mask": dict(Counter(str(p["slot_mask"])
                                  for p in parts).most_common()),
        "slot_source": dict(Counter(p["slot_source"] for p in parts)),
        "slot_name": dict(Counter(s for p in parts
                                  for s in p["_slots"]).most_common()),
        "partitions_unique_all_nifs": len(all_partitions),
        "partitions_top10_all_nifs": all_partitions.most_common(10),
        "partitions_unique_on_linked_nifs": len(part_partitions),
        "partitions_top10_on_linked_nifs": part_partitions.most_common(10),
        "body_candidate": dict(Counter(p["body_candidate"] for p in parts)),
        "body_evidence_source": dict(Counter(
            p["body_evidence"].split("(")[0].split(":")[0] for p in parts)),
        "physics": dict(Counter(p["physics"] for p in parts)),
        "is_empty_shell": dict(Counter(p["is_empty_shell"] for p in parts)),
        "zero_shape_parts": diag["zero_shape"][:40],
        "armo_without_arma_ref": diag["no_model"][:40],
        "armo_without_arma_ref_total": len(diag["no_model"]),
        "parts_with_bodyslide_project": sum(
            1 for p in parts if p["bodyslide_projects"]),
        "n_arma_refs_distribution": dict(Counter(
            p["n_arma_refs"] for p in parts)),
        "arma_linked_parts": sum(1 for p in parts if p["_n_arma_refs"]),
        "arma_resolved_all": sum(
            1 for p in parts if p["_n_arma_refs"]
            and p["ARMA_resolved"] == str(p["_n_arma_refs"]) + "/"
            + str(p["_n_arma_refs"])),
        "arma_link_1n_parts": sum(1 for p in parts if p["_n_arma_refs"] > 1),
        "parts_with_resolved_wearable_nif": sum(
            1 for p in parts if p["_n_game_nifs"]),
        "parts_with_pending_build_nif": sum(
            1 for p in parts if p["_n_pending"]),
        "parts_with_bodyslide_source_nif": sum(
            1 for p in parts if p["_n_source"]),
        "parts_with_world_model_path": sum(
            1 for p in parts if p["world_model_count"]),
        "parts_with_world_model_nif_in_vfs": sum(
            1 for p in parts if p["_n_world_resolved"]),
        "model_source": dict(Counter(p["model_source"] for p in parts)),
        "parts_with_texture_paths": sum(
            1 for p in parts if p["texture_set_paths"]),
        "matrix_category_caps": caps,
        "matrix_status": dict(Counter(r["status"] for r in mat_rows)),
        "matrix_potential_remap": dict(Counter(
            r["POTENTIAL_SLOT_REMAP"] for r in mat_rows)),
        "matrix_pairs_with_unknown_body": sum(
            1 for r in mat_rows
            if r["body_a"] == "UNKNOWN" or r["body_b"] == "UNKNOWN"),
        "csv_rows": {"04_PARTS_CATALOG.csv": n_cat,
                     "05_SLOT_PARTITION_MAP.csv": n_map,
                     "06_DIY_COMPATIBILITY_MATRIX.csv": n_mat},
    }

    payload = []
    for p in parts:
        q = {k: v for k, v in p.items() if not k.startswith("_")}
        q["nif_shapes"] = [
            {"nif_id": n["NIF_ID"], "source_mod": n["source_mod"],
             "nif_class": n["nif_class"], "stage_a_cat": n["stage_a_cat"],
             "shape_count": n["shape_count"], "has_skin": n["has_skin"],
             "has_smp": n["has_smp"], "smp_reason": n["smp_reason"],
             "shapes": n.get("shapes") or []}
            for n in p["_nif_rows"]]
        # NIF-internal texture slots are kept here for traceability: the
        # mandated texture_set_paths column comes from the ARMA instead.
        q["nif_texture_slots"] = p["_nif_textures"]
        payload.append(q)
    C.write_json(os.path.join(C.DATA, "04_parts.json"),
                 {"stats": stats, "parts": payload})
    C.log("wrote data/P00_RERUN/04_parts.json")

    for label, data in (("part_category",
                         Counter(p["part_category"] for p in parts)),
                        ("nif_resolved",
                         Counter(p["nif_resolved"] for p in parts)),
                        ("nif_link_source",
                         Counter(p["_link_src"] for p in parts)),
                        ("slot_source",
                         Counter(p["slot_source"] for p in parts)),
                        ("n_arma_refs",
                         Counter(p["n_arma_refs"] for p in parts)),
                        ("worn_mesh_provenance",
                         Counter(
                             "game" if p["_n_game_nifs"]
                             else "pending" if p["_n_pending"]
                             else "no_arma" for p in parts)),
                        ("body_candidate",
                         Counter(p["body_candidate"] for p in parts)),
                        ("physics", Counter(p["physics"] for p in parts)),
                        ("diy_status",
                         Counter(r["status"] for r in mat_rows))):
        C.log("--- " + label + " --- " + ", ".join(
            str(k) + "=" + str(v) for k, v in data.most_common()))
    C.log("unique PART_ID: " + str(len(set(ids))) + "/" + str(len(ids))
          + "   unique pair_id: " + str(len(set(pair_ids))) + "/"
          + str(len(pair_ids)))
    C.log("total time " + "%.1f" % (time.time() - t0) + "s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())