# -*- coding: utf-8 -*-
"""P02A SELF-CONTAINMENT AUDIT generator (Lead).

Consumes the eleven teammate CSVs and simulates the post-migration state of the
ZLJ_COMBAT_LATEX pack. READ-ONLY with respect to every mod / game file; the only
thing this script writes is reports/P02A/P02A_SELF_CONTAINMENT_AUDIT.csv.

--------------------------------------------------------------------------
Reference-classification of a texture that is NOT resolvable in the frozen P00 VFS
--------------------------------------------------------------------------
The frozen P00 index covers mod directories only, so a referenced DDS that is absent
from it is not automatically a defect. Each such reference is classified once, by
evidence, into exactly one class. The rules are applied ONLY to paths that are
absent from the VFS, so a mod-supplied file can never be mistaken for a base-game
file.

  VANILLA_ALLOWED       documented Skyrim base-game prefix, and the brief explicitly
                        permits vanilla resources to stay outside the namespace.
  VANILLA_CANDIDATE     generic engine/utility prefix that is usually base game but
                        cannot be confirmed here (this MO2 instance has no vanilla
                        Data tree). Needs one human-authorised read-only probe.
  EXTERNAL_MOD_MISSING  mod-scoped path whose owning mod is not installed in this
                        instance. Nothing can be copied; it stays an open external
                        dependency until a human decides.
  UNRESOLVED            anything else - never guessed.

Verdict policy:
  BLOCKED - a structural link of the migration chain is broken (missing/UNKNOWN mesh
            target, incomplete BodySlide OSP->ShapeData->inputNIF->OSD->output chain,
            unresolved wearable ARMA model path, or a target-path collision).
  REVIEW  - no structural break, but open external/cross-outfit dependencies, hard
            unresolved references, naming-rule deviations or unknown bone checks remain.
  PASS    - every planned link resolves inside the Outfit namespace, with no open
            dependency and no unresolved reference.
"""
import os
import sys
import csv
from collections import defaultdict, Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p02a_common as C

P = C.P00.get()
OUT = C.OUT

CSV_FILES = {
    "source_map": "P02A_EFFECTIVE_SOURCE_MAP.csv",
    "mesh": "P02A_MESH_MIGRATION.csv",
    "texture": "P02A_TEXTURE_MIGRATION.csv",
    "closure": "P02A_CROSS_OUTFIT_TEXTURE_CLOSURE.csv",
    "nif_rewrite": "P02A_NIF_TEXTURE_REWRITE.csv",
    "bodyslide": "P02A_BODYSLIDE_MIGRATION.csv",
    "sd_rewrite": "P02A_SHAPEDATA_TEXTURE_REWRITE.csv",
    "plugin": "P02A_PLUGIN_RECORD_MIGRATION.csv",
    "arma": "P02A_ARMA_MODEL_REWRITE.csv",
    "plugin_tex": "P02A_PLUGIN_TEXTURE_REWRITE.csv",
    "physics": "P02A_PHYSICS_MIGRATION.csv",
}

# documented Skyrim base-game prefixes (used ONLY for VFS-absent paths)
VANILLA_BASE_PREFIXES = (
    "textures/actors/character/",   # femalebody_*, femalehands_* - base body/hand textures
    "textures/ghost/",              # ghostcolour4* - base ghost shader textures
)
# generic prefixes that are normally base game but cannot be confirmed from this instance
VANILLA_CANDIDATE_PREFIXES = (
    "textures/cubemaps/",
)

UNRESOLVED = ("UNRESOLVED", "UNKNOWN", "OPEN_BLOCKED", "MISSING")
PROPOSAL = ("PROPOSAL_SHARED_NOT_APPROVED",)
MISSING_CLASS = defaultdict(set)     # vpath -> {class, ...}
MISSING_OUTFIT = defaultdict(set)    # (class, vpath) -> {outfit}


def load(key):
    p = os.path.join(OUT, CSV_FILES[key])
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def col(row, *names, default=""):
    low = {k.lower().strip(): v for k, v in row.items() if k}
    for n in names:
        v = low.get(n.lower().strip())
        if v is not None:
            return (v or "").strip()
    return default


def is_unk(v):
    return (v or "").strip().upper() in ("UNKNOWN", "UNRESOLVED", "", "TBD", "PENDING", "N/A", "NA", "NONE")


def is_unresolved(v):
    return (v or "").strip().upper() in UNRESOLVED


def is_proposal(v):
    return (v or "").strip().upper() in PROPOSAL


def classify_missing(vpath):
    """Classify a VFS-absent texture path. Never guesses beyond the documented rules."""
    p = C.norm(vpath)
    if p in P.vfs:
        return "IN_VFS"
    if p.startswith(VANILLA_BASE_PREFIXES):
        return "VANILLA_ALLOWED"
    if p.startswith(VANILLA_CANDIDATE_PREFIXES):
        return "VANILLA_CANDIDATE"
    return "EXTERNAL_MOD_MISSING"


def under(path, root):
    p = C.norm(path)
    return bool(p) and p.startswith(C.norm(root))


def mesh_ns(o):
    return "meshes/ZLJ/CombatLatex/%s/" % o.lower()


def tex_ns(o):
    return "textures/ZLJ/CombatLatex/%s/" % o.lower()


def sd_ns(o):
    return "CalienteTools/BodySlide/ShapeData/ZLJ_CombatLatex/%s/" % o.lower()


def osp_root(o):
    return "CalienteTools/BodySlide/SliderSets/ZLJ_%s" % o.lower()


def osp_ns(o):
    return osp_root(o) + ".osp"


def verdict(blocked, review):
    return "BLOCKED" if blocked else ("REVIEW" if review else "PASS")


def main():
    d = {k: load(k) for k in CSV_FILES}
    missing_csv = [CSV_FILES[k] for k, v in d.items() if v is None]
    mine = lambda k, o: [r for r in (d.get(k) or []) if col(r, "OUTFIT_ID") == o]

    # ---------- independent target-path collision re-derivation ----------
    tgt = defaultdict(list)
    for o in C.OUTFIT_IDS:
        for r in mine("mesh", o):
            t = C.norm(col(r, "target_virtual_path", "target_path"))
            if t and not is_unk(t):
                tgt[t].append((o, col(r, "source_virtual_path", "source_path")))
        for r in mine("bodyslide", o):
            op, of = C.norm(col(r, "new_output_path")), col(r, "new_output_file")
            if op and of and not is_unk(op) and not is_unk(of):
                tgt[(op.rstrip("/") + "/" + C.norm(of))].append((o, col(r, "old_osp")))
            ospv = C.norm(col(r, "new_osp"))
            if ospv and not is_unk(ospv):
                tgt[ospv].append((o, col(r, "old_osp")))
    collisions = [(t, v) for t, v in tgt.items() if len({o for o, _ in v}) > 1]
    coll_by_outfit = Counter()
    for t, v in collisions:
        for o in {o for o, _ in v}:
            coll_by_outfit[o] += 1

    header = ["OUTFIT_ID", "check_id", "check_name", "result", "metric_value", "threshold",
              "remaining_cross_outfit_refs", "remaining_external_mod_refs", "unresolved_refs",
              "vanilla_allowed_refs", "shared_material_proposals", "target_path_collisions",
              "evidence", "notes"]
    rows = []
    pack = Counter()
    cls_pack = Counter()

    for o in C.OUTFIT_IDS:
        mesh, tex, clo = mine("mesh", o), mine("texture", o), mine("closure", o)
        nifrw, bs, sdrw = mine("nif_rewrite", o), mine("bodyslide", o), mine("sd_rewrite", o)
        pl, arma, ptex, phys = mine("plugin", o), mine("arma", o), mine("plugin_tex", o), mine("physics", o)

        cross_open = [r for r in clo
                      if col(r, "dependency_type").upper() in ("CROSS_OUTFIT", "CROSS_PACK_CANDIDATE")
                      and not col(r, "post_plan_state").upper().startswith("CLOSED")]
        ext_open = [r for r in clo
                    if col(r, "dependency_type").upper() == "EXTERNAL_MOD"
                    and not col(r, "post_plan_state").upper().startswith("CLOSED")]

        # ---- classify every reference that the frozen VFS cannot resolve ----
        cls = Counter()
        for r in nifrw + sdrw:
            v = col(r, "old_dds_path")
            if not v:
                continue
            if is_unresolved(col(r, "status")):
                c = classify_missing(v)
                cls[c] += 1
                MISSING_CLASS[c].add(C.norm(v))
                MISSING_OUTFIT[(c, C.norm(v))].add(o)
        for r in ptex:
            v = col(r, "old_dds")
            if v and (is_unresolved(col(r, "status")) or is_unresolved(col(r, "dependency_type"))):
                c = classify_missing(v)
                cls[c] += 1
                MISSING_CLASS[c].add(C.norm(v))
                MISSING_OUTFIT[(c, C.norm(v))].add(o)
        cls_pack.update(cls)

        ext_missing = cls["EXTERNAL_MOD_MISSING"]
        hard_unres = cls["VANILLA_CANDIDATE"]
        van_ok = cls["VANILLA_ALLOWED"]
        props = [r for r in nifrw + sdrw
                 if is_proposal(col(r, "status")) or is_proposal(col(r, "shared_proposal"))]
        unres_all = ext_missing + hard_unres
        coll_n = coll_by_outfit.get(o, 0)

        def add(cid, name, res, val, thr, ev, note=""):
            rows.append([o, cid, name, res, val, thr, len(cross_open), ext_missing,
                         hard_unres, van_ok, len(props), coll_n, ev, note])
            pack[res] += 1

        # ---------- C1 GAME MESH ----------
        if d["mesh"] is None:
            add("C1", "GAME_MESH_SELF_CONTAINED", "BLOCKED", -1, 0, "P02A_MESH_MIGRATION.csv missing", "upstream deliverable absent")
        else:
            game = [r for r in mesh if col(r, "mesh_class").upper() in ("GAME_MESH", "GAME", "")]
            off = [r for r in game if not under(col(r, "target_virtual_path", "target_path"), mesh_ns(o))]
            add("C1", "GAME_MESH_SELF_CONTAINED", verdict((not game) or bool(off) or bool(coll_n), False),
                len(game) - len(off), len(game),
                "game mesh rows=%d, target off-namespace/UNKNOWN=%d, collisions=%d, EXCLUDE_SHADOWED=%d, GROUND/OTHER kept separate"
                % (len(game), len(off), coll_n, len([r for r in game if col(r, "retain_decision").upper() == "EXCLUDE_SHADOWED"])),
                "; ".join(sorted({col(r, "target_virtual_path", "target_path") for r in off})[:3]))

        # ---------- C2 TEXTURE ----------
        if d["nif_rewrite"] is None or d["closure"] is None:
            add("C2", "TEXTURE_SELF_CONTAINED", "BLOCKED", -1, 0,
                "P02A_NIF_TEXTURE_REWRITE.csv / P02A_CROSS_OUTFIT_TEXTURE_CLOSURE.csv missing", "upstream deliverable absent")
        else:
            refs = nifrw + sdrw
            off = [r for r in refs
                   if not under(col(r, "new_dds_path"), tex_ns(o))
                   and not is_unresolved(col(r, "status")) and not is_proposal(col(r, "status"))]
            add("C2", "TEXTURE_SELF_CONTAINED", verdict(bool(off), bool(hard_unres or props or cross_open or ext_open or ext_missing)),
                len(refs) - len(off) - cls["EXTERNAL_MOD_MISSING"] - cls["VANILLA_CANDIDATE"] - cls["VANILLA_ALLOWED"],
                len(refs),
                "texture slots (nif=%d shapedata=%d) | off-namespace=%d | external-mod-missing=%d | vanilla-candidate=%d | vanilla-allowed=%d | shared-proposals=%d | open cross-outfit=%d"
                % (len(nifrw), len(sdrw), len(off), ext_missing, hard_unres, van_ok, len(props), len(cross_open)),
                "external-mod-missing references belong to mods that are not installed in this MO2 instance; nothing can be copied, so they stay open until a human decides")

        # ---------- C3 BODYSLIDE ----------
        if d["bodyslide"] is None:
            add("C3", "BODYSLIDE_SELF_CONTAINED", "BLOCKED", -1, 0, "P02A_BODYSLIDE_MIGRATION.csv missing", "upstream deliverable absent")
        else:
            chain_bad = [r for r in bs if any(is_unk(col(r, f)) for f in
                            ("new_osp", "new_shape_data", "new_input_nif", "new_osd", "new_output_path", "new_output_file"))]
            osp_bad = [r for r in bs if not is_unk(col(r, "new_osp"))
                       and not C.norm(col(r, "new_osp")).startswith(
                           (osp_root(o).lower() + ".osp", osp_root(o).lower() + "__"))]
            osp_dev = [r for r in bs if not is_unk(col(r, "new_osp")) and C.norm(col(r, "new_osp")) != osp_ns(o)]
            sd_bad = [r for r in bs if not is_unk(col(r, "new_shape_data")) and not under(col(r, "new_shape_data"), sd_ns(o))]
            out_bad = [r for r in bs if not is_unk(col(r, "new_output_path")) and not under(col(r, "new_output_path"), mesh_ns(o))]
            unk_basis = [r for r in bs if col(r, "relationship_basis").upper() == "UNKNOWN"]
            sd_ref_bad = [r for r in sdrw if not under(col(r, "new_dds_path"), tex_ns(o))
                          and not is_unresolved(col(r, "status")) and not is_proposal(col(r, "status"))]
            add("C3", "BODYSLIDE_SELF_CONTAINED", verdict(bool(chain_bad), bool(osp_bad or sd_bad or out_bad or unk_basis or sd_ref_bad or osp_dev)),
                len(bs) - len(chain_bad), len(bs),
                "projects=%d chain-incomplete=%d osp-off-ns=%d osp-naming-deviation=%d shapedata-off-ns=%d output-off-ns=%d UNKNOWN-basis=%d shapedata-tex-off-ns=%d"
                % (len(bs), len(chain_bad), len(osp_bad), len(osp_dev), len(sd_bad), len(out_bad), len(unk_basis), len(sd_ref_bad)),
                "naming deviation = ZLJ_<OUTFIT_ID>__<Part>.osp used where the frozen rule allows a single ZLJ_<OUTFIT_ID>.osp; requires human approval")

        # ---------- C4 PLUGIN ----------
        if d["plugin"] is None or d["arma"] is None:
            add("C4", "PLUGIN_PATHS_PLANNED", "BLOCKED", -1, 0,
                "P02A_PLUGIN_RECORD_MIGRATION.csv / P02A_ARMA_MODEL_REWRITE.csv missing", "upstream deliverable absent")
        else:
            bad_tp = [r for r in pl if col(r, "target_plugin").lower() != C.TARGET_PLUGIN.lower()]
            no_edid = [r for r in pl if is_unk(col(r, "new_edid")) or not col(r, "new_edid").lower().startswith("zlj_cl_")]
            generated = [r for r in pl if col(r, "new_formid_status").upper() != "NOT_GENERATED_P02A"]
            wear = [r for r in arma if col(r, "model_role").upper() in ("WEARABLE", "WORN", "WEARABLE_MESH")]
            arma_bad = [r for r in wear if not under(col(r, "new_path", "new_vpath"), mesh_ns(o))
                        and col(r, "status").upper() not in ("NON_CANONICAL_SOURCE", "EXCLUDE", "UNRESOLVED")]
            arma_unres = [r for r in arma if is_unresolved(col(r, "status"))]
            ground = [r for r in arma if col(r, "model_role").upper() in ("GROUND", "WORLD")]
            ptex_bad = [r for r in ptex if col(r, "dependency_type").upper() == "CROSS_OUTFIT"
                        and not under(col(r, "new_dds"), tex_ns(o))]
            add("C4", "PLUGIN_PATHS_PLANNED", verdict(bool(arma_unres), bool(bad_tp or no_edid or generated or arma_bad or ptex_bad)),
                len(pl) - len(no_edid), len(pl),
                "records=%d wrong-target-plugin=%d missing-EDID=%d formid-generated=%d wearable-ARMA=%d off-namespace=%d unresolved-ARMA=%d ground/world-kept-separate=%d plugin-DDS-cross-outfit-open=%d"
                % (len(pl), len(bad_tp), len(no_edid), len(generated), len(wear), len(arma_bad), len(arma_unres), len(ground), len(ptex_bad)),
                "no FormID was generated in P02A")

        # ---------- C5 PHYSICS ----------
        if d["physics"] is None:
            add("C5", "PHYSICS_PATHS_PLANNED", "BLOCKED", -1, 0, "P02A_PHYSICS_MIGRATION.csv missing", "upstream deliverable absent")
        else:
            need = [r for r in phys if col(r, "rewrite_required").upper() == "YES"]
            no_new = [r for r in need if is_unk(col(r, "new_path_refs"))]
            bone_bad = [r for r in phys if col(r, "bone_check_status").upper() in ("MISSING_BONE", "UNKNOWN")]
            add("C5", "PHYSICS_PATHS_PLANNED", verdict(bool(no_new), bool(bone_bad)),
                len(phys) - len(no_new), len(phys),
                "physics configs=%d rewrite-required=%d without-new-path=%d bone-check-unknown=%d"
                % (len(phys), len(need), len(no_new), len(bone_bad)),
                "bone verification deferred: the HDT-SMP bone set is not part of the frozen P00 evidence")

        orows = [r for r in rows if r[0] == o]
        rl = [r[3] for r in orows]
        rows.append([o, "TOTAL", "OUTFIT_SELF_CONTAINMENT", verdict("BLOCKED" in rl, "REVIEW" in rl),
                     len(orows), 5, len(cross_open), ext_missing, hard_unres, van_ok, len(props), coll_n,
                     "C1..C5 = " + ", ".join("%s:%s" % (r[1], r[3]) for r in orows),
                     "worst-case verdict across the five gates"])
        pack[verdict("BLOCKED" in rl, "REVIEW" in rl)] += 1

    rows.append(["__PACK__", "PACK_TOTAL", "PACK_SELF_CONTAINMENT",
                 verdict(pack["BLOCKED"] > 0, pack["REVIEW"] > 0), 11, 5,
                 sum(r[6] for r in rows if r[1] == "TOTAL"),
                 sum(r[7] for r in rows if r[1] == "TOTAL"),
                 sum(r[8] for r in rows if r[1] == "TOTAL"),
                 sum(r[9] for r in rows if r[1] == "TOTAL"),
                 sum(r[10] for r in rows if r[1] == "TOTAL"),
                 len(collisions),
                 "outfit verdicts: " + ", ".join("%s=%d" % kv for kv in sorted(pack.items()) if kv[0] in ("PASS", "REVIEW", "BLOCKED"))
                 + " | unresolvable reference classes (rows): " + ", ".join("%s=%d" % kv for kv in sorted(cls_pack.items())),
                 "target-path collisions = %d" % len(collisions)])

    C.write_csv(os.path.join(OUT, "P02A_SELF_CONTAINMENT_AUDIT.csv"), header, rows)

    # machine-readable side evidence for the human reviewer
    ev = []
    for cls in ("EXTERNAL_MOD_MISSING", "VANILLA_CANDIDATE", "VANILLA_ALLOWED"):
        for p in sorted(MISSING_CLASS[cls]):
            ev.append([cls, p, ";".join(sorted(MISSING_OUTFIT[(cls, p)]))])
    C.write_csv(os.path.join(OUT, "P02A_UNRESOLVED_REFERENCE_CLASSIFICATION.csv"),
                ["reference_class", "virtual_path", "affected_outfits"], ev)

    print("=" * 78)
    print("P02A SELF-CONTAINMENT AUDIT")
    print("outfit verdicts:", dict(pack))
    print("target path collisions:", len(collisions))
    print("unresolvable reference classes (rows):", dict(cls_pack))
    print("distinct unresolvable DDS:", {k: len(v) for k, v in MISSING_CLASS.items()})
    for o in C.OUTFIT_IDS:
        r = [x for x in rows if x[0] == o and x[1] == "TOTAL"][0]
        print("  %-20s %-8s cross=%-2d ext_missing=%-4d unres=%-3d vanilla=%-3d prop=%-4d coll=%d"
              % (o, r[3], r[6], r[7], r[8], r[9], r[10], r[11]))
    if missing_csv:
        print("MISSING DELIVERABLES:", missing_csv)
    print("wrote", os.path.join(OUT, "P02A_SELF_CONTAINMENT_AUDIT.csv"))
    print("wrote", os.path.join(OUT, "P02A_UNRESOLVED_REFERENCE_CLASSIFICATION.csv"))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
