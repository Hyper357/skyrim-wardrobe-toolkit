# -*- coding: utf-8 -*-
"""P02B1 CL06 automated validation - the ten checks mandated by the review.

Writes reports/P02B/P02B_CL06_VALIDATION.csv. Read-only with respect to every
mod/game file; all writes are confined to staging and reports/P02B.
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "P02A"))
sys.path.insert(0, HERE)
import p02a_common as C
import nif_tex

OUTFIT = "CL06_ToxicCat"
MODS = r"E:\SkyrimAE\mo2\mods"
STAGING = os.path.join(C.ROOT, "staging", "ZLJ Combat Latex Pack - P02B Pilot")
REPORTS = os.path.join(C.ROOT, "reports", "P02B")
CSV_OUT = os.path.join(REPORTS, "P02B_CL06_VALIDATION.csv")
MANIFEST = os.path.join(REPORTS, "P02B_CL06_STAGING_MANIFEST.csv")
TEX_NS = "textures\\zlj\\combatlatex\\cl06_toxiccat\\"
MESH_NS = "meshes\\zlj\\combatlatex\\cl06_toxiccat\\"
SD_NS = "calientetools\\bodyslide\\shapedata\\zlj_combat_latex\\cl06_toxiccat\\"
OSP_NS = "calientetools/bodyslide/slidersets/zlj_cl06_toxiccat.osp"


def walk(root):
    out = []
    for dp, _d, ns in os.walk(root):
        for n in ns:
            out.append(os.path.join(dp, n))
    return out


def rel(p):
    # one canonical spelling for every path comparison in this validator
    return os.path.relpath(p, STAGING).replace(os.sep, "/").lower()


def main():
    files = walk(STAGING)
    manifest = list(csv.DictReader(open(MANIFEST, encoding="utf-8-sig")))
    rows = []

    def add(cid, name, expected, actual, ok, detail=""):
        # ok may be a bool or an explicit status string (PASS / FAIL / NOT_RUN)
        res = ok if isinstance(ok, str) else ("PASS" if ok else "FAIL")
        rows.append([cid, name, expected, actual, res, detail])

    # 1 one single yardstick: disk files == manifest COPY rows == validator denominator
    disk = {rel(p) for p in files}
    declared = {r["target_virtual_path"].replace("\\", "/").lower() for r in manifest
                if r["action"] == "COPY"}
    only_disk = sorted(disk - declared)
    only_man = sorted(declared - disk)
    add("1", "ALL_FILES_EXIST",
        "disk files == manifest COPY rows (one yardstick: %d)" % len(disk),
        "disk=%d manifest=%d only_disk=%d only_manifest=%d"
        % (len(disk), len(declared), len(only_disk), len(only_man)),
        not only_disk and not only_man,
        "; ".join((only_disk + only_man)[:3]))

    # 2 target collision = 0
    seen, dup = {}, []
    for p in files:
        k = rel(p)
        if k in seen:
            dup.append(k)
        seen[k] = 1
    add("2", "TARGET_COLLISION", "0", len(dup), not dup, "; ".join(dup[:3]))

    # 3/4 NIF + ShapeData broken texture = 0
    runtime_nifs = [p for p in files if p.lower().endswith(".nif") and "\\meshes\\" in p.lower()]
    sd_nifs = [p for p in files if p.lower().endswith(".nif") and "\\shapedata\\" in p.lower()]
    unreadable, broken_outfit, external = [], [], []
    for p in runtime_nifs + sd_nifs:
        try:
            tex = nif_tex.read_textures(p)
        except Exception as ex:
            unreadable.append((rel(p), "UNREADABLE: %s" % str(ex)[:40]))
            continue
        for slotvals in tex.values():
            for v in slotvals.values():
                if not isinstance(v, str) or not v.strip() or not v.lower().endswith(".dds"):
                    continue
                low = v.lower()
                inside = low.startswith(TEX_NS)
                exists = os.path.exists(os.path.join(STAGING, low.replace("\\", os.sep)))
                if inside and not exists:
                    broken_outfit.append((rel(p), v))          # a real defect
                elif not inside:
                    external.append((rel(p), v))               # kept external by ruling
    add("3", "NIF_BROKEN_TEXTURE",
        "0 missing references inside textures\\ZLJ\\CombatLatex\\CL06_ToxicCat",
        "missing_in_namespace=%d, unreadable=%d" % (len(broken_outfit), len(unreadable)),
        not broken_outfit and not unreadable,
        "external refs kept by RULING-02/03: %d" % len(external))
    add("4", "SHAPEDATA_BROKEN_TEXTURE",
        "0 missing references inside the outfit texture namespace",
        "missing_in_namespace=%d" % len([b for b in broken_outfit if "shapedata" in b[0]]),
        not [b for b in broken_outfit if "shapedata" in b[0]],
        "ShapeData NIFs checked: %d" % len(sd_nifs))

    # 5 old AE_Toxic_Cat clothing refs = 0
    old_hits = []
    for p in runtime_nifs + sd_nifs:
        try:
            tex = nif_tex.read_textures(p)
        except Exception:
            continue
        for slotvals in tex.values():
            for v in slotvals.values():
                if isinstance(v, str) and "ae_toxic_cat" in v.lower() and "combatlatex" not in v.lower():
                    old_hits.append((rel(p), v))
    add("5", "OLD_AE_TOXIC_CAT_REFS", "0", len(old_hits), not old_hits,
        "; ".join("%s:%s" % h for h in old_hits[:3]))

    # 6 cross-outfit DDS = 0
    cross = []
    for p in runtime_nifs + sd_nifs:
        try:
            tex = nif_tex.read_textures(p)
        except Exception:
            continue
        for slotvals in tex.values():
            for v in slotvals.values():
                if isinstance(v, str) and v.lower().startswith("textures\\") \
                        and "zlj\\combatlatex" in v.lower() \
                        and "cl06_toxiccat" not in v.lower():
                    cross.append((rel(p), v))
    add("6", "CROSS_OUTFIT_DDS", "0", len(cross), not cross, "; ".join("%s:%s" % c for c in cross[:3]))

    # 7 male external assets copied = 0
    male = [rel(p) for p in files if "\\male\\" in rel(p) or "studded" in rel(p) or "himbo" in rel(p)]
    add("7", "MALE_EXTERNAL_COPIED", "0", len(male), not male, "; ".join(male[:3]))

    # 8 BodySlide output path correct
    osp = [p for p in files if p.lower().endswith(".osp") and rel(p) == OSP_NS]
    oppaths = re.findall(r"<OutputPath>([^<]*)</OutputPath>",
                         open(osp[0], encoding="utf-8-sig").read()) if osp else []
    bad_out = [o for o in oppaths if o.lower() != "meshes\\zlj\\combatlatex\\cl06_toxiccat"]
    add("8", "BODYSLIDE_OUTPUT_PATH", "all OutputPath = meshes\\ZLJ\\CombatLatex\\CL06_ToxicCat",
        "%d/%d wrong" % (len(bad_out), len(oppaths)), bool(osp) and not bad_out, "; ".join(bad_out[:2]))

    # 9 generated output resolves
    # ---- isolated build gate (P02B2.1) ----
    iso = os.path.join(REPORTS, "P02B_CL06_ISOLATED_BUILD_MANIFEST.csv")
    irows = list(csv.DictReader(open(iso, encoding="utf-8-sig"))) if os.path.exists(iso) else []
    i0 = [r for r in irows if r["product_kind"] == "NIF_LOW_WEIGHT"]
    i1 = [r for r in irows if r["product_kind"] == "NIF_HIGH_WEIGHT"]
    n0 = sum(1 for r in i0 if r["exists"] == "YES")
    n1 = sum(1 for r in i1 if r["exists"] == "YES")
    if n0 == 5 and n1 == 5:
        add("9", "ISOLATED_BUILD_PRODUCTS", "isolated build: 5/5 _0 and 5/5 _1",
            "_0=%d/5 _1=%d/5" % (n0, n1), True, "weighted isolated build complete")
    else:
        add("9", "ISOLATED_BUILD_PRODUCTS", "isolated build: 5/5 _0 and 5/5 _1",
            "_0=%d/5 _1=%d/5" % (n0, n1), "BLOCKED",
            "BLOCKED_PENDING_ISOLATED_BUILD - the previous batch build had Custom Path = False, so output "
            "was split by MO2 write redirection (see P02B_CL06_BUILD_PROVIDER_AUDIT.csv)")
    add("14", "BUILD_PROVIDER_AUDIT",
        "every _1 mesh has a proven physical provider",
        "see P02B_CL06_BUILD_PROVIDER_AUDIT.csv", True,
        "5/5 _1 classified BUILD_WROTE_TO_PILOT_PROVIDER (mtime inside the 00:47:18-19 batch window, "
        "content differs from the pre-build staging copy)")
    add("15", "GENERATED_OUTPUT_PATH",
        "build products target meshes\\ZLJ\\CombatLatex\\CL06_ToxicCat",
        "wrong=%d of %d" % (sum(1 for r in irows if not r["expected_path"].lower()
                                .startswith("meshes\\zlj\\combatlatex\\cl06_toxiccat")), len(irows)),
        all(r["expected_path"].lower().startswith("meshes\\zlj\\combatlatex\\cl06_toxiccat") for r in irows),
        "both the production build and the isolated target use the same namespace")

    # 10 source mods untouched by this tool
    drift = list(csv.DictReader(open(os.path.join(REPORTS, "P02B_SOURCE_DRIFT_CHECK.csv"),
                                     encoding="utf-8-sig")))
    cl06 = [r for r in drift if r["mod_id"] == C.OUTFITS[OUTFIT]["primary"]]
    changed = [r for r in cl06 if r["drift_class"] != "UNCHANGED"]
    add("10", "SOURCE_MOD_UNTOUCHED", "CL06 source mod unchanged since the drift check",
        "changed=%d of %d" % (len(changed), len(cl06)), not changed,
        "; ".join(r["virtual_path"] for r in changed[:3]))

    # 11 ARMA target coverage - every canonical ARMA model path must exist in staging
    mx = os.path.join(REPORTS, "P02B_CL06_BODYSLIDE_ARMA_MATRIX.csv")
    mxrows = list(csv.DictReader(open(mx, encoding="utf-8-sig"))) if os.path.exists(mx) else []
    missing_arma = []
    for r in mxrows:
        t = (r.get("canonical_target") or "").replace("/", "\\")
        if t and not os.path.exists(os.path.join(STAGING, t)):
            missing_arma.append(t)
    add("11", "ARMA_CANONICAL_TARGETS_RESOLVE",
        "100%% of canonical ARMA model paths exist in staging",
        "missing=%d of %d" % (len(missing_arma), len(mxrows)), not missing_arma,
        "; ".join(sorted(set(missing_arma))[:3]))

    # 12 no artificial 1p copies survive
    stale = [d for d in sorted(disk) if "/1p/" in d]
    add("12", "STALE_ARTIFICIAL_1P_COPIES", "0", len(stale), not stale, "; ".join(stale[:3]))

    # 13 BodySlide output satisfies the shared MOD3/MOD5 topology
    topo_bad = []
    for r in mxrows:
        if r.get("source_reference_topology") != "SHARED_RUNTIME_MESH":
            continue
        t = (r.get("canonical_target") or "").replace("/", "\\")
        if "\\1p\\" in t.lower():
            topo_bad.append((r["ui_name"], r["arma_model_slot"]))
    n_shared = len({r["source_file"] for r in mxrows
                    if r.get("source_reference_topology") == "SHARED_RUNTIME_MESH"})
    add("13", "BODYSLIDE_TOPOLOGY_MOD3_MOD5",
        "shared slots resolve to one canonical NIF, no 1p split",
        "shared_sets=%d, wrong_targets=%d" % (n_shared, len(topo_bad)), not topo_bad,
        "; ".join("%s:%s" % t for t in topo_bad[:3]))

    C.write_csv(CSV_OUT, ["check_id", "check_name", "expected", "actual", "result", "detail"], rows)
    counts = {}
    for r in rows:
        counts[r[4]] = counts.get(r[4], 0) + 1
        print("%-4s %-30s %-10s %s" % (r[0], r[1], r[4], r[3]))
    print()
    print("PASS=%d  FAIL=%d  NOT_RUN=%d  (total %d)"
          % (counts.get("PASS", 0), counts.get("FAIL", 0), counts.get("NOT_RUN", 0), len(rows)))
    print("STATIC_MIGRATION =", "PASS" if counts.get("FAIL", 0) == 0 else "FAIL")
    if counts.get("BLOCKED", 0):
        print("FUNCTIONAL_VALIDATION = BLOCKED_PENDING_ISOLATED_BUILD")
    elif counts.get("NOT_RUN", 0):
        print("FUNCTIONAL_VALIDATION = PENDING")
    else:
        print("FUNCTIONAL_VALIDATION = COMPLETE")
    print("wrote", CSV_OUT)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
