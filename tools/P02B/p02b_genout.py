# -*- coding: utf-8 -*-
"""P02B2 CL06 generated-output validation.

Reads the BodySlide build output (read-only) and validates every generated NIF
with PyNifly. Writes:
  reports/P02B/P02B_CL06_GENERATED_OUTPUT_MANIFEST.csv
  reports/P02B/P02B_CL06_GENERATED_CHAIN.csv
"""
import csv
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "P02A"))
sys.path.insert(0, HERE)
sys.path.insert(0, r"E:\SkyrimAE\Tools\pynifly")
import p02a_common as C

OUTFIT = "CL06_ToxicCat"
STAGING = os.path.join(C.ROOT, "staging", "ZLJ Combat Latex Pack - P02B Pilot")
REPORTS = os.path.join(C.ROOT, "reports", "P02B")
OSP = os.path.join(STAGING, "CalienteTools", "BodySlide", "SliderSets", "ZLJ_CL06_ToxicCat.osp")
OUT_ROOT = r"E:\SkyrimAE\mo2\mods\输出·BodySlide Output"
TEX_NS = "textures\\zlj\\combatlatex\\cl06_toxiccat\\"
BODY_SKIN = "textures\\actors\\character\\female\\"
ALLOWED_OTHER = ("textures\\actors\\character\\",)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def sets_from_osp():
    t = open(OSP, encoding="utf-8-sig").read()
    out = []
    for name, body in re.findall(r'<SliderSet name="([^"]+)">(.*?)</SliderSet>', t, re.S):
        op = re.search(r"<OutputPath>([^<]*)</OutputPath>", body)
        of = re.search(r"<OutputFile[^>]*>([^<]*)</OutputFile>", body)
        sf = re.search(r"<SourceFile>([^<]*)</SourceFile>", body)
        df = re.search(r"<DataFolder>([^<]*)</DataFolder>", body)
        gw = re.search(r'GenWeights="([^"]*)"', of.group(0)) if of else None
        out.append(dict(ui=name,
                        output_path=op.group(1) if op else "",
                        output_file=of.group(1) if of else "",
                        source_file=sf.group(1) if sf else "",
                        data_folder=df.group(1) if df else "",
                        gen_weights=(gw.group(1) if gw else "absent"),
                        sliders=len(re.findall(r"<Slider ", body))))
    return out


def inspect(nif_path):
    from pyn.pynifly import NifFile
    nif = NifFile(nif_path)
    shapes, tex, parts, skinned = [], [], 0, 0
    for s in nif.shapes:
        shapes.append(s.name)
        try:
            if s.partitions:
                parts += len(s.partitions)
        except Exception:
            pass
        try:
            if s.skin:
                skinned += 1
        except Exception:
            pass
        try:
            for slot, v in (s.textures or {}).items():
                if isinstance(v, str) and v.strip():
                    tex.append((s.name, slot, v.strip()))
        except Exception:
            pass
    return dict(shapes=shapes, n_shapes=len(shapes), n_skinned=skinned,
                partitions=parts, textures=tex, parse_ok=True)


def main():
    rows, chain, problems = [], [], []
    for s in sets_from_osp():
        ui, op, of = s["ui"], s["output_path"].replace("/", "\\"), s["output_file"]
        base = op.rstrip("\\")
        for suffix in ("_0", "_1"):
            rel = base + "\\" + of + suffix + ".nif"
            p = os.path.join(OUT_ROOT, rel.replace("\\", os.sep))
            exists = os.path.isfile(p)
            size = os.path.getsize(p) if exists else 0
            sha = sha256(p) if exists else ""
            info = None
            if exists:
                try:
                    info = inspect(p)
                except Exception as ex:
                    problems.append(("NIF_PARSE_FAIL", rel, str(ex)[:60]))
            rows.append([OUTFIT, ui, op, of, of + suffix + ".nif", suffix,
                         "YES" if exists else "NO", size, sha,
                         info["n_shapes"] if info else "",
                         info["n_skinned"] if info else "",
                         info["partitions"] if info else "",
                         s["gen_weights"], s["sliders"]])
            if exists and info:
                bad = []
                for shp, slot, v in info["textures"]:
                    low = v.lower()
                    if low.startswith(TEX_NS):
                        continue
                    if low.startswith(ALLOWED_OTHER):
                        continue
                    bad.append((shp, slot, v))
                if bad:
                    problems.append(("UNEXPECTED_TEXTURE", rel, bad[:2]))
                if info["n_shapes"] == 0:
                    problems.append(("NO_SHAPES", rel, ""))
                # chain row per set
        chain.append([OUTFIT, ui, s["data_folder"], s["source_file"],
                      "CalienteTools\\BodySlide\\SliderSets\\ZLJ_CL06_ToxicCat.osp",
                      base + "\\" + of + "_0.nif",
                      base + "\\" + of + "_1.nif",
                      "PRESENT" if os.path.isfile(os.path.join(OUT_ROOT, (base + "\\" + of + "_0.nif").replace("\\", os.sep))) else "ABSENT",
                      "BUILD_OUTPUT" if os.path.isfile(os.path.join(OUT_ROOT, (base + "\\" + of + "_0.nif").replace("\\", os.sep))) else "MISSING",
                      "PRESENT_IN_PILOT_MOD" if os.path.isfile(os.path.join(STAGING, (base + "\\" + of + "_1.nif").replace("\\", os.sep))) else "MISSING",
                      "CLOSED" if os.path.isfile(os.path.join(OUT_ROOT, (base + "\\" + of + "_0.nif").replace("\\", os.sep))) else "OPEN"])
    C.write_csv(os.path.join(REPORTS, "P02B_CL06_GENERATED_OUTPUT_MANIFEST.csv"),
                ["outfit_id", "slider_set", "output_path", "output_file", "generated_file", "suffix",
                 "file_exists", "file_size", "sha256", "n_shapes", "n_skinned_shapes",
                 "n_partitions", "osp_gen_weights", "osp_sliders"], rows)
    C.write_csv(os.path.join(REPORTS, "P02B_CL06_GENERATED_CHAIN.csv"),
                ["outfit_id", "slider_set", "shapedata_folder", "source_file", "osp",
                 "generated_0", "generated_1", "generated_0_state", "generated_0_kind",
                 "runtime_1_state", "chain_state"], chain)
    print("%-46s %-8s %-9s %s" % ("slider set", "suffix", "exists", "shapes/skinned/parts"))
    for r in rows:
        print("%-46s %-8s %-9s %s/%s/%s" % (r[1][:46], r[5], r[6], r[9], r[10], r[11]))
    print()
    print("problems:", len(problems))
    for p in problems:
        print("   ", p)
    n0 = sum(1 for r in rows if r[5] == "_0" and r[6] == "YES")
    n1 = sum(1 for r in rows if r[5] == "_1" and r[6] == "YES")
    print()
    print("generated _0 for %d/5 sets; generated _1 for %d/5 sets" % (n0, n1))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
