#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p01_parts.py — VISUAL_PART aggregation for P01 curation.

P01 is HUMAN CURATION ASSISTANCE. This module turns the 1,448 frozen ARMO
records into the human-sized unit the brief asks for: a VISUAL_PART, i.e. one
garment the eye recognises, with its colour variants, its duplicate armour
records and its BodySlide variants folded in.

  176 records of "NyesLatexPackLatexUnitard <colour>" -> ONE visual part.

Nothing here judges taste. Every field emitted is an objective technical fact
or a count. USER_DECISION / USER_PRIORITY / USER_NOTE are emitted as
UNDECIDED / UNSET / empty and are never derived from the data.

READ-ONLY: reads the frozen P00 outputs, writes only under reports/P01/.
No mod, plugin, NIF, DDS or BodySlide file is opened for writing, and no
rendering is performed.
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PKT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(PKT, "tools", "P00_RERUN"))
import p00r_common as C  # noqa: E402

OUTDIR = os.path.join(PKT, "reports", "P01")
FROZEN = os.path.join(PKT, "reports", "P00_RERUN")

# P01 writes only into its own curation directory. This is an explicit opt-in,
# not a relaxed guard: a P00 module never calls it, so a P00 tool still cannot
# write anywhere near P01 (or anywhere else).
C.allow_extra_write_root(OUTDIR)

# Colour / finish / edition tokens that make two records the SAME garment.
# Stripping these is what collapses 176 colour variants into one visual part.
VARIANT_TOKENS = {
    # colours
    "BLACK", "BLUE", "BROWN", "GREEN", "GREY", "GRAY", "ORANGE", "PINK",
    "PURPLE", "RED", "WHITE", "YELLOW", "AUBURN", "CREAM", "IVORY", "BEIGE",
    "TAN", "NAVY", "TEAL", "SILVER", "GOLD", "GOLDISH", "BRONZE", "COPPER",
    "PLATINUM", "MAROON", "OLIVE", "LIME", "CYAN", "MAGENTA", "INDIGO",
    "CRIMSON", "SCARLET", "RUBY", "SAPPHIRE", "EMERALD", "AMBER", "TURQUOISE",
    "ROSE", "PEACH", "CORAL", "SALMON", "CHAMPAGNE", "MOCHA", "ESPRESSO",
    "CHARCOAL", "SLATE", "STEEL", "BRONZED", "GOLDEN", "SILVERED",
    # finishes / shades
    "DARK", "LIGHT", "PALE", "DEEP", "BRIGHT", "MUTED", "VIBRANT",
    "DARKER", "LIGHTER", "SHADE", "TONED", "DYED", "COLORED", "COLOURED",
    # edition / variant markers
    "EDITION", "VER", "VERSION", "V2", "MK2", "MKII", "REWORK", "REMAKE",
    "REPLACED", "REVISED", "UPGRADE", "ALT", "ALTERNATE", "VARIANT", "VAR",
    "AA", "BB", "CC", "NPC", "PLAYER", "INVENTORY", "RENDERED", "DROP",
    "WORLD", "PLACEHOLDER", "RIG", "BODY", "SE", "AE",
}

# categories that are individually reusable as a standalone garment
REUSABLE_CATEGORIES = {
    "BOOTS", "HEELS", "SHOES", "GLOVES", "SLEEVES", "MASK", "HOOD", "HAT",
    "COLLAR", "CHOKER", "BELT", "HARNESS", "STRAPS", "ACCESSORY", "DEVIL",
    "DEVICE", "TAIL", "VEIL", "STOCKINGS",
}
# categories that make a piece the centrepiece of an outfit
CORE_CATEGORIES = {"BODY", "BODYSUIT", "CORSET", "PANTY", "BRA", "COAT",
                   "SKIRT", "CLOAK", "CAPE"}

UBE_A = {"BODYSUIT", "BODY", "CORSET", "PANTY", "BRA", "UNITARD"}


def rd(name):
    with open(os.path.join(FROZEN, name), encoding="utf-8-sig",
              newline="") as fh:
        return list(csv.DictReader(fh))


def _tokens(text):
    """-> (display stem, machine key) for an EDID.

    `display` keeps the original casing minus the colour/finish tokens, so the
    human review board shows "NyesLatexOutfit2 Bodysuit" rather than an
    uppercased machine key. `key` is the uppercase, separator-normalised form
    used for grouping.
    """
    if not text:
        return "", ""
    raw = str(text)
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", raw)
    disp_toks, key_toks = [], []
    for tok in re.split(r"[^0-9A-Za-z一-鿿]+", spaced):
        if not tok:
            continue
        up = tok.upper()
        if up in VARIANT_TOKENS or re.fullmatch(r"0*\d+", up) \
                or (up.isdigit() and len(up) <= 3):
            continue
        disp_toks.append(tok)
        key_toks.append(up)
    return " ".join(disp_toks), "_".join(key_toks)


def norm_stem_unused():
    return None


def mesh_family(paths):
    """Family stem from a set of virtual mesh paths (foo_1.nif -> foo)."""
    fams = set()
    for p in paths:
        p = (p or "").replace("/", "\\").strip().lower()
        if not p:
            continue
        base = p.split("\\")[-1]
        base = re.sub(r"\.[a-z0-9]{1,5}$", "", base)
        base = re.sub(r"(1st|2nd|3rd)person.*$", "", base)
        base = re.sub(r"_\d+$", "", base).strip("_- ")
        if base:
            fams.add(base)
    return sorted(fams)


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    parts = rd("04_PARTS_CATALOG.csv")
    logical = rd("15_REWORK_RELATIONSHIPS.csv")
    bs = rd("07_BODYSLIDE_PROJECTS.csv")
    deps = rd("14_CROSS_MOD_DEPENDENCIES.csv")
    merge = rd("18_PLUGIN_MERGE_RISK.csv")
    dupes = rd("12_DUPLICATE_ASSETS.csv")
    mat = rd("11_MATERIAL_CLASSIFICATION.csv")
    pbr = rd("16_PBR_CURRENT_STATE.csv")

    # material per NIF so a part can report its real materials
    mat_by_nif = defaultdict(set)
    for m in mat:
        mc = (m.get("material_class") or "").strip()
        if mc and mc not in ("UNKNOWN", "PENDING_STAGE_11"):
            mat_by_nif[m["NIF_ID"]].add(mc)

    risk_by_mod = defaultdict(set)
    for r in merge:
        mod = r.get("source_mod") or ""
        if mod and r.get("risk_tier"):
            risk_by_mod[mod].add(r["risk_tier"])

    # cross-mod dependency pressure per mod
    dep_by_mod = Counter()
    unres_by_mod = Counter()
    scope = {l["MOD_ID"] for l in logical}
    for d in deps:
        f, t = d.get("from_mod"), d.get("to_mod")
        if f in scope:
            dep_by_mod[f] += 1
        if t not in scope:
            unres_by_mod[f] += 1

    dup_bytes_by_mod = Counter()
    for d in dupes:
        dup_bytes_by_mod[d.get("mod") or d.get("source_mod") or ""] += \
            int(d.get("bytes") or d.get("size") or 0) if str(
                d.get("bytes") or d.get("size") or "0").isdigit() else 0

    def body_of(rowset):
        c = Counter(r.get("body_candidate") or "UNKNOWN" for r in rowset)
        known = {k: v for k, v in c.items() if k != "UNKNOWN"}
        if not known:
            return "UNKNOWN"
        if len(known) > 1:
            return "MIXED"
        return next(iter(known))

    def physics_of(rowset):
        c = Counter()
        for r in rowset:
            ph = (r.get("physics") or "no").lower()
            if ph.startswith("yes:smp") or "smp" in ph:
                c["SMP"] += 1
            elif "havok" in ph or "cbpc" in ph or "tri" in ph:
                c["CBPC"] += 1
        if not c:
            return "NONE" if all((r.get("physics") or "no") == "no"
                                 for r in rowset) else "UNKNOWN"
        return "MIXED" if len(c) > 1 else next(iter(c))

    def norm_stem(text):
        """Strip colour / edition / variant tokens -> garment family stem."""
        return _tokens(text)[1]

    def strip_tokens(text):
        return _tokens(text)[0]

    # ---------------------------------------------------------------- group
    raw = defaultdict(list)
    for r in parts:
        cat = r.get("part_category") or "OTHER"
        stem = norm_stem(r.get("EDID"))
        if len(stem) < 4:
            fam = mesh_family((r.get("game_nif_paths") or "").split(";"))
            stem = "_".join(fam) if fam else \
                f"ARMO_{r.get('ARMO_formid','?')}"
        raw[(r.get("MOD_ID"), cat, stem)].append(r)

    # Unknown colour/finish words ("HOT", "NUDE", ...) are not in the token
    # list, which leaves a family split across near-identical stems. Collapse
    # any stem that is a strict token-prefix of another in the same
    # (mod, category) -- the shorter stem wins, because the longer one only
    # differs by a descriptor we did not recognise.
    by_mc = defaultdict(list)
    for (mod, cat, stem) in raw:
        by_mc[(mod, cat)].append(stem)
    canon = {}
    for key, stems in by_mc.items():
        stems = sorted(stems)
        for i, a in enumerate(stems):
            target = None
            for b in stems:
                if b != a and b.startswith(a + "_"):
                    target = b if target is None or len(b) < len(target) \
                        else target
            canon[(key[0], key[1], a)] = target or a

    groups = defaultdict(list)
    for (mod, cat, stem), rows in raw.items():
        groups[(mod, cat, canon[(mod, cat, stem)])].extend(rows)

    vps = []
    for (mod, cat, stem), rows in sorted(groups.items()):
        outfits = {l["LOGICAL_OUTFIT_ID"] for l in logical
                   if l["MOD_ID"] == mod}
        outfit = next(iter(outfits), "LOGICAL::unknown::" + str(mod))
        nifs = sorted({x.strip() for r in rows
                       for x in (r.get("game_nif_paths") or "").split(";")
                       if x.strip()})
        pend = sorted({x.strip() for r in rows
                       for x in (r.get("pending_build_nifs") or "").split(";")
                       if x.strip()})
        bsp = sorted({x.strip() for r in rows
                      for x in (r.get("bodyslide_projects") or "").split(";")
                      if x.strip()})
        slots = sorted({s.strip() for r in rows
                        for s in (r.get("slot_names") or "").split(";")
                        if s.strip()})
        mats = sorted({m for n in nifs for m in mat_by_nif.get(n, ())})
        has_smp = physics_of(rows) in ("SMP", "MIXED")
        has_phys = physics_of(rows) in ("CBPC", "MIXED", "SMP")
        unres = unres_by_mod.get(mod, 0)
        deps_n = dep_by_mod.get(mod, 0)

        # ---- TECHNICAL_COST (objective only) --------------------------
        cost_reasons = []
        if unres:
            cost_reasons.append(f"{unres} unresolved dep")
        if deps_n >= 50:
            cost_reasons.append(f"{deps_n} cross-mod dep")
        if risk_by_mod.get(mod) == {"HIGH"}:
            cost_reasons.append("HIGH merge risk")
        if bsp and not nifs:
            cost_reasons.append("BodySlide project with no built mesh on disk")
        if not nifs and not pend and not bsp:
            cost_reasons.append("no wearable mesh evidence at all")
        if has_smp:
            cost_reasons.append("SMP cloth")
        if len(cost_reasons) >= 3:
            cost = "HIGH"
        elif cost_reasons:
            cost = "MEDIUM"
        else:
            cost = "LOW"

        # ---- UBE_CONVERSION_CLASS (classification only, no conversion) --
        if not nifs and not pend and not bsp:
            ube = "E"
        elif has_smp or has_phys or cat in ("SKIRT", "COAT", "CLOAK", "CAPE"):
            ube = "D"            # physics / skirt / coat chain
        elif cat in ("DEVICE", "ACCESSORY", "TAIL", "VEIL", "HARNESS") or \
                len(nifs) > 6:
            ube = "C"            # multi-piece / complex accessory
        elif cat in UBE_A:
            ube = "A"            # tight skin-hugging 3BA mesh
        else:
            ube = "B"            # ordinary non-skin-hugging

        # ---- UNIQUENESS -------------------------------------------------
        fam = mesh_family(nifs + pend)
        if not nifs and not bsp:
            uniq = "NO_ASSET"
        elif len(rows) == 1 and not bsp:
            uniq = "SOLO"
        else:
            uniq = f"FAMILY_{len(rows)}"

        # ---- DIY_REUSE_VALUE --------------------------------------------
        if cat in REUSABLE_CATEGORIES:
            reuse = "HIGH"
        elif cat in CORE_CATEGORIES:
            reuse = "LOW"
        else:
            reuse = "MEDIUM"

        # prettiest original EDID stem in the group, original casing kept
        disp = Counter()
        for r in rows:
            d = _tokens(r.get("EDID") or "")[0]
            if d:
                disp[d] += 1
        display = (disp.most_common(1)[0][0] if disp
                   else stem.replace("_", " "))
        vps.append({
            "VISUAL_PART_ID": f"VP::{outfit}::{cat}::{stem}",
            "display_name": display,
            "source_outfit": outfit,
            "MOD_ID": mod,
            "part_category": cat,
            "n_ARMO_records": len(rows),
            "ARMO_formids": ";".join(sorted(r["ARMO_formid"] for r in rows)),
            "ARMA_formids": ";".join(sorted({x for r in rows for x in
                                             (r.get("ARMA_formids") or "")
                                             .split(";") if x})),
            "n_wearable_meshes": len(nifs),
            "wearable_meshes": ";".join(nifs)[:600],
            "pending_build_meshes": ";".join(pend)[:400],
            "mesh_families": ";".join(fam),
            "bodyslide_projects": ";".join(bsp)[:400],
            "slots": ";".join(slots),
            "body_type": body_of(rows),
            "physics": physics_of(rows),
            "materials": ";".join(mats) if mats else "UNKNOWN",
            "cross_mod_dep_count": deps_n,
            "unresolved_dep_count": unres,
            "merge_risk": ";".join(sorted(risk_by_mod.get(mod, {"UNKNOWN"}))),
            "technical_cost": cost,
            "technical_cost_reason": "; ".join(cost_reasons) or "none",
            "uniqueness": uniq,
            "diy_reuse_value": reuse,
            "UBE_CONVERSION_CLASS": ube,
            "CURATION_HINT": "",
            "USER_DECISION": "UNDECIDED",
            "USER_PRIORITY": "UNSET",
            "USER_NOTE": "",
        })

    # ---- CURATION_HINT + PARTIAL candidates ---------------------------
    by_outfit = defaultdict(list)
    for v in vps:
        by_outfit[v["source_outfit"]].append(v)

    partial = []
    for v in vps:
        v["CURATION_HINT"] = ""
    for outfit, items in by_outfit.items():
        core = [v for v in items if v["part_category"] in CORE_CATEGORIES]
        reuse = [v for v in items
                 if v["part_category"] in REUSABLE_CATEGORIES]
        hint_bits = []
        if len(items) > 1:
            hint_bits.append(f"{len(items)} visual part(s)")
        if any(v["n_ARMO_records"] > 1 for v in items):
            hint_bits.append("colour/duplicate variants collapsed")
        if core and reuse:
            hint_bits.append(
                f"centrepiece ({core[0]['display_name']}) plus "
                f"{len(reuse)} independently reusable piece(s)")
        if any(v["technical_cost"] == "HIGH" for v in items):
            hint_bits.append("has a HIGH technical-cost part")
        if any(v["UBE_CONVERSION_CLASS"] == "E" for v in items):
            hint_bits.append("part with unknown conversion class")
        for v in items:
            v["CURATION_HINT"] = "; ".join(hint_bits) or "single part"

        # a PARTIAL candidate = an outfit with a centrepiece body AND several
        # independently reusable accessories. This is a REVIEW HINT only; it
        # never decides anything.
        if core and len(reuse) >= 2:
            n_core_rec = sum(x["n_ARMO_records"] for x in core)
            n_reuse_rec = sum(x["n_ARMO_records"] for x in reuse)
            for v in items:
                partial.append({
                    "candidate_id": f"PARTIAL::{v['VISUAL_PART_ID']}",
                    "source_outfit": outfit,
                    "MOD_ID": v["MOD_ID"],
                    "visual_part": v["display_name"],
                    "VISUAL_PART_ID": v["VISUAL_PART_ID"],
                    "part_category": v["part_category"],
                    "role_in_outfit": ("CENTREPIECE" if v["part_category"]
                                       in CORE_CATEGORIES else "REUSABLE"),
                    "n_ARMO_records": v["n_ARMO_records"],
                    "diy_reuse_value": v["diy_reuse_value"],
                    "technical_cost": v["technical_cost"],
                    "why": (f"outfit has {n_core_rec} centrepiece record(s) "
                            f"and {n_reuse_rec} record(s) in independently "
                            f"reusable categories ({len(reuse)} part(s))"),
                    "note": "REVIEW HINT ONLY - the user decides",
                    "USER_DECISION": "UNDECIDED",
                    "USER_PRIORITY": "UNSET",
                    "USER_NOTE": "",
                })

    cols_vp = ["VISUAL_PART_ID", "display_name", "source_outfit", "MOD_ID",
               "part_category", "n_ARMO_records", "ARMO_formids",
               "ARMA_formids", "n_wearable_meshes", "wearable_meshes",
               "pending_build_meshes", "mesh_families",
               "bodyslide_projects", "slots", "body_type", "physics",
               "materials", "cross_mod_dep_count", "unresolved_dep_count",
               "merge_risk", "technical_cost", "technical_cost_reason",
               "uniqueness", "diy_reuse_value", "UBE_CONVERSION_CLASS",
               "CURATION_HINT", "USER_DECISION", "USER_PRIORITY",
               "USER_NOTE"]
    C.write_csv(os.path.join(OUTDIR, "P01_VISUAL_PARTS.csv"), cols_vp, vps)

    cols_pc = ["candidate_id", "source_outfit", "MOD_ID", "visual_part",
               "VISUAL_PART_ID", "part_category", "role_in_outfit",
               "n_ARMO_records", "diy_reuse_value", "technical_cost", "why",
               "note", "USER_DECISION", "USER_PRIORITY", "USER_NOTE"]
    C.write_csv(os.path.join(OUTDIR, "P01_PARTIAL_CANDIDATES.csv"),
                cols_pc, partial)

    cols_ube = ["VISUAL_PART_ID", "display_name", "source_outfit",
                "part_category", "UBE_CONVERSION_CLASS", "body_type",
                "physics", "n_ARMO_records", "n_wearable_meshes",
                "wearable_meshes", "pending_build_meshes",
                "bodyslide_projects", "materials", "uniqueness",
                "diy_reuse_value", "class_rationale", "note",
                "USER_DECISION", "USER_PRIORITY", "USER_NOTE"]
    RATIONALE = {
        "A": "tight skin-hugging 3BA mesh: bodysuit/body/corset class, no "
             "SMP, no physics chain -- expected to suit automated conversion",
        "B": "ordinary mesh that is not skin-hugging and has no physics chain",
        "C": "multi-piece or complex accessory (device / harness / tail / "
             "many meshes) -- conversion order matters",
        "D": "SMP or CBPC physics, or a skirt / coat / cloak / cape chain -- "
             "convert the chain, not the single mesh",
        "E": "no wearable mesh evidence; class cannot be assigned without "
             "guessing",
    }
    ube_rows = [{**v, "class_rationale": RATIONALE[v["UBE_CONVERSION_CLASS"]],
                 "note": "CLASSIFICATION ONLY - no UBE conversion performed"}
                for v in vps]
    C.write_csv(os.path.join(OUTDIR, "P01_UBE_CONVERSION_PREVIEW.csv"),
                cols_ube, ube_rows)

    C.log(f"P01_VISUAL_PARTS.csv            = {len(vps)} visual parts "
          f"(from {len(parts)} ARMO records)")
    C.log("  category  : " + ", ".join(
        f"{k}={v}" for k, v in Counter(v["part_category"]
                                       for v in vps).most_common(8)))
    C.log("  cost      : " + ", ".join(
        f"{k}={v}" for k, v in Counter(v["technical_cost"]
                                       for v in vps).most_common()))
    C.log("  reuse     : " + ", ".join(
        f"{k}={v}" for k, v in Counter(v["diy_reuse_value"]
                                       for v in vps).most_common()))
    C.log("  UBE class : " + ", ".join(
        f"{k}={v}" for k, v in Counter(v["UBE_CONVERSION_CLASS"]
                                       for v in vps).most_common()))
    C.log(f"P01_PARTIAL_CANDIDATES.csv      = {len(partial)} rows across "
          f"{len({p['source_outfit'] for p in partial})} outfits")
    C.log(f"P01_UBE_CONVERSION_PREVIEW.csv = {len(ube_rows)} rows")
    bad = [v for v in vps if v["USER_DECISION"] != "UNDECIDED"
           or v["USER_PRIORITY"] != "UNSET" or v["USER_NOTE"]]
    C.log(f"  user fields pre-filled: {len(bad)} (must be 0)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
