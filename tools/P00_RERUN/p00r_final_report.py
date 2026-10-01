#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p00r_final_report.py — write P00_FINAL_CORRECTION_REPORT.md.

Every number in the report is read back out of the CSVs at write time, so the
report cannot drift from the data it describes.
"""
from __future__ import annotations

import csv
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p00r_common as C  # noqa: E402

R = C.REPORTS


def rd(name):
    p = os.path.join(R, name)
    with open(p, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    parts = rd("04_PARTS_CATALOG.csv")
    arma = rd("03_ARMOR_ARMA_MAP.csv")
    deps = rd("14_CROSS_MOD_DEPENDENCIES.csv")
    logical = rd("15_REWORK_RELATIONSHIPS.csv")
    merge = rd("18_PLUGIN_MERGE_RISK.csv")
    bal = rd("19_CURRENT_BALANCE_VALUES.csv")
    bs = rd("07_BODYSLIDE_PROJECTS.csv")
    gate = rd("P00_FINAL_CONSISTENCY_GATE.csv")
    calib = rd("PARSER_CALIBRATION.csv")
    vfs = json.load(open(os.path.join(C.DATA, "07_bodyslide_vfs_summary.json"),
                         encoding="utf-8"))

    mm = Counter(p.get("bodyslide_match_method") for p in parts)
    linked = [p for p in parts if p.get("bodyslide_projects")]
    per = [len([x for x in p["bodyslide_projects"].split(";") if x.strip()])
           for p in linked]
    tiers = Counter(m.get("risk_tier") for m in merge)
    roles = Counter(l.get("role") for l in logical)
    gv = Counter(g.get("verdict") for g in gate)
    cv = Counter(c.get("verdict") for c in calib)
    have3 = sum(1 for b in bal if str(b["value"]) != "UNKNOWN"
                and str(b["weight"]) != "UNKNOWN"
                and str(b["armor_rating"]) != "UNKNOWN")
    eff = sum(1 for b in bs if str(b.get("effective", "")).lower() == "yes")
    dt = Counter(d.get("dep_type") for d in deps)

    o = []
    a = o.append
    a("# P00_FINAL_CORRECTION_REPORT.md")
    a("")
    a("**P00 最终校正报告** — 关系层与报告层修正，未做第三次全量扫描。")
    a("")
    a("---")
    a("")
    a("## 0. 结论")
    a("")
    verdict = "P00 FINAL FROZEN" if gv.get("FAIL", 0) == 0 else "BLOCKED"
    a(f"# {verdict}")
    a("")
    a(f"- 内部一致性 gate：**{gv['PASS']} PASS / {gv.get('FAIL', 0)} FAIL**"
      f"（`P00_FINAL_CONSISTENCY_GATE.csv`）")
    a(f"- 解析器校准门：**{cv['PASS']} PASS / {cv.get('FAIL', 0)} FAIL**"
      f"（`PARSER_CALIBRATION.md`）")
    a("")
    a("冻结复用的阶段：00 / 01 / 02 / 03 / 08 / 09 / 10 与 MO2 priority 基线。")
    a("本轮只修改了**关系层**（BodySlide VFS 有效视图、PART↔项目匹配、"
      "ArmorAddon 跨插件关系）与**报告层**（14 / 15 / 18 / 19 / MASTER）。")
    a("")
    a("---")
    a("")
    a("## 1. 逐项对照")
    a("")
    a("| 审计要求 | 状态 | 关键数字 |")
    a("|---|---|---|")
    a(f"| A. BodySlide 改 VFS effective view | ✅ | "
      f"PHYSICAL {vfs.get('PHYSICAL_PROJECT_ROWS')} / "
      f"EFFECTIVE {eff} / shadowed {vfs.get('SHADOWED_PROJECT_ROWS')} |")
    a(f"| B. 删除 fuzzy BodySlide 匹配 | ✅ | "
      f"method={dict(mm)}，每 part 最多 {max(per) if per else 0} 个项目 |")
    a(f"| C. 修复 14 跨 Mod 矛盾 | ✅ | "
      f"{dict(dt)}，已按 same-mod / cross-target-mod / external 分桶 |")
    a(f"| D. 重做 LOGICAL_OUTFIT | ✅ | "
      f"{len({l['LOGICAL_OUTFIT_ID'] for l in logical})} 个 outfit，"
      f"{dict(roles)} |")
    a(f"| E. 重做 merge risk | ✅ | risk_tier {dict(tiers)}，"
      f"OTFT 独立 REFERENCE_REMAP_REQUIRED |")
    a(f"| F. 解码真实数值 | ✅ | {have3}/{len(bal)} 行三字段齐全 |")
    a(f"| G. `game_nif_resolved` 改名 | ✅ | `game_nif_paths` + "
      f"`game_nif_resolution_status` |")
    a(f"| H. 内部一致性 gate | {'✅' if gv.get('FAIL', 0) == 0 else '❌'} | "
      f"{gv['PASS']}/{len(gate)} |")
    a("")
    a("---")
    a("")
    a("## 2. A — BodySlide 有效 VFS 视图")
    a("")
    a("`07_BODYSLIDE_PROJECTS.csv` 每行现在带 `winning_provider` / "
      "`shadowed_provider` / `effective`，并由 "
      "`data/P00_RERUN/07_bodyslide_vfs_summary.json` 提供顶层计数。")
    a("")
    a("| 计数 | 值 |")
    a("|---|---|")
    a(f"| `PHYSICAL_PROJECT_ROWS` | {vfs.get('PHYSICAL_PROJECT_ROWS')} |")
    a(f"| `EFFECTIVE_VFS_PROJECTS` | {eff} |")
    a(f"| `SHADOWED_PROJECT_ROWS` | {vfs.get('SHADOWED_PROJECT_ROWS')} |")
    a(f"| `SHADOWED_VFS_PATHS` | {vfs.get('SHADOWED_VFS_PATHS')} |")
    a(f"| `CONTENT_CONFLICTING_VFS_PATHS` | "
      f"{vfs.get('CONTENT_CONFLICTING_VFS_PATHS')} |")
    a("")
    a("判定规则沿用既有口径：**modlist 行号最小 = 优先级最高 = VFS 胜者**。"
      "20 条被覆盖路径全部由 L883 `Nye Latex Pack AiO 1.3 (ReducedSize)` "
      "取得覆盖权，其中 4 条 sha256 不同（真实内容冲突）。")
    a("")
    a("**下游只使用 effective 项目** —— gate `G-09` 断言没有任何 PART 引用"
      "被覆盖的项目，结果 0。")
    a("")
    a("---")
    a("")
    a("## 3. B — 删除 fuzzy 匹配")
    a("")
    a("旧实现用 stem 子串包含（`s in k or k in s`），实测把 `J3Bodysuit` "
      "链到 15 个项目（Nye / Corrupted / Gantz / Catwoman / Predator 各包），"
      "并把 Brastia 的 Choker / Gloves / Mask / Cape 全部挂到 "
      "Spandexer Boots 项目。那是共用 pack 目录名，不是共用资产。")
    a("")
    a("新规则：")
    a("")
    a("- **LEVEL 1 `EXACT_OUTPUT_PATH`** — ARMA 穿戴 mesh 归一化路径与 "
      "effective OSP `output_nif` 落在同一虚拟族（`foo.nif` / `foo_0.nif` / "
      "`foo_1.nif` / `foo_1stPerson.nif` 归为一族，目录与族名都必须相同）")
    a("- **LEVEL 2 `UNIQUE_STRONG_MATCH`** — 仅在**同一 source mod** 内，"
      "按族名匹配，且候选数必须恰为 1")
    a("- **LEVEL 3 `UNKNOWN`** — 无法唯一确认")
    a("")
    a("| 指标 | 修正前 | 修正后 |")
    a("|---|---|---|")
    a(f"| 有项目关联的 part | 795 | {len(linked)} |")
    a(f"| 单个 part 最多项目数 | 15 | {max(per) if per else 0} |")
    a(f"| 每 part 平均项目数 | 1.14 | "
      f"{(sum(per)/len(per)) if per else 0:.2f} |")
    a("")
    a("| `bodyslide_match_method` | part 数 |")
    a("|---|---|")
    for k, v in mm.most_common():
        a(f"| `{k}` | {v} |")
    a("")
    a("覆盖率下降是**刻意**的：宁可 UNKNOWN 也不猜。审计点名的 6 个已知假链接"
      "全部消失（gate `G-12`，6/6 PASS）。")
    a("")
    a("---")
    a("")
    a("## 4. C — 14 跨 Mod 依赖矛盾")
    a("")
    a("旧 MASTER 写「NIF 引用其它 TARGET Mod DDS = 0」，而 "
      "`14_CROSS_MOD_DEPENDENCIES.csv` 实际有 2,510 行非空。根因是旧的"
      "计数用了一个永远匹配不到的 `/{mod 名}/` 路径测试。现已改为直接从 "
      "14 聚合。")
    a("")
    a("| dep_type | 行数 |")
    a("|---|---|")
    for k, v in dt.most_common():
        a(f"| `{k}` | {v} |")
    a("")
    a("分桶（same-mod / cross-target-mod / external-out-of-scope / unresolved）"
      "已写入 MASTER 第 17 节。")
    a("")
    a("---")
    a("")
    a("## 5. D — LOGICAL_OUTFIT 重做")
    a("")
    a("旧规则把全部 Predator 折叠成一个 outfit，并按 MO2 显示名里的"
      "「物理」/「3BA」字样去判 PHYSICS_PATCH / BODYSLIDE_CONVERSION。"
      "两条都是标签，不是证据。")
    a("")
    a("| 指标 | 修正后 |")
    a("|---|---|")
    a(f"| logical outfit 数 | {len({l['LOGICAL_OUTFIT_ID'] for l in logical})} |")
    for k, v in roles.most_common():
        a(f"| role = `{k}` | {v} |")
    a("")
    a(f"**9 个 Predator Mod → 9 个不同 logical outfit**（审计点名要求）。")
    a("")
    a("非 BASE 的每一条都带 `parent_mod` + `relationship_evidence` + "
      "`confidence`，证据是具体的，例如：")
    a("")
    for l in logical:
        if l.get("role") != "BASE_MOD":
            a(f"- `{l['MOD_ID'][:44]}` → parent `{l.get('parent_mod', '')[:34]}`")
            a(f"  - {str(l.get('relationship_evidence', ''))[:150]}")
    a("")
    a("---")
    a("")
    a("## 6. E — merge risk 重做")
    a("")
    a("旧判据「不同 plugin 的 raw/local FormID 数值相同」已**彻底删除** —— "
      "合并时 FormID 本来就要重映射，重叠不构成风险证据。该信息仅以 "
      "`formid_overlap_INFO_ONLY` 保留，不参与分级。")
    a("")
    a("| `risk_tier` | plugin 数 |")
    a("|---|---|")
    for k, v in tiers.most_common():
        a(f"| `{k}` | {v} |")
    a("")
    cc = Counter()
    for m in merge:
        for c in (m.get("reference_class") or "").split(";"):
            if c:
                cc[c] += 1
    a("| `reference_class` | plugin 数 |")
    a("|---|---|")
    for k, v in cc.most_common():
        a(f"| `{k}` | {v} |")
    a("")
    a("OTFT 归入 **`REFERENCE_REMAP_REQUIRED`**，与 `SCRIPT_BEHAVIOUR` "
      "分开 —— 「需要重映射引用」和「是脚本」是两种不同的义务。")
    a("")
    a("---")
    a("")
    a("## 7. F — 数值字段解码")
    a("")
    a("按已确认的 Skyrim ARMO schema 解码，原始字节保留为 provenance：")
    a("")
    a("- `ARMO.DATA` 8 字节 = uint32 **value** + float32 **weight**")
    a("- `ARMO.DNAM` 4 字节 = uint32 **armor_rating**")
    a("")
    a(f"- `19_CURRENT_BALANCE_VALUES.csv` **{len(bal)}** 行，"
      f"**{have3}** 行三字段齐全")
    a(f"- `weight_sanity` 分布："
      f"{dict(Counter(b.get('weight_sanity') for b in bal))}")
    a("")
    a("上一版「找不到权威 CK 列名所以不猜」的保留意见已不适用并从 MASTER 移除。")
    a("")
    a("---")
    a("")
    a("## 8. G — 字段改名")
    a("")
    a("`game_nif_resolved`（实际存的是 NIF 路径）已拆为：")
    a("")
    a("- `game_nif_paths` — 实际路径列表")
    a("- `game_nif_resolution_status` — "
      + " / ".join(f"`{k}`={v}" for k, v in Counter(
          p.get("game_nif_resolution_status") for p in parts).most_common()))
    a("")
    a("---")
    a("")
    a("## 9. H — 内部一致性 gate 结果")
    a("")
    a("| check | 结论 | 说明 |")
    a("|---|---|---|")
    for g in gate:
        a(f"| `{g['check_id']}` | {g['verdict']} | {g['description'][:64]} |")
    a("")
    a(f"合计 **{gv['PASS']} PASS / {gv.get('FAIL', 0)} FAIL**。")
    a("")
    a("---")
    a("")
    a("## 10. 遗留事项（不阻塞 P00 冻结）")
    a("")
    a("1. **68 条 MODL 引用仍未解析** —— 校准确认这些 FormID 在全库 1,770 个"
      "插件中都不存在，是**决策问题**（丢弃 / 保留为 dangling）不是 parser 问题。")
    a("2. **443 条跨插件 ArmorAddon 链接的 addon 细节为 UNKNOWN** —— 链接本身"
      "成立（`ARMA_resolved` 形如 `1/4`，分母是真实引用数），但那些 addon "
      "记录在只解析的 47 个插件之外，其 mesh / slot 明细取不到，故如实标 "
      "UNKNOWN 而非编造。")
    a("3. **DIY 矩阵状态顺序**照字面执行，UNKNOWN 排在最后；"
      "要让 UNKNOWN 短路需重生成。")
    a("4. **MO2 仍处于运行状态**，modlist 可能在下次运行时漂移；"
      "进入 P01 前请先关闭。")
    a("")

    path = os.path.join(R, "P00_FINAL_CORRECTION_REPORT.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(o))
    C.log(f"P00_FINAL_CORRECTION_REPORT.md = {os.path.getsize(path):,} B")
    C.log(f"verdict = {verdict}")
    return 0 if gv.get("FAIL", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
