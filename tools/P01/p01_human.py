#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p01_human.py — P01_HUMAN_REVIEW.md and P01_CURATION_SUMMARY.md.

Deliberately NOT a long technical report. One short block per outfit, written
for a person deciding what to keep. Technical facts only; no taste, no
recommendation, and the checkboxes are never pre-ticked.

READ-ONLY with respect to every mod, plugin, mesh, texture and BodySlide file.
Writes only into reports/P01/.
"""
from __future__ import annotations

import csv
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PKT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(PKT, "tools", "P00_RERUN"))
import p00r_common as C  # noqa: E402

OUTDIR = os.path.join(PKT, "reports", "P01")
FROZEN = os.path.join(PKT, "reports", "P00_RERUN")
C.allow_extra_write_root(OUTDIR)


def rd(path, name):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def mib(v):
    try:
        n = int(str(v).replace(",", ""))
    except (TypeError, ValueError):
        return "?"
    if n >= 2 ** 30:
        return f"{n / 2**30:.2f} GiB"
    if n >= 2 ** 20:
        return f"{n / 2**20:.1f} MiB"
    if n >= 1024:
        return f"{n / 1024:.0f} KiB"
    return f"{n} B"


def main():
    outfits = rd(os.path.join(OUTDIR, "P01_OUTFIT_REVIEW.csv"),
                 "outfit")
    vps = rd(os.path.join(OUTDIR, "P01_VISUAL_PARTS.csv"), "vp")
    partial = rd(os.path.join(OUTDIR, "P01_PARTIAL_CANDIDATES.csv"), "pc")
    previews = []
    pv = os.path.join(OUTDIR, "P01_PREVIEW_INDEX.csv")
    if os.path.isfile(pv):
        previews = rd(pv, "pv")

    by_outfit = defaultdict(list)
    for v in vps:
        by_outfit[v["source_outfit"]].append(v)

    # Outfit-level technical cost: the worst cost among its visual parts. The
    # outfit board has no cost column of its own, and the review sheet and the
    # summary both need one -- an outfit that ships one HIGH-cost part is not a
    # cheap outfit.
    RANK = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
    outfit_cost = {}
    for oid, lst in by_outfit.items():
        # worst = highest rank (HIGH), ties broken by the first seen
        worst = max((v["technical_cost"] for v in lst),
                    key=lambda c: RANK.get(c, 1))
        outfit_cost[oid] = worst if lst else "UNKNOWN"
    for of in outfits:
        if of.get("OUTFIT_ID") in by_outfit:
            of["technical_cost"] = outfit_cost.get(of.get("OUTFIT_ID"), "UNKNOWN")
        else:
            # No ARMO in scope: P00's logical-outfit pass already classified
            # these as shipping only textures / meshes / physics / config. That
            # is a real state, not a gap, so say so rather than printing "?".
            of["technical_cost"] = "N/A（无 ARMO 记录）"

    partial_by = defaultdict(list)
    for p in partial:
        partial_by[p["source_outfit"]].append(p)
    prev_by = {p["MOD_ID"]: p for p in previews}

    # ------------------------------------------------------------ review --
    o = []
    a = o.append
    a("# P01 人工筛选表 / Human Curation Board")
    a("")
    a("P00 已冻结。以下是把 P00 数据整理成的**人工决策包**。")
    a("")
    a("**这里没有替你做决定。** 所有 `[ ]` 都没有勾选，"
      "`USER_DECISION` / `USER_PRIORITY` / `USER_NOTE` 全部留空。"
      "P01 不删除任何文件、不合并任何插件、不改任何资产。")
    a("")
    a("## 怎么看这张表")
    a("")
    a("| 字段 | 含义 |")
    a("|---|---|")
    a("| **大小** | 该 outfit 占用的大小（current = 磁盘，effective = MO2 实际保留）|")
    a("| **主要零件** | 折叠后的视觉零件（颜色变体 / 重复记录已合并），"
      "不是一条条 ARMO |")
    a("| **材质** | 从 11_MATERIAL_CLASSIFICATION 得到的材质候选 |")
    a("| **物理** | NONE / SMP / CBPC / MIXED / UNKNOWN |")
    a("| **技术成本** | LOW / MEDIUM / HIGH —— 依赖复杂度、body conversion、"
      "SMP、未解析引用、BodySlide 状态、跨 Mod 依赖综合而来，**不含审美** |")
    a("| **独特零件** | 只此一套有的零件（可单独留下）|")
    a("| **重复情况** | 与其它 outfit 重复的资产 |")
    a("| **依赖情况** | 跨 Mod 依赖与未解析引用 |")
    a("")
    a("`KEEP` / `PARTIAL` / `DROP` 与 `S/A/B/C` 的含义：")
    a("S = 核心主角衣装，A = 强烈保留，B = 有价值，C = 可有可无。")
    a("这是你自己的衣柜优先级，工具不会替你填。")
    a("")
    a("---")
    a("")

    for i, of in enumerate(outfits, 1):
        oid = of.get("OUTFIT_ID", "")
        mods = [x for x in (of.get("source_mods") or "").split(";") if x]
        vlist = sorted(by_outfit.get(oid, []),
                       key=lambda v: (-int(v["n_ARMO_records"] or 0),
                                      v["display_name"]))
        top = vlist[:8]
        extra = len(vlist) - len(top)
        uniq = [v for v in vlist if int(v["n_ARMO_records"] or 0) == 1
                and not v["bodyslide_projects"]]
        body = [v for v in vlist if v["part_category"] in
                ("BODY", "BODYSUIT", "CORSET", "PANTY", "BRA")]
        acc = [v for v in vlist if v["part_category"] in
               ("GLOVES", "BOOTS", "HEELS", "SHOES", "MASK", "HOOD", "HAT",
                "COLLAR", "CHOKER", "BELT", "HARNESS", "ACCESSORY", "TAIL",
                "VEIL", "SLEEVES", "STOCKINGS")]
        pv = None
        for m in mods:
            if m in prev_by and int(prev_by[m].get("preview_count") or 0) > 0:
                pv = prev_by[m]
                break

        a(f"## {i}. {of.get('display_name') or oid}")
        a("")
        a(f"- **Mod**：{', '.join(m[:60] for m in mods) or '?'}")
        if of.get("plugins"):
            a(f"- **插件**：{of['plugins'][:110]}")
        a(f"- **体型**：{of.get('body_type', 'UNKNOWN')}"
          f"　**物理**：{of.get('physics', 'UNKNOWN')}")
        a(f"- **大小**：{mib(of.get('current_size_bytes'))}"
          f"（MO2 实际保留 {mib(of.get('effective_asset_size_bytes'))}）")
        a(f"- **规模**：ARMO {of.get('n_ARMO', '?')}　"
          f"ARMA {of.get('n_ARMA', '?')}　"
          f"可穿戴 mesh {of.get('n_wearable_NIF', '?')}　"
          f"贴图 {of.get('n_texture', '?')}　"
          f"有效 BodySlide 项目 {of.get('n_effective_bodyslide_projects', '?')}")
        a(f"- **材质**：{of.get('material_candidates', 'UNKNOWN')}")
        a(f"- **PBR**：{of.get('pbr_state', 'UNKNOWN')}")
        a(f"- **技术成本**：**{of.get('technical_cost', '?')}**")
        a(f"- **重复资产**：{mib(of.get('duplicate_asset_bytes'))}"
          f"　**合并风险**：{of.get('merge_risk', '?')}")
        a(f"- **依赖**：跨 Mod {of.get('cross_mod_dependency_count', '?')}　"
          f"未解析 {of.get('unresolved_dependency_count', '?')}")
        a("")
        if top:
            a("主要零件：")
            for v in top:
                flags = []
                if int(v["n_ARMO_records"] or 0) > 1:
                    flags.append(f"×{v['n_ARMO_records']} 变体")
                if v["bodyslide_projects"]:
                    flags.append("BodySlide")
                if not v["n_wearable_meshes"] and v["pending_build_meshes"]:
                    flags.append("待 Build")
                if v["UBE_CONVERSION_CLASS"] == "E":
                    flags.append("UBE 分类未知")
                a(f"- {v['display_name'][:46]}　"
                  f"`{v['part_category']}`　{('，'.join(flags)) or '—'}")
            if extra > 0:
                a(f"- …另有 {extra} 个视觉零件")
        else:
            a("**该 outfit 在范围内没有任何 ARMO 记录。**"
              "P00 已判定这类 Mod 只提供贴图 / mesh / physics / config，"
              "不是独立衣装本体。是否保留取决于它是否为其它套装提供素材。")
            a("")
        if not vlist:
            body, acc, uniq = [], [], []
        if body and acc:
            names = "、".join(x["display_name"][:22] for x in acc[:5])
            a(f"**可能的部分保留**：主体（{body[0]['display_name'][:30]}）"
              f" + 独立配件 {len(acc)} 件 —— {names}")
            a("")
        if uniq:
            a(f"**独特零件**（仅此一套）："
              + "、".join(x["display_name"][:24] for x in uniq[:4]))
            a("")
        if pv:
            a(f"**预览图**：{pv.get('best_candidate_path', '')[:100]}")
            a("")
        a(f"> 备注位（自行填写，例如「只要靴子」「主体必留」「XP核心」）：")
        a("")
        a("- [ ] KEEP　　[ ] PARTIAL　　[ ] DROP")
        a("- Priority:　[ ] S　[ ] A　[ ] B　[ ] C")
        a("")
        a("Notes: ______________________________________________")
        a("")
        a("---")
        a("")

    path = os.path.join(OUTDIR, "P01_HUMAN_REVIEW.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(o))
    C.log(f"P01_HUMAN_REVIEW.md = {os.path.getsize(path):,} B  "
          f"({len(outfits)} outfit blocks)")

    # ----------------------------------------------------------- summary --
    s = []
    b = s.append
    b("# P01_CURATION_SUMMARY.md")
    b("")
    b("统计汇总。**本文件不做任何 KEEP / DROP 决策。**")
    b("")
    b("| 项 | 值 |")
    b("|---|---|")
    b(f"| Logical outfits | **{len(outfits)}** |")
    b(f"| Visual parts | **{len(vps)}**"
      f"（由 {sum(int(v['n_ARMO_records'] or 0) for v in vps)} 条 ARMO 折叠）|")
    b(f"| PARTIAL 候选行 | {len(partial)}"
      f"（涉及 {len(partial_by)} 套 outfit）|")
    b("")
    b("## 体型分布")
    b("")
    b("| body_type | outfits |")
    b("|---|---|")
    for k, v in Counter(o.get("body_type", "?") for o in outfits).most_common():
        b(f"| {k} | {v} |")
    b("")
    b("## 技术成本分布")
    b("")
    b("| technical_cost | outfits | visual parts |")
    b("|---|---|---|")
    tc_of = Counter(o.get("technical_cost", "?") for o in outfits)
    tc_vp = Counter(v["technical_cost"] for v in vps)
    for k in sorted(set(tc_of) | set(tc_vp)):
        b(f"| {k} | {tc_of.get(k, 0)} | {tc_vp.get(k, 0)} |")
    b("")
    b("## UBE 转换分类（仅分类，未执行任何转换）")
    b("")
    b("| class | visual parts | 含义 |")
    b("|---|---|---|")
    UBE = {
        "A": "紧身贴体 3BA mesh，预计非常适合自动转换",
        "B": "普通非贴身 mesh",
        "C": "多层 / 复杂配件",
        "D": "SMP / 裙 / 外套 / 物理链",
        "E": "未知 / 高风险",
    }
    for k, v in Counter(v["UBE_CONVERSION_CLASS"] for v in vps).most_common():
        b(f"| **{k}** | {v} | {UBE.get(k, '')} |")
    b("")
    b("## 物理分布")
    b("")
    b("| physics | outfits |")
    b("|---|---|")
    for k, v in Counter(o.get("physics", "?") for o in outfits).most_common():
        b(f"| {k} | {v} |")
    b("")
    b("## 视觉零件分类")
    b("")
    b("| part_category | visual parts | DIY 复用价值 |")
    b("|---|---|---|")
    by_cat = defaultdict(list)
    for v in vps:
        by_cat[v["part_category"]].append(v)
    for k, lst in sorted(by_cat.items(), key=lambda kv: -len(kv[1])):
        reuse = Counter(x["diy_reuse_value"] for x in lst).most_common(1)[0][0]
        b(f"| {k} | {len(lst)} | {reuse} |")
    b("")
    b("---")
    b("")
    b("## 等待人工决定")
    b("")
    b("请在 `P01_HUMAN_REVIEW.md` 中逐套填写，或直接在以下 CSV 中填写"
      "`USER_DECISION` / `USER_PRIORITY` / `USER_NOTE`：")
    b("")
    b("- `P01_OUTFIT_REVIEW.csv`")
    b("- `P01_VISUAL_PARTS.csv`")
    b("- `P01_PARTIAL_CANDIDATES.csv`")
    b("")
    b("**在人工填写完成之前，不进行任何删除、合并、转换或改写。**")
    b("")

    p2 = os.path.join(OUTDIR, "P01_CURATION_SUMMARY.md")
    with open(p2, "w", encoding="utf-8") as fh:
        fh.write("\n".join(s))
    C.log(f"P01_CURATION_SUMMARY.md = {os.path.getsize(p2):,} B")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
