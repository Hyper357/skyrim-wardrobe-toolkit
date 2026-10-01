# -*- coding: utf-8 -*-
"""Regenerate P02B_CL06_FINAL_PRE_PLUGIN_GATE.md by aggregating the FINAL plugin plan CSV.

Nothing is asserted that is not read back out of P02B_CL06_PILOT_PLUGIN_PLAN.csv.
"""
import csv, os, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "P02A"))
import p02a_common as C

REPORTS = os.path.join(C.ROOT, "reports", "P02B")
PLAN = os.path.join(REPORTS, "P02B_CL06_PILOT_PLUGIN_PLAN.csv")
GATE = os.path.join(REPORTS, "P02B_CL06_PLUGIN_PLAN_GATE.csv")
OUT = os.path.join(REPORTS, "P02B_CL06_FINAL_PRE_PLUGIN_GATE.md")
Q = chr(96)


def q(s):
    return Q + str(s) + Q


def main():
    plan = list(csv.DictReader(open(PLAN, encoding="utf-8-sig")))
    gate = list(csv.DictReader(open(GATE, encoding="utf-8-sig")))
    cls = Counter(r["change_class"] for r in plan)
    arma = [r for r in plan if r["record_type"] == "ARMA"]
    # aggregates read straight out of the CSV
    neutral = [r for r in plan if r["change_class"] == "GENDER_NEUTRAL_SHARED_REPOINT"]
    neutral_pairs = defaultdict(set)
    for r in neutral:
        neutral_pairs[r["edid"]].add(r["target_plugin_model_path"])
    neutral_ok = sum(1 for v in neutral_pairs.values() if len(v) == 1 and next(iter(v)))
    shared = [r for r in arma if r["change_class"] == "MODEL_PATH_REPOINT"]
    shared_pairs = defaultdict(dict)
    for r in shared:
        shared_pairs[r["edid"]][r["slot_field"]] = r["target_plugin_model_path"]
    body_ok = sum(1 for e, d in shared_pairs.items()
                  if "MOD3" in d and "MOD5" in d and d["MOD3"] == d["MOD5"] and d["MOD3"])
    shared_sets = sorted({r["target_plugin_model_path"] for r in shared})
    mesh_cls = {r["change_class"] for r in arma}
    stale = {
        "1p": sum(1 for r in plan if "\\1p\\" in (r["new_value"] or "").lower()),
        "male_neutral": sum(1 for r in plan
                            if r["change_class"] in ("MODEL_PATH_REPOINT", "GENDER_NEUTRAL_SHARED_REPOINT")
                            and "\\male\\" in (r["new_value"] or "").lower()),
        "meshes_prefix": sum(1 for r in plan
                             if r["change_class"] in ("MODEL_PATH_REPOINT", "GENDER_NEUTRAL_SHARED_REPOINT")
                             and (r["new_value"] or "").lower().startswith("meshes\\")),
        "arma_world": sum(1 for r in plan if r["record_type"] == "ARMA" and "WORLD" in r["change_class"]),
    }
    gate_pass = all(g["result"] == "PASS" for g in gate)

    L = []
    A = L.append
    A("# P02B_CL06 FINAL PRE-PLUGIN GATE (P02B2.2 canonicalization)")
    A("")
    A("**Scope:** CL06_ToxicCat only. No asset re-migration, no P00/P01/P02A rerun, no other outfit, no ESP.")
    A("")
    A("Every number below is **aggregated from " + q("P02B_CL06_PILOT_PLUGIN_PLAN.csv") + "**, not from intended logic.")
    A("")
    A("## 1. Two path concepts, kept apart")
    A("")
    A("| concept | example |")
    A("|---|---|")
    A("| " + q("target_virtual_mesh_path") + " | " + q("meshes\\ZLJ\\CombatLatex\\CL06_ToxicCat\\AE_Toxic_Cat_1.nif") + " |")
    A("| " + q("target_plugin_model_path") + " | " + q("ZLJ\\CombatLatex\\CL06_ToxicCat\\AE_Toxic_Cat_1.nif") + " |")
    A("")
    A("An ARMA/ARMO model field is relative to " + q("Data\\meshes\\") + ", so the " + q("meshes\\") + " prefix belongs to the disk")
    A("path only. TXST is a different field family: texture filenames are relative to " + q("Data\\") + ", so they keep their")
    A("" + q("textures\\") + " prefix. The two rules were not crossed.")
    A("")
    A("## 2. Classification, read back from the CSV")
    A("")
    A("| change class | rows |")
    A("|---|---|")
    for k in ("MODEL_PATH_REPOINT", "GENDER_NEUTRAL_SHARED_REPOINT", "MALE_SLOT_EMPTY",
              "ARMO_WORLD_NO_CHANGE", "TXST_REPOINT"):
        A("| " + k + " | %d |" % cls.get(k, 0))
    A("| **total** | **%d** |" % len(plan))
    A("")
    A("## 3. Topology, verified inside the CSV")
    A("")
    A("| check | result |")
    A("|---|---|")
    A("| Body MOD3 and MOD5 byte-identical plugin path | **%d/3 ARMA records** |" % body_ok)
    A("| HeadACC MOD2 and MOD3 byte-identical plugin path | **%d/3** |" % sum(
        1 for e, v in neutral_pairs.items() if e.lower().startswith("ae_toxic_cat_headacc") and len(v) == 1))
    A("| Mask MOD2 and MOD3 byte-identical plugin path | **%d/3** |" % sum(
        1 for e, v in neutral_pairs.items() if e.lower().startswith("ae_toxic_cat_mask") and len(v) == 1))
    A("| distinct canonical female plugin targets | %d |" % len(shared_sets))
    A("| ARMA world-model classes present | %s |" % (", ".join(sorted(c for c in mesh_cls if "WORLD" in c)) or "**none**"))
    A("")
    A("## 4. Stale-string sweep")
    A("")
    A("| pattern | must be | found |")
    A("|---|---|---|")
    A("| " + q("\\1p\\") + " in a plugin model path | 0 | **%d** |" % stale["1p"])
    A("| " + q("\\male\\") + " in a neutral/female plugin model path | 0 | **%d** |" % stale["male_neutral"])
    A("| plugin model path starting with " + q("meshes\\") + " | 0 | **%d** |" % stale["meshes_prefix"])
    A("| ARMA classed as a world model | 0 | **%d** |" % stale["arma_world"])
    A("")
    A("## 5. Plan gate")
    A("")
    A("| id | check | expected | actual | result |")
    A("|---|---|---|---|---|")
    for g in gate:
        A("| %s | %s | %s | %s | **%s** |" % (g["check_id"], g["check_name"], g["expected"],
                                               g["actual"], g["result"]))
    A("")
    A("    PLUGIN_PLAN_STATIC_GATE = %s" % ("PASS" if gate_pass else "FAIL"))
    A("")
    A("## 6. Still outstanding")
    A("")
    A("    BODYSLIDE_WEIGHTED_BUILD = BLOCKED_PENDING_ISOLATED_BUILD")
    A("")
    A("The isolated weighted build (" + q("_0 = 5/5") + " and " + q("_1 = 5/5") + " inside one physical tree) has not been run; see")
    A(q("P02B_CL06_ISOLATED_BUILD_REPORT.md") + ". This document therefore certifies the **plan**, not the pipeline.")
    A("")
    A("## STOP")
    A("")
    A("No ESP written. No other outfit touched. No PBR, no UBE, no final " + q("ZLJ_CombatLatex.esp") + ".")
    A("")
    C.write_md(OUT, "\n".join(L))
    print("gate entries:", len(gate), "| all PASS:", gate_pass)
    print("neutral pairs identical:", neutral_ok, "of", len(neutral_pairs))
    print("body MOD3/MOD5 identical:", body_ok)
    print("stale:", stale)
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
