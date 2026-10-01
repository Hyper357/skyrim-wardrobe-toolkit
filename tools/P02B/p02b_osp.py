# -*- coding: utf-8 -*-
"""P02B1 CL06_ToxicCat OSP migration.

Reads the source OSP (read-only) and writes the target OSP into staging with the
mandated namespace, keeping the source's slider set intact.

RULING-04: one Outfit = one target OSP, which may contain several SliderSets. This
pilot has a single set, so no merging is required and a multi-set OSP is explicitly
NOT treated as a blocker.
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "P02A"))
import p02a_common as C

OUTFIT = "CL06_ToxicCat"
MODS = r"E:\SkyrimAE\mo2\mods"
STAGING = os.path.join(C.ROOT, "staging", "ZLJ Combat Latex Pack - P02B Pilot")
REPORTS = os.path.join(C.ROOT, "reports", "P02B")


def bs_row():
    p = os.path.join(C.OUT, "P02A_BODYSLIDE_MIGRATION.csv")
    with open(p, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if r.get("OUTFIT_ID") == OUTFIT:
                return r
    raise SystemExit("no bodyslide row for " + OUTFIT)


def main():
    r = bs_row()
    old_osp = r["old_osp"]
    new_osp = r["new_osp"]
    ui = r["new_ui_name"]
    src = os.path.join(MODS, C.OUTFITS[OUTFIT]["primary"], old_osp.replace("\\", os.sep))
    dst = os.path.join(STAGING, new_osp.replace("\\", os.sep))
    if not os.path.isfile(src):
        raise SystemExit("source OSP not found: " + src)

    text = open(src, encoding="utf-8-sig").read()
    old_set_name = r["slider_set_name"]
    old_data_folder = r["old_shape_data"].rstrip("\\").split("\\")[-1]          # AE_Toxic_Cat
    new_data_folder = "ZLJ_Combat_Latex\\CL06_ToxicCat\\" + old_data_folder
    old_output_path = r["old_output_path"]                                       # meshes\AE_Toxic_Cat
    new_output_path = r["new_output_path"].rstrip("\\")                          # meshes\ZLJ\CombatLatex\CL06_ToxicCat

    # The source OSP already carries SEVERAL slider sets (this is exactly the structure
    # RULING-04 declares supported). Rename every set with the frozen UI convention;
    # the primary set keeps the name the review specified verbatim.
    PART_LABEL = {"": "AE Toxic Cat", "_Feet": "Feet", "_Hand": "Hands",
                  "_Top": "Top", "_St": "Stockings"}
    set_names = re.findall(r'<SliderSet name="([^"]+)">', text)
    set_rename = {}
    for name in set_names:
        if name == old_set_name:
            set_rename[name] = ui                       # exactly as the review specified
        else:
            suffix = name[len(old_set_name):] if name.startswith(old_set_name) else ""
            set_rename[name] = "[ZLJ Combat Latex] ToxicCat - " + PART_LABEL.get(suffix, suffix.lstrip("_") or name)

    edits = []
    for old_name, new_name in set_rename.items():
        edits.append(('<SliderSet name="%s">' % old_name, '<SliderSet name="%s">' % new_name))
    edits += [
        ("<DataFolder>%s</DataFolder>" % old_data_folder, "<DataFolder>%s</DataFolder>" % new_data_folder),
        ('DataFolder="%s"' % old_data_folder, 'DataFolder="%s"' % new_data_folder),
        ("<OutputPath>%s</OutputPath>" % old_output_path, "<OutputPath>%s</OutputPath>" % new_output_path),
    ]
    counts = {}
    for old, new in edits:
        n = text.count(old)
        counts[old] = n
        text = text.replace(old, new)
    counts["__slider_sets_renamed__"] = len(set_rename)

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8-sig", newline="") as f:
        f.write(text)

    # ---- verify against the source ----
    src_text = open(src, encoding="utf-8-sig").read()

    def count(t, pat):
        return len(re.findall(pat, t))

    report = dict(old_osp=old_osp, new_osp=new_osp, ui_name=ui,
                  old_data_folder=old_data_folder, new_data_folder=new_data_folder,
                  old_output_path=old_output_path, new_output_path=new_output_path,
                  edits=counts,
                  src_sliders=count(src_text, r"<Slider "),
                  dst_sliders=count(text, r"<Slider "),
                  src_shapes=count(src_text, r"<Shape "),
                  dst_shapes=count(text, r"<Shape "),
                  src_data=count(src_text, r"<Data "),
                  dst_data=count(text, r"<Data "),
                  src_slider_sets=count(src_text, r"<SliderSet "),
                  dst_slider_sets=count(text, r"<SliderSet "),
                  set_rename=set_rename,
                  dst_has_old_folder=old_data_folder in text and new_data_folder not in text,
                  leftovers=[old for old, _ in edits if old in text])
    print("OSP written:", dst)
    for k, v in report.items():
        print("   %-20s %s" % (k, v))
    print()
    # The OSP is a staged deliverable, so it must appear in the staging manifest too.
    man_path = os.path.join(REPORTS, "P02B_CL06_STAGING_MANIFEST.csv")
    if os.path.exists(man_path):
        with open(man_path, encoding="utf-8-sig", newline="") as f:
            rd = list(csv.reader(f))
        head, body = rd[0], rd[1:]
        body = [r for r in body if not (len(r) > 4 and r[4].lower().endswith(".osp"))]
        body.append([OUTFIT, "OSP", old_osp, C.OUTFITS[OUTFIT]["primary"], new_osp, "COPY",
                     "RULING-04 | topology=DEDICATED_3P", os.path.getsize(src), os.path.getsize(dst),
                     str(report["dst_sliders"]), "COPIED_TEXTURE_REWRITTEN",
                     "%d slider sets, %d sliders" % (report["dst_slider_sets"], report["dst_sliders"])])
        with open(man_path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f, quoting=csv.QUOTE_ALL)
            w.writerow(head)
            w.writerows(body)
        print("manifest updated with the OSP row")
    print("slider count preserved:", report["src_sliders"] == report["dst_sliders"])
    print("shape count preserved :", report["src_shapes"] == report["dst_shapes"])
    print("all edits applied     :", all(v > 0 for v in counts.values()))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
