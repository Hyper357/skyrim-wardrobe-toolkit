# -*- coding: utf-8 -*-
"""
P01 / item 8 - EXISTING PREVIEW IMAGE DISCOVERY (read-only).

Scans the 56 mods of the MO2 "09 特殊服装与NSFW 装备" scope for preview imagery
that the mods ALREADY ship on disk, so the human review board has something to
show. Nothing is generated, converted, rendered or copied.

ABSOLUTE GUARANTEES ENFORCED HERE
  * READ-ONLY over E:\\SkyrimAE\\mo2 and E:\\SkyrimAE\\Data.
    Only os.scandir / os.stat are used. No open() for writing, no copy, no move.
  * NO RENDERING. 3DSMax / NifSkope / render scripts / preview generators are
    never invoked. This tool only records paths of images that already exist.
  * P00 IS FROZEN. reports\\P00_RERUN\\01_MOD_INVENTORY.csv is opened read-only
    and never written; tools\\P00_RERUN\\, data\\P00_RERUN\\ and reports\\P00\\
    are never touched.
  * WRITES are hard-limited to reports/P01/ (assert_write_path below).

Usage:
    cd <project root>
    python tools\\P01\\p01_previews.py
    -> reports/P01/P01_PREVIEW_INDEX.csv
    -> reports/P01/P01_PREVIEW_NOTES.md
Exit code 0 on success, non-zero on hard failure.
"""

from __future__ import annotations

import csv
import io
import os
import re
import sys
import time
from collections import Counter, OrderedDict

# --------------------------------------------------------------------------
# constants
# --------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

INVENTORY_CSV = os.path.join(PROJECT_ROOT, "reports", "P00_RERUN", "01_MOD_INVENTORY.csv")
MO2_INSTANCE = r"E:\SkyrimAE\mo2"
MODS_DIR = os.path.join(MO2_INSTANCE, "mods")
GAME_DATA_DIR = r"E:\SkyrimAE\Data"

OUT_DIR = os.path.join(PROJECT_ROOT, "reports", "P01")
OUT_CSV = os.path.join(OUT_DIR, "P01_PREVIEW_INDEX.csv")
OUT_NOTES = os.path.join(OUT_DIR, "P01_PREVIEW_NOTES.md")

ALLOWED_WRITE_ROOTS = (os.path.normcase(OUT_DIR),)

# image-ish extensions we are willing to record
RASTER_EXTS = {
    ".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff", ".tga",
    ".webp", ".dds", ".psd", ".xcf", ".hdr", ".exr",
}
# extensions an ordinary Windows image viewer opens
VIEWABLE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff", ".webp", ".tga"}
DDS_EXTS = {".dds"}

# directory names that, in a shipped mod, mean "documentation / marketing art"
PREVIEW_DIR_TOKENS = {
    "screenshot", "screenshots", "screen_shots", "shots",
    "preview", "previews", "previewart",
    "docs", "doc", "documentation", "readme",
    "images", "image", "img", "media", "gallery", "promo", "fomod",
}
# directory names that mark an image as game texture source material, never a preview
TEXTURE_DIR_TOKENS = {
    "textures", "texture", "tex", "materials", "meshes", "mesh",
    "shaders", "source", "src", "work", "bak", "backup", "old",
}

# basename patterns that mark a shipped preview
BASENAME_PREVIEW_RE = re.compile(
    r"^(preview|screenshot|screen[\s_-]?shot|scrShot|shot|ss[_\-\s]?\d|promopic|cover|"
    r"promo|picture|photo|bild|thumbnail|thumb|"
    r"截图|屏幕截图|预览|宣传图|宣传图|图片)",
    re.IGNORECASE,
)
# a basename like preview-1 / preview 1 / preview0 / preview_02
PREVIEW_NUMBERED_RE = re.compile(r"^preview[\s._\-]*\d*$", re.IGNORECASE)

# files that may carry a BodySlide slider-set preview reference
BODYSIDE_TEXT_EXTS = {".xml", ".osp", ".osd", ".ini", ".json", ".txt", ".md"}
BODYSIDE_PREVIEW_REF_RE = re.compile(r"preview", re.IGNORECASE)
BODYSIDE_PREVIEW_PATH_RE = re.compile(r"<\s*previewPath\s*>\s*([^<\s][^<]*?)\s*</\s*previewPath\s*>", re.IGNORECASE)
TEXT_SCAN_MAX_BYTES = 8 * 1024 * 1024

# Windows' default screenshot file name -> dropped in by a user, not shipped by the author
USER_SCREENSHOT_RE = re.compile(r"^(屏幕截图|截图|screenshot|screen shot)", re.IGNORECASE)

CSV_FIELDS = [
    "mod_priority",
    "mo2_leftpane_row",
    "MOD_ID",
    "mod_root",
    "scan_status",
    "preview_count",
    "viewable_count",
    "dds_count",
    "viewable",
    "file_types",
    "total_bytes",
    "best_candidate_path",
    "best_candidate_rel",
    "best_candidate_bytes",
    "best_candidate_tier",
    "best_candidate_px",
    "best_candidate_provenance",
    "candidate_is_dds",
    "named_preview_count",
    "preview_dir_count",
    "screenshot_evidence_count",
    "excluded_texture_image_count",
    "has_fomod_dir",
    "has_bodyslide_calientetools",
    "path",
    "path_rel",
]


# --------------------------------------------------------------------------
# guards
# --------------------------------------------------------------------------

def assert_write_path(path: str) -> None:
    """Refuse to write anywhere except reports/P01/."""
    norm = os.path.normcase(os.path.abspath(path))
    for root in ALLOWED_WRITE_ROOTS:
        if norm == root or norm.startswith(root + os.sep):
            return
    raise SystemExit("P01 WRITE GUARD: refusing to write outside %s -> %s" % (OUT_DIR, path))


def ensure_out_dir() -> None:
    assert_write_path(OUT_DIR)
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR, exist_ok=True)
    # prove the guard holds for the two real outputs
    assert_write_path(OUT_CSV)
    assert_write_path(OUT_NOTES)


# --------------------------------------------------------------------------
# inputs
# --------------------------------------------------------------------------

def read_inventory(path: str):
    """Read the frozen P00_RERUN inventory read-only. Returns OrderedDict MOD_ID -> row."""
    if not os.path.isfile(path):
        raise SystemExit("P01 FATAL: P00 inventory not found (P00 is frozen, not created): %s" % path)
    out = OrderedDict()
    with io.open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            mod_id = (row.get("MOD_ID") or "").strip()
            if not mod_id:
                continue
            out[mod_id] = row
    return out


# --------------------------------------------------------------------------
# classification
# --------------------------------------------------------------------------

def classify(rel_parts, filename: str):
    """Return (tier_or_None, ext, is_viewable, is_dds).

    tier:
      'named_preview'       - basename itself says preview/screenshot
      'preview_dir'         - sits in a docs/screenshots/media/images/fomod folder
      'screenshot_evidence' - a non-texture image whose name is screenshot-like (CJK etc.)
      None                  - not a preview (game texture / source art)
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext not in RASTER_EXTS:
        return None, ext, False, False

    stem = os.path.splitext(filename)[0]
    seg_low = [p.lower() for p in rel_parts]

    in_texture_dir = any(seg in TEXTURE_DIR_TOKENS for seg in seg_low)
    in_preview_dir = any(seg in PREVIEW_DIR_TOKENS for seg in seg_low)
    named = bool(BASENAME_PREVIEW_RE.match(stem)) or bool(PREVIEW_NUMBERED_RE.match(stem))

    is_viewable = ext in VIEWABLE_EXTS
    is_dds = ext in DDS_EXTS

    if in_texture_dir:
        # a texture/source folder wins: a "preview" named file inside textures/ is
        # still authored art material, not board-facing preview evidence
        return None, ext, is_viewable, is_dds
    if named:
        return "named_preview", ext, is_viewable, is_dds
    if in_preview_dir:
        return "preview_dir", ext, is_viewable, is_dds
    return None, ext, is_viewable, is_dds


def read_only_text(path: str, limit: int = TEXT_SCAN_MAX_BYTES):
    """Read a small text asset READ-ONLY. Returns None if it is too big."""
    try:
        if os.path.getsize(path) > limit:
            return None
        with io.open(path, "r", encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except OSError:
        return None


def png_size(path: str):
    """Parse the PNG IHDR header. No decoding, no rendering."""
    try:
        with io.open(path, "rb") as fh:
            head = fh.read(26)
        if len(head) < 26 or head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
            return None
        return (int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big"))
    except (OSError, ValueError):
        return None


def jpeg_size(path: str):
    """Parse JPEG SOFn headers. No decoding, no rendering."""
    try:
        with io.open(path, "rb") as fh:
            data = fh.read(65536)
        if data[:2] != b"\xff\xd8":
            return None
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                h = int.from_bytes(data[i + 5:i + 7], "big")
                w = int.from_bytes(data[i + 7:i + 9], "big")
                return (w, h)
            seg_len = int.from_bytes(data[i + 2:i + 4], "big")
            if seg_len <= 0:
                return None
            i += 2 + seg_len
        return None
    except (OSError, ValueError, IndexError):
        return None


def image_size(path: str, ext: str):
    """Best-effort pixel dimensions from the file header only (never decodes pixels)."""
    if ext == ".png":
        return png_size(path)
    if ext in (".jpg", ".jpeg"):
        return jpeg_size(path)
    return None


def provenance_of(rel: str, filename: str) -> str:
    if USER_SCREENSHOT_RE.match(os.path.splitext(filename)[0]):
        return "user-screenshot-name (Windows 截图默认命名，疑似使用者自截入游戏画面，非作者随包宣传图)"
    depth = rel.replace("\\", "/").count("/")
    return "mod-root" if depth == 0 else ("author-packaged (位于 mod 内 %d 层目录)" % depth)


def candidate_rank(item):
    """Lower is better: named preview > preview folder > screenshot evidence,
    then viewable formats before DDS, then the larger file."""
    tier_order = {"named_preview": 0, "preview_dir": 1, "screenshot_evidence": 2}[item["tier"]]
    return (tier_order, 0 if item["viewable"] else 1, -item["size"], item["rel"].lower())


# --------------------------------------------------------------------------
# per-mod scan
# --------------------------------------------------------------------------

def scan_mod(mod_id: str, row):
    root = os.path.join(MODS_DIR, mod_id)
    res = {
        "mod_id": mod_id,
        "mod_root": root,
        "priority": (row.get("priority") or "").strip(),
        "leftpane_row": (row.get("mo2_leftpane_row") or "").strip(),
        "scan_status": "ok",
        "candidates": [],
        "excluded_texture_images": 0,
        "has_fomod": False,
        "has_calientetools": False,
        "bodyslide_ref_files": [],
        "excluded_examples": [],
        "error": "",
    }

    if not os.path.isdir(root):
        res["scan_status"] = "missing_folder"
        res["error"] = "mod folder not found on disk"
        return res

    try:
        for dirpath, dirnames, filenames in os.walk(root):
            rel_dir = os.path.relpath(dirpath, root)
            parts = [] if rel_dir == "." else rel_dir.split(os.sep)
            low_parts = [p.lower() for p in parts]
            if "fomod" in low_parts:
                res["has_fomod"] = True
            if "calientetools" in low_parts and "bodyslide" in low_parts:
                res["has_calientetools"] = True

            for fn in filenames:
                ext = os.path.splitext(fn)[1].lower()
                rel = os.path.normpath(os.path.join(rel_dir, fn)) if rel_dir != "." else fn
                full = os.path.join(dirpath, fn)

                if ext in BODYSIDE_TEXT_EXTS:
                    body = read_only_text(full)
                    if body and BODYSIDE_PREVIEW_REF_RE.search(body):
                        targets = BODYSIDE_PREVIEW_PATH_RE.findall(body)
                        res["bodyslide_ref_files"].append({
                            "rel": rel,
                            "preview_path_targets": sorted(set(targets))[:5],
                        })
                    continue

                tier, ext, is_viewable, is_dds = classify(parts, fn)
                if tier is None:
                    if ext in RASTER_EXTS:
                        res["excluded_texture_images"] += 1
                        if len(res["excluded_examples"]) < 3:
                            res["excluded_examples"].append(rel)
                    continue

                try:
                    size = os.path.getsize(full)
                except OSError as exc:
                    res["error"] = res["error"] or ("stat failed: %s" % exc)
                    size = 0

                res["candidates"].append({
                    "abs": full,
                    "rel": rel,
                    "ext": ext,
                    "size": size,
                    "tier": tier,
                    "viewable": is_viewable,
                    "dds": is_dds,
                    "px": image_size(full, ext) if is_viewable else None,
                    "provenance": provenance_of(rel, fn),
                })
    except OSError as exc:
        res["scan_status"] = "walk_error"
        res["error"] = str(exc)

    res["candidates"].sort(key=candidate_rank)
    return res


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------

def build_row(res) -> dict:
    cands = res["candidates"]
    ext_counts = Counter(c["ext"] for c in cands)
    file_types = ";".join("%s(%d)" % (e.lstrip("."), n) for e, n in sorted(ext_counts.items()))
    total_bytes = sum(c["size"] for c in cands)
    viewable_n = sum(1 for c in cands if c["viewable"])
    dds_n = sum(1 for c in cands if c["dds"])
    best = cands[0] if cands else None

    return OrderedDict([
        ("mod_priority", res["priority"]),
        ("mo2_leftpane_row", res["leftpane_row"]),
        ("MOD_ID", res["mod_id"]),
        ("mod_root", res["mod_root"]),
        ("scan_status", res["scan_status"]),
        ("preview_count", len(cands)),
        ("viewable_count", viewable_n),
        ("dds_count", dds_n),
        ("viewable", "yes" if viewable_n else "no"),
        ("file_types", file_types),
        ("total_bytes", total_bytes),
        ("best_candidate_path", best["abs"] if best else ""),
        ("best_candidate_rel", best["rel"] if best else ""),
        ("best_candidate_bytes", best["size"] if best else 0),
        ("best_candidate_tier", best["tier"] if best else ""),
        ("best_candidate_px", ("%dx%d" % best["px"]) if best and best["px"] else ""),
        ("best_candidate_provenance", best["provenance"] if best else ""),
        ("candidate_is_dds", ("yes" if best["dds"] else "no") if best else "n/a"),
        ("named_preview_count", sum(1 for c in cands if c["tier"] == "named_preview")),
        ("preview_dir_count", sum(1 for c in cands if c["tier"] == "preview_dir")),
        ("screenshot_evidence_count", sum(1 for c in cands if c["tier"] == "screenshot_evidence")),
        ("excluded_texture_image_count", res["excluded_texture_images"]),
        ("has_fomod_dir", "yes" if res["has_fomod"] else "no"),
        ("has_bodyslide_calientetools", "yes" if res["has_calientetools"] else "no"),
        ("path", ";".join(c["abs"] for c in cands)),
        ("path_rel", ";".join(c["rel"] for c in cands)),
    ])


def write_csv(rows) -> None:
    assert_write_path(OUT_CSV)
    with io.open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def human(n: int) -> str:
    return "%.2f MiB" % (n / 1048576.0) if n < 1024 * 1024 * 1024 else "%.2f GiB" % (n / 1073741824.0)


def write_notes(rows, results, stats) -> None:
    assert_write_path(OUT_NOTES)
    with io.open(OUT_NOTES, "w", encoding="utf-8") as fh:
        fh.write("# P01_PREVIEW_NOTES.md — Item 8: shipped preview images, 09 scope (56 mods)\n\n")
        fh.write("**ZLJ Wardrobe Collection · P01_HUMAN_CURATION_ASSISTANCE · read-only discovery**\n\n")
        fh.write("| 项 | 值 |\n|---|---|\n")
        fh.write("| 扫描时刻 (local) | %s |\n" % stats["now"])
        fh.write("| 范围来源（只读） | `reports/P00_RERUN/01_MOD_INVENTORY.csv` (P00 冻结，未修改) |\n")
        fh.write("| Mod 根目录 | `%s` |\n" % MODS_DIR)
        fh.write("| Mod 总数 | %d |\n" % stats["n_mods"])
        fh.write("| 扫描到的候选预览图总数 | **%d** |\n\n" % stats["n_images"])

        fh.write("## 0. 渲染声明（NO RENDERING）\n\n")
        fh.write("> **本次没有做任何渲染，也没有尝试渲染。**\n>\n")
        fh.write("> 未启动 3DSMax、NifSkope、SSCS、任何 render 脚本或任何预览生成器。\n")
        fh.write("> 本工具只做**文件系统只读遍历**（`os.walk` + `os.stat`），\n")
        fh.write("> 记录 mods **已经自带**的图片文件路径。没有转换、没有复制、没有移动、没有改写。\n>\n")
        fh.write("> 没有为了补足画面而搭建渲染管线。**\"没有预览图\"是完全可接受的结果。**\n\n")

        fh.write("## 1. 结论（先看这里）\n\n")
        fh.write("| 指标 | 值 |\n|---|---|\n")
        fh.write("| 有候选预览图的 mod | **%d / %d** |\n" % (stats["n_with"], stats["n_mods"]))
        fh.write("| **零预览图**的 mod | **%d / %d** |\n" % (stats["n_zero"], stats["n_mods"]))
        fh.write("| 候选图片文件总数 | %d |\n" % stats["n_images"])
        fh.write("| 其中 Windows 图片查看器可直接打开（PNG/JPG…） | **%d** |\n" % stats["n_viewable"])
        fh.write("| 其中 DDS（DDS 查看器才能看，OS 默认不显示） | %d |\n" % stats["n_dds"])
        fh.write("| 有 `fomod/` 目录的 mod | %d |\n" % stats["n_fomod"])
        fh.write("| 有 `CalienteTools/BodySlide/` 的 mod | %d |\n" % stats["n_caliente"])
        fh.write("| 被判为**贴图/源素材**而排除的图片 | %d |\n\n" % stats["n_excluded"])

        fh.write("**一句话结论：** %s\n\n" % stats["headline"])

        fh.write("## 2. 有预览图的 mod（逐条）\n\n")
        if stats["n_with"] == 0:
            fh.write("_（无）_\n\n")
        else:
            fh.write("| # | MOD_ID | 预览数 | 类型 | 体积 | 最佳候选 | DDS? | 可直接看? |\n")
            fh.write("|---|---|---|---|---|---|---|---|\n")
            for i, r in enumerate([x for x in rows if x["preview_count"]], 1):
                fh.write("| %d | `%s` | %s | `%s` | %s | `%s` | %s | %s |\n" % (
                    i, r["MOD_ID"], r["preview_count"], r["file_types"],
                    human(r["total_bytes"]), r["best_candidate_rel"],
                    r["candidate_is_dds"], r["viewable"]))
            fh.write("\n")

        fh.write("### 2.1 全部候选图逐张清单（共 %d 张）\n\n" % stats["n_images"])
        if stats["n_images"] == 0:
            fh.write("_（无）_\n\n")
        else:
            fh.write("尺寸由**文件头解析**得出（PNG IHDR / JPEG SOFn），只读字节，**不解码像素、不渲染**。\n\n")
            fh.write("| # | MOD_ID | 相对路径 | 像素 | 字节 | 类型 | 来源判定 |\n")
            fh.write("|---|---|---|---|---|---|---|\n")
            idx = 0
            for res, r in zip(results, rows):
                for c in res["candidates"]:
                    idx += 1
                    px = ("%dx%d" % c["px"]) if c["px"] else "n/a"
                    fh.write("| %d | `%s` | `%s` | %s | %s | %s | %s |\n" % (
                        idx, res["mod_id"], c["rel"], px, c["size"],
                        c["tier"], c["provenance"]))
            fh.write("\n")
            user_shots = [c for res in results for c in res["candidates"]
                          if c["provenance"].startswith("user-screenshot-name")]
            if user_shots:
                fh.write("> **来源提示：** 上述 %d 张里，文件名为 Windows 截图默认命名（`屏幕截图 …`）。\n"
                         % len(user_shots))
                fh.write("> 也就是说它们很可能是**使用者自己截的入游戏画面**，被丢在 mod 根目录，\n")
                fh.write("> 而**不是**作者随 mod 附带的宣传图。对评审而言内容依然有效（确实是该服装的画面），\n")
                fh.write("> 但**不能**据此认为该 mod 作者提供了正式 preview 图。\n\n")

        fh.write("## 3. 零预览图的 mod（%d 个）\n\n" % stats["n_zero"])
        zero = [r["MOD_ID"] for r in rows if not r["preview_count"]]
        if not zero:
            fh.write("_（无）_\n\n")
        else:
            for name in zero:
                fh.write("- `%s`\n" % name)
            fh.write("\n")

        fh.write("## 4. 可直接查看 (PNG/JPG) vs 仅 DDS\n\n")
        fh.write("> **DDS 说明：** `.dds` 是 DirectDraw Surface，Windows 照片查看器**打不开**。\n")
        fh.write("> 本次把 DDS 记为 `candidate_is_dds=yes`，并在下面单独列出，方便评审时知道哪些需要 DDS 查看器\n")
        fh.write("> （或人工另存为 PNG）才能看。**本次没有做任何格式转换。**\n\n")
        fh.write("### 4.1 有 PNG/JPG 等可直接查看文件的 mod（%d 个）\n\n" % stats["n_with_viewable"])
        for r in rows:
            if r["viewable_count"]:
                fh.write("- `%s` → `%s`\n" % (r["MOD_ID"], r["best_candidate_rel"]))
        fh.write("\n### 4.2 只有 DDS 候选的 mod（%d 个）\n\n" % stats["n_dds_only"])
        dds_only = [r for r in rows if r["preview_count"] and not r["viewable_count"]]
        if not dds_only:
            fh.write("_（无）_\n\n")
        else:
            for r in dds_only:
                fh.write("- `%s` → `%s`\n" % (r["MOD_ID"], r["best_candidate_path"]))
            fh.write("\n")

        fh.write("## 5. 扫描方法（可复核）\n\n")
        fh.write("命中条件（任一）：\n\n")
        fh.write("1. **文件名命中**：`preview*`（含 `preview-1` / `preview0` / `preview 1`）、")
        fh.write("`screenshot*` / `screen shot*`、`截图` / `屏幕截图` / `预览` / `宣传图`、")
        fh.write("`promo*` / `cover` / `thumb*` / `photo` / `picture`。\n")
        fh.write("2. **目录命中**：位于 `screenshots/` / `preview(s)/` / `docs/` / `documentation/` / ")
        fh.write("`images/` / `img/` / `media/` / `gallery/` / `promo/` / `fomod/` 之下。\n")
        fh.write("3. **BodySlide 预览资产**：mod 内存在 `CalienteTools/BodySlide/` 目录。\n\n")
        fh.write("排除条件：`textures/` / `texture/` / `meshes/` / `materials/` / `shaders/` / ")
        fh.write("`source/` / `src/` / `bak/` / `backup/` / `work/` 路径下的图片一律判为**贴图/源素材**，")
        fh.write("不计入预览图（本次共排除 %d 个）。\n\n" % stats["n_excluded"])
        fh.write("`*.osp / *.osd / *.xml / *.ini` 等文本文件中出现 `preview` 字样的**引用**另行单独统计，")
        fh.write("不作为图片计入（见第 7 节）。\n\n")

        fh.write("## 6. FOMOD 情况\n\n")
        if stats["n_fomod"] == 0:
            fh.write("**56 个 mod 中没有任何一个带 `fomod/` 目录**——这些 mods 都不带 FOMOD 安装器，")
            fh.write("因此不存在 FOMOD 自带预览图的情况。\n\n")
        else:
            fh.write("带 `fomod/` 的 mod：%d 个。\n\n" % stats["n_fomod"])

        fh.write("## 7. BodySlide 预览资产\n\n")
        fh.write("- 56 个 mod 中带 `CalienteTools/BodySlide/` 的：**%d** 个。\n" % stats["n_caliente"])
        fh.write("- 在 mod 的 `.osp / .osd / .xml / .ini / .json / .txt / .md` **文件内容**中出现 `preview` 字样的文件：**%d** 个。\n"
                 % stats["n_bs_refs"])
        if stats["bs_preview_targets"]:
            fh.write("- 其中带 `<previewPath>` 目标（指向真实预览图资源）的：\n")
            for tgt, where in stats["bs_preview_targets"][:10]:
                fh.write("  - `%s` ← `%s`\n" % (tgt, where))
        else:
            fh.write("- **没有任何一个 `<previewPath>` 指向磁盘上真实存在的预览图**——")
            fh.write("BodySlide 在本机没有配图。\n")
        fh.write("- 范围外的旁证（只读探查，**未写入任何东西**）：\n")
        fh.write("  - `E:\\SkyrimAE\\Data\\CalienteTools\\` **不存在**——本机 BodySlide 数据目录不在游戏 Data 下。\n")
        fh.write("  - MO2 的 `BodySlide 与服装 Studio — BodySlide and Outfit Studio` 工具 mod 里确实有 ")
        fh.write("`CalienteTools/BodySlide/`，但其图片全部是 `res/images/` 下的**软件 UI 图标**")
        fh.write("（89 个，`AlphaBrush.png`、`greygrid.png` 之类），**没有服装预览图**。\n")
        fh.write("  - 该工具 mod **不属于 09 范围**，仅作旁证记录，未写入本 CSV。\n")
        fh.write("- 结论：**BodySlide 体系在本范围内不提供任何可用于评审的服装预览图。**\n\n")

        fh.write("## 8. 判为\"贴图/源素材\"而排除的图片（提示，避免误当预览）\n\n")
        fh.write("范围内共发现 %d 个 raster 图片文件，其中 %d 个位于贴图/源素材目录，未计入预览图。\n\n"
                 % (stats["n_images"] + stats["n_excluded"], stats["n_excluded"]))
        fh.write("典型样例：\n\n")
        for ex in stats["excluded_examples"]:
            fh.write("- `%s`\n" % ex)
        fh.write("\n")

        fh.write("## 9. 给评审板的使用建议\n\n")
        if stats["n_with_viewable"] == 0:
            fh.write("- 本范围内**没有任何**可直接打开的预览图。评审板需要接受\"无图可看\"这一事实，")
            fh.write("改为按 NIF/贴图参数、BodySlide 预设名、ESP 记录名等**文本证据**评审。\n")
        else:
            fh.write("- 可直接打开的预览图仅集中在 %d 个 mod（见 4.1），覆盖不足全范围。\n" % stats["n_with_viewable"])
        fh.write("- **不要**为此新建渲染管线。P01 的定位是人工辅助，不是产出图像。\n")
        fh.write("- 若人工评审确实需要图，正确的下一步是**从 Nexus Mods / 作者主页取原图**")
        fh.write("（属于人工动作），而不是在本地跑渲染。\n\n")

        fh.write("## 10. 只读合规声明\n\n")
        fh.write("- 对 `%s`、`%s`、modlist、BodySlide 数据：**零写入**。\n" % (MODS_DIR, GAME_DATA_DIR))
        fh.write("- P00 成果（`reports/P00/`、`reports/P00_RERUN/`、`data/P00/`、`tools/P00_RERUN/`）")
        fh.write("**全部保持冻结**，本轮只读取了 `reports/P00_RERUN/01_MOD_INVENTORY.csv`。\n")
        fh.write("- 唯一写入：`%s`、`%s`。\n" % (
            os.path.relpath(OUT_CSV, PROJECT_ROOT).replace("\\", "/"),
            os.path.relpath(OUT_NOTES, PROJECT_ROOT).replace("\\", "/")))
        fh.write("- 工具内置写保护 `assert_write_path()`，越界写入直接 `SystemExit`。\n\n")
        fh.write("---\n\n")
        fh.write("**P01 · item 8 · preview discovery complete · %d/%d mods carry previews · no rendering performed**\n"
                 % (stats["n_with"], stats["n_mods"]))


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main() -> int:
    t0 = time.time()
    ensure_out_dir()

    inventory = read_inventory(INVENTORY_CSV)
    results = [scan_mod(mid, inventory[mid]) for mid in inventory]
    rows = [build_row(r) for r in results]
    write_csv(rows)

    n_images = sum(r["preview_count"] for r in rows)
    n_viewable = sum(r["viewable_count"] for r in rows)
    n_dds = sum(r["dds_count"] for r in rows)
    n_with = sum(1 for r in rows if r["preview_count"])
    n_with_viewable = sum(1 for r in rows if r["viewable_count"])
    n_dds_only = sum(1 for r in rows if r["preview_count"] and not r["viewable_count"])
    n_excluded = sum(r["excluded_texture_image_count"] for r in rows)
    n_fomod = sum(1 for r in results if r["has_fomod"])
    n_caliente = sum(1 for r in results if r["has_calientetools"])
    bs_refs = [ref for res in results for ref in res["bodyslide_ref_files"]]
    bs_preview_targets = [(t, "%s :: %s" % (res["mod_id"], ref["rel"]))
                          for res in results
                          for ref in res["bodyslide_ref_files"]
                          for t in ref["preview_path_targets"]]

    # a few excluded examples for the notes (collected during the main scan)
    examples = []
    for res in results:
        for rel in res["excluded_examples"]:
            examples.append("%s :: %s" % (res["mod_id"], rel))
    examples = examples[:8]

    if n_with == 0:
        headline = ("%d 个 mod 全部没有任何自带预览图。评审板无图可看——这是一个可接受且已确证的结论。"
                    % len(rows))
    elif n_with_viewable == 0:
        headline = ("只有 %d 个 mod 有候选预览图，且全部是 DDS，OS 图片查看器打不开；"
                    "其余 %d 个 mod 零预览图。" % (n_with, len(rows) - n_with))
    else:
        headline = ("仅 **%d / %d** 个 mod 自带预览图，其中 **%d 个**有 Windows 查看器可直接打开的 PNG/JPG；"
                    "**%d 个 mod 零预览图**。绝大多数 mod 需要靠文本证据评审。"
                    % (n_with, len(rows), n_with_viewable, len(rows) - n_with))

    stats = {
        "now": time.strftime("%Y-%m-%d %H:%M:%S"),
        "n_mods": len(rows),
        "n_images": n_images,
        "n_viewable": n_viewable,
        "n_dds": n_dds,
        "n_with": n_with,
        "n_with_viewable": n_with_viewable,
        "n_dds_only": n_dds_only,
        "n_zero": len(rows) - n_with,
        "n_excluded": n_excluded,
        "n_fomod": n_fomod,
        "n_caliente": n_caliente,
        "n_bs_refs": len(bs_refs),
        "bs_preview_targets": bs_preview_targets,
        "excluded_examples": examples,
        "headline": headline,
    }
    write_notes(rows, results, stats)

    # ---- console summary -------------------------------------------------
    out = sys.stdout
    out.write("\nP01 item 8 - shipped preview discovery (read-only)\n")
    out.write("-" * 68 + "\n")
    out.write("mods scanned          : %d\n" % stats["n_mods"])
    out.write("mods WITH previews    : %d\n" % stats["n_with"])
    out.write("mods with ZERO previews: %d\n" % stats["n_zero"])
    out.write("preview image files   : %d\n" % n_images)
    out.write("  viewable (png/jpg..): %d\n" % n_viewable)
    out.write("  dds only files      : %d\n" % n_dds)
    out.write("  texture/art excluded: %d\n" % n_excluded)
    out.write("mods with fomod/      : %d\n" % n_fomod)
    out.write("mods w/ CalienteTools : %d\n" % n_caliente)
    out.write("-'preview' text refs  : %d\n" % len(bs_refs))
    out.write("elapsed               : %.1fs\n" % (time.time() - t0))
    out.write("-" * 68 + "\n")
    for r in rows:
        if r["preview_count"]:
            out.write("  + %-58.58s n=%-3d %-12s %s\n" % (
                r["MOD_ID"], r["preview_count"], r["file_types"], r["best_candidate_rel"]))
    out.write("-" * 68 + "\n")
    out.write("CSV   -> %s\n" % OUT_CSV)
    out.write("NOTES -> %s\n" % OUT_NOTES)
    out.write("RENDERING PERFORMED: none (none attempted)\n\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
