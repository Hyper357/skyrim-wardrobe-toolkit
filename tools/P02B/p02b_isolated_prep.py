# -*- coding: utf-8 -*-
"""Prepare the isolated build target and its expected-product manifest."""
import csv, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "P02A"))
import p02a_common as C

OUTFIT = "CL06_ToxicCat"
ISO = os.path.join(C.ROOT, "staging", "ZLJ Combat Latex Pack - CL06 Isolated Build")
REPORTS = os.path.join(C.ROOT, "reports", "P02B")
OSP = os.path.join(C.ROOT, "staging", "ZLJ Combat Latex Pack - P02B Pilot",
                   "CalienteTools", "BodySlide", "SliderSets", "ZLJ_CL06_ToxicCat.osp")

os.makedirs(ISO, exist_ok=True)
t = open(OSP, encoding="utf-8-sig").read()
rows = []
for name, body in re.findall(r'<SliderSet name="([^"]+)">(.*?)</SliderSet>', t, re.S):
    op = re.search(r"<OutputPath>([^<]*)</OutputPath>", body).group(1).replace("/", "\\").rstrip("\\")
    of = re.search(r"<OutputFile[^>]*>([^<]*)</OutputFile>", body).group(1)
    for suffix, kind in (("_0", "NIF_LOW_WEIGHT"), ("_1", "NIF_HIGH_WEIGHT")):
        rel = op + "\\" + of + suffix + ".nif"
        p = os.path.join(ISO, rel.replace("\\", os.sep))
        rows.append([OUTFIT, name, kind, rel, "YES" if os.path.isfile(p) else "NO",
                     os.path.getsize(p) if os.path.isfile(p) else 0, "NOT_BUILT",
                     "expected product of the isolated build"])
    rel = op + "\\" + of + ".tri"
    p = os.path.join(ISO, rel.replace("\\", os.sep))
    rows.append([OUTFIT, name, "TRI_MORPH", rel, "YES" if os.path.isfile(p) else "NO",
                 os.path.getsize(p) if os.path.isfile(p) else 0, "NOT_BUILT",
                 "expected product of the isolated build"])
C.write_csv(os.path.join(REPORTS, "P02B_CL06_ISOLATED_BUILD_MANIFEST.csv"),
            ["outfit_id", "slider_set", "product_kind", "expected_path", "exists", "size", "state", "note"], rows)
print("isolated root :", ISO)
print("expected products:", len(rows), "(5 sets x (_0, _1, .tri) = 15 core + ...)")
print("present now      :", sum(1 for r in rows if r[4] == "YES"))
print()
for r in rows[:6]:
    print("   %-46s %-16s %s" % (r[1][:46], r[2], r[3]))
print("   ...")
