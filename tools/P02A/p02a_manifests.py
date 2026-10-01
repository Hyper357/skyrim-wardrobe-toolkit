# -*- coding: utf-8 -*-
"""P02A per-outfit manifest generator (Lead).

Reads every teammate CSV plus the frozen P00 evidence and writes
reports/P02A/outfits/<OUTFIT_ID>.md -- one self-contained manifest per outfit.
READ-ONLY with respect to all mod/game files.
"""
import os
import re
import sys
import csv
from collections import defaultdict, Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p02a_common as C
from p02a_audit2 import load, col, is_unk, under, mesh_ns, tex_ns, sd_ns, F as AUDIT_FILES

P = C.P00.get()
OUT = C.OUT
ODIR = os.path.join(OUT, "outfits")
Q = chr(96)          # markdown code fence / inline code delimiter
UNK_TOKENS = ("UNKNOWN", "UNRESOLVED", "TBD", "PENDING", "PROPOSAL_SHARED_NOT_APPROVED")


def q(s):
    return Q + str(s) + Q


def table(header, rows, limit=None):
    if not rows:
        return "_" + q("none") + "_\n"
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    for r in (rows[:limit] if limit else rows):
        out.append("| " + " | ".join("" if c is None else str(c).replace("|", "/") for c in r) + " |")
    if limit and len(rows) > limit:
        out.append("| " + q("... %d more rows in the CSV" % (len(rows) - limit)) + " |" + " |" * (len(header) - 1))
    return "\n".join(out) + "\n"


def build(o, data, audit_rows):
    meta = C.OUTFITS[o]
    src = data["source_map"] or []
    mesh = data["mesh"] or []
    tex = data["texture"] or []
    closure = data["closure"] or []
    nifrw = data["nif_rewrite"] or []
    bs = data["bodyslide"] or []
    sdrw = data["sd_rewrite"] or []
    pl = data["plugin"] or []
    arma = data["arma"] or []
    ptex = data["plugin_tex"] or []
    phys = data["physics"] or []
    mine = lambda rows: [r for r in rows if col(r, "OUTFIT_ID") == o]
    morph = mine(data["morph"] or [])
    lookup = {C.norm(r["virtual_path"]): r for r in (data["lookup"] or [])}

    src, mesh, tex, closure = mine(src), mine(mesh), mine(tex), mine(closure)
    nifrw, bs, sdrw, pl, arma, ptex, phys = (mine(nifrw), mine(bs), mine(sdrw), mine(pl),
                                             mine(arma), mine(ptex), mine(phys))

    mods = P.mods_of_outfit(o)
    wins = Counter()
    for r in src:
        wins[col(r, "winning_provider")] += 1
    blockers = []
    for r in audit_rows:
        if r.get("OUTFIT_ID") == o and r.get("result") in ("BLOCKED", "REVIEW"):
            blockers.append(q(r.get("check_id", "")) + " " + (r.get("check_name", "") or "") +
                            " = **" + r.get("result", "") + "** - " + (r.get("evidence", "") or ""))

    n_cross = [r for r in closure if col(r, "dependency_type").upper() in ("CROSS_OUTFIT", "CROSS_PACK_CANDIDATE")]
    n_ext = [r for r in closure if col(r, "dependency_type").upper() == "EXTERNAL_MOD"]
    n_unres = [r for r in (nifrw + sdrw + ptex) if col(r, "status").upper() in UNK_TOKENS]
    ar_total = next((r for r in audit_rows if r.get("OUTFIT_ID") == o and r.get("check_id") == "TOTAL"), {})
    cls_mine = [r for r in audit_rows if r.get("reference_class") and o in (r.get("_outfits") or [])]
    cls_count = Counter(r["reference_class"] for r in cls_mine)
    n_prop = [r for r in (nifrw + sdrw + ptex) if col(r, "status").upper() == "PROPOSAL_SHARED_NOT_APPROVED"]
    pbr_mods = [m for k, m in meta.get("support", {}).items() if "PBR" in k]
    pbr_files = P.files_of_mod.get(pbr_mods[0], []) if pbr_mods else []
    short = o.split("_", 1)[1]

    L = []
    A = L.append
    A("# %s - P02A migration manifest" % o)
    A("")
    A("> Pack: " + q(C.PACK_ID) + " (" + C.DISPLAY_NAME + ") - canonical body " + q(C.CANONICAL_BODY) +
      " - target plugin " + q(C.TARGET_PLUGIN))
    A("> Phase: **P02A design ledger (STRICT READ-ONLY)** - nothing has been copied, moved, renamed or rewritten.")
    A("")
    A("| field | value |")
    A("|---|---|")
    A("| Outfit ID (frozen) | " + q(o) + " |")
    A("| Source mod(s) | " + ", ".join(q(m) for m in mods) + " |")
    A("| Plugin (current) | " + q(meta["plugin"]) + " |")
    A("| Support mods | " + (", ".join(q(v) + " (" + k + ")" for k, v in meta.get("support", {}).items()) or "NONE") + " |")
    A("| Target mesh ns | " + q("meshes\\ZLJ\\CombatLatex\\%s\\" % o) + " |")
    A("| Target texture ns | " + q("textures\\ZLJ\\CombatLatex\\%s\\" % o) + " |")
    A("| Target ShapeData ns | " + q("CalienteTools\\BodySlide\\ShapeData\\ZLJ_CombatLatex\\%s\\" % o) + " |")
    A("| Target SliderSet | " + q("CalienteTools\\BodySlide\\SliderSets\\ZLJ_%s.osp" % o) + " |")
    A("")

    A("## 1. Source Mods")
    A("")
    A(table(["MOD_ID", "MO2 priority (low = wins)", "role", "file_count", "plugin"],
            [[m, P.priority.get(m, ""),
              "BASE" if m == meta["primary"] else
              next((k for k, v in meta.get("support", {}).items() if v == m), "SUPPORT"),
              len(P.files_of_mod.get(m, [])),
              next((a.get("plugin_files", "") for a in P.mod_aggs if a["MOD_ID"] == m), "")] for m in mods]))
    A("")

    A("## 2. Winning Providers")
    A("")
    A(table(["winning_provider", "VFS paths won"], [[k, v] for k, v in wins.most_common()]) if wins
      else "_P02A_EFFECTIVE_SOURCE_MAP.csv not available yet._")
    A("")

    A("## 3. Plugin Records")
    A("")
    ct = Counter(col(r, "record_type") for r in pl)
    A("Counts by record type: " + (", ".join(q(k) + "=%d" % v for k, v in ct.most_common()) or "PENDING") + "  ")
    A("Target plugin: " + q(C.TARGET_PLUGIN) + " - new EDID namespace: " + q("ZLJ_CL_%s_<PART>" % short) +
      " - **no FormID generated in P02A**")
    A("")
    A(table(["record_type", "formid", "edid", "new_edid", "notes"],
            [[col(r, "record_type"), col(r, "formid"), col(r, "edid"), col(r, "new_edid"), col(r, "notes")]
             for r in pl if col(r, "record_type").upper() in ("ARMO", "ARMA", "COBJ", "ENCH", "KYWD", "OTFT")], 20))
    A("")

    A("## 4. Game Mesh")
    A("")
    gm = [r for r in mesh if col(r, "mesh_class").upper() in ("GAME_NIF", "GAME_MESH", "GAME", "")]
    A(table(["mesh_role", "source_virtual_path", "source_provider", "target_virtual_path", "retain"],
            [[col(r, "mesh_role"), col(r, "source_virtual_path", "source_path"),
              col(r, "source_provider"), col(r, "target_virtual_path", "target_path"),
              col(r, "retain_decision")] for r in gm], 40))
    A("")

    A("## 5. ShapeData / OSP / OSD")
    A("")
    A(table(["old_ui_name", "new_ui_name", "old_osp", "new_osp", "new_shape_data",
             "new_input_nif", "new_osd", "new_output_path", "new_output_file", "basis"],
            [[col(r, "old_ui_name"), col(r, "new_ui_name"), col(r, "old_osp"), col(r, "new_osp"),
              col(r, "new_shape_data"), col(r, "new_input_nif"), col(r, "new_osd"),
              col(r, "new_output_path"), col(r, "new_output_file"), col(r, "relationship_basis")]
             for r in bs], 40))
    A("")

    A("## 6. DDS actually in use")
    A("")
    A("Distinct source DDS in the closure: **%d**" %
      len({col(r, "source_virtual_path") for r in tex if col(r, "source_virtual_path")}))
    A("")
    A(table(["source_virtual_path", "winning_provider", "owning_outfit_of_source", "target_virtual_path", "action"],
            [[col(r, "source_virtual_path"), col(r, "winning_provider"),
              col(r, "owning_outfit_of_source"), col(r, "target_virtual_path"), col(r, "action")]
             for r in tex], 30))
    A("")

    A("## 6b. Body morph TRI (not a physics config)")
    A("")
    A(table(["source_tri", "associated_output_nif", "target_tri", "rewrite_required", "status"],
            [[col(r, "source_tri"), col(r, "associated_output_nif"), col(r, "target_tri"),
              col(r, "BODYTRI_reference_rewrite_required"), col(r, "status")] for r in morph], 30))
    A("")
    A("## 6c. Model role (ARMA/ARMO slot semantics)")
    A("")
    A(table(["model_role", "canonical_runtime", "body_relevance", "old_path", "new_path", "status"],
            [[col(r, "model_role"), col(r, "canonical_runtime"), col(r, "body_relevance"),
              col(r, "old_path"), col(r, "new_path"), col(r, "status")]
             for r in arma if col(r, "model_role").upper() == "WEARABLE_FEMALE_3P"], 25))
    A("")
    A("Non-canonical roles kept separate: " + (", ".join(
        "%s=%d" % kv for kv in Counter(col(r, "model_role") for r in arma).most_common()
        if kv[0] != "WEARABLE_FEMALE_3P") or "none"))
    A("")
    A("## 7. Physics")
    A("")
    A(table(["config_file", "config_type", "mesh_references", "bone_dependencies",
             "rewrite_required", "bone_check_status", "status"],
            [[col(r, "config_file", "physics_file"), col(r, "config_type"), col(r, "mesh_references"),
              col(r, "bone_dependencies"), col(r, "rewrite_required"),
              col(r, "bone_check_status"), col(r, "status")] for r in phys], 30))
    A("")

    A("## 8. Existing PBR (provenance only)")
    A("")
    if pbr_mods:
        A("PBR patch mod: " + q(pbr_mods[0]) +
          " - recorded as **provenance only**, not adopted as final standard (P05/P06 redesign the material standard).")
        A("")
        A(table(["virtual_path", "winning_provider"], [[f["vpath"], f["mod"]] for f in pbr_files], 25))
    else:
        A("No PBR patch mod is registered for this outfit in the P02A registry.")
    A("")

    A("## 9. Cross dependencies (current -> planned)")
    A("")
    A("- cross-outfit texture dependencies: **%d** (open after plan: %d)"
      % (len(n_cross), len([r for r in n_cross if col(r, "post_plan_state").upper() not in ("CLOSED", "RESOLVED", "OK")])))
    A("- external-mod texture dependencies: **%d** (open after plan: %d)"
      % (len(n_ext), len([r for r in n_ext if col(r, "post_plan_state").upper() not in ("CLOSED", "RESOLVED", "OK")])))
    A("- audit counters: cross-outfit open **%s** / external-mod-missing **%s** / hard-unresolved **%s** / vanilla-allowed **%s** / shared proposals **%d**"
      % (ar_total.get("remaining_cross_outfit_refs", "?"), ar_total.get("remaining_external_mod_refs", "?"),
         ar_total.get("unresolved_refs", "?"), ar_total.get("vanilla_allowed_refs", "?"), len(n_prop)))
    A("- unresolvable DDS by class (distinct files): "
      + (", ".join("%s=%d" % kv for kv in sorted(cls_count.items())) or "none")
      + " - a DDS absent from the frozen P00 VFS is already broken at runtime today; it is listed, never guessed")
    if cls_mine:
        A("")
        A(table(["reference_class", "virtual_path"],
                sorted({(r["reference_class"], r["virtual_path"]) for r in cls_mine}), 25))
    A("")
    A(table(["dependency_type", "source_owner", "source_virtual_path", "referenced_by_nif",
             "resolution_plan", "target_virtual_path", "post_plan_state"],
            [[col(r, "dependency_type"), col(r, "source_owner"), col(r, "source_virtual_path"),
              col(r, "referenced_by_nif"), col(r, "resolution_plan"),
              col(r, "target_virtual_path"), col(r, "post_plan_state")] for r in closure], 30))
    A("")

    A("## 10. Self-containment audit (simulated post-migration)")
    A("")
    A(table(["gate", "result", "metric", "evidence"],
            [[r.get("check_name", ""), r.get("result", ""), r.get("metric_value", ""),
              r.get("evidence", "")] for r in audit_rows if r.get("OUTFIT_ID") == o]))
    A("")

    A("## 11. BLOCKERS")
    A("")
    for b in blockers:
        A("- " + b)
    if not blockers:
        A("- none recorded")
    A("")
    A("---")
    A("")
    A("P02A stops here. No COPY / MOVE / DELETE / NIF / ESP / OSP / DDS write was performed and none is "
      "authorised until this design is reviewed by a human.")
    A("")
    return "\n".join(L)


def main():
    data = {k: load(k) for k in
            ("source_map", "mesh", "texture", "closure", "nif_rewrite", "bodyslide", "morph",
             "sd_rewrite", "plugin", "arma", "plugin_tex", "physics", "lookup")}
    audit_rows = []
    for nm in ("P02A_SELF_CONTAINMENT_AUDIT.csv", "P02A_UNRESOLVED_REFERENCE_CLASSIFICATION.csv"):
        p = os.path.join(OUT, nm)
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        if nm.startswith("P02A_SELF"):
            audit_rows = rows
        else:
            for r in rows:
                for o in (r.get("affected_outfits") or "").split(";"):
                    if o:
                        r.setdefault("_outfits", []).append(o)
    os.makedirs(ODIR, exist_ok=True)
    for o in C.OUTFIT_IDS:
        p = os.path.join(ODIR, o + ".md")
        C.write_md(p, build(o, data, audit_rows))
        print("wrote", p)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
