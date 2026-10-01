#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p01_review_ui.py — build the standalone P01 Wardrobe Review page.

Emits a SINGLE self-contained HTML file: data, styles, scripts and the
handful of preview images are all inlined as base64, so it opens by double
click with no Node, no Python, no server and no network.

READ-ONLY with respect to everything else. It reads the frozen P01/P00
outputs and COPIES preview images (never moves or modifies them), and writes
only into reports/P01/review_ui/.
"""
from __future__ import annotations

import base64
import csv
import json
import mimetypes
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKT = os.path.dirname(os.path.dirname(HERE))
P01 = os.path.join(PKT, "reports", "P01")
OUT = os.path.join(P01, "review_ui")
sys.path.insert(0, os.path.join(PKT, "tools", "P00_RERUN"))
import p00r_common as C  # noqa: E402

C.allow_extra_write_root(OUT)

TEMPLATE = os.path.join(HERE, "review_template.html")
HTML = os.path.join(OUT, "P01_WARDROBE_REVIEW.html")
BAT = os.path.join(OUT, "OPEN_P01_REVIEW.bat")
README = os.path.join(OUT, "README.md")
ASSETS = os.path.join(OUT, "assets", "previews")

BAT_TEXT = """@echo off
rem Opens the P01 Wardrobe Review in your default browser.
rem Starts no server, changes no environment, and touches no game asset.
start "" "%~dp0P01_WARDROBE_REVIEW.html"
"""

README_TEXT = """# P01 Wardrobe Review — 使用说明

这是一个**单文件、离线**的人工筛选工具。它只读取已冻结的 P00 / P01 数据，
不修改任何 Skyrim / MO2 资产。

## 怎么用

1. 双击 `OPEN_P01_REVIEW.bat`
   （或直接双击 `P01_WARDROBE_REVIEW.html`）
2. 浏览 56 套 Outfit，点 **KEEP** / **PARTIAL** / **DROP**
   想取消就点 **UNDECIDED**。同一套永远只有一个 decision。
3. 点 **PARTIAL** 时会自动展开该套的 Visual Parts，
   逐个勾 **KEEP**（保留零件）或 **DROP**（丢弃零件）。
   默认全部 UNDECIDED，**不必一次勾完**。
4. **Notes** 随手写，例如「只要靴子和面罩」「XP 核心必留」「以后转 UBE」。
   Priority（S/A/B/C）是次要信息，留空也行。
5. 随时点 **Export Backup** 存一份完整进度。
6. 全部完成后点 **Export CSV** 和 **Export JSON**。
7. 把导出的三个文件交回项目：

   - `P01_USER_DECISIONS.csv`
   - `P01_USER_PART_DECISIONS.csv`
   - `P01_USER_DECISIONS.json`
     （可选）`P01_WARDROBE_REVIEW_STATE.json`

## 顺手的几个功能

- **▶ NEXT UNDECIDED** — 滚到下一套还没决定的，形成
  「看衣服 → 点决定 → NEXT」的快速流程
- 顶部筛选：Decision / Body / Cost / UBE / Material + 搜索框
- 排序：原始顺序 / 名称 / 体积 / Cost / UBE / Decision
- **Undo Last Decision**、**Reset Current Outfit**、**RESET ALL**（需两次确认）
- 关闭页面会**自动暂存**到浏览器 localStorage，但 localStorage 在
  `file://` 下不保证可靠，所以**务必用 Export Backup 落盘**

## 想换个时间继续

点 **Import Previous State** 选回 `P01_WARDROBE_REVIEW_STATE.json` 即可恢复
KEEP / PARTIAL / DROP、Priority、Notes 和所有零件勾选。导入时会校验
`outfit_id`，不匹配的行会被忽略并提示。

## 说明

- 预览图：56 套里只有 1 套带图（共 3 张 PNG），已内嵌进 HTML。
  其余显示 `No Preview Available`。这是真实情况，**没有做任何渲染**。
- 页面只做记录，不删除、不合并、不转换任何东西。
"""


def rd(p):
    with open(p, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    os.makedirs(OUT, exist_ok=True)
    outfits = rd(os.path.join(P01, "P01_OUTFIT_REVIEW.csv"))
    vps = rd(os.path.join(P01, "P01_VISUAL_PARTS.csv"))
    previews = rd(os.path.join(P01, "P01_PREVIEW_INDEX.csv"))

    # ---------------------------------------------------- preview images --
    # map MOD_ID -> inline data URI list. The source files are only READ;
    # a copy is written into assets/previews for reference, the originals
    # are never touched.
    by_mod = {}
    for r in previews:
        n = int(r.get("preview_count") or 0)
        if n <= 0:
            continue
        paths = [x.strip() for x in (r.get("path") or "").split(";") if x.strip()]
        imgs = []
        for p in paths:
            if not os.path.isfile(p):
                continue
            if os.path.splitext(p)[1].lower() in (".dds", ".dng"):
                continue          # DDS is a texture, never a preview photo
            try:
                mime = mimetypes.guess_type(p)[0] or "image/png"
                with open(p, "rb") as fh:
                    b = base64.b64encode(fh.read()).decode("ascii")
                imgs.append("data:%s;base64,%s" % (mime, b))
            except OSError:
                continue
        if imgs:
            by_mod[r["MOD_ID"]] = imgs
            os.makedirs(ASSETS, exist_ok=True)
            for p in paths:
                if os.path.isfile(p):
                    shutil.copy2(p, os.path.join(ASSETS,
                                                 os.path.basename(p)))

    # ------------------------------------------------------- assemble ----
    rows = []
    for i, o in enumerate(outfits):
        ps = [v for v in vps if v["MOD_ID"] == o.get("source_mods")]
        if not ps:
            # fall back to matching on the outfit id carried by the part
            ps = [v for v in vps if v["source_outfit"] == o["OUTFIT_ID"]]
        # source_mods is a ";"-joined list (a patch/rework outfit rolls in its
        # base), while the preview index is keyed per single mod -- so try
        # each member, not the joined string.
        preview = None
        for m in (o.get("source_mods") or "").split(";"):
            m = m.strip()
            if m and m in by_mod:
                preview = by_mod[m][0]
                break
        rows.append({
            "id": o["OUTFIT_ID"],
            "display_name": o.get("display_name") or o["OUTFIT_ID"],
            "source_mods": o.get("source_mods", ""),
            "plugins": o.get("plugins", ""),
            "current_size_bytes": o.get("current_size_bytes", ""),
            "effective_asset_size_bytes": o.get("effective_asset_size_bytes", ""),
            "n_ARMO": o.get("n_ARMO", ""),
            "n_ARMA": o.get("n_ARMA", ""),
            "n_wearable_NIF": o.get("n_wearable_NIF", ""),
            "n_texture": o.get("n_texture", ""),
            "n_effective_bodyslide_projects":
                o.get("n_effective_bodyslide_projects", ""),
            "body_type": o.get("body_type", "UNKNOWN"),
            "physics": o.get("physics", "UNKNOWN"),
            "material_candidates": o.get("material_candidates", "UNKNOWN"),
            "pbr_state": o.get("pbr_state", ""),
            "cross_mod_dependency_count": o.get("cross_mod_dependency_count", "0"),
            "unresolved_dependency_count": o.get("unresolved_dependency_count", "0"),
            "merge_risk": o.get("merge_risk", ""),
            "duplicate_asset_bytes": o.get("duplicate_asset_bytes", "0"),
            "role": o.get("role", ""),
            "review_hint": o.get("review_hint", ""),
            "preview": preview,
            "parts": [{
                "id": v["VISUAL_PART_ID"],
                "name": v["display_name"],
                "cat": v["part_category"],
                "slot": v["slots"],
                "body": v["body_type"],
                "phys": v["physics"],
                "ube": v["UBE_CONVERSION_CLASS"],
                "cost": v["technical_cost"],
            } for v in ps],
        })
        # Cost shown on the card = the worst cost among the outfit's visual
        # parts, matching reports/P01/P01_HUMAN_REVIEW.md. An outfit with no
        # ARMO in scope has no parts, and that is a real state, not a gap.
        costs = [p["cost"] for p in rows[-1]["parts"]]
        rows[-1]["technical_cost"] = (
            max(costs, key=lambda x: {"LOW": 0, "MEDIUM": 1,
                                      "HIGH": 2}.get(x, 1))
            if costs else "N/A（无 ARMO 记录）")
        rows[-1]["n_shadowed_projects"] = ""

    tpl = open(TEMPLATE, encoding="utf-8").read()
    payload = json.dumps({"outfits": rows}, ensure_ascii=False,
                         separators=(",", ":"))
    html = tpl.replace("/*__DATA__*/null", payload)
    if "/*__DATA__*/" in html:
        raise SystemExit("data placeholder was not substituted")

    with open(HTML, "w", encoding="utf-8") as fh:
        fh.write(html)
    with open(BAT, "w", encoding="ascii", errors="replace") as fh:
        fh.write(BAT_TEXT)
    with open(README, "w", encoding="utf-8") as fh:
        fh.write(README_TEXT)

    np = sum(len(r["parts"]) for r in rows)
    npv = sum(1 for r in rows if r["preview"])
    C.log(f"P01_WARDROBE_REVIEW.html = {os.path.getsize(HTML):,} B  "
          f"({len(rows)} outfits, {np} visual parts, {npv} previews inlined)")
    C.log(f"OPEN_P01_REVIEW.bat / README.md written to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
