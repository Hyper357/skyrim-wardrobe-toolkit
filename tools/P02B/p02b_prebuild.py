# -*- coding: utf-8 -*-
"""P02B1.1 pre-build corrections.

 1. P02B_CL06_UNKNOWN_TEXTURE_AUDIT.csv   - classify the 9 unresolved DDS rows
 2. P02B_CL06_BODYSLIDE_ARMA_MATRIX.csv   - BodySlide output -> ARMA slot matrix

Reports only: no asset is copied or rewritten here.
"""
import csv
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "P02A"))
import p02a_common as C

OUTFIT = "CL06_ToxicCat"
STAGING = os.path.join(C.ROOT, "staging", "ZLJ Combat Latex Pack - P02B Pilot")
REPORTS = os.path.join(C.ROOT, "reports", "P02B")
P = C.P00.get()


def R(f):
    return list(csv.DictReader(open(os.path.join(C.OUT, f), encoding="utf-8-sig")))


def mine(f):
    return [r for r in R(f) if (r.get("OUTFIT_ID") or "") == OUTFIT]


def main():
    # ---------------- 1. unknown texture audit ----------------
    tx = [r for r in mine("P02A_TEXTURE_MIGRATION.csv")
          if (r.get("action") or "").upper() == "UNRESOLVED"]
    nifrw = mine("P02A_NIF_TEXTURE_REWRITE.csv")
    mesh = {C.norm(r["source_virtual_path"]): r for r in mine("P02A_MESH_MIGRATION.csv")}
    rows = []
    for r in tx:
        ref = C.norm(r["referencing_nif"])
        m = mesh.get(ref, {})
        role = (m.get("model_role") or "UNKNOWN").upper()
        shape = (r.get("shape") or "").strip()
        slot = (r.get("texture_slot") or "").strip()
        dds = (r.get("source_virtual_path") or "").strip()
        if shape == "(whole mesh)" or slot == "(whole mesh)":
            if role in ("WEARABLE_MALE_3P", "FIRSTPERSON_MALE"):
                klass = "NOT_APPLICABLE"
                why = "external male body mesh - RULING-01 NON_CANONICAL_MALE, never migrated"
            elif role in ("WORLD_MALE", "WORLD_FEMALE"):
                klass = "NOT_APPLICABLE"
                why = "vanilla world/drop model - RULING-03 stays external, never migrated"
            else:
                klass = "PARSER_UNKNOWN"
                why = "whole-mesh row with no role; texture set not derivable from frozen P00"
        elif not dds:
            klass = "EMPTY_TEXTURE_SLOT"
            why = "named slot with no path"
        else:
            klass = "TRUE_UNRESOLVED_REFERENCE"
            why = "named slot referencing a path with no provider"
        rows.append([OUTFIT, ref, m.get("model_role", ""), shape, slot, dds,
                     klass, why, m.get("mesh_class", ""), m.get("existence", "")])
    C.write_csv(os.path.join(REPORTS, "P02B_CL06_UNKNOWN_TEXTURE_AUDIT.csv"),
                ["outfit_id", "referencing_nif", "model_role", "shape", "texture_slot",
                 "source_virtual_path", "classification", "reason", "mesh_class", "existence"], rows)

    from collections import Counter
    cls = Counter(r[6] for r in rows)
    print("UNKNOWN_TEXTURE_AUDIT rows:", len(rows), dict(cls))
    true_unres = [r for r in rows if r[6] == "TRUE_UNRESOLVED_REFERENCE"]
    print("TRUE_UNRESOLVED_REFERENCE (clothing):", len(true_unres))
    print("NOT_APPLICABLE (excluded by ruling) :", cls["NOT_APPLICABLE"])
    print("EMPTY_TEXTURE_SLOT                  :", cls["EMPTY_TEXTURE_SLOT"])
    print("PARSER_UNKNOWN                      :", cls["PARSER_UNKNOWN"])

    # ---------------- 2. BodySlide -> ARMA matrix ----------------
    osp = os.path.join(STAGING, "CalienteTools", "BodySlide", "SliderSets", "ZLJ_CL06_ToxicCat.osp")
    text = open(osp, encoding="utf-8-sig").read()
    blocks = re.findall(r'<SliderSet name="([^"]+)">(.*?)</SliderSet>', text, re.S)
    arma = mine("P02A_ARMA_MODEL_REWRITE.csv")
    by_src = defaultdict(list)
    for r in arma:
        by_src[C.norm(r.get("old_vpath") or r["old_path"])].append(r)
    parts = [p for p in P.parts if p.get("MOD_ID") == C.OUTFITS[OUTFIT]["primary"]]
    armo_of_arma = {}
    for p in parts:
        for e in (p.get("ARMA_edids") or "").split(";"):
            e = e.strip()
            if e:
                armo_of_arma[e] = p.get("ARMO_formid", "")

    mrows = []
    for name, body in blocks:
        df = re.search(r"<DataFolder>([^<]*)</DataFolder>", body)
        sf = re.search(r"<SourceFile>([^<]*)</SourceFile>", body)
        op = re.search(r"<OutputPath>([^<]*)</OutputPath>", body)
        of = re.search(r"<OutputFile[^>]*>([^<]*)</OutputFile>", body)
        datafolder = df.group(1) if df else ""
        srcfile = sf.group(1) if sf else ""
        outpath = op.group(1) if op else ""
        outfile = of.group(1) if of else ""
        sliders = len(re.findall(r"<Slider ", body))
        out0 = outpath.rstrip("\\") + "\\" + outfile + "_0.nif"
        out1 = outpath.rstrip("\\") + "\\" + outfile + "_1.nif"
        # ARMA references the BUILD OUTPUT of this slider set, i.e.
        #   <OutputFile>_0.nif / <OutputFile>_1.nif
        # not the ShapeData input (<SourceFile>). Match on the output names.
        wanted = {outfile.lower() + "_0.nif", outfile.lower() + "_1.nif", srcfile.lower()}
        hit = []
        for r in arma:
            base = C.norm(r.get("old_vpath") or r["old_path"]).rsplit("/", 1)[-1]
            if base in wanted:
                hit.append(r)
        # REFERENCE_TOPOLOGY_RULE: do several slots share one source NIF?
        slots = {r.get("subrecord", "") for r in hit}
        if len(slots) > 1:
            topology = "SHARED_RUNTIME_MESH"
        elif slots == {"MOD5"}:
            topology = "DEDICATED_1P"
        elif slots == {"MOD3"}:
            topology = "DEDICATED_3P"
        else:
            topology = "UNKNOWN"
        # canonical target: the namespace root file that BodySlide writes and that every
        # sharing slot points at. Never an artificial 1p copy.
        canonical_target = C.norm(outpath) + "/" + outfile + "_1.nif"
        if not hit:
            mrows.append([OUTFIT, name, srcfile, datafolder, outpath, outfile, out0, out1,
                          sliders, "", "", "", "NO_ARMA_REFERENCE", "n/a", "UNKNOWN",
                          canonical_target, "", "NO"])
        for r in hit:
            role = (r.get("model_role") or "").upper()
            canon = "FEMALE_3P" if role == "WEARABLE_FEMALE_3P" else (
                "FEMALE_1P" if role == "FIRSTPERSON_FEMALE" else "OTHER")
            ledger_target = C.norm(r.get("new_path") or "")
            supersedes = "YES" if ledger_target and ledger_target != C.norm(canonical_target) else "NO"
            mrows.append([OUTFIT, name, srcfile, datafolder, outpath, outfile, out0, out1,
                          sliders, armo_of_arma.get(r.get("edid", ""), ""), r.get("edid", ""),
                          r.get("formid", ""), r.get("subrecord", ""), canon, topology,
                          canonical_target, ledger_target, supersedes])
    C.write_csv(os.path.join(REPORTS, "P02B_CL06_BODYSLIDE_ARMA_MATRIX.csv"),
                ["outfit_id", "ui_name", "source_file", "data_folder", "output_path", "output_file",
                 "expected_0", "expected_1", "sliders", "related_armo_formid", "related_arma_edid",
                 "arma_formid", "arma_model_slot", "model_role", "source_reference_topology",
                 "canonical_target", "p02a_ledger_target", "corrected_by_p02b12"], mrows)
    print()
    print("ARMA_MATRIX rows:", len(mrows))
    for r in mrows:
        print("  %-46s %-26s slot=%-5s role=%-9s arm=%s" %
              (r[1][:46], r[2][:26], r[12], r[13], r[10][:22]))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
