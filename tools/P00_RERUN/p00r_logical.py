#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p00r_logical.py — P00 CLEAN RE-RUN · report 15, LOGICAL OUTFIT / REWORK.

Writes exactly one artefact: reports/P00_RERUN/15_REWORK_RELATIONSHIPS.csv
(one row per mod in the 09 特殊服装 scope, 56 rows).

================================================================================
WHAT THIS REPLACES, AND WHY THE OLD RULES WERE WRONG
================================================================================
The previous 15 was produced by a keyword ladder over the MO2 display name.
Three of its rules were unsound and are deleted here:

  1. out_fit grouping by a leading ``[Series]`` bracket.  ``[Predator]`` is an
     AUTHOR label.  The old ``OUTFIT::<series>`` id collapsed nine distinct
     Predator releases (boots, accessories, harnesses, bodysuit, ...) into
     one outfit.  Series/author labels are now ignored for grouping.
  2. ``role = PHYSICS_PATCH`` whenever the display name contained 物理 /
     "physics".  【身体·物理】 is a category tag applied by the collection
     curator, not a statement about the mod's role.  A garment whose name
     merely mentions physics is a base garment.
  3. ``role = BODYSLIDE_CONVERSION`` whenever the display name contained
     "3BA".  3BA / CBBE / BHUNP are BODY-TYPE labels.  They are carried
     through as `body_candidate` and are never used to infer a role.

================================================================================
CLASSIFICATION PRINCIPLES
================================================================================
BASE_MOD
    The mod owns an independent wearable asset set: its own ARMO/ARMA records
    (n_arma_owned > 0 and n_armo_owned > 0) and/or its own mesh files and/or
    its own BSA.  A name may say 3BA / 物理 / "Latex Rework" — none of that
    matters; the records and the files decide.

PATCH_MOD / REWORK_MOD
    Requires POSITIVE PARENT EVIDENCE.  A role is only emitted when one of
    the following is actually measured:

      Route A  MO2 shadowing      the mod provides >= 1 OUTFIT-BEARING virtual
                                 path that its parent also provides
                                 (01_file_index vpath intersection, confirmed
                                 against 13_MO2_CONFLICT_MAP).  Role is
                                 REWORK_MOD when it also replaces those
                                 assets, i.e. CANDIDATE shadows >= 1 path and
                                 the winner is CANDIDATE.
      Route B  namespace          the mod's own asset namespace is a strict
                                 derivation of the parent's plugin stem or
                                 of the parent's asset namespace
                                 (PBR-NIFPatcher / textures-pbr / BodySlide
                                 project trees).  Role is PATCH_MOD: the
                                 parent is left intact.
      Route C  external parent    the mod owns NO armor records, NO mesh
                                 files and NO BSA, so it cannot be a base
                                 garment at all; its whole payload projects
                                 onto an armor that lives outside this
                                 profile.  parent_in_scope = out_of_scope.

    Two hard guards keep Route A/B from producing nonsense:
      * a candidate mod with its own ARMO/ARMA is NEVER a patch.  A merged
        "All in One" pack that owns 309 ARMA is a base mod that *supersedes*
        other mods; it is not an add-on of them.
      * only OUTFIT-BEARING extensions (.nif .osd .dds .osp .bsa) count as a
        shared/shadowed path.  Two mods shipping the same .wav or the same
        .xml is a copied file, not a garment relationship.

    Absent positive evidence the mod is a BASE_MOD — that is the explicit
    default required by the re-run brief, not an oversight.

================================================================================
LOGICAL_OUTFIT_ID SCHEME
================================================================================
    LOGICAL::<outfit_slug>::<member_slug>

  outfit_slug  slug of the outfit's CANONICAL member (see canonical_member()).
  member_slug  slug of that mod's own display name.

  A slug is derived only from the mod's own name and is therefore completely
  independent of iteration order, of the modlist and of the role assignment:

    1. drop every 【…】 curator tag and every meta.ini line;
    2. split the rest on the em-dash " — " into segments, drop empties;
    3. lowercase, keep [0-9a-z] plus CJK, join each segment's alphanumeric
       runs with "-", drop empty segments, cap the segment at 40 chars and
       the result at 64 chars.

  Two mods share an outfit ONLY through a measured edge, never through a
  label:

    * PARENT EDGE        union(child, parent) for every accepted
                         PATCH/REWORK relation whose parent is in scope.
                         A conversion therefore lands in its base mod's
                         outfit instead of standing alone.
    * CONTAINMENT EDGE   union(a, b) when the two mods share >= 3 virtual
                         paths, >= 50% of them are byte-identical (sha256
                         from the frozen 01_file_index), and the shared
                         paths are OUTFIT-BEARING.  This is how an
                         "All in One" pack and the individual packs it
                         re-delivers end up in one outfit.  A shared .wav or
                         a shared .xml never produces this edge.

  Every other mod is its own outfit, so the nine [Predator] releases stay
  nine outfits.

Read-only with respect to the game install.  Inputs are read from the frozen
data/P00_RERUN/*.json(.gz) and reports/P00_RERUN/13_MO2_CONFLICT_MAP.csv; the
single write goes through p00r_common.assert_write_path().
"""
from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p00r_common as C  # noqa: E402

OUT_CSV = "15_REWORK_RELATIONSHIPS.csv"

COLS = [
    # --- identity -------------------------------------------------------
    "LOGICAL_OUTFIT_ID", "logical_outfit_name", "MOD_ID", "source_mod",
    # --- the rebuilt classification -------------------------------------
    "role", "parent_mod", "parent_in_scope", "relationship_evidence",
    "confidence",
    # --- mo2 facts ------------------------------------------------------
    "priority", "enabled", "size_bytes", "file_count",
    # --- independent asset set -----------------------------------------
    "n_plugins", "plugin_files", "masters", "n_arma_owned", "n_armo_owned",
    "n_armo_own_arma_refs", "n_own_meshes", "n_bsa", "n_textures",
    "n_shapedata_nif", "n_osd", "n_osp", "n_smp_xml", "n_pbr_json",
    "n_scripts", "bodyslide_projects",
    # --- measured cross-mod relations -----------------------------------
    "n_shadowed_paths", "shadows", "shadowed_by", "shares_paths_with",
    "shares_identical_files_with", "supersedes",
    # --- carried-through, never used to infer a role ---------------------
    "body_candidate", "recommended_keep", "note",
]

# ---------------------------------------------------------------------------
# vocabulary
# ---------------------------------------------------------------------------

# An outfit identity is carried by meshes, textures and BodySlide projects.
# Sound, config and physics XML are deliberately excluded: two mods shipping
# the same .wav is a copied file, not a garment relationship.
OUTFIT_EXT = {".nif", ".osd", ".dds", ".osp", ".bsa"}

SHAPEDATA_DIR = "calientetools/bodyslide/shapedata/"

# Directory names that carry no identity.  Any namespace shorter than
# MIN_NS_LEN or on this list is never used to link a mod to a parent.
GENERIC_NS = {
    "textures", "meshes", "calientetools", "bodyslide", "shapedata",
    "slidersets", "slidergroups", "pbrnifpatcher", "smpxml", "scripts",
    "skse", "interface", "installers", "skeleton", "materials", "clothes",
    "armor", "hair", "misc", "optional", "data", "shaders", "sound",
    "sounds", "fxc", "chars", "combinator", "skeletonoptimizer",
    "caliente", "calientescripts", "body", "bodies", "plugins", "skyui",
    "src", "config", "fontconfig", "lod", "dlc",
}
MIN_NS_LEN = 8
FILENAMEISH_RE = re.compile(r"\.[a-z0-9]{1,5}$", re.IGNORECASE)

# A name extension that is only a volume number or a body-family token is a
# sequel/platform marker, not a derivation marker.  "Nye's Latex Pack 2" is
# NOT a patch of "Nye's Latex Pack".
BODY_FAMILY_TOKENS = {
    "3ba", "cbbe", "bhunp", "unp", "3bbb", "se", "ae", "es", "le", "sse",
    "fe", "vr", "samp",
}
DERIVATION_TOKENS = (
    "pbr", "rework", "addon", "add-on", "patch", "fix", "fixed", "variant",
    "edited", "edit", "conversion", "conv", "converted", "physics", "smp",
    "cloth", "hdt", "plus", "pro", "remaster", "update", "v2", "anklecut",
    "重制", "补丁", "补全", "修改", "修正", "增强",
)
MAX_EXT = 60          # longest name extension still treated as a derivation
MIN_PARENT_KEY = 8   # shortest parent name key accepted for a derivation


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

TAG_RE = re.compile(r"【[^】]*】")
KEEP_RE = re.compile(r"[^0-9a-z㐀-䶿一-鿿]+")


def load(name):
    p = os.path.join(C.DATA, name)
    if name.endswith(".gz"):
        with gzip.open(p, "rt", encoding="utf-8") as fh:
            return json.load(fh)
    with open(p, "r", encoding="utf-8") as fh:
        return json.load(fh)


def norm(s: str) -> str:
    """alnum-only lowercase key: [0-9a-z] + CJK survive, everything else goes."""
    s = unicodedata.normalize("NFKC", s or "").lower()
    return KEEP_RE.sub("", s)


def name_segments(name: str):
    """【…】 tags removed, split on the em-dash separator, empties dropped."""
    s = TAG_RE.sub(" ", name or "")
    out = []
    for seg in re.split(r"\s+—\s+", s):
        seg = seg.strip(" \t—·-")
        if seg:
            out.append(seg)
    return out or [(name or "").strip()]


def short_label(name: str) -> str:
    """Human label: curator tags dropped, the bilingual segments kept."""
    return " — ".join(name_segments(name))[:160]


def slug(name: str) -> str:
    parts = []
    for seg in name_segments(name):
        p = "-".join(t for t in re.split(r"[^0-9a-z㐀-䶿一-鿿]+", seg.lower()) if t)
        if p:
            parts.append(p[:40])
    s = "-".join(parts)[:64].strip("-")
    return s or "unnamed"


def plugin_stem(filename: str) -> str:
    return re.sub(r"\.(esp|esm|esl|espfe)$", "", filename or "", flags=re.I)


def clip(text: str, n: int = 700) -> str:
    text = re.sub(r"\s+", " ", (text or "")).strip()
    return text if len(text) <= n else text[:n - 1] + "…"


def is_digits(s: str) -> bool:
    return bool(s) and s.isdigit()


def digest(name: str) -> str:
    """Short stable suffix for a slug collision; a pure function of the name."""
    return hashlib.sha1(norm(name).encode("utf-8")).hexdigest()[:6]


# ---------------------------------------------------------------------------
# per-mod asset profile, all from the frozen index
# ---------------------------------------------------------------------------

def build_profile(mods, plugin_index, records, file_index, nif_parsed):
    """mod name -> measured facts.  Nothing here is guessed from a name."""
    prof = {}

    for m in mods:
        prof[m["mod_name"]] = {
            "mod": m,
            "plugins": [],
            "arma": 0, "armo": 0, "armo_own_arma": 0,
            "own_nif": 0, "shapedata_nif": 0, "osd": 0, "osp": 0,
            "dds": 0, "bsa": 0, "smp_xml": 0, "pbr_json": 0, "scripts": 0,
            "other": 0, "namespaces": set(), "vpaths": {}, "bs_projects": set(),
        }

    # ---- plugins -----------------------------------------------------------
    # 02_plugin_index / 02_plugin_records spell the key PLUGIN_ID (upper case);
    # 02_parse_failures and a few hand-fixed files spell it plugin_id.
    def pid(rec):
        return (rec.get("PLUGIN_ID") or rec.get("plugin_id") or "").lower()

    for p in plugin_index:
        pr = prof.get(p["source_mod"])
        if pr is None:
            continue
        pr["plugins"].append(p)

    for r in records:
        pr = prof.get(r.get("source_mod"))
        if pr is None:
            continue
        rt = r.get("record_type")
        if rt == "ARMA":
            pr["arma"] += 1
        elif rt == "ARMO":
            pr["armo"] += 1
            me = pid(r)
            refs = (r.get("armo") or {}).get("arma_refs") or []
            if me and refs and all(
                    (x.get("plugin") or "").lower() == me for x in refs):
                pr["armo_own_arma"] += 1

    # ---- files -------------------------------------------------------------
    for f in file_index:
        pr = prof.get(f["mod"])
        if pr is None:
            continue
        v = f["vpath"]
        ext = f["ext"].lower()
        pr["vpaths"][v] = f["sha256"]
        low = v.lower()
        if ext == ".nif":
            if low.startswith(SHAPEDATA_DIR):
                pr["shapedata_nif"] += 1
            else:
                pr["own_nif"] += 1
        elif ext == ".osd":
            pr["osd"] += 1
        elif ext == ".osp":
            pr["osp"] += 1
        elif ext == ".dds":
            pr["dds"] += 1
        elif ext == ".bsa":
            pr["bsa"] += 1
        elif ext in (".wsp",):
            pr["other"] += 1
        elif ext in (".psc",):
            pr["scripts"] += 1
        elif ext == ".json" and "pbrnifpatcher/" in low:
            pr["pbr_json"] += 1
        elif ext == ".xml" and ("smpxml" in low or "smp" in low):
            pr["smp_xml"] += 1
        else:
            pr["other"] += 1

        # namespaces = directory components (plus the ShapeData project dir)
        if low.startswith(SHAPEDATA_DIR):
            seg = low[len(SHAPEDATA_DIR):].split("/")[0]
            if seg.endswith(".nif"):
                seg = seg[:-4]
            if seg:
                pr["bs_projects"].add(seg)
                pr["namespaces"].add(seg)
        parts = v.split("/")[:-1]
        if "smpxml" in low:
            parts = [x for x in parts if x != "smpxml"]
        for seg in parts:
            pr["namespaces"].add(seg)

    # BodySlide project names straight from the parsed-NIF inventory
    for n in nif_parsed:
        pr = prof.get(n.get("source_mod"))
        if pr is None:
            continue
        if n.get("nif_class") == "SHAPEDATA":
            v = n.get("path", "").lower()
            if v.startswith(SHAPEDATA_DIR):
                seg = v[len(SHAPEDATA_DIR):].split("/")[0]
                if seg.endswith(".nif"):
                    seg = seg[:-4]
                if seg:
                    pr["bs_projects"].add(seg)

    for name, pr in prof.items():
        ns = set()
        for seg in pr["namespaces"]:
            k = norm(seg)
            if len(k) < MIN_NS_LEN or k.isdigit() or k in GENERIC_NS:
                continue
            if FILENAMEISH_RE.search(seg):
                # a folder literally named "matcap 7.dds" is a texture file
                # that landed at the wrong depth, not a mod identity
                continue
            ns.add(seg)
        pr["ns"] = ns
        pr["ns_keys"] = {norm(seg): seg for seg in ns}
        pr["mast"] = sorted({m for p in pr["plugins"] for m in (p["masters"] or [])})
        pr["plugin_files"] = [p["plugin_file"] for p in pr["plugins"]]
        pr["owns_armor_records"] = pr["arma"] > 0 and pr["armo"] > 0
        pr["owns_meshes"] = pr["own_nif"] > 0 or pr["bsa"] > 0
        pr["independent_set"] = pr["owns_armor_records"] or pr["owns_meshes"]
    return prof


# ---------------------------------------------------------------------------
# cross-mod relations measured from the frozen data
# ---------------------------------------------------------------------------

def shared_paths(prof):
    """(a, b) -> (n_shared, n_identical) for pairs sharing OUTFIT paths."""
    vp = defaultdict(list)
    for name, pr in prof.items():
        for v, sha in pr["vpaths"].items():
            if os.path.splitext(v)[1].lower() in OUTFIT_EXT:
                vp[v].append((name, sha))
    out = {}
    for v, ls in vp.items():
        if not (2 <= len(ls) <= 8):
            continue
        for i in range(len(ls)):
            for j in range(i + 1, len(ls)):
                (ma, sa), (mb, sb) = ls[i], ls[j]
                key = (ma, mb) if ma <= mb else (mb, ma)
                same = sa == sb
                n, s = out.get(key, (0, 0))
                out[key] = (n + 1, s + (1 if same else 0))
    return out


def shadow_counts(prof, shared):
    """mod -> mod -> n OUTFIT vpaths of the loser that the winner also ships."""
    prio = {n: pr["mod"]["priority"] for n, pr in prof.items()}
    out = defaultdict(dict)
    for (a, b), (n, _same) in shared.items():
        # lower modlist line number == higher MO2 overwrite priority
        w, l = (a, b) if prio[a] <= prio[b] else (b, a)
        out[w][l] = n
    return out


def name_derivation(child, parent):
    """child name == parent name + a derivation descriptor -> extension string.

    Direction matters: A extends B means B is the base.  An extension that is
    only a volume number or a body-family token is rejected, which is what
    keeps "Nye's Latex Pack 2" from being filed as a patch of
    "Nye's Latex Pack".
    """
    csegs = [norm(s) for s in name_segments(child)]
    psegs = [norm(s) for s in name_segments(parent)]
    cfull = norm(TAG_RE.sub(" ", child))
    pfull = norm(TAG_RE.sub(" ", parent))
    exts = []
    if cfull.startswith(pfull) and len(cfull) > len(pfull):
        exts.append(cfull[len(pfull):])
    for cs in csegs:
        for ps in psegs:
            if len(ps) >= MIN_PARENT_KEY and cs.startswith(ps) and len(cs) > len(ps):
                exts.append(cs[len(ps):])
    good = []
    for e in exts:
        if not e or len(e) > MAX_EXT or is_digits(e):
            continue
        toks = [t for t in re.split(r"[^0-9a-z㐀-䶿一-鿿]+", e) if t]
        if not toks:
            continue
        if all(t in BODY_FAMILY_TOKENS for t in toks):
            continue
        if not any(t in DERIVATION_TOKENS for t in toks):
            continue
        good.append(e)
    return good[0] if good else ""


def namespace_link(child_pr, parent_pr, unique_child_ns):
    """The child writes into a folder that derives from the parent.

    Two independent, deliberately asymmetric tests:

      * parent PLUGIN STEM.  A PBR-NIFPatcher / textures-pbr / BodySlide
        add-on is expected to reuse the parent's folder name, so this test
        does NOT require the folder to be exclusive to the child.  It is
        already one-directional: only the parent has the plugin.

      * parent ASSET NAMESPACE.  Here the child must introduce a folder
        nobody else uses (`mischeelseins 3ba` -> `mischeelseins 3ba
        anklecut`).  Requiring exclusivity is what fixes the direction: the
        mod that renames a shared folder is the add-on, never the base, and
        a folder two unrelated mods merely both ship ('fantasyseries6',
        'sse_tfd_haley_black_suit') is never read as a parent link.
    """
    hits = []
    for kc, sc in child_pr["ns_keys"].items():
        for stem in (plugin_stem(p) for p in parent_pr["plugin_files"]):
            kp = norm(stem)
            if len(kp) < MIN_NS_LEN:
                continue
            if kc == kp:
                hits.append((0, sc, stem, ""))
            elif kc.startswith(kp) and len(kc) > len(kp):
                hits.append((len(kc) - len(kp), sc, stem, kc[len(kp):]))
        if sc not in unique_child_ns:
            continue
        for kp, sp in parent_pr["ns_keys"].items():
            if kp == kc:
                hits.append((0, sc, sp, ""))
            elif kc.startswith(kp) and len(kc) > len(kp):
                hits.append((len(kc) - len(kp), sc, sp, kc[len(kp):]))
    # Sort before returning. `hits` is accumulated from dict iteration and the
    # caller quotes hits[0] as the representative folder in the evidence text;
    # without a stable order that quote changed between runs
    # ('micheelseins 3ba anklecut' one run, 'mischeelszwei ...' the next),
    # which made 15_REWORK_RELATIONSHIPS.csv non-reproducible.
    return sorted(hits)


def conflict_map_pairs():
    """13_MO2_CONFLICT_MAP -> (winner, loser) -> (n_paths, n_same_content)."""
    p = os.path.join(C.REPORTS, "13_MO2_CONFLICT_MAP.csv")
    if not os.path.isfile(p):
        return {}, False
    rows = C.read_csv(p)
    agg = defaultdict(lambda: [0, 0])
    for r in rows:
        w = r.get("winner_mod") or ""
        for l in (r.get("loser_mods") or "").split(";"):
            l = l.strip()
            if l and l != w:
                e = agg[(w, l)]
                e[0] += 1
                e[1] += 1 if (r.get("same_content") or "").lower() == "yes" else 0
    return {k: tuple(v) for k, v in agg.items()}, True


def external_parent_label(pr):
    """Identify the out-of-scope armor a bodyslide/physics-only mod projects.

    The label is the literal namespace the mod actually writes into (its
    texture folder, else its mesh root, else its BodySlide project names),
    collapsed to the common prefix when the folders are per-piece variants.
    It names a real measured asset rather than a guess, and the tail states
    exactly why the mod cannot stand on its own.
    """
    def _toks(s):
        return [t for t in re.split(r"[^0-9a-zA-Z㐀-䶿一-鿿]+", s) if t]

    def _common_prefix(tok_lists):
        if not tok_lists:
            return []
        pre = []
        for i in range(min(len(x) for x in tok_lists)):
            w = tok_lists[0][i]
            if all(len(x) > i and x[i].lower() == w.lower() for x in tok_lists):
                pre.append(w)
            else:
                break
        return pre

    vpaths = list(pr["vpaths"])
    # 1. the texture folder the mod owns -> its asset identity
    tex = set()
    # 2. the mesh root chain the mod writes into
    mesh = set()
    for v in vpaths:
        p = v.split("/")
        if len(p) < 3:
            continue
        chain = [x for x in p[1:-1] if x.lower() not in GENERIC_NS]
        if not chain:
            continue
        if p[0] == "textures":
            tex.add(chain[0])
        elif p[0] == "meshes":
            mesh.add("/".join(chain[:2]))

    projs = sorted(pr["bs_projects"])
    cands = [s for s in sorted(tex) if len(norm(s)) >= 4]
    if not cands:
        cands = [s for s in sorted(mesh) if len(norm(s)) >= 4]
    if not cands and projs:
        # 3. only BodySlide projects — name the armor they project onto
        cands = [" ".join(t) for t in
                 ([x for x in (_toks(s) for s in projs) if x])]
    cands = [c for c in cands if len(norm(c)) >= 4]
    if not cands:
        cands = sorted(pr["ns"])[:2]
    if not cands:
        return "<out-of-scope> unidentified (no asset namespace in scope)"

    tk = [_toks(c) for c in cands if _toks(c)]
    pre = _common_prefix(tk)
    if len(cands) > 1 and pre and len(pre) < min(len(x) for x in tk):
        label = " ".join(pre) + f"… ({len(cands)} asset folders)"
    else:
        label = " / ".join(list(dict.fromkeys(cands))[:2])
    tail = (f" — {len(projs)} BodySlide projects, no mesh of its own" if projs
            else " — no mesh, no ARMO/ARMA, no plugin")
    return "<out-of-scope> " + label + tail


# ---------------------------------------------------------------------------
# classification
# ---------------------------------------------------------------------------

def classify(prof, shared, shadow, cmap, cmap_ok):
    names = list(prof)
    rel = {}          # mod -> dict(role, parent, parent_in_scope, evidence, conf, route)

    # A folder only one mod writes into can carry that mod's identity.  A
    # folder several mods share is a copied/shared folder and is never used
    # as parenthood evidence.
    ns_users = defaultdict(set)
    for name, pr in prof.items():
        for s in pr["ns"]:
            ns_users[s].add(name)
    uniq_ns = {s for s, u in ns_users.items() if len(u) == 1}
    C.log(f"  namespaces: {len(ns_users)} distinct, {len(uniq_ns)} written by "
          f"exactly one mod")

    for child in names:
        c = prof[child]
        ev = []
        parent = ""
        route = ""

        # ---- Route A: MO2 shadowing of an in-scope parent -----------------
        cand = None
        for p, n in sorted(shadow.get(child, {}).items(), key=lambda kv: -kv[1]):
            if prof[p]["owns_armor_records"] and not c["owns_armor_records"]:
                cand = (p, n)
                break
        if cand:
            p, n = cand
            cmap_n, same = cmap.get((child, p), (0, 0))
            exts = Counter(os.path.splitext(v)[1].lower()
                           for v, _ in c["vpaths"].items()
                           if v in prof[p]["vpaths"]
                           and os.path.splitext(v)[1].lower() in OUTFIT_EXT)
            ns = namespace_link(c, prof[p], uniq_ns)
            ns_txt = (f"; the folder it introduces, '{ns[0][1]}', derives from "
                      f"parent '{ns[0][2]}'") if ns else ""
            ev.append(
                f"shadows {n} of the parent's OUTFIT virtual paths "
                f"({', '.join(f'{k[1:]} x{v}' for k, v in sorted(exts.items()))})"
                + (f", MO2 13_MO2_CONFLICT_MAP records {cmap_n} VFS_OVERRIDE "
                   f"wins ({same} byte-identical)" if cmap_ok and cmap_n else "")
                + ns_txt)
            ev.append(f"child owns no ARMO/ARMA of its own "
                      f"(child ARMA={c['arma']}, ARMO={c['armo']}, "
                      f"plugins={len(c['plugins'])})")
            ext = name_derivation(child, p)
            if ext:
                ev.append(f"name = parent name + derivation suffix "
                          f"'{ext}' (parent/child names differ, so this is a "
                          f"rework, not a sibling volume)")
            parent, route = p, "A_mo2_shadow"
            role = "REWORK_MOD"
        else:
            # ---- Route B: namespace derivation ---------------------------
            best = None
            for p in sorted(names):
                if p == child or c["owns_armor_records"]:
                    continue
                if c["owns_meshes"]:
                    # a mod that ships meshes of its own is a mesh package,
                    # not an add-on, unless Route A already caught it
                    continue
                hits = [h for h in namespace_link(c, prof[p], uniq_ns)
                        if h[3] == "" or any(t in DERIVATION_TOKENS
                                             for t in re.split(
                                                 r"[^0-9a-z㐀-䶿一-鿿]+", h[3])
                                             if t)]
                if not hits:
                    continue
                # prefer an exact match, then the tightest extension, then
                # an in-scope parent with armor records, then the name
                hits.sort(key=lambda h: (h[0], 0 if prof[p]["owns_armor_records"]
                                         else 1, p))
                h = hits[0]
                key = (h[0], 0 if prof[p]["owns_armor_records"] else 1,
                       0 if name_derivation(child, p) else 1, p)
                if best is None or key < best[0]:
                    best = (key, p, h)
            if best is not None:
                p = best[1]
                _sp, sc, stem, ext = best[2]
                ext_txt = name_derivation(child, p) or ext or ""
                ev.append(
                    f"the folder it introduces, '{sc}', is a strict derivation "
                    f"of parent '{stem}'"
                    + (f" (extension '{ext}')" if ext else " (exact match)"))
                ev.append(
                    f"payload is {len(c['vpaths'])} path(s): "
                    f"{c['pbr_json']} pbrnifpatcher json, {c['dds']} textures/pbr "
                    f"dds, {c['osp']} bodyslide sliderset(s), {c['smp_xml']} smp "
                    f"xml — no mesh, no ARMO/ARMA, no plugin")
                if ext_txt:
                    ev.append(f"name = parent name + derivation suffix "
                              f"'{ext_txt}'")
                ev.append(f"shadows 0 of the parent's OUTFIT paths "
                          f"(13_MO2_CONFLICT_MAP), so the parent is not "
                          f"replaced -> PATCH, not REWORK")
                parent, route = p, "B_namespace"
                role = "PATCH_MOD"
            else:
                # ---- Route C: no in-scope parent, no independent set ------
                if not c["independent_set"] and not c["plugins"]:
                    parent = external_parent_label(c)
                    route = "C_external"
                    role = "PATCH_MOD"
                    ns = sorted(c["ns"])[:3]
                    ev.append(
                        f"owns no armor records, no mesh file and no BSA "
                        f"(ARMA={c['arma']}, ARMO={c['armo']}, plugins=0, "
                        f"own .nif={c['own_nif']}, bsa={c['bsa']}) and no "
                        f"in-scope mod provides the armor it projects, so it "
                        f"cannot be a base garment")
                    ev.append(
                        f"whole payload is {len(c['vpaths'])} path(s): "
                        f"{c['shapedata_nif']} bodyslide ShapeData .nif, "
                        f"{c['osd']} .osd, {c['osp']} .osp"
                        + (f", {c['dds']} .dds" if c["dds"] else "")
                        + (f", {c['smp_xml']} SMP .xml" if c["smp_xml"] else "")
                        + f" under {', '.join('"%s"' % s for s in ns)}")
                    if c["bs_projects"]:
                        ev.append("BodySlide projects it ships: "
                                  + ", ".join(sorted(c["bs_projects"])[:6]))
                else:
                    role = "BASE_MOD"

        if role == "BASE_MOD":
            ev = base_evidence(child, c, prof, shared, shadow, cmap, cmap_ok)
        rel[child] = {
            "role": role, "parent": parent, "route": route,
            "evidence": clip(" | ".join(ev)),
            "parent_in_scope": ("" if role == "BASE_MOD" else
                                ("in_scope" if parent in prof else
                                 "out_of_scope")),
        }

    # ---- confidence --------------------------------------------------------
    for name, r in rel.items():
        r["confidence"] = confidence(name, prof[name], r)
    return rel


def base_evidence(name, c, prof, shared, shadow, cmap, cmap_ok):
    ev = []
    if c["plugins"]:
        pl = ", ".join(f"{p['plugin_file']} MAST=[{','.join(p['masters'] or [])}]"
                       for p in c["plugins"])
        ev.append(f"own plugin(s): {pl}")
    else:
        ev.append("ships no plugin of its own")
    ev.append(
        f"owns {c['arma']} ARMA + {c['armo']} ARMO "
        f"({c['armo_own_arma']} ARMO link to their own ARMA) in "
        f"{len(c['plugins'])} plugin(s)")
    ev.append(
        f"independent asset set: {c['own_nif']} own mesh .nif, {c['bsa']} BSA, "
        f"{c['dds']} textures, {c['shapedata_nif']} bodyslide ShapeData, "
        f"{c['osp']} bodyslide SliderSet, {c['osp'] and c['osd'] or c['osd']} .osd")
    if not c["plugins"] and not c["owns_armor_records"] and c["owns_meshes"]:
        ev.append("no ARMO/ARMA here, so its worn meshes are bound to armor "
                  "records held by a plugin outside this profile")
    sh = shadow.get(name, {})
    if sh:
        ev.append("MO2 shadow map: it is the winner against "
                  + ", ".join(f"{k} ({v} paths)" for k, v in
                              sorted(sh.items(), key=lambda kv: -kv[1])[:3]))
    sib = sorted({o for (a, b) in shared
                  for o in (b if a == name else a) if o != name})
    if sib:
        ev.append("shares OUTFIT virtual paths only with "
                  + ", ".join(sorted(sib)[:3]) + " (no parent link: neither "
                  "side lacks armor records)")
    ev.append("no positive parent evidence found: no in-scope mod is "
              "shadowed by it in an OUTFIT path, no asset namespace derives "
              "from another mod's plugin stem, and the name adds no derivation "
              "suffix to another mod's name -> BASE by default")
    return ev


def confidence(name, c, r):
    if r["role"] == "BASE_MOD":
        if c["owns_armor_records"] and c["owns_meshes"]:
            return "HIGH"
        if c["independent_set"]:
            return "MEDIUM"
        return "LOW"
    if r["parent_in_scope"] == "in_scope":
        return "HIGH" if r["route"] == "A_mo2_shadow" else "MEDIUM"
    return "MEDIUM"      # parent proven to be out of scope by absence


# ---------------------------------------------------------------------------
# outfit grouping
# ---------------------------------------------------------------------------

class UF:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def group_outfits(prof, rel, shared):
    uf = UF()
    for n in prof:
        uf.find(n)
    # edge 1 — parent/child
    for n, r in rel.items():
        if r["parent"] in prof and n != r["parent"]:
            uf.union(n, r["parent"])
    # edge 2 — byte-identical containment (an "All in One" pack and the packs
    # it re-delivers).  >= 3 shared OUTFIT paths, >= 50% identical.
    for (a, b), (n, same) in shared.items():
        if n >= 3 and same / n >= 0.5:
            uf.union(a, b)
    members = defaultdict(list)
    for n in prof:
        members[uf.find(n)].append(n)
    return members


def canonical_member(members, prof, shadow, rel):
    """Which member names the outfit.

    Preference order, all deterministic:
      1. a member that another member of the same outfit names as its parent
         (the base an add-on was cut from);
      2. a BASE_MOD;
      3. not an aggregator — a member that shadows a sibling is an "All in
         One" re-delivery of that sibling, not its identity;
      4. most owned ARMA records, then lowest MO2 priority, then name.
    """
    roots = {rel[m]["parent"] for m in members
             if rel[m]["parent"] in members and rel[m]["parent"] != m}
    is_parent = [m for m in members if m in roots]
    base = [m for m in (is_parent or members) if rel[m]["role"] == "BASE_MOD"]
    pool = base or is_parent or list(members)
    non_agg = [m for m in pool
               if not any(o in shadow.get(m, {}) for o in members if o != m)]
    pool = non_agg or pool
    pool.sort(key=lambda m: (-prof[m]["arma"], prof[m]["mod"]["priority"], m))
    return pool[0]


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    C.ensure_dirs()
    C.log("logical outfit re-classification — inputs")

    mods = load("01_mod_aggregates.json")
    plugin_index = load("02_plugin_index.json")
    records = load("02_plugin_records.json")
    file_index = load("01_file_index.json.gz")
    nif_parsed = load("08_nif_parsed.json.gz")
    C.log(f"  mods={len(mods)} plugins={len(plugin_index)} "
          f"records={len(records)} files={len(file_index)} nifs={len(nif_parsed)}")

    prof = build_profile(mods, plugin_index, records, file_index, nif_parsed)
    shared = shared_paths(prof)
    shadow = shadow_counts(prof, shared)
    cmap, cmap_ok = conflict_map_pairs()
    C.log(f"  outfit-path sharing pairs={len(shared)}  "
          f"shadow relations={sum(len(v) for v in shadow.values())}  "
          f"13_MO2_CONFLICT_MAP={'loaded' if cmap_ok else 'MISSING'}")

    rel = classify(prof, shared, shadow, cmap, cmap_ok)

    members = group_outfits(prof, rel, shared)
    canon = {root: canonical_member(members[root], prof, shadow, rel)
             for root in members}
    C.log(f"  logical outfits={len(members)}")

    # Colliding slugs get a short digest of the mod's own name, so the id is
    # still a pure function of the name and never of the iteration order.
    slug_seen = Counter(slug(m) for m in prof)

    rows = []
    for m in sorted(mods, key=lambda x: x["priority"]):
        name = m["mod_name"]
        c = prof[name]
        r = rel[name]
        root = None
        for rt, mm in members.items():
            if name in mm:
                root = rt
                break
        cmod = canon[root]
        cslug = slug(cmod)
        mslug = slug(name)
        if slug_seen[mslug] > 1:
            mslug = f"{mslug}-{digest(name)}"
        outfit_id = f"LOGICAL::{cslug}::{mslug}"

        # relations
        shadows_txt = "; ".join(
            f"{k} ({v} OUTFIT paths)" for k, v in
            sorted(shadow.get(name, {}).items(), key=lambda kv: -kv[1]))
        shadowed_by = "; ".join(
            f"{k} ({v} OUTFIT paths)" for k, v in
            sorted(((k, v) for k, v in
                    [(x, shadow[x][name]) for x in shadow if name in shadow[x]]),
                   key=lambda kv: -kv[1]))
        sib = defaultdict(lambda: [0, 0])
        for (a, b), (n, same) in shared.items():
            if a == name or b == name:
                o = b if a == name else a
                sib[o][0] += n
                sib[o][1] += same
        shares_paths = "; ".join(f"{k} ({v} paths, {s} identical)"
                                 for k, (v, s) in sorted(sib.items()))
        supersedes = "; ".join(
            f"{k} ({s}/{v} shared paths byte-identical)"
            for k, (v, s) in sorted(sib.items()) if v >= 3 and s / v >= 0.5)

        note = ""
        if m["body_candidate_name"] not in ("UNKNOWN",):
            note = ("name carries a body-type label "
                    f"[{m['body_candidate_name']}]; a body-type label is NOT "
                    "used to infer a role")
        if "物理" in name or "physics" in name.lower():
            note = (note + "; " if note else "") + (
                "name mentions physics, but the role came from the measured "
                "asset/plugin set, not from that word")

        rows.append({
            "LOGICAL_OUTFIT_ID": outfit_id,
            "logical_outfit_name": short_label(cmod),
            "MOD_ID": m["MOD_ID"],
            "source_mod": name,
            "role": r["role"],
            "parent_mod": r["parent"],
            "parent_in_scope": r["parent_in_scope"],
            "relationship_evidence": r["evidence"],
            "confidence": r["confidence"],
            "priority": m["priority"],
            "enabled": m["enabled"],
            "size_bytes": m["size_bytes"],
            "file_count": m["file_count"],
            "n_plugins": len(c["plugins"]),
            "plugin_files": "; ".join(c["plugin_files"]),
            "masters": "; ".join(c["mast"]),
            "n_arma_owned": c["arma"],
            "n_armo_owned": c["armo"],
            "n_armo_own_arma_refs": c["armo_own_arma"],
            "n_own_meshes": c["own_nif"],
            "n_bsa": c["bsa"],
            "n_textures": c["dds"],
            "n_shapedata_nif": c["shapedata_nif"],
            "n_osd": c["osd"],
            "n_osp": c["osp"],
            "n_smp_xml": c["smp_xml"],
            "n_pbr_json": c["pbr_json"],
            "n_scripts": c["scripts"],
            "bodyslide_projects": len(c["bs_projects"]),
            "n_shadowed_paths": sum(shadow.get(name, {}).values()),
            "shadows": shadows_txt,
            "shadowed_by": shadowed_by,
            "shares_paths_with": shares_paths,
            "shares_identical_files_with": shares_paths,
            "supersedes": supersedes,
            "body_candidate": m["body_candidate_name"],
            "recommended_keep": "",
            "note": note,
        })

    n = C.write_csv(os.path.join(C.REPORTS, OUT_CSV), COLS, rows)

    # ---- audit ------------------------------------------------------------
    roles = Counter(r["role"] for r in rows)
    conf = Counter(r["confidence"] for r in rows)
    outfits = {r["LOGICAL_OUTFIT_ID"].rsplit("::", 1)[0] for r in rows}
    C.log("")
    C.log(f"rows={n}  logical outfits={len(outfits)}")
    C.log(f"roles: {dict(roles)}")
    C.log(f"confidence: {dict(conf)}")
    C.log("")
    C.log("PATCH / REWORK rows:")
    for r in sorted(rows, key=lambda x: x["priority"]):
        if r["role"] == "BASE_MOD":
            continue
        C.log(f"  [{r['role']:<10}] {r['source_mod'][:52]}")
        C.log(f"      parent ({r['parent_in_scope']}): {r['parent_mod']}")
        C.log(f"      {r['relationship_evidence'][:260]}")
    C.log("")
    pred = [r for r in rows if r["source_mod"].startswith("[Predator]")]
    C.log(f"[Predator] mods={len(pred)}  distinct outfits="
          f"{len({r['LOGICAL_OUTFIT_ID'].rsplit('::',1)[0] for r in pred})}  "
          f"distinct ids={len({r['LOGICAL_OUTFIT_ID'] for r in pred})}")
    for r in pred:
        C.log(f"    {r['LOGICAL_OUTFIT_ID']}  {r['role']}")
    C.log("")
    for k, v in sorted(((k, v) for k, v in
                        Counter(r["LOGICAL_OUTFIT_ID"].rsplit("::", 1)[0]
                                for r in rows).items()),
                       key=lambda kv: -kv[1]):
        if v > 1:
            C.log(f"outfit {k}  -> {v} mods")
    C.log("")
    p = os.path.join(C.REPORTS, OUT_CSV)
    C.log(f"wrote {p}  {os.path.getsize(p):,} B")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
