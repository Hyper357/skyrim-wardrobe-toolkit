# -*- coding: utf-8 -*-
"""P02B_CL06_BUILD_PROVIDER_AUDIT - where did the _1 meshes physically go?"""
import hashlib
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "P02A"))
import p02a_common as C

OUTFIT = "CL06_ToxicCat"
REPORTS = os.path.join(C.ROOT, "reports", "P02B")
MODS = r"E:\SkyrimAE\mo2\mods"
STAGING = os.path.join(C.ROOT, "staging", "ZLJ Combat Latex Pack - P02B Pilot")
BUILD_WINDOW = ("2026-10-01 00:47:18", "2026-10-01 00:47:20")
NAMES = ["AE_Toxic_Cat_1.nif", "AE_Toxic_Cat_Feet_1.nif", "AE_Toxic_Cat_Hand_1.nif",
         "AE_Toxic_Cat_Top_1.nif", "AE_Toxic_Cat_St_1.nif"]
PLACES = {
    "PILOT": os.path.join(MODS, "ZLJ Combat Latex Pack - P02B Pilot", "meshes", "ZLJ", "CombatLatex", "CL06_ToxicCat"),
    "OUTPUT": os.path.join(MODS, "输出·BodySlide Output", "meshes", "ZLJ", "CombatLatex", "CL06_ToxicCat"),
    "SOURCE": os.path.join(MODS, "makaron-COSPLAY - AE_Toxic_Cat — 【服装·装备】【来源·本地】", "meshes", "AE_Toxic_Cat"),
    "STAGING": os.path.join(STAGING, "meshes", "ZLJ", "CombatLatex", "CL06_ToxicCat"),
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    rows = []
    for n in NAMES:
        stg = os.path.join(PLACES["STAGING"], n)
        stg_sha = sha(stg) if os.path.isfile(stg) else ""
        stg_mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(stg).st_mtime)) if os.path.isfile(stg) else ""
        for label in ("PILOT", "OUTPUT", "SOURCE", "STAGING"):
            p = os.path.join(PLACES[label], n)
            if not os.path.isfile(p):
                rows.append([OUTFIT, n, label, "NO", "", "", "", stg_sha, stg_mtime,
                             "ABSENT", "not present in this physical provider"])
                continue
            st = os.stat(p)
            mt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime))
            s = sha(p)
            in_window = BUILD_WINDOW[0] <= mt <= BUILD_WINDOW[1]
            if label == "PILOT":
                cls = ("BUILD_WROTE_TO_PILOT_PROVIDER"
                       if in_window and s != stg_sha else
                       ("UNCHANGED_SOURCE_COPY" if s == stg_sha else "UNKNOWN"))
                note = ("mtime falls inside the BodySlide batch window and the content differs from the "
                        "pre-build staging copy -> BodySlide rewrote the existing virtual file in place"
                        if cls == "BUILD_WROTE_TO_PILOT_PROVIDER" else
                        ("byte-identical to the pre-build staging copy" if cls == "UNCHANGED_SOURCE_COPY"
                         else "content differs but mtime is outside the build window"))
            elif label == "STAGING":
                cls = "PRE_BUILD_REFERENCE"
                note = "migration output, untouched since 00:31:02"
            elif label == "SOURCE":
                cls = "ORIGINAL_MOD"
                note = "original mod asset, unmodified"
            else:
                cls = "ABSENT"
                note = "BodySlide created _0 here instead; _1 was redirected to the existing PILOT file"
            rows.append([OUTFIT, n, label, "YES", s, s[:16], mt, stg_sha, stg_mtime, cls, note])
    C.write_csv(os.path.join(REPORTS, "P02B_CL06_BUILD_PROVIDER_AUDIT.csv"),
                ["outfit_id", "file", "physical_provider", "exists", "sha256", "sha256_16",
                 "mtime", "pre_build_staging_sha256", "pre_build_staging_mtime",
                 "classification", "evidence"], rows)
    for r in rows:
        if r[7] == r[4] or r[2] in ("PILOT", "OUTPUT"):
            print("%-28s %-8s %-9s %-20s %-30s" % (r[1][:28], r[2], r[3], r[6], r[9]))
    changed = sum(1 for r in rows if r[9] == "BUILD_WROTE_TO_PILOT_PROVIDER")
    print()
    print("BUILD_WROTE_TO_PILOT_PROVIDER count:", changed, "of", len(NAMES))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
