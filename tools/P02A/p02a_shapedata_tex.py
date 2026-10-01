# -*- coding: utf-8 -*-
r"""P02A.1-6 -- ShapeData texture rewrite ledger, full coverage.

Sole authority for SHAPEDATA_SOURCE_NIF texture planning. The mesh/texture
teammate table covers GAME_NIF and BODYSLIDE_OUTPUT_NIF only, so this table
must not duplicate it -- it covers every ShapeData source NIF instead.

Coverage rule: every .nif owned by one of the 11 frozen outfits that lives under
CalienteTools\BodySlide\ShapeData\ -- 59 files, including the orphans that no
OSP claims (6 flat CL09 Latex-Rework NIFs + 2 CL11 orphan folders).

Shape names and texture slots come from the frozen P00 NIF parse
(C.P00.get().nifs, nif_class=SHAPEDATA). Nothing is guessed.

Provider resolution order:
  1. frozen P00 VFS winner by exact virtual path
  2. reports/P02A/P02A_GLOBAL_PROVIDER_LOOKUP.csv for references outside the
     frozen scope
  3. UNRESOLVED (never a fuzzy upgrade)

STRICT READ-ONLY: the only writes are this script and its single CSV.
"""
import collections
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p02a_common as C  # noqa: E402

P = C.P00.get()

UNKNOWN = "UNKNOWN"
SD_PREFIX = "CalienteTools/BodySlide/ShapeData/"
TEX_ROOT = "textures\\ZLJ\\CombatLatex\\"

# ------------------------------------------------------------------------
# FROZEN Pack texture-naming rule (lead ruling, P02A.1 review -- authoritative).
# This ledger is the sole authority for SHAPEDATA_SOURCE_NIF texture targets;
# the mesh/texture table must align to these two rules.
#
#   REPOINT_SELF_NAMESPACE   (material already belongs to this outfit)
#       -> textures\\ZLJ\\CombatLatex\\<OUTFIT_ID>\\<file name>
#          flat: the asset is the outfit's own, so it sits at the ns root.
#
#   COPY_FROM_CROSS_OUTFIT / COPY_FROM_EXTERNAL_MOD   (vendored material)
#       -> textures\\ZLJ\\CombatLatex\\<OUTFIT_ID>\\<original relative folder>\\<file name>
#          the original folder is preserved because two different sources can
#          share a base name. Hard evidence: CL09 owns BOTH
#          textures\\ae_corruptedbodysuit\\n.dds AND textures\\ae_latex_kitty\\n.dds;
#          flattening both would silently merge them into one n.dds (measured
#          6 MERGE_CONFLICT rows before this rule, 0 after). Preserving the
#          folder also records which source folder each vendored texture came
#          from, which keeps the copy auditable.
# ------------------------------------------------------------------------
TEX_RULE_SELF = "textures\\ZLJ\\CombatLatex\\<OUTFIT_ID>\\<file name>"
TEX_RULE_VENDORED = "textures\\ZLJ\\CombatLatex\\<OUTFIT_ID>\\<original relative folder>\\<file name>"
TEX_RULE_AUTHORITY = "lead ruling P02A.1 review; ledger is the SHAPEDATA_SOURCE_NIF authority"

ST_REPOINT = "REPOINT_SELF_NAMESPACE"
ST_CROSS = "COPY_FROM_CROSS_OUTFIT"
ST_EXTERNAL = "COPY_FROM_EXTERNAL_MOD"
ST_KEEP = "KEEP_EXTERNAL_REFERENCE"
ST_UNRESOLVED = "UNRESOLVED"

# lookup classification -> status
LOOKUP_MAP = {
    "EXTERNAL_PROVIDER_FOUND": ST_EXTERNAL,
    "GLOBAL_BODY_SKIN": ST_KEEP,
    "VANILLA_ENGINE_RESOURCE": ST_KEEP,
    "TRUE_MISSING": ST_UNRESOLVED,
    "UNKNOWN": ST_UNRESOLVED,
}


def bs(s):
    return str(s or "").replace("/", "\\")


def pack(j):
    return "; ".join(j) if j else "NONE"


# --------------------------------------------------------------------------
# ownership + canonical inventory
# --------------------------------------------------------------------------
OWNER_OF_MOD = {}
for _oid in C.OUTFIT_IDS:
    for _m in P.mods_of_outfit(_oid):
        OWNER_OF_MOD[_m] = _oid

inventory = {}
for f in P.file_index:
    if f["mod"] not in OWNER_OF_MOD or f["ext"] != ".nif":
        continue
    if not C.norm(f["vpath"]).startswith(C.norm(SD_PREFIX)):
        continue
    inventory.setdefault(C.norm(f["vpath"]), f)


def subfolder_of(vpath):
    """'' when the file sits directly in the ShapeData root."""
    rest = C.norm(vpath)[len(C.norm(SD_PREFIX)):]
    return rest.rsplit("/", 1)[0] if "/" in rest else ""


osp_declared = set()
for _oid in C.OUTFIT_IDS:
    for _m in P.mods_of_outfit(_oid):
        for _pr in P.bs_of_mod.get(_m, []):
            osp_declared.add(C.norm(_pr["data_folder"]))

# OSP adopts the rework's flat ShapeData set (CL09_REWORK_VS_BODYSLIDE_DECISION.md R2)
# C.OUTFITS[oid]["support"] maps role -> mod name, so LATEX_REWORK is the KEY.
REWORK_MODS = {mod for o in C.OUTFITS.values()
               for role, mod in o.get("support", {}).items()
               if role == "LATEX_REWORK" and mod in P.priority}


def canonical_flag(vpath, rec):
    sub = subfolder_of(vpath)
    if sub == "" and rec["mod"] in REWORK_MODS:
        return ("ADOPTED_PER_CL09_R2",
                "ADOPTED_PER_CL09_R2: this flat ShapeData NIF has no OSP claimant as "
                "shipped; decision R2 adopts the Latex Rework ShapeData set as the "
                "canonical CL09 ShapeData source for "
                "ZLJ_Combat_Latex/CL09_Corrupted/. Target folder therefore equals the "
                "outfit root with the ORIGINAL file name preserved.")
    if sub and sub not in osp_declared:
        return ("ORPHAN_NO_OSP_CLAIM",
                "ShapeData NIF sits in a folder that no frozen OSP declares; kept in "
                "the outfit footprint, no new target can be derived.")
    return ("OSP_DECLARED",
            "ShapeData NIF lives in an OSP-declared data folder.")


# --------------------------------------------------------------------------
# global provider lookup
# --------------------------------------------------------------------------
LOOKUP_FILE = os.path.join(C.OUT, "P02A_GLOBAL_PROVIDER_LOOKUP.csv")
lookup = {}
if os.path.isfile(LOOKUP_FILE):
    with open(LOOKUP_FILE, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            vp = C.norm(r.get("virtual_path", ""))
            cls = r.get("classification", "")
            if not vp or not cls:
                continue
            # the lookup stores some keys without the textures\ prefix
            lookup.setdefault(vp, cls)
            if not vp.startswith("textures/"):
                lookup.setdefault("textures/" + vp, cls)


def lookup_class(path):
    return lookup.get(C.norm(path))


# --------------------------------------------------------------------------
# optional naming alignment with the mesh/texture table (naming only)
# --------------------------------------------------------------------------
MESH_TEX_CSV = os.path.join(C.OUT, "P02A_NIF_TEXTURE_REWRITE.csv")
align_src = "NONE"
align_map = {}
if os.path.isfile(MESH_TEX_CSV):
    with open(MESH_TEX_CSV, newline="", encoding="utf-8-sig") as fh:
        rd = list(csv.DictReader(fh))
    if rd and "old_dds_path" in rd[0] and "new_dds_path" in rd[0]:
        for r in rd:
            o, n = r.get("old_dds_path", ""), r.get("new_dds_path", "")
            if o and n:
                align_map.setdefault((r.get("OUTFIT_ID", ""), C.norm(o)), bs(n))
        align_src = os.path.basename(MESH_TEX_CSV)


def target_dds(oid, old_dds, status):
    """Apply the frozen Pack texture-naming rule (see TEX_RULE_* constants)."""
    p = bs(old_dds)
    rel = p[len("textures\\"):] if p.lower().startswith("textures\\") \
        else os.path.basename(p)
    if status == ST_REPOINT:
        # frozen rule: own material -> flat file name at the namespace root
        rel = os.path.basename(p)
        basis = "FROZEN_RULE_SELF_NAMESPACE_FLAT_BASENAME"
    else:
        # frozen rule: vendored material -> keep the original relative folder
        basis = "FROZEN_RULE_VENDORED_PRESERVE_ORIGINAL_FOLDER"
    own = TEX_ROOT + oid + "\\" + rel
    hit = align_map.get((oid, C.norm(old_dds)))
    if hit and C.norm(hit) == C.norm(own):
        return own, basis + "_AGREES_WITH_" + align_src
    if hit:
        return own, (basis + "__DIVERGES_FROM_" + align_src
                     + "__divergent_value=" + hit)
    return own, basis


# --------------------------------------------------------------------------
# build the ledger
# --------------------------------------------------------------------------
rows = []
for key in sorted(inventory):
    rec = inventory[key]
    oid = OWNER_OF_MOD[rec["mod"]]
    vpath = bs(rec["vpath"])
    nif = P.nif(rec["vpath"])
    if not nif or not nif.get("shapes"):
        continue
    if nif.get("nif_class") != "SHAPEDATA":
        continue
    canon, canon_note = canonical_flag(rec["vpath"], rec)
    new_folder = "CalienteTools\\BodySlide\\ShapeData\\ZLJ_Combat_Latex\\%s\\" % oid

    for sh in nif.get("shapes", []):
        tex = sh.get("textures") or {}
        # iterate the frozen parse itself: no slot may be silently dropped
        for slot in sorted(tex):
            dds = str(tex.get(slot) or "").strip()
            if not dds:
                continue
            win = P.winner(dds)
            if win is not None:
                wmod = win["mod"]
                if OWNER_OF_MOD.get(wmod) == oid:
                    status = ST_REPOINT
                    basis = "frozen P00 VFS winner is a mod of this outfit"
                    owner = oid
                elif wmod in OWNER_OF_MOD:
                    status = ST_CROSS
                    owner = OWNER_OF_MOD[wmod]
                    basis = ("frozen P00 VFS winner belongs to frozen outfit %s; "
                             "P02A forbids cross-outfit borrowing so the file is "
                             "copied into this outfit's own namespace" % owner)
                else:
                    status = ST_EXTERNAL
                    owner = wmod
                    basis = ("frozen P00 VFS winner is a mod outside the 11 frozen "
                             "outfits; copied in to keep the outfit self-contained")
                new_path, nbasis = target_dds(oid, dds, status)
                src = wmod
                sha = win.get("sha256", "")
                shadowed = P.shadowed(dds)
                look = "IN_FROZEN_VFS"
            else:
                look = lookup_class(dds)
                status = LOOKUP_MAP.get(look, ST_UNRESOLVED) if look else ST_UNRESOLVED
                owner = UNKNOWN
                if look == ST_EXTERNAL:
                    basis = "global lookup classification=EXTERNAL_PROVIDER_FOUND"
                elif look == "GLOBAL_BODY_SKIN":
                    basis = ("global lookup classification=GLOBAL_BODY_SKIN: body/skin "
                             "system asset, reference is kept external and is NEVER "
                             "copied into the outfit namespace (decision R4)")
                elif look == "VANILLA_ENGINE_RESOURCE":
                    basis = ("global lookup classification=VANILLA_ENGINE_RESOURCE: "
                             "stock engine asset, reference is kept external")
                elif look == "TRUE_MISSING":
                    basis = ("global lookup classification=TRUE_MISSING: no provider "
                             "and no game-Data loose file")
                elif look == "UNKNOWN":
                    basis = ("global lookup classification=UNKNOWN (path mismatch): "
                             "same-basename files elsewhere are not proof of identity, "
                             "so no fuzzy upgrade is allowed")
                else:
                    basis = ("not resolvable from the frozen P00 VFS and absent from "
                             "P02A_GLOBAL_PROVIDER_LOOKUP.csv; no fuzzy fallback")
                if status == ST_KEEP:
                    new_path, nbasis = bs(dds), "KEEP_EXTERNAL_REFERENCE_NO_COPY"
                elif status == ST_UNRESOLVED:
                    new_path, nbasis = UNKNOWN, "UNKNOWN"
                else:
                    new_path, nbasis = target_dds(oid, dds, status)
                src = UNKNOWN
                sha = ""
                shadowed = []

            rows.append(dict(
                OUTFIT_ID=oid,
                shapedata_nif=vpath,
                shape_name=sh.get("name", ""),
                texture_slot=slot,
                old_dds_path=bs(dds),
                new_dds_path=new_path,
                source_provider=src,
                status=status,
                notes=basis,
                semantic_type=C.semantic_type(slot, dds),
                shapedata_nif_winning_provider=rec["mod"],
                shapedata_nif_sha256=rec.get("sha256", ""),
                shapedata_new_folder=new_folder,
                canonical_source=canon,
                canonical_source_notes=canon_note,
                new_dds_path_basis=nbasis,
                resolution_source=look,
                source_outfit_owner=owner,
                source_shadowed_providers=pack(shadowed),
                old_dds_sha256=sha,
                collision_flag="NONE",
            ))

# shared-material proposal: one sha256 consumed by more than one frozen outfit
by_sha = collections.defaultdict(set)
for r in rows:
    if r["old_dds_sha256"]:
        by_sha[r["old_dds_sha256"]].add(r["OUTFIT_ID"])
shared_sha = {s for s, o in by_sha.items() if len(o) > 1}
for r in rows:
    s = r["old_dds_sha256"]
    r["shared_material_proposal"] = (
        "PROPOSAL_SHARED_NOT_APPROVED" if s in shared_sha else "NONE")
    r["shared_with_outfits"] = pack(sorted(by_sha[s])) if s in shared_sha else "NONE"

# new_dds_path collision detection inside the Pack
src_of_target = collections.defaultdict(set)
for r in rows:
    if r["new_dds_path"] != UNKNOWN and r["status"] in (ST_REPOINT, ST_CROSS, ST_EXTERNAL):
        src_of_target[C.norm(r["new_dds_path"])].add(C.norm(r["old_dds_path"]))
merged = {t: s for t, s in src_of_target.items() if len(s) > 1}
for r in rows:
    k = C.norm(r["new_dds_path"])
    if r["new_dds_path"] == UNKNOWN or r["status"] not in (ST_REPOINT, ST_CROSS, ST_EXTERNAL):
        r["collision_flag"] = "N/A_KEEP_OR_UNRESOLVED"
    elif k in merged:
        r["collision_flag"] = "MERGE_CONFLICT_%d_SOURCES_INTO_1_TARGET" % len(merged[k])
    else:
        r["collision_flag"] = "NONE"

HEADER = [
    "OUTFIT_ID", "shapedata_nif", "shape_name", "texture_slot", "old_dds_path",
    "new_dds_path", "source_provider", "status", "notes",
    "semantic_type", "shapedata_nif_winning_provider", "shapedata_nif_sha256",
    "shapedata_new_folder", "canonical_source", "canonical_source_notes",
    "new_dds_path_basis", "resolution_source", "source_outfit_owner",
    "source_shadowed_providers", "old_dds_sha256",
    "shared_material_proposal", "shared_with_outfits", "collision_flag",
]

out = os.path.join(C.OUT, "P02A_SHAPEDATA_TEXTURE_REWRITE.csv")
C.write_csv(out, HEADER, [[r.get(h, "") for h in HEADER] for r in rows])


# --------------------------------------------------------------------------
# summary
# --------------------------------------------------------------------------
def summary():
    sys.stdout.reconfigure(encoding="utf-8")
    W = 100
    print("=" * W)
    print("P02A.1-6 ShapeData texture rewrite ledger -- FULL coverage")
    print("sole authority for SHAPEDATA_SOURCE_NIF texture planning")
    print("=" * W)
    covered = {C.norm(r["shapedata_nif"]) for r in rows}
    print("inventory (ShapeData .nif owned by the 11 outfits) = %d" % len(inventory))
    print("covered by this ledger                            = %d" % len(covered))
    missing = sorted(set(inventory) - covered)
    print("still uncovered                                   = %d %s"
          % (len(missing), missing))
    print("rows = %d over %d ShapeData NIF" % (len(rows), len(covered)))
    print("-" * W)
    print("FROZEN Pack texture-naming rule  (authority: %s)" % TEX_RULE_AUTHORITY)
    print("  REPOINT_SELF_NAMESPACE      -> %s" % TEX_RULE_SELF)
    print("  COPY_FROM_*_OUTFIT / _MOD   -> %s" % TEX_RULE_VENDORED)
    print("  KEEP_EXTERNAL_REFERENCE     -> reference unchanged, never copied"
          " (new_dds_path == old_dds_path)")
    print("  UNRESOLVED                  -> new_dds_path = UNKNOWN, never guessed")
    print("  mesh/texture table alignment source = %s (naming comparison only;"
          " this ledger is the SHAPEDATA_SOURCE_NIF authority)" % align_src)
    print("-" * W)
    print("%-20s %5s %6s %7s %7s %7s %7s %7s"
          % ("OUTFIT_ID", "nifs", "rows", "repoint", "cross", "ext", "keep", "unres"))
    for oid in C.OUTFIT_IDS:
        rr = [r for r in rows if r["OUTFIT_ID"] == oid]
        print("%-20s %5d %6d %7d %7d %7d %7d %7d"
              % (oid, len({C.norm(r["shapedata_nif"]) for r in rr}), len(rr),
                 sum(1 for r in rr if r["status"] == ST_REPOINT),
                 sum(1 for r in rr if r["status"] == ST_CROSS),
                 sum(1 for r in rr if r["status"] == ST_EXTERNAL),
                 sum(1 for r in rr if r["status"] == ST_KEEP),
                 sum(1 for r in rr if r["status"] == ST_UNRESOLVED)))
    print("-" * W)
    print("status: %s" % dict(collections.Counter(r["status"] for r in rows)))
    print("resolution_source: %s"
          % dict(collections.Counter(r["resolution_source"] for r in rows)))
    print("canonical_source: %s"
          % dict(collections.Counter(r["canonical_source"] for r in rows)))
    print("unique old dds = %d | unique copy targets = %d"
          % (len({r["old_dds_path"] for r in rows}),
             len({C.norm(r["new_dds_path"]) for r in rows
                  if r["collision_flag"] not in ("N/A_KEEP_OR_UNRESOLVED",)
                  and r["new_dds_path"] != UNKNOWN})))
    print("merge conflicts: %d rows over %d targets"
          % (sum(1 for r in rows if r["collision_flag"].startswith("MERGE_CONFLICT")),
             len(merged)))
    print("shared-material proposals: %d rows / %d distinct sha256"
          % (sum(1 for r in rows if r["shared_material_proposal"] != "NONE"),
             len(shared_sha)))
    # namespace self-check
    bad = [r for r in rows
           if r["new_dds_path"] != UNKNOWN and r["status"] in (ST_REPOINT, ST_CROSS, ST_EXTERNAL)
           and not r["new_dds_path"].lower().startswith(
               (TEX_ROOT + r["OUTFIT_ID"] + "\\").lower())]
    badf = [r for r in rows
            if not r["shapedata_new_folder"].lower().startswith(
                ("calientetools\\bodyslide\\shapedata\\zlj_combat_latex\\"
                 + r["OUTFIT_ID"].lower() + "\\"))]
    print("namespace self-check: new_dds_path violations = %d | ShapeData folder "
          "violations = %d" % (len(bad), len(badf)))
    print("-" * W)
    print("ORPHAN ShapeData coverage (8 files that no OSP claims as shipped):")
    orph = [r for r in rows if r["canonical_source"] != "OSP_DECLARED"]
    per = collections.OrderedDict()
    for r in orph:
        per.setdefault((r["OUTFIT_ID"], r["shapedata_nif"], r["canonical_source"]), 0)
        per[(r["OUTFIT_ID"], r["shapedata_nif"], r["canonical_source"])] += 1
    for (o, n, k), c in per.items():
        print("   %-20s %-62s %-22s rows=%d" % (o, os.path.basename(n), k, c))
    print("orphan rows total = %d" % len(orph))
    print("=" * W)
    print("wrote %s" % out)


if __name__ == "__main__":
    summary()
