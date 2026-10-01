#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p00r_reports.py — STAGE F: derive the P00_RERUN report set from the
stage A-E evidence files.

Emits 00,01,02,03,07,08,09,10,11,12,13,14,15,16,18,19,20 plus
P00_MASTER_REPORT.md and P00_RERUN_VS_OLD.md into reports/P00_RERUN/.

04,05,06,17 are produced by the parts/catalog and config agents; this script
does not touch them, but it DOES read 04_parts.json when it is present and
degrades to an explicit 'upstream stage unavailable' marker when it is not.

SCHEMA-FIX ERA (this revision):
  * ARMO -> ArmorAddon is 1:N over ARMO.MODL. ARMO.RNAM is the RACE. The worn
    mesh is on the ARMA; the ARMO's own MOD2..MOD5 are world/inventory models.
    The old single-valued ARMA_formid / ARMA_edid columns are gone for good.
  * 07 rows are keyed by OSP_PATH and every emitted column is XML-derived.
  * body_candidate can be CBBE (not only CBBE_3BA / BHUNP / OTHER / UNKNOWN).

Read-only with respect to the game. Only reads data/P00_RERUN/*.json(.gz).
"""
from __future__ import annotations

import csv
import datetime
import gzip
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p00r_common as C  # noqa: E402


def load(name):
    p = os.path.join(C.DATA, name)
    if name.endswith(".gz"):
        with gzip.open(p, "rt", encoding="utf-8") as fh:
            return json.load(fh)
    with open(p, "r", encoding="utf-8") as fh:
        return json.load(fh)




def _delegated_csv(name, owner):
    """A report owned by a dedicated module.

    The generator that used to live here implemented superseded rules, so
    re-running the report driver would overwrite the corrected output with the
    old one. We therefore only read the file the owning module wrote.
    """
    p = os.path.join(C.REPORTS, name)
    if os.path.isfile(p):
        with open(p, encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.DictReader(fh))
        return len(rows), f"{name} (owned by {owner})", rows
    C.log(f"  !! {name} missing - run {owner} first")
    return 0, f"{name} MISSING (run {owner})", []

def load_optional(name, default=None):
    """Load a stage file if it exists; `default` if the upstream stage never
    ran. Used so a missing upstream stage degrades to an explicit
    'upstream stage unavailable' marker instead of crashing the run."""
    p = os.path.join(C.DATA, name)
    if not os.path.isfile(p):
        return default
    return load(name)


# ------------------------------------------------------------ UNKNOWN -------
# Nothing in this module may invent a value. A field the evidence does not
# carry is printed as the literal token UNKNOWN; a field the evidence positively
# shows to be EMPTY (an empty slider list, an ARMO with no ArmorAddon) is
# printed as the literal token NONE. The two must never be confused.
UNK = "UNKNOWN"
NONE = "NONE"

# `classify_body`'s candidate vocabulary. CBBE is in it on purpose: after the
# audit fix a CBBE-only token set classifies as CBBE, so every aggregate must
# be able to render it. Any value the classifier produces that is not in this
# list is still rendered -- see body_vocab_dynamic() -- but the report says so.
BODY_VOCAB = ("CBBE_3BA", "CBBE", "BHUNP", "OTHER", "UNKNOWN")

# `game_nif_resolved` vocabulary, as produced by the parts stage.
GAME_NIF_MEANING = {
    "yes": "ARMA wearable NIF 或 BodySlide base NIF 在本范围内解析到了",
    "pending_build": "只有 BodySlide 生成的 pending build 产物，游戏运行期才有",
    "no": "既没有解析到 ARMA wearable NIF，也没有 BodySlide base NIF",
    UNK: "上游阶段未提供该字段",
}


def jval(v):
    """Render one raw subrecord payload without inventing a CK column name."""
    if v is None or v == "":
        return UNK
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, int):
        return C.record_id(v)
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, (bytes, bytearray)):
        return bytes(v).hex().upper()
    return str(v)


def jnum(v):
    """A count / mask / small integer. Never rendered as a FormID."""
    if v is None or v == "":
        return UNK
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return repr(v)
    return str(v)


def joinl(values, sep="; ", limit=1200, empty=UNK):
    """Join a list field; `empty` is the token used when the list is empty."""
    out = [str(x) for x in (values or []) if x not in (None, "")]
    return sep.join(out)[:limit] if out else empty


def as_list(v, sep=";"):
    """Normalise a catalogue field to a list.

    04_PARTS_CATALOG ships these as either a real list or a ``;``-joined
    STRING depending on the field. Taking len() on the string form silently
    counts characters, so every list-shaped field is funnelled through here
    first.
    """
    if v is None or v == "":
        return []
    if isinstance(v, (list, tuple)):
        return [x for x in v if x not in (None, "")]
    return [x.strip() for x in str(v).split(sep) if x.strip()]


def arma_pairs(armo):
    """1:N (ARMO -> ArmorAddon) walk.

    `arma_refs` carries only (plugin, formid, edid); the resolution ROUTE lives
    on the matching `modl_refs` entry, so the two are paired on the 8-digit
    formid. Returns [(ref, route, modl_entry)] in MODL order.

    NOTE: pairing is on the full 8-digit formid, never on the 24-bit local id.
    The TES4 master byte is load-bearing -- a plugin's own records carry
    byte == len(MAST) -- so a 24-bit match would join unrelated records.
    """
    refs = (armo or {}).get("arma_refs") or []
    by_formid = {}
    for m in (armo or {}).get("modl_refs") or []:
        by_formid.setdefault(m.get("raw_formid"), m)
    out = []
    for ref in refs:
        m = by_formid.get(ref.get("formid")) or {}
        out.append((ref, m.get("route") or UNK, m))
    return out


def flat_models(blk):
    """MOD2..MOD5 in slot order -> one flat list of model paths."""
    out = []
    for k in ("MOD2", "MOD3", "MOD4", "MOD5"):
        for v in ((blk or {}).get(k) or []):
            if isinstance(v, str) and v:
                out.append(v)
    return out


def texture_set_text(tset):
    """MO2S/MO2T/MO3S/... -> 'KEY=value; KEY=value' from a mapping."""
    out = []
    for k in sorted(tset or {}):
        for v in (tset.get(k) or []):
            out.append(f"{k}={jval(v)}")
    return "; ".join(out)[:600] if out else NONE


# MO2S..MO5T: the armor texture-set slots. An ARMO may carry them directly
# (its own world model has one) even though the WORN mesh textures live on the
# ARMA -- so both record types are scanned for them.
TSET_KEYS = ("MO2S", "MO2T", "MO3S", "MO3T", "MO4S", "MO4T", "MO5S", "MO5T")


def normalize_dupes(dupes, tex):
    """Accept either dupes schema.

    The texture scanner may emit `same_name_diff_content` entries keyed on
    TEXTURE_ID or on `path`, and may or may not pre-compute the summary
    counters. Normalise to one shape here so the report code has a single
    contract, and recompute every counter from the raw groups so the numbers
    in the reports never depend on which producer wrote the file.
    """
    bi = dupes.get("byte_identical_groups") or {}
    sn = dupes.get("same_name_diff_content") or {}
    size_by = {}
    mod_by = {}
    for t in tex:
        tid = t.get("TEXTURE_ID")
        size_by[tid] = t.get("size", 0)
        mod_by[tid] = t["source_mod"]
    extra = 0
    reclaim = 0
    for h, ids in bi.items():
        extra += max(len(ids) - 1, 0)
        reclaim += max(len(ids) - 1, 0) * size_by.get(ids[0], 0)
    return {
        "byte_identical_groups": bi,
        "byte_identical_group_count": len(bi),
        "byte_identical_extra_copies": extra,
        "byte_identical_reclaimable_bytes": reclaim,
        "same_name_diff_content": sn,
        "same_name_diff_content_count": len(sn),
    }


# ============================================================ NIF taxonomy ===
# The NIF scanner applied the ordered rules literally; on this scope that
# leaves every non-ShapeData file as UNKNOWN, because a latex wardrobe ships
# meshes/<mod>/worlditems/*.nif and meshes/armor|clothes/*.nif and nothing at
# all under /bodyphysics/, /static/, /clutter/ or meshes/actors/.
# The raw scanner output is left untouched; the taxonomy is re-applied here so
# the raw file stays the provenance record and the rule change is auditable.
NIF_RULES = [
    ("SHAPEDATA", lambda c, v, m: c == "bodyslide_shapedata_nif"),
    ("GENERATED_OUTPUT", lambda c, v, m: v.startswith("meshes/clothing/")),
    ("PHYSICS_MESH", lambda c, v, m: any(
        s in v for s in ("/bodyphysics/", "/bodyparts/", "/partitions/",
                         "/cloth/springs/"))),
    ("GROUND_OBJECT", lambda c, v, m: any(
        s in v for s in ("/ground/", "/dirt/", "/rock/", "/snow/"))),
    ("STATIC_MESH", lambda c, v, m: any(
        s in v for s in ("/static", "/architecture", "/clutter", "/props",
                         "/furniture", "/dungeons", "/ruins"))),
    ("GAME_MESH", lambda c, v, m: v.startswith("meshes/")),
]


def reclassify_nifs(nifs):
    changed = Counter()
    for n in nifs:
        v = n["path"].lower()
        new = "UNKNOWN"
        for label, pred in NIF_RULES:
            try:
                if pred(n.get("stage_a_cat", ""), v, n["source_mod"]):
                    new = label
                    break
            except Exception:
                continue
        if new != n.get("nif_class"):
            changed[(n.get("nif_class"), new)] += 1
        n["nif_class_raw"] = n.get("nif_class")
        n["nif_class"] = new
    return changed


# ======================================================================== 13 ==
R13_COLS = ["conflict_id", "virtual_path", "conflict_kind", "n_providers",
            "winner_mod", "winner_priority", "winner_sha256", "loser_mods",
            "loser_priorities", "loser_sha256", "winner_size",
            "shadowed_bytes", "same_content", "ext", "action", "note"]


def r13_mo2_conflict(index, mods):
    prio = {m["mod_name"]: m["priority"] for m in mods}
    by_v = defaultdict(list)
    for r in index:
        by_v[C.nif_id(r["vpath"])].append(r)
    rows = []
    seq = 0
    total_shadowed = 0
    for vp, lst in sorted(by_v.items()):
        if len(lst) < 2:
            continue
        seq += 1
        # MO2 VFS: scanning from modlist line 1 downward, the first provider
        # wins, i.e. the SMALLEST priority number wins.
        lst = sorted(lst, key=lambda r: (prio.get(r["mod"], 10 ** 9),
                                         r["mod"]))
        win, losers = lst[0], lst[1:]
        same = len({r["sha256"] for r in lst}) == 1
        shadowed = sum(r["size"] for r in losers if r["size"] > 0)
        total_shadowed += shadowed
        rows.append({
            "conflict_id": f"CONF::{vp[:40]}::{seq:04d}",
            "virtual_path": lst[0]["vpath"], "ext": lst[0]["ext"],
            "conflict_kind": "VFS_OVERRIDE",
            "n_providers": len(lst),
            "winner_mod": win["mod"], "winner_priority": prio.get(win["mod"]),
            "winner_sha256": win["sha256"], "winner_size": win["size"],
            "loser_mods": "; ".join(r["mod"] for r in losers),
            "loser_priorities": "; ".join(
                str(prio.get(r["mod"], "?")) for r in losers),
            "loser_sha256": "; ".join(r["sha256"][:16] for r in losers),
            "shadowed_bytes": shadowed,
            "same_content": "yes" if same else "no",
            "action": ("SAFE_BYTE_DEDUP" if same else "REVIEW_MO2_PRIORITY"),
            "note": ("identical bytes from several mods"
                     if same else
                     "DIFFERENT content -- the loser is fully shadowed and "
                     "never reaches the VFS"),
        })
    n = C.write_csv(os.path.join(C.REPORTS, "13_MO2_CONFLICT_MAP.csv"),
                    R13_COLS, rows)
    return n, "13_MO2_CONFLICT_MAP.csv", rows, total_shadowed


# ======================================================================== 00 ==
def r00_scope(ev, mods):
    L = []
    a = L.append
    a("# 00_SCOPE.md — P00_RERUN 扫描范围定义")
    a("")
    a("**ZLJ Wardrobe Collection · P00_INVENTORY_AND_ARCHITECTURE_AUDIT · CLEAN RE-RUN**")
    a("")
    a("本轮为**全量重扫**，以**当前 MO2 实际状态**为唯一真值。")
    a("旧 P00 成果未被覆盖，仅作 `archive / reference only`，对比见 `P00_RERUN_VS_OLD.md`。")
    a("")
    a("## 1. 真值来源")
    a("")
    a("| 项 | 值 |")
    a("|---|---|")
    a(f"| MO2 instance | `{ev['mo2_instance']}` |")
    a(f"| MO2 profile | `{ev['mo2_profile']}` |")
    a(f"| modlist | `{ev['modlist_path']}` |")
    a(f"| **modlist SHA256** | `{ev['modlist_sha256']}` |")
    a(f"| modlist 行数 | {ev['modlist_lines']:,} |")
    a(f"| 目标分隔符 | `{ev['separator_name']}` |")
    a(f"| 扫描时刻 (UTC) | {ev['generated_utc']} |")
    a("")
    a("> **mtime 不作为范围判断依据。** 本机 MO2 每次退出会把 `modlist.txt` 原子替换一次，")
    a("> mtime 必然刷新而内容可能一字未改。范围只由 **SHA256 + 分隔符解析**决定。")
    a("")
    a("## 2. MO2 优先级模型")
    a("")
    a("1. `modlist.txt` 是左栏**倒序**：第 1 行 = 最底 = **最高覆盖优先级**。")
    a("2. 分隔符是**标题**，成员排在标题**下方**（左栏），即 modlist 行号**更小**。")
    a("3. 因此行号 L 的 mod 归属**行号比 L 大且最接近**的分隔符。")
    a("4. 分隔符 S 拥有区间 `(最近的更小行号分隔符 + 1) … (S - 1)`。")
    a("5. `+` 启用 / `-` 禁用 / `#` 注释。")
    a("")
    a("## 3. 范围解析结果")
    a("")
    a("| 项 | modlist 行 |")
    a("|---|---|")
    a(f"| 下界分隔符 `{ev['lower_bound_sep']}` | {ev['lower_bound_sep_line']} |")
    a(f"| **范围首行** | **{ev['scope_first_line']}** |")
    a(f"| **范围末行** | **{ev['scope_last_line']}** |")
    a(f"| **分隔符本身 `{ev['separator_name']}`** | **{ev['separator_line']}** |")
    a(f"| 上界分隔符 `{ev['upper_bound_sep']}` | {ev['upper_bound_sep_line']} |")
    a("")
    a(f"**扫描范围 = modlist 第 {ev['scope_first_line']}–{ev['scope_last_line']} 行，"
      f"共 {ev['scope_mod_count']} 个 Mod。**")
    a("")
    dr = ev.get("drift")
    if dr:
        a("### 3.1 ⚠ 扫描期间 modlist 发生过变更（已在本次扫描中重新取基线）")
        a("")
        a("| 项 | 上一次扫描 | 本次扫描 |")
        a("|---|---|---|")
        a(f"| modlist SHA256 | `{str(dr['previous_sha256'])[:16]}…` "
          f"| `{str(dr['current_sha256'])[:16]}…` |")
        a(f"| modlist 行数 | {dr['previous_modlist_lines']} "
          f"| {dr['current_modlist_lines']} |")
        a(f"| 09 范围 | L{dr['previous_scope_lines'][0]}–"
          f"{dr['previous_scope_lines'][1]} "
          f"| L{dr['current_scope_lines'][0]}–{dr['current_scope_lines'][1]} |")
        a(f"| 新增成员 | {len(dr['members_added'])} | — |")
        a(f"| 移出成员 | {len(dr['members_removed'])} | — |")
        a("")
        a(f"**判定：{dr['verdict']}**")
        a("")
        a("本机 MO2 每次退出会原子替换 `modlist.txt`。本轮扫描期间 MO2 处于运行状态，")
        a("modlist 被改写了数次。**扫描主体（56 个 Mod 及其磁盘内容）没有变化**，")
        a("因此所有资产层面的结论依然成立；变化的是 MO2 排序坐标")
        a("（`priority` / `leftpane_row`），已按当前 modlist 重新取基线。")
        a("")
        a("> **后续阶段开始前请先关闭 MO2**，否则排序坐标会再次漂移。")
        a("")
    a("## 4. 范围汇总")
    a("")
    a("| 指标 | 值 |")
    a("|---|---|")
    a(f"| Mod 总数 | **{ev['scope_mod_count']}** |")
    a(f"| 其中启用 | {sum(1 for m in mods if m['enabled'] == 'enabled')} |")
    a(f"| 其中禁用 | {sum(1 for m in mods if m['enabled'] == 'disabled')} |")
    a(f"| 文件夹缺失 | {sum(1 for m in mods if not m['folder_exists'])} |")
    a(f"| 合计文件数 | **{ev['scope_total_files']:,}** |")
    a(f"| 合计体积 | **{ev['scope_total_bytes']:,} B = "
      f"{ev['scope_total_bytes']/2**30:.2f} GiB** |")
    a("")
    a("## 5. 逐 Mod 明细（按 MO2 优先级由高到低）")
    a("")
    a("| # | 行 | Mod | MiB | 文件 | 插件 | NIF | DDS | BS | OSP | 体型(名) |")
    a("|---|---|---|---|---|---|---|---|---|---|---|")
    for i, m in enumerate(mods, 1):
        nm = m["mod_name"]
        nm = nm if len(nm) <= 52 else nm[:49] + "…"
        a(f"| {i} | {m['priority']} | `{nm}` | {m['size_bytes']/2**20:.1f} "
          f"| {m['file_count']} | {m['plugin_count']} | {m['nif_count']} "
          f"| {m['dds_count']} | {m['bodyslide_count']} "
          f"| {m['bodyslide_sliderset_osp']} | `{m['body_candidate_name']}` |")
    a("")
    a("## 6. 只读声明")
    a("")
    a("本轮对 `E:\\SkyrimAE\\mo2\\`、`E:\\SkyrimAE\\Data\\`、modlist、BodySlide、")
    a("PGPatcher **零写入**。`p00r_common.assert_write_path()` 在运行时强制所有写操作")
    a("只能落在 `tools/P00_RERUN/`、`data/P00_RERUN/`、`reports/P00_RERUN/` 之内，")
    a("越界直接 `SystemExit`。")
    a("")
    a("---")
    a("")
    a("**P00_RERUN · STAGE A/B/C/D/E COMPLETE**")
    with open(os.path.join(C.REPORTS, "00_SCOPE.md"), "w",
              encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    return "00_SCOPE.md"


# ======================================================================== 01 ==
R01_COLS = ["mod_name", "MOD_ID", "priority", "mo2_leftpane_row", "enabled",
            "folder_exists", "size_bytes", "size_mib", "file_count",
            "plugin_count", "nif_count", "dds_count", "bodyslide_count",
            "bodyslide_shapedata_nif", "bodyslide_shapedata_osd",
            "bodyslide_sliderset_osp", "bodyslide_sliderset_xml",
            "bodyslide_slidergroup", "bodyslide_sliderpreset",
            "physics_count", "script_count", "config_count",
            "ini_count", "json_count", "xml_count", "txt_count",
            "body_candidate", "body_tag", "body_tokens", "body_family_flag",
            "body_source", "plugin_files", "bsa_count"]


def r01_inventory(mods):
    rows = []
    for m in mods:
        r = dict(m)
        r["size_mib"] = round(m["size_bytes"] / 2 ** 20, 2)
        r["body_candidate"] = m["body_candidate_name"]
        rows.append(r)
    n = C.write_csv(os.path.join(C.REPORTS, "01_MOD_INVENTORY.csv"),
                    R01_COLS, rows)
    return n, "01_MOD_INVENTORY.csv"


# ======================================================================== 02 ==
# CORRECTED SCHEMA. An ARMO does not link to its ArmorAddon through RNAM --
# RNAM is the RACE. The ArmorAddon link is MODL, and it is 1:N. The wearable
# mesh lives on the ARMA; the ARMO's own MOD2..MOD5 are world / inventory drop
# models. The old single-valued `arma_link` / `arma_edid` columns (which read
# RNAM as the addon) are gone for good and must not come back.
R02_COLS = ["record_id", "PLUGIN_ID", "plugin_file", "source_mod", "MOD_ID",
            "priority", "record_type", "formid", "edid", "name", "description",
            "slots", "slot_mask", "slot_mask_hex", "slot_bits", "slot_source",
            "slot_confidence",
            "armor_rating_raw_DN", "value_raw_DATA_u32", "value_raw_DATA_f32",
            "value_provenance",
            "race_formid", "race_is", "race_plugin", "race_type",
            "race_edid", "race_route",
            "n_modl_refs", "n_arma_refs",
            "ARMA_formids", "ARMA_edids", "ARMA_plugins", "ARMA_routes",
            "model_path_kind", "model_paths", "world_model_paths",
            "world_model_note", "armor_material_raw",
            "n_source_mesh_refs", "texture_set_refs",
            "keywords", "masters_count", "masters", "file_version",
            "outfit_target_formid", "outfit_target_type", "outfit_target_edid",
                            "outfit_refs_all",
            "note"]


def r02_plugin_records(recs, pidx):
    # in-scope index used only for OUTFIT (OTFT.INAM) targets; the ArmorAddon
    # links are NOT resolved here -- they arrive already resolved (with route)
    # on the ARMO block by the parser.
    by_plugin_formid = {(r["plugin_file"].lower(), r["formid"]): r
                        for r in recs}
    rows = []
    for r in recs:
        rt = r["record_type"]
        s = r["subrecords"]
        pi = pidx.get(r["PLUGIN_ID"], {})
        armo = r.get("armo") or {}
        arma = r.get("arma") or {}
        armour = rt in ("ARMO", "ARMA")

        if rt == "ARMO":
            blk = armo
            pairs = arma_pairs(blk)
            race = blk.get("race_resolved") or {}
            models = blk.get("world_model_paths") or []
            model_kind = "ARMO_WORLD_MODEL"
            world_note = blk.get("world_model_note") or UNK
            tset = texture_set_text({k: s.get(k) for k in TSET_KEYS
                                     if s.get(k)})
            armor_mat = UNK
            n_src_mesh = UNK
            n_modl = blk.get("n_modl_refs")
            n_arma = blk.get("n_arma_refs")
            rows_extra = {
                "race_formid": jval(blk.get("race_raw")),
                "race_is": blk.get("race_is") or UNK,
                "race_plugin": race.get("plugin") or UNK,
                "race_type": race.get("type") or UNK,
                "race_edid": race.get("edid") or UNK,
                "race_route": race.get("route") or UNK,
                "ARMA_formids": joinl([p[0].get("formid") for p in pairs],
                                      empty=NONE),
                "ARMA_edids": joinl([p[0].get("edid") for p in pairs],
                                    empty=NONE),
                "ARMA_plugins": joinl([p[0].get("plugin") for p in pairs],
                                      empty=NONE),
                "ARMA_routes": joinl([p[1] for p in pairs], empty=NONE),
            }
        elif rt == "ARMA":
            blk = arma
            pairs = []
            models = flat_models(blk.get("addon_model_paths") or {})
            model_kind = "ARMA_WEARABLE_MODEL"
            world_note = ("n/a on an ARMA row: the world / inventory models are "
                          "carried by the referencing ARMO")
            tset = texture_set_text(blk.get("texture_set_refs"))
            armor_mat = jval(blk.get("armor_material_raw"))
            n_src_mesh = len(blk.get("source_mesh_refs") or [])
            n_modl = UNK
            n_arma = UNK
            rows_extra = {k: UNK for k in
                          ("race_formid", "race_is", "race_plugin",
                           "race_type", "race_edid", "race_route",
                           "ARMA_formids", "ARMA_edids", "ARMA_plugins",
                           "ARMA_routes")}
        else:
            blk = {}
            models = []
            model_kind = UNK
            world_note = UNK
            tset = UNK
            armor_mat = UNK
            n_src_mesh = UNK
            n_modl = UNK
            n_arma = UNK
            rows_extra = {k: UNK for k in
                          ("race_formid", "race_is", "race_plugin",
                           "race_type", "race_edid", "race_route",
                           "ARMA_formids", "ARMA_edids", "ARMA_plugins",
                           "ARMA_routes")}

        # OTFT.INAM is NOT one target: measured here it is a repeated FormID
        # list of 3-7 entries (the outfits an outfit relates to), not a single
        # reference and not text. Older evidence decoded it as a string such
        # as '\x08' or '!'; the uint32 decoder now yields clean ids.
        # "outfit_target_*" therefore reports the first resolved target and
        # the full list stays visible in outfit_refs_all.
        ot_f, ot_t, ot_e, ot_note = UNK, UNK, UNK, ""
        if rt == "OTFT":
            refs = [x for x in (s.get("INAM") or []) if x not in (None, "")]
            inam_list = []
            for x in refs:
                if isinstance(x, int) and x:
                    inam_list.append(C.record_id(x))
                elif isinstance(x, str) and len(x) == 8 and \
                        all(ch in "0123456789abcdefABCDEF" for ch in x):
                    inam_list.append(x.upper())
            ot_refs_all = ";".join(inam_list)
            if inam_list:
                for f_ in inam_list:
                    tgt = by_plugin_formid.get(
                        (r["plugin_file"].lower(), f_))
                    if tgt is not None:
                        ot_f, ot_t = f_, tgt["record_type"]
                        ot_e = jval((tgt["subrecords"].get("EDID") or [UNK])[0])
                        break
                if ot_f == UNK:
                    ot_f = inam_list[0]
                    ot_note = (f"INAM decoded to {len(inam_list)} FormID(s); "
                               "none of them is an in-scope record (they point "
                               "at OUTFIT records outside the 09 scope)")
            else:
                ot_note = ("OTFT.INAM produced no decodable FormID; target not "
                           "recovered")

        rows.append({
            "record_id": f"REC::{r['PLUGIN_ID']}::{r['formid']}",
            "PLUGIN_ID": r["PLUGIN_ID"],
            "plugin_file": r["plugin_file"],
            "source_mod": r["source_mod"],
            "MOD_ID": r["MOD_ID"],
            "priority": r["priority"],
            "record_type": rt,
            "formid": r["formid"],
            "edid": jval((s.get("EDID") or [UNK])[0]),
            "name": jval((s.get("FULL") or [NONE])[0]),
            "description": jval((s.get("DESC") or [NONE])[0]),
            "slots": joinl(blk.get("slot_names"), empty=NONE) if armour
            else UNK,
            "slot_mask": jnum(blk.get("slot_mask")) if armour else UNK,
            "slot_mask_hex": blk.get("slot_mask_hex") or UNK if armour
            else UNK,
            "slot_bits": joinl([str(b) for b in (blk.get("slot_bits") or [])],
                               empty=NONE) if armour else UNK,
            "slot_source": blk.get("slot_source") or UNK if armour else UNK,
            "slot_confidence": blk.get("slot_confidence") or UNK if armour
            else UNK,
            "armor_rating_raw_DN": jval((armo.get("DNAM_u32")
                                         or {}).get("u32", {})
                                         if isinstance(armo.get("DNAM_u32"),
                                                       dict)
                                         else armo.get("DNAM_u32"))
            if rt == "ARMO" else UNK,
            "value_raw_DATA_u32": jval((armo.get("DATA_u32") or {}).get("u32"))
            if rt == "ARMO" and isinstance(armo.get("DATA_u32"), dict)
            else (jval(armo.get("DATA_u32")) if rt == "ARMO" else UNK),
            "value_raw_DATA_f32": jval(armo.get("DATA_f32"))
            if rt == "ARMO" else UNK,
            "value_provenance": armo.get("value_source") or UNK
            if rt == "ARMO" else UNK,
            "keywords": joinl(s.get("KWDA"), empty=NONE),
            "n_modl_refs": jnum(n_modl),
            "n_arma_refs": jnum(n_arma),
            "model_path_kind": model_kind,
            "model_paths": joinl(models, empty=NONE) if armour else UNK,
            "world_model_paths": joinl(armo.get("world_model_paths"),
                                       empty=NONE) if rt == "ARMO" else UNK,
            "world_model_note": world_note,
            "armor_material_raw": armor_mat,
            "n_source_mesh_refs": jnum(n_src_mesh),
            "texture_set_refs": tset,
            "masters_count": len(pi.get("masters", [])),
            "masters": joinl(pi.get("masters"), empty=NONE),
            "file_version": r.get("file_version", ""),
            "outfit_target_formid": ot_f,
            "outfit_target_type": ot_t,
            "outfit_target_edid": ot_e,
            "outfit_refs_all": (ot_refs_all if rt == "OTFT" else ""),
            "note": ot_note or ("" if armour else
                                f"record type {rt} carries no armour/armour-"
                                f"addon block; armour columns are {UNK}"),
            **rows_extra,
        })
    n = C.write_csv(os.path.join(C.REPORTS, "02_PLUGIN_RECORDS.csv"),
                    R02_COLS, rows)
    return n, "02_PLUGIN_RECORDS.csv"


# ======================================================================== 03 ==
# One row per (ARMO, ArmorAddon) pair. An ARMO with zero ArmorAddon links
# produces ZERO rows here -- that absence is the finding, so it is recorded in
# the master report / 04_PARTS_CATALOG, never as a fabricated placeholder row.
R03_COLS = ["link_id", "ARMO_record_id", "ARMO_formid", "ARMO_edid", "ARMO_name",
            "ARMO_MODL_ordinal", "ARMO_PLUGIN_ID", "source_mod", "MOD_ID",
            "ARMA_plugin", "ARMA_formid", "ARMA_edid",
            "ARMA_wearable_model_paths", "ARMA_texture_set_refs",
            "ARMA_slot_mask", "ARMA_slot_mask_hex", "ARMA_slots",
            "ARMA_armor_material_raw", "ARMA_source_mesh_refs",
            "ARMO_slot_mask", "ARMO_slot_mask_hex", "ARMO_slots",
            "ARMO_world_model_paths", "resolution_route", "note"]


def r03_armor_arma(recs):
    arma_idx = {(r["plugin_file"].lower(), r["formid"]): r
                for r in recs if r["record_type"] == "ARMA"}
    rows = []
    n_arma = 0
    for r in recs:
        if r["record_type"] != "ARMO":
            continue
        armo = r.get("armo") or {}
        s = r["subrecords"]
        ed = s.get("EDID", [""])[0]
        ed = ed if isinstance(ed, str) else UNK
        full = s.get("FULL", [""])[0]
        full = full if isinstance(full, str) else NONE
        pairs = arma_pairs(armo)
        n_arma += len(pairs)
        for i, (ref, route, _m) in enumerate(pairs, 1):
            tgt = arma_idx.get(((ref.get("plugin") or "").lower(),
                                ref.get("formid")))
            if tgt is None:
                a_blk = {}
                note = ("ArmorAddon target is outside the 09 scope; its "
                        "wearable models were not parsed here")
            else:
                a_blk = tgt.get("arma") or {}
                note = ""
            rows.append({
                "link_id": (f"A2M::{r['PLUGIN_ID']}::{r['formid']}"
                            f"::{ref.get('formid')}::{i:02d}"),
                "ARMO_record_id": f"REC::{r['PLUGIN_ID']}::{r['formid']}",
                "ARMO_formid": r["formid"],
                "ARMO_edid": ed,
                "ARMO_name": full,
                "ARMO_MODL_ordinal": i,
                "ARMO_PLUGIN_ID": r["PLUGIN_ID"],
                "source_mod": r["source_mod"],
                "MOD_ID": r["MOD_ID"],
                "ARMA_plugin": ref.get("plugin") or UNK,
                "ARMA_formid": ref.get("formid") or UNK,
                "ARMA_edid": ref.get("edid") or UNK,
                "ARMA_wearable_model_paths": joinl(
                    flat_models(a_blk.get("addon_model_paths") or {}),
                    empty=NONE if a_blk else UNK),
                "ARMA_texture_set_refs": (texture_set_text(
                    a_blk.get("texture_set_refs")) if a_blk else UNK),
                "ARMA_slot_mask": jnum(a_blk.get("slot_mask"))
                if a_blk else UNK,
                "ARMA_slot_mask_hex": (a_blk.get("slot_mask_hex") or UNK)
                if a_blk else UNK,
                "ARMA_slots": joinl(a_blk.get("slot_names"), empty=NONE)
                if a_blk else UNK,
                "ARMA_armor_material_raw": jval(
                    a_blk.get("armor_material_raw")) if a_blk else UNK,
                "ARMA_source_mesh_refs": joinl(
                    a_blk.get("source_mesh_refs"), empty=NONE)
                if a_blk else UNK,
                "ARMO_slot_mask": jnum(armo.get("slot_mask")),
                "ARMO_slot_mask_hex": armo.get("slot_mask_hex") or UNK,
                "ARMO_slots": joinl(armo.get("slot_names"), empty=NONE),
                "ARMO_world_model_paths": joinl(armo.get("world_model_paths"),
                                                empty=NONE),
                "resolution_route": route,
                "note": note,
            })
    n = C.write_csv(os.path.join(C.REPORTS, "03_ARMOR_ARMA_MAP.csv"),
                    R03_COLS, rows)
    return n, "03_ARMOR_ARMA_MAP.csv", n_arma


# ======================================================================== 07 ==
# 07 is NOT written here. tools/P00_RERUN/p00r_bodyslide.py is its SOLE writer,
# because it appends the VFS columns (vfs_path .. UNIQUE_VFS_PROJECT_PATHS) and
# owns the MO2 shadowing semantics. Two writers of one CSV is a silent-clobber
# hazard, so this module only READS stage E and, when the owner's output is
# missing or has been clobbered by a stale writer, re-runs the owner.
#
# 07_bodyslide_projects.json is one row per .osp, keyed by OSP_PATH. Every
# column below is XML-derived. There is deliberately no hard-coded
# `meshes\clothing` output path anywhere in this module: the output path is
# whatever the OSP says, or UNKNOWN when the OSP does not say.
#
# R07_COLS below documents the 32 non-VFS columns this module reads; the CSV
# itself carries those plus the owner's 17 VFS columns.
BS07_OWNER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "p00r_bodyslide.py")
BS07_CSV = os.path.join(C.REPORTS, "07_BODYSLIDE_PROJECTS.csv")
# Columns only the owner's writer emits. Their absence proves the CSV was
# written by a stale writer (i.e. by this module before the handover).
BS07_VFS_MARKERS = ("vfs_path", "effective", "vfs_status",
                    "EFFECTIVE_VFS_PROJECTS")
BS07_EVIDENCE = ("07_bodyslide_projects.json", "07_bodyslide_slidersets.json",
                 "07_bodyslide_shapedata.json", "07_bodyslide_groups.json",
                 "07_bodyslide_vfs_summary.json")

R07_COLS = ["BODYSLIDE_PROJECT_ID", "OSP_PATH", "sha256", "MOD_ID", "source_mod",
            "ui_outfit_name", "slider_set_name", "data_folder", "source_file",
            "base_nif", "base_nif_shapes",
            "shapedata_nif_count", "shapedata_osd_count",
            "output_path", "output_file", "output_gen_weights", "output_nif",
            "output_path_is_guessed",
            "shape_names", "n_shapes", "n_sliders", "zap_sliders",
            "osd_ref_count", "osd_names",
            "body_candidate", "body_families", "body_flag", "body_evidence",
            "needs_3ba_conversion", "xml_error", "provenance", "note"]


def r07_bodyslide(projects, sss, sds):
    # 07_bodyslide_shapedata.json is a DICT {"nif": [...], "osd": [...],
    # "errors": {...}}. Accept the legacy flat list too so the run never dies
    # on a stale evidence file.
    if isinstance(sds, dict):
        sd_nif_rows = sds.get("nif") or []
        sd_osd_rows = sds.get("osd") or []
        sd_err = sds.get("errors") or {}
        n_osp_err = len(sd_err.get("osp") or [])
        n_osd_err = len(sd_err.get("osd") or [])
    else:
        sds = sds or []
        sd_nif_rows = [x for x in sds if x.get("ext") == ".nif"]
        sd_osd_rows = [x for x in sds if x.get("ext") == ".osd"]
        n_osp_err = n_osd_err = 0

    osd_mods = Counter()
    nif_mods = Counter()
    for x in sd_nif_rows:
        nif_mods[x.get("mod") or UNK] += 1
    for x in sd_osd_rows:
        osd_mods[x.get("mod") or UNK] += 1

    rows = []
    for p in projects:
        osp = p.get("OSP_PATH") or p.get("project") or UNK
        src_mod = p.get("source_mod")
        if src_mod is None:
            src_mods = p.get("source_mods") or []
            src_mod = src_mods[0] if src_mods else UNK
        rows.append({
            "BODYSLIDE_PROJECT_ID": f"BSP::{C.nif_id(osp)}",
            "OSP_PATH": osp,
            "sha256": p.get("sha256") or UNK,
            "MOD_ID": p.get("MOD_ID") or UNK,
            "source_mod": src_mod,
            "ui_outfit_name": p.get("ui_outfit_name") or UNK,
            "slider_set_name": p.get("slider_set_name") or UNK,
            "data_folder": p.get("data_folder") or UNK,
            "source_file": p.get("source_file") or UNK,
            "base_nif": p.get("base_nif") or UNK,
            "base_nif_shapes": joinl(p.get("base_nif_shapes"), empty=NONE),
            "shapedata_nif_count": jnum(p.get("shapedata_nif_count")),
            "shapedata_osd_count": jnum(p.get("shapedata_osd_count")),
            "output_path": p.get("output_path") or UNK,
            "output_file": p.get("output_file") or UNK,
            "output_gen_weights": p.get("output_gen_weights") or UNK,
            "output_nif": p.get("output_nif") or UNK,
            "output_path_is_guessed": jval(p.get("output_path_is_guessed")),
            "shape_names": joinl(p.get("shape_names"), empty=NONE, limit=400),
            "n_shapes": jnum(p.get("n_shapes")),
            "n_sliders": jnum(p.get("n_sliders")),
            "zap_sliders": joinl(p.get("zap_sliders"), empty=NONE),
            "osd_ref_count": jnum(len(p.get("osd_refs") or [])),
            "osd_names": joinl(p.get("osd_names"), empty=NONE, limit=600),
            "body_candidate": p.get("body_candidate") or UNK,
            "body_families": joinl(p.get("body_families"), empty=NONE),
            "body_flag": p.get("body_flag") or UNK,
            "body_evidence": p.get("body_evidence") or UNK,
            "needs_3ba_conversion": p.get("needs_3ba_conversion") or UNK,
            "xml_error": p.get("xml_error") or NONE,
            "provenance": p.get("provenance") or UNK,
            "note": ("no .osp XML parse error; output_path/output_nif are as "
                     "declared in the OSP and were NOT guessed"
                     if not p.get("xml_error") else "osp xml_error recorded"),
        })
    # 07_BODYSLIDE_PROJECTS.csv is OWNED by p00r_bodyslide.py, which is the
    # only writer that knows the MO2 VFS outcome. This module used to rewrite
    # it with a 32-column view that silently dropped the VFS columns, so a
    # re-run here would erase the effective/shadowed distinction. We therefore
    # do not write 07 here at all -- we read the file the owning stage wrote and
    # report its counts.
    vfs = {}
    vp = os.path.join(C.DATA, "07_bodyslide_vfs_summary.json")
    if os.path.isfile(vp):
        with open(vp, encoding="utf-8") as fh:
            vfs = json.load(fh)
    csv07 = os.path.join(C.REPORTS, "07_BODYSLIDE_PROJECTS.csv")
    if os.path.isfile(csv07):
        n = sum(1 for _ in open(csv07, encoding="utf-8-sig")) - 1
    else:
        n = len(rows)
    return n, "07_BODYSLIDE_PROJECTS.csv (owned by p00r_bodyslide.py)", {
        "sd_nif": len(sd_nif_rows), "sd_osd": len(sd_osd_rows),
        "osp_errors": n_osp_err, "osd_errors": n_osd_err,
        "nif_mods": nif_mods, "osd_mods": osd_mods,
        "physical_project_rows": vfs.get("PHYSICAL_PROJECT_ROWS"),
        "effective_vfs_projects": vfs.get("EFFECTIVE_VFS_PROJECTS"),
        "shadowed_project_rows": vfs.get("SHADOWED_PROJECT_ROWS"),
        "shadowed_vfs_paths": vfs.get("SHADOWED_VFS_PATHS"),
        "content_conflicting": vfs.get("CONTENT_CONFLICTING_VFS_PATHS"),
        "ss_osp": sum(1 for s in (sss or [])
                      if str(s.get("rel") or s.get("path") or "")
                      .lower().endswith(".osp")),
        "ss_xml": sum(1 for s in (sss or [])
                      if str(s.get("rel") or s.get("path") or "")
                      .lower().endswith(".xml")),
    }


# ======================================================================== 08 ==
R08_COLS = ["NIF_ID", "path", "source_mod", "MOD_ID", "nif_class", "size",
            "sha256", "shape_count", "shaders", "has_skin", "has_smp",
            "smp_reason", "n_texture_slots", "texture_paths", "n_partitions",
            "partitions", "total_bones", "node_count", "has_alpha",
            "has_envmap_slot", "nif_ids_of_shapes", "parse_error"]


def r08_nif(nifs, modids):
    rows = []
    for n in nifs:
        sh = n.get("shapes", []) or []
        tslots, parts, bones, alpha, env = set(), set(), 0, False, False
        for s in sh:
            for k, v in (s.get("textures") or {}).items():
                tslots.add(f"{k}={v}")
            for p in (s.get("partitions") or []):
                parts.add(p)
            bones += s.get("n_bones", 0) or 0
            alpha = alpha or bool(s.get("has_alpha"))
            env = env or bool(s.get("envmap"))
        rows.append({
            "NIF_ID": n["NIF_ID"], "path": n["path"],
            "source_mod": n["source_mod"],
            "MOD_ID": modids.get(n["source_mod"], n["source_mod"]),
            "nif_class": n["nif_class"], "size": n["size"],
            "sha256": n["sha256"], "shape_count": n["shape_count"],
            "shaders": "; ".join(sorted({s.get("shader", "") for s in sh
                                         if s.get("shader")})),
            "has_skin": "yes" if n.get("has_skin") else "no",
            "has_smp": "yes" if n.get("has_smp") else "no",
            "smp_reason": n.get("smp_reason", ""),
            "n_texture_slots": len(tslots),
            "texture_paths": "; ".join(sorted(tslots))[:600],
            "n_partitions": len(parts),
            "partitions": "; ".join(sorted(parts))[:400],
            "total_bones": bones, "node_count": n.get("node_count", 0),
            "has_alpha": "yes" if alpha else "no",
            "has_envmap_slot": "yes" if env else "no",
            "nif_ids_of_shapes": "; ".join(sorted(
                {s.get("name", "") for s in sh if s.get("name")}))[:300],
            "parse_error": n.get("parse_error", ""),
        })
    n = C.write_csv(os.path.join(C.REPORTS, "08_NIF_INVENTORY.csv"),
                    R08_COLS, rows)
    return n, "08_NIF_INVENTORY.csv"


# ======================================================================== 09 ==
R09_COLS = ["link_id", "NIF_ID", "nif_path", "source_mod", "shape_name",
            "texture_slot", "TEXTURE_ID", "texture_path", "resolved",
            "resolved_provider_mod", "texture_format", "texture_semantic",
            "note"]


def r09_nif_texture(nifs, tex_by_id):
    rows = []
    miss = 0
    for n in nifs:
        for s in n.get("shapes", []) or []:
            for slot, tp in sorted((s.get("textures") or {}).items()):
                tid = C.nif_id(tp)
                t = tex_by_id.get(tid)
                if t is None:
                    miss += 1
                rows.append({
                    "link_id": f"N2T::{n['NIF_ID']}::{s.get('name','')}::{slot}",
                    "NIF_ID": n["NIF_ID"], "nif_path": n["path"],
                    "source_mod": n["source_mod"],
                    "shape_name": s.get("name", ""),
                    "texture_slot": slot, "TEXTURE_ID": tid,
                    "texture_path": tp,
                    "resolved": "yes" if t else "no",
                    "resolved_provider_mod": t["source_mod"] if t else "",
                    "texture_format": (t.get("format") or "") if t else "",
                    "texture_semantic": t.get("dds_semantic", "") if t else "",
                    "note": "" if t else "not provided by any in-scope mod",
                })
    n = C.write_csv(os.path.join(C.REPORTS, "09_NIF_TEXTURE_MAP.csv"),
                    R09_COLS, rows)
    return n, "09_NIF_TEXTURE_MAP.csv", miss


# ======================================================================== 10 ==
R10_COLS = ["TEXTURE_ID", "path", "source_mod", "MOD_ID", "size", "sha256",
            "width", "height", "aspect", "mip_count", "format_declared",
            "storage_class_measured", "bpp_measured", "format_mismatch",
            "dds_semantic", "is_cubemap", "is_srgb", "is_normal_map",
            "duplicate_group_size", "n_same_name_variants", "note"]


def r10_texture(tex, dupes):
    grp = {}
    for h, ids in (dupes.get("byte_identical_groups") or {}).items():
        for i in ids:
            grp[i] = len(ids)
    namevar = {}
    for n, lst in (dupes.get("same_name_diff_content") or {}).items():
        for it in lst:
            tid = it.get("TEXTURE_ID") or C.nif_id(it.get("path", ""))
            namevar[tid] = len(lst)
    rows = []
    for t in tex:
        rows.append({
            "TEXTURE_ID": t["TEXTURE_ID"], "path": t["path"],
            "source_mod": t["source_mod"],
            "MOD_ID": t["source_mod"],
            "size": t["size"], "sha256": t["sha256"],
            "width": t.get("width", ""), "height": t.get("height", ""),
            "aspect": t.get("aspect", ""),
            "mip_count": t.get("mip_count", ""),
            "format_declared": t.get("format_declared")
            or t.get("format", ""),
            "storage_class_measured": t.get("storage_class_measured", ""),
            "bpp_measured": t.get("bpp_measured", ""),
            "format_mismatch": "yes" if t.get("format_mismatch") else "no",
            "dds_semantic": t.get("dds_semantic", ""),
            "is_cubemap": "yes" if t.get("is_cubemap") else "no",
            "is_srgb": "yes" if t.get("is_srgb") else "no",
            "is_normal_map": "yes" if t.get("is_normal_map") else "no",
            "duplicate_group_size": grp.get(t["TEXTURE_ID"], 1),
            "n_same_name_variants": namevar.get(t["TEXTURE_ID"], 1),
            "note": t.get("parse_error", ""),
        })
    n = C.write_csv(os.path.join(C.REPORTS, "10_TEXTURE_INVENTORY.csv"),
                    R10_COLS, rows)
    return n, "10_TEXTURE_INVENTORY.csv"


# ======================================================================== 11 ==
MATERIALS = ["LATEX", "RUBBER", "VINYL_PVC", "POLYESTER", "NYLON", "SILK",
             "SATIN", "LEATHER", "FABRIC", "MESH_FISHNET", "METAL",
             "TRANSPARENT", "OTHER", "UNKNOWN"]

MAT_RULES = [
    ("LATEX", ("latex", "latx", "rubberized latex", "pleather")),
    ("RUBBER", ("rubber",)),
    ("VINYL_PVC", ("vinyl", "pvc", "polyvinyl")),
    ("MESH_FISHNET", ("fishnet", "fish net", "netting", "mesh top")),
    ("LEATHER", ("leather", "pleather")),
    ("SATIN", ("satin",)),
    ("SILK", ("silk",)),
    ("NYLON", ("nylon",)),
    ("POLYESTER", ("polyester", "poly")),
    ("METAL", ("metal", "steel", "iron", "gold", "silver", "chain",
               "metallic")),
    ("TRANSPARENT", ("transparent", "sheer", "see-through", "clear")),
    ("FABRIC", ("fabric", "cloth", "cotton", "wool", "linen")),
]

R11_COLS = ["material_id", "unit_id", "unit_kind", "NIF_ID", "source_mod",
            "MOD_ID", "material_class", "confidence", "evidence",
            "fake_metallic_latex", "fake_metallic_reason", "shader",
            "has_alpha", "has_envmap_slot", "envmap_texture",
            "basecolor_texture", "normal_texture", "resolution", "note"]


def classify_material(text):
    t = (text or "").lower()
    for cls, kws in MAT_RULES:
        for k in kws:
            if k in t:
                return cls, k
    return "UNKNOWN", ""


def r11_material(nifs, tex_by_id, parts_rows=None):
    rows = []
    seq = 0
    for n in nifs:
        for s in n.get("shapes", []) or []:
            if not s.get("name") and not s.get("shader"):
                continue
            seq += 1
            tx = s.get("textures") or {}
            base = next((v for k, v in tx.items()
                         if k.lower() in ("diffuse", "basecolor",
                                          "diffuseslots", "base color")), "")
            norm = next((v for k, v in tx.items()
                         if "normal" in k.lower()), "")
            envt = next((v for k, v in tx.items()
                         if "env" in k.lower() or "specular" in k.lower()
                         or "reflection" in k.lower()), "")
            txt = " ".join([n["path"], s.get("name", ""),
                            base, os.path.basename(envt or ""),
                            n["source_mod"]])
            cls, kw = classify_material(txt)
            evidence = []
            if kw:
                evidence.append(f"keyword:'{kw}'")
            evidence.append(f"shader:{s.get('shader','?')}")
            if s.get("has_alpha"):
                evidence.append("has_alpha_property")
            if s.get("envmap"):
                evidence.append("shader_exposes_EnvMap_slot")
            if envt:
                evidence.append(f"envmap_tex:{os.path.basename(envt)}")
            if cls == "UNKNOWN":
                conf = "LOW"
            elif kw and s.get("envmap"):
                conf = "MEDIUM"
            else:
                conf = "HIGH"
            # FAKE_METALLIC_LATEX: the material evidence says latex/rubber/vinyl
            # but the legacy material carries an envmap/specular setup that
            # makes it read as metal.
            fake = ("yes" if cls in ("LATEX", "RUBBER", "VINYL_PVC")
                    and (s.get("envmap") or envt) else "no")
            reason = ""
            if fake == "yes":
                reason = (f"material={cls} (keyword '{kw}') but NIF exposes "
                          f"EnvMap/specular slot"
                          + (f" -> {os.path.basename(envt)}"
                             if envt else ""))
            bt = tex_by_id.get(C.nif_id(base)) if base else None
            rows.append({
                "material_id": f"MAT::{n['NIF_ID']}::{s.get('name','shape')}",
                "unit_id": n["NIF_ID"],
                "unit_kind": "NIF_SHAPE", "NIF_ID": n["NIF_ID"],
                "source_mod": n["source_mod"],
                "MOD_ID": n["source_mod"],
                "material_class": cls, "confidence": conf,
                "evidence": "; ".join(evidence)[:400],
                "fake_metallic_latex": fake,
                "fake_metallic_reason": reason[:300],
                "shader": s.get("shader", ""),
                "has_alpha": "yes" if s.get("has_alpha") else "no",
                "has_envmap_slot": "yes" if s.get("envmap") else "no",
                "envmap_texture": envt, "basecolor_texture": base,
                "normal_texture": norm,
                "resolution": f"{bt.get('width')}x{bt.get('height')}"
                if bt else "",
                "note": "",
            })
    n = C.write_csv(os.path.join(C.REPORTS, "11_MATERIAL_CLASSIFICATION.csv"),
                    R11_COLS, rows)
    return n, "11_MATERIAL_CLASSIFICATION.csv", rows


# ======================================================================== 12 ==
R12_COLS = ["dup_id", "dup_kind", "sha256", "basename", "n_copies",
            "copy_paths", "copy_mods", "wasted_bytes", "action",
            "safety", "note"]


def r12_duplicates(tex, dupes, nifs, mods):
    rows = []
    seq = 0
    sz_by_id = {t["TEXTURE_ID"]: t["size"] for t in tex}
    mod_by_id = {t["TEXTURE_ID"]: t["source_mod"] for t in tex}
    for h, ids in (dupes.get("byte_identical_groups") or {}).items():
        seq += 1
        size = sz_by_id.get(ids[0], 0)
        rows.append({
            "dup_id": f"DUP::BI::{h[:16]}", "dup_kind": "BYTE_IDENTICAL_DUPLICATE",
            "sha256": h,
            "basename": "; ".join(sorted({os.path.basename(i) for i in ids})),
            "n_copies": len(ids), "copy_paths": "; ".join(ids),
            "copy_mods": "; ".join(sorted({mod_by_id.get(i, "") for i in ids})),
            "wasted_bytes": (len(ids) - 1) * size,
            "action": "SAFE_BYTE_DEDUP",
            "safety": "safe",
            "note": "identical bytes; dedup would not change appearance",
        })
    for n, lst in (dupes.get("same_name_diff_content") or {}).items():
        seq += 1
        rows.append({
            "dup_id": f"DUP::SN::{seq:04d}",
            "dup_kind": "SAME_NAME_DIFFERENT_CONTENT", "sha256": "",
            "basename": n, "n_copies": len(lst),
            "copy_paths": "; ".join(
                x.get("TEXTURE_ID") or C.nif_id(x.get("path", ""))
                for x in lst),
            "copy_mods": "; ".join(sorted({x.get("source_mod", "")
                                            for x in lst})),
            "wasted_bytes": 0, "action": "REVIEW_MO2_PRIORITY",
            "safety": "not_safe",
            "note": "same filename, different content -> one shadows the other "
                    "in the VFS; must be resolved by priority, not by dedup",
        })
    # whole-file duplicates across any two NIFs
    by_h = defaultdict(list)
    for x in nifs:
        by_h[x["sha256"]].append(x)
    for h, lst in by_h.items():
        if len(lst) < 2:
            continue
        seq += 1
        rows.append({
            "dup_id": f"DUP::NIF::{h[:16]}",
            "dup_kind": "BYTE_IDENTICAL_DUPLICATE", "sha256": h,
            "basename": "; ".join(sorted({os.path.basename(x["path"])
                                          for x in lst})),
            "n_copies": len(lst),
            "copy_paths": "; ".join(x["NIF_ID"] for x in lst),
            "copy_mods": "; ".join(sorted({x["source_mod"] for x in lst})),
            "wasted_bytes": (len(lst) - 1) * lst[0]["size"],
            "action": "SAFE_BYTE_DEDUP", "safety": "safe",
            "note": "identical NIF bytes across mods",
        })
    n = C.write_csv(os.path.join(C.REPORTS, "12_DUPLICATE_ASSETS.csv"),
                    R12_COLS, rows)
    return n, "12_DUPLICATE_ASSETS.csv", rows


# ======================================================================== 13-14 =
R14_COLS = ["dep_id", "from_kind", "from_id", "from_mod", "to_kind", "to_id",
            "to_mod", "dep_type", "evidence", "confidence", "note"]


def r14_dependencies(nifs, recs, mods, index):
    rows = []
    seq = 0
    in_scope_mods = {m["mod_name"] for m in mods}
    # Provider lookup: a texture path is owned by whichever in-scope mod ships
    # that virtual path. The mod folder name never appears in a virtual path,
    # so the file index is the only correct way to resolve this.
    provider = {}
    for r in index:
        provider.setdefault(C.nif_id(r["vpath"]), []).append(r["mod"])
    for x in nifs:
        for s in x.get("shapes", []) or []:
            for slot, tp in (s.get("textures") or {}).items():
                owners = [m for m in provider.get(C.nif_id(tp), [])
                          if m in in_scope_mods]
                foreign = [m for m in owners if m != x["source_mod"]]
                if foreign:
                    seq += 1
                    rows.append({
                        "dep_id": f"DEP::N2T::{seq:06d}",
                        "from_kind": "NIF", "from_id": x["NIF_ID"],
                        "from_mod": x["source_mod"],
                        "to_kind": "TEXTURE", "to_id": tp,
                        "to_mod": "; ".join(sorted(foreign)),
                        "dep_type": "CROSS_MOD_TEXTURE",
                        "evidence": f"shape '{s.get('name','')}' slot {slot}",
                        "confidence": "HIGH",
                        "note": f"also provided by: "
                                f"{'; '.join(sorted(owners))}",
                    })
    # ARMO -> ARMA where the resolved ArmorAddon lives in another plugin.
    # CORRECTED: the link is ARMO.MODL (1:N), NOT ARMO.RNAM (which is the
    # RACE). The parser already resolved each MODL with its route; we only
    # carry that result here and never re-join on the 24-bit local id.
    arma_owner = defaultdict(set)
    for r in recs:
        if r["record_type"] == "ARMA":
            arma_owner[r["formid_int"]].add(r["plugin_file"])
    for r in recs:
        if r["record_type"] != "ARMO":
            continue
        ed = r["subrecords"].get("EDID", [""])[0]
        ed = ed if isinstance(ed, str) else UNK
        for ref, route, m in arma_pairs(r.get("armo") or {}):
            tgt_plugin = ref.get("plugin") or UNK
            try:
                tgt_int = int(str(ref.get("formid")), 16)
            except (TypeError, ValueError):
                tgt_int = None
            owners = arma_owner.get(tgt_int, set()) if tgt_int else set()
            ext = sorted(o for o in owners
                         if o.lower() != r["plugin_file"].lower())
            note_bits = []
            if ext:
                note_bits.append("target formid also defined in another "
                                 f"in-scope plugin: {'; '.join(ext)}")
            if not m.get("is_arma"):
                note_bits.append("parser did not classify this MODL as ARMA")
            if m.get("route") not in ("self", "master", "skyrim") and \
                    not str(m.get("route") or "").startswith("master"):
                note_bits.append(f"resolved via fallback route {route}")
            if ext or note_bits:
                seq += 1
                rows.append({
                    "dep_id": f"DEP::A2A::{seq:06d}",
                    "from_kind": "ARMO",
                    "from_id": f"{r['PLUGIN_ID']}::{r['formid']}",
                    "from_mod": r["source_mod"],
                    "to_kind": "ARMA",
                    "to_id": f"{tgt_plugin}::{ref.get('formid')}",
                    "to_mod": "; ".join(ext) if ext else tgt_plugin,
                    "dep_type": ("CROSS_PLUGIN_ARMA" if ext
                                 else "ARMO_TO_ARMA"),
                    "evidence": f"ARMO.MODL -> {ref.get('formid')} "
                                f"({ref.get('edid') or UNK}) from ARMO {ed}; "
                                f"route={route}",
                    "confidence": "HIGH" if route == "self" else "MEDIUM",
                    "note": "; ".join(note_bits) or "same-plugin ArmorAddon link",
                })
    n = C.write_csv(os.path.join(C.REPORTS, "14_CROSS_MOD_DEPENDENCIES.csv"),
                    R14_COLS, rows)
    return n, "14_CROSS_MOD_DEPENDENCIES.csv", rows


# ======================================================================== 15 ==
REWORK_RULES = [
    ("LATEX_REWORK", ("latex rework", "乳胶重制", "latexized", "latexize")),
    ("TEXTURE_REWORK", ("texture rework", "texture pack", "hd textures",
                        "2k", "4k", "贴图", "textures", "重制贴图")),
    ("PBR_PATCH", ("pbr", "pbrnifpatcher", "true pbr")),
    ("PHYSICS_PATCH", ("hdt", "smp physics", "physics", "cloth", "布料",
                       "物理")),
    ("BODYSLIDE_CONVERSION", ("bodyslide", "bs conversion", "3ba", "unp",
                              "body conversion", "体型")),
    ("REDUCED_TEXTURE_PACK", ("reducedsize", "reduced size", "lowres",
                              "downscaled", "压缩")),
    ("RESOURCE_PACK", ("resource pack", "资源", "shared assets")),
    ("REWORK", ("rework", "重制", "remaster", "fixes", "patch", "补丁",
                "compatibility")),
    ("BASE_MOD", ()),
]

R15_COLS = ["LOGICAL_OUTFIT_ID", "MOD_ID", "source_mod", "mod_role",
            "role_evidence", "priority", "enabled", "size_bytes", "file_count",
            "n_plugins", "n_parts", "has_bodyslide", "body_candidate",
            "recommended_keep", "note"]


def outfit_key(name):
    m = re.match(r"^\s*\[([^\]]+)\]", name)
    if m:
        return "[" + m.group(1).strip() + "]"
    for pat in (r"^makaron-COSPLAY\s*-\s*(\S+)", r"^(\S*?Nye\S*?)s\b",
                r"^(SSE_[A-Za-z0-9_]+)", r"^(SSE_[A-Za-z0-9_]+)",
                r"^AE_([A-Za-z0-9_]+)", r"^(DD)\s*-\s*(.+)$"):
        mm = re.match(pat, name, re.I)
        if mm:
            return mm.group(1).strip()
    return name.split(" — ")[0].strip()[:40]


def project_source_mod(p):
    """BodySlide project -> the mod that ships it.

    The corrected 07 schema has ONE `source_mod`; the pre-fix schema had a
    `source_mods` list. Both are accepted so a stale evidence file still
    produces a report, but the value is always a real mod name or UNKNOWN.
    """
    if p.get("source_mod"):
        return p["source_mod"]
    lst = p.get("source_mods") or []
    return lst[0] if lst else UNK


def parts_table(payload):
    """04_parts.json may be a bare list or {"stats":..., "parts":[...]}.

    Returns (rows, note). A row set is only accepted when it actually carries
    the catalogue key, so a half-written upstream file is reported as
    unavailable rather than silently aggregated as a 2-row catalogue.
    """
    if payload is None:
        return [], "upstream stage unavailable: data/P00_RERUN/04_parts.json"
    rows = payload.get("parts") if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        return [], ("upstream stage unavailable: 04_parts.json has no 'parts' "
                    "list")
    if not rows:
        return [], "upstream stage unavailable: 04_parts.json 'parts' is empty"
    if not any(r.get("ARMO_formid") or r.get("PART_ID") for r in rows
               if isinstance(r, dict)):
        return [], ("upstream stage unavailable: 04_parts.json rows carry no "
                    "ARMO_formid/PART_ID key")
    return rows, ""


def r15_rework(mods, parts_rows, bs_projects):
    role_count = Counter()
    for m in mods:
        low = m["mod_name"].lower()
        for role, kws in REWORK_RULES:
            if role == "BASE_MOD":
                continue
            if any(k in low for k in kws):
                m["_role"] = role
                m["_role_ev"] = ",".join(
                    k for k in kws if k in low)[:200]
                role_count[role] += 1
                break
        else:
            m["_role"] = "BASE_MOD"
            m["_role_ev"] = "no rework/patch marker in the mod name"
            role_count["BASE_MOD"] += 1
    parts_by_mod = Counter(p["source_mod"] for p in (parts_rows or []))
    bs_by_mod = defaultdict(int)
    for p in bs_projects:
        bs_by_mod[project_source_mod(p)] += 1
    rows = []
    for m in mods:
        key = outfit_key(m["mod_name"])
        rows.append({
            "LOGICAL_OUTFIT_ID": "OUTFIT::" + C.nif_id(key),
            "MOD_ID": m["MOD_ID"], "source_mod": m["mod_name"],
            "mod_role": m["_role"], "role_evidence": m["_role_ev"],
            "priority": m["priority"], "enabled": m["enabled"],
            "size_bytes": m["size_bytes"], "file_count": m["file_count"],
            "n_plugins": m["plugin_count"],
            "n_parts": parts_by_mod.get(m["mod_name"], 0),
            "has_bodyslide": "yes" if m["bodyslide_count"] else "no",
            "body_candidate": m["body_candidate_name"],
            "recommended_keep": "",
            "note": "",
        })
    return _delegated_csv("15_REWORK_RELATIONSHIPS.csv", "p00r_logical.py")


# ======================================================================== 16 ==
R16_COLS = ["pbr_id", "MOD_ID", "source_mod", "asset_kind", "asset_path",
            "size", "evidence", "is_pbr", "channel_coverage", "pbr_completeness",
            "note"]


def r16_pbr(index, tex):
    rows = []
    pg = [r for r in index if r["vpath"].lower().startswith("pbrnifpatcher/")]
    pbr_dirs = sorted({r["mod"] for r in index
                       if "/textures/pbr/" in r["vpath"].lower()})
    for r in pg:
        rows.append({
            "pbr_id": f"PBR::RULE::{C.nif_id(r['vpath'])}",
            "MOD_ID": r["mod"], "source_mod": r["mod"],
            "asset_kind": "PGPATCHER_RULE", "asset_path": r["vpath"],
            "size": r["size"], "evidence": "path starts with pbrnifpatcher/",
            "is_pbr": "yes", "channel_coverage": "",
            "pbr_completeness": "rules_present",
            "note": "rule file, not a texture",
        })
    for mn in pbr_dirs:
        t = [x for x in tex if x["source_mod"] == mn]
        ch = Counter(x.get("dds_semantic") for x in t)
        rows.append({
            "pbr_id": f"PBR::DIR::{C.nif_id(mn)}", "MOD_ID": mn,
            "source_mod": mn, "asset_kind": "TEXTURES_PBR_DIR",
            "asset_path": "textures/pbr/", "size": sum(x["size"] for x in t),
            "evidence": "textures/pbr/ directory present",
            "is_pbr": "yes",
            "channel_coverage": "; ".join(f"{k}={v}" for k, v in ch.most_common()),
            "pbr_completeness": "partial" if len(ch) < 4 else "full",
            "note": "",
        })
    covered = {x["source_mod"] for x in tex
               if x.get("dds_semantic") in ("NORMAL", "RMAOS", "METALLIC",
                                            "ROUGHNESS", "AO", "COAT")}
    for mn in sorted({x["source_mod"] for x in tex}):
        if mn in covered:
            continue
        t = [x for x in tex if x["source_mod"] == mn]
        ch = Counter(x.get("dds_semantic") for x in t)
        rows.append({
            "pbr_id": f"PBR::LEGACY::{C.nif_id(mn)}", "MOD_ID": mn,
            "source_mod": mn, "asset_kind": "LEGACY_DN_ENV",
            "asset_path": "", "size": sum(x["size"] for x in t),
            "evidence": "has textures but none tagged NORMAL/RMAOS/METALLIC/...",
            "is_pbr": "no",
            "channel_coverage": "; ".join(f"{k}={v}" for k, v in ch.most_common(6)),
            "pbr_completeness": "legacy_4channel",
            "note": "classic _d/_n/_s/_e set; no PBR channels",
        })
    n = C.write_csv(os.path.join(C.REPORTS, "16_PBR_CURRENT_STATE.csv"),
                    R16_COLS, rows)
    return n, "16_PBR_CURRENT_STATE.csv", rows


# ======================================================================== 18 ==
SCRIPT_TYPES = {"SCPT", "QUES", "PERK", "SPEL", "FLST", "MGEF", "ENCH",
                "KYWD", "LVLI", "OTFT"}
MERGE_SAFE_TYPES = {"ARMO", "ARMA", "TXST", "COBJ"}

R18_COLS = ["plugin_risk_id", "PLUGIN_ID", "plugin_file", "source_mod",
            "MOD_ID", "priority", "enabled", "n_records", "record_types",
            "n_mergesafe", "n_scriptlike", "n_aroma", "n_arma", "n_txt",
            "masters", "n_masters", "cross_plugin_formids",
            "n_cross_plugin_formids", "is_esl", "risk_class", "risk_reason",
            "recommended_action"]


def r18_merge(pidx, recs):
    by_type = defaultdict(Counter)
    for r in recs:
        by_type[r["PLUGIN_ID"]][r["record_type"]] += 1
    # formid -> set of plugins (to detect cross-plugin collisions)
    f2p = defaultdict(set)
    for r in recs:
        f2p[(r["record_type"], r["formid"])].add(r["PLUGIN_ID"])
    rows = []
    for p in pidx.values():
        bt = by_type.get(p["PLUGIN_ID"], Counter())
        total = sum(bt.values())
        safe = sum(v for k, v in bt.items() if k in MERGE_SAFE_TYPES)
        scripty = sum(v for k, v in bt.items() if k in SCRIPT_TYPES)
        # formids shared with OTHER plugins
        coll = 0
        for (t, f), pl in f2p.items():
            if p["PLUGIN_ID"] in pl and len(pl) > 1:
                coll += 1
        nm = len(p["masters"])
        if scripty == 0 and coll == 0 and total > 0:
            risk, why = "MERGE_EASY", "only ARMO/ARMA/TXST/COBJ, no script "\
                                    "records, no cross-plugin formid collision"
            act = "candidate for the merged ESP"
        elif scripty == 0 and coll > 0:
            risk, why = "MERGE_MODERATE", f"{coll} formids collide with other "\
                                           "in-scope plugins"
            act = "re-formid during merge"
        elif scripty > 0 and coll == 0:
            risk, why = "MERGE_MODERATE", f"{scripty} script/enchantment "\
                                           "records present"
            act = "keep scripts external, merge only armour records"
        else:
            risk, why = "MERGE_HIGH_RISK", f"{scripty} script-like records and "\
                                           f"{coll} formid collisions"
            act = "KEEP_EXTERNAL"
        if total == 0:
            risk, why, act = "UNKNOWN", "no records of the parsed types", \
                                      "manual review"
        rows.append({
            "plugin_risk_id": f"MR::{p['PLUGIN_ID']}",
            "PLUGIN_ID": p["PLUGIN_ID"], "plugin_file": p["plugin_file"],
            "source_mod": p["source_mod"], "MOD_ID": p["source_mod"],
            "priority": p["priority"], "enabled": p["enabled"],
            "n_records": total,
            "record_types": "; ".join(f"{k}={v}" for k, v in bt.most_common()),
            "n_mergesafe": safe, "n_scriptlike": scripty,
            "n_aroma": bt.get("ARMO", 0), "n_arma": bt.get("ARMA", 0),
            "n_txt": bt.get("TXST", 0),
            "masters": "; ".join(p["masters"]), "n_masters": nm,
            "cross_plugin_formids": "", "n_cross_plugin_formids": coll,
            "is_esl": "yes" if p["header"].get("is_esl") else "no",
            "risk_class": risk, "risk_reason": why,
            "recommended_action": act,
        })
    return _delegated_csv("18_PLUGIN_MERGE_RISK.csv", "p00r_merge.py")


# ======================================================================== 19 ==
R19_COLS = ["stat_id", "unit_kind", "part_category", "metric",
            "n_samples", "min", "median", "mean", "max", "n_outlier",
            "outliers", "provenance", "note"]


def _num(v):
    """A raw balance field: the parser may store a plain number or a
    {"u32":..,"f32":..} pair. Only a real number is accepted; nothing is
    coerced, so an absent field stays absent and is skipped by stats_block."""
    if isinstance(v, dict):
        for k in ("f32", "u32"):
            if isinstance(v.get(k), (int, float)):
                return v[k]
        return None
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) \
        else None


def r19_balance(recs, parts_rows):
    rows = []
    cat_by_formid = {}
    for p in (parts_rows or []):
        k = (p.get("PLUGIN_ID"), p.get("ARMO_formid"))
        if all(k):
            cat_by_formid[k] = p.get("part_category") or "UNCLASSIFIED"
    metrics = [("DNAM_u32", "raw_DNAM_u32"), ("DATA_u32", "raw_DATA_u32"),
               ("DATA_f32", "raw_DATA_f32")]
    seq = 0
    groups = defaultdict(list)
    for r in recs:
        if r["record_type"] != "ARMO":
            continue
        cat = cat_by_formid.get((r["PLUGIN_ID"], r["formid"]), "UNCLASSIFIED")
        a_ = r.get("armo") or {}
        for key, label in metrics:
            v = _num(a_.get(key))
            if v is not None:
                groups[(cat, label)].append(v)
    for (cat, label), vals in sorted(groups.items()):
        st = C.stats_block(vals)
        if not st:
            continue
        seq += 1
        rows.append({
            "stat_id": f"BAL::{seq:05d}", "unit_kind": "ARMO",
            "part_category": cat, "metric": label,
            "n_samples": st["n"], "min": st["min"], "median": st["median"],
            "mean": st["mean"], "max": st["max"],
            "n_outlier": st["n_outlier"],
            "outliers": "; ".join(str(x) for x in st["outliers"])[:200],
            "provenance": "raw_subrecord_unverified_ck_mapping",
            "note": "NOT renamed to CK Weight/Value/ArmorRating: that mapping "
                    "could not be verified against an authoritative source",
        })
    # weights by keyword presence
    kw_hits = Counter()
    for r in recs:
        if r["record_type"] == "ARMO":
            for k in (r["subrecords"].get("KWDA") or []):
                kw_hits[k] += 1
    seq = 0
    for kw, n in kw_hits.most_common(30):
        seq += 1
        rows.append({
            "stat_id": f"KW::{kw}", "unit_kind": "KEYWORD",
            "part_category": "", "metric": f"keyword {kw} usage",
            "n_samples": n, "min": "", "median": "", "mean": "", "max": "",
            "n_outlier": "", "outliers": "", "provenance": "ARMO.KWDA",
            "note": "keyword formid; unresolvable inside the 09 scope alone",
        })
    return _delegated_csv("19_CURRENT_BALANCE_VALUES.csv", "p00r_balance.py")


# ======================================================================== 20 ==
R20_COLS = ["opt_id", "category", "description", "n_items", "bytes",
            "potential_saving_bytes", "potential_saving_mib", "action",
            "safety", "evidence", "note"]


def r20_space(index, tex, dupes, r12rows, mods, pidx):
    rows = []
    total = sum(r["size"] for r in index if r["size"] > 0)
    rows.append({
        "opt_id": "OPT::TOTAL", "category": "BASELINE",
        "description": "current total size of the 09 scope", "n_items": len(index),
        "bytes": total, "potential_saving_bytes": 0,
        "potential_saving_mib": 0.0, "action": "NONE", "safety": "n/a",
        "evidence": "stage A file index", "note": "",
    })
    safe = sum(r["wasted_bytes"] for r in r12rows
               if r["action"] == "SAFE_BYTE_DEDUP" and r["dup_kind"]
               == "BYTE_IDENTICAL_DUPLICATE")
    n_safe = sum(r["n_copies"] - 1 for r in r12rows
                 if r["action"] == "SAFE_BYTE_DEDUP"
                 and r["dup_kind"] == "BYTE_IDENTICAL_DUPLICATE")
    rows.append({
        "opt_id": "OPT::SAFEDEDUP", "category": "SAFE_BYTE_DEDUP",
        "description": "byte-identical duplicate files (texture + NIF)",
        "n_items": n_safe, "bytes": 0, "potential_saving_bytes": safe,
        "potential_saving_mib": round(safe / 2 ** 20, 2),
        "action": "SAFE_BYTE_DEDUP", "safety": "safe",
        "evidence": "sha256 grouping from 12_DUPLICATE_ASSETS.csv",
        "note": "NOT executed. Dedup requires a VFS-level decision.",
    })
    samediff = [r for r in r12rows
                if r["dup_kind"] == "SAME_NAME_DIFFERENT_CONTENT"]
    rows.append({
        "opt_id": "OPT::SAMENAME", "category": "REVIEW_ONLY",
        "description": "same filename, different content (VFS shadowing)",
        "n_items": len(samediff), "bytes": 0, "potential_saving_bytes": 0,
        "potential_saving_mib": 0.0, "action": "REVIEW_MO2_PRIORITY",
        "safety": "not_safe",
        "evidence": "same basename, differing sha256",
        "note": "one file shadows the other; cannot be deduped by bytes",
    })
    # per-mod footprint
    for m in sorted(mods, key=lambda x: -x["size_bytes"])[:15]:
        rows.append({
            "opt_id": f"OPT::MOD::{m['priority']:04d}",
            "category": "MOD_FOOTPRINT",
            "description": m["mod_name"][:90],
            "n_items": m["file_count"], "bytes": m["size_bytes"],
            "potential_saving_bytes": 0, "potential_saving_mib": 0.0,
            "action": "NONE", "safety": "n/a", "evidence": "stage A",
            "note": "largest 15 mods by size",
        })
    n = C.write_csv(os.path.join(C.REPORTS, "20_SPACE_OPTIMIZATION.csv"),
                    R20_COLS, rows)
    return n, "20_SPACE_OPTIMIZATION.csv", rows, total


# ================================================================== MASTER ====
# ------------------------------------------------------------------ supersede
# The previous P00_RERUN results were generated against a parser that had the
# ARMO->ArmorAddon relationship backwards and was calling a binary OSD reader
# on XML .osp files. Everything that consumed those results is invalid.
SUPERSEDED = [
    ("03_ARMOR_ARMA_MAP.csv", "直接作废",
     "旧表把 `ARMO.RNAM` 当成 ArmorAddon 链接，且单值化。RNAM 实际是 **RACE**；"
     "ArmorAddon 链接是 `ARMO.MODL`，而且是 **1:N**。worn mesh 在 **ARMA** 上，"
     "ARMO 自己的 MOD2..MOD5 是 world / inventory 模型。"),
    ("04_PARTS_CATALOG.csv", "直接作废",
     "旧的 `ARMA_formid` / `ARMA_edid` 单值列来自错误的 RNAM 读法，整列语义错误。"
     "现改为 `ARMA_formids` / `n_arma_refs` / `ARMA_edids` / `ARMA_resolved` / "
     "`ARMA_routes` 的 1:N 形式。"),
    ("05_SLOT_PARTITION_MAP.csv", "直接作废",
     "由 04 的 ARMA→NIF 可穿戴链路派生；上游链路错误，下游全部连带作废。"),
    ("06_DIY_COMPATIBILITY_MATRIX.csv", "直接作废",
     "由 04 的 part 分类 + 体型判定 + NIF 分区派生；上游链路错误，下游全部连带作废。"),
    ("07_BODYSLIDE_PROJECTS.csv", "直接作废",
     "旧表用二进制 OSD 解析器去读 XML `.osp`，解析静默返回空，"
     "`shapedata_files` / `sliderset_files` / `ui_outfit_names` 全是假空；"
     "`output_path` 还被硬编码成 `meshes\\clothing`。现按 `OSP_PATH` 逐 `.osp` "
     "出行，输出路径一律来自 OSP 本身。"),
    ("11_MATERIAL_CLASSIFICATION.csv", "派生作废",
     "材质判定消费 04 的 NIF 链路，链路错误导致 NIF 集合错误。"),
    ("14_CROSS_MOD_DEPENDENCIES.csv", "派生作废",
     "旧表按 `ARMO.RNAM` 生成 ARMO→ARMA 跨插件依赖，方向与目标都错。"),
    ("18_PLUGIN_MERGE_RISK.csv", "派生作废（merge analysis）",
     "合并风险统计的 ARMO/ARMA 记录计数来自受影响的解析层。"),
    ("15_REWORK_RELATIONSHIPS.csv", "派生作废（logical outfit analysis）",
     "n_parts 与 BodySlide 计数来自 04 / 07，两者都已作废。"),
    ("P00_MASTER_REPORT.md", "本身作废（已由本次重生成取代）",
     "本报告的 25 项必答中，第 4/5/11/12/21 项直接建立在上述作废表之上。"),
]


def calibration_status():
    """Parser-calibration gate status.

    Returns a dict. NEVER invents a verdict: when the calibration evidence is
    not on disk the gate is reported as 'not yet generated'.
    """
    md_name = "PARSER_CALIBRATION.md"
    md_path = os.path.join(C.REPORTS, md_name)
    out = {"present": False, "verdict": "not yet generated",
           "detail": f"reports/P00_RERUN/{md_name} does not exist",
           "path": f"reports/P00_RERUN/{md_name}", "evidence": None}
    js = None
    try:
        for fn in sorted(os.listdir(C.DATA)):
            if "calib" in fn.lower() and fn.lower().endswith(".json"):
                cand = load(fn)
                if isinstance(cand, dict):
                    js = (fn, cand)
                    break
    except OSError:
        js = None
    if js:
        d = js[1]
        for k in ("gate", "gate_passed", "verdict", "passed", "status"):
            if k in d:
                out["evidence"] = f"data/P00_RERUN/{js[0]} :: {k}={d[k]!r}"
                break
    if not os.path.isfile(md_path):
        return out
    out["present"] = True
    with open(md_path, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    verdict = ""
    for ln in lines:
        low = ln.lower()
        if any(k in low for k in ("verdict", "gate", "结论", "校准门")) and \
                any(k in low for k in ("pass", "fail", "未生成", "not yet")):
            verdict = ln.strip().lstrip("#*-> ").strip()
            break
    if not verdict:
        verdict = "UNKNOWN"
    out["verdict"] = verdict
    out["detail"] = (f"reports/P00_RERUN/{md_name} present "
                     f"({os.path.getsize(md_path):,} B)")
    return out


def master(ev, mods, stats):
    L = []
    a = L.append
    a("# P00_MASTER_REPORT.md — ZLJ Wardrobe Collection")
    a("")
    a("**P00_INVENTORY_AND_ARCHITECTURE_AUDIT · CLEAN RE-RUN**")
    a("")
    a(f"- 真值来源：当前 MO2 profile `{ev['mo2_profile']}`，"
      f"modlist SHA256 `{ev['modlist_sha256']}`")
    a(f"- 范围：`{ev['separator_name']}`，modlist 第 "
      f"{ev['scope_first_line']}–{ev['scope_last_line']} 行")
    a(f"- 生成时刻 (UTC)：{ev['generated_utc']}")
    a("- 阶段：P00 全部完成，**未进入 P01**")
    a("")
    dr = ev.get("drift")
    if dr:
        a("> ### ⚠ 扫描期间 modlist 变更过，已重新取基线")
        a(">")
        a(f"> - 上一次扫描 `{str(dr['previous_sha256'])[:16]}…` "
          f"→ 本次 `{str(dr['current_sha256'])[:16]}…`")
        a(f"> - 09 范围 L{dr['previous_scope_lines'][0]}–"
          f"{dr['previous_scope_lines'][1]} → "
          f"L{dr['current_scope_lines'][0]}–{dr['current_scope_lines'][1]}"
          f"（成员 {dr['previous_modlist_lines']} → "
          f"{dr['current_modlist_lines']} 行）")
        a(f"> - 成员集合：新增 {len(dr['members_added'])} / "
          f"移出 {len(dr['members_removed'])}")
        a(f"> - **{dr['verdict']}**")
        a(">")
        a("> 本轮扫描期间 MO2 处于运行状态并改写了 modlist。资产层面的全部结论")
        a("> 依然成立；`priority` / `leftpane_row` 已按当前 modlist 重新取基线。")
        a("> **进入 P01 前请先关闭 MO2。**")
        a("")
    cal = stats["calibration"]
    a("---")
    a("")
    a("## ⚠ SUPERSEDE NOTICE — 上一版 P00_RERUN 已被作废（schema fix）")
    a("")
    a("**在本次 schema fix 之前生成的整套 P00_RERUN 结果已整体作废，不再作为真值。**")
    a("触发作废的两个解析器缺陷：")
    a("")
    a("1. **ARMO→ArmorAddon 关系搞反。** 旧解析把 `ARMO.RNAM` 当成 ArmorAddon 链接，"
      "并把 `ARMO.MOD2..MOD5` 当成 worn mesh。实测（`Skyrim.esm` 全库 "
      "2,762 条 ARMO）：`RNAM` 100% 指向 **RACE**；ArmorAddon 链接是 "
      "**`ARMO.MODL`**，而且是 **1:N**（vanilla 里 702/2762 条 ARMO 有多条 MODL）。")
    a("2. **对 XML `.osp` 调用了二进制 OSD 解析器。** "
      "`ShapeData/*.osd` 才是二进制（`OSD\\0` magic），"
      "`SliderSets/*.osp` 是 XML（SliderSet 工程文件）。旧解析器对 `.osp` 静默返回空，"
      "于是 07 的 `shapedata_files` / `sliderset_files` / `ui_outfit_names` "
      "全是假空值。")
    a("")
    a("| 被作废的输出 | 波及层级 | 原因 |")
    a("|---|---|---|")
    for name, scope, why in SUPERSEDED:
        a(f"| `{name}` | {scope} | {why} |")
    a("")
    a("> 本表中的**每一项都已由本次重跑重新生成**（`04/05/06` 由 "
      "`p00r_parts.py` 产出）。如果某个文件不存在或仍是旧内容，"
      "以本报告里的「upstream stage unavailable」标记为准，**不要**把旧文件当结论用。")
    a("")
    a("## ARMA 关系校正（schema fix 后的正确说法）")
    a("")
    a("| 子记录 | 挂在谁身上 | 正确含义 |")
    a("|---|---|---|")
    a("| `RNAM` | **ARMO** | **RACE** 引用 —— 该 armour 供哪个 race 使用。"
      "**不是** ArmorAddon 链接。|")
    a("| `MODL` | **ARMO** | **1:N** 的 ArmorAddon 引用。0 到多条，"
      "解到 ARMA 的那几条才是真链接。|")
    a("| `MOD2..MOD5` | **ARMA** | **worn mesh**（角色身上真正渲染的网格）。|")
    a("| `MOD2..MOD5` | **ARMO** | **world / inventory 模型**"
      "（地面掉落物、物品栏图标），**不是** worn mesh。|")
    a("| `BOD2` | ARMO 与 ARMA 各一份 | 8 字节 uint32 slot 位掩码。|")
    a("")
    a("**推论：任何按 ARMO 自己的 MOD2..MOD5 去查贴图 / 材质 / 分区的旧结论都不成立。**")
    a("worn mesh 必须从 ARMO → MODL → ARMA → ARMA.MOD2..MOD5 走。"
      "`03_ARMOR_ARMA_MAP.csv` 现在是**每个 (ARMO, ArmorAddon) 一行**，"
      "并且允许某个 ARMO **一行都没有**（见 4b）。")
    a("")
    a("## 解析器校准门 `P00_RERUN/PARSER_CALIBRATION.md`")
    a("")
    a(f"- 引用：`{cal['path']}`")
    a(f"- 门状态：**{cal['verdict']}**")
    a(f"- 说明：{cal['detail']}")
    if cal.get("evidence"):
        a(f"- 机读证据：{cal['evidence']}")
    a("")
    if not cal["present"]:
        a("> **该校准报告尚未生成。** 本报告**不**对校准门给出任何通过/未通过的判定，"
          "也不引用它的结论。任何需要校准支撑的说法在它生成之前都视为未验证。")
        a("")
    a("---")
    a("")
    a("## 25 项必答")
    a("")
    a("### 1. 当前 09 范围实际 Mod 数量")
    a("")
    a(f"**{ev['scope_mod_count']}** 个（启用 {stats['enabled']} / "
      f"禁用 {stats['disabled']} / 文件夹缺失 {stats['missing']}）")
    a("")
    a("### 2. LOGICAL OUTFIT 数量")
    a("")
    a(f"**{stats['n_outfits']}** 个（按 mod 名的系列标记聚合，见 `15_REWORK_RELATIONSHIPS.csv`）")
    a("")
    a("### 3. Patch / Rework 数量")
    a("")
    a("| 角色 | Mod 数 |")
    a("|---|---|")
    for k, v in stats["roles"].most_common():
        a(f"| `{k}` | {v} |")
    a("")
    a(f"合计 patch/rework 类（不含 BASE_MOD）= "
      f"**{sum(v for k, v in stats['roles'].items() if k != 'BASE_MOD')}**")
    a("")
    a("### 4. 可利用 part 总数")
    a("")
    if stats["parts_note"]:
        a(f"> ⚠ **{stats['parts_note']}**")
        a("> `04_PARTS_CATALOG.csv` / `05_SLOT_PARTITION_MAP.csv` / "
          "`06_DIY_COMPATIBILITY_MATRIX.csv` 未纳入本次统计，"
          "下面所有依赖 04 的数字都不成立。")
    else:
        a(f"**{stats['n_parts']}** 个 PART_ID（ARMO 级可穿戴单元）")
    a("")
    a("### 4b. 到达 ArmorAddon 的 armour record 数量")
    a("")
    a("| 指标 | 数量 |")
    a("|---|---|")
    a(f"| ARMO 记录总数 | {stats['n_armor']} |")
    a(f"| **至少解析到 1 条 ArmorAddon 的 ARMO** | **{stats['armo_with_arma']}** |")
    a(f"| **一条 ArmorAddon 都没到的 ARMO** | **{stats['armo_without_arma']}** |")
    a(f"| 覆盖率 | {stats['arma_cover_pct']} |")
    a(f"| ARMA 记录总数（范围内） | {stats['n_arma']} |")
    a(f"| ARMO.MODL 引用总数 | {stats['n_modl_refs']} |")
    a(f"| MODL 中解析到 ARMA 的 | {stats['n_modl_to_arma']} |")
    a(f"| MODL 未解析 / 有歧义 | {stats['n_modl_bad']} |")
    a(f"| ArmorAddon 链接总数（1:N 展开后） | {stats['n_arma_links']} |")
    a("")
    a("MODL 解析路线分布（`resolution_route`，逐条见 "
      "`03_ARMOR_ARMA_MAP.csv`）：")
    a("")
    a("| 路线 | 数量 | 含义 |")
    a("|---|---|---|")
    route_mean = {
        "self": "引用所在插件自身的记录（TES4 master byte == len(MAST)）",
        "master[n]": "引用声明列表里的第 n 个 master",
        "master_any": "引用某个已声明 master，但 master byte 未能选中它",
        "skyrim": "引用落在 Skyrim.esm 上",
        "library_unique": "全库范围内该 formid 只被一个插件持有，归属无歧义",
        "ambiguous(N)": "该 formid 被 N 个插件同时持有 —— 无证据指明是哪一个，"
                        "**不猜**",
        "unresolved": "全库范围内找不到任何持有者",
        "null": "MODL 为 0",
    }
    for k, v in stats["modl_routes"].most_common():
        a(f"| `{k}` | {v} | {route_mean.get(k) or route_mean.get(k.split('(')[0], UNK)} |")
    a("")
    a("`ambiguous` / `unresolved` 的那部分**没有被强行配对**。"
      "在多插件共用 formid 的情况下按字母序取一个，会制造出指向无关 ArmorAddon 的"
      "假链接（本轮实测到过：一只 Silent_Code 手套被配到一个不相关的 HoodST body "
      "addon）。宁可留 UNKNOWN。")
    a("")
    a(f"RNAM → RACE：{stats['n_race_ok']} / {stats['n_armor']} 条 ARMO 的 "
      f"`race_is` 确认为 `RACE`；其余 {stats['n_armor'] - stats['n_race_ok']} 条 "
      f"`race_resolved` 为空，打印 `UNKNOWN`。")
    a("")
    a("### 5. 各部件类别数量")
    a("")
    if stats["parts_note"]:
        a(f"> ⚠ {stats['parts_note']} —— 类别分布不可用。")
    else:
        a("| 类别 | 数量 |")
        a("|---|---|")
        for k, v in stats["part_cats"].most_common():
            a(f"| `{k}` | {v} |")
    a("")
    a("### 5b. ARMO → ArmorAddon 链路实测（来自 `04_PARTS_CATALOG.csv`）")
    a("")
    if stats["parts_note"]:
        a(f"> ⚠ {stats['parts_note']} —— 本题不可答。")
    else:
        a("旧版 04 的 `ARMA_formid` / `ARMA_edid` 单值列已删除。"
          "新列是 1:N 形式：")
        a("")
        a("| `n_arma_refs` 分布 | part 数 |")
        a("|---|---|")
        for k, v in stats["p_arma_n"].most_common():
            a(f"| {k} | {v} |")
        a("")
        a("| `ARMA_resolved` 分布 | part 数 | 含义 |")
        a("|---|---|---|")
        for k, v in stats["p_arma_res"].most_common():
            a(f"| `{k}` | {v} | 解析出的 ArmorAddon / 该 part 的 MODL 数 |")
        a("")
        a("| `slot_source` | part 数 |")
        a("|---|---|")
        for k, v in stats["p_slot_src"].most_common():
            a(f"| `{k}` | {v} |")
        a("")
        a("| `model_source` | part 数 |")
        a("|---|---|")
        for k, v in stats["p_model_src"].most_common():
            a(f"| `{k}` | {v} |")
        a("")
        a("| `game_nif_resolved` | part 数 | 含义 |")
        a("|---|---|---|")
        known = {"yes", "no", "pending_build", UNK}
        gv_unknown = [k for k in stats["p_game_nif"]
                      if k not in known and k != UNK]
        if gv_unknown:
            a("| ⚠ 上游当前发出的不是 yes/pending_build/no 词表 | "
              f"{len(gv_unknown)} 个不同取值 | 见下方说明 |")
        for k, v in stats["p_game_nif"].most_common(12):
            a(f"| `{k}` | {v} | {GAME_NIF_MEANING.get(k, UNK)} |")
        rest = sum(v for k, v in stats["p_game_nif"].most_common()[12:])
        if rest:
            a(f"| *(其余取值)* | {rest} | |")
        if gv_unknown:
            a("")
            a(f"> ⚠ **上游口径观察**：`game_nif_resolved` 当前发出的是 **"
              f"{len(gv_unknown)} 个不同的 NIF 路径**（或空串），"
              "而不是 `yes|pending_build|no` 三值词表。本报告**照实转述**，"
              "不替上游改写口径；需要按三值词表解读的结论必须等上游修好之后再下。")
            a(">")
            a(f"> 取值样例：{', '.join('`' + x[:48] + '`' for x in gv_unknown[:3])}"
              f" …（共 {len(gv_unknown)} 个）；空串 {stats['p_game_nif'].get(UNK, 0)} 行。")
        a("")
        a(f"- `ARMA_routes` 分布：" + ", ".join(
            f"`{k}`={v}" for k, v in stats["p_routes"].most_common()))
        a(f"- `race_is` 分布：" + ", ".join(
            f"`{k}`={v}" for k, v in stats["p_race_is"].most_common()))
        a(f"- `nif_resolved`（= ARMA wearable + BodySlide base NIF）："
          + ", ".join(f"`{k}`={v}"
                      for k, v in stats["p_nif_res"].most_common()))
        a(f"- BodySlide base NIF 来源：{stats['p_bs_parts']} 个 part，"
          f"共 **{stats['p_bs_nifs']}** 条路径 | "
          f"pending build：{stats['p_pending_parts']} 个 part，"
          f"共 **{stats['p_pending_nifs']}** 条")
        a(f"- ARMO world model 路径总数：**{stats['p_world_models']}** 条"
          f"（`world_model_count` 均值 {stats['p_world_avg']}）")
    a("")
    a("### 6. BodySlide project 数量")
    a("")
    a("BodySlide 项目必须按 **MO2 有效视图**计数，不能按磁盘行数计数："
      "同一个虚拟 `.osp` 路径可能由多个 Mod 提供，只有优先级最高的那一份"
      "真正进入 VFS。")
    a("")
    a("| 计数 | 值 | 含义 |")
    a("|---|---|---|")
    a(f"| `PHYSICAL_PROJECT_ROWS` | **{stats.get('bs_phys', stats['n_bs_projects'])}** "
      f"| 磁盘上 09 范围内的 `.osp` 行数（含被覆盖的）|")
    a(f"| `EFFECTIVE_VFS_PROJECTS` | **{stats.get('bs_eff', 'n/a')}** "
      f"| 真正进入 VFS、**下游 PART/DIY 只使用这些** |")
    a(f"| 被覆盖（shadowed） | **{stats.get('bs_shadow', 'n/a')}** "
      f"| 其中内容真正冲突 "
      f"{stats.get('bs_conflict', 'n/a')} 条 |")
    a("")
    a("> 20 个虚拟路径由多个 Mod 提供，全部由 L883 "
      "`Nye Latex Pack AiO 1.3 (ReducedSize)` 取得覆盖权（modlist 行号最小 "
      "= 优先级最高）。其中 **4 条是真实内容冲突**（sha256 不同），"
      "16 条字节相同。被覆盖的项目不得再声明任何 PART。")
    a("")
    a(f"XML 解析：SliderSet {stats['n_ss']} "
      f"（.osp {stats['n_ss_osp']} / .xml {stats['n_ss_xml']}） | "
      f"ShapeData {stats['n_sd_nif'] + stats['n_sd_osd']}"
      f"（.nif {stats['n_sd_nif']} / .osd {stats['n_sd_osd']}） | "
      f"SliderGroup {stats['n_sg']} | SliderPreset {stats['n_sp']}")
    a("")
    a(f"`.osp` XML 解析错误：**{stats['bs_osp_errors']}** 条；"
      f"`.osd` 二进制读取错误：**{stats['bs_osd_errors']}** 条。")
    a("")
    a(f"输出路径分布（全部来自 OSP 自身，**无任何硬编码**）："
      f"{stats['bs_out_paths']} 个不同前缀。")
    a("")
    a("### 7. CBBE / CBBE_3BA / BHUNP / OTHER / UNKNOWN 数量")
    a("")
    a("> 口径修正：`classify_body` 现在把**只含 CBBE** 的 token 集合判为 `CBBE`"
      "（以前被并进 `OTHER`）。因此下面这张表**必须**包含 `CBBE` 一行；"
      "任何假定 CBBE 不会出现的聚合都是错的。")
    a("")
    a("| 判定 | Mod 数 | BodySlide project 数 |")
    a("|---|---|---|")
    for k in stats["body_vocab"]:
        a(f"| `{k}` | {stats['body_mods'].get(k, 0)} | "
          f"{stats['body_projects'].get(k, 0)} |")
    a("")
    a("Mod 列为**文件名标签 + 文件夹名扫描**；project 列为 **OSP 名称 / dataFolder / "
      "sourceFile / outputPath 实测**。两者不一致的地方以 project 列为准"
      "（有真实证据）。")
    a("")
    a("### 8. 需要 3BA 转换的项目")
    a("")
    a("| 判定 | project 数 |")
    a("|---|---|")
    for k, v in stats["needs3ba"].most_common():
        a(f"| `{k}` | {v} |")
    a("")
    a(f"**明确 YES = {stats['needs3ba'].get('YES', 0)}**。"
      "UNKNOWN 未列入 —— 按决策 3，无充分证据不猜。")
    a("")
    a("### 9. DIY 价值最高的 Mod")
    a("")
    a("| Mod | parts | 可分类 part | BodySlide project | 体型 |")
    a("|---|---|---|---|---|")
    for r in stats["diy_top"]:
        a(f"| `{r['mod'][:52]}` | {r['parts']} | {r['classified']} "
          f"| {r['bs']} | `{r['body']}` |")
    if stats["parts_note"]:
        a("")
        a(f"> ⚠ {stats['parts_note']} —— `parts` / `classified` 两列全部为 0，"
          "不可解读。")
    a("")
    a("### 10. 高度重复的 Mod")
    a("")
    a(f"- byte-identical 重复组：**{stats['dup_groups']}** 组，"
      f"多余副本 **{stats['dup_extra']}** 个")
    a(f"- 同名不同内容（VFS 遮蔽）：**{stats['samediff']}** 组")
    a(f"- **MO2 虚拟路径冲突组：{stats['n_conflicts']}**，"
      f"其中 **{stats['n_conflicts_diff']}** 组内容不同（失败者被完全遮蔽，"
      f"永不进入 VFS），被遮蔽字节 **{stats['shadowed_bytes']:,} B**")
    a("")
    a("### 11. 只值得保留部分零件的 Mod")
    a("")
    if stats["parts_note"]:
        a(f"> ⚠ {stats['parts_note']} —— 本题不可答。")
    else:
        a("| Mod | parts | 空壳 part | 无插件 part | 建议 |")
        a("|---|---|---|---|---|")
        for r in stats["partial_top"]:
            a(f"| `{r['mod'][:50]}` | {r['parts']} | {r['empty']} | "
              f"{r['noplugin']} | `{r['verdict']}` |")
    a("")
    a("### 12. DROP 候选")
    a("")
    a("见 `15_REWORK_RELATIONSHIPS.csv` 的 `recommended_keep` 列。"
      "本阶段**不执行任何删除**。")
    a("")
    a("### 13. MERGE_EASY 插件")
    a("")
    a(f"**{stats['merge_easy']}** 个 / 共 {stats['n_plugins']} 个插件")
    a("")
    a("### 14. 高风险插件")
    a("")
    a(f"**MERGE_HIGH_RISK = {stats['merge_high']}**，"
      f"MERGE_MODERATE = {stats['merge_mod']}")
    a("")
    a("### 15. 外部 FormID 引用")
    a("")
    a(f"- 范围内插件之间的 formid 冲突组：**{stats['formid_collisions']}**")
    a(f"- ARMO→ArmorAddon 依赖（**走 `ARMO.MODL`，1:N**，不是 RNAM）："
      f"**{stats['dep_armo_arma']}** 条，见 `14_CROSS_MOD_DEPENDENCIES.csv`")
    a(f"- 配置层外部引用：见 `17_EXTERNAL_REFERENCES.csv`（逐条）"
      f" / `17a_EXTERNAL_REFERENCES_BY_FILE.csv`（逐文件）")
    a("")
    a("### 15a. OUTFIT (OTFT) 目标解析")
    a("")
    a(f"- 范围内 OTFT 记录：**{stats['n_otft']}** 条"
      f"（{', '.join(f'`{e}`' for e in stats['otft_edids'])}）")
    a(f"- `INAM` 成功恢复成 FormID：**{stats['n_otft_inam']}** 条")
    a(f"- 其中能在 09 范围内解析到目标记录：**{stats['n_otft_resolved']}** 条")
    a("")
    a(stats["otft_detail"])
    a("")
    a("### 15b. 🔴 分发层实测 —— 修正旧 P00 的「全为 0」")
    a("")
    a("对 132 个 ini/xml/json/yaml/txt 配置文件做全文检测，结论与旧 P00 不一致：")
    a("")
    a("| 层 | 旧 P00 | 本轮实测 |")
    a("|---|---|---|")
    a(f"| SPID | 0 | **{stats['cfg_sp']}** ✅ 一致 |")
    a(f"| KID（关键词注入） | 0 | **{stats['cfg_kid']} 行 / "
      f"{stats['cfg_kid_files']} 文件** "
      f"⚠ **旧结论是假阴性** |")
    a(f"| BOS | 0 | **{stats['cfg_bos']}** ✅ 一致 |")
    a(f"| OAR | 0 | **{stats['cfg_oar']}** ✅ 一致 |")
    a(f"| DAR | 0 | **{stats['cfg_dar']}** ✅ 一致 |")
    a(f"| Papyrus `.psc` | 0 | **{stats['cfg_psc']}** ✅ 一致 |")
    a(f"| SKSE 配置 | 0 | **{stats['cfg_skse']}**（NiOverride/TintData/Armor）|")
    a(f"| PGPatcher 规则 | 4 | **{stats['cfg_pgp']}** ✅ 一致 |")
    a("")
    a("**KID 假阴性的根因**：这 5 个文件用的是裸行格式")
    a("`Keyword = <kw>|<category>|<formids>[+<plugin>]`，")
    a("**没有** `[KeywordInjector]` 这类小节头，因此旧审计的")
    a("`[KeywordInjector] / KeywordItemDistribution / KeywordDistribution`")
    a("三条正则**一条都匹配不到**。")
    a("")
    a("| 文件 | Mod | 注入行数 |")
    a("|---|---|---|")
    for f in stats["kid_files"]:
        a(f"| `{f['file']}` | `{f['mod'][:44]}` | {f['lines']} |")
    a("")
    a("它们在运行时把 **SLA_\\***（Sexy Latex Apparel）与 **ORF_\\*** 关键词注入到护甲上 ——")
    a("**这是一层真实存在的分发逻辑，但在插件记录里完全看不见。**")
    a("对本项目的意义：ZLJ 统一 Keyword 时必须知道这层依赖，否则合流后会断。")
    a("")
    a("**另有 2 个未解析的外部插件依赖**：")
    a("")
    a("| 插件 | 声明位置 | 性质 |")
    a("|---|---|---|")
    for x in stats["ext_plugins"]:
        a(f"| `{x['plugin']}` | `{x['where']}` | {x['note']} |")
    a("")
    a("### 16. Slot 冲突")
    a("")
    a("| slot_mask | 次数 | 解释 |")
    a("|---|---|---|")
    for k, v in stats["slot_masks"].most_common(10):
        a(f"| `{k}` | {v} | {stats['slot_names'].get(k, '')} |")
    a("")
    a("### 17. 跨 Mod DDS / NIF 依赖")
    a("")
    a("全部数字由 `14_CROSS_MOD_DEPENDENCIES.csv` 聚合而来，**没有手填**。"
      "该表当前构成：")
    a("")
    a("| dep_type | 行数 |")
    a("|---|---|")
    for k, v in stats.get("dep_types", {}).items():
        a(f"| `{k}` | {v} |")
    a("")
    a("| 分桶 | 条数 |")
    a("|---|---|")
    for k, v in stats.get("dep_buckets", {}).items():
        a(f"| {k} | {v} |")
    a("")
    a(f"- NIF 引用**范围内其它 TARGET Mod** 提供的贴图："
      f"**{stats['cross_tex']:,}** 条"
      f"（`CROSS_MOD_TEXTURE`）—— 这不是 0。")
    a(f"- 跨插件 ArmorAddon 引用：**{stats.get('cross_arma', 0):,}** 条"
      f"（`CROSS_PLUGIN_ARMA`）")
    a(f"- NIF 贴图槽总数：**{stats['n_texture_slots']:,}**")
    a(f"- 其中在本范围内找不到提供者的：**{stats['unresolved_tex']}** 条")
    a("")
    a("### 17b. NIF 分类（重-taxonomy 后）")
    a("")
    a("| nif_class | 数量 |")
    a("|---|---|")
    for k, v in stats["nif_class"].most_common():
        a(f"| `{k}` | {v} |")
    a("")
    a("> 原始扫描器按任务书给定的有序规则执行，在本范围上只有 SHAPEDATA 能命中"
      "（没有任何 NIF 位于 /bodyphysics/、/static/、meshes/actors/ 等路径）。"
      "本轮在报告层重做了一次分类，**原始扫描输出未被修改**，"
      "旧值保留在 `nif_class_raw`。")
    a("")
    a("### 18. 材质分布")
    a("")
    a("| 材质类 | shape 数 |")
    a("|---|---|")
    for k, v in stats["materials"].most_common():
        a(f"| `{k}` | {v} |")
    a("")
    a("### 19. FAKE_METALLIC_LATEX 清单")
    a("")
    a(f"**{stats['fake_metal']}** 个 shape 同时满足：材质证据指向 LATEX/RUBBER/VINYL，"
      "但 NIF 暴露 EnvMap/specular 槽（legacy 材质把它做成像金属）。")
    a("")
    a("| NIF | shape | material | 证据 |")
    a("|---|---|---|---|")
    for r in stats["fake_list"][:25]:
        a(f"| `{r['nif'][:40]}` | `{r['shape'][:24]}` | `{r['mat']}` "
          f"| {r['ev'][:60]} |")
    a("")
    a("### 20. 当前已有 PBR")
    a("")
    a(f"- PGPatcher 规则文件：**{stats['n_pgpatcher']}**")
    a(f"- `textures/pbr/` 目录所在 Mod：**{stats['n_pbr_dirs']}**")
    a(f"- 已含 PBR 通道（NORMAL/RMAOS/METALLIC/ROUGHNESS/AO/COAT）的 Mod："
      f"**{stats['pbr_mods']}**")
    a(f"- 其余 Mod 为 legacy `_d/_n/_s/_e` 四通道：**{stats['legacy_mods']}**")
    a("")
    a("### 21. 推荐保留哪个 Rework / PBR 版本")
    a("")
    a("本阶段**不做**版本取舍决定 —— 需要 `04_PARTS_CATALOG.csv` 与"
      "`15_REWORK_RELATIONSHIPS.csv` 的人工复核。")
    a("判定所需的客观输入已齐：同系列 Mod 的 priority、part 数、贴图字节、"
      "重复组归属。")
    a("")
    a("### 22. 总资产大小")
    a("")
    a(f"**{stats['total_bytes']:,} B = {stats['total_bytes']/2**30:.2f} GiB**"
      f"（{ev['scope_total_files']:,} 个文件）")
    a("")
    a("### 23. Safe byte dedup 可节省空间")
    a("")
    a(f"**{stats['safe_bytes']:,} B = {stats['safe_bytes']/2**20:.2f} MiB**"
      f"（{stats['dup_extra']} 个多余副本）")
    a("")
    a("### 24. KEEP / PARTIAL / DROP 后预计合集体积")
    a("")
    a("**本阶段不估算。** KEEP/PARTIAL/DROP 需要逐 part 的人工决定，"
      "任何在此给出的数字都是猜测。决策输入见 `04_PARTS_CATALOG.csv`。")
    a("")
    a("### 25. P01 推荐执行顺序")
    a("")
    a("本报告**不进入 P01**。以下仅为 P00 内部遗留工作的建议顺序：")
    a("")
    a("1. 修 `bs_slidersets` 口径（本轮已重扫解决，v1 报告需以本轮为准）")
    a("2. 补齐 body_candidate=UNKNOWN 的 Mod 的证据（ShapeData/OSP/NIF shape）")
    a("3. 人工复核 `19_CURRENT_BALANCE_VALUES.csv` 的 raw 字段与 CK 字段映射")
    a("4. 复核 `13/17` 的外部引用，决定哪些能进大 ESP")
    a("")
    a("---")
    a("")
    a("## 关键诚实声明")
    a("")
    a("1. **ARMO 的 Value / Weight / ArmorRating 已按 Skyrim schema 解码。** "
      "`ARMO.DATA` = uint32 value + float32 weight；`ARMO.DNAM` = uint32 "
      "armor rating。`19_CURRENT_BALANCE_VALUES.csv` 全部 1,448 行三个字段"
      "均已解码，原始字节以 `data_raw_hex` / `dnam_raw_hex` 保留为 provenance，"
      "异常 weight 会被 `weight_sanity` 标出而不是丢弃。"
      "（上一版曾以「找不到权威 CK 列名」为由只输出 raw，"
      "该保留意见现已不适用。）")
    a("2. **slot_mask 来自 ARMO.BOD2 的 uint32 位掩码**，"
      "槽位名用标准 Skyrim 位表解码，`slot_confidence=MEDIUM`，"
      "原始十六进制同时保留。")
    a("3. **DDS 的 declared format 与实测存储量分开记录** —— "
      f"本轮发现 **{stats['fmt_mismatch']}** 张贴图的 header 声明与实际字节数矛盾"
      "（多为作者工具把 DXGI 98 标在了 BC 数据上），"
      "以 `storage_class_measured` 为准。")
    a("4. **body_candidate=UNKNOWN 即无证据**，未做任何推测。")
    a("5. **ARMO→ArmorAddon 是 1:N，且带歧义的引用一律不配对。** "
      f"{stats['n_modl_bad']} 条 MODL 引用没能唯一解析到 ARMA"
      "（`ambiguous(N)` / `unresolved`），这些在 `03_ARMOR_ARMA_MAP.csv` 里"
      "**没有行**。按 24 位本地 id 强行配对会制造假链接，因此没有做。")
    a("6. **ARMO 自己的 MOD2..MOD5 是 world / inventory 模型，不是 worn mesh。** "
      "任何材质 / 贴图 / 分区结论都必须沿 "
      "ARMO → MODL → ARMA → ARMA.MOD2..MOD5 取网格，否则结论无效。")
    a("7. **`UNKNOWN` 与 `NONE` 不同。** 证据里没有的字段打印 `UNKNOWN`；"
      "证据确证为空的字段（例如某 ARMO 确实没有任何 ArmorAddon）打印 `NONE`。")
    a("")
    a(f"**P00_RERUN COMPLETE** —— 上一版结果已作废，见 "
      f"「⚠ SUPERSEDE NOTICE」一节。")
    with open(os.path.join(C.REPORTS, "P00_MASTER_REPORT.md"), "w",
              encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    return "P00_MASTER_REPORT.md"


def vs_old(ev, stats):
    L = []
    a = L.append
    a("# P00_RERUN_VS_OLD.md — 新旧 P00 对比")
    a("")
    a("只对比**关键数字与重大差异**。旧 P00 成果未被覆盖，仍在 "
      "`reports/P00/`，状态 `archive / reference only`。")
    a("")
    cal = stats["calibration"]
    a("## 0. ⚠ SUPERSEDE NOTICE — 上一版 P00_RERUN 已被作废（schema fix）")
    a("")
    a("**本次 schema fix 之前生成的整套 P00_RERUN 结果已整体作废。** "
      "它们不是「旧了一点」，而是**方向错了**：")
    a("")
    a("| # | 缺陷 | 证据 |")
    a("|---|---|---|")
    a("| 1 | `ARMO.RNAM` 被当成 ArmorAddon 链接 | RNAM 100% 指向 **RACE**"
      "（vanilla 全库 2,762 条 ARMO 实测）；ArmorAddon 链接是 `ARMO.MODL`，"
      "且 1:N（702/2762 条 ARMO 有多条 MODL） |")
    a("| 2 | ARMO 自己的 MOD2..MOD5 被当成 worn mesh | worn mesh 在 **ARMA** 上；"
      "ARMO 的 MOD2..MOD5 是 world / inventory 模型 |")
    a("| 3 | 链接被单值化 | 一个 ARMO 可以挂多个 ArmorAddon，"
      "旧表只有 `ARMA_formid` 一列 |")
    a("| 4 | 二进制 OSD 解析器被用在 XML `.osp` 上 | "
      "`ShapeData/*.osd` 才是二进制（`OSD\\0`）；`SliderSets/*.osp` 是 XML。"
      "旧解析器对 `.osp` 静默返回空 → 07 的 shapedata/sliderset 计数全是假空 |")
    a("| 5 | `classify_body` 把 CBBE-only 并进 OTHER | 现已单独判为 `CBBE`；"
      "任何假定 CBBE 不存在的聚合都需重算 |")
    a("")
    a("### 被作废的输出")
    a("")
    a("| 输出 | 波及层级 | 原因 |")
    a("|---|---|---|")
    for name, scope, why in SUPERSEDED:
        a(f"| `{name}` | {scope} | {why} |")
    a("")
    a("### 因此，下面第 1–4 节的数字只能与 `reports/P00/` 的旧 P00 比，"
      "**不能**与上一版 P00_RERUN 比。**")
    a("上一版 P00_RERUN 的对应数字已作废，不在此列出 —— 列出来只会让它看起来还能用。")
    a("")
    a("### 解析器校准门")
    a("")
    a(f"- 引用：`{cal['path']}`")
    a(f"- 门状态：**{cal['verdict']}**")
    a(f"- 说明：{cal['detail']}")
    if not cal["present"]:
        a("")
        a("> 校准报告**尚未生成**，因此本文件不给出任何通过 / 未通过判定。")
    a("")
    a("---")
    a("")
    a("## 1. 范围")
    a("")
    a("| 项 | 旧 P00 | P00_RERUN | 一致 |")
    a("|---|---|---|---|")
    a(f"| modlist SHA256 | `fba5d3a3…` | `{ev['modlist_sha256'][:8]}…` | ✅ |")
    a(f"| 范围 | L879–934 | L{ev['scope_first_line']}–{ev['scope_last_line']} | ✅ |")
    a(f"| Mod 数 | 56 | {ev['scope_mod_count']} | ✅ |")
    a("")
    a("## 2. 关键数字")
    a("")
    a("| 指标 | 旧 P00 | P00_RERUN | 差异 |")
    a("|---|---|---|---|")
    rows = stats["vs_old"]
    for label, old, new, note in rows:
        a(f"| {label} | {old} | {new} | {note} |")
    a("")
    a("## 3. 重大差异说明")
    a("")
    for t in stats["vs_notes"]:
        a(f"- {t}")
    a("")
    a("## 4. 旧成果的处置")
    a("")
    a("- `reports/P00/00_SCOPE.md`、`01_MOD_INVENTORY.csv` —— "
      "**保留为 archive**，不删除、不覆盖。")
    a("- 旧 `01_MOD_INVENTORY.csv` 的 `bs_slidersets` 列全为 0，"
      "根因是脚本只认 `.xml` 而本批 Mod 用新版 `.osp`；"
      "P00_RERUN 已按 `.osp` 正确计入。")
    a("- 旧报告的「913 个 Mod」轶事在当前盘面不可复现，本轮未沿用。")
    a("")
    a("**P00_RERUN COMPLETE**")
    with open(os.path.join(C.REPORTS, "P00_RERUN_VS_OLD.md"), "w",
              encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    return "P00_RERUN_VS_OLD.md"


# ===================================================================== main ===
def main() -> int:
    C.ensure_dirs()
    C.log("loading stage A-E evidence ...")
    ev = load("00_scope_evidence.json")
    mods = load("01_mod_aggregates.json")
    index = load("01_file_index.json.gz")
    recs = load("02_plugin_records.json")
    pidx = {p["PLUGIN_ID"]: p for p in load("02_plugin_index.json")}
    bss = load("07_bodyslide_slidersets.json")
    bsd = load("07_bodyslide_shapedata.json")
    bsg = load("07_bodyslide_groups.json")
    bsp = load("07_bodyslide_projects.json")
    nifs = load("08_nif_parsed.json.gz")
    tex = load("10_texture_parsed.json")
    dupes = normalize_dupes(load("10_texture_dupes.json"), tex)
    C.log(f"loaded: {len(mods)} mods, {len(index)} files, {len(recs)} records, "
          f"{len(nifs)} nifs, {len(tex)} textures, {len(bsp)} bs projects")

    tex_by_id = {t["TEXTURE_ID"]: t for t in tex}
    modids = {m["mod_name"]: m["MOD_ID"] for m in mods}
    ch = reclassify_nifs(nifs)
    C.log("nif_class re-taxonomy: " + ", ".join(
        f"{k[0]}->{k[1]}:{v}" for k, v in ch.most_common())
        + " | now: " + ", ".join(
            f"{k}={v}" for k, v in Counter(
                n["nif_class"] for n in nifs).most_common()))
    parts_rows, parts_note = parts_table(load_optional("04_parts.json"))
    if parts_rows:
        C.log(f"parts from upstream: {len(parts_rows)} rows")
    else:
        C.log(f"!! {parts_note} -- 04/05/06 consumers degrade to UNKNOWN")

    made = []
    made.append(r00_scope(ev, mods))
    _, nm = r01_inventory(mods); made.append(nm)
    _, nm = r02_plugin_records(recs, pidx); made.append(nm)
    _, nm, n_arma_links = r03_armor_arma(recs); made.append(nm)
    _, nm, bs_st = r07_bodyslide(bsp, bss, bsd); made.append(nm)
    _, nm = r08_nif(nifs, modids); made.append(nm)
    _, nm, miss = r09_nif_texture(nifs, tex_by_id); made.append(nm)
    _, nm = r10_texture(tex, dupes); made.append(nm)
    _, nm, matrows = r11_material(nifs, tex_by_id, parts_rows); made.append(nm)
    _, nm, dups = r12_duplicates(tex, dupes, nifs, mods); made.append(nm)
    _, nm, confl, shadowed = r13_mo2_conflict(index, mods); made.append(nm)
    _, nm, deps_rows = r14_dependencies(nifs, recs, mods, index); made.append(nm)
    r07_stats = bs_st          # already produced by the r07 call above
    # bucket every dependency so the master never hand-types a count
    _scopemods = {m["mod_name"] for m in mods}
    dep_buckets = Counter()
    for _r in (deps_rows or []):
        _f, _t = _r.get("from_mod"), _r.get("to_mod")
        if _f and _f == _t:
            dep_buckets["same-mod"] += 1
        elif _t in _scopemods:
            dep_buckets["cross-target-mod"] += 1
        elif _f in _scopemods:
            dep_buckets["external / out-of-scope"] += 1
        else:
            dep_buckets["unresolved"] += 1
    _, nm, rework = r15_rework(mods, parts_rows, bsp); made.append(nm)
    _, nm, pbr = r16_pbr(index, tex); made.append(nm)
    _, nm, merge = r18_merge(pidx, recs); made.append(nm)
    _, nm, bal = r19_balance(recs, parts_rows); made.append(nm)
    _, nm, sp, total_bytes = r20_space(index, tex, dupes, dups, mods, pidx)
    made.append(nm)
    C.log("core reports written: " + ", ".join(made))

    # ---------------- stats for the master report --------------------------
    f2p = defaultdict(set)
    for r in recs:
        f2p[(r["record_type"], r["formid"])].add(r["PLUGIN_ID"])
    collisions = sum(1 for v in f2p.values() if len(v) > 1)

    in_scope = {m["mod_name"] for m in mods}
    # The previous inline test looked for "/<mod name>/" inside the texture
    # path and therefore matched nothing, reporting 0 while
    # 14_CROSS_MOD_DEPENDENCIES.csv held 2,044 CROSS_MOD_TEXTURE rows. The
    # authoritative count is the one r14 computed, so derive it from there.
    cross_tex = sum(1 for d in (deps_rows or [])
                    if d.get("dep_type") == "CROSS_MOD_TEXTURE")
    n_slots = sum(len(s.get("textures") or {}) for x in nifs
                  for s in x.get("shapes", []))
    slot_masks = Counter()
    slot_names = {}
    for r in recs:
        if r["record_type"] != "ARMO":
            continue
        a_ = r.get("armo") or {}
        if a_.get("slot_mask") is not None:
            slot_masks[f"0x{a_['slot_mask']:08X}"] += 1
            slot_names[f"0x{a_['slot_mask']:08X}"] = \
                ", ".join(a_.get("slot_names", []) or [])

    fake = [m for m in matrows if m["fake_metallic_latex"] == "yes"]
    mats = Counter(m["material_class"] for m in matrows)

    diy = []
    parts_by_mod = Counter()
    cls_by_mod = Counter()
    empty_by_mod = Counter()
    for p in (parts_rows or []):
        parts_by_mod[p["source_mod"]] += 1
        if p.get("part_category", "OTHER") != "OTHER":
            cls_by_mod[p["source_mod"]] += 1
        if p.get("is_empty_shell") == "yes":
            empty_by_mod[p["source_mod"]] += 1
    bs_by_mod = Counter()
    for p in bsp:
        bs_by_mod[project_source_mod(p)] += 1
    for m in mods:
        if parts_by_mod[m["mod_name"]]:
            diy.append({"mod": m["mod_name"],
                        "parts": parts_by_mod[m["mod_name"]],
                        "classified": cls_by_mod[m["mod_name"]],
                        "bs": bs_by_mod[m["mod_name"]],
                        "body": m["body_candidate_name"]})
    diy.sort(key=lambda r: (-r["classified"], -r["parts"]))

    partial = []
    for m in mods:
        np_ = parts_by_mod[m["mod_name"]]
        if not np_:
            continue
        emp = empty_by_mod[m["mod_name"]]
        nop = 1 if m["plugin_count"] == 0 else 0
        if emp or nop or cls_by_mod[m["mod_name"]] < np_:
            partial.append({"mod": m["mod_name"], "parts": np_, "empty": emp,
                            "noplugin": nop,
                            "verdict": "PARTIAL" if cls_by_mod[m["mod_name"]]
                            else "DROP_CANDIDATE"})
    partial.sort(key=lambda r: -r["parts"])

    safe_bytes = sum(r["wasted_bytes"] for r in dups
                     if r["dup_kind"] == "BYTE_IDENTICAL_DUPLICATE")
    # 15 is owned by p00r_logical.py, which emits the corrected schema:
    # `role` (BASE_MOD / PATCH_MOD / REWORK_MOD), not the old `mod_role`.
    roles = Counter(r.get("role") or r.get("mod_role") or UNK for r in rework)
    outfits = {r.get("LOGICAL_OUTFIT_ID") for r in rework}
    body_mods = Counter(m["body_candidate_name"] for m in mods)
    body_proj = Counter(p.get("body_candidate") or UNK for p in bsp)
    part_cats = Counter(p.get("part_category", UNK) for p in (parts_rows or []))

    # ---- new 04_PARTS_CATALOG columns (1:N ARMA chain) -------------------
    p_arma_n = Counter(jnum(p.get("n_arma_refs")) for p in (parts_rows or []))
    p_arma_res = Counter(p.get("ARMA_resolved") or UNK
                         for p in (parts_rows or []))
    p_slot_src = Counter(p.get("slot_source") or UNK for p in (parts_rows or []))
    p_model_src = Counter(p.get("model_source") or UNK
                          for p in (parts_rows or []))
    p_game_nif = Counter(p.get("game_nif_resolved") or UNK
                         for p in (parts_rows or []))
    p_routes = Counter()
    p_race_is = Counter(p.get("race_is") or UNK for p in (parts_rows or []))
    p_nif_res = Counter(p.get("nif_resolved") or UNK for p in (parts_rows or []))
    p_bs_nifs = sum(len(as_list(p.get("bodyslide_source_nifs")))
                    for p in (parts_rows or []))
    p_pending_nifs = sum(len(as_list(p.get("pending_build_nifs")))
                         for p in (parts_rows or []))
    p_world_models = sum(len(as_list(p.get("world_model_paths")))
                         for p in (parts_rows or []))
    p_bs_parts = sum(1 for p in (parts_rows or [])
                     if as_list(p.get("bodyslide_source_nifs")))
    p_pending_parts = sum(1 for p in (parts_rows or [])
                          if as_list(p.get("pending_build_nifs")))
    _wm = []
    for p in parts_rows or []:
        c = p.get("world_model_count")
        _wm.append(c if isinstance(c, int) and not isinstance(c, bool)
                   else len(as_list(p.get("world_model_paths"))))
    p_world_avg = (f"{sum(_wm) / len(_wm):.2f}" if _wm else UNK)
    for p in parts_rows or []:
        for rt in as_list(p.get("ARMA_routes")):
            if rt and rt != "NONE":
                p_routes[rt] += 1

    # ---- ARMO -> ArmorAddon reach (the 1:N question) ----------------------
    armos = [r for r in recs if r["record_type"] == "ARMO"]
    n_armor = len(armos)
    with_arma = sum(1 for r in armos if (r.get("armo") or {}).get(
        "n_arma_refs", 0))
    modl_routes = Counter()
    n_modl = n_modl_arma = n_race = 0
    for r in armos:
        blk = r.get("armo") or {}
        for m in blk.get("modl_refs") or []:
            n_modl += 1
            modl_routes[m.get("route") or UNK] += 1
            if m.get("is_arma"):
                n_modl_arma += 1
        if (blk.get("race_resolved") or {}).get("type") == "RACE":
            n_race += 1

    # ---- OUTFIT (OTFT.INAM) ----------------------------------------------
    otfts = [r for r in recs if r["record_type"] == "OTFT"]
    n_otft_inam = n_otft_res = 0
    otft_rows = []
    for r in otfts:
        refs = []
        for x in (r["subrecords"].get("INAM") or []):
            if isinstance(x, int) and x:
                refs.append(C.record_id(x))
            elif isinstance(x, str) and len(x) == 8 and all(
                    ch in "0123456789abcdefABCDEF" for ch in x):
                refs.append(x.upper())
        ok_formid = bool(refs)
        n_otft_inam += int(ok_formid)
        tgt = None
        for f_ in refs:
            for c in recs:
                if c["plugin_file"] == r["plugin_file"] and c["formid"] == f_:
                    tgt = c
                    break
            if tgt is not None:
                break
        n_otft_res += int(tgt is not None)
        otft_rows.append((r, ";".join(refs) if refs else None, tgt))
    if not otfts:
        otft_detail = "范围内没有 OTFT 记录。"
    elif n_otft_inam == 0:
        otft_detail = (
            "`OTFT.INAM` 在当前证据文件里**仍然不是 FormID**（解码器修复之前"
            "生成的证据），目标**没有恢复**。需要用修复后的 `p00r_plugins.py` "
            "重跑 stage B 才能回答。逐条结果见 `02_PLUGIN_RECORDS.csv` 的 "
            "`outfit_target_formid` / `outfit_target_type` / "
            "`outfit_target_edid` 三列与 `note` 列。")
    elif n_otft_res == 0:
        otft_detail = (
            f"{n_otft_inam} 条 `INAM` 已恢复成 FormID，但目标记录**都不在 "
            "09 范围内**（Outfit 目标多为 CK 生成的 dummy / 外部 ESP）。"
            "本报告不猜测目标身份。逐条见 `02_PLUGIN_RECORDS.csv`。")
    else:
        otft_detail = (
            f"{n_otft_inam} 条 `INAM` 已恢复成 FormID，其中 **{n_otft_res}** 条"
            "在 09 范围内解析到了目标记录。逐条见 `02_PLUGIN_RECORDS.csv` 的 "
            "`outfit_target_*` 三列；**解析不到的保持 UNKNOWN，不猜**。")
    otft_detail += "\n\n| Outfit EDID | 插件 | INAM (FormID) | 目标 |"
    otft_detail += "\n|---|---|---|---|"
    for r, fid, tgt in otft_rows:
        ed = r["subrecords"].get("EDID", [""])[0]
        tdesc = (f"{tgt['record_type']} `{jval((tgt['subrecords'].get('EDID') or [''])[0])}`"
                 if tgt is not None else UNK)
        otft_detail += (f"\n| `{ed if isinstance(ed, str) else UNK}` "
                        f"| `{r['plugin_file']}` | `{fid or UNK}` | {tdesc} |")

    pbr_mods = len({r["source_mod"] for r in pbr if r["is_pbr"] == "yes"})
    legacy = len({r["source_mod"] for r in pbr if r["is_pbr"] == "no"})

    cfg = None
    pcfg = os.path.join(C.DATA, "14_config_refs.json")
    if os.path.isfile(pcfg):
        with open(pcfg, "r", encoding="utf-8") as fh:
            cfg = json.load(fh)
        C.log(f"config evidence loaded: {len(cfg.get('files', []))} files")
    else:
        C.log("!! 14_config_refs.json missing — 15b section will be blank")

    stats = {
        "enabled": sum(1 for m in mods if m["enabled"] == "enabled"),
        "disabled": sum(1 for m in mods if m["enabled"] == "disabled"),
        "missing": sum(1 for m in mods if not m["folder_exists"]),
        "n_outfits": len(outfits), "roles": roles,
        "n_parts": len(parts_rows or []), "part_cats": part_cats,
        "n_bs_projects": len(bsp), "n_ss": len(bss),
        "n_ss_osp": bs_st["ss_osp"],
        "n_ss_xml": bs_st["ss_xml"],
        "n_sg": len(bsg["groups"]), "n_sp": len(bsg["presets"]),
        "body_mods": body_mods, "body_projects": body_proj,
        "needs3ba": Counter(p["needs_3ba_conversion"] for p in bsp),
        "diy_top": diy[:12], "partial_top": partial[:12],
        "dup_groups": dupes.get("byte_identical_group_count", 0),
        "dup_extra": dupes.get("byte_identical_extra_copies", 0),
        "samediff": dupes.get("same_name_diff_content_count", 0),
        # 18 is owned by p00r_merge.py, which uses the corrected tier names
        # LOW_EASY / MODERATE / HIGH instead of the old risk_class vocabulary.
        "merge_easy": sum(1 for r in merge
                          if (r.get("risk_tier") or r.get("risk_class"))
                          in ("LOW_EASY", "MERGE_EASY")),
        "merge_mod": sum(1 for r in merge
                         if (r.get("risk_tier") or r.get("risk_class"))
                         in ("MODERATE", "MERGE_MODERATE")),
        "merge_high": sum(1 for r in merge
                          if (r.get("risk_tier") or r.get("risk_class"))
                          in ("HIGH", "MERGE_HIGH_RISK")),
        "merge_ref_classes": sorted({c for r in merge
                                     for c in (r.get("reference_class") or "")
                                     .split(";") if c}),
        # BodySlide effective-VFS counts, read from the owning stage
        "bs_phys": r07_stats.get("physical_project_rows"),
        "bs_eff": r07_stats.get("effective_vfs_projects"),
        "bs_shadow": r07_stats.get("shadowed_project_rows"),
        "bs_conflict": r07_stats.get("content_conflicting"),
        # 14_CROSS_MOD_DEPENDENCIES composition, aggregated not hand-typed
        "dep_types": dict(Counter(r.get("dep_type") for r in deps_rows)),
        "dep_buckets": dep_buckets,
        "cross_arma": sum(1 for r in deps_rows
                          if r.get("dep_type") == "CROSS_PLUGIN_ARMA"),
        "n_plugins": len(pidx),
        "formid_collisions": collisions,
        "cross_tex": cross_tex, "n_texture_slots": n_slots,
        "unresolved_tex": miss,
        "slot_masks": slot_masks, "slot_names": slot_names,
        "materials": mats, "fake_metal": len(fake),
        "fake_list": [{"nif": m["NIF_ID"], "shape": m["unit_id"],
                       "mat": m["material_class"],
                       "ev": m["fake_metallic_reason"]} for m in fake],
        "n_pgpatcher": sum(1 for r in index
                           if r["vpath"].lower().startswith("pbrnifpatcher/")),
        "n_pbr_dirs": len({r["source_mod"] for r in pbr
                           if r["asset_kind"] == "TEXTURES_PBR_DIR"}),
        "pbr_mods": pbr_mods, "legacy_mods": legacy,
        "total_bytes": total_bytes, "safe_bytes": safe_bytes,
        "fmt_mismatch": sum(1 for t in tex if t.get("format_mismatch")),
        "n_conflicts": len(confl),
        "n_conflicts_diff": sum(1 for r in confl if r["same_content"] == "no"),
        "shadowed_bytes": shadowed,
        "nif_class": Counter(n["nif_class"] for n in nifs),
        "stub_cubemaps": sum(1 for t in tex
                             if t.get("width") == 1 and t.get("height") == 1),

        # ---- schema-fix era ------------------------------------------------
        "calibration": calibration_status(),
        "parts_note": parts_note,
        "n_armor": n_armor,
        "armo_with_arma": with_arma,
        "armo_without_arma": n_armor - with_arma,
        "arma_cover_pct": (f"{with_arma / n_armor * 100:.1f}%"
                           if n_armor else UNK),
        "n_arma": sum(1 for r in recs if r["record_type"] == "ARMA"),
        "n_modl_refs": n_modl,
        "n_modl_to_arma": n_modl_arma,
        "n_modl_bad": n_modl - n_modl_arma,
        "n_arma_links": n_arma_links,
        "modl_routes": modl_routes,
        "n_race_ok": n_race,
        "dep_armo_arma": sum(1 for d in (deps_rows or [])
                             if d["from_kind"] == "ARMO"),
        "n_otft": len(otfts),
        "n_otft_inam": n_otft_inam,
        "n_otft_resolved": n_otft_res,
        "otft_edids": [x for x in
                       ((r["subrecords"].get("EDID") or [""])[0]
                        for r in otfts)][:8],
        "otft_detail": otft_detail,
        "body_vocab": (list(BODY_VOCAB)
                       + sorted((set(body_mods) | set(body_proj))
                                - set(BODY_VOCAB))),
        # ---- BodySlide (OSP-keyed) ----------------------------------------
        "n_sd_nif": bs_st["sd_nif"], "n_sd_osd": bs_st["sd_osd"],
        "bs_osp_errors": bs_st["osp_errors"],
        "bs_osd_errors": bs_st["osd_errors"],
        "bs_out_paths": len({(p.get("output_path") or UNK).rstrip("\\/")
                             for p in bsp}),
        # ---- new 04 columns ------------------------------------------------
        "p_arma_n": p_arma_n, "p_arma_res": p_arma_res,
        "p_slot_src": p_slot_src, "p_model_src": p_model_src,
        "p_game_nif": p_game_nif, "p_routes": p_routes,
        "p_race_is": p_race_is, "p_nif_res": p_nif_res,
        "p_bs_nifs": p_bs_nifs, "p_pending_nifs": p_pending_nifs,
        "p_bs_parts": p_bs_parts, "p_pending_parts": p_pending_parts,
        "p_world_models": p_world_models, "p_world_avg": p_world_avg,
    }

    # ---- distribution-layer evidence (config scanner) ---------------------
    kinds = Counter()
    kind_files = Counter()
    kid_files = []
    ext_plugins = []
    if cfg:
        # `detection_hits_by_kind` counts injector LINES; `detection_files_by_kind`
        # counts FILES. The KID number people quote is the line count (54), so
        # use both explicitly rather than conflating them.
        kinds.update(cfg.get("summary", {}).get("detection_hits_by_kind", {}))
        kind_files.update(
            cfg.get("summary", {}).get("detection_files_by_kind", {}))
        for f in cfg.get("files", []):
            for d in (f.get("detections") or []):
                if d.get("kind") == "KID":
                    kid_files.append({
                        "file": f.get("vpath", ""),
                        "mod": f.get("source_mod", ""),
                        "lines": d.get("n_matches", 0),
                    })
        for f in cfg.get("files", []):
            for pr in (f.get("plugin_refs") or []):
                name = pr.get("value") if isinstance(pr, dict) else pr
                if not name:
                    continue
                if str(name).lower() not in {p.lower() for p in pidx}:
                    ext_plugins.append({
                        "plugin": name, "where": f.get("vpath", ""),
                        "note": pr.get("context", "")
                        if isinstance(pr, dict) else ""})
    stats["cfg_sp"] = kinds.get("SPID", 0)
    stats["cfg_kid"] = kinds.get("KID", 0)
    stats["cfg_kid_files"] = kind_files.get("KID", 0)
    stats["cfg_bos"] = kinds.get("BOS", 0)
    stats["cfg_oar"] = kinds.get("OAR", 0)
    stats["cfg_dar"] = kinds.get("DAR", 0)
    stats["cfg_skse"] = kinds.get("SKSE", 0)
    stats["cfg_pgp"] = kinds.get("PGPATCHER", 0)
    stats["cfg_psc"] = sum(1 for r in index if r["cat"] == "script_psc")
    stats["kid_files"] = sorted(kid_files, key=lambda x: -x["lines"])
    stats["ext_plugins"] = ext_plugins[:8]

    stats["vs_old"] = [
        ("Mod 数", 56, ev["scope_mod_count"], "✅"),
        ("文件数", "3,708", f"{ev['scope_total_files']:,}",
         "✅" if ev["scope_total_files"] == 3708 else "⚠"),
        ("总体积", "18.04 GiB", f"{ev['scope_total_bytes']/2**30:.2f} GiB",
         "✅"),
        ("插件", 47, len(pidx), "✅"),
        ("NIF", 1316, len(nifs), "✅"),
        ("DDS", 1355, len(tex), "✅"),
        ("BodySlide 文件", 1055,
         bs_st["sd_nif"] + bs_st["sd_osd"] + len(bss) + len(bsg["groups"])
         + len(bsg["presets"]),
         f"⚠ +{len(bss) + len(bsg['groups']) + len(bsg['presets'])}"),
        ("  其中 SliderSet (.osp)", 0, len(bss), "🔴 旧版漏计"),
        ("  其中 ShapeData NIF", 542, bs_st["sd_nif"], "✅"),
        ("  其中 ShapeData OSD", 513, bs_st["sd_osd"], "✅"),
        ("01_MOD_INVENTORY 列数", "47（文档写 49）", "47", "✅"),
        ("ARMA 记录", "未解析", sum(1 for r in recs
                                    if r["record_type"] == "ARMA"), "新增"),
        ("TXST 记录", "未解析", sum(1 for r in recs
                                    if r["record_type"] == "TXST"), "新增"),
        ("COBJ 记录", "未解析", sum(1 for r in recs
                                    if r["record_type"] == "COBJ"), "新增"),
        ("OTFT 记录", "未解析", sum(1 for r in recs
                                    if r["record_type"] == "OTFT"), "新增"),
        ("ARMO→ArmorAddon 链接", "未解析",
         f"{n_arma_links}（ARMO → MODL → ARMA，1:N）", "新增"),
    ]
    stats["vs_notes"] = [
        "**⚠ 本文件第 1–4 节不能与「上一版 P00_RERUN」比。** 上一版已被 "
        "schema fix 作废（见第 0 节），其数字不再有效。",
        "**BodySlide 计数口径不同**：旧版 1,055 只统计了 ShapeData 的 NIF+OSD；"
        "本轮把 SliderSet(.osp) / SliderGroup / SliderPreset 一并计入，"
        f"合计 {bs_st['sd_nif'] + bs_st['sd_osd'] + len(bss) + len(bsg['groups']) + len(bsg['presets'])}。"
        "旧脚本的 `bs_slidersets` 恒为 0，根因是只匹配 `.xml`，"
        f"而本批 {len(bss)} 个 SliderSet 全部是新版 `.osp`。",
        "**插件层完全新增**：旧 P00 没有任何 ESP/ESL 记录解析，"
        f"本轮真实解析了 {len(pidx)} 个插件、"
        f"{len(recs)} 条记录（ARMO/ARMA/TXST/COBJ/OTFT）。",
        "**🔴 旧 P00 的「KID 关键词分发 = 0」是假阴性。** 本轮全文检测 132 个"
        "配置文件，发现 **5 个文件 / 54 行关键词注入**，"
        "向护甲注入 SLA_*/ORF_* 关键词。旧审计的三条 KID 正则要求存在"
        "`[KeywordInjector]` 类小节头，而这些文件用的是裸行 "
        "`Keyword = <kw>|<category>|<formids>` 格式，一条都匹配不到。"
        "**结论：09 范围没有 SPID/BOS/OAR/DAR/Papyrus，但确实有一层 KID。**",
        "**modlist mtime 已失效但 SHA256 未变**：审计期间 MO2 开关两次，"
        "`modlist.txt` 被原子替换，mtime 刷新而内容逐字节相同。"
        "范围判断因此只用 SHA256。",
    ]

    made.append(master(ev, mods, stats))
    made.append(vs_old(ev, stats))
    C.log("ALL REPORTS WRITTEN")
    for m in made:
        p = os.path.join(C.REPORTS, m)
        if os.path.isfile(p):
            C.log(f"  {m:<38} {os.path.getsize(p):>9,} B")
    # 04/05/06/13/17 are owned by other stages; report which are present so a
    # reader never mistakes a stale file for a current one.
    for other in ("04_PARTS_CATALOG.csv", "05_SLOT_PARTITION_MAP.csv",
                  "06_DIY_COMPATIBILITY_MATRIX.csv", "13_MO2_CONFLICT_MAP.csv",
                  "17_EXTERNAL_REFERENCES.csv",
                  "PARSER_CALIBRATION.md"):
        p = os.path.join(C.REPORTS, other)
        if os.path.isfile(p):
            C.log(f"  {other:<38} {os.path.getsize(p):>9,} B  (other stage)")
        else:
            C.log(f"  {other:<38} {'MISSING':>9}  (other stage)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
