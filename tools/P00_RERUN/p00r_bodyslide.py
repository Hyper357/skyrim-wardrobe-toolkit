#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p00r_bodyslide.py — STAGE E: BodySlide project graph + effective VFS view.

PART 2 (this revision) adds the MO2 EFFECTIVE VFS VIEW on top of the XML
extraction. The extraction is unchanged and stays authoritative; this layer only
ADDS fields.

  Verified fact this layer exists to express: 07 has 176 physical .osp rows but
  only 156 unique virtual VFS paths. 20 paths are supplied by more than one mod
  (40 rows), so MO2 shadows part of the corpus. A consumer that reads 07 as a
  flat list will double-count those 20 projects and may read a body/3BA verdict
  off a .osp that the game never actually loads.

  MO2 priority rule (already implemented and frozen in 01_mod_aggregates.json,
  NOT re-derived here):
      modlist.txt lists the left pane in REVERSE. Line 1 is the BOTTOM row of
      the left pane and therefore the HIGHEST overwrite priority. A mod's
      `priority` field is that line number, so the VFS WINNER for a virtual path
      is the provider with the SMALLEST priority number.
  Windows virtual paths are case-insensitive, so grouping is done on
  vfs_key = rel.replace("/", "\\").lower(), which is exactly C.nif_id()'s
  normal form and therefore the same key 13_MO2_CONFLICT_MAP uses.

  Per project row, added here:
      vfs_path / vfs_provider_count / vfs_shadowed_path
      winning_provider / winning_provider_priority / winning_provider_sha256
      this_mod_priority
      shadowed_provider            semicolon list of the mods at this VFS path
                                  whose copy is OVERRIDDEN (i.e. every provider
                                  except the winner). This is a property of the
                                  PATH, so it is identical on every row of that
                                  path; `effective` is what says whether THIS
                                  row is the usable one.
      effective                   "yes" only for the single winning row of a
                                  path; "no" for every shadowed row. A row
                                  with effective=no is trace-only and must
                                  never be treated as a usable project.
      vfs_status / vfs_effective_reason / content_conflict

  Counts are published two ways so nothing has to be recomputed downstream:
    * on EVERY project row, as PHYSICAL_PROJECT_ROWS / EFFECTIVE_VFS_PROJECTS /
      SHADOWED_PROJECT_ROWS / UNIQUE_VFS_PROJECT_PATHS;
    * at top level in 07_bodyslide_vfs_summary.json.
  07_bodyslide_projects.json deliberately stays a LIST so the frozen
  p00r_reports.py consumer (bsp = load(...); for p in bsp) keeps working.

---
Original stage-E header, retained for the extraction rationale:
CORRECTED (audit finding #3). The first P00_RERUN pass called parse_osd() on
every SliderSets/*.osp file. That was wrong on two counts:

  * .osp is a SliderSet project in XML, not an OSD container. parse_osd()
    checked for the b"OSD\\0" magic, never matched, and returned empty without
    raising -- so the run reported "0 OSP parse errors" while having extracted
    nothing. That false clean is the worst kind of bug.
  * the old code then fell back to a hard-coded
    output_path = "meshes\\clothing", i.e. a fabricated value.

Real shapes, measured on this install:
  CalienteTools/BodySlide/SliderSets/*.osp
      XML: SliderSetInfo/SliderSet[@name]/DataFolder/SourceFile/
           OutputPath/OutputFile[@GenWeights]/Shape[@target]/
           Slider[@name]/Data[@name][@target][@local]
      often starts with a UTF-8 BOM, so a naive head[:1] == b"<" test fails.
  CalienteTools/BodySlide/ShapeData/*.osd
      binary slider-diff container. The magic is the 4 bytes b"OSD\\0"
      stored LITTLE-ENDIAN, so the on-disk bytes read b"\\x00DSO". The first
      pass compared the file's first 4 bytes to b"OSD\\0" and therefore never
      matched it either.
  CalienteTools/BodySlide/ShapeData/*.nif
      the base mesh, parsed by stage C.

If a field cannot be extracted it is recorded as UNKNOWN. Nothing is invented.
"""
from __future__ import annotations

import json
import os
import re
import struct
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p00r_common as C  # noqa: E402

UNKNOWN = "UNKNOWN"

# SliderSets / ShapeData / SliderGroups / SliderPresets live under this root.
BS_ROOT = "CalienteTools/BodySlide"
OSD_MAGIC = 0x4F534400          # "OSD\0" as a little-endian uint32


# ---------------------------------------------------------------- OSD ----
def parse_osd(path: str) -> dict:
    """Parse a ShapeData/*.osd binary slider-diff container.

    Layout confirmed by hex inspection (RileyHeels / Nyes osd files):
        0x00  uint32  magic  == 0x4F534400 ("OSD\\0", little-endian)
        0x04  uint32  version (1 on this install)
        0x08  uint32  data offset
        ...   zero padding
        data offset:
                uint8  name length
                char[] shape name            (e.g. "Corset7B Lowerw")
                binary slider blocks         (not decoded here)
    We extract the container identity and the shape name, which is what the
    project graph needs. Slider weights are left UNKNOWN rather than guessed.
    """
    try:
        with open(path, "rb") as fh:
            blob = fh.read(1 << 20)
    except OSError as e:
        return {"error": repr(e)[:120], "shape_names": [], "sliders": []}
    if len(blob) < 12:
        return {"error": "too short", "shape_names": [], "sliders": []}
    magic = struct.unpack_from("<I", blob, 0)[0]
    if magic != OSD_MAGIC:
        return {"error": f"bad magic 0x{magic:08X}", "shape_names": [],
                "sliders": []}
    out = {
        "magic": f"0x{magic:08X}",
        "version": struct.unpack_from("<I", blob, 4)[0],
        "data_offset": struct.unpack_from("<I", blob, 8)[0],
        "bytes": os.path.getsize(path),
        "shape_names": [],
        "sliders": [],
        "slider_count": None,
    }
    # CORRECTED: the length-prefixed shape name sits at 0x0C, i.e. directly
    # after the 12-byte header. The uint32 at 0x08 is NOT a usable offset --
    # it takes 243 distinct values (1..2442) across the corpus and only 6/513
    # files parse at it, so treating it as an offset left 507/513 shape names
    # silently UNKNOWN. That is the same false-clean failure mode as the
    # original .osp bug, so the fallback is kept but never used as primary.
    off = 12
    if off >= len(blob):
        out["shape_names"] = [UNKNOWN]
        out["shape_offset_used"] = "truncated"
        return out
    p = off
    names = []
    while p < len(blob) and len(names) < 64:
        ln = blob[p]
        if ln == 0 or 1 <= ln <= 120 and p + 1 + ln <= len(blob):
            raw = blob[p + 1:p + 1 + ln]
            try:
                s = raw.decode("utf-8")
            except UnicodeDecodeError:
                break
            if not s or not all(9 <= ord(ch) < 127 for ch in s):
                break
            names.append(s)
            p += 1 + ln
            continue
        break
    out["shape_offset_used"] = "0x0C"
    out["shape_names"] = names or [UNKNOWN]
    return out


# ---------------------------------------------------------------- OSP ----
def parse_osp(path: str) -> dict:
    """Parse a SliderSets/*.osp XML project. Returns the real field set."""
    out = {
        "slider_set_name": None,
        "data_folder": None,
        "source_file": None,
        "output_path": None,
        "output_file": None,
        "output_gen_weights": None,
        "shapes": [],
        "sliders": [],
        "zap_sliders": [],
        "osd_refs": [],
        "parse_error": None,
    }
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError as e:
        out["parse_error"] = repr(e)[:120]
        return out
    # strip the UTF-8 BOM that many of these files carry
    if raw[:3] == b"\xef\xbb\xbf":
        raw = raw[3:]
    try:
        root = ET.fromstring(raw.decode("utf-8", "replace"))
    except ET.ParseError as e:
        out["parse_error"] = f"XML: {e}"
        return out

    ss = root.find("SliderSet")
    if ss is None:
        ss = root
    out["slider_set_name"] = ss.get("name") or (ss.findtext("DataFolder")
                                                 or UNKNOWN)
    out["data_folder"] = ss.findtext("DataFolder")
    out["source_file"] = ss.findtext("SourceFile")
    out["output_path"] = ss.findtext("OutputPath")
    of = ss.find("OutputFile")
    if of is not None:
        out["output_file"] = (of.text or "").strip() or None
        out["output_gen_weights"] = of.get("GenWeights")
    else:
        out["output_file"] = None

    for sh in ss.findall("Shape"):
        out["shapes"].append({
            "name": (sh.text or "").strip(),
            "target": sh.get("target"),
            "lock_normals": sh.get("LockNormals"),
            "zap": sh.get("zap") or sh.get("Zap"),
        })
        if (sh.get("zap") or "").lower() in ("true", "1"):
            out["zap_sliders"].append((sh.text or "").strip())

    for sl in ss.findall("Slider"):
        name = sl.get("name")
        d = sl.find("Data")
        entry = {
            "name": name,
            "invert": sl.get("invert"),
            "small": sl.get("small"),
            "big": sl.get("big"),
            "data_name": d.get("name") if d is not None else None,
            "data_target": d.get("target") if d is not None else None,
            "data_local": d.get("local") if d is not None else None,
            "osd_ref": (d.text or "").strip() if d is not None else None,
        }
        out["sliders"].append(entry)
        if entry["osd_ref"]:
            out["osd_refs"].append(entry["osd_ref"])

    # never fabricate: anything still missing is explicitly UNKNOWN
    for k in ("data_folder", "source_file", "output_path", "output_file"):
        if not out[k]:
            out[k] = UNKNOWN
    if not out["slider_set_name"]:
        out["slider_set_name"] = UNKNOWN
    return out


# ------------------------------------------------------------ grouping ---
def family_from(path: str) -> str:
    p = path.replace("\\", "/")
    if "SliderSets/" in p:
        return "SLIDERSET_OSP"
    if "ShapeData/" in p and p.lower().endswith(".osd"):
        return "SHAPEDATA_OSD"
    if "ShapeData/" in p and p.lower().endswith(".nif"):
        return "SHAPEDATA_NIF"
    if "SliderGroups/" in p:
        return "SLIDERGROUP"
    if "SliderPresets/" in p:
        return "SLIDERPRESET"
    return "OTHER"


# ============================================================ VFS VIEW =====
VFS_RULE = (
    "MO2 VFS: modlist.txt lists the left pane in REVERSE, line 1 is the BOTTOM "
    "row and therefore the HIGHEST overwrite priority. priority == that line "
    "number (data/P00_RERUN/01_mod_aggregates.json), so for each virtual path "
    "the WINNER is the provider with the SMALLEST priority number. Grouping key "
    "vfs_path = OSP_PATH with / -> \\ and lower-cased (Windows virtual paths are "
    "case-insensitive; same normal form as 13_MO2_CONFLICT_MAP).")

R07_COLS = ["BODYSLIDE_PROJECT_ID", "OSP_PATH", "sha256", "MOD_ID", "source_mod",
            "ui_outfit_name", "slider_set_name", "data_folder", "source_file",
            "base_nif", "base_nif_shapes",
            "shapedata_nif_count", "shapedata_osd_count",
            "output_path", "output_file", "output_gen_weights", "output_nif",
            "output_path_is_guessed",
            "shape_names", "n_shapes", "n_sliders", "zap_sliders",
            "osd_ref_count", "osd_names",
            "body_candidate", "body_families", "body_flag", "body_evidence",
            "needs_3ba_conversion", "xml_error", "provenance",
            # ---- effective VFS view (added by this revision) ----
            "vfs_path", "vfs_provider_count", "vfs_shadowed_path",
            "winning_provider", "winning_provider_priority",
            "winning_provider_sha256", "this_mod_priority",
            "shadowed_provider", "shadowed_provider_count",
            "effective", "vfs_status", "vfs_effective_reason",
            "content_conflict",
            "PHYSICAL_PROJECT_ROWS", "EFFECTIVE_VFS_PROJECTS",
            "SHADOWED_PROJECT_ROWS", "UNIQUE_VFS_PROJECT_PATHS",
            "note"]


def vfs_key(rel: str) -> str:
    """Windows virtual path: backslashes, case-folded. Same form as C.nif_id."""
    return (rel or "").replace("/", "\\").lower()


def _jval(v):
    """Same rendering contract as p00r_reports.jval (UNKNOWN for absent)."""
    if v is None or v == "":
        return UNKNOWN
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, int):
        return C.record_id(v)
    return str(v)


def _jnum(v):
    """Same rendering contract as p00r_reports.jnum (counts, never FormIDs)."""
    if v is None or v == "":
        return UNKNOWN
    if isinstance(v, bool):
        return "yes" if v else "no"
    return str(v)


def _joinl(values, sep="; ", limit=1200, empty=UNKNOWN):
    out = [str(x) for x in (values or []) if x not in (None, "")]
    return sep.join(out)[:limit] if out else empty


def resolve_vfs(projects, priority_by_mod):
    """Decide, per project row, which mod's .osp actually reaches the VFS.

    Mutates `projects` in place (additive only) and returns the summary dict
    that is written to 07_bodyslide_vfs_summary.json.

    Nothing here is guessed. A provider whose mod is absent from
    01_mod_aggregates.json has no verifiable priority, so it is reported as
    UNKNOWN and can never be declared the winner.
    """
    groups = defaultdict(list)
    for p in projects:
        groups[vfs_key(p.get("OSP_PATH"))].append(p)

    unresolved = []
    conflicts = []          # genuine priority ties (should be impossible)
    shadowed_paths = []
    n_shadowed_rows = 0

    for key in sorted(groups):
        rows = groups[key]

        def prio_of(r):
            v = priority_by_mod.get(r.get("MOD_ID"))
            return v if isinstance(v, int) else None

        ranked = sorted(
            rows,
            key=lambda r: (0 if prio_of(r) is not None else 1,
                           prio_of(r) if prio_of(r) is not None else 0,
                           r.get("sha256") or "",
                           r.get("MOD_ID") or ""))
        winner = ranked[0]
        w_mod = winner.get("MOD_ID")
        w_prio = prio_of(winner)
        w_sha = winner.get("sha256")

        if w_prio is None:
            unresolved.append({"vfs_path": key, "mod": w_mod,
                               "reason": "winner candidate has no priority in "
                                         "01_mod_aggregates.json"})
        tied = [r.get("MOD_ID") for r in rows
                if prio_of(r) is not None and prio_of(r) == w_prio
                and r is not winner]
        if tied:
            conflicts.append({"vfs_path": key, "priority": w_prio,
                              "mods": [w_mod] + tied,
                              "tie_break": "sha256 then mod name (deterministic)"})

        losers = [r for r in rows if r is not winner]
        shadow_names = [r.get("MOD_ID") or UNKNOWN for r in losers]

        for r in rows:
            is_win = r is winner
            p_prio = prio_of(r)
            if p_prio is None:
                unresolved.append({"vfs_path": key, "mod": r.get("MOD_ID"),
                                   "reason": "provider priority UNKNOWN in "
                                             "01_mod_aggregates.json"})
            if is_win:
                status = "sole_provider" if not losers else f"winner_of_{len(rows)}"
                if not losers:
                    reason = ("only provider at this VFS path; nothing shadows it")
                else:
                    reason = (f"wins: modlist line {w_prio} is the HIGHEST "
                              f"overwrite priority among {len(rows)} providers")
            else:
                status = f"shadowed_of_{len(rows)}"
                reason = (f"SHADOWED: modlist line {p_prio} loses to mod "
                          f"{w_mod} (line {w_prio}) at this VFS path -- this "
                          f"copy never reaches the game; trace only, do not use")
            r["vfs_path"] = key
            r["vfs_provider_count"] = len(rows)
            r["vfs_shadowed_path"] = "yes" if losers else "no"
            r["winning_provider"] = w_mod or UNKNOWN
            r["winning_provider_priority"] = w_prio
            r["winning_provider_sha256"] = w_sha
            r["this_mod_priority"] = p_prio
            r["shadowed_provider"] = shadow_names
            r["shadowed_provider_count"] = len(shadow_names)
            r["effective"] = "yes" if is_win else "no"
            r["vfs_status"] = status
            r["vfs_effective_reason"] = reason
            r["content_conflict"] = (
                "no" if (r.get("sha256") or "") == (w_sha or "") else "yes")

        if losers:
            n_shadowed_rows += len(losers)
            shadowed_paths.append({
                "vfs_path": key,
                "winning_provider": w_mod or UNKNOWN,
                "winning_provider_priority": w_prio,
                "winning_provider_sha256": w_sha,
                "shadowed_provider": shadow_names,
                "shadowed_provider_count": len(shadow_names),
                "physical_rows": len(rows),
                "content_conflict": any(
                    (r.get("sha256") or "") != (w_sha or "") for r in rows),
            })

    n_phys = len(projects)
    n_eff = sum(1 for p in projects if p.get("effective") == "yes")
    n_uniq = len(groups)
    for p in projects:
        p["PHYSICAL_PROJECT_ROWS"] = n_phys
        p["EFFECTIVE_VFS_PROJECTS"] = n_eff
        p["SHADOWED_PROJECT_ROWS"] = n_phys - n_eff
        p["UNIQUE_VFS_PROJECT_PATHS"] = n_uniq

    shadow_by_mod = Counter()
    for s in shadowed_paths:
        for m in s["shadowed_provider"]:
            shadow_by_mod[m] += 1
    win_by_mod = Counter(s["winning_provider"] for s in shadowed_paths)

    summary = {
        # ---- the two counts the master report must read, not recompute ----
        "PHYSICAL_PROJECT_ROWS": n_phys,
        "EFFECTIVE_VFS_PROJECTS": n_eff,
        # ---- supporting counts ----
        "SHADOWED_PROJECT_ROWS": n_phys - n_eff,
        "UNIQUE_VFS_PROJECT_PATHS": n_uniq,
        "SHADOWED_VFS_PATHS": len(shadowed_paths),
        "SOLE_PROVIDER_VFS_PATHS": n_uniq - len(shadowed_paths),
        "CONTENT_CONFLICTING_VFS_PATHS": sum(
            1 for s in shadowed_paths if s["content_conflict"]),
        "VFS_RULE": VFS_RULE,
        "VFS_KEY_NORMALISATION": "OSP_PATH with / -> \\ and lower-cased",
        "PRIORITY_SOURCE": "data/P00_RERUN/01_mod_aggregates.json .priority "
                           "(= modlist.txt line number; SMALLEST wins)",
        "READ_THIS_NOT_RECOMPUTE": (
            "The master report must read PHYSICAL_PROJECT_ROWS and "
            "EFFECTIVE_VFS_PROJECTS from here rather than re-deriving them "
            "from the 176-row list, which double-counts shadowed projects."),
        "ROW_SEMANTICS": {
            "effective=yes": "the single winning row of its virtual path; this "
                             "is the .osp the game loads. Usable.",
            "effective=no": "trace-only. This mod's copy is overridden and never "
                            "reaches the VFS. Must NOT be treated as a usable "
                            "BodySlide project.",
            "shadowed_provider": "semicolon list of the mods at this virtual "
                                 "path whose copy IS overridden. It is a "
                                 "property of the path, so it is identical on "
                                 "every row of that path (including the "
                                 "winner's row, where the list names the losers).",
            "content_conflict": "yes when the shadowed copy's sha256 differs "
                                "from the winner's, i.e. the override changes "
                                "what the game sees. no = byte-identical dupe.",
        },
        "CSV_OWNER_NOTE": (
            "07_BODYSLIDE_PROJECTS.csv (VFS columns included) is written by "
            "tools/P00_RERUN/p00r_bodyslide.py. p00r_reports.py is frozen and "
            "still has its own r07 writer WITHOUT the VFS columns, so if it is "
            "re-run it will overwrite this CSV. Re-run p00r_bodyslide.py "
            "afterwards; the JSON files and the counts above are unaffected."),
        "shadowed_provider_mod_counts": dict(shadow_by_mod),
        "winning_provider_mod_counts": dict(win_by_mod),
        "priority_tie_conflicts": conflicts,
        "unresolved_providers": unresolved,
        "shadowed_paths": shadowed_paths,
        "generated_by": "tools/P00_RERUN/p00r_bodyslide.py",
    }
    return summary


def project_csv_row(p):
    """One 07_BODYSLIDE_PROJECTS.csv row. Column-for-column compatible with the
    frozen p00r_reports.r07_bodyslide(), plus the VFS columns."""
    osp = p.get("OSP_PATH") or UNKNOWN
    row = {
        "BODYSLIDE_PROJECT_ID": f"BSP::{C.nif_id(osp)}",
        "OSP_PATH": osp,
        "sha256": p.get("sha256") or UNKNOWN,
        "MOD_ID": p.get("MOD_ID") or UNKNOWN,
        "source_mod": p.get("source_mod") or UNKNOWN,
        "ui_outfit_name": p.get("ui_outfit_name") or UNKNOWN,
        "slider_set_name": p.get("slider_set_name") or UNKNOWN,
        "data_folder": p.get("data_folder") or UNKNOWN,
        "source_file": p.get("source_file") or UNKNOWN,
        "base_nif": p.get("base_nif") or UNKNOWN,
        "base_nif_shapes": _joinl(p.get("base_nif_shapes"), empty="NONE"),
        "shapedata_nif_count": _jnum(p.get("shapedata_nif_count")),
        "shapedata_osd_count": _jnum(p.get("shapedata_osd_count")),
        "output_path": p.get("output_path") or UNKNOWN,
        "output_file": p.get("output_file") or UNKNOWN,
        "output_gen_weights": p.get("output_gen_weights") or UNKNOWN,
        "output_nif": p.get("output_nif") or UNKNOWN,
        "output_path_is_guessed": _jval(p.get("output_path_is_guessed")),
        "shape_names": _joinl(p.get("shape_names"), empty="NONE", limit=400),
        "n_shapes": _jnum(p.get("n_shapes")),
        "n_sliders": _jnum(p.get("n_sliders")),
        "zap_sliders": _joinl(p.get("zap_sliders"), empty="NONE"),
        "osd_ref_count": _jnum(len(p.get("osd_refs") or [])),
        "osd_names": _joinl(p.get("osd_names"), empty="NONE", limit=600),
        "body_candidate": p.get("body_candidate") or UNKNOWN,
        "body_families": _joinl(p.get("body_families"), empty="NONE"),
        "body_flag": p.get("body_flag") or UNKNOWN,
        "body_evidence": p.get("body_evidence") or UNKNOWN,
        "needs_3ba_conversion": p.get("needs_3ba_conversion") or UNKNOWN,
        "xml_error": p.get("xml_error") or "NONE",
        "provenance": p.get("provenance") or UNKNOWN,
        # ---- effective VFS view ----
        "vfs_path": p.get("vfs_path") or UNKNOWN,
        "vfs_provider_count": _jnum(p.get("vfs_provider_count")),
        "vfs_shadowed_path": p.get("vfs_shadowed_path") or UNKNOWN,
        "winning_provider": p.get("winning_provider") or UNKNOWN,
        "winning_provider_priority": _jnum(p.get("winning_provider_priority")),
        "winning_provider_sha256": p.get("winning_provider_sha256") or UNKNOWN,
        "this_mod_priority": _jnum(p.get("this_mod_priority")),
        "shadowed_provider": _joinl(p.get("shadowed_provider"), empty="NONE"),
        "shadowed_provider_count": _jnum(p.get("shadowed_provider_count")),
        "effective": p.get("effective") or UNKNOWN,
        "vfs_status": p.get("vfs_status") or UNKNOWN,
        "vfs_effective_reason": p.get("vfs_effective_reason") or UNKNOWN,
        "content_conflict": p.get("content_conflict") or UNKNOWN,
        "PHYSICAL_PROJECT_ROWS": _jnum(p.get("PHYSICAL_PROJECT_ROWS")),
        "EFFECTIVE_VFS_PROJECTS": _jnum(p.get("EFFECTIVE_VFS_PROJECTS")),
        "SHADOWED_PROJECT_ROWS": _jnum(p.get("SHADOWED_PROJECT_ROWS")),
        "UNIQUE_VFS_PROJECT_PATHS": _jnum(p.get("UNIQUE_VFS_PROJECT_PATHS")),
    }
    base_note = ("no .osp XML parse error; output_path/output_nif are as "
                 "declared in the OSP and were NOT guessed"
                 if not p.get("xml_error") else "osp xml_error recorded")
    if p.get("effective") == "no":
        row["note"] = ("SHADOWED - NOT USABLE. " + base_note + ". "
                       + str(p.get("vfs_effective_reason") or ""))
    else:
        row["note"] = base_note + ". " + str(p.get("vfs_effective_reason") or "")
    return row


def main() -> int:
    C.ensure_dirs()
    with open(os.path.join(C.DATA, "01_mod_aggregates.json"),
              encoding="utf-8") as fh:
        mods = json.load(fh)
    names = {m["mod_name"] for m in mods}
    C.log(f"loaded {len(mods)} mods from stage A")

    import gzip
    with gzip.open(os.path.join(C.DATA, "01_file_index.json.gz"), "rt",
                   encoding="utf-8") as fh:
        idx = json.load(fh)

    # Trust the stage-A classification rather than re-guessing from the path:
    # 122 of these files live outside CalienteTools/BodySlide (mods vendored
    # their own layout), and a prefix test silently dropped them last time.
    CATMAP = {
        "bodyslide_sliderset": "SLIDERSET_OSP",
        "bodyslide_shapedata_nif": "SHAPEDATA_NIF",
        "bodyslide_shapedata_osd": "SHAPEDATA_OSD",
        "bodyslide_slidergroup": "SLIDERGROUP",
        "bodyslide_sliderpreset": "SLIDERPRESET",
    }
    buckets = defaultdict(list)
    for r in idx:
        if r["mod"] not in names:
            continue
        k = CATMAP.get(r["cat"])
        if k:
            buckets[k].append(r)
        elif r["cat"] == "bodyslide_other":
            buckets["OTHER"].append(r)

    C.log("category counts: " + ", ".join(
        f"{k}={len(v)}" for k, v in sorted(buckets.items())))

    # ---- OSP projects ---------------------------------------------------
    osp_rows, osp_errors = [], []
    for r in sorted(buckets["SLIDERSET_OSP"], key=lambda x: x["rel"]):
        p = os.path.join(C.MODS_DIR, r["mod"],
                         r["rel"].replace("/", os.sep))
        d = parse_osp(p)
        if d["parse_error"]:
            osp_errors.append({"path": r["rel"], "mod": r["mod"],
                               "error": d["parse_error"]})
        d["rel"] = r["rel"]
        d["mod"] = r["mod"]
        d["sha256"] = r["sha256"]
        d["size"] = r["size"]
        osp_rows.append(d)
    C.log(f"parsed {len(osp_rows)} .osp XML projects, "
          f"{len(osp_errors)} XML errors")

    # ---- OSD containers --------------------------------------------------
    osd_rows, osd_errors = [], []
    for r in sorted(buckets["SHAPEDATA_OSD"], key=lambda x: x["rel"]):
        p = os.path.join(C.MODS_DIR, r["mod"],
                         r["rel"].replace("/", os.sep))
        d = parse_osd(p)
        if d.get("error"):
            osd_errors.append({"path": r["rel"], "mod": r["mod"],
                               "error": d["error"]})
        d["rel"] = r["rel"]
        d["mod"] = r["mod"]
        d["folder"] = os.path.dirname(r["rel"])
        osd_rows.append(d)
    C.log(f"parsed {len(osd_rows)} .osd containers, {len(osd_errors)} errors")
    if osd_rows:
        C.log("  osd versions: " + str(dict(Counter(
            d.get("version") for d in osd_rows).most_common())))

    # ---- shape-data base meshes -----------------------------------------
    nif_rows = [{"rel": r["rel"], "mod": r["mod"], "sha256": r["sha256"],
                 "size": r["size"],
                 "folder": os.path.dirname(r["rel"])}
                for r in sorted(buckets["SHAPEDATA_NIF"],
                                key=lambda x: x["rel"])]

    # ---- NIF shape names from stage C, to prove the OSP chain -----------
    try:
        import gzip as _gz
        with _gz.open(os.path.join(C.DATA, "08_nif_parsed.json.gz"), "rt",
                      encoding="utf-8") as fh:
            nifdata = json.load(fh)
    except Exception:                                    # noqa: BLE001
        nifdata = []
    shape_by_path = {}
    for n in nifdata:
        shape_by_path[n.get("vpath", "")] = n.get("shape_names", [])

    # ---- join: UI name -> set -> folder -> base nif -> osd -> outputs ---
    by_folder_nif = defaultdict(list)
    by_folder_osd = defaultdict(list)
    for n in nif_rows:
        by_folder_nif[n["folder"]].append(n)
    for d in osd_rows:
        by_folder_osd[d["folder"]].append(d)

    projects = []
    for d in osp_rows:
        folder = (d["data_folder"] if d["data_folder"] != UNKNOWN else None)
        shapedata_dir = f"{BS_ROOT}/ShapeData/{folder}" if folder else None
        src = d["source_file"]
        base_nif = None
        if folder and src:
            cand = f"{shapedata_dir}/{src}"
            if any(n["rel"].lower() == cand.lower() for n in nif_rows):
                base_nif = cand
        osd_refs = sorted({o.rsplit("\\", 1)[-1].rsplit("/", 1)[-1]
                           for o in d["osd_refs"]})
        out_nif = UNKNOWN
        if d["output_path"] != UNKNOWN and d["output_file"] not in (None,
                                                                    UNKNOWN):
            sep = "\\" if "\\" in d["output_path"] else "/"
            out_nif = (d["output_path"].rstrip("\\/") + sep
                       + d["output_file"] + ".nif")
        p = {
            "OSP_PATH": d["rel"],
            "MOD_ID": d["mod"],
            "source_mod": d["mod"],
            "sha256": d["sha256"],
            "ui_outfit_name": d["slider_set_name"],
            "slider_set_name": d["slider_set_name"],
            "data_folder": d["data_folder"],
            "source_file": d["source_file"],
            "base_nif": base_nif or UNKNOWN,
            "shapedata_nif_count": len(by_folder_nif.get(shapedata_dir or "", [])),
            "shapedata_osd_count": len(by_folder_osd.get(shapedata_dir or "", [])),
            "output_path": d["output_path"],
            "output_file": d["output_file"],
            "output_gen_weights": d["output_gen_weights"],
            "output_nif": out_nif,
            "shape_names": [s["name"] for s in d["shapes"]],
            "n_shapes": len(d["shapes"]),
            "n_sliders": len(d["sliders"]),
            "zap_sliders": d["zap_sliders"],
            "osd_refs": d["osd_refs"],
            "osd_names": osd_refs,
            "base_nif_shapes": (shape_by_path.get(base_nif, [])
                                if base_nif else []),
            "xml_error": d["parse_error"] or "",
            "provenance": "osp_xml_parsed",
        }
        projects.append(p)

    # ---- groups / presets ------------------------------------------------
    groups = [{"rel": r["rel"], "mod": r["mod"], "size": r["size"],
               "sha256": r["sha256"], "kind": family_from(r["rel"])}
              for r in sorted(buckets["SLIDERGROUP"], key=lambda x: x["rel"])]
    presets = [{"rel": r["rel"], "mod": r["mod"], "size": r["size"],
                "sha256": r["sha256"]} for r in
               sorted(buckets["SLIDERPRESET"], key=lambda x: x["rel"])]

    # ---- body type / conversion verdict, evidence-only -------------------
    for p in projects:
        toks = C.body_tokens(
            " ".join([p["ui_outfit_name"] or "", p["data_folder"] or "",
                      p["source_file"] or "", p.get("output_path") or ""]))
        p["body_candidate"], p["body_families"], p["body_flag"] = \
            C.classify_body(toks)
        p["body_evidence"] = "osp_name+datafolder+sourcefile+outputpath"
        p["needs_3ba_conversion"] = "UNKNOWN"
        cand = p["body_candidate"]
        if cand == "CBBE_3BA":
            p["needs_3ba_conversion"] = "NO"
        elif cand == "UNKNOWN":
            p["needs_3ba_conversion"] = "UNKNOWN"
        else:
            p["needs_3ba_conversion"] = "YES"
        p["output_path_is_guessed"] = False

    # ---- effective VFS view (MO2 shadow resolution) ----------------------
    # priority = modlist.txt line number; SMALLEST wins. Read from the frozen
    # stage-A aggregate, never re-derived from modlist.txt here.
    priority_by_mod = {m["mod_name"]: m.get("priority") for m in mods}
    vfs = resolve_vfs(projects, priority_by_mod)
    C.log(f"VFS: physical_rows={vfs['PHYSICAL_PROJECT_ROWS']} "
          f"effective={vfs['EFFECTIVE_VFS_PROJECTS']} "
          f"shadowed_rows={vfs['SHADOWED_PROJECT_ROWS']} "
          f"unique_paths={vfs['UNIQUE_VFS_PROJECT_PATHS']} "
          f"shadowed_paths={vfs['SHADOWED_VFS_PATHS']} "
          f"content_conflicts={vfs['CONTENT_CONFLICTING_VFS_PATHS']}")
    if vfs["priority_tie_conflicts"]:
        C.log(f"  !! {len(vfs['priority_tie_conflicts'])} priority ties "
              f"broken deterministically")
    if vfs["unresolved_providers"]:
        C.log(f"  !! {len(vfs['unresolved_providers'])} providers with "
              f"UNKNOWN priority (cannot be declared winner)")
    for s in vfs["shadowed_paths"]:
        C.log(f"  shadowed: {s['vfs_path']}  <- winner L"
              f"{s['winning_provider_priority']} {s['winning_provider']} | "
              f"overridden: {'; '.join(s['shadowed_provider'])} | "
              f"content_conflict={s['content_conflict']}")

    # The raw per-.osp parse rows (07_bodyslide_slidersets.json) get the same
    # VFS annotation so the two stage-E files cannot disagree.
    vfs_by_row = {(p["MOD_ID"], p["OSP_PATH"]): p for p in projects}
    for d in osp_rows:
        p = vfs_by_row.get((d["mod"], d["rel"]))
        if not p:
            continue
        for k in ("vfs_path", "vfs_provider_count", "vfs_shadowed_path",
                  "winning_provider", "winning_provider_priority",
                  "winning_provider_sha256", "this_mod_priority",
                  "shadowed_provider", "shadowed_provider_count",
                  "effective", "vfs_status", "vfs_effective_reason",
                  "content_conflict", "PHYSICAL_PROJECT_ROWS",
                  "EFFECTIVE_VFS_PROJECTS", "SHADOWED_PROJECT_ROWS",
                  "UNIQUE_VFS_PROJECT_PATHS"):
            d[k] = p[k]

    C.write_json(os.path.join(C.DATA, "07_bodyslide_slidersets.json"), osp_rows)
    C.write_json(os.path.join(C.DATA, "07_bodyslide_shapedata.json"),
                 {"nif": nif_rows, "osd": osd_rows,
                  "errors": {"osp": osp_errors, "osd": osd_errors}})
    C.write_json(os.path.join(C.DATA, "07_bodyslide_groups.json"),
                 {"groups": groups, "presets": presets})
    C.write_json(os.path.join(C.DATA, "07_bodyslide_projects.json"), projects)
    C.write_json(os.path.join(C.DATA, "07_bodyslide_vfs_summary.json"), vfs)
    n_csv = C.write_csv(os.path.join(C.REPORTS, "07_BODYSLIDE_PROJECTS.csv"),
                        R07_COLS, [project_csv_row(p) for p in projects])
    C.log(f"wrote 07_BODYSLIDE_PROJECTS.csv rows={n_csv} "
          f"(07_bodyslide_projects.json stays a LIST for p00r_reports.py)")

    cc = Counter(p["body_candidate"] for p in projects)
    nc = Counter(p["needs_3ba_conversion"] for p in projects)
    C.log(f"projects={len(projects)}  body_candidate: "
          + ", ".join(f"{k}={v}" for k, v in cc.most_common()))
    C.log("needs_3ba_conversion: "
          + ", ".join(f"{k}={v}" for k, v in nc.most_common()))
    C.log(f"  sliders total={sum(p['n_sliders'] for p in projects)}  "
          f"zap={sum(len(p['zap_sliders']) for p in projects)}")
    C.log(f"  base_nif resolved="
          f"{sum(1 for p in projects if p['base_nif'] != UNKNOWN)}"
          f"/{len(projects)}  "
          f"output_nif={sum(1 for p in projects if p['output_nif'] != UNKNOWN)}")
    C.log("DONE stage E")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
