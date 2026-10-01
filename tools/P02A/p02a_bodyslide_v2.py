# -*- coding: utf-8 -*-
r"""P02A.1-3 -- BodySlide OSP rule freeze + TRI morph separation + physics re-class.

STRICT READ-ONLY design phase. Produces exactly three CSVs:

  reports/P02A/P02A_BODYSLIDE_MIGRATION.csv        (regenerated, frozen OSP rule)
  reports/P02A/P02A_BODYSLIDE_MORPH_MIGRATION.csv  (new -- *.tri = BODY_MORPH_TRI)
  reports/P02A/P02A_PHYSICS_MIGRATION.csv          (regenerated, no HAVOK_TRI)

Frozen decisions implemented here:
  * ONE target OSP per outfit -> CalienteTools\BodySlide\SliderSets\ZLJ_<OID>.osp
    for EVERY row of that outfit. Multiple slider sets share that one OSP and
    are told apart by set_index_in_osp.
  * *.tri is a body morph asset, not a physics config: it moves to the morph
    table and must not appear in the physics table.
  * ShapeData statistics are reported with strict, separate denominators:
    SHAPEDATA_NIF_FILES vs SHAPEDATA_TEXTURE_REWRITE_ROWS.

Nothing in MO2 / Skyrim / Data is modified, copied or moved. The only MO2
access is read-only os.path.isfile + a bounded text read of .xml config files
(never .nif / .dds / .esp binaries). Re-running is deterministic.
"""
import collections
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p02a_common as C  # noqa: E402

P = C.P00.get()

MODS_DIR = r"E:\SkyrimAE\mo2\mods"
SD_PREFIX = "CalienteTools/BodySlide/ShapeData/"
UNKNOWN = "UNKNOWN"

# P02A.1 authority ruling: the ShapeData target folder is ZLJ_Combat_Latex
# (underscore between Combat and Latex). This is deliberately NOT the same as
# the mesh/texture namespace meshes\ZLJ\CombatLatex\<OID>\ .
# C.SD_ROOT in p02a_common.py still carries the old ZLJ_CombatLatex spelling;
# that shared constant is outside this task's write scope, so the corrected
# root is applied locally here and the discrepancy is reported to the lead.
SD_ROOT_TARGET = C.SD_ROOT.replace("ZLJ_CombatLatex", "ZLJ_Combat_Latex")
BONE_OVERLAP_THRESHOLD = 0.60

# --------------------------------------------------------------------------
# Part labels. Only labels an authority stated verbatim are hard-coded; the
# rest are a pure textual normalisation of the frozen OSP slider set name.
# --------------------------------------------------------------------------
PART_LABEL_OVERRIDE = {
    ("CL04_Haley", "SSE_TFD_Haley_Black_Suit"): ("Bodysuit", "P02A_BRIEF_EXAMPLE"),
    ("CL09_Corrupted", "AE_CorruptedBodySuit"): ("Body", "LEAD_EXAMPLE"),
    ("CL09_Corrupted", "AE_CorruptedBodySuit_Hand"): ("Hands", "LEAD_EXAMPLE"),
    ("CL09_Corrupted", "AE_CorruptedBodySuit_Head"): ("Head", "LEAD_EXAMPLE_POSITIONAL"),
    ("CL09_Corrupted", "AE_CorruptedBodySuit_Mask"): ("Mask", "LEAD_EXAMPLE"),
}

# config_type is a closed enum; anything that is not a real SMP / CBPC config
# must land on OTHER_PHYSICS_CONFIG rather than being mislabelled.
CFG_HDT_SMP = "HDT_SMP_XML"
CFG_CBPC = "CBPC_CONFIG"
CFG_OTHER = "OTHER_PHYSICS_CONFIG"
CONFIG_TYPE_ENUM = (CFG_HDT_SMP, CFG_CBPC, CFG_OTHER)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def bs(s):
    return str(s or "").replace("/", "\\")


def norm_key(*parts):
    return "|".join(str(x or "").replace("/", "\\").lower() for x in parts)


def pack(j):
    return "; ".join(j) if j else "NONE"


def abs_path(mod, vpath):
    return os.path.join(MODS_DIR, mod, str(vpath).replace("/", os.sep))


def folder_files(folder_norm, ext):
    pref = C.norm(folder_norm) + "/"
    return [f for f in P.file_index
            if C.norm(f["vpath"]).startswith(pref) and f["ext"] == ext]


def read_text_head(mod, vpath, limit=524288):
    fp = abs_path(mod, vpath)
    if not os.path.isfile(fp):
        return None
    with open(fp, "rb") as fh:
        raw = fh.read(limit)
    return raw.decode("utf-8-sig", errors="ignore")


def part_label(oid, set_name):
    if (oid, set_name) in PART_LABEL_OVERRIDE:
        return PART_LABEL_OVERRIDE[(oid, set_name)]
    txt = re.sub(r"[_-]+", " ", str(set_name or ""))
    return (re.sub(r"\s+", " ", txt).strip(),
            "DERIVED_FROM_FROZEN_OSP_SLIDERSET_NAME")


def part_slug(label):
    return re.sub(r"[^A-Za-z0-9]+", "_", label).strip("_") or "Part"


# --------------------------------------------------------------------------
# ownership map
# --------------------------------------------------------------------------
OWNER_OF_MOD = {}
for _oid in C.OUTFIT_IDS:
    for _m in P.mods_of_outfit(_oid):
        OWNER_OF_MOD[_m] = _oid


# ==========================================================================
# PART A -- BodySlide migration ledger (frozen: ONE OSP per outfit)
# ==========================================================================
rows = []
set_mesh_index = {}   # vpath(built mesh, normalised) -> (osp, set_index, set_name)
sd_folders = {}       # oid -> set of ShapeData folder vpaths

for oid in C.OUTFIT_IDS:
    mods = P.mods_of_outfit(oid)
    projects = []
    for m in mods:
        projects.extend(P.bs_of_mod.get(m, []))
    n_sets = len(projects)

    # ---- frozen target OSP: identical for every row of this outfit --------
    new_osp = C.OSP_ROOT + "ZLJ_" + oid + ".osp"

    used_folders = set()
    for idx, pr in enumerate(projects):
        old_sd = SD_PREFIX + pr["data_folder"]
        used_folders.add(C.norm(old_sd))

        osp = bs(pr["OSP_PATH"])
        ui = pr.get("ui_outfit_name") or UNKNOWN
        set_name = pr.get("slider_set_name") or UNKNOWN
        label, label_basis = part_label(oid, ui)
        slug = part_slug(label)

        nifs = sorted(folder_files(old_sd, ".nif"), key=lambda f: f["vpath"])
        osds = sorted(folder_files(old_sd, ".osd"), key=lambda f: f["vpath"])
        nif_names = [os.path.basename(bs(f["vpath"])) for f in nifs]
        osd_names = [os.path.basename(bs(f["vpath"])) for f in osds]

        base_nif = bs(pr.get("base_nif") or (old_sd + "/" + pr["source_file"]))
        stem = os.path.splitext(os.path.basename(base_nif))[0]
        old_base_osd = bs(old_sd) + "\\" + stem + ".osd"
        if not P.exists(old_base_osd):
            old_base_osd = UNKNOWN

        old_out_path = bs(pr.get("output_path") or "") or UNKNOWN
        old_out_file = str(pr.get("output_file") or "") or UNKNOWN
        if old_out_path != UNKNOWN and old_out_file != UNKNOWN:
            lod0 = old_out_path + "\\" + old_out_file + "_0.nif"
            lod1 = old_out_path + "\\" + old_out_file + "_1.nif"
        else:
            lod0 = lod1 = UNKNOWN
        lod0_ok = old_out_path != UNKNOWN and P.exists(lod0)
        lod1_ok = old_out_path != UNKNOWN and P.exists(lod1)

        new_sd = SD_ROOT_TARGET + oid + "\\" + pr["data_folder"] + "\\"
        new_out_path = C.MESH_ROOT + oid + "\\"
        new_ui = C.ui_name(oid, label)

        # built-mesh reverse index for the morph table
        for cand_stem in [old_out_file] + [os.path.splitext(n)[0] for n in nif_names]:
            if not cand_stem:
                continue
            for suf in ("", "_0", "_1"):
                key = C.norm(old_out_path + "\\" + cand_stem + suf + ".nif")
                if key not in set_mesh_index:
                    set_mesh_index[key] = (osp, idx, set_name)

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
        if pr.get("shapedata_nif_count") != len(nifs):
            blockers.append("SHAPEDATA_NIF_COUNT_MISMATCH_P00")
        if pr.get("shapedata_osd_count") != len(osds):
            blockers.append("SHAPEDATA_OSD_COUNT_MISMATCH_P00")
        if pr.get("needs_3ba_conversion") == "YES":
            blockers.append("NEEDS_3BA_CONVERSION")
        elif pr.get("needs_3ba_conversion") not in ("YES", "NO"):
            shp = list(pr.get("shape_names") or [])
            fams = []
            for s in shp:
                head = str(s).split("_")[0].split(".")[0].upper()
                if head in ("3BA", "CBBE", "3BBB", "BHUNP") and head not in fams:
                    fams.append(head)
            if not fams:
                blockers.append("BODY_CONVERSION_UNRESOLVED_IN_P00")

        notes.append("OSP_RULE=FROZEN_ONE_PER_OUTFIT: this slider set becomes "
                     "set_index_in_osp=%d inside the single target OSP %s "
                     "(source OSP %s is retired)." % (idx, new_osp, osp))
        notes.append("OSP rewrite attrs: name=%s | outputPath=%s | outputFile=%s; "
                     "datafoldername/niffilename unchanged."
                     % (new_ui, new_out_path, slug))
        notes.append("Preset NIF/OSD file names are preserved verbatim; only the "
                     "ShapeData folder moves, so every preset pair moves 1:1.")
        if pr.get("needs_3ba_conversion") == "YES":
            notes.append("CBBE-only slider set; P00 requires a 3BA conversion before "
                         "it can join the CBBE_3BA female canonical pack.")
        if n_sets > 1:
            notes.append("This outfit merges %d source OSPs into 1 target OSP; "
                         "set_index_in_osp disambiguates." % n_sets)

        osp_off = new_osp.lower().startswith((C.OSP_ROOT + "zlj_" + oid).lower())
        sd_off = new_sd.lower().startswith((SD_ROOT_TARGET + oid + "\\").lower())
        out_off = new_out_path.lower().startswith((C.MESH_ROOT + oid).lower())

        rows.append(dict(
            OUTFIT_ID=oid,
            part_label=label,
            old_ui_name=ui,
            new_ui_name=new_ui,
            slider_set_name=set_name,
            set_index_in_osp=idx,
            set_count_in_osp=n_sets,
            slider_count=pr.get("n_sliders", 0),
            old_osp=osp,
            new_osp=new_osp,
            old_shape_data=bs(old_sd) + "\\",
            new_shape_data=new_sd,
            old_input_nif=base_nif,
            new_input_nif=new_sd + os.path.basename(base_nif),
            old_osd=old_base_osd,
            new_osd=(new_sd + os.path.basename(old_base_osd)
                     if old_base_osd != UNKNOWN else UNKNOWN),
            old_output_path=old_out_path,
            old_output_file=old_out_file,
            new_output_path=new_out_path,
            new_output_file=slug,
            relationship_basis=basis,
            collision_check="PENDING",
            blockers=";".join(blockers),
            notes=" | ".join(notes),
            row_kind="SLIDER_SET",
            part_label_basis=label_basis,
            old_osp_sha256=pr.get("sha256", ""),
            new_output_sha256_expected=(P.sha(lod0) if lod0_ok else UNKNOWN),
            new_output_sha256_basis=("COPY_RENAME_LOD0_VERBATIM" if lod0_ok
                                     else "UNKNOWN_BUILD_OUTPUT_REQUIRED"),
            old_osp_winning_provider=pr.get("winning_provider") or P.winning_mod(osp),
            old_osp_shadowed_providers=pack(pr.get("shadowed_provider") or []),
            old_shape_data_providers=pack(sorted({f["mod"] for f in nifs})),
            old_input_nif_all="; ".join(bs(f["vpath"]) for f in nifs),
            new_input_nif_all="; ".join(new_sd + n for n in nif_names),
            old_osd_all="; ".join(bs(f["vpath"]) for f in osds),
            new_osd_all="; ".join(new_sd + n for n in osd_names),
            shapedata_nif_files=len(nifs),
            shapedata_texture_rewrite_rows="SEE_P02A_SHAPEDATA_TEXTURE_REWRITE_CSV",
            old_output_nif_lod0=(lod0 if lod0_ok else UNKNOWN),
            old_output_nif_lod1=(lod1 if lod1_ok else UNKNOWN),
            old_body_flag=pr.get("body_flag", ""),
            old_needs_3ba_conversion=pr.get("needs_3ba_conversion", ""),
            non_canonical_body=(C.OUTFITS[oid].get("support", {})
                                .get("NON_CANONICAL_BODY", "NONE")),
            osp_off_namespace="NO" if osp_off else "YES",
            outputpath_off_namespace="NO" if out_off else "YES",
            shapedata_off_namespace="NO" if sd_off else "YES",
            target_plugin=C.TARGET_PLUGIN,
        ))
        sd_folders.setdefault(oid, set()).add(C.norm(old_sd))

    # ---- orphan ShapeData NIFs: owned by the outfit, claimed by no OSP -----
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
        nifs = sorted(folder_files(folder_norm, ".nif"), key=lambda x: x["vpath"])
        osds = sorted(folder_files(folder_norm, ".osd"), key=lambda x: x["vpath"])
        label = re.sub(r"\s+", " ", str(folder or f["vpath"])).strip()
        rows.append(dict(
            OUTFIT_ID=oid, part_label=label, old_ui_name=UNKNOWN, new_ui_name=UNKNOWN,
            slider_set_name=UNKNOWN, set_index_in_osp="", set_count_in_osp=n_sets,
            slider_count=0, old_osp=UNKNOWN, new_osp=new_osp,
            old_shape_data=bs(folder_norm) + "\\", new_shape_data=UNKNOWN,
            old_input_nif=bs(f["vpath"]), new_input_nif=UNKNOWN,
            old_osd=UNKNOWN, new_osd=UNKNOWN,
            old_output_path=UNKNOWN, old_output_file=UNKNOWN,
            new_output_path=UNKNOWN, new_output_file=UNKNOWN,
            relationship_basis=UNKNOWN, collision_check="PENDING",
            blockers="SHAPEDATA_WITHOUT_OSP;REQUIRES_HUMAN_CONFIRMATION",
            notes=("ShapeData NIF is owned by this outfit's mod (priority %s) but no "
                   "frozen OSP declares it, so no frozen strong relationship exists and "
                   "no new target can be derived without human confirmation. It is kept "
                   "in the outfit footprint so the ShapeData texture ledger still "
                   "covers it. new_osp is shown only to record that the outfit owns "
                   "exactly one target OSP; this row does not claim it."
                   % P.priority.get(f["mod"], "?")),
            row_kind="ORPHAN_SHAPEDATA",
            part_label_basis="DERIVED_FROM_ORPHAN_FOLDER_NAME",
            old_osp_sha256=UNKNOWN, new_output_sha256_expected=UNKNOWN,
            new_output_sha256_basis="UNKNOWN",
            old_osp_winning_provider=UNKNOWN, old_osp_shadowed_providers=UNKNOWN,
            old_shape_data_providers=f["mod"],
            old_input_nif_all="; ".join(bs(x["vpath"]) for x in nifs),
            new_input_nif_all=UNKNOWN,
            old_osd_all="; ".join(bs(x["vpath"]) for x in osds),
            new_osd_all=UNKNOWN,
            shapedata_nif_files=len(nifs),
            shapedata_texture_rewrite_rows="SEE_P02A_SHAPEDATA_TEXTURE_REWRITE_CSV",
            old_output_nif_lod0=UNKNOWN, old_output_nif_lod1=UNKNOWN,
            old_body_flag="", old_needs_3ba_conversion=UNKNOWN,
            non_canonical_body=(C.OUTFITS[oid].get("support", {})
                                .get("NON_CANONICAL_BODY", "NONE")),
            osp_off_namespace="NO", outputpath_off_namespace="NO",
            shapedata_off_namespace="NO", target_plugin=C.TARGET_PLUGIN,
        ))
        sd_folders.setdefault(oid, set()).add(folder_norm)


# ---- collision + off-namespace accounting ---------------------------------
out_hits = collections.Counter(
    norm_key(r["new_output_path"], r["new_output_file"]) for r in rows)
for r in rows:
    ck = norm_key(r["new_output_path"], r["new_output_file"])
    if r["new_output_path"] == UNKNOWN:
        r["collision_check"] = "N/A_UNRESOLVED_ROW"
    elif out_hits[ck] > 1:
        r["collision_check"] = "COLLISION_new_output_path+new_output_file(%d)" % out_hits[ck]
    else:
        r["collision_check"] = "OK_UNIQUE"
    if r["new_shape_data"] != UNKNOWN:
        sd_hits = collections.Counter(
            norm_key(x["new_shape_data"]) for x in rows
            if x["new_shape_data"] != UNKNOWN)
        if sd_hits[norm_key(r["new_shape_data"])] > 1:
            r["collision_check"] = "COLLISION_new_shape_data"

osp_per_outfit = collections.defaultdict(set)
for r in rows:
    osp_per_outfit[r["OUTFIT_ID"]].add(r["new_osp"])
osp_rule_ok = all(len(v) == 1 for v in osp_per_outfit.values())
for r in rows:
    if r["collision_check"].startswith("COLLISION_new_osp"):
        r["collision_check"] = "COLLISION_new_osp"


HEADER_BS = [
    "OUTFIT_ID", "part_label", "old_ui_name", "new_ui_name", "slider_set_name",
    "set_index_in_osp", "slider_count",
    "old_osp", "new_osp", "old_shape_data", "new_shape_data",
    "old_input_nif", "new_input_nif", "old_osd", "new_osd",
    "old_output_path", "old_output_file", "new_output_path", "new_output_file",
    "relationship_basis", "collision_check", "blockers", "notes",
    "row_kind", "set_count_in_osp", "part_label_basis",
    "shapedata_nif_files", "shapedata_texture_rewrite_rows",
    "old_osp_sha256", "new_output_sha256_expected", "new_output_sha256_basis",
    "old_osp_winning_provider", "old_osp_shadowed_providers",
    "old_shape_data_providers", "old_input_nif_all", "new_input_nif_all",
    "old_osd_all", "new_osd_all",
    "old_output_nif_lod0", "old_output_nif_lod1",
    "old_body_flag", "old_needs_3ba_conversion", "non_canonical_body",
    "osp_off_namespace", "outputpath_off_namespace", "shapedata_off_namespace",
    "target_plugin",
]
C.write_csv(os.path.join(C.OUT, "P02A_BODYSLIDE_MIGRATION.csv"),
            HEADER_BS, [[r.get(h, "") for h in HEADER_BS] for r in rows])


# ==========================================================================
# PART B -- BODY_MORPH_TRI  (*.tri is a morph asset, NOT a physics config)
# ==========================================================================
nif_bones = collections.defaultdict(set)
for n in P.nifs:
    bs_ = set()
    for sh in n.get("shapes", []) or []:
        bs_ |= set(sh.get("bones") or [])
    nif_bones[C.norm(n["path"])] = bs_


def bind_tri(tri_vpath, oid):
    """Deterministic tri -> mesh binding. No fuzzy guessing."""
    stem = os.path.splitext(os.path.basename(tri_vpath))[0]
    folder = tri_vpath.rsplit("/", 1)[0]
    for suf in ("", "_0", "_1"):
        cand = C.norm(folder + "/" + stem + suf + ".nif")
        w = P.winner(cand)
        if w and w["mod"] in OWNER_OF_MOD and OWNER_OF_MOD[w["mod"]] == oid:
            return cand, "SAME_MOD_SAME_DIR_SAME_STEM"
    best = (0.0, None)
    for nv, bones in nif_bones.items():
        w = P.winning_mod(nv)
        if OWNER_OF_MOD.get(w) != oid or not bones:
            continue
        frac = 1.0  # placeholder replaced below by caller via xml bones
        best = (frac, nv)
    return None, UNKNOWN


morph_rows = []
for f in sorted([x for x in P.file_index if x["ext"] == ".tri"],
                key=lambda x: (OWNER_OF_MOD.get(x["mod"], ""), x["vpath"])):
    oid = OWNER_OF_MOD.get(f["mod"])
    if oid is None:
        continue
    tri = bs(f["vpath"])
    mesh, evidence = bind_tri(f["vpath"], oid)
    if mesh is None:
        mesh = UNKNOWN
        evidence = "NO_SAME_MOD_SAME_DIR_SAME_STEM_MESH"
        blockers = "TRI_MESH_BINDING_UNRESOLVED"
        status = "UNRESOLVED"
        set_info = (UNKNOWN, "", "")
    else:
        blockers = ""
        status = "COPY_AND_REPOINT"
        osp, sidx, sname = set_mesh_index.get(C.norm(mesh), (UNKNOWN, "", ""))
        new_osp_for_set = C.OSP_ROOT + "ZLJ_" + oid + ".osp"
        set_info = ("%s#%s" % (new_osp_for_set, sidx) if osp != UNKNOWN else UNKNOWN,
                    osp, sname)
    target = C.MESH_ROOT + oid + "\\" + os.path.basename(tri)
    mesh_target = UNKNOWN
    if mesh != UNKNOWN:
        mesh_csv = os.path.join(C.OUT, "P02A_MESH_MIGRATION.csv")
        if os.path.isfile(mesh_csv):
            with open(mesh_csv, newline="", encoding="utf-8-sig") as fh:
                for rec in csv.DictReader(fh):
                    if C.norm(rec.get("source_virtual_path", "")) == C.norm(mesh):
                        mesh_target = rec.get("target_virtual_path", UNKNOWN)
                        break
        if mesh_target == UNKNOWN:
            mesh_target = C.MESH_ROOT + oid + "\\" + os.path.basename(mesh)

    morph_rows.append(dict(
        OUTFIT_ID=oid,
        source_tri=tri,
        associated_output_nif=(bs(mesh) if mesh != UNKNOWN else UNKNOWN),
        **{"associated_osp/set": set_info[0]},
        target_tri=target,
        BODYTRI_reference_rewrite_required="YES",
        status=status,
        associated_osp_source=set_info[1],
        associated_set_name=set_info[2],
        mesh_binding_evidence=evidence,
        source_provider=f["mod"],
        provider_priority=P.priority.get(f["mod"], ""),
        shadowed_providers=pack(P.shadowed(f["vpath"])),
        sha256=f.get("sha256", ""),
        size=f.get("size", ""),
        associated_output_nif_target=mesh_target,
        blockers=blockers,
        notes=("ASSET_CLASS=BODY_MORPH_TRI: a .tri is a body morph asset, not a "
               "physics config, so it is recorded here and removed from "
               "P02A_PHYSICS_MIGRATION.csv. It keeps its original file name inside "
               "the outfit mesh namespace, matching P02A_MESH_MIGRATION.csv. "
               "Reference rewrite required because the virtual path changes."),
        target_plugin=C.TARGET_PLUGIN,
    ))

HEADER_MORPH = [
    "OUTFIT_ID", "source_tri", "associated_output_nif", "associated_osp/set",
    "target_tri", "BODYTRI_reference_rewrite_required", "status",
    "associated_osp_source", "associated_set_name", "mesh_binding_evidence",
    "source_provider", "provider_priority", "shadowed_providers",
    "sha256", "size", "associated_output_nif_target", "blockers", "notes",
    "target_plugin",
]
C.write_csv(os.path.join(C.OUT, "P02A_BODYSLIDE_MORPH_MIGRATION.csv"),
            HEADER_MORPH, [[r.get(h, "") for h in HEADER_MORPH] for r in morph_rows])


# ==========================================================================
# PART C -- physics configs only (NO .tri here)
# ==========================================================================
def classify_config(text, ext):
    """Deterministic, content-based classification. Closed enum."""
    if ext != ".xml":
        # Only CBPC lives outside XML. Everything else non-XML (PBR NifPatcher
        # json, meta.ini, KeywordInjector ini) is NOT a physics config.
        if re.search(r"(?i)cbpc|collisionObject", text):
            return CFG_CBPC, "CBPC_JSON", UNKNOWN
        return None, "NOT_A_PHYSICS_CONFIG", UNKNOWN
    stripped = re.sub(r"<\?.*?\?>", "", text, flags=re.S)
    m = re.search(r"<([A-Za-z_:][\w.:-]*)", stripped)
    root = m.group(1) if m else UNKNOWN
    if root == "SMP":
        return CFG_HDT_SMP, "SMP_XML", root
    if root == "system":
        # AUTHORITY RULING (lead, P02A.1 review): every in-scope Havok system
        # description that belongs to a Pack outfit is classified HDT_SMP_XML.
        # config_format keeps the literal on-disk evidence so nothing is lost.
        if "description.xsd" in text or re.search(r"<\s*per-triangle-shape", text):
            return CFG_HDT_SMP, "HAVOK_SYSTEM_DESCRIPTION_XML", root
        return CFG_HDT_SMP, "GENERIC_SYSTEM_XML", root
    if re.search(r"(?i)cbpc|collisionObject", text):
        return CFG_CBPC, "CBPC_XML", root
    return None, "NOT_A_PHYSICS_CONFIG", root


phys_rows = []
xml_candidates = [f for f in P.file_index if f["ext"] in (".xml", ".json")
                  and f["mod"] in OWNER_OF_MOD]
for f in sorted(xml_candidates, key=lambda x: (OWNER_OF_MOD[x["mod"]], x["vpath"])):
    oid = OWNER_OF_MOD[f["mod"]]
    text = read_text_head(f["mod"], f["vpath"])
    if text is None:
        continue
    ctype, cfmt, root = classify_config(text, f["ext"])
    if ctype is None:
        continue                       # tintmasks / slidergroups / presets etc.
    xbones = set(re.findall(r"<bone\s+name=\"([^\"]+)\"", text))
    tags = re.findall(r"<per-triangle-shape\s+name=\"([^\"]+)\"", text)
    same_stem = C.norm(f["vpath"].rsplit("/", 1)[0] + "/"
                       + os.path.splitext(os.path.basename(f["vpath"]))[0] + ".nif")
    mesh, evidence = None, "NONE"
    if P.exists(same_stem) and OWNER_OF_MOD.get(P.winning_mod(same_stem)) == oid:
        mesh, evidence = same_stem, "SAME_MOD_SAME_DIR_SAME_STEM"
    elif xbones:
        best = (0.0, None)
        for nv, boneset in nif_bones.items():
            if OWNER_OF_MOD.get(P.winning_mod(nv)) != oid or not boneset:
                continue
            frac = len(boneset & xbones) / float(len(xbones))
            if frac > best[0]:
                best = (frac, nv)
        if best[0] >= BONE_OVERLAP_THRESHOLD:
            mesh, evidence = best[1], "BONE_OVERLAP_%.2f" % best[0]

    if mesh is not None:
        ref_bones = nif_bones.get(C.norm(mesh), set())
        missing = sorted(xbones - ref_bones)
    else:
        ref_bones, missing = set(), []
    if mesh is None:
        status = "UNRESOLVED_NO_MESH_BINDING"
        blockers = "PHYSICS_MESH_BINDING_UNRESOLVED"
    elif P.winning_mod(f["vpath"]) != f["mod"]:
        status = "COPY_AND_REPOINT_EXTERNAL_WINNER"
        blockers = "VFS_WINNER_IS_EXTERNAL_MOD"
    else:
        status = "COPY_AND_REPOINT"
        blockers = ""

    shadow = P.shadowed(f["vpath"])
    providers = [x["mod"] for x in P.providers(f["vpath"])]
    if len(providers) > 1 and shadow:
        status = status if status.startswith("COPY") else status

    new_cfg = (C.MESH_ROOT + oid + "\\physics\\"
               + os.path.basename(bs(f["vpath"])))
    phys_rows.append(dict(
        OUTFIT_ID=oid,
        config_file=bs(f["vpath"]),
        config_type=ctype,
        config_format=cfmt,
        xml_root_element=root,
        current_provider=f["mod"],
        vfs_winning_provider=P.winning_mod(f["vpath"]) or UNKNOWN,
        provider_priority=P.priority.get(f["mod"], ""),
        shadowed_providers=pack(shadow),
        all_providers=pack(providers),
        sha256=f.get("sha256", ""),
        size=f.get("size", ""),
        mesh_references=(bs(mesh) if mesh else UNKNOWN),
        mesh_binding_evidence=evidence,
        xml_bone_count=len(xbones),
        xml_per_triangle_tags=pack(tags),
        mesh_bone_count=len(ref_bones),
        bone_check_status=("MISSING_BONE" if missing else
                           ("OK" if mesh else "UNKNOWN")),
        missing_bones=pack(missing) if missing else "NONE",
        old_path_refs=bs(f["vpath"]),
        new_path_refs=new_cfg,
        rewrite_required="YES" if mesh else "UNKNOWN",
        status=status,
        blockers=blockers,
        notes=("config_type=HDT_SMP_XML per the P02A.1 authority ruling; "
               "config_format=%s records the literal on-disk format "
               "(root element <%s>, Havok description.xsd schema). "
               "Binding evidence: %s. %s"
               % (cfmt, root, evidence,
                  ("Shipped by this outfit's mod but the VFS winner is an "
                   "external mod, so P02A still copies it in."
                   if P.winning_mod(f["vpath"]) != f["mod"] else ""))),
        target_plugin=C.TARGET_PLUGIN,
    ))

HEADER_PHYS = [
    "OUTFIT_ID", "config_file", "config_type", "config_format", "xml_root_element",
    "current_provider", "vfs_winning_provider", "provider_priority",
    "shadowed_providers", "all_providers", "sha256", "size",
    "mesh_references", "mesh_binding_evidence",
    "xml_bone_count", "xml_per_triangle_tags", "mesh_bone_count",
    "bone_check_status", "missing_bones",
    "old_path_refs", "new_path_refs", "rewrite_required", "status", "blockers",
    "notes", "target_plugin",
]
C.write_csv(os.path.join(C.OUT, "P02A_PHYSICS_MIGRATION.csv"),
            HEADER_PHYS, [[r.get(h, "") for h in HEADER_PHYS] for r in phys_rows])


# ==========================================================================
# PART D -- strict, separate counters (audit item 6)
# ==========================================================================
shapedata_all = {f["vpath"] for f in P.file_index
                 if f["mod"] in OWNER_OF_MOD and f["ext"] == ".nif"
                 and C.norm(f["vpath"]).startswith(C.norm(SD_PREFIX))}
osp_declared_folders = set()
for _oid in C.OUTFIT_IDS:
    for _m in P.mods_of_outfit(_oid):
        for _pr in P.bs_of_mod.get(_m, []):
            osp_declared_folders.add(C.norm(SD_PREFIX + _pr["data_folder"]))
shapedata_nif_files = sorted(shapedata_all)
shapedata_in_folders = sorted(v for v in shapedata_all
                              if C.norm(v).rsplit("/", 1)[0] in osp_declared_folders)
shapedata_root_orphan = sorted(v for v in shapedata_all
                               if C.norm(v).rsplit("/", 1)[0] not in osp_declared_folders)

bodyslide_out_nifs = sorted({
    k for k in set_mesh_index
    if P.exists(k.replace("/", "\\"))})

morph_tris = sorted({r["source_tri"] for r in morph_rows})

outfit_nifs = {f["vpath"] for f in P.file_index
               if f["mod"] in OWNER_OF_MOD and f["ext"] == ".nif"}
game_nifs = sorted(C.norm(v) for v in outfit_nifs
                   if C.norm(v) not in set_mesh_index
                   and C.norm(v) not in {C.norm(x) for x in shapedata_nif_files})

tex_csv = os.path.join(C.OUT, "P02A_SHAPEDATA_TEXTURE_REWRITE.csv")
shapedata_texture_rows = 0
if os.path.isfile(tex_csv):
    with open(tex_csv, newline="", encoding="utf-8-sig") as fh:
        shapedata_texture_rows = sum(1 for _ in csv.DictReader(fh))


# ==========================================================================
# PART E -- summary
# ==========================================================================
def summary():
    sys.stdout.reconfigure(encoding="utf-8")
    W = 100
    print("=" * W)
    print("P02A.1-3 BodySlide OSP freeze + TRI morph separation + physics re-class")
    print("STRICT READ-ONLY. pack=%s plugin=%s canonical_body=%s female"
          % (C.PACK_ID, C.TARGET_PLUGIN, C.CANONICAL_BODY))
    print("=" * W)

    print("[A] BODYSLIDE_MIGRATION.csv")
    print("%-20s %5s %5s %5s %6s %9s %8s %8s %8s"
          % ("OUTFIT_ID", "rows", "sets", "orph", "coll", "new_osp", "ospOff", "outOff", "sdOff"))
    for oid in C.OUTFIT_IDS:
        rr = [r for r in rows if r["OUTFIT_ID"] == oid]
        print("%-20s %5d %5d %5d %6d %9s %8s %8s %8s"
              % (oid, len(rr),
                 sum(1 for r in rr if r["row_kind"] == "SLIDER_SET"),
                 sum(1 for r in rr if r["row_kind"] == "ORPHAN_SHAPEDATA"),
                 sum(1 for r in rr if r["collision_check"].startswith("COLLISION")),
                 len(osp_per_outfit[oid]),
                 sum(1 for r in rr if r["osp_off_namespace"] == "YES"),
                 sum(1 for r in rr if r["outputpath_off_namespace"] == "YES"),
                 sum(1 for r in rr if r["shapedata_off_namespace"] == "YES")))
    print("-" * W)
    print("rows=%d (slider sets=%d, orphan shapedata=%d)"
          % (len(rows),
             sum(1 for r in rows if r["row_kind"] == "SLIDER_SET"),
             sum(1 for r in rows if r["row_kind"] == "ORPHAN_SHAPEDATA")))
    print("FROZEN RULE one-OSP-per-outfit holds: %s   distinct new_osp total = %d"
          % (osp_rule_ok, len({r["new_osp"] for r in rows})))
    for oid in C.OUTFIT_IDS:
        s = sorted({r["new_osp"] for r in rows if r["OUTFIT_ID"] == oid})
        print("   %-20s slider_sets=%d -> %s" % (oid, osp_per_outfit and
              sum(1 for r in rows if r["OUTFIT_ID"] == oid
                  and r["row_kind"] == "SLIDER_SET"), s))
    print("relationship_basis: %s"
          % dict(collections.Counter(r["relationship_basis"] for r in rows)))
    print("OFF-NAMESPACE TOTALS  osp=%d  outputPath=%d  shapeData=%d"
          % (sum(1 for r in rows if r["osp_off_namespace"] == "YES"),
             sum(1 for r in rows if r["outputpath_off_namespace"] == "YES"),
             sum(1 for r in rows if r["shapedata_off_namespace"] == "YES")))
    print("collisions: %d"
          % sum(1 for r in rows if r["collision_check"].startswith("COLLISION")))
    bc = collections.Counter()
    for r in rows:
        for b in filter(None, r["blockers"].split(";")):
            bc[b] += 1
    print("blocker histogram: %s" % dict(bc))
    orphans = [r for r in rows if r["row_kind"] == "ORPHAN_SHAPEDATA"]
    print("orphan ShapeData rows (%d):" % len(orphans))
    for r in orphans:
        print("   %-20s %s" % (r["OUTFIT_ID"], r["old_shape_data"]))
    print("-" * W)

    print("[B] BODYSLIDE_MORPH_MIGRATION.csv")
    print("BODY_MORPH_TRI rows=%d over %d distinct .tri" % (len(morph_rows), len(morph_tris)))
    mc = collections.Counter(r["OUTFIT_ID"] for r in morph_rows)
    print("per outfit: %s" % dict(mc))
    print("status: %s" % dict(collections.Counter(r["status"] for r in morph_rows)))
    print("binding evidence: %s"
          % dict(collections.Counter(r["mesh_binding_evidence"] for r in morph_rows)))
    print("BODYTRI_reference_rewrite_required: %s"
          % dict(collections.Counter(r["BODYTRI_reference_rewrite_required"]
                                     for r in morph_rows)))
    for r in morph_rows:
        print("   %-20s %-52s -> %-52s set=%s"
              % (r["OUTFIT_ID"], os.path.basename(r["source_tri"]),
                 r["target_tri"].split("\\")[-1], r["associated_osp/set"]))
    print("-" * W)

    print("[C] PHYSICS_MIGRATION.csv")
    print("rows=%d over %d distinct configs" % (len(phys_rows),
                                                 len({r["config_file"] for r in phys_rows})))
    print("config_type: %s" % dict(collections.Counter(r["config_type"] for r in phys_rows)))
    print("config_format: %s" % dict(collections.Counter(r["config_format"] for r in phys_rows)))
    print("xml_root_element: %s"
          % dict(collections.Counter(r["xml_root_element"] for r in phys_rows)))
    print("HAS HAVOK_TRI IN PHYSICS TABLE: %s"
          % (any(r["config_file"].lower().endswith(".tri") for r in phys_rows)))
    print("per outfit: %s"
          % dict(collections.Counter(r["OUTFIT_ID"] for r in phys_rows)))
    for r in phys_rows:
        print("   %-20s %-58s %-22s %s"
              % (r["OUTFIT_ID"], os.path.basename(r["config_file"]),
                 r["config_type"], r["status"]))
    print("-" * W)

    print("[D] STRICT COUNTERS (audit item 6 - never mix these denominators)")
    print("  SHAPEDATA_NIF_FILES            = %d   (ALL distinct .nif under ShapeData"
          % len(shapedata_nif_files))
    print("                                       owned by the 11 outfits)")
    print("      of which in an OSP-declared data folder = %d" % len(shapedata_in_folders))
    print("      of which orphaned at the ShapeData root = %d  %s"
          % (len(shapedata_root_orphan),
             ",".join(os.path.basename(v) for v in shapedata_root_orphan)))
    print("  SHAPEDATA_TEXTURE_REWRITE_ROWS = %d   (shape x texture-slot rows, NOT NIFs)"
          % shapedata_texture_rows)
    print("  BODY_MORPH_TRI                 = %d   (distinct .tri body morph assets)"
          % len(morph_tris))
    print("  BODYSLIDE_OUTPUT_NIF           = %d   (distinct built meshes on disk)"
          % len(bodyslide_out_nifs))
    print("  GAME_NIF                       = %d   (distinct outfit meshes, not ShapeData,"
          " not a built output)" % len(game_nifs))
    print("  reconciliation: %d + %d + %d = %d distinct outfit-owned .nif vpaths"
          % (len(shapedata_nif_files), len(bodyslide_out_nifs), len(game_nifs),
             len(shapedata_nif_files) + len(bodyslide_out_nifs) + len(game_nifs)))
    print("=" * W)


if __name__ == "__main__":
    summary()
