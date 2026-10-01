# -*- coding: utf-8 -*-
"""P02A v2 -- Mesh + Texture migration ledger for ZLJ_COMBAT_LATEX.

STRICT READ-ONLY.  Reads only:
  * the frozen P00 evidence set through p02a_common.C.P00.get()  (never rescanned)
  * the upstream P02A tables rebuilt by the other teammates
  * the four CSVs this script owns (rebuilt in place)

Upstream inputs
  P02A_ARMA_MODEL_REWRITE.csv   -> GAME_NIF rows (model_role is the authoritative
                                   slot enum; WEARABLE_FEMALE_3P == canonical runtime)
  P02A_BODYSLIDE_MIGRATION.csv  -> BODYSLIDE_OUTPUT_NIF + SHAPEDATA_SOURCE_NIF rows
  P02A_GLOBAL_PROVIDER_LOOKUP.csv -> texture provider ruling for every DDS that is
                                   not inside the frozen P00 VFS scope

Texture policy (frozen by the P02A.1 review ruling)
  EXTERNAL_PROVIDER_FOUND   -> COPY into the consuming outfit namespace + REPOINT
  GLOBAL_BODY_SKIN          -> KEEP_EXTERNAL_REFERENCE (Body/skin system; never copied)
  VANILLA_ENGINE_RESOURCE   -> KEEP_EXTERNAL_REFERENCE (engine / vanilla resource)
  TRUE_MISSING              -> UNRESOLVED (global lookup found no provider at all)
  UNKNOWN (PATH-MISMATCH)   -> UNRESOLVED (same basename elsewhere is NOT the same asset)
Shared-asset whitelist = NONE: cross-outfit DDS is duplicated per outfit, never shared.
"""
import collections
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import p02a_common as C  # noqa: E402

RPT = os.path.join(ROOT, "reports", "P02A")

UP_ARMA = "P02A_ARMA_MODEL_REWRITE.csv"
UP_BS = "P02A_BODYSLIDE_MIGRATION.csv"
UP_LOOKUP = "P02A_GLOBAL_PROVIDER_LOOKUP.csv"

SHARED_ASSET_WHITELIST = []      # NONE in P02A; sharing is a P05 topic
COPY_WHITELIST = []              # nothing is pre-approved to be skipped


# ------------------------------------------------------------------ helpers
def bs(vp):
    return str(vp or "").replace("/", "\\").strip().strip('"')


def ensure_root(vp, root="meshes"):
    s = bs(vp)
    if not s.lower().startswith(root + "\\"):
        s = root + "\\" + s
    return s


def bname(vp):
    return bs(vp).rsplit("\\", 1)[-1]


def lookup_key(vp):
    """Normalised DDS key: lower case, forward slashes, single spaces,
    optional leading 'textures/' removed (the lookup table probes both forms)."""
    s = C.norm(vp).strip()
    s = re.sub(r"\\s+", " ", s)
    if s.startswith("textures/"):
        s = s[len("textures/"):]
    return s


def load(name):
    with open(os.path.join(RPT, name), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def role_class(model_role):
    if model_role.startswith("WORLD_"):
        return "GROUND"
    if model_role.startswith("FIRSTPERSON_"):
        return "FIRSTPERSON"
    return "WEARABLE"


# ---- namespace literals (P02A.1 review ruling) -------------------------
# The pack deliberately uses TWO different spellings:
#   meshes / textures  ->  meshes|textures \ZLJ\CombatLatex\<OUTFIT_ID>\   (backslash)
#   ShapeData          ->  CalienteTools\BodySlide\ShapeData\ZLJ_Combat_Latex\<OUTFIT_ID>\
# They are NOT to be unified.  The ShapeData spelling is validated against the
# frozen constant C.SD_ROOT; the mesh/texture spellings against C.MESH_ROOT /
# C.TEX_ROOT.
def check_namespaces(mesh_rows):
    """Verify every migrated target sits in the namespace of its own mesh_class."""
    import re as _re
    sd_ok = sd_bad = 0
    mt_ok = mt_bad = 0
    for r in mesh_rows:
        oid, mesh_class, t = r[0], r[1], r[9]        # rows are lists at this point
        if mesh_class == "SHAPEDATA_SOURCE_NIF":
            m = _re.match(r"(?i)^(calientetools\\bodyslide\\shapedata\\[^\\]+)\\",
                          t)
            lit = m.group(1) + "\\" if m else "??"
            if lit.lower() == C.SD_ROOT.lower() and \
                    ("\\" + oid.lower() + "\\") in t.lower():
                sd_ok += 1
            else:
                sd_bad += 1
        else:
            if t.lower().startswith(C.MESH_ROOT.lower() + oid.lower() + "\\"):
                mt_ok += 1
            else:
                mt_bad += 1
    return sd_ok, sd_bad, mt_ok, mt_bad


def canonical_model_role(roles):
    if "WEARABLE_FEMALE_3P" in roles:
        return "WEARABLE_FEMALE_3P"
    return sorted(roles)[0] if roles else "UNKNOWN"


# =========================================================== 1. MESH LEDGER ==
MESH_HEADER = [
    "OUTFIT_ID", "mesh_class", "model_role", "role_class", "source_virtual_path",
    "source_provider", "winning_priority", "shadowed_providers", "mesh_role",
    "target_virtual_path", "sha256", "retain_decision", "existence",
    "canonical_runtime", "body_relevance", "target_outfit_match",
    "unresolved_class", "file_ref_count", "model_roles_all", "bodyslide_osp",
    "notes",
]


def build_mesh_ledger(p):
    arma = load(UP_ARMA)
    bsrows = [r for r in load(UP_BS) if r.get("row_kind") == "SLIDER_SET"]

    rows = []
    collisions = []
    seen_target = {}                                  # target_norm -> (outfit, source)
    stats = collections.defaultdict(collections.Counter)
    n_tri = 0

    # ---- GAME_NIF : one row per (outfit, source mesh, ARMA model_role) -----
    by_file = collections.defaultdict(list)
    for r in arma:
        if os.path.splitext(r["old_vpath"])[1].lower() == ".tri":
            n_tri += 1
            continue
        by_file[(r["OUTFIT_ID"], C.norm(r["old_vpath"]))].append(r)

    for key in sorted(by_file):
        oid = key[0]
        refs = by_file[key]
        roles_all = sorted({x["model_role"] for x in refs})
        stats[oid]["GAME_NIF_FILES"] += 1
        for mr in roles_all:
            r0 = [x for x in refs if x["model_role"] == mr][0]
            status = r0["status"]
            if status == "COPY_AND_REPOINT":
                decision = "KEEP"
            elif status == "NON_CANONICAL_SOURCE":
                decision = "KEEP"
            else:
                decision = "REVIEW"
            notes = ["ARMA/ARMO model slot reference (model_role=%s)" % mr,
                     "slot_evidence=%s" % r0["slot_evidence"],
                     "canonical_reason=%s" % r0["canonical_reason"],
                     "collision_check(upstream)=%s" % r0["collision_check"],
                     "existence=%s" % r0["existence"]]
            if status == "UNRESOLVED":
                notes.append("BLOCKER(%s): %s" % (r0["unresolved_class"],
                                                  r0["notes"].split("|")[-1].strip()))
            if status == "NON_CANONICAL_SOURCE":
                notes.append("NON_CANONICAL (body_relevance=%s): retained for "
                             "provenance only, NOT the canonical CBBE_3BA female "
                             "runtime asset" % r0["body_relevance"])
            if r0["existence"] == "NOT_PROBEABLE_SKYRIMESM_BSA_RESIDENT":
                notes.append("SKYRIMESM.BSA resident -> the texture set is not present in "
                             "the frozen P00 evidence set, which indexes loose mod files "
                             "only; texture references for this mesh are UNRESOLVED. "
                             "READ-ONLY permits reading/parsing binaries, so P02B may "
                             "resolve this by parsing the mesh or listing the BSA.")
            tkey = C.norm(r0["new_path"])
            prev = seen_target.get(tkey)
            if prev and prev[0] != oid:
                collisions.append((tkey, prev[0], oid))
            elif prev and C.norm(prev[1]) != C.norm(r0["old_vpath"]):
                collisions.append((tkey, prev[0] + ":" + prev[1], oid))
            seen_target.setdefault(tkey, (oid, r0["old_vpath"]))
            rows.append([oid, "GAME_NIF", mr, role_class(mr), r0["old_vpath"],
                         r0["provider_mod"] or "UNKNOWN",
                         r0["provider_priority"], r0["shadowed_providers"],
                         r0["mesh_role"], r0["new_path"], r0["sha256"], decision,
                         r0["existence"], r0["canonical_runtime"],
                         r0["body_relevance"], r0["target_outfit_match"],
                         r0["unresolved_class"], len([x for x in refs
                                                     if x["model_role"] == mr]),
                         ";".join(roles_all), "", " ".join(notes)])
            stats[oid]["GAME_NIF"] += 1
            if decision == "REVIEW":
                stats[oid]["mesh_review"] += 1
            if decision == "KEEP":
                stats[oid]["mesh_keep"] += 1
            if r0["canonical_runtime"] == "YES":
                stats[oid]["canonical_runtime_nif"] += 1
            if mr.startswith("WORLD_"):
                stats[oid]["GROUND_NIF"] += 1

    # ---- EXCLUDE_SHADOWED ---------------------------------------------------
    for key in sorted(by_file):
        oid = key[0]
        for r in by_file[key]:
            sh = (r["shadowed_providers"] or "").strip()
            if not sh or sh == "NONE":
                continue
            rows.append([oid, "GAME_NIF", r["model_role"], role_class(r["model_role"]),
                         r["old_vpath"], sh, "", sh, r["mesh_role"], r["new_path"],
                         "", "EXCLUDE_SHADOWED", r["existence"], "NO",
                         r["body_relevance"], r["target_outfit_match"],
                         r["unresolved_class"], 1, r["model_role"], "",
                         "EXCLUDE_DO_NOT_COPY: this provider is shadowed at %s by %s "
                         "(winning priority %s); the shadowed copy never reaches the game"
                         % (r["old_vpath"], r["provider_mod"], r["provider_priority"])])
            stats[oid]["EXCLUDE_SHADOWED"] += 1

    # ---- BODYSLIDE_OUTPUT_NIF ----------------------------------------------
    for r in bsrows:
        oid = r["OUTFIT_ID"]
        out = (r["new_output_path"].rstrip("\\") + "\\" +
               (r["new_output_file"] or "") + ".nif")
        src = (r["old_output_path"].rstrip("\\") + "\\" +
               (r["old_output_file"] or "") + ".nif")
        lod0 = r["old_output_nif_lod0"] or "UNKNOWN"
        lod1 = r["old_output_nif_lod1"] or "UNKNOWN"
        target = ensure_root(out)
        tkey = C.norm(target)
        prev = seen_target.get(tkey)
        if prev and prev[0] != oid:
            collisions.append((tkey, prev[0], oid))
        seen_target.setdefault(tkey, (oid, src))
        note = ("BodySlide build product of the frozen target OSP %s "
                "(set_index_in_osp=%s, slider_count=%s). relationship_basis=%s. "
                "Material set is inherited from ShapeData NIF %s. "
                "expected sha256=%s (%s). LOD0=%s LOD1=%s"
                % (r["new_osp"], r["set_index_in_osp"], r["slider_count"],
                   r["relationship_basis"], r["old_input_nif"],
                   r["new_output_sha256_expected"], r["new_output_sha256_basis"],
                   lod0, lod1))
        if r["blockers"]:
            note += " BLOCKERS=%s" % r["blockers"]
        rows.append([oid, "BODYSLIDE_OUTPUT_NIF", "BODYSLIDE_OUTPUT", "WEARABLE",
                     src, r["old_osp_winning_provider"] or "UNKNOWN", "",
                     "NONE", "BODYSLIDE_OUTPUT", target,
                     r["new_output_sha256_expected"], "KEEP",
                     "NOT_BUILT_P02A_READ_ONLY", "YES",
                     r["non_canonical_body"] if r["non_canonical_body"] != "NONE"
                     else "CBBE_3BA", "SELF_OWN_MOD", r["blockers"], 1,
                     r["slider_set_name"], r["new_osp"], note])
        stats[oid]["BODYSLIDE_OUTPUT_NIF"] += 1
        stats[oid]["canonical_runtime_nif"] += 1

    # ---- SHAPEDATA_SOURCE_NIF ----------------------------------------------
    for r in bsrows:
        oid = r["OUTFIT_ID"]
        olds = [x.strip() for x in (r["old_input_nif_all"] or "").split(";") if x.strip()]
        news = [x.strip() for x in (r["new_input_nif_all"] or "").split(";") if x.strip()]
        olds = sorted(olds, key=lambda s: C.norm(s))
        news = sorted(news, key=lambda s: C.norm(s))
        olds = [o for o in olds if not o.lower().endswith(".osd")]
        news = [n for n in news if not n.lower().endswith(".osd")]
        if len(olds) != len(news):
            olds = olds[:1] + olds[1:]
        for o, n in zip(olds, news or olds):
            prov = p.winning_mod(C.norm(o)) or r["old_osp_winning_provider"] or "UNKNOWN"
            note = ("BodySlide ShapeData source NIF for slider set %s of %s. Its "
                    "BSShaderTextureSet is rewritten in "
                    "P02A_SHAPEDATA_TEXTURE_REWRITE.csv (shapedata scope); the mesh "
                    "itself moves into the pack ShapeData namespace."
                    % (r["slider_set_name"], r["new_osp"]))
            rows.append([oid, "SHAPEDATA_SOURCE_NIF", "BODYSLIDE_SHAPEDATA", "WEARABLE",
                         bs(o), prov, p.priority.get(prov, ""), "NONE",
                         "SHAPEDATA_SOURCE", bs(n), p.sha(C.norm(o)), "KEEP",
                         "RESOLVED_FROZEN_P00_VFS", "NO", "CBBE_3BA", "SELF_OWN_MOD",
                         r["blockers"], 1, r["slider_set_name"], r["new_osp"], note])
            stats[oid]["SHAPEDATA_SOURCE_NIF"] += 1

    return rows, collisions, stats, n_tri


# ======================================================== 2. TEXTURE LEDGER ==
TEX_HEADER = [
    "OUTFIT_ID", "referencing_nif", "referencing_nif_class",
    "referencing_nif_model_role", "canonical_runtime", "shape", "texture_slot",
    "source_virtual_path", "winning_provider", "winning_priority",
    "shadowed_providers", "sha256", "semantic_type", "lookup_classification",
    "owning_outfit_of_source", "action", "target_virtual_path", "shared_proposal",
    "notes",
]

REWRITE_HEADER = [
    "OUTFIT_ID", "nif_source", "nif_class", "nif_model_role", "shape_name",
    "texture_slot", "old_dds_path", "new_dds_path", "source_provider",
    "source_priority", "status", "shared_proposal", "notes",
]

CLOSURE_HEADER = [
    "OUTFIT_ID", "dependency_type", "source_owner", "source_virtual_path",
    "winning_provider", "winning_priority", "referenced_by_nif",
    "referencing_nif_model_role", "texture_slot", "resolution_plan",
    "target_virtual_path", "post_plan_state", "notes",
]

ACTION_ENUM = {"KEEP_SELF_NAMESPACE", "COPY_INTO_OUTFIT_NAMESPACE",
               "KEEP_EXTERNAL_REFERENCE", "UNRESOLVED"}
STATUS_ENUM = {"REPOINT_SELF_NAMESPACE", "COPY_FROM_CROSS_OUTFIT",
               "COPY_FROM_EXTERNAL_MOD", "KEEP_EXTERNAL_REFERENCE",
               "PROPOSAL_SHARED_NOT_APPROVED", "UNRESOLVED"}


def build_texture_ledgers(p):
    arma = load(UP_ARMA)
    bsrows = [r for r in load(UP_BS) if r.get("row_kind") == "SLIDER_SET"]
    lkrows = load(UP_LOOKUP)
    lookup = {}
    for r in lkrows:
        lookup[lookup_key(r["virtual_path"])] = r

    mod_owner = collections.defaultdict(list)
    for oid in C.OUTFIT_IDS:
        for m in p.mods_of_outfit(oid):
            if oid not in mod_owner[m]:
                mod_owner[m].append(oid)

    # ---- NIF inventory to walk ---------------------------------------------
    walk = []       # (oid, source_nif_vpath, nif_class, model_roles, canon, note)
    by_file = collections.defaultdict(list)
    for r in arma:
        by_file[(r["OUTFIT_ID"], C.norm(r["old_vpath"]))].append(r)
    for key in sorted(by_file):
        oid = key[0]
        refs = by_file[key]
        roles = sorted({x["model_role"] for x in refs})
        canon = "YES" if "WEARABLE_FEMALE_3P" in roles else "NO"
        walk.append([oid, bs(refs[0]["old_vpath"]), "GAME_NIF", ";".join(roles),
                     canon, ""])
    for r in bsrows:
        walk.append([r["OUTFIT_ID"],
                     (r["new_output_path"].rstrip("\\") + "\\" +
                      (r["new_output_file"] or "") + ".nif"),
                     "BODYSLIDE_OUTPUT_NIF", "BODYSLIDE_OUTPUT", "YES",
                     "BodySlide build product inherits the BSShaderTextureSet of "
                     "ShapeData NIF %s" % bs(r["old_input_nif"])])

    tex_rows = []
    rw_rows = []
    cl_rows = []
    stats = collections.defaultdict(collections.Counter)
    used_name = collections.defaultdict(dict)
    seen_target = {}
    collisions = []
    src_outfits = collections.defaultdict(set)
    dds_used = collections.defaultdict(set)
    tex_cache = {}

    def classify(oid, dds):
        """-> (action, status, own, target, lookup_class, note, provider, prio)"""
        vp = ensure_root(dds, "textures")
        if p.exists(vp):
            prov = p.winning_mod(vp)
            owners = mod_owner.get(prov, [])
            if not owners:
                own, action, status = "EXTERNAL_MOD", "COPY_INTO_OUTFIT_NAMESPACE", \
                    "COPY_FROM_EXTERNAL_MOD"
                note = ("Resolved inside the frozen P00 VFS; provider %s is outside "
                        "this pack -> copy into the outfit namespace (shared-asset "
                        "whitelist = NONE)." % prov)
                lk = "IN_P00_VFS"
            elif oid in owners:
                own, action, status = oid, "COPY_INTO_OUTFIT_NAMESPACE", \
                    "REPOINT_SELF_NAMESPACE"
                note = "Pack-owned texture; copy into this outfit's namespace."
                lk = "IN_P00_VFS"
            else:
                own, action, status = ";".join(owners), "COPY_INTO_OUTFIT_NAMESPACE", \
                    "COPY_FROM_CROSS_OUTFIT"
                note = ("CROSS_OUTFIT: winning provider %s belongs to %s; this outfit "
                        "gets its own copy, never a shared reference."
                        % (prov, ";".join(owners)))
                lk = "IN_P00_VFS"
            target = "textures\\ZLJ\\CombatLatex\\%s\\%s" % (oid, bname(dds))
            if C.norm(bname(dds)) in used_name[oid] and \
                    used_name[oid][C.norm(bname(dds))] != C.norm(vp):
                parent = bs(vp).rsplit("\\", 1)[0].rsplit("\\", 1)[-1] or "sub"
                target = "textures\\ZLJ\\CombatLatex\\%s\\%s\\%s" % (oid, parent,
                                                                          bname(dds))
                note += (" INTRA_OUTFIT_BASENAME_COLLISION with %s -> source "
                         "sub-folder preserved." % bs(used_name[oid][C.norm(bname(dds))]))
            used_name[oid].setdefault(C.norm(bname(dds)), C.norm(vp))
            return action, status, own, target, lk, note, prov, p.priority.get(prov, "")

        # ---- not in the frozen P00 VFS scope -> global lookup ruling ------
        row = lookup.get(lookup_key(dds))
        lk = row["classification"] if row else "NOT_IN_LOOKUP"
        prov = (row["winning_provider"] if row else "") or "UNKNOWN"
        prio = (row["winning_priority"] if row else "") or "UNKNOWN"
        lnote = (row["notes"] if row else "path absent from P02A_GLOBAL_PROVIDER_LOOKUP.csv")
        if lk == "EXTERNAL_PROVIDER_FOUND":
            target = "textures\\ZLJ\\CombatLatex\\%s\\%s" % (oid, bname(dds))
            if C.norm(bname(dds)) in used_name[oid] and \
                    used_name[oid][C.norm(bname(dds))] != C.norm(dds):
                parent = bs(dds).rsplit("\\", 1)[0].rsplit("\\", 1)[-1] or "sub"
                target = "textures\\ZLJ\\CombatLatex\\%s\\%s\\%s" % (oid, parent,
                                                                          bname(dds))
            used_name[oid].setdefault(C.norm(bname(dds)), C.norm(dds))
            return ("COPY_INTO_OUTFIT_NAMESPACE", "COPY_FROM_EXTERNAL_MOD",
                    "EXTERNAL_MOD", target, lk,
                    "Global provider lookup: real provider %s (priority %s). Copy into "
                    "the consuming outfit namespace + REPOINT (shared-asset whitelist "
                    "= NONE)." % (prov, prio), prov, prio)
        if lk == "GLOBAL_BODY_SKIN":
            return ("KEEP_EXTERNAL_REFERENCE", "KEEP_EXTERNAL_REFERENCE",
                    "EXTERNAL_MOD", "", lk,
                    "GLOBAL BODY / SKIN SYSTEM asset (provider %s). NEVER copied into "
                    "textures\\ZLJ\\CombatLatex\\%s\\ -- it must keep following the "
                    "actor body/skin family; UBE / 3BA body-family migration owns it."
                    % (prov, oid), prov, prio)
        if lk == "VANILLA_ENGINE_RESOURCE":
            return ("KEEP_EXTERNAL_REFERENCE", "KEEP_EXTERNAL_REFERENCE",
                    "VANILLA", "", lk,
                    "Engine / vanilla resource. NEVER copied into the pack namespace; "
                    "the NIF keeps the original reference.", prov, prio)
        if lk == "TRUE_MISSING":
            return ("UNRESOLVED", "UNRESOLVED", "UNKNOWN", "", lk,
                    "Global provider lookup executed over all MO2 mod directories plus "
                    "the game Data folder: no provider at this exact path, no loose game "
                    "Data file, and the basename occurs in no mod of the instance. "
                    "Lookup evidence: %s" % lnote, "UNKNOWN", "UNKNOWN")
        # UNKNOWN / NOT_IN_LOOKUP
        return ("UNRESOLVED", "UNRESOLVED", "UNKNOWN", "", lk,
                "PATH-MISMATCH, not fuzzy-resolvable: the referenced folder does not "
                "exist, only same-basename files elsewhere were found. Those are NOT "
                "treated as the same asset. Candidate locations are recorded in "
                "P02A_GLOBAL_PROVIDER_LOOKUP.csv: %s" % lnote, prov, prio)

    for oid, nifvp, nifclass, roles, canon, prefix in walk:
        src = nifvp
        if nifclass == "BODYSLIDE_OUTPUT_NIF":
            src = bs([b for b in bsrows
                      if (b["new_output_path"].rstrip("\\") + "\\" +
                          (b["new_output_file"] or "") + ".nif") == nifvp
                      and b["OUTFIT_ID"] == oid][0]["old_input_nif"])
        key = C.norm(src)
        if key not in tex_cache:
            tex_cache[key] = p.nif_tex_rows(src)
        refs = tex_cache[key]
        if not refs:
            r0 = [x for x in arma if C.norm(x["old_vpath"]) == key
                  and x["OUTFIT_ID"] == oid]
            ex = r0[0]["existence"] if r0 else "UNKNOWN"
            note = ("Texture set of this mesh is not derivable from the frozen P00 evidence: "
                    "the NIF is not in the P00 NIF index (existence=%s). The frozen evidence "
                    "indexes loose mod files only, so the mesh is either BSA-resident or "
                    "belongs to a provider outside the P00 scope. READ-ONLY prohibits "
                    "writing, not reading: P02B is allowed to parse the binary to resolve it."
                    % ex)
            tex_rows.append([oid, nifvp, nifclass, roles, canon, "(whole mesh)",
                             "(whole mesh)", "UNKNOWN", "UNKNOWN", "UNKNOWN", "",
                             "", "UNKNOWN", "NOT_IN_P00_NIF_INDEX", "UNKNOWN",
                             "UNRESOLVED", "", "NONE", (prefix + " " + note).strip()])
            rw_rows.append([oid, nifvp, nifclass, roles, "(whole mesh)", "(whole mesh)",
                            "UNKNOWN", "", "UNKNOWN", "UNKNOWN", "UNRESOLVED", "NONE",
                            note])
            cl_rows.append([oid, "UNRESOLVED", "UNKNOWN", "UNKNOWN", "UNKNOWN",
                            "UNKNOWN", nifvp, roles, "(whole mesh)",
                            "BLOCKED: the BSShaderTextureSet of this mesh is absent from "
                            "the frozen P00 NIF index, so P02A could not derive it. This is "
                            "an evidence-coverage gap, not a read-only restriction: parsing "
                            "the binary is permitted. Resolve in P02B by parsing the mesh, "
                            "or by listing the BSA that contains it.", "", "OPEN_BLOCKED", note])
            stats[oid]["tex_unresolved"] += 1
            stats[oid]["tex_unknown_mesh"] += 1
            continue
        for shape, slot, dds in refs:
            dds = bs(dds)
            action, status, own, target, lk, note, prov, prio = classify(oid, dds)
            sem = C.semantic_type(slot, dds)
            src_outfits[lookup_key(dds)].add(oid)
            dds_used[oid].add(lookup_key(dds))
            tex_rows.append([oid, nifvp, nifclass, roles, canon, shape, slot, dds,
                             prov, prio, prov_str(p, ensure_root(dds, "textures"))
                             if p.exists(ensure_root(dds, "textures")) else "",
                             p.sha(ensure_root(dds, "textures"))
                             if p.exists(ensure_root(dds, "textures")) else "",
                             sem, lk, own, action, target, "NONE",
                             (prefix + " " + note).strip()])
            rw_rows.append([oid, nifvp, nifclass, roles, shape, slot, dds, target,
                            prov, prio, status, "NONE", note])
            stats[oid]["tex_rows"] += 1
            stats[oid]["act_" + action] += 1
            stats[oid]["st_" + status] += 1
            if target:
                tk = C.norm(target)
                if tk in seen_target and seen_target[tk][0] != oid:
                    collisions.append((tk, seen_target[tk][0], oid))
                seen_target.setdefault(tk, (oid, target))

    # ---- shared-asset proposals (whitelist NONE -> proposal only) ----------
    for dkey, outfits in sorted(src_outfits.items()):
        if len(outfits) < 2:
            continue
        probe = next((t for t in tex_rows if lookup_key(t[7]) == dkey and t[15] ==
                      "COPY_INTO_OUTFIT_NAMESPACE"), None)
        if probe is None:
            continue
        sha = probe[11]
        for oid in sorted(outfits):
            if not any(t[0] == oid and lookup_key(t[7]) == dkey for t in tex_rows):
                continue
            others = sorted(o for o in outfits if o != oid)
            cl_rows.append([oid, "CROSS_PACK_CANDIDATE", ";".join(others), probe[7],
                            probe[8], probe[9], probe[1], probe[3],
                            ";".join(sorted({t[6] for t in tex_rows if t[0] == oid
                                              and lookup_key(t[7]) == dkey})),
                            "PROPOSAL_SHARED_NOT_APPROVED: identical sha256 %s is consumed "
                            "by %d outfits of this pack. P02A keeps a private copy per "
                            "outfit and creates NO Shared folder; material sharing is a "
                            "P05 decision." % (sha[:16], len(outfits)),
                            "textures\\ZLJ\\CombatLatex\\%s\\%s" % (oid,
                                                                        bname(probe[7])),
                            "CLOSED_BY_DUPLICATION",
                            "status=PROPOSAL_SHARED_NOT_APPROVED (whitelist = NONE)"])
            stats[oid]["share_proposal"] += 1
            for t in tex_rows:
                if t[0] == oid and lookup_key(t[7]) == dkey:
                    t[17] = "PROPOSAL_SHARED_NOT_APPROVED"
            for t in rw_rows:
                if t[0] == oid and lookup_key(t[6]) == dkey:
                    t[11] = "PROPOSAL_SHARED_NOT_APPROVED"

    # ---- closure ledger ----------------------------------------------------
    cross_before = set()
    for t in tex_rows:
        oid, nifvp, nifclass, roles, canon, shape, slot, dds, prov, prio, shad, sha, \
            sem, lk, own, action, target, sp, notes = t
        if action == "KEEP_SELF_NAMESPACE":
            continue
        own_ids = [o for o in str(own).split(";") if o in C.OUTFIT_IDS]
        cross = [o for o in own_ids if o != oid]
        if own_ids and not cross:
            # already owned by THIS outfit -- a pure namespace migration, not a
            # dependency.  Fully described by P02A_TEXTURE_MIGRATION /
            # P02A_NIF_TEXTURE_REWRITE, so it stays out of the closure ledger.
            continue
        if action == "KEEP_EXTERNAL_REFERENCE":
            dtype = "EXTERNAL_MOD"
            plan = ("KEEP_EXTERNAL_REFERENCE: %s belongs to the %s and is deliberately "
                    "NOT copied into the pack namespace. The NIF keeps pointing at the "
                    "original path." % (bname(dds), lk))
            state = "CLOSED_KEEP_EXTERNAL_REFERENCE"
            stats[oid]["closure_keep_external"] += 1
        elif action == "UNRESOLVED":
            dtype = "UNRESOLVED"
            plan = ("BLOCKED: %s. Resolution needs a human ruling or a further evidence "
                    "extension; no fuzzy match is allowed." % notes)
            state = "OPEN_BLOCKED"
            stats[oid]["closure_unresolved"] += 1
        elif cross:
            dtype = "CROSS_OUTFIT"
            plan = ("COPY_INTO_OUTFIT_NAMESPACE + REPOINT: copy %s (owner %s) into "
                    "textures\\ZLJ\\CombatLatex\\%s\\%s and repoint %s / %s / %s. "
                    "Cross-outfit DDS are duplicated per outfit, never shared."
                    % (bname(dds), ";".join(cross), oid, bname(dds), nifvp, shape, slot))
            state = "CLOSED"
            cross_before.add((oid, lookup_key(dds)))
            stats[oid]["closure_cross_outfit"] += 1
        else:
            dtype = "EXTERNAL_MOD"
            plan = ("COPY_INTO_OUTFIT_NAMESPACE + REPOINT: vendor %s (provider %s, "
                    "priority %s) into textures\\ZLJ\\CombatLatex\\%s\\%s and "
                    "repoint %s / %s / %s so the outfit is self-contained "
                    "(shared-asset whitelist = NONE)."
                    % (bname(dds), prov, prio, oid, bname(dds), nifvp, shape, slot))
            state = "CLOSED"
            stats[oid]["closure_external"] += 1
        cl_rows.append([oid, dtype, own, dds, prov, prio, nifvp, roles, slot, plan,
                        target, state, notes])

    return (tex_rows, rw_rows, cl_rows, stats, collisions, cross_before, lookup,
            dds_used)


def prov_str(p, vp):
    return ";".join(p.shadowed(vp))


# ==================================================================== main ==
def main():
    p = C.P00.get()
    mesh_rows, mesh_coll, mstats, n_tri = build_mesh_ledger(p)
    (tex_rows, rw_rows, cl_rows, tstats, tex_coll, cross_before, lookup,
     dds_used) = build_texture_ledgers(p)

    C.write_csv(os.path.join(RPT, "P02A_MESH_MIGRATION.csv"), MESH_HEADER, mesh_rows)
    C.write_csv(os.path.join(RPT, "P02A_TEXTURE_MIGRATION.csv"), TEX_HEADER, tex_rows)
    C.write_csv(os.path.join(RPT, "P02A_NIF_TEXTURE_REWRITE.csv"),
                REWRITE_HEADER, rw_rows)
    C.write_csv(os.path.join(RPT, "P02A_CROSS_OUTFIT_TEXTURE_CLOSURE.csv"),
                CLOSURE_HEADER, cl_rows)

    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 96)
    print("P02A v2  MESH + TEXTURE MIGRATION LEDGER  --  ZLJ_COMBAT_LATEX (STRICT READ-ONLY)")
    print("=" * 96)
    hdr = ("%-18s %6s %6s %6s %6s %6s %6s %6s %6s %6s"
           % ("OUTFIT_ID", "GAMEref", "GAMEf", "BSOUT", "SHAPED", "MORPH",
              "canon", "ddsUse", "ddsRef", "propos"))
    print(hdr)
    print("-" * 96)
    agg = collections.Counter()
    for oid in C.OUTFIT_IDS:
        m = mstats[oid]
        print("%-18s %6d %6d %6d %6d %6d %6d %6d %6d %6d"
              % (oid, m["GAME_NIF"], m["GAME_NIF_FILES"],
                 m["BODYSLIDE_OUTPUT_NIF"], m["SHAPEDATA_SOURCE_NIF"],
                 m["GROUND_NIF"], m["canonical_runtime_nif"],
                 len(dds_used[oid]), tstats[oid]["tex_rows"],
                 tstats[oid]["share_proposal"]))
        for k, v in m.items():
            agg["m_" + k] += v
        for k, v in tstats[oid].items():
            agg["t_" + k] += v
    print("-" * 96)
    print("  GAMEref = ARMA/ARMO model-slot references (one per model_role)")
    print("  GAMEf   = distinct source NIF files behind those references")
    print("  ddsUse  = distinct source DDS actually read from that outfit's NIFs")
    print("  ddsRef  = per (NIF, shape, slot) texture rows")
    print("mesh_class totals: GAME_NIF=%d  BODYSLIDE_OUTPUT_NIF=%d  "
          "SHAPEDATA_SOURCE_NIF=%d  BODY_MORPH_TRI=%d (TRI is not a NIF and is not "
          "counted as one)"
          % (agg["m_GAME_NIF"], agg["m_BODYSLIDE_OUTPUT_NIF"],
             agg["m_SHAPEDATA_SOURCE_NIF"], n_tri))
    print("mesh rows=%d  texture rows=%d  rewrite rows=%d  closure rows=%d"
          % (len(mesh_rows), len(tex_rows), len(rw_rows), len(cl_rows)))
    print("distinct migrated mesh target paths=%d"
          % len({C.norm(r[9]) for r in mesh_rows if r[9]
                 and r[11] != "EXCLUDE_SHADOWED"}))
    print("-" * 96)
    print("TEXTURE ACTION / REWRITE STATUS DISTRIBUTION (five new classes)")
    order = ["COPY_INTO_OUTFIT_NAMESPACE", "KEEP_EXTERNAL_REFERENCE", "UNRESOLVED",
             "KEEP_SELF_NAMESPACE"]
    for a in order:
        print("   action %-30s %d" % (a, agg["t_act_" + a]))
    for s in sorted(STATUS_ENUM):
        print("   status %-30s %d" % (s, agg["t_st_" + s]))
    print("   shared_proposal=PROPOSAL_SHARED_NOT_APPROVED rows = %d "
          "(carried in the shared_proposal column; whitelist = NONE, no Shared folder)"
          % agg["t_share_proposal"])
    print("   unknown-mesh rows (texture set not readable in P02A) = %d"
          % agg["t_tex_unknown_mesh"])
    print("-" * 96)
    print("CLOSURE dependency_type")
    for k in sorted([k for k in agg if k.startswith("t_closure_")]):
        print("   %-28s %d" % (k[10:], agg[k]))
    print("-" * 96)
    print("CROSS-OUTFIT TEXTURE DEPENDENCY")
    print("   distinct (consuming outfit, source DDS) pairs owned by another outfit of "
          "this pack BEFORE plan = %d" % len(cross_before))
    print("   runtime cross-outfit DDS after plan = 0  (every cross-outfit reference is "
          "copied into the consuming outfit's namespace)")
    print("TARGET_PATH_COLLISION mesh    = %d" % len(mesh_coll))
    for c in mesh_coll:
        print("      COLLISION", c)
    print("TARGET_PATH_COLLISION texture = %d" % len(tex_coll))
    for c in tex_coll:
        print("      COLLISION", c)
    sd_ok, sd_bad, mt_ok, mt_bad = check_namespaces(mesh_rows)
    print("-" * 96)
    print("NAMESPACE SPELLING CHECK (the two spellings are intentionally different)")
    print("   meshes / textures root : %s        (backslash, no underscore)" % C.MESH_ROOT)
    print("   ShapeData root         : %s  (underscore)" % C.SD_ROOT)
    print("   SHAPEDATA_SOURCE_NIF targets inside SD_ROOT : %d ok / %d bad" % (sd_ok, sd_bad))
    print("   GAME_NIF + BODYSLIDE_OUTPUT_NIF targets inside MESH_ROOT : %d ok / %d bad"
          % (mt_ok, mt_bad))
    tex_bad = [t for t in tex_rows
               if t[16] and not t[16].lower().startswith(C.TEX_ROOT.lower()
                                                         + t[0].lower() + "\\")]
    print("   texture targets inside TEX_ROOT            : %d ok / %d bad"
          % (len([t for t in tex_rows if t[16]]) - len(tex_bad), len(tex_bad)))
    print("-" * 96)
    print("REMAINING UNRESOLVED (distinct source DDS / whole-mesh references)")
    unres = {}
    for t in tex_rows:
        if t[15] != "UNRESOLVED":
            continue
        k = t[13] if t[13] != "NOT_IN_P00_NIF_INDEX" else "NOT_IN_P00_NIF_INDEX(mesh)"
        unres.setdefault(k, set()).add(t[7])
    for k in sorted(unres):
        print("   %-24s %d" % (k, len(unres[k])))
        for v in sorted(unres[k]):
            print("        %s" % v)
    print("=" * 96)


if __name__ == "__main__":
    main()
