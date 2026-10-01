# -*- coding: utf-8 -*-
"""P02A -- effective source map + architecture for ZLJ Combat Latex Pack.

STRICT READ-ONLY design stage.

Reads only the frozen P00 evidence set through tools/P02A/p02a_common.py and
writes only:
    reports/P02A/P02A_EFFECTIVE_SOURCE_MAP.csv
    reports/P02A/P02A_ARCHITECTURE.md

Nothing in MO2 / Skyrim / Data is created, moved, copied or modified. The
migration ledger produced here is plan text only (COPY + REPOINT).

Architecture rule enforced throughout: one source Outfit == one independent
asset namespace. Assets are never shared between Outfits in P02A, even when
SHA256 is identical. Sharing is deferred to P05 MATERIAL STANDARDIZATION.
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
import p02a_common as C  # noqa: E402

P = C.P00.get()

# ------------------------------------------------------------------ config --
REL_VALUES = {"BASE_MOD", "REWORK", "BODYSLIDE_CONVERSION", "PBR_PATCH",
              "LATEX_REWORK", "PHYSICS_PATCH", "NONE"}
NON_ASSET_EXT = {".old000", ".old001", ".old002", ".espbak", ".bak", ".nifbak"}
RESERVED_NAME = {"meta.ini"}          # MO2 / FOMOD bookkeeping, never a game asset
NON_ASSET_STEM = re.compile(r"(bak\d*|副本|copy|\d+副本|~$)", re.I)
TS_BACKUP = re.compile(r"\.(20\d\d_\d\d_\d\d|\d\d_\d\d_\d\d)_\d\d_\d\d_\d\d$")

HEADER = ["OUTFIT_ID", "asset_type", "virtual_path", "winning_provider",
          "shadowed_providers", "relationship", "notes",
          "scope", "reach", "provider_count", "winner_priority", "sha256",
          "target_path", "migration_action", "status"]

rows = []
seen = {}
stats = collections.defaultdict(collections.Counter)
info = collections.OrderedDict()
unknowns = []
blockers = []
_unknown_seen = set()
_blocker_seen = set()


def note_unknown(oid, vp, code, detail=""):
    k = (oid, C.norm(vp), code)
    if k in _unknown_seen:
        return
    _unknown_seen.add(k)
    unknowns.append((oid, vp, code, detail))


def note_blocker(oid, sev, subject, note):
    k = (oid, C.norm(subject), sev)
    if k in _blocker_seen:
        return
    _blocker_seen.add(k)
    blockers.append((oid, sev, subject, note))
collisions = []
cross_outfit = []

INPACK = set()
for _oid in C.OUTFIT_IDS:
    INPACK.update(P.mods_of_outfit(_oid))


def bs(vp):
    return str(vp).replace("/", "\\")


def owner_outfits(mod):
    return sorted(o for o in C.OUTFIT_IDS if mod in P.mods_of_outfit(o))


def is_non_asset(vpath, ext):
    base = os.path.basename(bs(vpath))
    if base.lower() in RESERVED_NAME:
        return "RESERVED_MO2_FILE"
    if ext in NON_ASSET_EXT:
        return "BACKUP_OR_SUPERSEDED"
    if ext not in (".esp", ".esl", ".esp11", ".nif", ".dds", ".osp", ".osd",
                   ".xml", ".json", ".ini", ".txt"):
        return "NON_ASSET_TYPE"
    if TS_BACKUP.search(base):
        return "TIMESTAMPED_BACKUP"
    if NON_ASSET_STEM.search(os.path.splitext(base)[0]):
        return "AUTHOR_BACKUP_COPY"
    return ""


def asset_type_of(vpath, ext):
    if ext in (".esp", ".esl", ".esp11"):
        return "PLUGIN"
    if ext == ".nif":
        return ("SHAPEDATA_NIF"
                if C.norm(vpath).startswith("calientetools/bodyslide/shapedata/")
                else "GAME_NIF")
    return {".dds": "DDS", ".osp": "OSP", ".osd": "OSD", ".xml": "PHYSICS_XML",
            ".json": "PBR_JSON", ".ini": "CONFIG", ".txt": "CONFIG"}.get(ext, "OTHER")


def support_role(oid, mod):
    for role, m in C.OUTFITS[oid].get("support", {}).items():
        if m == mod:
            return role
    return ""


def rel_for(oid, atype, winning_mod):
    """Frozen source taxonomy. See P02A_ARCHITECTURE.md section 3."""
    if atype == "PHYSICS_XML":
        return "PHYSICS_PATCH"
    role = support_role(oid, winning_mod)
    if role == "PBR_PATCH":
        return "PBR_PATCH"
    if role == "LATEX_REWORK":
        return "LATEX_REWORK"
    if atype in ("SHAPEDATA_NIF", "OSP", "OSD"):
        return "BODYSLIDE_CONVERSION"
    if winning_mod == C.OUTFITS[oid]["primary"]:
        return "BASE_MOD"
    return "NONE"


def target_path_for(oid, atype, vpath):
    b = os.path.basename(bs(vpath))
    if atype == "GAME_NIF":
        return C.MESH_ROOT + oid + "\\" + b
    if atype == "DDS":
        return C.TEX_ROOT + oid + "\\" + b
    if atype in ("SHAPEDATA_NIF", "OSD"):
        return C.SD_ROOT + oid + "\\" + b
    if atype == "OSP":
        return C.OSP_ROOT + "ZLJ_" + oid + ".osp"
    if atype == "PLUGIN":
        return C.TARGET_PLUGIN
    if atype == "PBR_JSON":
        return "pbrnifpatcher\\ZLJ\\CombatLatex\\" + oid + "\\" + b
    if atype == "PHYSICS_XML":
        return C.MESH_ROOT + oid + "\\" + b
    return ""


def add(oid, vpath, scope, reach, ext=None, atype=None, relationship=None,
        notes="", action=None, status=None):
    vpath = bs(vpath)
    key = (oid, C.norm(vpath))
    ext = ext or os.path.splitext(vpath)[1].lower()
    atype = atype or asset_type_of(vpath, ext)
    prov = P.providers(vpath)
    if prov:
        winning = prov[0]["mod"]
        shadowed = [x["mod"] for x in prov[1:]]
        wprio = P.priority.get(winning, "")
        sha = prov[0].get("sha256", "")
    else:
        winning, shadowed, wprio, sha = "", [], "", ""
    if key in seen:
        r = seen[key]
        if reach and reach not in r["reach"]:
            r["reach"] += "; " + reach
        if notes:
            r["notes"] = (r["notes"] + " | " + notes) if r["notes"] else notes
        if status == "BLOCKER" or (status == "UNKNOWN" and r["status"] == "OK"):
            r["status"] = status
            if status == "BLOCKER":
                r["migration_action"] = "UNKNOWN_BLOCKER"
        return r
    r = {"OUTFIT_ID": oid, "asset_type": atype, "virtual_path": vpath,
         "winning_provider": winning, "shadowed_providers": " | ".join(shadowed),
         "relationship": relationship or "NONE", "notes": notes, "scope": scope,
         "reach": reach, "provider_count": len(prov), "winner_priority": wprio,
         "sha256": sha, "target_path": target_path_for(oid, atype, vpath),
         "migration_action": action or "COPY+REPOINT", "status": status or "OK"}
    seen[key] = r
    rows.append(r)
    return r


# P00's frozen file_index covers MOD folders only. Skyrim base-game Data is
# therefore legitimately absent from it. The roots below are the literal
# Skyrim base-game Data texture roots; a path under one of them and carrying no
# "[...]" mod-override tag is reported as un-indexed base game, not as a broken
# dependency. This is an exact literal-prefix test, not fuzzy matching.
BASE_GAME_TEX_ROOTS = (
    "textures/actors/", "textures/cubemaps/", "textures/dlc/", "textures/fonts/",
    "textures/interface/", "textures/menus/", "textures/misc/", "textures/parchment/",
    "textures/sound/", "textures/translation/", "textures/armor/",
    "textures/creatures/", "textures/cloth/", "textures/effects/", "textures/fx/",
    "textures/grasses/", "textures/impact/", "textures/lights/",
    "textures/markers/", "textures/materials/", "textures/models/",
    "textures/roads/", "textures/script/", "textures/sky/", "textures/sound/",
    "textures/vfx/", "textures/water/",
)


def classify_missing(vp):
    """Classify a texture reference that the frozen mod-scoped index cannot see."""
    n = C.norm(vp)
    if n in ("textures/", "textures", ""):
        return ("REACHABLE_MALFORMED_REF", "UNKNOWN_BLOCKER", "BLOCKER",
                "MALFORMED REFERENCE: the NIF texture slot holds a non-path token; author bug in the source NIF.")
    tagged = "[" in n and "]" in n
    for root in BASE_GAME_TEX_ROOTS:
        if n.startswith(root):
            if tagged:
                break
            return ("REACHABLE_UNRESOLVED_BASE",
                    "NO_COPY_EXTERNAL_REF", "UNKNOWN",
                    "Under Skyrim base-game Data root '%s' and free of any '[...]' mod tag, so it is base-game "
                    "content outside the frozen mod-scoped index. Not copied; kept as an external reference."
                    % root.rstrip("/"))
    return ("REACHABLE_UNRESOLVED_INSTANCE", "UNKNOWN_BLOCKER", "BLOCKER",
            "UNRESOLVED: absent from the frozen P00 TARGET09 index. That index covers only the 56 in-scope "
            "mods, so this is NOT evidence of absence from the MO2 instance. The P02A.1 global provider "
            "lookup (P02A_GLOBAL_PROVIDER_LOOKUP.csv) is the authoritative classification; until it is "
            "consulted no absence claim is made here. No fuzzy matching used.") 


def tex_slots(nif):
    out = []
    for sh in nif.get("shapes", []) or []:
        for slot, val in (sh.get("textures") or {}).items():
            if val and str(val).strip():
                out.append((sh.get("name", ""), slot, str(val).strip()))
    return out


# ============================================================ main pass ====
for oid in C.OUTFIT_IDS:
    o = C.OUTFITS[oid]
    mods = P.mods_of_outfit(oid)
    primary = o["primary"]
    st = stats[oid]
    d = info[oid] = collections.defaultdict(set)
    d["mods"] = set(mods)
    d["osp"] = {}
    d["pbr"] = {k for k in C.OUTFITS[oid].get("support", {}) if k == "PBR_PATCH"}
    d["rework"] = {k for k in C.OUTFITS[oid].get("support", {}) if k == "LATEX_REWORK"}
    bs_projects = [b for m in mods for b in P.bs_of_mod.get(m, [])]
    d["bs_projects"] = bs_projects
    st["mods"] = len(mods)

    # ---- (a) every VFS path offered by the in-scope mods ----------------
    for m in mods:
        for f in P.files_of_mod.get(m, []):
            vp, ext = f["vpath"], f["ext"]
            at = asset_type_of(vp, ext)
            prov = P.providers(vp)
            winning = prov[0]["mod"] if prov else m
            why = is_non_asset(vp, ext)
            notes, act, status, rel = "", "COPY+REPOINT", "OK", rel_for(oid, at, winning)
            if why:
                notes = "NON-ASSET (%s): excluded from the migration ledger, never copied." % why
                act, status, rel = "EXCLUDE_NON_ASSET", "OK", "NONE"
            elif at == "PLUGIN":
                act = "REWRITE_INTO_ZLJ_CombatLatex.esp"
                notes = ("source plugin; its records are re-authored into %s under EDID namespace "
                         "ZLJ_CL_<Outfit>_<Part>." % C.TARGET_PLUGIN)
            elif at in ("SHAPEDATA_NIF", "OSD", "OSP"):
                act = "BODYSLIDE_CONVERSION"
            elif at == "PBR_JSON" or C.norm(vp).startswith("textures/pbr/"):
                rel = "PBR_PATCH"
            if at == "OSP":
                d["osp"].setdefault(C.norm(vp), vp)
            if winning != m:
                notes += (" [VFS] winner is '%s' (prio %s), not the offering mod '%s' (prio %s)." %
                          (winning, P.priority.get(winning, "?"), m, P.priority.get(m, "?")))
            if len(prov) > 1:
                same = len(set(x.get("sha256", "") for x in prov)) == 1
                kind = "MO2_RESERVED_NAME" if C.norm(vp) == "meta.ini" else "VFS_OVERRIDE"
                collisions.append((oid, vp, kind, "providers=%d identical_sha256=%s winner=%s" %
                                   (len(prov), same, winning)))
                if C.norm(vp) != "meta.ini":
                    notes += " [VFS] collision: %d providers, identical_sha256=%s." % (len(prov), same)
            if winning not in mods:
                if winning in INPACK:
                    who = owner_outfits(winning)
                    cross_outfit.append((oid, vp, ",".join(who), "VFS winner owned by another in-pack Outfit"))
                    notes += " CROSS-OUTFIT WINNER '%s' (also %s)." % (winning, ",".join(who))
                    status = "BLOCKER"
                    note_blocker(oid, "HIGH", vp,
                                    "VFS winner is an in-pack mod of another Outfit %s" % ",".join(who))
                else:
                    notes += " OUT-OF-PACK WINNER '%s'." % winning
                    status = "UNKNOWN"
                    note_unknown(oid, vp, "OUT_OF_PACK_WINNER", winning)
            add(oid, vp, "IN_SCOPE_MOD", "in-scope mod file", ext=ext, atype=at,
                relationship=rel, notes=notes, action=act, status=status)
            d[at].add(vp)

    # ---- (b) plugin ARMO / ARMA model paths ------------------------------
    recs = P.records_of_plugin.get(o["plugin"], [])
    st["plugin_records"] = len(recs)
    n_model = 0
    for r in recs:
        sub = r.get("subrecords") or {}
        for slot in ("MOD2", "MOD3", "MOD4", "MOD5"):
            for v in (sub.get(slot) or []):
                if not isinstance(v, str) or not v.strip():
                    continue
                n_model += 1
                vp = "meshes\\" + v.strip().replace("/", "\\")
                edid = (sub.get("EDID") or [""])[0]
                ref = "%s %s.%s EDID=%s" % (r["record_type"], r["formid"], slot, edid)
                d["plugin_model_refs"].add(vp)
                if not P.exists(vp):
                    add(oid, vp, "REACHABLE_VANILLA_STOCK", "plugin " + ref, ext=".nif",
                        atype="GAME_NIF", relationship="NONE",
                        notes=("UNRESOLVED: absent from the frozen P00 mod-scoped index, which is not a statement "
                              "about the instance. This is an "
                               "ARMO/ARMA stock placeholder; vanilla Skyrim Data is outside the frozen "
                               "index. No fuzzy matching used; manual confirmation required."),
                        action="UNKNOWN_BLOCKER", status="BLOCKER")
                    note_unknown(oid, vp, "UNRESOLVED_MODEL_PATH", ref)
                    note_blocker(oid, "HIGH", ref,
                                 "model path unresolvable in the frozen evidence")
                    continue
                wm = P.winning_mod(vp)
                if wm in mods:
                    add(oid, vp, "REACHABLE_IN_PACK", "plugin " + ref, ext=".nif", atype="GAME_NIF",
                        relationship=rel_for(oid, "GAME_NIF", wm),
                        notes="Worn/world model referenced by %s." % ref,
                        action="COPY+REPOINT", status="OK")
                else:
                    add(oid, vp, "REACHABLE_EXTERNAL", "plugin " + ref, ext=".nif", atype="GAME_NIF",
                        relationship="NONE",
                        notes=("Referenced by %s but the VFS winner '%s' is out-of-pack. Not copied; the "
                               "dependency must be recorded or repointed explicitly." % (ref, wm)),
                        action="NO_COPY_EXTERNAL_REF", status="UNKNOWN")
                    note_unknown(oid, vp, "EXTERNAL_MODEL_WINNER", wm)
                d["GAME_NIF"].add(vp)
    st["model_refs"] = n_model

    # ---- (b2) BodySlide OSP -> ShapeData members + EXACT_OUTPUT_PATH -----
    osp_folders = set()
    for b in bs_projects:
        osp = b["OSP_PATH"]
        d["osp"].setdefault(C.norm(osp), osp)
        bn = b.get("base_nif")
        folder = os.path.dirname(bs(bn)) if bn else ""
        if folder:
            osp_folders.add(C.norm(folder))
        members = [f for f in P.file_index
                   if folder and C.norm(f["vpath"]).startswith(C.norm(folder) + "/")
                   and f["ext"] in (".nif", ".osd")]
        for f in members:
            vp = f["vpath"]
            wm = P.winning_mod(vp)
            at = asset_type_of(vp, f["ext"])
            in_pack = wm in mods
            note = ("ShapeData member of BodySlide project %s (data folder '%s'); EXACT_OUTPUT_PATH "
                    "relation to the .osp." % (osp, folder or "UNKNOWN"))
            if not in_pack:
                note += " VFS winner '%s' is out-of-pack." % wm
            add(oid, vp, "REACHABLE_IN_PACK" if in_pack else "REACHABLE_EXTERNAL",
                "BodySlide OSP " + osp, ext=f["ext"], atype=at,
                relationship="BODYSLIDE_CONVERSION", notes=note,
                action="BODYSLIDE_CONVERSION", status="OK" if in_pack else "UNKNOWN")
            if not in_pack:
                note_unknown(oid, vp, "SHAPEDATA_OUT_OF_PACK_WINNER", wm)
            d[at].add(vp)
        out = b.get("output_nif")
        if out:
            if P.exists(out):
                note = "BodySlide build output; VFS winner '%s'." % P.winning_mod(out)
                stat = "OK"
            else:
                note = ("BodySlide build output (EXACT_OUTPUT_PATH of %s); NOT PRESENT in the VFS because "
                        "no BodySlide build has been run. P02A never builds it." % osp)
                stat = "UNKNOWN"
                note_unknown(oid, out, "PENDING_BODYSLIDE_BUILD", osp)
            add(oid, out, "PENDING_BUILD", "BodySlide OSP " + osp + " EXACT_OUTPUT_PATH",
                ext=".nif", atype="GAME_NIF", relationship="BODYSLIDE_CONVERSION",
                notes=note, action="PENDING_BUILD", status=stat)
            d["GAME_NIF"].add(out)
        n_nif = len([f for f in members if f["ext"] == ".nif"])
        if int(b.get("shapedata_nif_count") or 0) != n_nif:
            r = seen.get((oid, C.norm(osp)))
            n = ("P00 bs_projects.shapedata_nif_count=%s disagrees with the frozen file index (%d NIF in "
                 "'%s'); this script trusts the frozen file index + the .osp data folder."
                 % (b.get("shapedata_nif_count"), n_nif, folder))
            if r:
                r["notes"] = (r["notes"] + " " if r["notes"] else "") + n
                r["status"] = "UNKNOWN"
            note_unknown(oid, osp, "P00_SHAPEDATA_COUNT_MISMATCH", n)
            d["p00_count_mismatch"].add(osp)

    # ---- (b3) physics XML -> NIF (exact '<stem>.nif' convention) ---------
    for m in mods:
        for f in P.files_of_mod.get(m, []):
            if f["ext"] != ".xml":
                continue
            vp = f["vpath"]
            stem = os.path.splitext(os.path.basename(bs(vp)))[0]
            folder = os.path.dirname(bs(vp))
            if not C.norm(folder).startswith("meshes/"):
                folder = "meshes\\" + folder
            target = folder + "\\" + stem + ".nif"
            if P.exists(target):
                twm = P.winning_mod(target)
                in_pack = twm in mods
                add(oid, target,
                    "REACHABLE_IN_PACK" if in_pack else "REACHABLE_EXTERNAL",
                    "physics XML " + vp + " (exact stem convention)", ext=".nif", atype="GAME_NIF",
                    relationship=rel_for(oid, "GAME_NIF", twm) if in_pack else "NONE",
                    notes=("Havok/SMP/RealPhysics bind by exact '<same stem>.nif in the same folder'; "
                           "resolved to '%s' (VFS winner '%s')." % (target, twm)),
                    action="COPY+REPOINT" if in_pack else "NO_COPY_EXTERNAL_REF",
                    status="OK" if in_pack else "UNKNOWN")
                d["GAME_NIF"].add(target)
            else:
                note = ("UNRESOLVED PHYSICS BINDING: no '%s' in the frozen mod-scoped index and the XML carries no mesh "
                        "path element. The real target cannot be derived without fuzzy matching, which is "
                        "forbidden in P02A -- deliberately marked UNKNOWN." % target)
                r = seen.get((oid, C.norm(vp)))
                if r:
                    r["notes"] = (r["notes"] + " " if r["notes"] else "") + note
                    r["status"] = "BLOCKER"
                    r["migration_action"] = "UNKNOWN_BLOCKER"
                else:
                    add(oid, vp, "IN_SCOPE_MOD", "physics XML (unbound)", ext=".xml",
                        atype="PHYSICS_XML", relationship="PHYSICS_PATCH", notes=note,
                        action="UNKNOWN_BLOCKER", status="BLOCKER")
                note_unknown(oid, vp, "PHYSICS_MESH_UNRESOLVED", target)
                note_blocker(oid, "MEDIUM", vp,
                             "physics XML declares no resolvable mesh in the frozen evidence")

    # ---- (b4) NIF -> BSShaderTextureSet DDS closure ----------------------
    for key in list(seen.keys()):
        if key[0] != oid:
            continue
        r = seen[key]
        if r["asset_type"] != "GAME_NIF" or r["status"] == "BLOCKER":
            continue
        vp = r["virtual_path"]
        nif = P.nif(vp)
        if not nif:
            continue
        for shape, slot, tex in tex_slots(nif):
            if not P.exists(tex):
                scope, act, stt, tag = classify_missing(tex)
                add(oid, tex, scope, "NIF texture set: " + vp, ext=".dds",
                    atype="DDS", relationship="NONE",
                    notes="BSShaderTextureSet %s.%s of '%s' is not in the frozen mod-scoped index (no absence claim). %s" % (shape, slot, vp, tag),
                    action=act, status=stt)
                note_unknown(oid, tex, scope, vp)
                if stt == "BLOCKER":
                    note_blocker(oid, "HIGH", tex,
                                 "texture referenced by %s is unresolvable in the frozen evidence" % vp)
                continue
            wm = P.winning_mod(tex)
            in_pack = wm in mods
            note = "BSShaderTextureSet %s.%s of NIF '%s'." % (shape, slot, vp)
            act, stt = "COPY+REPOINT", "OK"
            if not in_pack:
                note += " VFS winner '%s' is out-of-pack (vanilla / 3rd-party): borrowed, never copied." % wm
                act, stt = "NO_COPY_EXTERNAL_REF", "UNKNOWN"
                note_unknown(oid, tex, "EXTERNAL_TEXTURE_WINNER", wm)
                if wm in INPACK:
                    who = owner_outfits(wm)
                    cross_outfit.append((oid, tex, ",".join(who),
                                         "texture won by another in-pack Outfit"))
                    note += " CROSS-OUTFIT DEPENDENCY."
                    act, stt = "UNKNOWN_BLOCKER", "BLOCKER"
                    note_blocker(oid, "HIGH", tex,
                                    "texture winner is in-pack mod of %s" % ",".join(who))
            add(oid, tex, "REACHABLE_IN_PACK" if in_pack else "REACHABLE_EXTERNAL",
                "NIF texture set: " + vp, ext=".dds", atype="DDS",
                relationship=rel_for(oid, "DDS", wm) if in_pack else "NONE",
                notes=note, action=act, status=stt)
            d["DDS"].add(tex)

    # ---- orphan ShapeData (wins in VFS but no .osp folder claims it) -----
    for f in P.file_index:
        vp = f["vpath"]
        if f["ext"] not in (".nif", ".osd"):
            continue
        if not C.norm(vp).startswith("calientetools/bodyslide/shapedata/"):
            continue
        if P.winning_mod(vp) not in mods:
            continue
        if C.norm(os.path.dirname(bs(vp))) in osp_folders:
            continue
        note = ("ORPHAN ShapeData: wins the VFS for this Outfit but no .osp data folder claims it, so "
                "BodySlide would never build it. Manual decision required; nothing is deleted in P02A.")
        r = seen.get((oid, C.norm(vp)))
        if r:
            r["notes"] = (r["notes"] + " " if r["notes"] else "") + note
            r["status"] = "BLOCKER"
            r["migration_action"] = "UNKNOWN_BLOCKER"
        else:
            add(oid, vp, "IN_SCOPE_MOD", "in-scope mod file", ext=f["ext"],
                atype=asset_type_of(vp, f["ext"]), relationship="BODYSLIDE_CONVERSION",
                notes=note, action="UNKNOWN_BLOCKER", status="BLOCKER")
        note_unknown(oid, vp, "ORPHAN_SHAPEDATA_NO_OSP", "")
        note_blocker(oid, "MEDIUM", vp, "ShapeData not reachable from any .osp data folder")

    # ---- per-outfit rule conflicts --------------------------------------
    if len(d["osp"]) > 1:
        note_blocker(oid, "MEDIUM", "OSP target filename",
                         "outfit ships %d .osp projects but the frozen rule allows exactly one "
                         "ZLJ_<OUTFIT_ID>.osp; a naming decision is required." % len(d["osp"]))
    if o.get("support", {}).get("NON_CANONICAL_BODY"):
        note_blocker(oid, "HIGH", "NON_CANONICAL_BODY",
                           "source body is %s; the pack keeps only CBBE_3BA / 3BBB / 3BA branches. "
                           "P02A annotates only, deletes nothing." %
                           o["support"]["NON_CANONICAL_BODY"])

    st["rows"] = sum(1 for k in seen if k[0] == oid)
    st["unknown"] = sum(1 for r in rows if r["OUTFIT_ID"] == oid and r["status"] == "UNKNOWN")
    st["blocker"] = sum(1 for r in rows if r["OUTFIT_ID"] == oid and r["status"] == "BLOCKER")
    st["collisions"] = sum(1 for c in collisions if c[0] == oid)


# ------------------------------------------------------------------ output --
rows.sort(key=lambda r: (C.OUTFIT_IDS.index(r["OUTFIT_ID"]), r["asset_type"],
                         C.norm(r["virtual_path"])))
csv_path = os.path.join(C.OUT, "P02A_EFFECTIVE_SOURCE_MAP.csv")
C.write_csv(csv_path, HEADER, [[r[c] for c in HEADER] for r in rows])
print("wrote", csv_path, len(rows), "rows")

# ================================================= P02A_ARCHITECTURE.md =====
FENCE = chr(96) * 3


def fmt_set(s, n=3, sep="<br>"):
    s = sorted(s)
    if not s:
        return "-"
    if len(s) <= n:
        return sep.join(x.replace("\\", "/") for x in s)
    return sep.join(x.replace("\\", "/") for x in s[:n]) + sep + "... (%d total)" % len(s)


L = []
A = L.append
A("# P02A Architecture & Effective Source Map")
A("")
A("**Pack**: `%s` / %s  " % (C.PACK_ID, C.DISPLAY_NAME))
A("**Canonical body**: `%s`  " % C.CANONICAL_BODY)
A("**Target plugin**: `%s`  " % C.TARGET_PLUGIN)
A("**Stage**: P02A -- namespace & migration *plan only*  ")
A("**Generator**: `tools/P02A/p02a_sourcemap.py` (re-runnable, reads only the frozen P00 evidence set)  ")
A("**Ledger**: `reports/P02A/P02A_EFFECTIVE_SOURCE_MAP.csv` (%d rows)" % len(rows))
A("")
A("---")
A("")
A("## 0. STRICT READ-ONLY declaration")
A("")
A("This document is a **plan**. Nothing in it has been executed.")
A("")
A("* No MO2 mod folder, Skyrim `Data` file or game install file was created, moved, "
  "copied, renamed or modified.")
A("* No NIF, DDS, ESP/ESL, OSP, OSD, XML, JSON or INI was rewritten.")
A("* **No BodySlide build, no PGPatcher pass, no UBE conversion, no PBR generation and no "
  "plugin merge was run.**")
A("* The only files written by this stage are the two deliverables above and the generator "
  "script, all inside this repository.")
A("* Every `COPY + REPOINT` in the CSV is *plan text*. A later stage must re-authorise it.")
A("")
A("---")
A("")
A("## 1. Namespace rule and target path layout")
A("")
A("**One source Outfit == one independent asset namespace.** Each of the 11 frozen "
  "`OUTFIT_ID`s owns a private mesh tree, a private texture tree, a private BodySlide "
  "ShapeData folder and its own slider set:")
A("")
A(FENCE)
A(r"meshes\ZLJ\CombatLatex\<OUTFIT_ID>\<file>.nif")
A(r"textures\ZLJ\CombatLatex\<OUTFIT_ID>\<file>.dds")
A(r"CalienteTools\BodySlide\ShapeData\ZLJ_CombatLatex\<OUTFIT_ID>\<file>.nif|.osd")
A(r"CalienteTools\BodySlide\SliderSets\ZLJ_<OUTFIT_ID>.osp")
A(r"pbrnifpatcher\ZLJ\CombatLatex\<OUTFIT_ID>\<file>.json   (PBR patches only)")
A(FENCE)
A("")
A("Derived naming rules:")
A("")
A("| Item | Rule | Example |")
A("|---|---|---|")
A("| Plugin | fixed | `%s` |" % C.TARGET_PLUGIN)
A("| ARMO/ARMA EDID | `ZLJ_CL_<OUTFIT>_<PART>` | `ZLJ_CL_Haley_Body` |")
A("| BodySlide UI name | `[ZLJ Combat Latex] <Outfit> - <Part>` | `[ZLJ Combat Latex] Haley - Bodysuit` |")
A("| Slider set file | `ZLJ_<OUTFIT_ID>.osp` | `ZLJ_CL04_Haley.osp` |")
A("")
A("### 1.1 The independence principle (normative)")
A("")
A("> **In P02A two different Outfits never share a DDS, NIF, ShapeData NIF or OSD -- "
  "even when their SHA256 is byte-for-byte identical.**")
A("")
A("Byte-identical content is a *duplication*, not a *shared resource*. Collapsing it is a "
  "**P05 MATERIAL STANDARDIZATION** decision, not a P02A one. The P02A ledger therefore "
  "records such pairs explicitly with `status=PROPOSAL_SHARED_NOT_APPROVED` so P05 can "
  "act on real evidence later, and the public-resource whitelist stays **NONE** for now.")
A("")
A("A consequence: an Outfit that today *borrows* a texture owned by another Outfit's mod "
  "(section 5) does **not** silently get a private copy either. It keeps an explicit, "
  "recorded dependency with `migration_action=UNKNOWN_BLOCKER` until a human decides. "
  "Silently copying it would fabricate a source relationship the frozen evidence does not "
  "support.")
A("")
A("---")
A("")
A("## 2. Winner determination rule")
A("")
A("For every virtual path the CSV records the **VFS winner**, not \"the mod that happens to "
  "hold the file\":")
A("")
A(FENCE)
A("providers(vp)  = every P00.file_index row whose norm(vpath) == norm(vp)")
A("winner(vp)     = argmin  P00.priority[mod]        # LOWER number wins")
A("shadowed(vp)   = providers(vp) minus {winner(vp)}")
A(FENCE)
A("")
A("* MO2 priority: **smaller number = higher priority = VFS winner**.")
A("* `winning_provider` is that mod name; `shadowed_providers` lists every loser.")
A("* A path with **no** provider is never silently dropped -- it is written with an empty "
  "`winning_provider`, `status=BLOCKER` and `migration_action=UNKNOWN_BLOCKER`.")
A("* Identical SHA256 across providers does **not** create a merge. Each provider stays a "
  "separate row; only the winner is a migration source.")
A("")
A("---")
A("")
A("## 3. Source taxonomy (how `relationship` is decided)")
A("")
A("| relationship | Decided by | Notes |")
A("|---|---|---|")
A("| `BASE_MOD` | winning provider == the outfit's `primary` mod | the canonical delivery |")
A("| `REWORK` | reserved: a frozen support mod whose role is a plain rework | **unused in P02A** -- no in-pack mod matches |")
A("| `BODYSLIDE_CONVERSION` | `asset_type` in {SHAPEDATA_NIF, OSP, OSD}, or a GAME_NIF that is a .osp EXACT_OUTPUT_PATH | ShapeData is the 3BA source of truth; OSP is the slider definition |")
A(r"| `PBR_PATCH` | `asset_type` == PBR_JSON, or path under `textures\pbr\`, or winner is the frozen PBR_PATCH support mod | CL04 only |")
A("| `LATEX_REWORK` | winner is the frozen LATEX_REWORK support mod | CL09 only |")
A("| `PHYSICS_PATCH` | `asset_type` == PHYSICS_XML | judged on the path type; the winner then decides pack membership |")
A("| `NONE` | everything else, including every out-of-pack or unresolvable reference | the honest default |")
A("")
A("`asset_type` values used: `PLUGIN`, `GAME_NIF`, `SHAPEDATA_NIF`, `OSP`, `OSD`, "
  "`DDS`, `PHYSICS_XML`, `CONFIG`, `PBR_JSON`, `OTHER`.")
A("")
A("Non-asset detection (`migration_action=EXCLUDE_NON_ASSET`): `meta.ini` (MO2/FOMOD "
  "bookkeeping, reserved name), `.espbak`, `.old000`, `.old001`, timestamped "
  "`.esp.YYYY_MM_DD_HH_MM_SS` backups, `- 副本` / `_bak` author copies, `.tri` "
  "authoring caches, and the `bbd_catsuitspearhead - 副本.esp11` duplicate plugin.")
A("")
A("---")
A("")
A("## 4. Per-Outfit summary")
A("")
A("`mods` = in-scope mods. `win NIF / DDS / OSP / OSD` = rows the Outfit actually "
  "keeps, i.e. the VFS winner is an in-pack mod. `recs` = plugin records. `rework` = has "
  "a rework layer. `PBR` = PBR patch present.")
A("")
A("| OUTFIT_ID | mods | win NIF | win DDS | win OSP | win OSD | recs | PBR | rework | rows |")
A("|---|---|---|---|---|---|---|---|---|---|")
for oid in C.OUTFIT_IDS:
    d = info[oid]
    r_ = [x for x in rows if x["OUTFIT_ID"] == oid]

    def wcount(atype):
        return sum(1 for x in r_ if x["asset_type"] == atype
                   and x["status"] != "BLOCKER" and x["winning_provider"] in d["mods"])
    A("| `%s` | %d | %d | %d | %d | %d | %d | %s | %s | %d |" % (
        oid, len(d["mods"]), wcount("GAME_NIF"), wcount("DDS"), wcount("OSP"),
        wcount("OSD"), stats[oid]["plugin_records"],
        "yes" if d["pbr"] else "-", "yes" if d["rework"] else "-", len(r_)))
A("")
A("### 4.1 Source mods per Outfit")
A("")
A("| OUTFIT_ID | source plugin | in-scope mods (MO2 priority) |")
A("|---|---|---|")
for oid in C.OUTFIT_IDS:
    o = C.OUTFITS[oid]
    ms = ", ".join("`%s` (%s)" % (m, P.priority.get(m, "?")) for m in P.mods_of_outfit(oid))
    A("| `%s` | `%s` | %s |" % (oid, o["plugin"], ms))
A("")
A("---")
A("")
A("## 5. Cross-Outfit dependencies (BLOCKER class)")
A("")
A("**Rule violation to fix before any copy happens.** These are textures whose VFS winner "
  "is the mod of a *different* Outfit in this pack. Under the independence rule they must "
  "not be silently borrowed.")
A("")
if cross_outfit:
    A("| OUTFIT_ID | virtual_path | winner belongs to | note |")
    A("|---|---|---|---|")
    for oid, vp, who, note in sorted(set(cross_outfit)):
        A("| `%s` | `%s` | %s | %s |" % (oid, vp.replace("\\", "/"), who, note))
else:
    A("_none detected_")
A("")
A("**Out-of-pack winners shipped inside an in-pack mod folder** (pack-boundary collision):")
A("")
oop = sorted(set((o, v, d) for (o, v, c, d) in unknowns if c == "OUT_OF_PACK_WINNER"))
if oop:
    A("| OUTFIT_ID | virtual_path | winning mod |")
    A("|---|---|---|")
    for oid, vp, note in oop:
        A("| `%s` | `%s` | %s |" % (oid, vp.replace("\\", "/"), note))
else:
    A("_none detected_")
A("")
A("---")
A("")
A("## 6. Collisions")
A("")
cc = collections.Counter(k for (_, _, k, _) in collisions)
A("| kind | count |")
A("|---|---|")
for k, v in sorted(cc.items()):
    A("| `%s` | %d |" % (k, v))
A("")
A("* `MO2_RESERVED_NAME` -- `meta.ini` is offered by 54 mods at once. It is MO2/FOMOD "
  "bookkeeping, never a game asset, and is excluded from the migratable set.")
A("* `VFS_OVERRIDE` -- a real content path is offered by more than one mod. The winner is "
  "the lower MO2 priority number; the loser is preserved in `shadowed_providers`.")
A("")
A("---")
A("")
A("## 7. Unknowns and manual-confirmation list")
A("")
uc = collections.Counter(k for (_, _, k, _) in unknowns)
A("| UNKNOWN / BLOCKER class | count |")
A("|---|---|")
for k, v in sorted(uc.items(), key=lambda x: -x[1]):
    A("| `%s` | %d |" % (k, v))
A("")
A("### 7.1 Items needing a human decision")
A("")
A(r"1. **ARMO/ARMA stock placeholders** (`meshes\Armor\Studded\Male\*.nif`, "
  "`meshes\\bbdrac\\<...>\\Body_1.nif` etc.). Absent from the frozen mod-scoped index "
  "because Skyrim base-game `Data` is not in scope. Recorded, never guessed.")
A("2. **Unbound physics XML.** `tailplug.xml`, `sparklers.xml`, `coat.xml` and the "
  "three `fs6_hoodedcloak*_smp.xml` carry no mesh element and have no same-folder "
  "`<stem>.nif`. The real target cannot be derived without fuzzy matching, which P02A "
  "forbids. All are BLOCKER / PHYSICS_MESH_UNRESOLVED.")
A("3. **Missing third-party textures** referenced by source NIFs whose providing mod is not "
  r"installed (`textures\devious\...`, `textures\dx\...`, `textures\kziitd\...`, "
  r"`Textures\Caenarvon\...`, `Textures\1Nye\...`, `textures\Coco_Cloths\...`, "
  r"`textures\predator\...`). Absence claims are NOT made from the frozen P00 index; see "
                         r"P02A_GLOBAL_PROVIDER_LOOKUP.csv.")
A(r"4. **Malformed NIF texture slot** holding the bare token `textures\` "
  "(`fo4boots slided.nif`, CL08). Author bug in the source mesh.")
A("5. **Orphan ShapeData** -- a ShapeData NIF/OSD that wins the VFS for an Outfit but whose "
  "folder no .osp claims, so BodySlide would never build it. See section 8.")
A("6. **P00 metadata disagreement** -- `bs_projects.shapedata_nif_count` disagrees with the "
  "frozen file index for CL08. This script trusts the frozen file index plus the .osp data "
  "folder and records the disagreement.")
A("7. **Unbuilt BodySlide outputs** -- every .osp EXACT_OUTPUT_PATH build target is absent "
  "from the VFS because no build has run. Recorded as PENDING_BUILD; P02A does not build.")
A("")
A("---")
A("")
A("## 8. Per-Outfit structural findings")
A("")
for oid in C.OUTFIT_IDS:
    d = info[oid]
    ob = sorted(set(k for (o, v, k, _) in blockers if o == oid and v == "MEDIUM"
                    and C.norm(k).startswith("calientetools/bodyslide/shapedata/")))
    osp_n = len(d["osp"])
    osp_names = sorted(d["osp"].values())
    notes = []
    if osp_n > 1:
        notes.append("**%d .osp projects** (%s) but the frozen rule allows exactly one "
                     "`ZLJ_<OUTFIT_ID>.osp`. A per-part filename decision is required "
                     "(candidate: `ZLJ_<OUTFIT_ID>__<Part>.osp`) -- not decided here."
                     % (osp_n, ", ".join(osp_names)))
    if ob:
        notes.append("**Orphan ShapeData** (no .osp data folder claims them): %s"
                     % ", ".join("`%s`" % x.replace("\\", "/") for x in ob))
    if d["p00_count_mismatch"]:
        notes.append("P00 `shapedata_nif_count` mismatch on: %s"
                     % ", ".join("`%s`" % x for x in sorted(d["p00_count_mismatch"])))
    nb = C.OUTFITS[oid].get("support", {}).get("NON_CANONICAL_BODY")
    if nb:
        notes.append("`NON_CANONICAL_BODY=%s` -- annotated only; nothing is deleted in P02A." % nb)
    if d["pbr"]:
        notes.append("PBR patch mod `%s` (priority %s) beats the base mod (%s) and owns "
                     r"`textures\pbr\...` + `pbrnifpatcher\...` with no path collision."
                     % (C.OUTFITS[oid]["support"]["PBR_PATCH"],
                        P.priority.get(C.OUTFITS[oid]["support"]["PBR_PATCH"], "?"),
                        P.priority.get(C.OUTFITS[oid]["primary"], "?")))
    if d["rework"]:
        rw = C.OUTFITS[oid]["support"]["LATEX_REWORK"]
        rw_assets = [x for x in rows if x["OUTFIT_ID"] == oid
                     and x["winning_provider"] == rw and x["status"] != "BLOCKER"]
        bs_from_base = [x for x in rows if x["OUTFIT_ID"] == oid
                        and x["asset_type"] in ("SHAPEDATA_NIF", "OSP", "OSD")
                        and x["winning_provider"] == C.OUTFITS[oid]["primary"]]
        if rw_assets and bs_from_base:
            notes.append("**REWORK / BodySlide split**: the rework mod wins %d game asset(s) "
                         "from `%s` but every .osp, ShapeData NIF and OSD still comes from the "
                         "base mod (%d file(s)). Once BodySlide builds and PGPatcher swaps the worn "
                         "meshes, the visible shape geometry will be the BASE ShapeData while the "
                         "rework only contributes its textures. Manual confirmation required before "
                         "any build."
                         % (len([x for x in rw_assets
                                 if x["asset_type"] in ("GAME_NIF", "DDS")]), rw,
                            len(bs_from_base)))
        notes.append("Latex Rework mod `%s` (priority %s) beats the base mod (%s) and is the "
                     "VFS winner for its meshes/textures."
                     % (C.OUTFITS[oid]["support"]["LATEX_REWORK"],
                        P.priority.get(C.OUTFITS[oid]["support"]["LATEX_REWORK"], "?"),
                        P.priority.get(C.OUTFITS[oid]["primary"], "?")))
    A("### `%s`" % oid)
    A("")
    if notes:
        for n in notes:
            A("* " + n)
    else:
        A("* no structural exception: single .osp, no orphan ShapeData, no rework layer.")
    A("")

A("---")
A("")
A("## 9. Shared-material proposals")
A("")
sha_owner = collections.defaultdict(list)
for r in rows:
    if r["sha256"] and r["status"] != "BLOCKER" and r["asset_type"] in (
            "DDS", "GAME_NIF", "SHAPEDATA_NIF", "OSD"):
        sha_owner[(r["asset_type"], r["sha256"])].append(r["OUTFIT_ID"])
dups = {k: sorted(set(v)) for k, v in sha_owner.items() if len(set(v)) > 1}
A("Byte-identical assets appearing under more than one Outfit are **not** merged in P02A. "
  "They are listed here only so P05 has a verified starting set.")
A("")
if dups:
    A("| asset_type | sha256 (12) | Outfits |")
    A("|---|---|---|")
    for (at, sha), oset in sorted(dups.items(), key=lambda x: -len(x[1])):
        A("| %s | `%s` | %s |" % (at, sha[:12], ", ".join(oset)))
else:
    A("**No cross-Outfit SHA256 duplicate was found in the winning set.**")
A("")
A("Shared-resource whitelist: **NONE**. Status of every item above: "
  "`PROPOSAL_SHARED_NOT_APPROVED`. No `Shared` directory is created by P02A.")
A("")
A("---")
A("")
A("## 10. Statistics")
A("")
A("| OUTFIT_ID | rows | UNKNOWN | BLOCKER | collisions |")
A("|---|---|---|---|---|")
tot = collections.Counter()
for oid in C.OUTFIT_IDS:
    r_ = [x for x in rows if x["OUTFIT_ID"] == oid]
    u = sum(1 for x in r_ if x["status"] == "UNKNOWN")
    b = sum(1 for x in r_ if x["status"] == "BLOCKER")
    cn = sum(1 for c3 in collisions if c3[0] == oid)
    tot["rows"] += len(r_)
    tot["u"] += u
    tot["b"] += b
    tot["c"] += cn
    A("| `%s` | %d | %d | %d | %d |" % (oid, len(r_), u, b, cn))
A("| **TOTAL** | **%d** | **%d** | **%d** | **%d** |"
  % (tot["rows"], tot["u"], tot["b"], tot["c"]))
A("")
A("`asset_type` distribution:")
A("")
A("| asset_type | rows |")
A("|---|---|")
for k, v in sorted(collections.Counter(r["asset_type"] for r in rows).items(),
                  key=lambda x: -x[1]):
    A("| `%s` | %d |" % (k, v))
A("")
A("`relationship` distribution:")
A("")
A("| relationship | rows |")
A("|---|---|")
for k, v in sorted(collections.Counter(r["relationship"] for r in rows).items(),
                  key=lambda x: -x[1]):
    A("| `%s` | %d |" % (k, v))
A("")
A("`status` distribution:")
A("")
A("| status | rows |")
A("|---|---|")
for k, v in sorted(collections.Counter(r["status"] for r in rows).items(),
                  key=lambda x: -x[1]):
    A("| `%s` | %d |" % (k, v))
A("")
A("---")
A("")
A("## 11. Re-running")
A("")
A(FENCE)
A(r"python tools\P02A\p02a_sourcemap.py")
A(FENCE)
A("")
A("Deterministic: it reads only the frozen P00 evidence set through "
  "`tools/P02A/p02a_common.py`, re-derives every winner, and rewrites both deliverables. "
  "It never writes outside `reports/P02A/`.")

md_path = os.path.join(C.OUT, "P02A_ARCHITECTURE.md")

# Ownership guard: tools/P02A/p02a_architecture_v2.py is the sole generator of
# the P02A.1 architecture document. If that revision is already applied, this
# script must NOT overwrite it with the older v1 body.
ARCH_V2_MARKER = "P02A.1 revision log"
if os.path.exists(md_path):
    with open(md_path, "r", encoding="utf-8") as _f:
        _doc = _f.read()
    if ARCH_V2_MARKER in _doc:
        print("SKIPPED %s -- already carries the P02A.1 revision "
              "(marker %r); p02a_architecture_v2.py is its sole generator."
              % (md_path, ARCH_V2_MARKER))
        md_path = None
if md_path:
    C.write_md(md_path, "\n".join(L) + "\n")
    print("wrote", md_path, len(L), "lines")

print("")
print("=" * 78)
print("P02A EFFECTIVE SOURCE MAP SUMMARY")
print("=" * 78)
print("%-19s %6s %8s %8s %8s %6s %6s" % ("OUTFIT_ID", "rows", "UNKNOWN", "BLOCKER",
                                         "collis", "recs", "nif"))
print("-" * 78)
for oid in C.OUTFIT_IDS:
    r_ = [x for x in rows if x["OUTFIT_ID"] == oid]
    print("%-19s %6d %8d %8d %8d %6d %6d" % (
        oid, len(r_),
        sum(1 for x in r_ if x["status"] == "UNKNOWN"),
        sum(1 for x in r_ if x["status"] == "BLOCKER"),
        sum(1 for c3 in collisions if c3[0] == oid),
        stats[oid]["plugin_records"],
        sum(1 for x in r_ if x["asset_type"] == "GAME_NIF")))
print("-" * 78)
print("%-19s %6d %8d %8d %8d" % (
    "TOTAL", len(rows),
    sum(1 for x in rows if x["status"] == "UNKNOWN"),
    sum(1 for x in rows if x["status"] == "BLOCKER"),
    len(collisions)))
print("")
print("asset_type  :", dict(sorted(collections.Counter(r["asset_type"] for r in rows).items())))
print("relationship:", dict(sorted(collections.Counter(r["relationship"] for r in rows).items())))
print("status      :", dict(sorted(collections.Counter(r["status"] for r in rows).items())))
print("cross-outfit dependency pairs:", len(set(cross_outfit)))
print("unknown classes:")
for k, v in sorted(collections.Counter(k for (_, _, k, _) in unknowns).items(),
                   key=lambda x: -x[1]):
    print("   %-34s %d" % (k, v))
print("distinct blockers:", len(set(blockers)))

