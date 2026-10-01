#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p01_outfit.py -- P01 HUMAN CURATION ASSISTANCE :: outfit-level review sheet.

P01 is a CURATION ASSISTANCE phase.  This tool performs NO aesthetic
judgement and NO automatic curation.  It only re-aggregates the FROZEN P00
measurements from the 56 LOGICAL_OUTFIT rows into one flat, human-readable
sheet.  The three user columns are emitted as untouched placeholders:

    USER_DECISION = UNDECIDED
    USER_PRIORITY = UNSET
    USER_NOTE     = (empty)

READ-ONLY contract
------------------
* Every input is opened mode "r" and lives under reports/P00_RERUN (frozen).
* The single write target is reports/P01/P01_OUTFIT_REVIEW.csv and it is
  asserted to sit under reports/P01/ before the file is opened.
* No mod, ESP, NIF, DDS or BodySlide file is opened, written or hashed.
  The MO2 mod folders are never touched at all; folder sizes come from the
  frozen 01_MOD_INVENTORY totals and the frozen file index.

Aggregation rules (all deterministic, all traceable to a P00 column)
-------------------------------------------------------------------
outfit mods
    the 15_REWORK_RELATIONSHIPS row's own MOD_ID, plus its parent_mod when
    parent_in_scope == "in_scope" (a patch/rework row is a sub-unit of the
    outfit it patches).  Rows that merely share a virtual path are NOT merged
    -- P00 already decided the grouping.

body_type
    set of the non-UNKNOWN 04_PARTS_CATALOG.body_candidate values over the
    outfit's parts.  1 value -> that value; >1 -> MIXED; none -> UNKNOWN.

physics
    04_PARTS_CATALOG.physics      yes:havok_tri -> CBPC, yes:nif_smp -> SMP
    01_MOD_INVENTORY.physics_count > 0 -> CBPC
        (p00r_scan.PHYS_EXT = .hkx/.hkproj/.tri/.hkxstd/.hkxstm, i.e. Havok
        collision meshes, which is what CBPC reads.)
    exactly one kind -> that kind; both -> MIXED; none -> UNKNOWN.

material_candidates
    joined through 11_MATERIAL_CLASSIFICATION by NIF_ID (04's own
    material_class column is the PENDING_STAGE_11 placeholder and is NOT
    used).  The mesh set is every distinct 04 nif_ids token for the outfit's
    parts plus every effective (07 output_nif) BodySlide output mesh.  Classes
    are ordered HIGH > MEDIUM > LOW confidence, then alphabetically; UNKNOWN
    is emitted only when nothing else is known.

pbr_state
    16_PBR_CURRENT_STATE asset kinds owned by the outfit's mods
    (PGPATCHER_RULE / LEGACY_DN_ENV) plus 11.fake_metallic_latex over the
    outfit's meshes.  "NONE" = no PBR or fake-metallic evidence exists.

effective_asset_size_bytes
    current_size_bytes minus the exact byte size of every VFS copy this
    outfit's mods LOSE.  13_MO2_CONFLICT_MAP gives (virtual_path, loser_mod);
    the per-copy size is looked up in the frozen P00 stage-A file index and is
    verified to sum to 13's own shadowed_bytes for all 161 rows.  If any loser
    size cannot be looked up the whole column falls back to UNKNOWN -- the
    figure is never estimated.

duplicate_asset_bytes
    12_DUPLICATE_ASSETS.wasted_bytes apportioned to this outfit as
    wasted_bytes * (copies owned by the outfit's mods) / n_copies, because a
    duplicate group is only wasted to the extent that the losing copy is ours.

cross_mod_dependency_count / unresolved_dependency_count
    14_CROSS_MOD_DEPENDENCIES rows whose from_mod belongs to the outfit.
    "Unresolved" is verified at asset level: the row's to_id must not be
    present in ANY of its listed in-scope providers (10_TEXTURE_INVENTORY for
    TEXTURE, 02_PLUGIN_RECORDS for ARMA).  If none of the providers is in
    scope at all the row is likewise unresolved.

merge_risk
    worst 18_PLUGIN_MERGE_RISK.risk_tier across the outfit's plugins,
    ordered LOW_EASY < MODERATE < HIGH.  "NONE" when the outfit ships no
    plugin, "UNKNOWN" when a plugin is missing from 18.

No column of this sheet is an opinion.  A human fills in the three USER_*
columns; this tool never writes them.
"""
from __future__ import annotations

import csv
import gzip
import json
import os
import sys
from collections import Counter, defaultdict

# ------------------------------------------------------------------ paths ----
PROJECT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P00 = os.path.join(PROJECT, "reports", "P00_RERUN")
P00_DATA = os.path.join(PROJECT, "data", "P00_RERUN")
OUT_DIR = os.path.join(PROJECT, "reports", "P01")
OUT_CSV = os.path.join(OUT_DIR, "P01_OUTFIT_REVIEW.csv")

EXPECTED_OUTFITS = 56

COLUMNS = [
    "OUTFIT_ID", "display_name", "source_mods", "plugins",
    "current_size_bytes", "effective_asset_size_bytes",
    "n_ARMO", "n_ARMA", "n_wearable_NIF", "n_texture",
    "n_effective_bodyslide_projects",
    "body_type", "physics", "material_candidates", "pbr_state",
    "cross_mod_dependency_count", "unresolved_dependency_count",
    "merge_risk", "duplicate_asset_bytes",
    "role", "review_hint",
    "USER_DECISION", "USER_PRIORITY", "USER_NOTE",
]

# --------------------------------------------------------- helper readers ----
def read_csv(name):
    path = os.path.join(P00, name)
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def read_gz_json(path):
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        return json.load(fh)


def to_int(value, default=None):
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def to_bool(value):
    return str(value).strip().lower() in ("yes", "true", "1")


def split_list(value):
    """P00 uses '; ' as the intra-cell list separator everywhere."""
    return [t.strip() for t in str(value or "").split(";") if t.strip()]


def nif_key(path):
    return str(path or "").replace("/", "\\").strip().lower()


# ------------------------------------------------------------------ load ----
def main() -> int:
    rel = read_csv("15_REWORK_RELATIONSHIPS.csv")
    if len(rel) != EXPECTED_OUTFITS:
        print(f"FATAL: 15_REWORK_RELATIONSHIPS.csv has {len(rel)} rows, "
              f"expected {EXPECTED_OUTFITS}", file=sys.stderr)
        return 2

    inv = {r["MOD_ID"]: r for r in read_csv("01_MOD_INVENTORY.csv")}
    parts = read_csv("04_PARTS_CATALOG.csv")
    bsp = read_csv("07_BODYSLIDE_PROJECTS.csv")
    textures = read_csv("10_TEXTURE_INVENTORY.csv")
    matcls = read_csv("11_MATERIAL_CLASSIFICATION.csv")
    dups = read_csv("12_DUPLICATE_ASSETS.csv")
    conflicts = read_csv("13_MO2_CONFLICT_MAP.csv")
    deps = read_csv("14_CROSS_MOD_DEPENDENCIES.csv")
    pbr = read_csv("16_PBR_CURRENT_STATE.csv")
    merge = {r["plugin_file"].strip().lower(): r
             for r in read_csv("18_PLUGIN_MERGE_RISK.csv")}

    # stage-A file index: (mod, lowercase vpath) -> size, for exact shadow math
    file_index = {(e["mod"], e["vpath"].lower()): e["size"]
                  for e in read_gz_json(os.path.join(P00_DATA, "01_file_index.json.gz"))}

    # ------------------------------------------------- per-mod lookups ----
    rel_by_mod = {r["MOD_ID"]: r for r in rel}

    parts_by_mod = defaultdict(list)
    for p in parts:
        parts_by_mod[p["MOD_ID"]].append(p)

    bsp_by_mod = defaultdict(list)
    for b in bsp:
        bsp_by_mod[b["MOD_ID"]].append(b)

    tex_by_mod = Counter(t["MOD_ID"] for t in textures)

    # 16 PBR: mod -> set of asset kinds
    pbr_kind_by_mod = defaultdict(set)
    for r in pbr:
        if to_bool(r.get("is_pbr")):
            pbr_kind_by_mod[r["MOD_ID"]].add(r["asset_kind"].strip())

    # 11 materials: NIF_ID -> {class: best confidence rank}
    CONF_RANK = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    mat_by_nif = defaultdict(dict)
    fake_metallic_nifs = set()
    for m in matcls:
        nk = nif_key(m["NIF_ID"])
        if not nk:
            continue
        cls = m["material_class"].strip() or "UNKNOWN"
        rank = CONF_RANK.get(m["confidence"].strip().upper(), 0)
        cur = mat_by_nif[nk].get(cls)
        if cur is None or rank > cur:
            mat_by_nif[nk][cls] = rank
        if to_bool(m.get("fake_metallic_latex")):
            fake_metallic_nifs.add(nk)

    # 14 deps -> resolved flag
    tex_paths_by_mod = defaultdict(set)
    for t in textures:
        tex_paths_by_mod[t["MOD_ID"]].add(t["TEXTURE_ID"].lower())
    arma_by_plugin = defaultdict(set)
    with open(os.path.join(P00, "02_PLUGIN_RECORDS.csv"), "r",
              encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            arma_by_plugin[r["plugin_file"].strip().lower()].add(
                r["formid"].strip().lower())

    deps_by_mod = defaultdict(lambda: [0, 0])          # mod -> [total, unresolved]
    for d in deps:
        src = d["from_mod"].strip()
        if not src:
            continue
        providers = split_list(d["to_mod"])
        ok = False
        for prov in providers:
            if d["to_kind"] == "TEXTURE":
                if d["to_id"].strip().lower() in tex_paths_by_mod.get(prov, ()):
                    ok = True
            else:
                plugin, _, formid = d["to_id"].partition("::")
                if formid.strip().lower() in arma_by_plugin.get(prov.lower(), ()):
                    ok = True
        slot = deps_by_mod[src]
        slot[0] += 1
        if not ok:
            slot[1] += 1

    # 12 duplicates -> per-mod apportioned wasted bytes
    dup_bytes_by_mod = defaultdict(int)
    for d in dups:
        mods = split_list(d["copy_mods"])
        n_copies = to_int(d.get("n_copies"), 0) or 0
        wasted = to_int(d.get("wasted_bytes"), 0) or 0
        if not n_copies or not wasted:
            continue
        for m in mods:
            dup_bytes_by_mod[m] += wasted // n_copies

    # 13 conflicts -> per-mod bytes lost to MO2 shadowing (exact)
    lost_by_mod = defaultdict(int)
    shadow_rows_by_mod = Counter()
    shadow_complete = True
    for c in conflicts:
        vpath = c["virtual_path"].strip().lower()
        losers = split_list(c["loser_mods"])
        lost_here = 0
        total_here = 0
        for l in losers:
            size = file_index.get((l, vpath))
            if size is None:
                shadow_complete = False
                continue
            total_here += size
            lost_by_mod[l] += size
            lost_here += size
        if total_here != (to_int(c.get("shadowed_bytes"), -1) or -1):
            shadow_complete = False
        for l in losers:
            shadow_rows_by_mod[l] += 1

    # 18 merge risk -> per-mod worst tier
    TIER_RANK = {"LOW_EASY": 1, "MODERATE": 2, "HIGH": 3}
    risk_by_mod = {}
    for mod, row in rel_by_mod.items():
        worst, tier_name = 0, ""
        for plug in split_list(row.get("plugin_files")):
            rec = merge.get(plug.lower())
            if rec is None:
                continue
            rank = TIER_RANK.get(rec["risk_tier"].strip().upper(), 0)
            if rank > worst:
                worst, tier_name = rank, rec["risk_tier"].strip()
        if worst:
            risk_by_mod[mod] = tier_name
    plugins_without_risk = set()
    for mod, row in rel_by_mod.items():
        for plug in split_list(row.get("plugin_files")):
            if plug.lower() not in merge:
                plugins_without_risk.add(plug)

    # ------------------------------------------------------ per-outfit ----
    rows = []
    for r in rel:
        oid = r["LOGICAL_OUTFIT_ID"]
        primary = r["MOD_ID"].strip()
        mods = [primary]
        if r.get("parent_in_scope", "").strip() == "in_scope" and r.get("parent_mod", "").strip():
            mods.append(r["parent_mod"].strip())
        modset = set(mods)

        # -- names / plugins
        display = r.get("logical_outfit_name", "").strip() or primary
        plugs, seen = [], set()
        for m in mods:
            for p in split_list(rel_by_mod.get(m, {}).get("plugin_files")):
                if p.lower() not in seen:
                    seen.add(p.lower())
                    plugs.append(p)

        # -- sizes
        current = 0
        size_known = True
        for m in mods:
            row01 = inv.get(m)
            if row01 is None:
                size_known = False
                continue
            current += to_int(row01.get("size_bytes"), 0) or 0
        current_txt = str(current) if size_known else "UNKNOWN"
        if size_known and shadow_complete:
            effective_txt = str(current - sum(lost_by_mod.get(m, 0) for m in mods))
        else:
            effective_txt = "UNKNOWN"

        # -- parts
        myparts = [p for m in mods for p in parts_by_mod.get(m, ())]
        addon_parts = [p for p in myparts if p["MOD_ID"] != primary]
        armo = {p["ARMO_formid"].strip().lower() for p in myparts
                if p["ARMO_formid"].strip()}
        arma = {t.strip().lower() for p in myparts
                for t in split_list(p.get("ARMA_formids")) if t.strip()}
        mesh_nifs = {nif_key(t) for p in myparts for t in split_list(p.get("nif_ids"))}

        mybsp = [b for m in mods for b in bsp_by_mod.get(m, ())]
        eff_bsp = [b for b in mybsp if to_bool(b.get("effective"))]
        shd_bsp = [b for b in mybsp if not to_bool(b.get("effective"))]
        for b in eff_bsp:
            if b.get("output_nif", "").strip():
                mesh_nifs.add(nif_key(b["output_nif"]))

        # The worn mesh of a PENDING_BODYSLIDE part is not in 04.nif_ids at all --
        # P00 leaves that column empty until the BodySlide stage.  For those
        # parts the effective BodySlide project's output_nif IS the wearable
        # mesh, so it is counted here (and only when the project is effective).
        for b in eff_bsp:
            onif = nif_key(b.get("output_nif"))
            if onif.startswith("meshes\\"):
                mesh_nifs.add(onif)
        wearable_nifs = {n for n in mesh_nifs
                         if n and not n.startswith("calientetools\\bodyslide\\")}

        # -- textures
        n_texture = sum(tex_by_mod.get(m, 0) for m in mods)

        # -- body type
        bodies = {p["body_candidate"].strip() for p in myparts
                  if p["body_candidate"].strip() and
                  p["body_candidate"].strip() != "UNKNOWN"}
        body_type = bodies.pop() if len(bodies) == 1 else ("MIXED" if bodies else "UNKNOWN")

        # -- physics
        kinds = set()
        for p in myparts:
            ph = p["physics"].strip()
            if ph == "yes:havok_tri":
                kinds.add("CBPC")
            elif ph == "yes:nif_smp":
                kinds.add("SMP")
        for m in mods:
            if (to_int(inv.get(m, {}).get("physics_count"), 0) or 0) > 0:
                kinds.add("CBPC")
        physics = kinds.pop() if len(kinds) == 1 else ("MIXED" if kinds else "UNKNOWN")

        # -- material candidates
        best = {}
        for n in mesh_nifs:
            for cls, rank in mat_by_nif.get(n, {}).items():
                if cls != "UNKNOWN" and rank > best.get(cls, -1):
                    best[cls] = rank
        if best:
            material_candidates = "; ".join(
                c for c, _ in sorted(best.items(), key=lambda kv: (-kv[1], kv[0])))
        else:
            material_candidates = "UNKNOWN"

        # -- pbr state
        pbr_bits = []
        for m in mods:
            for kind in pbr_kind_by_mod.get(m, ()):
                if kind == "PGPATCHER_RULE":
                    pbr_bits.append("PBRNIFPATCHER_RULES")
                elif kind == "LEGACY_DN_ENV":
                    pbr_bits.append("LEGACY_DN_ENV")
        if mesh_nifs & fake_metallic_nifs:
            pbr_bits.append("FAKE_METALLIC_LATEX")
        pbr_state = "+".join(sorted(set(pbr_bits))) if pbr_bits else "NONE"

        # -- dependencies
        dep_total = sum(deps_by_mod.get(m, [0, 0])[0] for m in mods)
        dep_unres = sum(deps_by_mod.get(m, [0, 0])[1] for m in mods)

        # -- merge risk
        tiers = [TIER_RANK.get(risk_by_mod.get(m, ""), 0) for m in mods]
        if not plugs:
            merge_risk = "NONE"
        elif max(tiers, default=0) == 0:
            merge_risk = "UNKNOWN"
        else:
            merge_risk = next(t for t in ("HIGH", "MODERATE", "LOW_EASY")
                              if TIER_RANK[t] == max(tiers))

        # -- duplicates
        dup_bytes = sum(dup_bytes_by_mod.get(m, 0) for m in mods)

        # -- review hint (facts only)
        shadow_paths = sum(shadow_rows_by_mod.get(m, 0) for m in mods)
        bits = [f"{len(myparts)} parts"]
        if addon_parts:
            bits.append(f"{len(addon_parts)} parts from linked mod "
                        f"{addon_parts[0]['MOD_ID'][:28]}")
        bits.append(f"{len(eff_bsp)} effective / {len(shd_bsp)} shadowed "
                    f"BodySlide projects")
        bits.append(f"{dep_total} cross-mod deps ({dep_unres} unresolved)")
        if shadow_paths:
            bits.append(f"{shadow_paths} VFS paths shadowed")
        if dup_bytes:
            bits.append(f"{dup_bytes / 1048576:.1f} MiB duplicate assets")
        review_hint = ", ".join(bits)

        rows.append({
            "OUTFIT_ID": oid,
            "display_name": display,
            "source_mods": "; ".join(mods),
            "plugins": "; ".join(plugs) if plugs else "NONE",
            "current_size_bytes": current_txt,
            "effective_asset_size_bytes": effective_txt,
            "n_ARMO": len(armo),
            "n_ARMA": len(arma),
            "n_wearable_NIF": len(wearable_nifs),
            "n_texture": n_texture,
            "n_effective_bodyslide_projects": len(eff_bsp),
            "body_type": body_type,
            "physics": physics,
            "material_candidates": material_candidates,
            "pbr_state": pbr_state,
            "cross_mod_dependency_count": dep_total,
            "unresolved_dependency_count": dep_unres,
            "merge_risk": merge_risk,
            "duplicate_asset_bytes": dup_bytes,
            "role": r.get("role", "").strip(),
            "review_hint": review_hint,
            # human-owned fields: emitted untouched, never derived
            "USER_DECISION": "UNDECIDED",
            "USER_PRIORITY": "UNSET",
            "USER_NOTE": "",
        })

    # ---------------------------------------------------------- write ----
    out_abs = os.path.abspath(OUT_CSV)
    if os.path.abspath(OUT_DIR) not in out_abs:
        print(f"FATAL: refusing to write outside {OUT_DIR}", file=sys.stderr)
        return 3
    os.makedirs(OUT_DIR, exist_ok=True)
    tmp = out_abs + ".tmp"
    with open(tmp, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)
    os.replace(tmp, out_abs)

    # --------------------------------------------------------- report ----
    print(f"wrote {out_abs}")
    print(f"rows = {len(rows)} (expected {EXPECTED_OUTFITS})")
    for col in ("body_type", "physics", "pbr_state", "merge_risk", "role"):
        dist = Counter(x[col] for x in rows)
        print(f"  {col:<12} " + ", ".join(f"{k}={v}" for k, v in sorted(dist.items())))
    unk_eff = sum(1 for x in rows if x["effective_asset_size_bytes"] == "UNKNOWN")
    unk_cur = sum(1 for x in rows if x["current_size_bytes"] == "UNKNOWN")
    print(f"  effective_size UNKNOWN rows = {unk_eff}; current_size UNKNOWN rows = {unk_cur}")
    if not shadow_complete:
        print("  NOTE: 13_MO2_CONFLICT_MAP loser sizes did not reconcile; "
              "effective_asset_size_bytes degraded to UNKNOWN")
    if plugins_without_risk:
        print(f"  NOTE: {len(plugins_without_risk)} plugin(s) absent from 18: "
              + ", ".join(sorted(plugins_without_risk)))
    bad = [x["OUTFIT_ID"] for x in rows
           if (x["USER_DECISION"] != "UNDECIDED" or x["USER_PRIORITY"] != "UNSET"
               or x["USER_NOTE"] != "")]
    print(f"  user-field integrity: {'OK (all 56 untouched)' if not bad else 'BROKEN ' + str(bad)}")
    print(f"  distinct OUTFIT_ID = {len({x['OUTFIT_ID'] for x in rows})}")
    return 0 if len(rows) == EXPECTED_OUTFITS and not bad else 4


if __name__ == "__main__":
    sys.exit(main())
