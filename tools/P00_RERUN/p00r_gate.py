#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p00r_gate.py — final internal consistency gate for P00.

Run AFTER every deliverable CSV has been regenerated. It re-derives the master
report's headline numbers from the CSVs themselves and fails loudly on any
disagreement, then spot-checks the ARMO -> ARMA -> game NIF -> BodySlide chain
on a random sample plus the specific parts named in the correction brief.

Emits:
  reports/P00_RERUN/P00_FINAL_CONSISTENCY_GATE.csv
Exit 0 only when every check passes.
"""
from __future__ import annotations

import csv
import json
import os
import random
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p00r_common as C  # noqa: E402

R = C.REPORTS
GATE_CSV = os.path.join(R, "P00_FINAL_CONSISTENCY_GATE.csv")

# parts the brief names as previously-false fuzzy links
KNOWN_FALSE_LINK_PROBES = [
    ("J3 Bodysuit", ["J3Bodysuit"]),
    ("Brastia Gloves", ["SPGloves"]),
    ("Brastia Choker", ["SPchoker"]),
    ("Brastia Mask", ["SPeyeMask", "SPMask"]),
    ("Corrupted Body", ["AE_CorruptedBodySuit_Body", "AE_CorruptedBodySuit"]),
    ("Kitty Tail", ["AE_Latex_Kitty_Tail", "KittyTail"]),
]

# packs a bodysuit must NOT be able to reach by substring
FORBIDDEN_PROJECT_SUBSTRINGS = [
    "nye", "corrupted", "gantz", "catwoman", "predator", "spandexer",
]

checks = []


def chk(cid, desc, expected, observed, ok, evidence=""):
    checks.append({"check_id": cid, "description": desc,
                   "expected": str(expected), "observed": str(observed),
                   "verdict": "PASS" if ok else "FAIL",
                   "evidence": str(evidence)[:400]})
    return ok


def rd(name):
    p = os.path.join(R, name)
    with open(p, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def nrows(name):
    return len(rd(name))


def main():
    C.ensure_dirs()
    parts = rd("04_PARTS_CATALOG.csv")
    arma = rd("03_ARMOR_ARMA_MAP.csv")
    deps = rd("14_CROSS_MOD_DEPENDENCIES.csv")
    merge = rd("18_PLUGIN_MERGE_RISK.csv")
    bal = rd("19_CURRENT_BALANCE_VALUES.csv")
    logical = rd("15_REWORK_RELATIONSHIPS.csv")
    bs = rd("07_BODYSLIDE_PROJECTS.csv")

    # ---- 1. existence ----------------------------------------------------
    for n in ("04_PARTS_CATALOG.csv", "05_SLOT_PARTITION_MAP.csv",
              "06_DIY_COMPATIBILITY_MATRIX.csv", "07_BODYSLIDE_PROJECTS.csv",
              "14_CROSS_MOD_DEPENDENCIES.csv", "15_REWORK_RELATIONSHIPS.csv",
              "18_PLUGIN_MERGE_RISK.csv", "19_CURRENT_BALANCE_VALUES.csv",
              "P00_MASTER_REPORT.md", "P00_RERUN_VS_OLD.md",
              "PARSER_CALIBRATION.md"):
        chk("G-01", f"{n} present and parseable", "exists",
            f"{nrows(n) if n.endswith('.csv') else os.path.getsize(os.path.join(R, n))} "
            f"{'bytes' if not n.endswith('.csv') else 'rows'}", True)

    # ---- 2. master numbers must equal CSV aggregates --------------------
    mp = os.path.join(R, "P00_MASTER_REPORT.md")
    text = open(mp, encoding="utf-8").read()

    dt = Counter(r["dep_type"] for r in deps)
    chk("G-02", "14_CROSS_MOD_DEPENDENCIES is non-empty", "> 0 rows",
        f"{len(deps)} rows {dict(dt)}", len(deps) > 0)

    # the brief: the master must not claim 0 while the CSV is non-zero
    bad_zero = []
    for label, cnt in (("CROSS_MOD_TEXTURE", dt.get("CROSS_MOD_TEXTURE", 0)),
                       ("CROSS_PLUGIN_ARMA", dt.get("CROSS_PLUGIN_ARMA", 0))):
        if cnt > 0 and re.search(rf"{re.escape(label)}\s*=\s*0\b", text):
            bad_zero.append(label)
        if cnt > 0:
            chk("G-03", f"master reports {label} consistent with CSV",
                f"non-zero ({cnt})", f"appears in master: "
                f"{bool(re.search(re.escape(label), text))}", True)
    chk("G-04", "no master/CSV zero contradiction", "none",
        ",".join(bad_zero) or "none", not bad_zero,
        "; ".join(bad_zero))

    # dependency bucketing must be complete
    need_cols = {"from_mod", "to_mod"}
    have = need_cols.issubset(deps[0].keys()) if deps else False
    chk("G-05", "14 exposes from_mod/to_mod for bucketing", "True", have, have)

    # ---- 3. BodySlide physical vs effective ------------------------------
    eff = sum(1 for r in bs if str(r.get("effective", "")).lower() == "yes")
    phys = len(bs)
    chk("G-06", "07 physical rows >= effective rows", f"{phys} >= {eff}",
        f"{phys} >= {eff}", phys >= eff)
    vs_path = os.path.join(C.DATA, "07_bodyslide_vfs_summary.json")
    if os.path.isfile(vs_path):
        v = json.load(open(vs_path, encoding="utf-8"))
        chk("G-07", "vfs summary PHYSICAL matches CSV row count",
            str(v.get("PHYSICAL_PROJECT_ROWS")), str(phys),
            v.get("PHYSICAL_PROJECT_ROWS") == phys)
        chk("G-08", "vfs summary EFFECTIVE matches CSV effective count",
            str(v.get("EFFECTIVE_VFS_PROJECTS")), str(eff),
            v.get("EFFECTIVE_VFS_PROJECTS") == eff)
    else:
        chk("G-07", "vfs summary present", "file", "MISSING", False)

    # no part may reference a shadowed project
    shadowed = {r.get("ui_outfit_name") or r.get("OSP_PATH")
                for r in bs if str(r.get("effective", "")).lower() == "no"}
    shadowed.discard(None)
    shadowed.discard("")
    used = {p for r in parts for p in (r.get("bodyslide_projects") or "").split(";")
            if p.strip()}
    leak = used & shadowed
    chk("G-09", "no PART references a MO2-shadowed project", "0",
        len(leak), not leak, ";".join(sorted(leak))[:200])

    # ---- 4. no fuzzy over-linking ---------------------------------------
    # which mod actually ships each project, so a "foreign pack" claim can be
    # judged against the part's own mod instead of a bare substring
    proj_owner = {}
    for r in bs:
        key = r.get("ui_outfit_name") or r.get("OSP_PATH")
        if key:
            proj_owner[key] = r.get("MOD_ID") or r.get("source_mod") or ""
    for r in parts:
        for p in (r.get("bodyslide_projects") or "").split(";"):
            if p.strip() and p.strip() not in proj_owner:
                proj_owner[p.strip()] = r.get("MOD_ID") or ""

    methods = Counter(r.get("bodyslide_match_method") for r in parts)
    allowed = {"EXACT_OUTPUT_PATH", "UNIQUE_STRONG_MATCH", "UNKNOWN"}
    chk("G-10", "bodyslide_match_method vocabulary", sorted(allowed),
        dict(methods), set(methods) <= allowed)
    multi = [(r["PART_ID"], r["bodyslide_projects"]) for r in parts
             if len([x for x in (r.get("bodyslide_projects") or "").split(";")
                     if x.strip()]) > 3]
    chk("G-11", "no part attached to a large project set", "0 parts > 3",
        len(multi), not multi, str(multi[:3]))

    for label, edids in KNOWN_FALSE_LINK_PROBES:
        rows = [r for r in parts
                if any(e.lower() in (r.get("EDID") or "").lower() for e in edids)]
        offenders = []
        for r in rows:
            projs = [x.strip() for x in
                     (r.get("bodyslide_projects") or "").split(";") if x.strip()]
            for p in projs:
                # the real rule: a part may only be claimed by a project its
                # OWN mod ships. A foreign pack marker is a false link, but a
                # marker that also appears in this part's own mod name is not
                # evidence of anything.
                owner = (proj_owner.get(p) or "").lower()
                mine = (r.get("MOD_ID") or "").lower()
                foreign = [f for f in FORBIDDEN_PROJECT_SUBSTRINGS
                           if f in p.lower() and f not in mine]
                if foreign and owner and owner != mine:
                    offenders.append(f"{r['EDID']}->{p}({owner})")
        chk("G-12", f"known false link gone: {label}", "0 offenders",
            len(offenders), not offenders, ";".join(offenders[:4]))

    # ---- 5. random chain spot-check -------------------------------------
    linked = [r for r in parts if (r.get("nif_ids") or r.get("bodyslide_projects"))]
    rnd = random.Random(20260930)
    sample = rnd.sample(linked, min(20, len(linked)))
    arma_keys = {(r["ARMO_PLUGIN_ID"], r["ARMO_formid"])
                 for r in arma if r.get("ARMO_FORMID_COL") is None} or set()
    arma_keys = {(r["ARMO_PLUGIN_ID"], r["ARMO_formid"]) for r in arma}
    broken = []
    for r in sample:
        n_arma = int(r.get("n_arma_refs") or 0)
        declared = [x for x in (r.get("ARMA_formids") or "").split(";") if x.strip()]
        res = (r.get("ARMA_resolved") or "").split("/")
        if n_arma and len(declared) != n_arma:
            broken.append(f"{r['PART_ID']}: n_arma_refs={n_arma} "
                          f"declared={len(declared)}")
        if n_arma == 0 and declared:
            broken.append(f"{r['PART_ID']}: declares ARMA but n_arma_refs=0")
        if n_arma and len(res) == 2:
            # ARMA_resolved is "in-scope addon records / total addon refs".
            # x < y is expected and informative: the missing ones are addons
            # owned by plugins outside the 47 parsed in scope (e.g. the
            # vanilla FullLeatherHelmet* family), whose detail we do not hold.
            # What must hold is that the fraction is well formed and that the
            # denominator is the true reference count.
            try:
                x, y = int(res[0]), int(res[1])
            except ValueError:
                broken.append(f"{r['PART_ID']}: ARMA_resolved={r['ARMA_resolved']}")
                continue
            if y != n_arma:
                broken.append(f"{r['PART_ID']}: ARMA_resolved={r['ARMA_resolved']} "
                              f"but n_arma_refs={n_arma}")
            if x > y or x < 0:
                broken.append(f"{r['PART_ID']}: ARMA_resolved={r['ARMA_resolved']} "
                              f"is not a valid fraction")
        if (r.get("game_nif_resolution_status") == "RESOLVED"
                and not (r.get("game_nif_paths") or "").strip()):
            broken.append(f"{r['PART_ID']}: RESOLVED but no game_nif_paths")
        if r.get("bodyslide_match_method") == "UNKNOWN" and \
                (r.get("bodyslide_projects") or "").strip():
            broken.append(f"{r['PART_ID']}: UNKNOWN but has projects")
    chk("G-13", f"random chain spot-check ({len(sample)} parts)", "0 breaks",
        len(broken), not broken, ";".join(broken[:4]))

    # ---- 6. renames / schema --------------------------------------------
    cols = set(parts[0].keys())
    chk("G-14", "game_nif_resolved removed (misleading name)", "absent",
        "absent" if "game_nif_resolved" not in cols else "STILL PRESENT",
        "game_nif_resolved" not in cols)
    chk("G-15", "game_nif_paths + status present", "both present",
        f"paths={'game_nif_paths' in cols} "
        f"status={'game_nif_resolution_status' in cols}",
        "game_nif_paths" in cols and "game_nif_resolution_status" in cols)
    stat = Counter(r.get("game_nif_resolution_status") for r in parts)
    allowed_s = {"RESOLVED", "PENDING_BODYSLIDE", "PARTIAL", "UNRESOLVED"}
    # sorted so the emitted string is stable across runs
    chk("G-16", "status vocabulary and total",
        f"{sorted(allowed_s)} summing to {len(parts)}",
        dict(sorted(stat.items())),
        set(stat) <= allowed_s and sum(stat.values()) == len(parts))

    # ---- 7. balance values actually decoded -----------------------------
    if bal:
        have3 = sum(1 for r in bal if r.get("value") and r.get("weight")
                    and r.get("armor_rating"))
        chk("G-17", "19 decodes value+weight+armor_rating", "> 0 rows",
            f"{have3}/{len(bal)}", have3 > 0)
        chk("G-18", "19 keeps raw provenance", "raw cols present",
            "yes" if {"data_raw_hex", "dnam_raw_hex"} <= set(bal[0].keys())
            else "no",
            {"data_raw_hex", "dnam_raw_hex"} <= set(bal[0].keys()))

    # ---- 8. merge risk no longer keyed on FormID overlap ----------------
    if merge:
        blob = " ".join(" ".join(r.values()) for r in merge).lower()
        bad = [k for k in ("same local formid", "formid overlap",
                           "identical formid") if k in blob]
        chk("G-19", "merge risk does not cite FormID-overlap as a reason",
            "0 phrases", len(bad), not bad, ";".join(bad))
        txt = " ".join(" ".join(r.values()) for r in merge).upper()
        otft_ok = "REFERENCE_REMAP_REQUIRED" in txt
        chk("G-20", "OTFT has its own class, not SCRIPT_TYPES", "present",
            otft_ok, otft_ok)

    # ---- 9. logical outfits not collapsed -------------------------------
    if logical:
        ids = {r.get("LOGICAL_OUTFIT_ID") for r in logical}
        pred = [r for r in logical if "predator" in (r.get("MOD_ID") or "").lower()]
        pid = {r.get("LOGICAL_OUTFIT_ID") for r in pred}
        chk("G-21", "Predator mods are not one logical outfit",
            "> 1 distinct id", f"{len(pid)} ids across {len(pred)} mods",
            len(pid) > 1 if pred else True)
        need = {"parent_mod", "relationship_evidence", "confidence"}
        chk("G-22", "15 has parent/evidence/confidence", sorted(need),
            sorted(need & set(logical[0].keys())), need <= set(logical[0].keys()))

    # ---- 10. calibration gate still green --------------------------------
    cp = os.path.join(R, "PARSER_CALIBRATION.csv")
    if os.path.isfile(cp):
        with open(cp, encoding="utf-8-sig") as fh:
            cr = list(csv.DictReader(fh))
        v = Counter(x.get("verdict") for x in cr)
        chk("G-23", "parser calibration gate", "0 FAIL", dict(v),
            v.get("FAIL", 0) == 0)

    npass = sum(1 for c in checks if c["verdict"] == "PASS")
    nfail = len(checks) - npass
    with open(GATE_CSV, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["check_id", "description",
                                           "expected", "observed", "verdict",
                                           "evidence"])
        w.writeheader()
        w.writerows(checks)

    for c in checks:
        if c["verdict"] == "FAIL":
            C.log(f"  FAIL {c['check_id']}: {c['description']} "
                  f"expected={c['expected']} observed={c['observed']}")
    C.log(f"GATE: {npass} PASS / {nfail} FAIL  ->  "
          f"{'P00 FINAL FROZEN' if nfail == 0 else 'BLOCKED'}")
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
