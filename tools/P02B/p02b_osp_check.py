# -*- coding: utf-8 -*-
"""Static BodySlide wiring check for the staged CL06 OSP.

Resolves every reference BodySlide would resolve at load time:
  DataFolder + SourceFile  -> the ShapeData NIF
  DataFolder + *.osd       -> the OSD file
  OutputPath + OutputFile  -> the build target
and reports anything missing. This is the automatable part of the OSP load test.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "P02A"))
import p02a_common as C

STAGING = os.path.join(C.ROOT, "staging", "ZLJ Combat Latex Pack - P02B Pilot")
OSP = os.path.join(STAGING, "CalienteTools", "BodySlide", "SliderSets", "ZLJ_CL06_ToxicCat.osp")
SD_ROOT = os.path.join(STAGING, "CalienteTools", "BodySlide", "ShapeData")
MODS = r"E:\SkyrimAE\mo2\mods"


def norm(p):
    return p.replace("/", "\\").strip("\\").lower()


def main():
    text = open(OSP, encoding="utf-8-sig").read()
    blocks = re.findall(r"<SliderSet name=\"([^\"]+)\">(.*?)</SliderSet>", text, re.S)
    print("slider sets found:", len(blocks))
    problems = []
    for name, body in blocks:
        df = re.search(r"<DataFolder>([^<]*)</DataFolder>", body)
        mv = re.search(r"<SourceFile>([^<]*)</SourceFile>", body)
        op = re.search(r"<OutputPath>([^<]*)</OutputPath>", body)
        of = re.search(r"<OutputFile[^>]*>([^<]*)</OutputFile>", body)
        datafolder = df.group(1) if df else ""
        srcfile = mv.group(1) if mv else ""
        outpath = op.group(1) if op else ""
        outfile = of.group(1) if of else ""
        sliders = len(re.findall(r"<Slider ", body))
        shapes = len(re.findall(r"<Shape ", body))
        nif = os.path.join(SD_ROOT, datafolder.replace("\\", os.sep), srcfile)
        osds = sorted({m.split("\\")[0] for m in re.findall(r"<Data [^>]*>([^<]*)</Data>", body)})
        osd_paths = [os.path.join(SD_ROOT, datafolder.replace("\\", os.sep), o) for o in osds]
        ok_nif = os.path.isfile(nif)
        miss_osd = [p for p in osd_paths if not os.path.isfile(p)]
        # An OSD reference that is not in the DataFolder is normally a GLOBAL BodySlide
        # resource shipped by a body mod (e.g. CBBE). RULING-03 keeps those external.
        external_osd, real_missing = [], []
        for p in miss_osd:
            base = os.path.basename(p).lower().replace(" ", "")
            found = None
            for mod in os.listdir(MODS):
                root = os.path.join(MODS, mod)
                if not os.path.isdir(root):
                    continue
                for dp, _d, ns in os.walk(root):
                    for n in ns:
                        if n.replace(" ", "").lower() == base:
                            found = os.path.join(mod, os.path.relpath(os.path.join(dp, n), root))
                            break
                    if found:
                        break
                if found:
                    break
            (external_osd if found else real_missing).append((p, found))
        print()
        print("  set: %s" % name)
        print("     DataFolder   %s" % datafolder)
        print("     SourceFile   %-24s -> %s  %s" % (srcfile, "FOUND" if ok_nif else "MISSING", nif))
        print("     OutputPath   %s  + OutputFile %s" % (outpath, outfile))
        status = "all local" if not miss_osd else (
            "external global x%d" % len(external_osd) if not real_missing else "REAL MISSING x%d" % len(real_missing))
        print("     sliders=%-4d shapes=%-3d OSD refs=%d (%s)"
              % (sliders, shapes, len(osd_paths), status))
        for p, prov in external_osd:
            print("        GLOBAL_BODYSLIDE_RESOURCE: %s  <- %s  (kept external, never vendored)"
                  % (os.path.basename(p), prov))
        if not ok_nif:
            problems.append(("MISSING_INPUT_NIF", name, nif))
        for p, _ in real_missing:
            problems.append(("MISSING_OSD", name, p))
        if "ZLJ" not in outpath:
            problems.append(("OUTPUT_NOT_IN_NAMESPACE", name, outpath))
    print()
    print("PROBLEMS:", len(problems))
    for p in problems:
        print("   ", p)
    print()
    total_sliders = len(re.findall(r"<Slider ", text))
    print("total sliders in OSP:", total_sliders)
    print("LOAD_TEST_STATIC =", "PASS" if not problems else "FAIL")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
