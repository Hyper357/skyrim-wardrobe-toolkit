#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p00r_scan.py 鈥?STAGE A: deterministic read-only file index of the 09 scope.

Walks every mod in the resolved scope exactly once and records, for every file:
mod, relative path, MO2 virtual path, size, sha256, and a category tag.
Also emits per-mod aggregates and the scope evidence block.

Writes ONLY into data/P00_RERUN/. Opens game files in "rb" only.

Usage: python tools/P00_RERUN/p00r_scan.py
"""
from __future__ import annotations

import datetime
import json
import os
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p00r_common as C  # noqa: E402

WORKERS = 8

# VFS root folders that MO2 merges into the game's virtual filesystem.
VFS_ROOTS = ("meshes", "textures", "skse", "scripts", "sounds", "sequence",
             "dialogue", "music", "facegen", "hair", "shaders", "strings",
             "CalienteTools", "bodyphysics", "misc", "docs", "fonts",
             "interface", "tutorial", "video", "grass", "survival")

# file-category tables -------------------------------------------------------
BODYS = (
    ("bodyslide_shapedata_nif", "calientetools/bodyslide/shapedata/", ".nif"),
    ("bodyslide_shapedata_osd", "calientetools/bodyslide/shapedata/", ".osd"),
    ("bodyslide_sliderset", "calientetools/bodyslide/slidersets/", None),
    ("bodyslide_slidergroup", "calientetools/bodyslide/slidergroups/", ".xml"),
    ("bodyslide_sliderpreset", "calientetools/bodyslide/sliderpresets/", ".xml"),
    ("bodyslide_conversion", "calientetools/bodyslide/conversionsets/", None),
    ("bodyslide_other", "calientetools/", None),
)

PHYS_EXT = {".hkx", ".hkproj", ".tri", ".hkxstd", ".hkxstm"}


def vpath_of(rel_lower: str) -> str:
    for root in VFS_ROOTS:
        if rel_lower.startswith(root + "/"):
            return rel_lower
    return rel_lower


def classify(rel_lower: str, ext: str) -> str:
    for name, prefix, want_ext in BODYS:
        if rel_lower.startswith(prefix) and (want_ext is None or ext == want_ext):
            return name
    if ext in C.PLUGIN_EXT:
        return "plugin"
    if ext == ".nif":
        return "nif"
    if ext == ".dds":
        return "dds"
    if ext in PHYS_EXT:
        return "physics_mesh"
    if ext == ".psc":
        return "script_psc"
    if ext == ".json":
        return "json"
    if ext == ".ini":
        return "ini"
    if ext == ".toml":
        return "toml"
    if ext in (".yaml", ".yml"):
        return "yaml"
    if ext == ".xml":
        return "xml"
    if ext == ".txt":
        return "txt"
    if ext == ".fomod":
        return "fomod"
    if ext in (".bsa", ".ba2"):
        return "bsa"
    if ext in (".esm",):
        return "plugin"
    return "other"


def main() -> int:
    C.ensure_dirs()
    entries = C.read_modlist()
    sep, lower, above, lo, hi, members = C.resolve_scope(entries)
    total_lines = len(entries)
    current_sha = C.sha256_file(C.MODLIST)

    # ---- scope drift detection -------------------------------------------
    # MO2 rewrites modlist.txt on every exit. If it changed since the last
    # scan, record exactly what moved so the reports can be re-based instead
    # of silently carrying stale priority numbers.
    drift_note = None
    pre_baseline = None
    prev_path = os.path.join(C.DATA, "00_scope_evidence.json")
    if os.path.isfile(prev_path):
        try:
            with open(prev_path, "r", encoding="utf-8") as fh:
                prev = json.load(fh)
            pre_baseline = prev.get("pre_drift_baseline")
            # Compare against the oldest recorded snapshot, not just the last
            # one, so a re-based run still reports the full drift history.
            base = pre_baseline or prev
            prev_sha = base.get("modlist_sha256")
            prev_names = set(base.get("scope_member_names")
                             or prev.get("scope_member_names") or [])
            if prev_sha and prev_sha != current_sha:
                cur_names = {m.name for m in members}
                drift_note = {
                    "previous_sha256": prev_sha,
                    "current_sha256": current_sha,
                    "previous_generated_utc": prev.get("generated_utc"),
                    "previous_scope_lines": [base.get("scope_first_line"),
                                             base.get("scope_last_line")],
                    "current_scope_lines": [lo, hi],
                    "previous_modlist_lines": base.get("modlist_lines"),
                    "current_modlist_lines": total_lines,
                    "members_added": sorted(cur_names - prev_names),
                    "members_removed": sorted(prev_names - cur_names),
                    "member_set_unchanged": cur_names == prev_names,
                    "verdict": ("member set unchanged - only the MO2 ordering "
                                "coordinates shifted; asset findings remain "
                                "valid, priority/leftpane_row were re-based"
                                if cur_names == prev_names else
                                "MEMBER SET CHANGED - the scan subject itself "
                                "moved; every stage must be re-run"),
                }
                C.log("!! SCOPE DRIFT detected vs previous scan")
                C.log(f"   sha {prev.get('modlist_sha256')[:16]}... -> "
                      f"{current_sha[:16]}...")
                C.log(f"   scope L{prev.get('scope_first_line')}-"
                      f"{prev.get('scope_last_line')} -> L{lo}-{hi}")
                C.log(f"   added={len(cur_names - prev_names)} "
                      f"removed={len(prev_names - cur_names)}")
        except Exception as e:                            # noqa: BLE001
            # never let drift bookkeeping break the scan, but do not hide it
            C.log(f"!! drift bookkeeping failed: {e!r}")
            drift_note = {"error": repr(e)[:200],
                          "current_sha256": current_sha}

    C.log(f"scope L{lo}..L{hi}  members={len(members)}  "
          f"modlist={current_sha[:16]}... lines={total_lines}")

    jobs = []          # (idx, mod, rel, full, size, ext, cat, vpath)
    mod_meta = {}
    for m in members:
        root = C.MODS_DIR and os.path.join(C.MODS_DIR, m.name)
        exists = os.path.isdir(root)
        mod_meta[m.name] = {
            "line_no": m.line_no,
            "state": m.state,
            "leftpane_row": total_lines - m.line_no + 1,
            "section": sep.name,
            "exists": exists,
            "root": root,
        }
        if not exists:
            C.log(f"  !! FOLDER MISSING: {m.name}")
            continue
        for rel, full, size in C.iter_files(root):
            low = rel.lower()
            ext = os.path.splitext(low)[1]
            jobs.append((m.name, rel, low, full, size, ext,
                         classify(low, ext), vpath_of(low)))

    C.log(f"files to index: {len(jobs):,}")

    def work(job):
        mod, rel, low, full, size, ext, cat, vp = job
        try:
            digest = C.sha256_file(full)
        except OSError as e:
            digest = "ERROR:" + repr(e)[:60]
        try:
            mt = os.path.getmtime(full)
        except OSError:
            mt = -1.0
        return {"mod": mod, "rel": rel, "vpath": vp, "ext": ext,
                "cat": cat, "size": size, "sha256": digest, "mtime": mt}

    t0 = time.time()
    files = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for i, rec in enumerate(ex.map(work, jobs, chunksize=64), 1):
            files.append(rec)
            if i % 1000 == 0:
                C.log(f"  hashed {i:,}/{len(jobs):,}  "
                      f"({time.time()-t0:.0f}s)")
    C.log(f"hashing done in {time.time()-t0:.0f}s")

    # ---- per-mod aggregates ------------------------------------------------
    by_mod = defaultdict(Counter)
    size_by_mod = defaultdict(Counter)
    for f in files:
        by_mod[f["mod"]][f["cat"]] += 1
        size_by_mod[f["mod"]][f["cat"]] += max(f["size"], 0)
    mod_rows = []
    for m in members:
        c = by_mod[m.name]
        s = size_by_mod[m.name]
        cand, tag, fam, flag, src = C.body_candidate_from_name(m.name)
        mod_rows.append({
            "mod_name": m.name,
            "MOD_ID": m.name,
            "priority": m.line_no,
            "mo2_leftpane_row": total_lines - m.line_no + 1,
            "enabled": m.state,
            "folder_exists": int(mod_meta[m.name]["exists"]),
            "size_bytes": sum(s.values()),
            "file_count": sum(c.values()),
            "plugin_count": c["plugin"],
            "nif_count": c["nif"],
            "dds_count": c["dds"],
            "bodyslide_count": (c["bodyslide_shapedata_nif"]
                                + c["bodyslide_shapedata_osd"]
                                + c["bodyslide_sliderset"]
                                + c["bodyslide_slidergroup"]
                                + c["bodyslide_sliderpreset"]
                                + c["bodyslide_conversion"]),
            "bodyslide_shapedata_nif": c["bodyslide_shapedata_nif"],
            "bodyslide_shapedata_osd": c["bodyslide_shapedata_osd"],
            "bodyslide_sliderset_osp": sum(
                1 for f in files
                if f["mod"] == m.name
                and f["cat"] == "bodyslide_sliderset" and f["ext"] == ".osp"),
            "bodyslide_sliderset_xml": sum(
                1 for f in files
                if f["mod"] == m.name
                and f["cat"] == "bodyslide_sliderset" and f["ext"] == ".xml"),
            "bodyslide_slidergroup": c["bodyslide_slidergroup"],
            "bodyslide_sliderpreset": c["bodyslide_sliderpreset"],
            "physics_count": c["physics_mesh"],
            "script_count": c["script_psc"],
            "config_count": (c["ini"] + c["json"] + c["toml"] + c["yaml"]
                             + c["xml"] + c["txt"]),
            "ini_count": c["ini"], "json_count": c["json"],
            "xml_count": c["xml"], "txt_count": c["txt"],
            "toml_count": c["toml"], "yaml_count": c["yaml"],
            "bsa_count": c["bsa"],
            "body_candidate_name": cand,
            "body_tag": tag, "body_tokens": "+".join(fam),
            "body_family_flag": flag, "body_source": src,
            "plugin_files": "; ".join(
                sorted(f["rel"] for f in files
                       if f["mod"] == m.name and f["cat"] == "plugin")),
        })

    C.write_json(os.path.join(C.DATA, "00_scope_evidence.json"), {
        "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "mo2_instance": C.MO2_INSTANCE, "mo2_profile": C.MO2_PROFILE,
        "modlist_path": C.MODLIST, "modlist_sha256": C.sha256_file(C.MODLIST),
        "modlist_lines": total_lines,
        "modlist_mtime": datetime.datetime.fromtimestamp(
            os.path.getmtime(C.MODLIST)).isoformat(),
        "scope_rule": "mod on line L belongs to nearest separator at LARGER line; "
                      "separator S owns (nearest_sep_below_S + 1) .. (S - 1)",
        "separator_name": sep.name, "separator_line": sep.line_no,
        "separator_leftpane_row": total_lines - sep.line_no + 1,
        "lower_bound_sep": lower.name if lower else None,
        "lower_bound_sep_line": lower.line_no if lower else None,
        "upper_bound_sep": above.name if above else None,
        "upper_bound_sep_line": above.line_no if above else None,
        "scope_first_line": lo, "scope_last_line": hi,
        "scope_mod_count": len(members),
        "scope_total_files": len(files),
        "scope_total_bytes": sum(max(f["size"], 0) for f in files),
        "scope_member_names": [m.name for m in members],
        "drift": drift_note,
        # The oldest snapshot is carried forward so drift history survives
        # repeated re-basing; without this the baseline is lost on every write.
        "pre_drift_baseline": (pre_baseline or {
            "modlist_sha256": current_sha,
            "modlist_lines": total_lines,
            "scope_first_line": lo,
            "scope_last_line": hi,
        }),
    })
    C.write_json_gz(os.path.join(C.DATA, "01_file_index.json.gz"), files)
    C.write_json(os.path.join(C.DATA, "01_mod_aggregates.json"), mod_rows)

    cats = Counter(f["cat"] for f in files)
    C.log("category totals: " + ", ".join(f"{k}={v}" for k, v in
                                          cats.most_common()))
    C.log(f"DONE stage A: {len(mod_rows)} mods, {len(files):,} files, "
          f"{sum(max(f['size'],0) for f in files):,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
