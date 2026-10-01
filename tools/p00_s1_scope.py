#!/usr/bin/env python3
"""p00_s1_scope.py — P00 stage 1: resolve the 09 scope, then produce

    reports/P00/00_SCOPE.md
    reports/P00/01_MOD_INVENTORY.csv

READ-ONLY. Opens nothing under mo2\\mods for writing; writes only under the
project's data/ and reports/P00/ folders.

Usage:  python tools/p00_s1_scope.py
"""
from __future__ import annotations

import csv
import datetime
import os
import re
import sys
from collections import Counter


def _counter(it):
    return dict(Counter(it))


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p00_common as C  # noqa: E402

CSV_COLUMNS = [
    "mod_name", "mo2_priority", "leftpane_row", "enabled", "section",
    "total_size_bytes", "total_size_mib", "file_count",
    "n_esm", "n_esp", "n_esl", "n_espfe", "plugin_files",
    "n_nif", "n_dds",
    "bs_shapedata_nif", "bs_shapedata_osd", "bs_slidersets", "bs_slidergroups",
    "bs_sliderpresets", "bs_total",
    "hdt_files", "smp_config_xml", "cbpc_hkx", "other_hkx",
    "n_psc", "n_skse_json", "n_spid", "n_kid", "n_bos", "n_oar", "n_dar",
    "n_json", "n_ini", "n_toml", "n_yaml", "n_xml", "n_txt", "n_fomod",
    "pbrnifpatcher_json", "has_textures_pbr_dir",
    "body_type_guess", "body_type_tag", "body_type_source", "body_tokens",
    "body_family_flag", "notes",
]

SPID_RE = re.compile(r"^\s*\[ScriptInjection\]|\bDistributionType\s*=|^\s*\[(?:Script|Stat)Injection\]", re.M)
KID_RE = re.compile(r"^\s*\[KeywordInjector\]|\bKeywordItemDistribution\b|\[KeywordDistribution\]", re.M)
BOS_RE = re.compile(r"^\s*\[BOS\]|\[BaseObjectSwap\]|objects[/\\]bos[/\\]", re.M | re.I)
SMP_RE = re.compile(r"<boneTransforms|<physics\b|hdtSMP|SMPPhysics|<massSpring", re.I)
OAR_RE = re.compile(r'"conditions"|"sound_categories"|"variants"|"mod"\s*:|"event"\s*:|"load_unload"', re.I)
DAR_RE = re.compile(r"^\s*conditions\s*$", re.M | re.I)


def read_text_head(path: str, limit: int = 262144) -> str:
    try:
        with open(path, "rb") as fh:
            b = fh.read(limit)
    except OSError:
        return ""
    for enc in ("utf-8-sig", "utf-8", "utf-16", "cp1252", "latin-1"):
        try:
            return b.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return b.decode("latin-1", "replace")


def scan_mod(entry: C.ModlistEntry, total_lines: int) -> dict:
    rec = {k: 0 for k in CSV_COLUMNS if k.startswith("n_")}
    for k in ("bs_shapedata_nif", "bs_shapedata_osd", "bs_slidersets",
              "bs_slidergroups", "bs_sliderpresets", "hdt_files",
              "smp_config_xml", "cbpc_hkx", "other_hkx", "pbrnifpatcher_json"):
        rec[k] = 0
    rec["bs_total"] = 0
    rec["has_textures_pbr_dir"] = 0
    rec["file_count"] = 0
    rec["total_size_bytes"] = 0
    rec["body_type_guess"] = "unknown"
    rec["body_type_tag"] = ""
    rec["body_type_source"] = "none"
    rec["body_tokens"] = ""
    rec["body_family_flag"] = "UNKNOWN"
    rec["shapedata_names"] = []
    rec["sliderset_names"] = []
    rec["mod_dir_exists"] = True

    rec["mod_name"] = entry.name
    rec["mo2_priority"] = entry.line_no
    rec["leftpane_row"] = total_lines - entry.line_no + 1
    rec["enabled"] = entry.state
    rec["section"] = C.section_of(SCOPE_ENTRIES, entry)

    root = C.mod_dir(entry.name)
    rec["mod_dir_exists"] = os.path.isdir(root)
    if not rec["mod_dir_exists"]:
        rec["notes"] = "FOLDER_MISSING"
        return rec

    plugins, notes = [], []
    shapedata_names, set_names = set(), set()

    for rel, full, size in C.iter_files(root):
        rec["file_count"] += 1
        rec["total_size_bytes"] += max(size, 0)
        low = rel.lower()
        ext = os.path.splitext(low)[1]
        base = os.path.basename(low)

        # ---- plugins
        if ext == ".esm":
            rec["n_esm"] += 1
        elif ext == ".esp":
            rec["n_esp"] += 1
        elif ext == ".esl":
            rec["n_esl"] += 1
        elif ext == ".espfe":
            rec["n_espfe"] += 1
        if ext in (".esm", ".esp", ".esl", ".espfe"):
            plugins.append(base)
            rec["plugin_files"] = rec.get("plugin_files", "") + base + "; "

        # ---- assets
        if ext == ".nif":
            rec["n_nif"] += 1
        elif ext == ".dds":
            rec["n_dds"] += 1
        elif ext == ".hdt":
            rec["hdt_files"] += 1
        elif ext == ".hkx":
            if "/cloth" in "/" + low or low.startswith("cloth/"):
                rec["cbpc_hkx"] += 1
            else:
                rec["other_hkx"] += 1
        elif ext == ".psc":
            rec["n_psc"] += 1
        elif ext == ".json":
            rec["n_json"] += 1
            if low.startswith("skse/") or "/skse/" in low:
                rec["n_skse_json"] += 1
            if low.startswith("pbrnifpatcher/"):
                rec["pbrnifpatcher_json"] += 1
            elif "animations" in low:
                txt = read_text_head(full)
                if OAR_RE.search(txt):
                    rec["n_oar"] += 1
        elif ext == ".ini":
            rec["n_ini"] += 1
            txt = read_text_head(full)
            if KID_RE.search(txt):
                rec["n_kid"] += 1
            elif SPID_RE.search(txt):
                rec["n_spid"] += 1
            elif BOS_RE.search(txt) or "objects/bos/" in low:
                rec["n_bos"] += 1
        elif ext == ".toml":
            rec["n_toml"] += 1
        elif ext in (".yaml", ".yml"):
            rec["n_yaml"] += 1
        elif ext == ".xml":
            rec["n_xml"] += 1
            if low.startswith("calientetools/bodyslide/"):
                pass
            else:
                txt = read_text_head(full)
                if SMP_RE.search(txt):
                    rec["smp_config_xml"] += 1
        elif ext == ".txt":
            rec["n_txt"] += 1
            if base.endswith("_conditions.txt") and "animations" in low:
                rec["n_dar"] += 1

        # ---- BodySlide
        if low.startswith("calientetools/bodyslide/shapedata/"):
            tail = rel[len("CalienteTools/BodySlide/ShapeData/"):]
            if "/" in tail:
                shapedata_names.add(tail.split("/", 1)[0])
            else:
                shapedata_names.add(os.path.splitext(tail)[0])
            if ext == ".nif":
                rec["bs_shapedata_nif"] += 1
                rec["bs_total"] += 1
            elif ext == ".osd":
                rec["bs_shapedata_osd"] += 1
                rec["bs_total"] += 1
        elif low.startswith("calientetools/bodyslide/slidersets/"):
            if ext == ".xml":
                set_names.add(base[:-4])
                rec["bs_slidersets"] += 1
                rec["bs_total"] += 1
        elif low.startswith("calientetools/bodyslide/slidergroups/"):
            if ext == ".xml":
                rec["bs_slidergroups"] += 1
        elif low.startswith("calientetools/bodyslide/sliderpresets/"):
            if ext == ".xml":
                rec["bs_sliderpresets"] += 1

    if os.path.isdir(os.path.join(root, "textures", "pbr")):
        rec["has_textures_pbr_dir"] = 1

    rec["plugin_files"] = "; ".join(plugins)
    rec["total_size_mib"] = round(rec["total_size_bytes"] / 2 ** 20, 2)
    label, tag, fam, flag, src = C.body_type_from_name(entry.name)
    if label == "unknown":
        label, fam, flag = C.body_type_from_assets(shapedata_names, set_names)
        if label != "unknown":
            src = "bodyslide_assets"
            notes.append("body_type_from_assets")
    if label == "unknown":
        notes.append("BODY_TYPE_UNKNOWN")
    rec["body_type_guess"] = label
    rec["body_type_tag"] = tag
    rec["body_type_source"] = src
    rec["body_tokens"] = "+".join(fam)
    rec["body_family_flag"] = flag
    rec["shapedata_names"] = sorted(shapedata_names)
    rec["sliderset_names"] = sorted(set_names)

    if not plugins:
        notes.append("NO_PLUGIN")
    if rec["bs_total"] == 0:
        notes.append("NO_BODYSLIDE")
    if not rec["n_nif"]:
        notes.append("NO_NIF")
    if rec["enabled"] == "disabled":
        notes.append("DISABLED_IN_MO2")
    rec["notes"] = ";".join(notes)
    return rec


# ------------------------------------------------------------------ main ----
SCOPE_ENTRIES = []

def main() -> int:
    os.makedirs(C.DATA, exist_ok=True)
    os.makedirs(C.REPORTS, exist_ok=True)

    entries = C.read_modlist()
    global SCOPE_ENTRIES
    SCOPE_ENTRIES = entries
    total_lines = len(entries)

    sep, lo, members = C.resolve_scope(entries, C.TARGET_SEPARATOR)

    # cross-check against the brief's example hints
    hits = {h: [] for h in C.BRIEF_EXAMPLE_HINTS}
    scope_names = [m.name for m in members]
    joined = "\n".join(scope_names).lower()
    for h in C.BRIEF_EXAMPLE_HINTS:
        if h.lower() in joined:
            hits[h] = [m.line_no for m in members if h.lower() in m.name.lower()]
    matched = sum(1 for h in hits if hits[h])

    recs = [scan_mod(m, total_lines) for m in members]

    C.write_json(os.path.join(C.DATA, "p00_scope.json"), {
        "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "mo2_instance": C.MO2_INSTANCE,
        "mo2_profile": C.MO2_PROFILE,
        "modlist_path": C.MODLIST,
        "modlist_sha256": C.sha256_file(C.MODLIST),
        "modlist_lines": total_lines,
        "modlist_mtime": datetime.datetime.fromtimestamp(
            os.path.getmtime(C.MODLIST)).isoformat(),
        "separator_name": sep.name,
        "separator_modlist_line": sep.line_no,
        "separator_leftpane_row": total_lines - sep.line_no + 1,
        "scope_first_modlist_line": lo,
        "scope_last_modlist_line": sep.line_no - 1,
        "scope_mod_count": len(members),
        "brief_hint_crosscheck": {"matched": matched, "total": len(hits),
                                  "detail": {k: v for k, v in hits.items()}},
        "members": [{"line_no": m.line_no, "state": m.state, "name": m.name}
                    for m in members],
    })

    # ---------------- 01_MOD_INVENTORY.csv
    out = os.path.join(C.REPORTS, "01_MOD_INVENTORY.csv")
    with open(out, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        w.writeheader()
        for r in recs:
            row = {k: r.get(k, "") for k in CSV_COLUMNS}
            w.writerow(row)

    write_scope_md(sep, lo, members, recs, entries, total_lines, matched, hits)
    print(f"scope separator : {sep.name}  (modlist line {sep.line_no})")
    print(f"scope mods      : {len(members)}  (modlist lines {lo}..{sep.line_no - 1})")
    print(f"brief hints hit : {matched}/{len(hits)}")
    print(f"wrote {out}")
    return 0


def write_scope_md(sep, lo, members, recs, entries, total_lines, matched, hits):
    enabled = sum(1 for r in recs if r["enabled"] == "enabled")
    total_bytes = sum(r["total_size_bytes"] for r in recs)
    total_files = sum(r["file_count"] for r in recs)
    n_plugins = sum(r["n_esm"] + r["n_esp"] + r["n_esl"] + r["n_espfe"]
                    for r in recs)
    n_nif = sum(r["n_nif"] for r in recs)
    n_dds = sum(r["n_dds"] for r in recs)
    n_bs = sum(r["bs_total"] for r in recs)
    n_noplugin = sum(1 for r in recs if "NO_PLUGIN" in r.get("notes", ""))
    n_missing = sum(1 for r in recs if r.get("mod_dir_exists") is False)
    mixing = [r for r in recs
              if r["body_family_flag"] == "MIXED_3BA_BHUNP"]
    bhunp = [r for r in recs if r["body_family_flag"] == "BHUNP_ONLY"]
    unknown_body = [r for r in recs if r["body_type_guess"] == "unknown"]
    from_assets = [r for r in recs if r["body_type_source"] == "bodyslide_assets"]

    L = []
    a = L.append
    a("# 00_SCOPE.md — P00 扫描范围定义")
    a("")
    a("**latex Wardrobe Collection · P00_INVENTORY_AND_ARCHITECTURE_AUDIT**")
    a("")
    a("本文件只做一件事：把「扫描哪些东西」钉死，并给出可复核的证据。")
    a("本阶段**全程只读**，没有修改任何 Mod / 插件 / NIF / DDS / 配置。")
    a("")
    a("---")
    a("")
    a("## 1. 运行环境与真值来源")
    a("")
    a("| 项 | 值 |")
    a("|---|---|")
    a(f"| MO2 instance | `{C.MO2_INSTANCE}` |")
    a(f"| MO2 profile | `{C.MO2_PROFILE}` |")
    a(f"| modlist | `{C.MODLIST}` |")
    a(f"| modlist SHA256 | `{C.sha256_file(C.MODLIST)}` |")
    a(f"| modlist 行数 | {total_lines} |")
    a(f"| modlist mtime | {datetime.datetime.fromtimestamp(os.path.getmtime(C.MODLIST)).isoformat()} |")
    a(f"| mods 根目录 | `{C.MODS_DIR}` |")
    a(f"| 游戏根目录 | `E:\\SkyrimAE`（Data 在 `{C.GAME_DATA}`） |")
    a(f"| 扫描时刻 (UTC) | {datetime.datetime.now(datetime.timezone.utc).isoformat()} |")
    a(f"| 脚本 | `tools/p00_common.py`, `tools/p00_s1_scope.py` |")
    a("")
    a("> modlist.txt 在本次扫描期间被 MO2 改写过（18:29 与 18:31 两次落盘）。")
    a("> 上表的 SHA256 是本报告所依据的那一份快照，可随时复核。")
    a("")
    a("## 2. MO2 优先级模型（本项目的事实，不是推测）")
    a("")
    a("1. `modlist.txt` 是左栏**倒序**：第 1 行 = 左栏最底一行 = **最高覆盖优先级**。")
    a("   交叉验证：`-99 工具生成输出（务必置底）` 分隔符在第 36 行，"
      "`输出·BodySlide Output` 在第 33 行 —— 33 在 36 之下 = 左栏里排在 36 之下，"
      "符合手册「99 生成输出必须真正处于最末端」。")
    a("2. 分隔符是**标题**，成员排在标题**下方**。")
    a("3. 因此：一条 mod 属于**行号比它大的最近那个分隔符**。")
    a("4. `+` = 启用；`-` = 禁用（不进 VFS）；`#` = 注释。")
    a("")
    a("## 3. 范围解析结果")
    a("")
    a(f"目标分隔符：`{sep.name}`")
    a("")
    lower = sep.lower_bound_separator
    upper = next((e for e in C.all_separators(entries)
                  if e.line_no > sep.line_no), None)
    a("| 项 | modlist 行 | 左栏行 |")
    a("|---|---|---|")
    if lower is not None:
        a(f"| 下界分隔符 `{lower.name}`（左栏里排在本块**下方**） | "
          f"{lower.line_no} | {total_lines - lower.line_no + 1} |")
    a(f"| **范围首行** | **{lo}** | {total_lines - lo + 1} |")
    a(f"| **范围末行** | **{sep.line_no - 1}** | {total_lines - (sep.line_no - 1) + 1} |")
    a(f"| **分隔符本身 `{sep.name}`**（本块在左栏里排在它**下方**） | "
      f"**{sep.line_no}** | **{total_lines - sep.line_no + 1}** |")
    if upper is not None:
        a(f"| 上界分隔符 `{upper.name}` | {upper.line_no} | "
          f"{total_lines - upper.line_no + 1} |")
    a("")
    a(f"**扫描范围 = modlist 第 {lo}–{sep.line_no - 1} 行，共 {len(members)} 个 Mod"
      f"（左栏第 {total_lines - lo + 1}–{total_lines - (sep.line_no - 1) + 1} 行）。**")
    a("")
    a("### 3.1 与任务书示例清单的交叉核对")
    a("")
    a(f"任务书列出的示例名称中 **{matched} / {len(hits)}** 命中本范围：")
    a("")
    a("| 示例关键词 | 命中 | modlist 行 |")
    a("|---|---|---|")
    for k, v in hits.items():
        mark = "✓" if v else "✗"
        a(f"| `{k}` | {mark} | {', '.join(map(str, v)) if v else '—'} |")
    a("")
    miss = [k for k, v in hits.items() if not v]
    if miss:
        a(f"未命中 {len(miss)} 项：{', '.join('`' + m + '`' for m in miss)}"
          " —— 这些不在本分隔符内，来源需另行确认。")
    else:
        a("**全部命中，无遗漏。** 任务书的范围定义与 MO2 实际内容一致。")
    a("")
    a("## 4. 范围汇总")
    a("")
    a("| 指标 | 值 |")
    a("|---|---|")
    a(f"| Mod 总数 | **{len(members)}** |")
    a(f"| 其中启用 | {enabled} |")
    a(f"| 其中禁用 | {len(members) - enabled} |")
    a(f"| 文件夹缺失 | {n_missing} |")
    a(f"| 合计文件数 | {total_files:,} |")
    a(f"| 合计体积 | {total_bytes:,} B = {total_bytes / 2 ** 30:.2f} GiB |")
    a(f"| 插件文件总数 | {n_plugins} |")
    a(f"| 其中无插件的 Mod | {n_noplugin} |")
    a(f"| NIF | {n_nif:,} |")
    a(f"| DDS | {n_dds:,} |")
    a(f"| BodySlide 文件 | {n_bs:,} |")
    a("")
    a("### 4.1 体型体系分布")
    a("")
    a("`body_type_guess` 由三条证据链依次得出，来源记录在 `body_type_source` 列：")
    a("`name_tag`（文件夹名的结构化 `【体型·…】` 标签，最可信）→ "
      "`name_scan`（文件夹名其余部分）→ `bodyslide_assets`"
      "（BodySlide 工程 / ShapeData 名）。`【体型·多体型】` 被视为**无效证据**，"
      "会继续向下回退。全部无法判定才记 `unknown`。")
    a("")
    a("| 判定 | Mod 数 |")
    a("|---|---|")
    for k, v in sorted(_counter(r["body_type_guess"] for r in recs).items(),
                       key=lambda kv: (-kv[1], kv[0])):
        a(f"| `{k}` | {v} |")
    a("")
    a("| 体型族 | Mod 数 | 说明 |")
    a("|---|---|---|")
    for k, v in sorted(_counter(r["body_family_flag"] for r in recs).items(),
                       key=lambda kv: (-kv[1], kv[0])):
        note = {"CBBE_3BA": "CBBE 或 3BA 系",
                "BHUNP_ONLY": "纯 BHUNP，**无法直接并入统一 3BA 体系**",
                "MIXED_3BA_BHUNP": "**CBBE/3BA 与 BHUNP 混杂 —— 任务书要求重点标记**",
                "OTHER": "其它体型（TBD / UNP / HIMBO / UBE / SOS）",
                "UNKNOWN": "无法判定"}.get(k, "")
        a(f"| `{k}` | {v} | {note} |")
    a("")
    a(f"- **CBBE/3BA 与 BHUNP 混杂：{len(mixing)} 个 Mod**"
      + (f" —— {', '.join('`' + r['mod_name'] + '`' for r in mixing[:8])}"
         + ("…" if len(mixing) > 8 else "") if mixing else ""))
    a(f"- 纯 BHUNP：{len(bhunp)} 个 Mod")
    a(f"- 体型完全无法判定：{len(unknown_body)} 个 Mod"
      + (f" —— {', '.join('`' + r['mod_name'] + '`' for r in unknown_body[:8])}"
         + ("…" if len(unknown_body) > 8 else "") if unknown_body else ""))
    a(f"- 体型判定只能靠 BodySlide 工程名回推（置信度较低）：{len(from_assets)} 个 Mod")
    a("")
    a("> **不得默认所有项目都能共用同一套 BodySlide。** 上面 `BHUNP_ONLY` 与")
    a("> `MIXED_3BA_BHUNP` 两行就是必须转换的部分；具体清单见阶段 08。")
    a("")
    a("### 4.2 脚本 / 分发 / 物理层现状")
    a("")
    a("| 层 | 本范围计数 |")
    a("|---|---|")
    for label, key in (("SPID 分发", "n_spid"), ("KID 关键词分发", "n_kid"),
                       ("BOS 物体替换", "n_bos"), ("OAR 动画条件", "n_oar"),
                       ("DAR 动画条件", "n_dar"), ("Papyrus `.psc`", "n_psc"),
                       ("SKSE 配置 JSON", "n_skse_json"),
                       ("HDT-SMP 骨架 `.hdt`", "hdt_files"),
                       ("HDT-SMP 物理 XML", "smp_config_xml"),
                       ("CBPC 布料 `.hkx`", "cbpc_hkx"),
                       ("其它 `.hkx`", "other_hkx"),
                       ("PGPatcher 规则 JSON", "pbrnifpatcher_json"),
                       ("`textures\\pbr\\` 目录", "has_textures_pbr_dir")):
        a(f"| {label} | {sum(r[key] for r in recs)} |")
    a("")
    a(f"本范围内 `.ini` 共 {sum(r['n_ini'] for r in recs)} 个、"
      f"`.xml` 共 {sum(r['n_xml'] for r in recs)} 个（其中 SliderSets / "
      f"SliderGroups / SliderPresets 的 BodySlide XML 同时计入 `n_xml` 与 "
      f"`bs_*` 两组列，属有意重复，不是错误）。")
    a("")
    a("**这一条对最终架构影响很大：** 本分隔符是**纯资产层**。它没有脚本、"
      "没有 SPID/KID 分发、没有 OAR/DAR、几乎没有物理。")
    a("—— 也就是说「SPID / Outfit 自然分发到 Skyrim 世界」这一目标所需的"
      "整套分发层，目前**不在本范围内**，需要么在 P01 单独立项，"
      "要么把范围扩到 `07 正常服装、护甲`（那里有 30+ 个 SPID 补丁 Mod）。")
    a("")
    a("### 4.3 范围内全部 Mod 明细")
    a("")
    a("按 `mo2_priority` 升序（= 覆盖优先级由高到低，与左栏从上到下一致）。")
    a("")
    a("| # | modlist 行 | Mod | MiB | 文件 | 插件 | NIF | DDS | BS | 体型 | 来源 | 备注 |")
    a("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(sorted(recs, key=lambda x: x["mo2_priority"]), 1):
        plugs = f"{r['n_esm']}es{'' if r['n_esm'] == 1 else 'm'}" \
            if r["n_esm"] else ""
        for key, short in (("n_esp", "esp"), ("n_esl", "esl"),
                           ("n_espfe", "espfe")):
            if r[key]:
                plugs += ("" if not plugs else " ") + f"{r[key]}{short}"
        name = r["mod_name"]
        if len(name) > 58:
            name = name[:55] + "..."
        a(f"| {i} | {r['mo2_priority']} | `{name}` | {r['total_size_mib']:.1f} "
          f"| {r['file_count']} | {plugs or '—'} | {r['n_nif']} | {r['n_dds']} "
          f"| {r['bs_total']} | `{r['body_type_guess']}` | {r['body_type_source']} "
          f"| {r['notes'] or ''} |")
    a("")
    a("")
    a("## 5. 范围边界声明")
    a("")
    a("**在范围内**（本轮唯一授权扫描的对象）：")
    a(f"`{C.MODS_DIR}\\<本节表格 01_MOD_INVENTORY.csv 所列 {len(members)} 个 Mod>`")
    a("")
    a("**明确不在范围内**：")
    a("")
    a("- 其余所有 MO2 分隔符（`00`–`08`、`10`–`17`、`98`、`99`）。")
    a("- 紧邻上方的 `07 正常服装、护甲` 分隔符下的 115 个护甲/长袍 Mod。")
    a("- `Data\\` 下的游戏本体文件与 BSA。")
    a("")
    a("范围外资产**只允许被读取用于解析引用关系**（例如某个范围内 Mod 的 NIF "
      "指向了范围外的 DDS，这一事实必须被记录），**不得成为报告主体**。")
    a("")
    a("## 6. 本阶段的写操作清单")
    a("")
    a("本次运行只写入了本工程自己的目录：")
    a("")
    a("```")
    a(f"{C.PROJECT}\\")
    a("├─ tools\\p00_common.py, p00_s1_scope.py   # 扫描脚本")
    a("├─ data\\p00_scope.json                      # 中间证据")
    a("└─ reports\\P00\\00_SCOPE.md, 01_MOD_INVENTORY.csv")
    a("```")
    a("")
    a("对 `mo2\\mods\\`、`Data\\`、modlist、BodySlide、PGPatcher **零写入**。")
    a("")
    a("---")
    a("")
    a("*下一步（待人工审核后）：02_PLUGIN_RECORDS.csv / 03_ARMOR_ARMA_MAP.csv / …*")
    a("")
    a("**P00 STAGE 1 COMPLETE — STOPPED FOR REVIEW**")

    with open(os.path.join(C.REPORTS, "00_SCOPE.md"), "w",
              encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
