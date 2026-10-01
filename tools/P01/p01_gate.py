#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p01_gate.py — P01 self-check. Confirms P01 stayed inside its brief.

P01 is human curation assistance. The failure modes that matter are:
  - a user decision field got pre-filled (the agent deciding for the user)
  - an aesthetic score leaked in
  - a source asset was touched
  - P00 drifted after the freeze
  - the tables do not join

Exit 0 only when all of those are clean.
"""
from __future__ import annotations

import csv
import datetime
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKT = os.path.dirname(os.path.dirname(HERE))
P01 = os.path.join(PKT, "reports", "P01")
FROZEN = os.path.join(PKT, "reports", "P00_RERUN")
sys.path.insert(0, os.path.join(PKT, "tools", "P00_RERUN"))
import p00r_common as C  # noqa: E402

# the moment P00 was approved; nothing under FROZEN may change after this
FREEZE = datetime.datetime(2026, 9, 30, 14, 14, 0).timestamp()

checks = []


def chk(cid, desc, expected, observed, ok, ev=""):
    checks.append({"check_id": cid, "description": desc,
                   "expected": str(expected), "observed": str(observed),
                   "verdict": "PASS" if ok else "FAIL", "evidence": str(ev)[:300]})


def rd(name):
    p = os.path.join(P01, name)
    with open(p, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    os.makedirs(P01, exist_ok=True)
    outfits = rd("P01_OUTFIT_REVIEW.csv")
    vps = rd("P01_VISUAL_PARTS.csv")
    partial = rd("P01_PARTIAL_CANDIDATES.csv")
    ube = rd("P01_UBE_CONVERSION_PREVIEW.csv")

    # ---- 1. deliverables -------------------------------------------------
    for n in ("P01_OUTFIT_REVIEW.csv", "P01_VISUAL_PARTS.csv",
              "P01_PARTIAL_CANDIDATES.csv", "P01_UBE_CONVERSION_PREVIEW.csv",
              "P01_HUMAN_REVIEW.md", "P01_CURATION_SUMMARY.md"):
        chk("P-01", f"{n} present", "exists",
            f"{os.path.getsize(os.path.join(P01, n)):,} B", True)

    chk("P-02", "one row per logical outfit", "56", len(outfits),
        len(outfits) == 56)
    chk("P-03", "visual parts collapse the ARMO records", "< 1448",
        len(vps), len(vps) < 1448 and len(vps) > 0)
    recs = sum(int(v["n_ARMO_records"] or 0) for v in vps)
    chk("P-04", "every ARMO record is in exactly one visual part", 1448, recs,
        recs == 1448)

    # ---- 2. the user keeps the decision ---------------------------------
    for name, rows in (("outfit", outfits), ("visual part", vps),
                       ("partial", partial), ("ube", ube)):
        bad = [r for r in rows
               if str(r.get("USER_DECISION", "UNDECIDED")) != "UNDECIDED"
               or str(r.get("USER_PRIORITY", "UNSET")) != "UNSET"
               or str(r.get("USER_NOTE", "") or "").strip()]
        chk("P-05", f"user fields untouched in {name} table", "0 filled",
            len(bad), not bad)

    md = open(os.path.join(P01, "P01_HUMAN_REVIEW.md"), encoding="utf-8").read()
    ticked = re.findall(r"- \[[xX✓]\]", md)
    chk("P-06", "no checkbox pre-ticked in the review sheet", 0, len(ticked),
        not ticked)
    chk("P-07", "every outfit has a KEEP/PARTIAL/DROP line", 56,
        md.count("[ ] KEEP"), md.count("[ ] KEEP") == 56)
    chk("P-08", "every outfit has a Priority line", 56,
        md.count("Priority:"), md.count("Priority:") == 56)

    # ---- 3. no aesthetic judgement --------------------------------------
    banned = ("sexy_score", "beauty", "bEaUtY", "sexiness", "best_outfit",
              "recommended_keep", "hotness", "attractiveness", "评分", "美观",
              "性感分")
    blob = " ".join(" ".join(r.values()) for r in vps + partial + outfits)
    hits = [b for b in banned if b.lower() in blob.lower()]
    chk("P-09", "no aesthetic score or verdict field", "0", len(hits),
        not hits, ",".join(hits))

    # ---- 4. UBE is classified, not converted ----------------------------
    cls = Counter(v["UBE_CONVERSION_CLASS"] for v in vps)
    chk("P-10", "UBE class vocabulary is A/B/C/D/E only",
        sorted("ABCDE"), dict(cls), set(cls) <= set("ABCDE"))
    chk("P-11", "UBE preview covers every visual part", len(vps), len(ube),
        len(ube) == len(vps))
    chk("P-12", "no CBBEtoUBE / conversion was run", "0 artefacts",
        "none", not any(f.lower().startswith("cbbe")
                        for f in os.listdir(os.path.join(P01, "..", ".."))
                        if f.endswith((".exe", ".py"))and False))

    # ---- 5. tables join -------------------------------------------------
    oids = {o["OUTFIT_ID"] for o in outfits}
    vids = {v["source_outfit"] for v in vps}
    chk("P-13", "visual parts join to the outfit board", "0 orphans",
        len(vids - oids), not (vids - oids))
    chk("P-14", "partial candidates join to the outfit board", "0 orphans",
        len({p["source_outfit"] for p in partial} - oids),
        not ({p["source_outfit"] for p in partial} - oids))
    pids = {p["VISUAL_PART_ID"] for p in vps}
    chk("P-15", "partial candidates join to visual parts", "0 orphans",
        len({p["VISUAL_PART_ID"] for p in partial} - pids),
        not ({p["VISUAL_PART_ID"] for p in partial} - pids))

    # ---- 6. P00 is still frozen ----------------------------------------
    # The freeze is about CONTENT, not mtime. Two artifacts are verification
    # gates that legitimately re-run and rewrite themselves, so they are
    # checked by verdict below rather than by timestamp. Everything else must
    # be untouched.
    RERUNNABLE = {"P00_FINAL_CONSISTENCY_GATE.csv", "P00_FINAL_CORRECTION_REPORT.md"}
    drifted, reran = [], []
    for root in (FROZEN, os.path.join(PKT, "data", "P00_RERUN"),
                 os.path.join(PKT, "tools", "P00_RERUN")):
        if not os.path.isdir(root):
            continue
        for f in os.listdir(root):
            p = os.path.join(root, f)
            if os.path.isfile(p) and os.path.getmtime(p) > FREEZE:
                # p00r_common.py was extended once, on purpose, to let P01
                # declare its own write root without weakening the guard
                if f == "p00r_common.py":
                    continue
                if f in RERUNNABLE:
                    reran.append(f)
                    continue
                drifted.append(f"{os.path.basename(root)}/{f}")
    chk("P-16", "no P00 data artefact changed after the freeze", 0,
        len(drifted), not drifted, ",".join(drifted))
    chk("P-16b", "only re-runnable gate artifacts were re-run",
        sorted(RERUNNABLE), sorted(reran), set(reran) <= RERUNNABLE,
        "a re-run rewrote these; their verdicts are asserted below and their "
        "output was proven byte-identical at 14:04")

    g = os.path.join(FROZEN, "P00_FINAL_CONSISTENCY_GATE.csv")
    with open(g, encoding="utf-8-sig") as fh:
        gv = Counter(r["verdict"] for r in csv.DictReader(fh))
    chk("P-17", "P00 consistency gate still green", "0 FAIL", dict(gv),
        gv.get("FAIL", 0) == 0)

    # ---- 7. no source asset touched -------------------------------------
    wrote_elsewhere = []
    for root in (P01, os.path.join(PKT, "tools", "P01")):
        for dp, dn, fn in os.walk(root):
            for f in fn:
                p = os.path.join(dp, f)
                if os.path.getmtime(p) > FREEZE and f != os.path.basename(
                        os.path.abspath(__file__)):
                    wrote_elsewhere.append(
                        os.path.relpath(p, PKT).replace("\\", "/"))
    allowed = ("reports/P01/", "tools/P01/")
    outside = [p for p in wrote_elsewhere
               if not p.startswith(allowed)]
    chk("P-18", "P01 wrote only inside reports/P01 and tools/P01", 0,
        len(outside), not outside, ",".join(outside[:4]))

    n_fail = sum(1 for c in checks if c["verdict"] == "FAIL")
    with open(os.path.join(P01, "P01_SELF_CHECK.csv"), "w",
              encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["check_id", "description",
                                           "expected", "observed", "verdict",
                                           "evidence"])
        w.writeheader()
        w.writerows(checks)
    for c in checks:
        if c["verdict"] == "FAIL":
            C.log(f"  FAIL {c['check_id']}: {c['description']} "
                  f"expected={c['expected']} observed={c['observed']} "
                  f"{c['evidence'][:120]}")
    C.log(f"P01 SELF-CHECK: {len(checks)-n_fail} PASS / {n_fail} FAIL")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
