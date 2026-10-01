# -*- coding: utf-8 -*-
"""P02A.1 final self-containment audit (Lead).

Adds the four gates mandated by the P02A.1 human review on top of the P02A gates:
  G6 ARMA/ARMO model-role schema  - exact enum, no path-name guessing
  G7 TRI physics misclassification - must be 0
  G8 target OSP namespace         - exactly 11, one per outfit
  G9 unresolved-reference provenance - every unresolved DDS must have a global
     provider-lookup verdict; nothing may be called missing without one

READ-ONLY with respect to every mod/game file. Writes only
reports/P02A/P02A_SELF_CONTAINMENT_AUDIT.csv and
reports/P02A/P02A_UNRESOLVED_REFERENCE_CLASSIFICATION.csv.
"""
import csv
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p02a_common as C

P = C.P00.get()
OUT = C.OUT

F = {
    "source_map": "P02A_EFFECTIVE_SOURCE_MAP.csv",
    "mesh": "P02A_MESH_MIGRATION.csv",
    "texture": "P02A_TEXTURE_MIGRATION.csv",
    "closure": "P02A_CROSS_OUTFIT_TEXTURE_CLOSURE.csv",
    "nif_rewrite": "P02A_NIF_TEXTURE_REWRITE.csv",
    "bodyslide": "P02A_BODYSLIDE_MIGRATION.csv",
    "morph": "P02A_BODYSLIDE_MORPH_MIGRATION.csv",
    "sd_rewrite": "P02A_SHAPEDATA_TEXTURE_REWRITE.csv",
    "plugin": "P02A_PLUGIN_RECORD_MIGRATION.csv",
    "arma": "P02A_ARMA_MODEL_REWRITE.csv",
    "plugin_tex": "P02A_PLUGIN_TEXTURE_REWRITE.csv",
    "physics": "P02A_PHYSICS_MIGRATION.csv",
    "lookup": "P02A_GLOBAL_PROVIDER_LOOKUP.csv",
}

MODEL_ROLE_ENUM = {
    "WEARABLE_MALE_3P", "WEARABLE_FEMALE_3P",
    "FIRSTPERSON_MALE", "FIRSTPERSON_FEMALE",
    "WORLD_MALE", "WORLD_FEMALE",
    "UNKNOWN_SLOT",
}
LEGACY_ROLE = ("WEARABLE", "WORLD", "GROUND", "UNKNOWN")
CANONICAL_ROLE = "WEARABLE_FEMALE_3P"
PHYSICS_ENUM = ("HDT_SMP_XML", "CBPC_CONFIG", "OTHER_PHYSICS_CONFIG")
LOOKUP_CLASSES = ("EXTERNAL_PROVIDER_FOUND", "TRUE_MISSING", "GLOBAL_BODY_SKIN",
                  "VANILLA_ENGINE_RESOURCE", "UNKNOWN")


def load(k):
    p = os.path.join(OUT, F[k])
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def col(r, *names, default=""):
    low = {k.lower().strip(): v for k, v in r.items() if k}
    for n in names:
        v = low.get(n.lower().strip())
        if v is not None:
            return (v or "").strip()
    return default


def is_unk(v):
    return (v or "").strip().upper() in ("UNKNOWN", "UNRESOLVED", "", "TBD", "PENDING", "N/A", "NA", "NONE")


def under(p, root):
    """True when p is inside root. Tolerates a missing trailing separator and
    a bare directory value that equals the namespace root itself."""
    p = C.norm(p).rstrip("/")
    r = C.norm(root).rstrip("/")
    if not p or not r:
        return False
    return p == r or p.startswith(r + "/")


def mesh_ns(o):
    return "meshes/ZLJ/CombatLatex/%s/" % o.lower()


def tex_ns(o):
    return "textures/ZLJ/CombatLatex/%s/" % o.lower()


def sd_ns(o):
    return "CalienteTools/BodySlide/ShapeData/ZLJ_Combat_Latex/%s/" % o.lower()


def osp_ns(o):
    return C.norm("CalienteTools\\BodySlide\\SliderSets\\ZLJ_%s.osp" % o)


def verdict(b, r):
    return "BLOCKED" if b else ("REVIEW" if r else "PASS")


def main():
    d = {k: load(k) for k in F}
    absent = [F[k] for k in F if d.get(k) is None]
    mine = lambda k, o: [r for r in (d.get(k) or []) if col(r, "OUTFIT_ID") == o]

    # ---------- global provider lookup index ----------
    lk = {}
    for r in (d["lookup"] or []):
        lk[C.norm(r["virtual_path"])] = r

    # ---------- independent collision re-derivation ----------
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
            v = C.norm(col(r, "new_osp"))
            if v and not is_unk(v):
                tgt[v].append((o, col(r, "old_osp")))
        for r in mine("morph", o):
            v = C.norm(col(r, "target_tri"))
            if v and not is_unk(v):
                tgt[v].append((o, col(r, "source_tri")))
    collisions = [(t, v) for t, v in tgt.items() if len({o for o, _ in v}) > 1]
    coll_by = Counter()
    for t, v in collisions:
        for o in {o for o, _ in v}:
            coll_by[o] += 1

    header = ["OUTFIT_ID", "check_id", "check_name", "result", "metric_value", "threshold",
              "remaining_cross_outfit_refs", "remaining_external_mod_refs", "unresolved_refs",
              "vanilla_allowed_refs", "global_body_skin_refs", "true_missing_refs",
              "shared_material_proposals", "target_path_collisions", "evidence", "notes"]
    rows = []
    pack = Counter()
    cls_pack = Counter()
    missing_prov = []

    for o in C.OUTFIT_IDS:
        mesh, tex, clo = mine("mesh", o), mine("texture", o), mine("closure", o)
        nifrw, bs, sdrw = mine("nif_rewrite", o), mine("bodyslide", o), mine("sd_rewrite", o)
        pl, arma, ptex = mine("plugin", o), mine("arma", o), mine("plugin_tex", o)
        phys, morph = mine("physics", o), mine("morph", o)

        cross_open = [r for r in clo
                      if col(r, "dependency_type").upper() in ("CROSS_OUTFIT", "CROSS_PACK_CANDIDATE")
                      and not col(r, "post_plan_state").upper().startswith("CLOSED")]

        # ---- reference classes from the global provider lookup ----
        SENT = ("UNKNOWN", "", "(WHOLE MESH)", "N/A", "NONE", "PENDING")
        cls = Counter()
        for r in nifrw + sdrw:
            raw = (col(r, "old_dds_path") or "").strip()
            v = C.norm(raw)
            if not v or raw.upper() in SENT or not (col(r, "status") or "").upper().startswith("UNRESOLVED"):
                continue
            g = lk.get(v)
            if g is None:
                missing_prov.append((o, v))
                cls["NO_LOOKUP_PROVENANCE"] += 1
                continue
            c = g["classification"]
            cls[c] += 1
            cls_pack[c] += 1
        ext_missing = cls["EXTERNAL_PROVIDER_FOUND"]
        true_missing = cls["TRUE_MISSING"]
        hard = cls["UNKNOWN"] + cls["NO_LOOKUP_PROVENANCE"]
        van_ok = cls["VANILLA_ENGINE_RESOURCE"]
        gskin = cls["GLOBAL_BODY_SKIN"]
        props = [r for r in nifrw + sdrw
                 if (col(r, "status") or "").upper() == "PROPOSAL_SHARED_NOT_APPROVED"
                 or (col(r, "shared_proposal") or "").upper() == "PROPOSAL_SHARED_NOT_APPROVED"]
        coll_n = coll_by.get(o, 0)

        def add(cid, name, res, val, thr, ev, note=""):
            rows.append([o, cid, name, res, val, thr, len(cross_open), ext_missing, hard,
                         van_ok, gskin, true_missing, len(props), coll_n, ev, note])
            pack[res] += 1

        # ---------- C1 GAME MESH ----------
        if d["mesh"] is None:
            add("C1", "GAME_MESH_SELF_CONTAINED", "BLOCKED", -1, 0, "P02A_MESH_MIGRATION.csv missing", "upstream absent")
        else:
            game = [r for r in mesh if col(r, "mesh_class").upper() in ("GAME_NIF", "GAME_MESH", "GAME", "")]
            off = [r for r in game if not under(col(r, "target_virtual_path", "target_path"), mesh_ns(o))]
            add("C1", "GAME_MESH_SELF_CONTAINED", verdict((not game) or bool(off) or bool(coll_n), False),
                len(game) - len(off), len(game),
                "game mesh rows=%d, target off-namespace=%d, collisions=%d" % (len(game), len(off), coll_n),
                "; ".join(sorted({col(r, "target_virtual_path", "target_path") for r in off})[:3]))

        # ---------- C2 TEXTURE ----------
        if d["nif_rewrite"] is None or d["closure"] is None:
            add("C2", "TEXTURE_SELF_CONTAINED", "BLOCKED", -1, 0, "NIF/closure CSV missing", "upstream absent")
        else:
            refs = nifrw + sdrw
            off = [r for r in refs if not under(col(r, "new_dds_path"), tex_ns(o))
                   and not (col(r, "status") or "").upper().startswith("UNRESOLVED")
                   and (col(r, "status") or "").upper() != "PROPOSAL_SHARED_NOT_APPROVED"
                   and (col(r, "status") or "").upper() != "KEEP_EXTERNAL_REFERENCE"]
            add("C2", "TEXTURE_SELF_CONTAINED", verdict(bool(off), bool(props or cross_open or ext_missing or true_missing or hard)),
                len(refs) - len(off) - ext_missing - true_missing - hard - van_ok - gskin, len(refs),
                "slots(nif=%d shapedata=%d) | off-namespace=%d | provider-found=%d | true-missing=%d | path-mismatch-unknown=%d | no-lookup=%d | vanilla=%d | global-body-skin=%d | proposals=%d | open cross-outfit=%d"
                % (len(nifrw), len(sdrw), len(off), ext_missing, true_missing, cls["UNKNOWN"],
                   cls["NO_LOOKUP_PROVENANCE"], van_ok, gskin, len(props), len(cross_open)),
                "GLOBAL_BODY_SKIN must never be copied into the outfit namespace")

        # ---------- C3 BODYSLIDE ----------
        if d["bodyslide"] is None:
            add("C3", "BODYSLIDE_SELF_CONTAINED", "BLOCKED", -1, 0, "P02A_BODYSLIDE_MIGRATION.csv missing", "upstream absent")
        else:
            chain_bad = [r for r in bs if any(is_unk(col(r, f)) for f in
                            ("new_osp", "new_shape_data", "new_input_nif", "new_osd", "new_output_path", "new_output_file"))]
            osp_off = [r for r in bs if not is_unk(col(r, "new_osp")) and C.norm(col(r, "new_osp")) != osp_ns(o)]
            sd_off = [r for r in bs if not is_unk(col(r, "new_shape_data")) and not under(col(r, "new_shape_data"), sd_ns(o))]
            out_off = [r for r in bs if not is_unk(col(r, "new_output_path")) and not under(col(r, "new_output_path"), mesh_ns(o))]
            unk_basis = [r for r in bs if col(r, "relationship_basis").upper() == "UNKNOWN"]
            sd_off_tex = [r for r in sdrw if not under(col(r, "new_dds_path"), tex_ns(o))
                          and (col(r, "status") or "").upper() not in ("UNRESOLVED", "PROPOSAL_SHARED_NOT_APPROVED", "KEEP_EXTERNAL_REFERENCE")]
            add("C3", "BODYSLIDE_SELF_CONTAINED", verdict(bool(chain_bad), bool(osp_off or sd_off or out_off or unk_basis or sd_off_tex)),
                len(bs) - len(chain_bad), len(bs),
                "projects=%d chain-incomplete=%d OSP-off-ns=%d ShapeData-off-ns=%d Output-off-ns=%d UNKNOWN-basis=%d shapedata-tex-off-ns=%d"
                % (len(bs), len(chain_bad), len(osp_off), len(sd_off), len(out_off), len(unk_basis), len(sd_off_tex)),
                "frozen rule: one target OSP per outfit, multiple slider sets inside it")

        # ---------- C4 PLUGIN / C6 MODEL ROLE ----------
        if d["arma"] is None:
            add("C4", "PLUGIN_PATHS_PLANNED", "BLOCKED", -1, 0, "ARMA CSV missing", "upstream absent")
            add("C6", "MODEL_ROLE_SCHEMA", "BLOCKED", -1, 0, "ARMA CSV missing", "upstream absent")
        else:
            bad_tp = [r for r in pl if col(r, "target_plugin").lower() != C.TARGET_PLUGIN.lower()]
            no_edid = [r for r in pl if is_unk(col(r, "new_edid")) or not col(r, "new_edid").lower().startswith("zlj_cl_")]
            roles = Counter(col(r, "model_role").upper() for r in arma)
            legacy = {k: v for k, v in roles.items() if k in LEGACY_ROLE}
            bad_enum = {k: v for k, v in roles.items() if k not in MODEL_ROLE_ENUM}
            wear_f = [r for r in arma if col(r, "model_role").upper() == CANONICAL_ROLE]
            wear_f_off = [r for r in wear_f if not under(col(r, "new_path", "new_vpath"), mesh_ns(o))]
            canon_flag = [r for r in wear_f if col(r, "canonical_runtime").upper() == "YES"]
            absent = [r for r in arma if col(r, "unresolved_class").upper() == "SOURCE_ASSET_ABSENT"]
            foreign = [r for r in arma if col(r, "unresolved_class").upper() == "FOREIGN_BODY_DECISION_REQUIRED"]
            world = [r for r in arma if col(r, "model_role").upper() in ("WORLD_MALE", "WORLD_FEMALE")]
            ptex_bad = [r for r in ptex if col(r, "dependency_type").upper() == "CROSS_OUTFIT"
                        and not under(col(r, "new_dds"), tex_ns(o))]
            add("C4", "PLUGIN_PATHS_PLANNED", verdict(bool(absent), bool(no_edid or wear_f_off or ptex_bad or foreign)),
                len(pl) - len(no_edid), len(pl),
                "records=%d wrong-target-plugin=%d missing-EDID=%d canonical-female-models=%d flagged-canonical=%d world-models=%d plugin-DDS-cross-outfit-open=%d | model refs: source-asset-absent=%d foreign-body-decision=%d"
                % (len(pl), len(bad_tp), len(no_edid), len(wear_f), len(canon_flag), len(world), len(ptex_bad),
                   len(absent), len(foreign)),
                "no FormID generated in P02A; FOREIGN_BODY refs exist but belong to another body system and need a decision")
            add("C6", "MODEL_ROLE_SCHEMA", verdict(bool(legacy) or bool(bad_enum), bool(wear_f_off)),
                len(arma) - sum(legacy.values()) - sum(bad_enum.values()), len(arma),
                "role enum violations (legacy WORLD/WEARABLE/GROUND)=%d, unknown-enum=%d | distribution: %s"
                % (sum(legacy.values()), sum(bad_enum.values()),
                   ", ".join("%s=%d" % kv for kv in roles.most_common())),
                "canonical body is CBBE_3BA female; %s is the canonical runtime wearable mesh" % CANONICAL_ROLE)

        # ---------- C5 PHYSICS + G7 TRI ----------
        if d["physics"] is None:
            add("C5", "PHYSICS_PATHS_PLANNED", "BLOCKED", -1, 0, "physics CSV missing", "upstream absent")
        else:
            ctypes = Counter(col(r, "config_type").upper() for r in phys)
            tri_rows = [r for r in phys if "TRI" in col(r, "config_type").upper()
                        or col(r, "config_file", "physics_file").lower().endswith(".tri")] 
            bone_bad = [r for r in phys if col(r, "bone_check_status").upper() in ("MISSING_BONE", "UNKNOWN")]
            no_new = [r for r in phys if is_unk(col(r, "new_path_refs"))]
            add("C5", "PHYSICS_PATHS_PLANNED", verdict(bool(no_new), bool(bone_bad)),
                len(phys) - len(no_new), len(phys),
                "physics configs=%d types=%s | without-new-path=%d bone-unknown=%d"
                % (len(phys), ", ".join("%s=%d" % kv for kv in ctypes.most_common()), len(no_new), len(bone_bad)),
                "config_type must be a real physics config; *.tri belongs to BodySlide morph")
            if d["morph"] is None:
                add("G7", "TRI_MORPH_SEPARATION", "BLOCKED", -1, 0, "P02A_BODYSLIDE_MORPH_MIGRATION.csv missing", "upstream absent")
            else:
                tri_ok = [r for r in morph if col(r, "source_tri").lower().endswith(".tri")]
                add("G7", "TRI_MORPH_SEPARATION", verdict(bool(tri_rows), bool(len(morph) == 0 and tri_rows == 0 and False)),
                    len(morph) - len(tri_rows), len(morph),
                    "morph rows=%d (.tri sources=%d) | TRI rows wrongly present in physics table=%d | physics types=%s"
                    % (len(morph), len(tri_ok), len(tri_rows), ", ".join("%s=%d" % kv for kv in ctypes.most_common())),
                    "*.tri is BODY_MORPH_TRI, never a physics config")

        # ---------- C8 TARGET OSP ----------
        if d["bodyslide"] is None:
            add("C8", "TARGET_OSP_NAMESPACE", "BLOCKED", -1, 1, "bodyslide CSV missing", "upstream absent")
        else:
            oset = {C.norm(col(r, "new_osp")) for r in bs if not is_unk(col(r, "new_osp"))}
            ok = (oset == {osp_ns(o)})
            add("C8", "TARGET_OSP_NAMESPACE", verdict(not ok, False), len(oset), 1,
                "distinct target OSP for this outfit=%d expected=1 -> %s" % (len(oset), sorted(oset)[:3]),
                "frozen rule: exactly one ZLJ_<OUTFIT_ID>.osp per outfit, multiple slider sets inside")

        # ---------- C9 UNRESOLVED PROVENANCE ----------
        SENTINEL = ("UNKNOWN", "", "(WHOLE MESH)", "N/A", "NONE", "PENDING")
        unresolved_paths = set()
        no_texture_set = 0
        for r in nifrw + sdrw:
            if not (col(r, "status") or "").upper().startswith("UNRESOLVED"):
                continue
            raw = (col(r, "old_dds_path") or "").strip()
            if raw.upper() in SENTINEL or not col(r, "old_dds_path"):
                no_texture_set += 1
                continue
            unresolved_paths.add(C.norm(raw))
        no_prov = [p for p in unresolved_paths if p not in lk]
        add("C9", "UNRESOLVED_REFERENCE_PROVENANCE",
            verdict(bool(no_prov), bool(unresolved_paths)),
            len(unresolved_paths) - len(no_prov), len(unresolved_paths),
            "distinct unresolved DDS=%d, without a global provider-lookup verdict=%d, rows whose texture set is not derivable at all (BSA-resident stock mesh, no path to look up)=%d" % (len(unresolved_paths), len(no_prov), no_texture_set),
            "nothing may be called missing without a targeted global VFS lookup")

        orows = [r for r in rows if r[0] == o]
        rl = [r[3] for r in orows]
        rows.append([o, "TOTAL", "OUTFIT_SELF_CONTAINMENT", verdict("BLOCKED" in rl, "REVIEW" in rl),
                     len(orows), 9, len(cross_open), ext_missing, hard, van_ok, gskin, true_missing,
                     len(props), coll_n,
                     "C1..C9 = " + ", ".join("%s:%s" % (r[1], r[3]) for r in orows),
                     "worst-case verdict across the gates"])
        pack[verdict("BLOCKED" in rl, "REVIEW" in rl)] += 1

    # ---- pack level: the 11 OSP rule is global ----
    all_osp = Counter()
    for r in (d["bodyslide"] or []):
        v = C.norm(col(r, "new_osp"))
        if v:
            all_osp[v] += 1
    distinct_osp = len(all_osp)
    rows.append(["__PACK__", "PACK_TOTAL", "PACK_SELF_CONTAINMENT",
                 verdict(pack["BLOCKED"] > 0, pack["REVIEW"] > 0), 11, 9,
                 sum(r[6] for r in rows if r[1] == "TOTAL"),
                 sum(r[7] for r in rows if r[1] == "TOTAL"),
                 sum(r[8] for r in rows if r[1] == "TOTAL"),
                 sum(r[9] for r in rows if r[1] == "TOTAL"),
                 sum(r[10] for r in rows if r[1] == "TOTAL"),
                 sum(r[11] for r in rows if r[1] == "TOTAL"),
                 sum(r[12] for r in rows if r[1] == "TOTAL"),
                 len(collisions),
                 "outfit verdicts: " + ", ".join("%s=%d" % kv for kv in sorted(pack.items()) if kv[0] in ("PASS", "REVIEW", "BLOCKED"))
                 + " | distinct target OSP pack-wide = %d (expected 11)" % distinct_osp
                 + " | reference classes: " + ", ".join("%s=%d" % kv for kv in sorted(cls_pack.items())),
                 "target-path collisions = %d" % len(collisions)])

    C.write_csv(os.path.join(OUT, "P02A_SELF_CONTAINMENT_AUDIT.csv"), header, rows)

    # ---- refreshed unresolved classification, sourced from the global lookup ----
    cls_rows = []
    for r in (d["nif_rewrite"] or []) + (d["sd_rewrite"] or []):
        v = C.norm(col(r, "old_dds_path"))
        if not v or not (col(r, "status") or "").upper().startswith("UNRESOLVED"):
            continue
        g = lk.get(v)
        cls_rows.append([
            col(r, "OUTFIT_ID"),
            v,
            g["classification"] if g else "NO_LOOKUP_PROVENANCE",
            (g["winning_provider"] if g else ""),
            (g["winning_priority"] if g else ""),
            (g["providers_all"] if g else ""),
            (g["lookup_scope"] if g else "no global provider-lookup row for this path"),
            col(r, "status"),
            col(r, "notes"),
        ])
    C.write_csv(os.path.join(OUT, "P02A_UNRESOLVED_REFERENCE_CLASSIFICATION.csv"),
                ["OUTFIT_ID", "virtual_path", "reference_class", "winning_provider", "winning_priority",
                 "providers_all", "lookup_scope", "ledger_status", "notes"], cls_rows)

    print("=" * 78)
    print("P02A.1 SELF-CONTAINMENT AUDIT")
    print("outfit verdicts:", dict(pack))
    print("target path collisions:", len(collisions))
    print("distinct target OSP pack-wide: %d (expected 11)" % distinct_osp)
    print("reference classes (rows):", dict(cls_pack))
    for o in C.OUTFIT_IDS:
        r = [x for x in rows if x[0] == o and x[1] == "TOTAL"][0]
        print("  %-20s %-8s cross=%-2d prov=%-4d true_missing=%-3d unknown=%-3d gskin=%-3d coll=%d"
              % (o, r[3], r[6], r[7], r[11], r[8], r[10], r[13]))
    if absent:
        print("ABSENT DELIVERABLES:", absent)
    if missing_prov:
        print("unresolved paths lacking provider provenance:", len(set(missing_prov)))
    print("wrote", os.path.join(OUT, "P02A_SELF_CONTAINMENT_AUDIT.csv"))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
