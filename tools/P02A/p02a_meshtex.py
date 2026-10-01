# -*- coding: utf-8 -*-
"""P02A -- Game Mesh + Texture migration ledger for ZLJ_COMBAT_LATEX.

STRICT READ-ONLY DESIGN PHASE.  This script never writes into MO2, Skyrim or
any mod folder.  It only *plans* (COPY + REPOINT) and writes four CSV ledgers
into reports/P02A/.

Evidence model (frozen P00 set only, via p02a_common):
  * MO2 priority: LOWER number = higher priority = VFS winner.
  * GAME_MESH inventory comes from the frozen ARMO/ARMA reachability
    (p.parts[*].game_nif_paths) -- i.e. meshes the outfit plugin actually
    points at.
  * BODYSLIDE_OUTPUT inventory comes from the frozen BodySlide projects
    (p.bs_projects[*].output_nif) of the outfit's own OSP files, plus the
    frozen ARMA model slots that no OSP of that outfit produces.
  * Texture inventory is derived BACKWARDS: retained NIF -> BSShaderTextureSet
    -> DDS virtual path -> MO2 winning provider.

No fuzzy matching.  Anything not provable from the frozen set is UNKNOWN /
UNRESOLVED / REVIEW.
"""
import os
import re
import sys
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import p02a_common as C  # noqa: E402

OUT_DIR = os.path.join(ROOT, "reports", "P02A")

# ---- P02A policy constants -------------------------------------------------
VANILLA_ALLOWLIST = []          # frozen whitelist of provably-vanilla DDS: NONE
SHARED_ASSET_WHITELIST = []     # cross-outfit shared assets: NONE (P05 topic)


# ---------------------------------------------------------------- path utils
def bs(vp):
    """MO2 style backslash virtual path (case preserved as in the source)."""
    return str(vp or "").replace("/", "\\").strip().strip('"')


def ensure_root(vp, root="meshes"):
    s = bs(vp)
    if not s.lower().startswith(root + "\\"):
        s = root + "\\" + s
    return s


def bname(vp):
    return bs(vp).rsplit("\\", 1)[-1]


def dname(vp):
    parts = bs(vp).rsplit("\\", 1)
    return parts[0] if len(parts) > 1 else ""


def squeeze(s):
    """lowercase, keep [a-z0-9] only -- used for deterministic keyword tests."""
    return re.sub(r"[^a-z0-9]", "", str(s or "").lower())


# ------------------------------------------------------------ role classifier
# Documented, deterministic keyword rules (applied in this exact order).
# BBD "catsuit" naming convention handled first because the generic BODY
# keyword "catsuit"/"cat" would otherwise swallow hood / glove / leg variants.
BBD_RULES = (
    ("catsuith", "HOOD"),
    ("catsuita", "BODY"),
    ("catsuitg", "GLOVES"),
    ("catsuitl", "BOOTS"),
)

# Name-keyword evidence, tested in this exact order.  "specific" classes
# (ground / tail / coat / boots / gloves / mask) are decided from the mesh name
# first, then BODY, then HOOD -- HOOD last because mod folder names such as
# "AE_HoodST" would otherwise swallow every mesh of that outfit.
ROLE_KEYWORDS = (
    ("GROUND", ("gnd", "ground")),
    ("TAIL", ("tail",)),
    ("COAT", ("cape", "coat", "vail", "mant", "cloak", "corset")),
    ("BOOTS", ("boot", "feet", "foot", "shoe", "heel", "stocking", "ankle")),
    ("GLOVES", ("glove", "hand", "gauntlet", "wrist")),
    ("MASK", ("mask", "helm", "head", "muzzle", "gag", "ear", "hairacc")),
    ("BODY", ("body", "bodi", "torso", "cuirass", "leotard", "shirt",
              "suit", "catsuit", "catb", "catt", "3ba", "top")),
    ("HOOD", ("hood",)),
)

NAME_FIRST = ("GROUND", "TAIL", "COAT", "BOOTS", "GLOVES", "MASK")
EVIDENCE_FIRST = ("COAT", "BOOTS", "GLOVES", "MASK", "BODY")

SLOT_FALLBACK = {
    "body": "BODY",
    "forearms": "GLOVES",
    "hands": "GLOVES",
    "lowerleg": "BOOTS",
    "shield": "BODY",
    "chest": "BODY",
    "calves": "BOOTS",
    "thigh": "BODY",
    "pelvis": "BODY",
    "head": "MASK",
    "face": "MASK",
    "hair": "OTHER",
    "leftweapon": "OTHER",
    "rightweapon": "OTHER",
    "rightshoulder": "OTHER",
    "neck": "OTHER",
}

CBBE_SLOT_MESH_ROLE = {
    "body_1.nif": "BODY",
    "1stpersonbody_1.nif": "BODY",
    "gloves_1.nif": "GLOVES",
    "1stpersongloves_1.nif": "GLOVES",
    "boots_1.nif": "BOOTS",
}


def mesh_role(stem, edids="", slots=""):
    """Deterministic mesh_role.

    Evidence order (all exact substring tests on a [a-z0-9]-squeezed token,
    no fuzzy matching):
      1. BBD "catsuit" naming convention (h/a/g/l = hood/body/gloves/boots)
      2. ground-object / tail tokens in the mesh name
      3. specific part tokens (coat / boots / gloves / mask) in the mesh name
      4. the same specific tokens in the ARMA EDID / ShapeData shape names
      5. generic body tokens in the EDID / shape names
      6. generic body tokens, then hood, in the mesh name
      7. the ARMA armor slot (authoritative for body-part class)
    """
    s = squeeze(stem)
    raw = str(stem or "").lower()
    for pre, role in BBD_RULES:
        if s.startswith(pre):
            return role
    kws = dict(ROLE_KEYWORDS)
    if "gnd" in s or "ground" in s or s.endswith("go") or "_go" in raw:
        return "GROUND"
    for role in NAME_FIRST:
        if role == "GROUND":
            continue
        for k in kws[role]:
            if k in s:
                return role
    toks = [squeeze(x) for x in re.split(r"[;,\s]+", edids or "") if x.strip()]
    for role in EVIDENCE_FIRST:
        for e in toks:
            for k in kws[role]:
                if k in e:
                    return role
    for role in ("BODY", "HOOD"):
        for k in kws[role]:
            if k in s:
                return role
    for sl in (slots or "").split(";"):
        r = SLOT_FALLBACK.get(sl.strip().lower())
        if r:
            return r
    return "OTHER"


def studded_role(vp):
    b = bname(vp).lower()
    if b in CBBE_SLOT_MESH_ROLE:
        return CBBE_SLOT_MESH_ROLE[b]
    return mesh_role(b.rsplit(".nif", 1)[0])


# ------------------------------------------------------------------ pack maps
def build_pack_maps(p):
    """mod -> owning OUTFIT_ID list, plugin_file -> OUTFIT_ID."""
    mod_owner = collections.defaultdict(list)
    for oid in C.OUTFIT_IDS:
        for m in p.mods_of_outfit(oid):
            if oid not in mod_owner[m]:
                mod_owner[m].append(oid)
    plugin_owner = {C.OUTFITS[o]["plugin"]: o for o in C.OUTFIT_IDS}
    return mod_owner, plugin_owner


def parts_of(p, plugin_owner):
    out = collections.defaultdict(list)
    for r in p.parts:
        oid = plugin_owner.get(r.get("plugin_file"))
        if oid:
            out[oid].append(r)
    return out


def osp_rows_of(p, oid):
    """Winning BodySlide projects of one outfit, keyed by OSP virtual path."""
    mods = set(p.mods_of_outfit(oid))
    by_osp = collections.defaultdict(list)
    for pr in p.bs_projects:
        if pr.get("MOD_ID") in mods:
            by_osp[C.norm(pr["OSP_PATH"])].append(pr)
    winners = {}
    for ospk, rows in by_osp.items():
        wmod = p.winning_mod(ospk)
        win = None
        for r in rows:
            if r.get("MOD_ID") == wmod:
                win = r
                break
        winners[ospk] = (win, rows, wmod)
    return winners


# ------------------------------------------------------------------- helpers
def prov_str(p, vp):
    return ";".join(p.shadowed(vp))


def split_list(v):
    return [x.strip() for x in str(v or "").split(";") if x.strip()]


# =========================================================== 1. MESH LEDGER ==
MESH_HEADER = [
    "OUTFIT_ID", "mesh_class", "source_virtual_path", "source_provider",
    "winning_provider", "shadowed_providers", "priority", "mesh_role",
    "target_virtual_path", "sha256", "retain_decision", "exists_in_vfs",
    "arma_edids", "arma_slots", "bodyslide_osp", "notes",
]


def build_mesh_ledger(p, pmap, poown):
    rows = []
    collisions = []            # (target_norm, outfit_a, outfit_b)
    seen_target = {}           # target_norm -> (outfit, source)
    used_names = collections.defaultdict(dict)   # outfit -> basename -> source
    per_outfit = collections.defaultdict(lambda: collections.Counter())

    for oid in C.OUTFIT_IDS:
        mods = set(p.mods_of_outfit(oid))
        ps = pmap.get(oid, [])
        ospw = osp_rows_of(p, oid)
        osp_out_vpaths = set()
        osp_out_by_norm = {}
        for ospk, (win, _rows, wmod) in sorted(ospw.items()):
            if win is not None and wmod in mods:
                on = ensure_root(win.get("output_nif") or "", "meshes")
                osp_out_vpaths.add(C.norm(on))
                osp_out_by_norm[C.norm(on)] = win

        # ---- A. GAME_MESH : ARMO/ARMA reachable -------------------------
        ref_meta = collections.defaultdict(lambda: {"edids": set(), "slots": set()})
        for r in ps:
            for vp in split_list(r.get("game_nif_paths")):
                ref_meta[C.norm(ensure_root(vp))]["edids"].add(r.get("EDID") or "")
                ref_meta[C.norm(ensure_root(vp))]["slots"].add(r.get("slot_names") or "")

        for key in sorted(ref_meta):
            vp = ensure_root(key)
            meta = ref_meta[key]
            prov = p.providers(vp)
            if not prov:
                continue
            wmod = prov[0]["mod"]
            sha = prov[0].get("sha256", "")
            in_pack = wmod in mods
            edids = ";".join(sorted(x for x in meta["edids"] if x))
            slots = ";".join(sorted(x for x in meta["slots"] if x))
            role = mesh_role(bname(vp).rsplit(".nif", 1)[0], edids, slots)
            sub = "ground\\" if role == "GROUND" else ""
            tname = bname(vp)
            decision = "KEEP" if in_pack else "REVIEW"
            notes = []
            if not in_pack:
                notes.append("WINNER_MOD_NOT_IN_OUTFIT(%s) -- cross-outfit or external "
                             "mesh dependency; manual confirm required" % wmod[:48])
                decision = "REVIEW"
            # LOD companion (deterministic: <stem>_0.nif sibling, identical sha)
            if bname(vp).lower().endswith("_1.nif"):
                sib = dname(vp) + "\\" + bname(vp).lower()[:-6] + "_0.nif"
                srow = p.winner(sib)
                if srow and srow.get("sha256") == sha:
                    notes.append("LOD_COMPANION_DUPLICATE %s has identical sha256 and "
                                 "is NOT ARMA-referenced -> excluded from migration"
                                 % bs(sib).lower())
            target = "meshes\\ZLJ\\CombatLatex\\%s\\%s%s" % (oid, sub, tname)
            tkey = C.norm(target)
            if tname in used_names[oid] and C.norm(used_names[oid][tname]) != key:
                tname = bname(vp).rsplit(".nif", 1)[0] + "__" + role.lower() + ".nif"
                target = "meshes\\ZLJ\\CombatLatex\\%s\\%s%s" % (oid, sub, tname)
                decision = "KEEP_WITH_RENAME"
                notes.append("INTRA_OUTFIT_BASENAME_COLLISION with %s -> renamed"
                             % bs(used_names[oid][bname(vp)]))
            if C.norm(tname) not in used_names[oid]:
                used_names[oid][C.norm(tname)] = vp
            if tkey in seen_target and seen_target[tkey][0] != oid:
                collisions.append((tkey, seen_target[tkey][0], oid))
            seen_target.setdefault(tkey, (oid, vp))
            rows.append([oid, "GAME_MESH", vp, wmod, wmod, prov_str(p, vp),
                         p.priority.get(wmod, ""), role, target, sha, decision,
                         "TRUE", edids, slots, "",
                         ("ARMO-reachable worn/world model. " + " ".join(notes)).strip()])
            per_outfit[oid]["GAME_MESH"] += 1
            if decision == "REVIEW":
                per_outfit[oid]["review"] += 1

            # shadowed providers -> explicit EXCLUDE_SHADOWED ledger rows
            for f in prov[1:]:
                if f["mod"] not in mods:
                    continue
                rows.append([oid, "GAME_MESH", vp, f["mod"], wmod,
                             prov_str(p, vp), p.priority.get(f["mod"], ""), role,
                             target, f.get("sha256", ""), "EXCLUDE_SHADOWED", "TRUE",
                             edids, slots, "",
                             "EXCLUDE_DO_NOT_COPY: VFS shadowed by %s (prio %s); this "
                             "copy never reaches the game at runtime"
                             % (wmod[:48], p.priority.get(wmod))])
                per_outfit[oid]["EXCLUDE_SHADOWED"] += 1

        # ---- B. BODYSLIDE_OUTPUT : the outfit's own OSP build products ---
        for ospk, (win, _rows, wmod) in sorted(ospw.items()):
            osp = bs(win["OSP_PATH"])
            if win is None or wmod not in mods:
                owner = wmod if wmod else "UNKNOWN"
                rows.append([oid, "BODYSLIDE_OUTPUT", osp, owner, owner,
                             prov_str(p, ospk), p.priority.get(owner, ""),
                             "UNKNOWN", "", "", "EXCLUDE_SHADOWED", "TRUE", "", "",
                             osp,
                             "EXCLUDE_DO_NOT_COPY: OSP virtual path is won by %s which is "
                             "outside outfit %s" % (str(owner)[:48], oid)])
                per_outfit[oid]["EXCLUDE_SHADOWED"] += 1
                continue
            out = ensure_root(win.get("output_nif") or "", "meshes")
            base = bs(win.get("base_nif") or "")
            tname = bname(out)
            role = mesh_role(tname.rsplit(".nif", 1)[0],
                             " ".join([win.get("ui_outfit_name") or ""]
                                      + list(win.get("shape_names") or [])), "")
            sub = "ground\\" if role == "GROUND" else ""
            target = "meshes\\ZLJ\\CombatLatex\\%s\\%s%s" % (oid, sub, tname)
            decision = "KEEP"
            notes = ["OSP=%s" % osp,
                     "current output_path=%s output_file=%s" % (win.get("output_path"),
                                                               win.get("output_file")),
                     "shapedata source=%s" % base,
                     "SHA256=N/A_NOT_BUILT (BodySlide build product; P02A never runs Build)"]
            if C.norm(out) not in ref_meta:
                notes.append("OSP_OUTPUT_NOT_ARMA_REFERENCED: no ARMO/ARMA record of %s "
                             "points at this path (ARMA points at the shipped LOD1 mesh); "
                             "P03 must decide whether the rebuilt output replaces the "
                             "shipped mesh or becomes an additional asset" % oid)
                decision = "REVIEW"
            if p.exists(out):
                notes.append("WARNING: a file already exists at the planned source output path")
            tkey = C.norm(target)
            if tkey in seen_target and seen_target[tkey][0] != oid:
                collisions.append((tkey, seen_target[tkey][0], oid))
            seen_target.setdefault(tkey, (oid, out))
            rows.append([oid, "BODYSLIDE_OUTPUT", out, wmod, wmod, prov_str(p, ospk),
                         p.priority.get(wmod, ""), role, target, "", decision,
                         "TRUE" if p.exists(out) else "FALSE", "", "", osp,
                             " ".join(notes)])
            per_outfit[oid]["BODYSLIDE_OUTPUT"] += 1
            if decision == "REVIEW":
                per_outfit[oid]["review"] += 1

        # ---- B2. ARMA.MOD2..MOD5 world / inventory drop models ----------
        wm_seen = set()
        for r in ps:
            for vp in split_list(r.get("world_model_paths")):
                full = ensure_root(vp)
                key = C.norm(full)
                if key in wm_seen or key in ref_meta or key in osp_out_vpaths:
                    continue
                wm_seen.add(key)
                edids = r.get("EDID") or ""
                tname = bname(full)
                target = "meshes\\ZLJ\\CombatLatex\\%s\\ground\\%s" % (oid, tname)
                if C.norm(target) in seen_target:
                    tname = tname.rsplit(".nif", 1)[0] + "__drop.nif"
                    target = "meshes\\ZLJ\\CombatLatex\\%s\\ground\\%s" % (oid, tname)
                seen_target.setdefault(C.norm(target), (oid, full))
                if p.exists(full):
                    wmod = p.winning_mod(full)
                    decision = "KEEP" if wmod in mods else "REVIEW"
                    note = ("ARMA.MOD2..MOD5 world / inventory drop model (P00 "
                            "world_model_paths). %s"
                            % ("Winning provider is outside this outfit -- confirm."
                               if decision == "REVIEW"
                               else "Mod-owned ground object."))
                    rows.append([oid, "GAME_MESH", full, wmod, wmod, prov_str(p, full),
                                 p.priority.get(wmod, ""), "GROUND", target,
                                 p.sha(full), decision, "TRUE", edids,
                                 r.get("slot_names") or "", "", note])
                else:
                    note = ("EXTERNAL_GO_MODEL: ARMA %s (slots %s) uses %s as its "
                            "world/inventory drop model. It is owned by no mod of %s and is "
                            "absent from the frozen P00 VFS scope (stock CBBE/vanilla GO). "
                            "PROPOSED repoint target only -- NOT approved; keep CBBE as an "
                            "external prerequisite or author a pack-local GO mesh in P02B."
                            % (edids, r.get("slot_names"), full, oid))
                    rows.append([oid, "GAME_MESH", full, "UNKNOWN", "UNKNOWN", "", "",
                                 "GROUND", target, "", "REVIEW", "FALSE", edids,
                                 r.get("slot_names") or "", "", note])
                per_outfit[oid]["GAME_MESH"] += 1
                per_outfit[oid]["review"] += 1

        # ---- C. ARMA model slots that no OSP of this outfit produces -----
        pending_seen = set()
        for r in ps:
            for vp in split_list(r.get("pending_build_nifs")):
                full = ensure_root(vp)
                key = C.norm(full)
                if key in pending_seen or key in osp_out_vpaths:
                    continue
                pending_seen.add(key)
                cbbe = key.startswith(C.norm("meshes\\armor\\studded\\"))
                role = studded_role(full)
                folder = "drop\\" if cbbe else "bodyslided\\"
                target = "meshes\\ZLJ\\CombatLatex\\%s\\%s%s" % (oid, folder,
                                                                     bname(full))
                if cbbe:
                    note = ("EXTERNAL_CBBE_SLOT_MESH: ARMA %s (slots %s) references the "
                            "stock CBBE armor-slot model %s via ARMA.MODL/MODn. It is NOT a "
                            "pack asset and is NOT produced by any OSP of %s; the pack must "
                            "either keep CBBE as an external prerequisite or own a pack-local "
                            "drop/1st-person mesh built in P02B. PROPOSED repoint target only "
                            "-- NOT approved." % (r.get("EDID"), r.get("slot_names"),
                                                  full, oid))
                    prov = "UNKNOWN"
                else:
                    note = ("MISSING_RUNTIME_MESH: ARMA %s (slots %s) references %s but no "
                            "OSP of %s produces it and no ShapeData source is registered "
                            "(P00 status=%s). The worn mesh does not exist in this install."
                            % (r.get("EDID"), r.get("slot_names"), full, oid,
                               r.get("game_nif_resolution_status")))
                    prov = "UNKNOWN"
                rows.append([oid, "BODYSLIDE_OUTPUT", full, prov, prov, "",
                             "", role, target, "", "REVIEW", "FALSE",
                             r.get("EDID") or "", r.get("slot_names") or "", "", note])
                per_outfit[oid]["BODYSLIDE_OUTPUT"] += 1
                per_outfit[oid]["review"] += 1
                per_outfit[oid]["unresolved"] += 1

    return rows, collisions, per_outfit


# ======================================================== 2. TEXTURE LEDGER ==
TEX_HEADER = [
    "OUTFIT_ID", "referencing_nif", "referencing_nif_class", "shape",
    "texture_slot", "source_virtual_path", "winning_provider",
    "shadowed_providers", "sha256", "semantic_type", "target_virtual_path",
    "owning_outfit_of_source", "action", "exists_in_vfs", "shared_proposal",
    "notes",
]

REWRITE_HEADER = [
    "OUTFIT_ID", "nif_source", "shape_name", "texture_slot", "old_dds_path",
    "new_dds_path", "source_provider", "status", "shared_proposal", "notes",
]

CLOSURE_HEADER = [
    "OUTFIT_ID", "dependency_type", "source_owner", "source_virtual_path",
    "winning_provider", "referenced_by_nif", "texture_slot", "resolution_plan",
    "target_virtual_path", "post_plan_state", "notes",
]


def build_texture_ledgers(p, pmap, mod_owner):
    """Walk the RETAINED meshes of every outfit backwards into the DDS VFS."""
    tex_rows = []
    rw_rows = []
    cl_rows = []
    rw_stats = collections.defaultdict(collections.Counter)
    stats = collections.defaultdict(collections.Counter)
    tex_target_owner = collections.defaultdict(set)   # target_norm -> outfits
    source_outfits = collections.defaultdict(set)     # dds_norm -> referencing outfits
    tex_collisions = []
    seen_target = {}
    used = collections.defaultdict(dict)               # outfit -> bname -> dds
    tex_cache = {}

    def nif_rows(vp):
        key = C.norm(vp)
        if key not in tex_cache:
            tex_cache[key] = p.nif_tex_rows(vp)
        return tex_cache[key]

    # -- collect the mesh inventory we decided to keep ----------------------
    work = []            # (oid, nif_vpath, nif_class, note_prefix)
    for oid in C.OUTFIT_IDS:
        ospw = osp_rows_of(p, oid)
        mods = set(p.mods_of_outfit(oid))
        ref = set()
        for r in pmap.get(oid, []):
            for vp in split_list(r.get("game_nif_paths")):
                ref.add(ensure_root(vp))
        for k in sorted(ref):
            if p.exists(k):
                work.append((oid, k, "GAME_MESH", ""))
        for ospk, (win, _r, wmod) in sorted(ospw.items()):
            if win is None or wmod not in mods:
                continue
            base = win.get("base_nif")
            if not base:
                continue
            work.append((oid, ensure_root(win.get("output_nif") or "", "meshes"),
                         "BODYSLIDE_OUTPUT",
                         "BodySlide build product inherits the BSShaderTextureSet of "
                         "ShapeData NIF %s" % bs(base)))

    for oid, nifvp, cls, prefix in work:
        for shape, slot, dds in nif_rows(nifvp):
            dds = bs(dds)
            dn = C.norm(dds)
            exists = p.exists(dds)
            wmod = p.winning_mod(dds)
            owners = mod_owner.get(wmod, []) if wmod else []
            if not exists:
                own = "UNKNOWN"
            elif owners:
                own = ";".join(owners)
            else:
                own = "EXTERNAL_MOD"
            source_outfits[dn].add(oid)

            # ---- action / target ----
            notes = []
            if not exists:
                action = "UNRESOLVED"
                target = ""
                status = "UNRESOLVED"
                own = "UNKNOWN"
                notes.append("NOT_IN_FROZEN_P00_VFS: the frozen P00 VFS scope only covers "
                             "the 56 latex-scope mods (data/P00_RERUN/00_scope_evidence.json); "
                             "absence cannot distinguish Skyrim-vanilla from a mod outside "
                             "that scope -> UNRESOLVED, no guessing")
            elif dn.startswith(C.norm("textures\\zlj\\combatlatex\\" + oid.lower())):
                action = "KEEP_SELF_NAMESPACE"
                target = dds
                status = "REPOINT_SELF_NAMESPACE"
            else:
                action = "COPY_INTO_OUTFIT_NAMESPACE"
                target = "textures\\ZLJ\\CombatLatex\\%s\\%s" % (oid, bname(dds))
                if wmod in mod_owner:
                    others = [o for o in owners if o != oid]
                    if others:
                        status = "COPY_FROM_CROSS_OUTFIT"
                        notes.append("CROSS_OUTFIT: winning provider %s belongs to %s"
                                     % (wmod[:48], ";".join(others)))
                    else:
                        status = "REPOINT_SELF_NAMESPACE"
                else:
                    status = "COPY_FROM_EXTERNAL_MOD"
                    notes.append("EXTERNAL_MOD source %s -- copied into this outfit "
                                 "namespace (shared-asset whitelist = NONE)"
                                 % wmod[:48])
                # intra-outfit basename collision -> keep the source sub-folder
                bn = C.norm(bname(dds))
                if bn in used[oid] and used[oid][bn] != dn:
                    parent = dname(dds).rsplit("\\", 1)[-1] or "sub"
                    target = "textures\\ZLJ\\CombatLatex\\%s\\%s\\%s" % (oid,
                                                                              parent,
                                                                              bname(dds))
                    notes.append("INTRA_OUTFIT_BASENAME_COLLISION with %s -> source "
                                 "sub-folder preserved" % bs(used[oid][bn]))
                used[oid].setdefault(bn, dn)

            shared_prop = "NONE"
            if exists:
                tex_target_owner[C.norm(target)].add(oid)

            sem = C.semantic_type(slot, dds)
            tex_rows.append([oid, nifvp, cls, shape, slot, dds, wmod or "UNKNOWN",
                             prov_str(p, dds) if exists else "", p.sha(dds) if exists else "",
                             sem, target, own, action, "TRUE" if exists else "FALSE",
                             shared_prop,
                             (" ".join([prefix] + notes)).strip()])
            rw_rows.append([oid, nifvp, shape, slot, dds, target,
                            wmod or "UNKNOWN", status, shared_prop,
                            (" ".join(notes)).strip()])
            stats[oid]["tex"] += 1
            rw_stats[oid][status] += 1
            if not exists:
                stats[oid]["unresolved"] += 1

    # ---- shared-asset proposals (whitelist NONE -> proposal only) --------
    for dn, outfits in sorted(source_outfits.items()):
        if len(outfits) < 2:
            continue
        for oid in sorted(outfits):
            if not p.exists(dn):
                continue
            sha = p.sha(dn)
            cl_rows.append([
                oid, "CROSS_PACK_CANDIDATE",
                ";".join(sorted(o for o in outfits if o != oid)) or "UNKNOWN",
                [t[5] for t in tex_rows if C.norm(t[5]) == dn and t[0] == oid][0],
                p.winning_mod(dn),
                ";".join(sorted({t[1] for t in tex_rows
                                 if C.norm(t[5]) == dn and t[0] == oid})),
                ";".join(sorted({t[4] for t in tex_rows
                                 if C.norm(t[5]) == dn and t[0] == oid})),
                "PROPOSAL_SHARED_NOT_APPROVED: identical sha256 %s is consumed by %d "
                "outfits of this pack; P02A duplicates it into each outfit namespace and "
                "does NOT create a Shared folder. Sharing is a P05 decision."
                % (sha[:16], len(outfits)),
                "textures\\ZLJ\\CombatLatex\\%s\\%s" % (oid, bname(dn)),
                "CLOSED_BY_DUPLICATION",
                "status=PROPOSAL_SHARED_NOT_APPROVED (shared-asset whitelist = NONE)",
            ])
            stats[oid]["share_proposal"] += 1
            for t in rw_rows:
                if t[0] == oid and C.norm(t[4]) == dn:
                    t[8] = "PROPOSAL_SHARED_NOT_APPROVED"
            for t in tex_rows:
                if t[0] == oid and C.norm(t[5]) == dn:
                    t[14] = "PROPOSAL_SHARED_NOT_APPROVED"

    # ---- closure ledger: every non-self-namespace dependency -------------
    runtime_cross_before = set()
    for t in tex_rows:
        oid, nifvp, cls, shape, slot, dds, wmod, shad, sha, sem, target, own, action,             ex, sp, notes = t
        if action == "KEEP_SELF_NAMESPACE":
            continue
        # only real OUTFIT_IDs count as pack owners; "EXTERNAL_MOD"/"UNKNOWN" do not
        own_list = [o for o in str(own).split(";") if o in C.OUTFIT_IDS]
        cross = [o for o in own_list if o != oid]
        if not cross and own_list:
            # the asset already belongs to THIS outfit and simply moves into this
            # outfit's namespace -- a pure migration, not a dependency.  It is fully
            # described by P02A_TEXTURE_MIGRATION / P02A_NIF_TEXTURE_REWRITE.
            continue
        if (not ex) or str(ex).upper() != "TRUE":
            dtype = "UNRESOLVED"
            plan = ("BLOCKED: source DDS is absent from the frozen P00 VFS scope. "
                    "Resolution needs (a) a P00 evidence extension over Skyrim Data + the "
                    "referencing mods, or (b) an explicit manual allowlist. No fuzzy match.")
            state = "OPEN_BLOCKED"
        elif cross:
            dtype = "CROSS_OUTFIT"
            plan = ("COPY_INTO_OUTFIT_NAMESPACE + REPOINT: copy %s (owner %s) into "
                    "textures\\ZLJ\\CombatLatex\\%s\\ and repoint %s / %s / %s"
                    % (bname(dds), ";".join(cross), oid, nifvp, shape, slot))
            state = "CLOSED"
            runtime_cross_before.add((oid, dn_norm(dds)))
        elif str(own) == "EXTERNAL_MOD":
            dtype = "EXTERNAL_MOD"
            plan = ("COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor %s into "
                    "textures\\ZLJ\\CombatLatex\\%s\\%s and repoint %s / %s / %s so "
                    "the outfit is self-contained (shared-asset whitelist = NONE)"
                    % (bname(dds), oid, bname(dds), nifvp, shape, slot))
            state = "CLOSED"
        else:
            dtype = "EXTERNAL_MOD"
            plan = ("COPY_INTO_OUTFIT_NAMESPACE + REPOINT into "
                    "textures\\ZLJ\\CombatLatex\\%s\\%s" % (oid, bname(dds)))
            state = "CLOSED"
        cl_rows.append([oid, dtype, own, dds, wmod or "UNKNOWN", nifvp, slot, plan,
                        target, state, notes])
        stats[oid]["closure_" + dtype.lower()] += 1

    # ---- target collision accounting -------------------------------------
    for t in tex_rows:
        if not t[10] or t[12] == "UNRESOLVED":
            continue
        k = C.norm(t[10])
        if k in seen_target and seen_target[k][0] != t[0]:
            tex_collisions.append((k, seen_target[k][0], t[0]))
        seen_target.setdefault(k, (t[0], t[10]))

    return (tex_rows, rw_rows, cl_rows, stats, rw_stats, tex_collisions,
            runtime_cross_before)


def dn_norm(dds):
    return C.norm(dds)


# ==================================================================== main ==
def main():
    p = C.P00.get()
    mod_owner, plugin_owner = build_pack_maps(p)
    pmap = parts_of(p, plugin_owner)

    mesh_rows, mesh_coll, mesh_stats = build_mesh_ledger(p, pmap, plugin_owner)
    (tex_rows, rw_rows, cl_rows, tex_stats,
     rw_stats, tex_coll, cross_before) = build_texture_ledgers(p, pmap, mod_owner)

    os.makedirs(OUT_DIR, exist_ok=True)
    C.write_csv(os.path.join(OUT_DIR, "P02A_MESH_MIGRATION.csv"), MESH_HEADER, mesh_rows)
    C.write_csv(os.path.join(OUT_DIR, "P02A_TEXTURE_MIGRATION.csv"), TEX_HEADER, tex_rows)
    C.write_csv(os.path.join(OUT_DIR, "P02A_NIF_TEXTURE_REWRITE.csv"),
                REWRITE_HEADER, rw_rows)
    C.write_csv(os.path.join(OUT_DIR, "P02A_CROSS_OUTFIT_TEXTURE_CLOSURE.csv"),
                CLOSURE_HEADER, cl_rows)

    # ------------------------------- summary ------------------------------
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 78)
    print("P02A MESH + TEXTURE MIGRATION LEDGER -- ZLJ_COMBAT_LATEX (STRICT READ-ONLY)")
    print("=" * 78)
    hdr = ("%-18s %5s %5s %5s %5s %5s %5s %5s %5s %5s"
           % ("OUTFIT_ID", "mesh", "gmesh", "bsout", "excl", "tex", "rw", "clos",
              "unres", "review"))
    print(hdr)
    print("-" * 78)
    tot = collections.Counter()
    for oid in C.OUTFIT_IDS:
        m = mesh_stats[oid]
        t = tex_stats[oid]
        clos = sum(v for k, v in t.items() if k.startswith("closure_"))
        print("%-18s %5d %5d %5d %5d %5d %5d %5d %5d %5d"
              % (oid, sum(m.values()), m["GAME_MESH"], m["BODYSLIDE_OUTPUT"],
                 m["EXCLUDE_SHADOWED"], t["tex"], sum(rw_stats[oid].values()),
                 clos, t["unresolved"], m["review"]))
        for k, v in m.items():
            tot["m_" + k] += v
        for k, v in t.items():
            tot["t_" + k] += v
        for k, v in rw_stats[oid].items():
            tot["rw_" + k] += v
    print("-" * 78)
    print("TOTALS  mesh rows=%d  texture rows=%d  rewrite rows=%d  closure rows=%d"
          % (len(mesh_rows), len(tex_rows), len(rw_rows), len(cl_rows)))
    print("  GAME_MESH=%d  BODYSLIDE_OUTPUT=%d  EXCLUDE_SHADOWED=%d"
          % (tot["m_GAME_MESH"], tot["m_BODYSLIDE_OUTPUT"], tot["m_EXCLUDE_SHADOWED"]))
    print("  distinct target paths retained: %d" % len({C.norm(r[8]) for r in mesh_rows
                                                       if r[8] and r[10] != "EXCLUDE_SHADOWED"}))
    print("TARGET_PATH_COLLISION mesh   = %d" % len(mesh_coll))
    for c in mesh_coll:
        print("    COLLISION", c)
    print("TARGET_PATH_COLLISION texture = %d" % len(tex_coll))
    for c in tex_coll:
        print("    COLLISION", c)
    print("-" * 78)
    print("CROSS-OUTFIT TEXTURE DEPENDENCY")
    print("  distinct (referencing outfit, source DDS) pairs owned by another "
          "outfit of this pack BEFORE plan = %d" % len(cross_before))
    print("  runtime cross-outfit texture dependency AFTER plan = 0 "
          "(every retained reference is repointed into its own outfit namespace)")
    unres_src = sorted({r[5] for r in tex_rows if r[12] == "UNRESOLVED"})
    print("  UNRESOLVED distinct source DDS not in frozen P00 VFS scope = %d"
          % len(unres_src))
    print("-" * 78)
    print("BLOCKERS / REVIEW ITEMS")
    blk = [r for r in mesh_rows if r[10] == "REVIEW"]
    print("  mesh REVIEW rows = %d" % len(blk))
    reasons = collections.Counter()
    for r in blk:
        if "EXTERNAL_CBBE_SLOT_MESH" in r[15]:
            reasons["EXTERNAL_CBBE_SLOT_MESH"] += 1
        elif "MISSING_RUNTIME_MESH" in r[15]:
            reasons["MISSING_RUNTIME_MESH"] += 1
        elif "OSP_OUTPUT_NOT_ARMA_REFERENCED" in r[15]:
            reasons["OSP_OUTPUT_NOT_ARMA_REFERENCED"] += 1
        elif "EXTERNAL_GO_MODEL" in r[15]:
            reasons["EXTERNAL_GO_MODEL"] += 1
        elif "WINNER_MOD_NOT_IN_OUTFIT" in r[15]:
            reasons["WINNER_MOD_NOT_IN_OUTFIT"] += 1
        else:
            reasons["OTHER"] += 1
    for k, v in reasons.most_common():
        print("    %-32s %d" % (k, v))
    print("  texture UNRESOLVED rows = %d" % tot["t_unresolved"])
    print("  NIF texture rewrite status breakdown:")
    for k in sorted([k for k in tot if k.startswith("rw_")]):
        print("    %-30s %d" % (k[3:], tot[k]))
    print("  closure dependency_type breakdown:")
    for k in sorted([k for k in tot if k.startswith("t_closure_")]):
        print("    %-30s %d" % (k[10:], tot[k]))
    print("  shared-asset proposals (whitelist NONE, P05 topic) = %d"
          % tot["t_share_proposal"])
    print("=" * 78)


if __name__ == "__main__":
    main()
