# -*- coding: utf-8 -*-
"""P02A -- BodySlide migration ledger (STRICT READ-ONLY design phase).

Builds two planning CSVs from the frozen P00 evidence set:

  reports/P02A/P02A_BODYSLIDE_MIGRATION.csv
  reports/P02A/P02A_SHAPEDATA_TEXTURE_REWRITE.csv

Chain covered per BodySlide slider set:
    OSP -> ShapeData folder -> input (preset) NIF -> OSD -> output path/file
plus every orphan ShapeData asset that belongs to one of the 11 frozen outfits.

No MO2 / Skyrim / Data file is modified, moved or copied. The only artefacts
this script produces are the two CSVs above. Re-running is deterministic.
"""
import collections
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p02a_common as C  # noqa: E402

P = C.P00.get()

SD_PREFIX = "CalienteTools/BodySlide/ShapeData/"
UNKNOWN = "UNKNOWN"

# --------------------------------------------------------------------------
# frozen planning conventions
# --------------------------------------------------------------------------
# BodySlide UI "Part" label overrides. Only values the P02A brief states
# explicitly are listed here; every other label is a pure textual
# normalisation of the frozen OSP-declared slider set name.
PART_LABEL_OVERRIDE = {
    ("CL04_Haley", "SSE_TFD_Haley_Black_Suit"): ("Bodysuit", "P02A_BRIEF_EXAMPLE"),
}

# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


def _bs(s):
    """MO2-style backslash virtual path."""
    return str(s or "").replace("/", "\\")


def _part_label(oid, ui_name):
    if (oid, ui_name) in PART_LABEL_OVERRIDE:
        return PART_LABEL_OVERRIDE[(oid, ui_name)]
    txt = re.sub(r"[_-]+", " ", str(ui_name or ""))
    txt = re.sub(r"\s+", " ", txt).strip()
    return (txt, "DERIVED_FROM_FROZEN_OSP_SLIDERSET_NAME")


def _part_slug(label):
    return re.sub(r"[^A-Za-z0-9]+", "_", label).strip("_") or "Part"


def _folder_files(folder_norm, ext):
    pref = C.norm(folder_norm) + "/"
    return [f for f in P.file_index
            if C.norm(f["vpath"]).startswith(pref) and f["ext"] == ext]


def _prov(vp):
    return "; ".join(f["mod"] for f in P.providers(vp))


def _pack(j):
    return "; ".join(j) if j else "NONE"


def _key(*parts):
    return "|".join(str(x or "").replace("/", "\\").lower() for x in parts)


# --------------------------------------------------------------------------
# 0. pack-wide mod ownership map
# --------------------------------------------------------------------------
OWNER_OF_MOD = {}
for _oid in C.OUTFIT_IDS:
    for _m in P.mods_of_outfit(_oid):
        OWNER_OF_MOD[_m] = _oid


# --------------------------------------------------------------------------
# 1. effective slider sets + orphan ShapeData assets, per outfit
# --------------------------------------------------------------------------
rows = []
sd_footprint = {}

for oid in C.OUTFIT_IDS:
    mods = P.mods_of_outfit(oid)
    projects = []
    for m in mods:
        projects.extend(P.bs_of_mod.get(m, []))

    used_folders = set()
    for idx, pr in enumerate(projects):
        used_folders.add(C.norm(SD_PREFIX + pr["data_folder"]))
        old_sd = SD_PREFIX + pr["data_folder"]
        old_sd_bs = _bs(old_sd) + "\\"

        osp = _bs(pr["OSP_PATH"])
        ui = pr.get("ui_outfit_name") or UNKNOWN
        label, label_basis = _part_label(oid, ui)
        slug = _part_slug(label)

        nifs = sorted(_folder_files(old_sd, ".nif"), key=lambda f: f["vpath"])
        osds = sorted(_folder_files(old_sd, ".osd"), key=lambda f: f["vpath"])
        nif_names = [os.path.basename(_bs(f["vpath"])) for f in nifs]
        osd_names = [os.path.basename(_bs(f["vpath"])) for f in osds]

        base_nif = _bs(pr.get("base_nif") or (old_sd + "/" + pr["source_file"]))
        base_stem = os.path.basename(base_nif)
        base_stem = os.path.splitext(base_stem)[0]

        old_base_osd = old_sd_bs + base_stem + ".osd"
        if not P.exists(old_base_osd):
            old_base_osd = UNKNOWN

        old_out_path = _bs(pr.get("output_path") or "") or UNKNOWN
        old_out_file = str(pr.get("output_file") or "") or UNKNOWN
        if old_out_path != UNKNOWN and old_out_file != UNKNOWN:
            lod0 = old_out_path + "\\" + old_out_file + "_0.nif"
            lod1 = old_out_path + "\\" + old_out_file + "_1.nif"
        else:
            lod0 = lod1 = UNKNOWN
        lod0_ok = old_out_path != UNKNOWN and P.exists(lod0)
        lod1_ok = old_out_path != UNKNOWN and P.exists(lod1)

        # ---------------- new namespace targets ------------------------
        if idx == 0:
            new_osp = C.OSP_ROOT + "ZLJ_" + oid + ".osp"
            osp_naming = "PACK_RULE_ZLJ_<OUTFIT_ID>.osp"
        else:
            new_osp = C.OSP_ROOT + "ZLJ_" + oid + "__" + slug + ".osp"
            osp_naming = "DEVIATION_MULTI_PART_ZLJ_<OUTFIT_ID>__<PART>.osp"
        new_sd = C.SD_ROOT + oid + "\\" + pr["data_folder"] + "\\"
        new_out_path = C.MESH_ROOT + oid
        new_ui = C.ui_name(oid, label)

        # ---------------- relationship basis ---------------------------
        chain_ok = bool(P.exists(osp) and P.exists(base_nif) and nifs)
        if lod0_ok and lod1_ok and chain_ok:
            basis = "EXACT_OUTPUT_PATH"
        elif chain_ok:
            basis = "FROZEN_STRONG"
        else:
            basis = UNKNOWN

        blockers = []
        notes = []
        if pr.get("effective") != "yes":
            blockers.append("OSP_SHADOWED_NOT_EFFECTIVE")
        if not lod0_ok:
            blockers.append("MISSING_OUTPUT_LOD0")
        if not lod1_ok:
            blockers.append("MISSING_OUTPUT_LOD1")
        if not osds:
            blockers.append("NO_OSD_IN_SHAPEDATA_FOLDER")
        elif old_base_osd == UNKNOWN:
            blockers.append("BASE_PRESET_OSD_MISSING")
        if pr.get("shapedata_nif_count") != len(nifs):
            blockers.append("SHAPEDATA_NIF_COUNT_MISMATCH_P00")
        if pr.get("shapedata_osd_count") != len(osds):
            blockers.append("SHAPEDATA_OSD_COUNT_MISMATCH_P00")
        # deterministic body-family evidence read off the frozen OSP shape list
        # (no fuzzy asset matching): a shape token that starts with 3BA / CBBE / 3BBB.
        shp = list(pr.get("shape_names") or [])
        fams = []
        for s in shp:
            head = str(s).split("_")[0].split(".")[0].upper()
            if head in ("3BA", "CBBE", "3BBB", "BHUNP") and head not in fams:
                fams.append(head)
        derived_fam = "; ".join(fams) or UNKNOWN
        if pr.get("needs_3ba_conversion") == "YES":
            blockers.append("NEEDS_3BA_CONVERSION")
        elif pr.get("needs_3ba_conversion") not in ("YES", "NO") and derived_fam == UNKNOWN:
            blockers.append("BODY_CONVERSION_UNRESOLVED_IN_P00")
        if str(pr.get("output_path_is_guessed")).lower() == "true":
            blockers.append("P00_FLAGGED_OUTPUT_PATH_AS_GUESSED")

        if osp_naming.startswith("DEVIATION"):
            notes.append("DEVIATION: brief defines one OSP per outfit but this outfit "
                         "owns %d slider sets; extra part gets a __<PART> suffix so the "
                         "Pack stays 0-collision." % len(projects))
        notes.append("OSP rewrite attrs: name=%s | outputPath=%s | outputFile=%s; "
                     "datafoldername/niffilename unchanged."
                     % (new_ui, new_out_path, slug))
        notes.append("ShapeData preset file names preserved verbatim; only the ShapeData "
                     "folder moves, so every preset NIF/OSD pair moves 1:1.")
        notes.append("old_input_nif keeps the OSP-declared file name with original case; the "
                     "*_all lists are rebuilt from the lower-cased P00 file_index, so "
                     "re-case them from the source folder when the copy is executed.")
        if derived_fam != UNKNOWN:
            notes.append("P00 body_flag=UNKNOWN but frozen OSP shape list carries %s family "
                         "shape tokens." % derived_fam)
        if pr.get("needs_3ba_conversion") == "YES":
            notes.append("CBBE-only slider set; P00 says a 3BA conversion is required "
                         "before it can join the CBBE_3BA canonical pack.")

        non_canon = C.OUTFITS[oid].get("support", {}).get("NON_CANONICAL_BODY", "")

        rows.append(dict(
            OUTFIT_ID=oid,
            row_kind="SLIDER_SET",
            part_index=idx + 1,
            part_label=label,
            part_label_basis=label_basis,
            old_ui_name=ui,
            old_osp=osp,
            old_shape_data=old_sd_bs,
            old_input_nif=base_nif,
            old_osd=old_base_osd,
            old_output_path=old_out_path,
            old_output_file=old_out_file,
            new_ui_name=new_ui,
            new_osp=new_osp,
            new_shape_data=new_sd,
            new_input_nif=new_sd + os.path.basename(base_nif),
            new_osd=(new_sd + os.path.basename(old_base_osd)
                     if old_base_osd != UNKNOWN else UNKNOWN),
            new_output_path=new_out_path,
            new_output_file=slug,
            relationship_basis=basis,
            slider_count=pr.get("n_sliders", 0),
            shapedata_nif_count=len(nifs),
            osd_count=len(osds),
            old_osp_sha256=pr.get("sha256", ""),
            new_output_sha256_expected=(P.sha(lod0) if lod0_ok else UNKNOWN),
            blockers=";".join(blockers),
            notes=" | ".join(notes),
            old_osp_winning_provider=pr.get("winning_provider") or P.winning_mod(osp),
            old_osp_shadowed_providers=_pack(pr.get("shadowed_provider") or []),
            old_osp_providers=_prov(osp),
            old_shape_data_providers=_pack(sorted({f["mod"] for f in nifs})),
            old_input_nif_all="; ".join(_bs(f["vpath"]) for f in nifs),
            new_input_nif_all="; ".join(new_sd + n for n in nif_names),
            old_osd_all="; ".join(_bs(f["vpath"]) for f in osds),
            new_osd_all="; ".join(new_sd + n for n in osd_names),
            old_output_nif_lod0=(lod0 if lod0_ok else UNKNOWN),
            old_output_nif_lod1=(lod1 if lod1_ok else UNKNOWN),
            old_output_lod0_sha256=(P.sha(lod0) if lod0_ok else UNKNOWN),
            old_output_lod0_providers=(_prov(lod0) if lod0_ok else UNKNOWN),
            old_output_lod0_shadowed_providers=(_pack(P.shadowed(lod0)) if lod0_ok else UNKNOWN),
            derived_body_family_evidence=derived_fam,
            new_output_sha256_basis=("COPY_RENAME_LOD0_VERBATIM" if lod0_ok
                                     else "UNKNOWN_BUILD_OUTPUT_REQUIRED"),
            old_shape_names=_pack(pr.get("shape_names") or []),
            old_osd_slider_count=pr.get("n_sliders", 0),
            old_body_flag=pr.get("body_flag", ""),
            old_body_families=_pack(pr.get("body_families") or []),
            old_needs_3ba_conversion=pr.get("needs_3ba_conversion", ""),
            non_canonical_body=non_canon or "NONE",
            osp_naming_rule=osp_naming,
            collision_flag="NONE",
            collision_key="",
            target_plugin=C.TARGET_PLUGIN,
            _sd=[C.norm(old_sd)],
        ))
        sd_footprint.setdefault(oid, set()).add(C.norm(old_sd))

    # ---- orphan ShapeData NIFs owned by this outfit but not in any OSP ---
    owned = set(mods)
    for f in P.file_index:
        if f["mod"] not in owned or f["ext"] != ".nif":
            continue
        vpn = C.norm(f["vpath"])
        if not vpn.startswith(C.norm(SD_PREFIX)):
            continue
        rest = vpn[len(C.norm(SD_PREFIX)):]
        folder = rest.rsplit("/", 1)[0] if "/" in rest else ""
        folder_norm = C.norm(SD_PREFIX + folder)
        if folder_norm in used_folders:
            continue
        used_folders.add(folder_norm)
        nifs = sorted(_folder_files(folder_norm, ".nif"), key=lambda x: x["vpath"])
        osds = sorted(_folder_files(folder_norm, ".osd"), key=lambda x: x["vpath"])
        label = re.sub(r"\s+", " ", str(folder or f["vpath"])).strip()
        rows.append(dict(
            OUTFIT_ID=oid,
            row_kind="ORPHAN_SHAPEDATA",
            part_index="",
            part_label=label,
            part_label_basis="DERIVED_FROM_ORPHAN_FOLDER_NAME",
            old_ui_name=UNKNOWN,
            old_osp=UNKNOWN,
            old_shape_data=_bs(folder_norm) + "\\",
            old_input_nif=_bs(f["vpath"]),
            old_osd=UNKNOWN,
            old_output_path=UNKNOWN,
            old_output_file=UNKNOWN,
            new_ui_name=UNKNOWN,
            new_osp=UNKNOWN,
            new_shape_data=UNKNOWN,
            new_input_nif=UNKNOWN,
            new_osd=UNKNOWN,
            new_output_path=UNKNOWN,
            new_output_file=UNKNOWN,
            relationship_basis=UNKNOWN,
            slider_count=0,
            shapedata_nif_count=len(nifs),
            osd_count=len(osds),
            old_osp_sha256=UNKNOWN,
            new_output_sha256_expected=UNKNOWN,
            blockers="SHAPEDATA_WITHOUT_OSP;REQUIRES_HUMAN_CONFIRMATION",
            notes=("ShapeData NIF is owned by this outfit's mod (priority %s) but no "
                   "frozen OSP declares it, so there is no frozen strong relationship "
                   "and no derivable new target. Flagged for human confirmation; the "
                   "asset is still inside the outfit footprint so CSV2 covers its "
                   "texture rewrite." % P.priority.get(f["mod"], "?")),
            old_osp_winning_provider=UNKNOWN,
            old_osp_shadowed_providers=UNKNOWN,
            old_osp_providers=UNKNOWN,
            old_shape_data_providers=f["mod"],
            old_input_nif_all="; ".join(_bs(x["vpath"]) for x in nifs),
            new_input_nif_all=UNKNOWN,
            old_osd_all="; ".join(_bs(x["vpath"]) for x in osds),
            new_osd_all=UNKNOWN,
            old_output_nif_lod0=UNKNOWN,
            old_output_nif_lod1=UNKNOWN,
            old_output_lod0_sha256=UNKNOWN,
            old_output_lod0_providers=UNKNOWN,
            old_output_lod0_shadowed_providers=UNKNOWN,
            derived_body_family_evidence=UNKNOWN,
            new_output_sha256_basis="UNKNOWN",
            old_shape_names="",
            old_osd_slider_count=0,
            old_body_flag="",
            old_body_families="",
            old_needs_3ba_conversion=UNKNOWN,
            non_canonical_body=(C.OUTFITS[oid].get("support", {})
                                .get("NON_CANONICAL_BODY", "NONE")),
            osp_naming_rule="NOT_APPLICABLE",
            collision_flag="NONE",
            collision_key="",
            target_plugin=C.TARGET_PLUGIN,
            _sd=[folder_norm],
        ))
        sd_footprint.setdefault(oid, set()).add(folder_norm)


# --------------------------------------------------------------------------
# 2. collision detection inside the Pack
# --------------------------------------------------------------------------
out_hits = collections.Counter(_key(r["new_output_path"], r["new_output_file"]) for r in rows)
osp_hits = collections.Counter(_key(r["new_osp"]) for r in rows)
for r in rows:
    ck = _key(r["new_output_path"], r["new_output_file"])
    r["collision_key"] = ck
    r["collision_flag"] = "NONE"
    if r["new_output_path"] != UNKNOWN and out_hits[ck] > 1:
        r["collision_flag"] = "DUPLICATE_new_output_path+new_output_file(%d)" % out_hits[ck]
    if r["new_osp"] != UNKNOWN and osp_hits[_key(r["new_osp"])] > 1:
        r["collision_flag"] = "DUPLICATE_new_osp"
collisions = [r for r in rows if r["collision_flag"] != "NONE"]


# --------------------------------------------------------------------------
# 3. write CSV 1
# --------------------------------------------------------------------------
HEADER1 = [
    "OUTFIT_ID", "old_ui_name", "old_osp", "old_shape_data", "old_input_nif", "old_osd",
    "old_output_path", "old_output_file",
    "new_ui_name", "new_osp", "new_shape_data", "new_input_nif", "new_osd",
    "new_output_path", "new_output_file",
    "relationship_basis", "slider_count", "shapedata_nif_count", "osd_count",
    "old_osp_sha256", "new_output_sha256_expected", "blockers", "notes",
    "row_kind", "part_index", "part_label", "part_label_basis",
    "old_osp_winning_provider", "old_osp_shadowed_providers", "old_osp_providers",
    "old_shape_data_providers", "old_input_nif_all", "new_input_nif_all",
    "old_osd_all", "new_osd_all",
    "old_output_nif_lod0", "old_output_nif_lod1", "old_output_lod0_sha256",
    "old_output_lod0_providers", "old_output_lod0_shadowed_providers",
    "derived_body_family_evidence", "new_output_sha256_basis",
    "old_shape_names", "old_body_flag", "old_body_families", "old_needs_3ba_conversion",
    "non_canonical_body", "osp_naming_rule", "collision_flag", "collision_key",
    "target_plugin",
]

out1 = os.path.join(C.OUT, "P02A_BODYSLIDE_MIGRATION.csv")
C.write_csv(out1, HEADER1, [[r.get(h, "") for h in HEADER1] for r in rows])


# --------------------------------------------------------------------------
# 4. ShapeData texture rewrite ledger (CSV 2)
# --------------------------------------------------------------------------
# Optional alignment with the mesh/texture teammate's deliverable. When that CSV
# exists it wins; otherwise the fallback naming rule from the brief is used.
TEX_CSV_CANDIDATES = [
    os.path.join(C.OUT, "P02A_NIF_TEXTURE_REWRITE.csv"),
    os.path.join(C.OUT, "P02A_TEXTURE_MIGRATION.csv"),
]
ALIGN_SRC = "NONE"
align_map = {}
align_pairs = []
for cand in TEX_CSV_CANDIDATES:
    if not os.path.isfile(cand):
        continue
    with open(cand, newline="", encoding="utf-8-sig") as fh:
        rd = list(csv.DictReader(fh))
    if not rd:
        continue
    oldc = next((c for c in ("old_dds_path", "old_texture_path", "old_path") if c in rd[0]), None)
    newc = next((c for c in ("new_dds_path", "new_texture_path", "new_path") if c in rd[0]), None)
    if not oldc or not newc:
        continue
    oidc = "OUTFIT_ID" if "OUTFIT_ID" in rd[0] else None
    for rec in rd:
        o, n = rec.get(oldc, ""), rec.get(newc, "")
        if not (o and n):
            continue
        # key by (consuming outfit, old dds): the same source DDS legitimately
        # lands in a DIFFERENT namespace for every outfit that consumes it.
        k = ((rec.get(oidc, "") if oidc else ""), C.norm(o))
        align_map[k] = _bs(n)
    align_pairs = [(r.get("old_dds_path", ""), r.get("new_dds_path", "")) for r in rd]
    ALIGN_SRC = os.path.basename(cand)
    break


def _target_dds(oid, old_dds):
    """New DDS virtual path for the outfit's own texture namespace."""
    if ALIGN_SRC != "NONE":
        hit = align_map.get((oid, C.norm(old_dds)))
        if hit:
            return hit, "ALIGNED_WITH_" + ALIGN_SRC
    # Fallback: no entry in the texture teammate ledger -> keep the original
    # file name and drop it straight under the outfit texture namespace, which
    # is the flat basename convention the teammate ledger already uses.
    rel = os.path.basename(_bs(old_dds))
    return (C.TEX_ROOT + oid + "\\" + rel,
            "FALLBACK_MATCHES_MESHTEX_FLAT_BASENAME_CONVENTION")


# gather every ShapeData NIF in each outfit footprint -> texture slot rows
tex_rows = []
for oid in C.OUTFIT_IDS:
    mods = set(P.mods_of_outfit(oid))
    for folder in sorted(sd_footprint.get(oid, ())):
        for f in sorted(_folder_files(folder, ".nif"), key=lambda x: x["vpath"]):
            nif = P.nif(f["vpath"])
            if nif is None:
                continue
            for shape, slot, dds in P.nif_tex_rows(f["vpath"], nif):
                w = P.winner(dds)
                if w is None:
                    status = "UNRESOLVED"
                    owner = UNKNOWN
                    basis = ("NOT_IN_FROZEN_P00_VFS(3708 files / 56 in-scope mods); "
                             "game Data root is not recorded in P00 evidence and "
                             "re-scanning is out of scope for P02A, so "
                             "vanilla-vs-missing cannot be decided here")
                elif w["mod"] in mods:
                    status = "REPOINT_SELF_NAMESPACE"
                    owner = oid
                    basis = "winning provider is a mod of this outfit"
                elif w["mod"] in OWNER_OF_MOD:
                    status = "COPY_FROM_CROSS_OUTFIT"
                    owner = OWNER_OF_MOD[w["mod"]]
                    basis = ("winning provider belongs to frozen outfit %s; P02A forbids "
                             "cross-outfit borrowing, so the file is copied into this "
                             "outfit's own texture namespace" % owner)
                else:
                    status = "COPY_FROM_EXTERNAL_MOD"
                    owner = w["mod"]
                    basis = ("winning provider is a mod outside the 11 frozen outfits; "
                             "copied in to make the outfit self-contained")
                if w is None:
                    new_path = UNKNOWN
                    nbasis = "UNKNOWN"
                else:
                    new_path, nbasis = _target_dds(oid, dds)
                tex_rows.append(dict(
                    OUTFIT_ID=oid,
                    shapedata_nif=_bs(f["vpath"]),
                    shapedata_nif_winning_provider=f["mod"],
                    shape_name=shape,
                    texture_slot=slot,
                    semantic_type=C.semantic_type(slot, dds),
                    old_dds_path=_bs(dds),
                    new_dds_path=new_path,
                    new_dds_path_basis=nbasis,
                    source_provider=(w["mod"] if w else UNKNOWN),
                    source_shadowed_providers=_pack(P.shadowed(dds) if w else []),
                    source_outfit_owner=owner,
                    old_dds_sha256=(w.get("sha256", "") if w else ""),
                    status=status,
                    notes=basis,
                ))

# shared-material proposal: identical sha256 consumed by >1 frozen outfit
by_sha = collections.defaultdict(set)
for r in tex_rows:
    if r["old_dds_sha256"]:
        by_sha[r["old_dds_sha256"]].add(r["OUTFIT_ID"])
shared_sha = {s for s, oids in by_sha.items() if len(oids) > 1}
for r in tex_rows:
    r["shared_material_proposal"] = (
        "PROPOSAL_SHARED_NOT_APPROVED" if r["old_dds_sha256"] in shared_sha else "NONE")
    r["shared_with_outfits"] = _pack(sorted(shared_sha and by_sha[r["old_dds_sha256"]] or [])) \
        if r["old_dds_sha256"] in shared_sha else "NONE"

# new_dds_path collision detection inside the Pack
src_of_target = collections.defaultdict(set)
for r in tex_rows:
    if r["new_dds_path"] != UNKNOWN:
        src_of_target[C.norm(r["new_dds_path"])].add(C.norm(r["old_dds_path"]))
merged = {t: s for t, s in src_of_target.items() if len(s) > 1}
for r in tex_rows:
    if r["new_dds_path"] == UNKNOWN:
        r["collision_flag"] = "NONE"
    elif C.norm(r["new_dds_path"]) in merged:
        r["collision_flag"] = "MERGE_CONFLICT_%d_SOURCES_INTO_1_TARGET" % len(
            merged[C.norm(r["new_dds_path"])])
    else:
        r["collision_flag"] = "NONE"

HEADER2 = [
    "OUTFIT_ID", "shapedata_nif", "shape_name", "texture_slot", "old_dds_path",
    "new_dds_path", "source_provider", "status", "notes",
    "semantic_type", "shapedata_nif_winning_provider", "new_dds_path_basis",
    "source_shadowed_providers", "source_outfit_owner", "old_dds_sha256",
    "shared_material_proposal", "shared_with_outfits", "collision_flag",
]

out2 = os.path.join(C.OUT, "P02A_SHAPEDATA_TEXTURE_REWRITE.csv")
C.write_csv(out2, HEADER2, [[r.get(h, "") for h in HEADER2] for r in tex_rows])


# --------------------------------------------------------------------------
# 4b. namespace self-check (every planned target must sit in its own outfit ns)
# --------------------------------------------------------------------------
def _violations():
    bad = []
    for r in rows:
        oid = r["OUTFIT_ID"]
        checks = [
            ("new_osp", r["new_osp"], C.OSP_ROOT + "ZLJ_" + oid),
            ("new_shape_data", r["new_shape_data"], C.SD_ROOT + oid + "\\"),
            ("new_output_path", r["new_output_path"], C.MESH_ROOT + oid),
        ]
        for col, val, pref in checks:
            if val == UNKNOWN:
                continue
            if not val.lower().startswith(pref.lower()):
                bad.append("%s %s.%s -> %s" % (oid, col, r["row_kind"], val))
    for r in tex_rows:
        val = r["new_dds_path"]
        if val == UNKNOWN:
            continue
        pref = C.TEX_ROOT + r["OUTFIT_ID"] + "\\"
        if not val.lower().startswith(pref.lower()):
            bad.append("%s new_dds_path -> %s" % (r["OUTFIT_ID"], val))
    return bad


# --------------------------------------------------------------------------
# 5. statistics summary
# --------------------------------------------------------------------------
def summary():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 100)
    print("P02A BodySlide migration ledger  (STRICT READ-ONLY, plan only)")
    print("pack=%s  target_plugin=%s  canonical_body=%s"
          % (C.PACK_ID, C.TARGET_PLUGIN, C.CANONICAL_BODY))
    print("texture naming alignment source: %s" % ALIGN_SRC)
    print("=" * 100)
    print("%-20s %5s %5s %5s %8s %8s %7s %9s"
          % ("OUTFIT_ID", "rows", "sets", "orph", "UNKNOWN", "collide", "blockr", "textrows"))
    for oid in C.OUTFIT_IDS:
        rr = [r for r in rows if r["OUTFIT_ID"] == oid]
        tt = [r for r in tex_rows if r["OUTFIT_ID"] == oid]
        unk = sum(1 for r in rr if UNKNOWN in (r["relationship_basis"], r["new_osp"],
                                               r["new_input_nif"], r["new_output_path"]))
        col = sum(1 for r in rr if r["collision_flag"] != "NONE")
        blk = sum(1 for r in rr if r["blockers"])
        print("%-20s %5d %5d %5d %8d %8d %7d %9d"
              % (oid, len(rr), sum(1 for r in rr if r["row_kind"] == "SLIDER_SET"),
                 sum(1 for r in rr if r["row_kind"] == "ORPHAN_SHAPEDATA"),
                 unk, col, blk, len(tt)))
    print("-" * 100)
    print("CSV1 rows=%d (slider sets=%d, orphan shapedata=%d)"
          % (len(rows), sum(1 for r in rows if r["row_kind"] == "SLIDER_SET"),
             sum(1 for r in rows if r["row_kind"] == "ORPHAN_SHAPEDATA")))
    basis = collections.Counter(r["relationship_basis"] for r in rows)
    print("relationship_basis: %s" % dict(basis))
    print("collisions (new_output_path+new_output_file / new_osp): %d" % len(collisions))
    print("rows carrying blockers: %d" % sum(1 for r in rows if r["blockers"]))
    bc = collections.Counter()
    for r in rows:
        for b in filter(None, r["blockers"].split(";")):
            bc[b] += 1
    print("blocker histogram: %s" % dict(bc))
    print("-" * 100)
    print("CSV2 rows=%d over %d ShapeData NIFs / %d outfits"
          % (len(tex_rows),
             len({r["shapedata_nif"] for r in tex_rows}),
             len({r["OUTFIT_ID"] for r in tex_rows})))
    st = collections.Counter(r["status"] for r in tex_rows)
    print("status: %s" % dict(st))
    print("unique old dds=%d  unique new dds=%d  unresolved targets=%d"
          % (len({r["old_dds_path"] for r in tex_rows}),
             len({r["new_dds_path"] for r in tex_rows if r["new_dds_path"] != UNKNOWN}),
             sum(1 for r in tex_rows if r["new_dds_path"] == UNKNOWN)))
    print("shared-material proposals: %d rows / %d distinct sha256"
          % (sum(1 for r in tex_rows
                 if r["shared_material_proposal"] != "NONE"), len(shared_sha)))
    print("new_dds_path merge conflicts: %d rows over %d targets"
          % (sum(1 for r in tex_rows if r["collision_flag"] != "NONE"), len(merged)))
    print("-" * 100)
    print("cross-outfit borrowing (must become per-outfit copies):")
    co = collections.defaultdict(set)
    for r in tex_rows:
        if r["status"] == "COPY_FROM_CROSS_OUTFIT":
            co[(r["OUTFIT_ID"], r["source_outfit_owner"])].add(r["old_dds_path"])
    for (a, b), s in sorted(co.items()):
        print("   %-20s <- %-20s  %d distinct dds" % (a, b, len(s)))
    print("external-mod dependency (must become per-outfit copies):")
    ex = collections.defaultdict(set)
    for r in tex_rows:
        if r["status"] == "COPY_FROM_EXTERNAL_MOD":
            ex[(r["OUTFIT_ID"], r["source_provider"])].add(r["old_dds_path"])
    for (a, b), s in sorted(ex.items()):
        print("   %-20s <- %-52s %d distinct dds" % (a, b[:52], len(s)))
    print("-" * 100)
    v = _violations()
    print("namespace self-check violations: %d" % len(v))
    for x in v[:20]:
        print("   VIOLATION %s" % x)
    print("-" * 100)
    print("wrote %s" % out1)
    print("wrote %s" % out2)


if __name__ == "__main__":
    summary()
