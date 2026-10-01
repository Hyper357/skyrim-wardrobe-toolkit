#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p00r_nif.py — STAGE C0: read-only NIF parse for the whole 09 scope.

Scope = every stage-A file whose cat is "nif" or "bodyslide_shapedata_nif".
Note that BodySlide ShapeData NIFs are their own category and are NOT counted
as plain "nif" -- both are parsed here because both are NIFs.

Parsing uses the vendored PyNifly at E:/SkyrimAE/Tools/pynifly (already proven
on this machine). Nifly is loaded READ-ONLY: NifFile.__init__ -> nifly.load().
Nothing in this script calls nifly.save/saveNif/skinShape/setTexture, i.e. no
code path that mutates the in-memory nif and could ever write back. The game
file itself is never opened by Python at all -- Nifly opens it read-only
internally -- and no file under mo2/, Data/ or any mod folder is ever written.

Parallelism: Nifly is a *single* native object shared per process, so threads
are unsafe. This script uses multiprocessing (spawn) with a small worker count
(4-6 by default) and automatically falls back to a single process if the pool
cannot start or a worker dies. Each worker process loads its own DLL instance.

Usage:  python tools\P00_RERUN\p00r_nif.py
        python tools\P00_RERUN\p00r_nif.py --workers 1
"""
from __future__ import annotations

import argparse
import gzip
import json
import multiprocessing as mp
import os
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p00r_common as C  # noqa: E402

PYNIFLY = r"E:\SkyrimAE\Tools\pynifly"
INDEX = os.path.join(C.DATA, "01_file_index.json.gz")

BONE_BUF = 1_000_000     # bone-name string buffer, per the brief
MAX_BONES = 80           # bone names stored per shape
MAX_NODES = 400          # node names stored per file
MAX_PARTS = 40

# Populated in each worker by _init_worker().
_NifFile = None
_nifly = None
_create_string_buffer = None


def _init_worker() -> None:
    global _NifFile, _nifly, _create_string_buffer
    if _NifFile is not None:
        return
    if PYNIFLY not in sys.path:
        sys.path.insert(0, PYNIFLY)
    from pyn.pynifly import NifFile, nifly, create_string_buffer
    _NifFile, _nifly, _create_string_buffer = NifFile, nifly, create_string_buffer


# --------------------------------------------------------------- classifier --
def classify_nif(cat: str, vpath: str) -> str:
    """Brief's ordered rules, first match wins."""
    v = vpath.lower()
    if cat == "bodyslide_shapedata_nif":
        return "SHAPEDATA"
    if cat == "physics_mesh":
        return "PHYSICS_MESH"
    if "/bodyphysics/" in v:
        return "PHYSICS_MESH"
    if "/bodyparts/" in v or "/partitions/" in v:
        return "PHYSICS_MESH"
    if v.startswith("meshes/actors/") and not ("character/female" in v
                                               or "character/male" in v):
        return "GAME_MESH"
    if "/static" in v or "/architecture" in v or "/clutter" in v:
        return "STATIC_MESH"
    if "/ground" in v or "/dirt" in v or "/rock" in v:
        return "GROUND_OBJECT"
    return "UNKNOWN"


# SMP / cloth detection -------------------------------------------------------
# A shape "reports an SMP/physics property" when the nif carries a cloth /
# spring / physics property block or a node named SMP*.
SMP_CLASS_HINTS = ("cloth", "smp", "hkp", "bhkphysics", "sphereffect")
SMP_FOLDER_NAMES = ("cloth", "springs")


def _node_blocknames(nf):
    out = []
    for n in nf.nodes.values():
        try:
            out.append((n.name, n.blockname))
        except Exception:
            try:
                out.append((n.name, type(n).__name__))
            except Exception:
                pass
    return out


# ------------------------------------------------------------------ parsing --
def parse_one(rec: dict) -> dict:
    vpath = rec["vpath"]
    row = {
        "NIF_ID": C.nif_id(vpath),
        "path": vpath,
        "source_mod": rec["mod"],
        "sha256": rec["sha256"],
        "size": rec["size"],
        "stage_a_cat": rec["cat"],
        "nif_class": classify_nif(rec["cat"], vpath),
        "shape_count": 0,
        "shapes": [],
        "nodes": [],
        "node_count": 0,
        "has_skin": False,
        "has_smp": False,
        "smp_reason": "",
        "parse_error": "",
    }

    folders = [p.lower() for p in vpath.split("/")[:-1]]
    path_smp = any(f in SMP_FOLDER_NAMES for f in folders)
    if path_smp:
        row["has_smp"] = True
        row["smp_reason"] = "path_folder"

    full = os.path.join(C.MODS_DIR, rec["mod"], rec["rel"].replace("/", os.sep))
    row["file_exists"] = os.path.isfile(full)

    nf = None
    try:
        nf = _NifFile(full)                      # nifly.load() -- read only
        shapes = nf.shapes
        row["shape_count"] = len(shapes)

        for sh in shapes:
            name = ""
            try:
                name = sh.name or ""
            except Exception:
                pass
            block = ""
            try:
                block = sh.blockname or ""
            except Exception:
                pass
            shader = ""
            try:
                shader = sh.shader_block_name or ""
            except Exception:
                pass

            # --- skin instance (read-only: skin_instance_name only reads a
            #     block name; sh.skin() is a MUTATOR and is never called) ----
            skin_block = ""
            try:
                skin_block = sh.skin_instance_name or ""
            except Exception:
                pass
            hsi = False
            try:
                hsi = bool(sh.has_skin_instance)
            except Exception:
                hsi = bool(skin_block)
            if hsi or skin_block:
                row["has_skin"] = True

            # --- alpha -------------------------------------------------------
            ap = None
            try:
                ap = sh.alpha_property
            except Exception:
                pass
            has_alpha = ap is not None
            alpha_val = None
            alpha_flags = None
            if has_alpha:
                try:
                    alpha_val = float(ap.properties.threshold)
                    alpha_flags = int(ap.properties.flags)
                except Exception:
                    pass

            # --- textures ----------------------------------------------------
            textures = {}
            try:
                textures = dict(sh.textures or {})
            except Exception:
                textures = {}
            envmap = "EnvMap" in textures

            # --- partitions --------------------------------------------------
            parts = []
            try:
                parts = [p.name for p in sh.partitions][:MAX_PARTS]
            except Exception:
                parts = []

            # --- bones (the brief's exact call) -----------------------------
            nbones, bones = 0, []
            try:
                buf = _create_string_buffer(BONE_BUF)
                n = _nifly.getShapeBoneNames(nf._handle, sh._handle, buf, BONE_BUF)
                bones = ([x for x in buf.value.decode("utf-8", "replace").split("\n")
                          if x] if n > 0 else [])
                nbones = n
            except Exception:
                nbones, bones = 0, []
            if nbones == 0 and not bones:
                try:
                    bn = sh.bone_names
                    bones = list(bn)
                    nbones = len(bones)
                except Exception:
                    pass

            row["shapes"].append({
                "name": name,
                "blockname": block,
                "shader": shader,
                "skin": skin_block,
                "has_skin_instance": hsi,
                "has_alpha": has_alpha,
                "alpha": alpha_val,
                "alpha_flags": alpha_flags,
                "envmap": envmap,
                "n_bones": nbones,
                "bones": bones[:MAX_BONES],
                "n_bones_truncated": nbones > MAX_BONES,
                "partitions": parts,
                "textures": textures,
            })

        # --- nodes ---------------------------------------------------------
        blocks = _node_blocknames(nf)
        names = [b[0] for b in blocks]
        row["nodes"] = names[:MAX_NODES]
        row["node_count"] = len(names)
        row["nodes_truncated"] = len(names) > MAX_NODES

        # --- SMP / physics ---------------------------------------------------
        if any(n.startswith("SMP") for n in names):
            row["has_smp"] = True
            row["smp_reason"] = (row["smp_reason"] + "|node_name"
                                 if row["smp_reason"] else "node_name")
        prop_hit = [b for _, b in blocks
                    if b and any(h in b.lower() for h in SMP_CLASS_HINTS)]
        if prop_hit:
            row["has_smp"] = True
            row["smp_reason"] = (row["smp_reason"] + "|block:" + ",".join(sorted(set(prop_hit))[:4])
                                 if row["smp_reason"]
                                 else "block:" + ",".join(sorted(set(prop_hit))[:4]))
        row["node_blocks"] = sorted({b for _, b in blocks if b})[:40]

        # A shape "reports an SMP/physics property" also when the shader
        # exposes parallax/physics-ish flags; keep the cheap version only.
    except Exception as ex:
        row["parse_error"] = repr(ex)[:200]
    finally:
        del nf
    return row


# ------------------------------------------------------------------ driver ---
def load_scope():
    with gzip.open(INDEX, "rt", encoding="utf-8") as fh:
        index = json.load(fh)
    return [r for r in index
            if r["cat"] in ("nif", "bodyslide_shapedata_nif")], len(index)


def _run_pool(records, workers):
    ctx = mp.get_context("spawn")
    out = []
    with ctx.Pool(processes=workers, initializer=_init_worker) as pool:
        for i, row in enumerate(pool.imap_unordered(parse_one, records, chunksize=8), 1):
            out.append(row)
            if i % 200 == 0 or i == len(records):
                C.log(f"  parsed {i:,}/{len(records):,}")
    return out


def _run_seq(records):
    _init_worker()
    out = []
    for i, rec in enumerate(records, 1):
        out.append(parse_one(rec))
        if i % 200 == 0 or i == len(records):
            C.log(f"  parsed {i:,}/{len(records):,}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=5,
                    help="process pool size (4-6 recommended, 1 = single process)")
    ap.add_argument("--force-seq", action="store_true")
    args = ap.parse_args()

    C.ensure_dirs()
    t0 = time.time()
    records, total_index = load_scope()
    C.log(f"stage C0: {len(records):,} NIF in scope "
          f"(of {total_index:,} indexed files)")

    rows = None
    if args.force_seq or args.workers <= 1:
        C.log("single process")
        rows = _run_seq(records)
    else:
        C.log(f"multiprocessing spawn pool, workers={args.workers}")
        try:
            rows = _run_pool(records, args.workers)
        except Exception as ex:
            C.log(f"!! pool failed ({ex!r}) -- falling back to a single process")
            rows = None
    if rows is None:
        rows = _run_seq(records)
    C.log(f"parse loop finished in {time.time()-t0:.1f}s")

    # stable order: by NIF_ID then source_mod
    rows.sort(key=lambda r: (r["NIF_ID"], r["source_mod"]))

    hist = Counter()
    for r in rows:
        for s in r["shapes"]:
            n = s["name"]
            if n:
                hist[n] += 1

    ok = [r for r in rows if not r["parse_error"]]
    bad = [r for r in rows if r["parse_error"]]
    missing = [r for r in rows if not r.get("file_exists")]

    out_nif = os.path.join(C.DATA, "08_nif_parsed.json.gz")
    C.write_json_gz(out_nif, rows)
    C.log(f"wrote {out_nif} ({len(rows):,} rows)")

    out_hist = os.path.join(C.DATA, "08_nif_shape_histogram.json")
    C.write_json(out_hist, dict(hist.most_common()))
    C.log(f"wrote {out_hist} ({len(hist):,} distinct shape names)")

    C.log("nif_class: " + ", ".join(
        f"{k}={v}" for k, v in Counter(r["nif_class"] for r in rows).most_common()))
    C.log(f"parse errors: {len(bad):,} / {len(rows):,}")
    for e in Counter(r["parse_error"] for r in bad).most_common(20):
        C.log(f"  ! x{e[1]} :: {e[0][:180]}")
    if missing:
        C.log(f"missing on disk: {len(missing)}")
        for m in missing[:10]:
            C.log(f"  ! {m['source_mod']} :: {m['path'][:90]}")
    C.log(f"has_skin: {sum(1 for r in rows if r['has_skin']):,}"
          f"   has_smp: {sum(1 for r in rows if r['has_smp']):,}")
    C.log(f"shapes total: {sum(r['shape_count'] for r in rows):,}"
          f"   nodes total: {sum(r['node_count'] for r in rows):,}")
    C.log("top-20 shape names: " +
          ", ".join(f"{k}={v}" for k, v in hist.most_common(20)))
    C.log(f"total time {time.time()-t0:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
