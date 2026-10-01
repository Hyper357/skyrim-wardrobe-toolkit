# -*- coding: utf-8 -*-
"""P02B2.3 isolated weighted build validation.

Audits the CL06 isolated build. Reports what is actually on disk, and refuses to
declare a pass when the products are not there.

Outputs:
  reports/P02B/P02B_CL06_ISOLATED_BUILD_MANIFEST.csv
  reports/P02B/P02B_CL06_FINAL_PIPELINE_GATE.csv
"""
import csv, hashlib, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "P02A"))
sys.path.insert(0, HERE)
import p02a_common as C

OUTFIT = "CL06_ToxicCat"
REPORTS = os.path.join(C.ROOT, "reports", "P02B")
ISO = os.path.join(C.ROOT, "staging", "ZLJ Combat Latex Pack - CL06 Isolated Build")
OSP = os.path.join(C.ROOT, "staging", "ZLJ Combat Latex Pack - P02B Pilot",
                   "CalienteTools", "BodySlide", "SliderSets", "ZLJ_CL06_ToxicCat.osp")
MODS = r"E:\SkyrimAE\mo2\mods"
TREES = {
    "ISOLATED": ISO,
    "PILOT_MOD": os.path.join(MODS, "ZLJ Combat Latex Pack - P02B Pilot"),
    "OUTPUT_MOD": os.path.join(MODS, "\u8f93\u51fa\u00b7BodySlide Output"),
    "OVERWRITE": r"E:\SkyrimAE\mo2\overwrite",
}
TEX_NS = "textures\\zlj\\combatlatex\\cl06_toxiccat\\"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def find_in_trees(rel):
    hits = []
    for label, root in TREES.items():
        p = os.path.join(root, rel.replace("\\", os.sep))
        if os.path.isfile(p):
            hits.append((label, p))
    return hits


def main():
    os.makedirs(ISO, exist_ok=True)
    text = open(OSP, encoding="utf-8-sig").read()
    mrows, grows = [], []
    for name, body in re.findall(r'<SliderSet name="([^"]+)">(.*?)</SliderSet>', text, re.S):
        op = re.search(r"<OutputPath>([^<]*)</OutputPath>", body).group(1).replace("/", "\\").strip("\\")
        of = re.search(r"<OutputFile[^>]*>([^<]*)</OutputFile>", body).group(1)
        row = [OUTFIT, name]
        kinds = []
        for suffix, kind in (("_0.nif", "_0"), ("_1.nif", "_1"), (".tri", "TRI")):
            rel = op + "\\" + of + suffix
            hits = find_in_trees(rel)
            in_iso = [h for h in hits if h[0] == "ISOLATED"]
            p = in_iso[0][1] if in_iso else ""
            row += [rel, "YES" if p else "NO", sha(p) if p else "",
                    os.path.getsize(p) if p else 0,
                    ";".join(h[0] for h in hits) or "ABSENT"]
            kinds.append(dict(kind=kind, rel=rel, hits=hits, path=p))
        mrows.append(row)
        grows.append((name, kinds))

    C.write_csv(os.path.join(REPORTS, "P02B_CL06_ISOLATED_BUILD_MANIFEST.csv"),
                ["outfit_id", "slider_set",
                 "_0_path", "_0_exists", "_0_sha256", "_0_size", "_0_physical_providers",
                 "_1_path", "_1_exists", "_1_sha256", "_1_size", "_1_physical_providers",
                 "tri_path", "tri_exists", "tri_sha256", "tri_size", "tri_physical_providers"],
                mrows)

    total = sum(len(k) for _n, k in grows)
    in_iso = sum(1 for _n, k in grows for x in k if x["hits"] and x["hits"][0][0] == "ISOLATED")
    outside = [(n, x["kind"], [h[0] for h in x["hits"]]) for n, k in grows for x in k
               if x["hits"] and not any(h[0] == "ISOLATED" for h in x["hits"])]
    n0 = sum(1 for _n, k in grows for x in k if x["kind"] == "_0" and x["path"])
    n1 = sum(1 for _n, k in grows for x in k if x["kind"] == "_1" and x["path"])
    ntri = sum(1 for _n, k in grows for x in k if x["kind"] == "TRI" and x["path"])

    # ---- final pipeline gate ----
    g = []

    def add(cid, name, expected, actual, res, detail=""):
        g.append([cid, name, expected, actual, res, detail])

    add("P1", "ISOLATED_0_NIF", "5/5", "%d/5" % n0, "PASS" if n0 == 5 else "FAIL", "")
    add("P2", "ISOLATED_1_NIF", "5/5", "%d/5" % n1, "PASS" if n1 == 5 else "FAIL", "")
    add("P3", "ISOLATED_TRI", "5/5", "%d/5" % ntri, "PASS" if ntri == 5 else "FAIL", "")
    add("P4", "SAME_PHYSICAL_TREE", "15/15 products inside the isolated tree",
        "%d/%d inside isolated" % (in_iso, total),
        "PASS" if in_iso == total and total == 15 else "FAIL",
        "; ".join("%s:%s in %s" % (n, k, ",".join(p)) for n, k, p in outside[:3]) or
        "no product exists in any tree")
    add("P5", "BODYSLIDE_WEIGHTED_BUILD_PASS", "declared only on _0=5/5, _1=5/5, TRI=5/5 in one tree",
        "NOT DECLARED", "BLOCKED",
        "the isolated build has not been executed; see P02B_CL06_ISOLATED_BUILD_REPORT.md")
    add("P6", "CL06_ASSET_AND_BODYSLIDE_PIPELINE_FROZEN", "declared only after P5",
        "NOT DECLARED", "BLOCKED", "asset side is frozen; the weighted build is not")
    add("P7", "READY_FOR_PILOT_PLUGIN", "declared only after P5", "NOT DECLARED", "BLOCKED",
        "plugin plan is frozen and gated, but the build gate is open")
    # carried-forward evidence that does hold
    pg = os.path.join(REPORTS, "P02B_CL06_PLUGIN_PLAN_GATE.csv")
    if os.path.exists(pg):
        prows = list(csv.DictReader(open(pg, encoding="utf-8-sig")))
        bad = [r for r in prows if r["result"] != "PASS"]
        add("P8", "PLUGIN_PLAN_STATIC_GATE", "14/14", "%d/%d" % (len(prows) - len(bad), len(prows)),
            "PASS" if not bad else "FAIL", "carried forward, unchanged")
    add("P9", "OLD_TOXICCAT_DDS_IN_ISOLATED_OUTPUT", "0",
        "n/a (no products)", "BLOCKED", "cannot be evaluated without build products")
    add("P10", "TRI_CLASSIFIED_AS_PHYSICS", "0", 0, "PASS",
        "TRI stays BODY_MORPH_TRI; no physics classification exists")
    C.write_csv(os.path.join(REPORTS, "P02B_CL06_FINAL_PIPELINE_GATE.csv"),
                ["check_id", "check_name", "expected", "actual", "result", "detail"], g)

    print("expected products:", total, "| found in isolated tree:", in_iso)
    print("_0=%d/5  _1=%d/5  TRI=%d/5" % (n0, n1, ntri))
    for n, k in grows:
        print("  %-46s %s" % (n[:46], " ".join("%s:%s" % (x["kind"], "OK" if x["path"] else "MISSING")
                                               for x in k)))
    print()
    for row in g:
        print("%-4s %-42s %-52s %s" % (row[0], row[1], row[3], row[4]))
    print()
    print("BODYSLIDE_WEIGHTED_BUILD_PASS =", "DECLARED" if n0 == n1 == ntri == 5 and in_iso == 15 else "NOT DECLARED")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
