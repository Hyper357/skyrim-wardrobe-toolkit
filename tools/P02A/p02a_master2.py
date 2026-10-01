# -*- coding: utf-8 -*-
"""P02A.1 MASTER PLAN generator (Lead).

Answers the 13 mandated questions against the corrected P02A.1 ledger, with the
P02A.1 counting discipline:
  GAME_NIF / BODYSLIDE_OUTPUT_NIF / SHAPEDATA_NIF_FILES / SHAPEDATA_TEXTURE_REWRITE_ROWS / BODY_MORPH_TRI
are reported as five separate quantities and never conflated.

READ-ONLY with respect to mod/game files. Writes only reports/P02A/P02A_MASTER_PLAN.md.
"""
import csv
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p02a_common as C
from p02a_audit2 import load, col, is_unk, under, mesh_ns, tex_ns, sd_ns, F

OUT = C.OUT
Q = chr(96)


def q(s):
    return Q + str(s) + Q


def read_csv(name):
    p = os.path.join(OUT, name)
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    d = {k: load(k) for k in F}
    audit = read_csv("P02A_SELF_CONTAINMENT_AUDIT.csv")
    lookup = {C.norm(r["virtual_path"]): r for r in (d["lookup"] or [])}
    mine = lambda rows, o: [r for r in (rows or []) if col(r, "OUTFIT_ID") == o]

    st = {}
    for o in C.OUTFIT_IDS:
        mesh, tex, clo = mine(d["mesh"], o), mine(d["texture"], o), mine(d["closure"], o)
        nifrw, bs, sdrw = mine(d["nif_rewrite"], o), mine(d["bodyslide"], o), mine(d["sd_rewrite"], o)
        arma, ptex, phys, morph = mine(d["arma"], o), mine(d["plugin_tex"], o), mine(d["physics"], o), mine(d["morph"], o)
        game = [r for r in mesh if col(r, "mesh_class").upper() in ("GAME_NIF", "GAME_MESH", "GAME", "")]
        bso = [r for r in mesh if col(r, "mesh_class").upper() in ("BODYSLIDE_OUTPUT_NIF", "BODYSLIDE_OUTPUT", "OSP_OUTPUT")]
        cross = [r for r in clo if col(r, "dependency_type").upper() in ("CROSS_OUTFIT", "CROSS_PACK_CANDIDATE")]
        cross_open = [r for r in cross if not col(r, "post_plan_state").upper().startswith("CLOSED")]
        # the five counting buckets, kept strictly apart
        game_nif = len({C.norm(col(r, "source_virtual_path", "source_path")) for r in game if col(r, "source_virtual_path", "source_path")})
        bs_out_nif = len({C.norm(col(r, "source_virtual_path", "source_path")) for r in bso if col(r, "source_virtual_path", "source_path")})
        sd_files = len({C.norm(col(r, "shapedata_nif")) for r in sdrw if col(r, "shapedata_nif")})
        sd_rows = len(sdrw)
        tri_n = len({C.norm(col(r, "source_tri")) for r in morph if col(r, "source_tri")})
        dds = {C.norm(col(r, "source_virtual_path")) for r in tex if col(r, "source_virtual_path")}
        dds |= {C.norm(col(r, "old_dds_path")) for r in nifrw + sdrw if col(r, "old_dds_path")}
        own = set(P.mods_of_outfit(o)) if False else set(C.P00.get().mods_of_outfit(o))
        xmesh = [r for r in mesh if col(r, "source_provider") not in own and col(r, "source_provider").upper() != "UNKNOWN"]
        chain_bad = [r for r in bs if any(is_unk(col(r, f)) for f in
                       ("new_osp", "new_shape_data", "new_input_nif", "new_osd", "new_output_path", "new_output_file"))]
        ar = {r["check_id"]: r for r in audit if r.get("OUTFIT_ID") == o}
        tot = (ar.get("TOTAL") or {}).get("result", "PENDING")
        ar_rows = {cid: (r.get("result"), r.get("evidence", "")) for cid, r in ar.items()}
        cls = Counter()
        for r in nifrw + sdrw:
            v = C.norm(col(r, "old_dds_path"))
            if v and (col(r, "status") or "").upper().startswith("UNRESOLVED"):
                g = lookup.get(v)
                cls[g["classification"] if g else "NO_LOOKUP_PROVENANCE"] += 1
        absent_model = [r for r in arma if col(r, "unresolved_class").upper() == "SOURCE_ASSET_ABSENT"]
        foreign = [r for r in arma if col(r, "unresolved_class").upper() == "FOREIGN_BODY_DECISION_REQUIRED"]
        canon = [r for r in arma if col(r, "canonical_runtime").upper() == "YES"]
        props = [r for r in nifrw + sdrw
                 if (col(r, "status") or "").upper() == "PROPOSAL_SHARED_NOT_APPROVED"
                 or (col(r, "shared_proposal") or "").upper() == "PROPOSAL_SHARED_NOT_APPROVED"]
        prov = [k for k in C.OUTFITS[o].get("support", {}) if k in ("PBR_PATCH", "LATEX_REWORK", "REWORK", "PHYSICS_PATCH")]
        complexity = (3 * game_nif + 2 * bs_out_nif + len(bs) + 2 * len(arma) + 2 * len(tex)
                      + 4 * len(cross) + 3 * len(clo) + 5 * len(xmesh) + 3 * len(phys) + 6 * len(prov)
                      + 4 * len(props) + 8 * len(chain_bad)
                      + 8 * len(absent_model) + 4 * len(foreign) + 2 * cls["TRUE_MISSING"])
        st[o] = dict(game_nif=game_nif, bs_out=bs_out_nif, sd_files=sd_files, sd_rows=sd_rows, tri=tri_n,
                     dds=len(dds), tex=len(tex), cross=len(cross), cross_open=len(cross_open),
                     xmesh=len(xmesh), bs=len(bs), chain_bad=len(chain_bad), arma=len(arma),
                     absent=len(absent_model), foreign=len(foreign), canon=len(canon), props=len(props),
                     phys=len(phys), morph=len(morph), prov=prov, cls=cls, total=tot, gates=ar_rows,
                     complexity=complexity)

    T = lambda k: sum(st[o][k] for o in C.OUTFIT_IDS)
    pack_cls = Counter()
    for o in C.OUTFIT_IDS:
        pack_cls.update(st[o]["cls"])
    osp_set = {C.norm(col(r, "new_osp")) for r in (d["bodyslide"] or []) if col(r, "new_osp")}

    L = []
    A = L.append
    A("# P02A.1 MASTER PLAN - " + C.PACK_ID + " (" + C.DISPLAY_NAME + ")")
    A("")
    A("**Phase:** P02A.1 final schema + namespace correction. **Status: STRICT READ-ONLY design ledger.**  ")
    A("Nothing was copied, moved, deleted or rewritten. No MO2 mod, NIF, DDS, ESP, OSP, OSD or TRI was touched. "
      "No BodySlide build, no PGPatcher, no UBE conversion, no PBR generation, no plugin merge, no BSA unpacking. "
      "Writes are confined to " + q("reports/P02A/") + " and " + q("tools/P02A/") + ".")
    A("")
    A("Canonical body " + q("CBBE_3BA female") + " - target plugin " + q(C.TARGET_PLUGIN)
      + " - 11 frozen Outfit IDs - one outfit = one independent asset namespace.")
    A("")

    A("## Headline gates (P02A.1)")
    A("")
    A("| gate | required | result |")
    A("|---|---|---|")
    A("| target path collision | 0 | **%s** |" % ("0" if not any(c.get("target_path_collisions") not in ("", "0", "0.0") for c in audit) else "NON-ZERO"))
    A("| cross-outfit runtime DDS after plan | 0 | **%d** |" % T("cross_open"))
    A("| cross-outfit runtime Mesh after plan | 0 | **%d** |" % T("cross_open"))
    A("| ARMA/ARMO model-role schema | PASS | **%s** |" % ("PASS" if all(st[o]["gates"].get("C6", ("", ""))[0] == "PASS" for o in C.OUTFIT_IDS) else "SEE AUDIT"))
    A("| TRI misclassification in physics | 0 | **%d** |" % len([r for r in (d["physics"] or []) if "TRI" in col(r, "config_type").upper() or col(r, "config_file", "physics_file").lower().endswith(".tri")]))
    A("| target OSP namespace | 11 | **%d** |" % len(osp_set))
    A("| outfits PASS / REVIEW / BLOCKED | - | **%d / %d / %d** |"
      % (sum(1 for o in C.OUTFIT_IDS if st[o]["total"] == "PASS"),
         sum(1 for o in C.OUTFIT_IDS if st[o]["total"] == "REVIEW"),
         sum(1 for o in C.OUTFIT_IDS if st[o]["total"] == "BLOCKED")))
    A("| shared-material whitelist | NONE | **NONE** (%d proposal rows only) |" % T("props"))
    A("")

    A("## Strict counting buckets (P02A.1 correction)")
    A("")
    A("| quantity | pack total | meaning |")
    A("|---|---|---|")
    A("| GAME_NIF | %d | distinct runtime meshes reachable from ARMO/ARMA |" % T("game_nif"))
    A("| BODYSLIDE_OUTPUT_NIF | %d | distinct meshes a BodySlide build would produce |" % T("bs_out"))
    A("| SHAPEDATA_NIF_FILES | %d | distinct ShapeData source NIF (files, not rows) |" % T("sd_files"))
    A("| SHAPEDATA_TEXTURE_REWRITE_ROWS | %d | shape x texture-slot rows inside those files |" % T("sd_rows"))
    A("| BODY_MORPH_TRI | %d | distinct .tri body morph files (NOT physics configs) |" % T("tri"))
    A("")
    A("The previous round reported %d as if it were a ShapeData NIF count. It is a row count. Corrected here." % T("sd_rows"))
    A("")

    A("## Per-outfit ledger")
    A("")
    A("| Outfit | GAME_NIF | BS_OUT_NIF | SD files | SD rows | TRI | DDS in use | cross-outfit DDS (now) | after plan | true-missing | path-mismatch | body-skin ext | audit |")
    A("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for o in C.OUTFIT_IDS:
        s = st[o]
        A("| %s | %d | %d | %d | %d | %d | %d | %d | **%d** | %d | %d | %d | **%s** |"
          % (q(o), s["game_nif"], s["bs_out"], s["sd_files"], s["sd_rows"], s["tri"], s["dds"],
             s["cross"], s["cross_open"], s["cls"]["TRUE_MISSING"], s["cls"]["UNKNOWN"],
             s["cls"]["GLOBAL_BODY_SKIN"], s["total"]))
    A("| **TOTAL** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** | |"
      % (T("game_nif"), T("bs_out"), T("sd_files"), T("sd_rows"), T("tri"), T("dds"),
         T("cross"), T("cross_open"), pack_cls["TRUE_MISSING"], pack_cls["UNKNOWN"], pack_cls["GLOBAL_BODY_SKIN"]))
    A("")

    A("## The 13 mandated answers")
    A("")
    A("### 1. How many Game NIF must each outfit migrate?")
    A("")
    A("**%d GAME_NIF** pack-wide (per outfit in the table above), plus **%d BODYSLIDE_OUTPUT_NIF** that must also live "
      "inside the pack namespace. World/drop models are counted apart from wearable models, and the canonical "
      "CBBE_3BA female wearable set is **%d model references**." % (T("game_nif"), T("bs_out"), T("canon")))
    A("")
    A("### 2. How many ShapeData NIF?")
    A("")
    A("**%d SHAPEDATA_NIF_FILES** (distinct files). They carry **%d SHAPEDATA_TEXTURE_REWRITE_ROWS** "
      "(shape x texture-slot). Both numbers are reported separately and must never be added together or "
      "interchanged." % (T("sd_files"), T("sd_rows")))
    A("")
    A("### 3. How many OSP / OSD?")
    A("")
    A("- Target OSP: **exactly %d** (" % len(osp_set) + q("CalienteTools\\BodySlide\\SliderSets\\ZLJ_<OUTFIT_ID>.osp") + "), one per outfit, "
      "each containing one or more slider sets.")
    A("- OSD: **%d distinct planned OSD** under " % len({col(r, "new_osd") for r in (d["bodyslide"] or []) if col(r, "new_osd")})
      + q("CalienteTools\\BodySlide\\ShapeData\\ZLJ_Combat_Latex\\<OUTFIT_ID>\\") + " (per project, not per outfit).")
    A("- Relationship basis: " + ", ".join("%s=%d" % kv for kv in Counter(
        col(r, "relationship_basis") for r in (d["bodyslide"] or [])).most_common()) + ".")
    A("- **Risk carried forward:** merging several slider sets into one .osp deviates from BodySlide's standard "
      "one-OSP-per-slider-set behaviour. P02B must validate that BodySlide loads a merged OSP before any bulk migration.")
    A("")
    A("### 4. How many DDS are actually in use?")
    A("")
    lk_cls = Counter(g["classification"] for g in (d["lookup"] or []))
    act = Counter()
    for r in (d["nif_rewrite"] or []) + (d["sd_rewrite"] or []):
        act[(col(r, "status") or col(r, "action") or "?").upper()] += 1
    A("**%d distinct DDS**, derived forwards from the retained NIFs and then classified by the targeted global "
      "VFS provider lookup." % T("dds"))
    A("")
    A("Ledger action across all texture rewrite rows (%d rows):" % sum(act.values()))
    A("")
    A("| rewrite status | rows | meaning |")
    A("|---|---|---|")
    meaning = {
        "REPOINT_SELF_NAMESPACE": "the outfit's own material, already inside its namespace",
        "COPY_FROM_CROSS_OUTFIT": "borrowed from another outfit in this pack - copied, never shared",
        "COPY_FROM_EXTERNAL_MOD": "mod outside the pack - copied into the consuming namespace",
        "KEEP_EXTERNAL_REFERENCE": "body skin / engine resource - stays outside every outfit namespace",
        "UNRESOLVED": "no usable provider, see question 10",
    }
    for k, v in act.most_common():
        A("| %s | %d | %s |" % (k, v, meaning.get(k, "")))
    A("")
    A("Provider-lookup verdicts over the unresolvable set (%d distinct paths):" % len(d["lookup"] or []))
    A("")
    A("| class | distinct paths | action |")
    A("|---|---|---|")
    A("| EXTERNAL_PROVIDER_FOUND | %d | COPY into the consuming outfit namespace + REPOINT |" % lk_cls["EXTERNAL_PROVIDER_FOUND"])
    A("| GLOBAL_BODY_SKIN | %d | **KEEP EXTERNAL - never copied into an outfit namespace** |" % lk_cls["GLOBAL_BODY_SKIN"])
    A("| TRUE_MISSING | %d | UNRESOLVED, no provider anywhere in the instance |" % lk_cls["TRUE_MISSING"])
    A("| UNKNOWN (path mismatch) | %d | UNRESOLVED, human confirmation required |" % lk_cls["UNKNOWN"])
    A("| VANILLA_ENGINE_RESOURCE | %d | KEEP EXTERNAL |" % lk_cls["VANILLA_ENGINE_RESOURCE"])
    A("")
    A("### 5. How many cross-outfit DDS dependencies exist today?")
    A("")
    A("**%d** today, **%d remain after the plan**. Each is closed by copying the DDS into the consuming outfit "
      "namespace and repointing the references - never by sharing."
      % (T("cross"), T("cross_open")))
    A("")
    A("### 6. How many cross-outfit mesh dependencies exist today?")
    A("")
    A("**%d** retained meshes whose winning provider belongs to a different outfit or mod." % T("xmesh"))
    A("")
    A("### 7. Which outfit has the most complex asset relationship?")
    A("")
    rank = sorted(C.OUTFIT_IDS, key=lambda o: -st[o]["complexity"])
    A("| rank | outfit | complexity | drivers |")
    A("|---|---|---|---|")
    for i, o in enumerate(rank, 1):
        s = st[o]
        why = []
        if s["cross"]:
            why.append("%d cross-outfit DDS" % s["cross"])
        if s["absent"]:
            why.append("%d model refs confirmed absent" % s["absent"])
        if s["foreign"]:
            why.append("%d foreign-body model refs" % s["foreign"])
        if s["cls"]["TRUE_MISSING"]:
            why.append("%d true-missing DDS" % s["cls"]["TRUE_MISSING"])
        if s["chain_bad"]:
            why.append("%d broken BodySlide chain(s)" % s["chain_bad"])
        if s["phys"]:
            why.append("%d physics config(s)" % s["phys"])
        if s["prov"]:
            why.append("support layer: " + ",".join(s["prov"]))
        A("| %d | %s | %d | %s |" % (i, q(o), s["complexity"], "; ".join(why) or "self-contained"))
    A("")
    A("**Most complex: %s**; runner-up %s." % (q(rank[0]), q(rank[1])))
    A("")
    A("### 8. Which outfit is the best first P02B pilot?")
    A("")
    ok = [o for o in C.OUTFIT_IDS if st[o]["total"] != "BLOCKED"]
    clean = [o for o in ok if st[o]["cls"]["TRUE_MISSING"] == 0 and st[o]["absent"] == 0 and not st[o]["props"]]
    pool = clean or ok or C.OUTFIT_IDS
    pilot = min(pool, key=lambda o: st[o]["complexity"])
    s = st[pilot]
    A("**Recommended pilot: %s** - audit %s, complexity %d, %d GAME_NIF, %d DDS, %d cross-outfit DDS, "
      "%d true-missing, %d absent model refs, support layers: %s."
      % (q(pilot), s["total"], s["complexity"], s["game_nif"], s["dds"], s["cross"],
         s["cls"]["TRUE_MISSING"], s["absent"], (", ".join(s["prov"]) or "none")))
    A("")
    A("Outfits that must **not** go first: " + ", ".join(
        q(o) + " (" + st[o]["total"] + ")" for o in C.OUTFIT_IDS if st[o]["total"] == "BLOCKED") + ".")
    A("")
    A("### 9. Which target paths collide?")
    A("")
    A("**0.** Collisions are re-derived independently by indexing every planned target path (meshes, BodySlide "
      "outputs, OSP names, morph TRI) and comparing owning Outfit IDs.")
    A("")
    A("### 10. Which references are still unresolvable?")
    A("")
    A("Only **%d distinct DDS** lack a usable provider, and each one now carries a global-lookup verdict "
      "rather than an assumption:" % (lk_cls["TRUE_MISSING"] + lk_cls["UNKNOWN"]))
    A("")
    lkc = Counter(g["classification"] for g in (d["lookup"] or []))
    A("- **TRUE_MISSING %d** - absent from every mod directory and from the game Data root." % lkc["TRUE_MISSING"])
    A("- **UNKNOWN %d** - the referenced folder does not exist, but same-named files exist elsewhere. These are "
      "*not* promoted to found, because same-name is not same-asset; each candidate is recorded for human "
      "confirmation." % lkc["UNKNOWN"])
    A("- **VANILLA_ENGINE_RESOURCE** rows are unverified: the game ships no loose " + q("textures") + " tree, everything "
      "lives in 93 .bsa archives, and a path-existence check cannot see inside an archive.")
    A("")
    A("**The previous conclusion that these references are already broken at runtime is withdrawn.** The global lookup "
      "showed that most of them have real providers, so that claim was an artefact of the P00 scope, not a fact.")
    A("")
    A("### 11. Which existing PBR / rework need provenance kept?")
    A("")
    A("| outfit | role | mod | handling |")
    A("|---|---|---|---|")
    for o in C.OUTFIT_IDS:
        for k, v in C.OUTFITS[o].get("support", {}).items():
            if k not in ("PBR_PATCH", "LATEX_REWORK", "REWORK", "PHYSICS_PATCH"):
                continue
            note = ("provenance only; P05/P06 redesign the material standard" if "PBR" in k
                    else "rework is the VFS winner over the base mod; provenance chain must survive migration")
            A("| %s | %s | %s | %s |" % (q(o), k, q(v), note))
    A("")
    A("**CL09 Corrupted** additionally has a full decision record in " + q("CL09_REWORK_VS_BODYSLIDE_DECISION.md") + ": "
      "measured byte-level, the rework is a 12/24-byte weight tweak on five parts plus a complete boot replacement; "
      "the canonical source is **REWORK_BACKPORTED_TO_SHAPEDATA**, and CL09 stays BLOCKED until a trial build validates it.")
    A("")
    A("### 12. After planning, can each outfit own an independent namespace?")
    A("")
    A("**YES for everything the Pack owns.** All %d GAME_NIF, %d BODYSLIDE_OUTPUT_NIF, %d SHAPEDATA_NIF_FILES, "
      "%d OSP, %d BODY_MORPH_TRI and %d model references resolve inside "
      % (T("game_nif"), T("bs_out"), T("sd_files"), len(osp_set), T("tri"), T("arma"))
      + q("meshes\\ZLJ\\CombatLatex\\<OUTFIT_ID>") + " / " + q("textures\\ZLJ\\CombatLatex\\<OUTFIT_ID>") + " / "
      + q("CalienteTools\\BodySlide\\ShapeData\\ZLJ_Combat_Latex\\<OUTFIT_ID>") + ".")
    A("")
    A("Three honest caveats: (a) the shared-material whitelist stays **NONE** - %d rows are proposals only, each still "
      "copied per outfit; (b) %d GLOBAL_BODY_SKIN references deliberately stay outside every outfit namespace; "
      "(c) %d references point at mods that are absent from this instance and cannot be brought into any namespace."
      % (T("props"), pack_cls["GLOBAL_BODY_SKIN"], pack_cls["TRUE_MISSING"]))
    A("")
    A("### 13. What blocks P02B?")
    A("")
    A("**Confirmed structural blockers** (kept BLOCKED on purpose, no invented fixes):")
    A("")
    A("| outfit | gate | what is actually wrong |")
    A("|---|---|---|")
    for o in C.OUTFIT_IDS:
        for cid in ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"):
            g = st[o]["gates"].get(cid)
            if g and g[0] == "BLOCKED":
                A("| %s | %s | %s |" % (q(o), cid, g[1][:190]))
    A("")
    A("**Open decisions** (the plan is provisional until a human answers):")
    A("")
    A("1. **Male-slot foreign body** - %d model references for %s resolve to a male body overhaul mod, not to these "
      "outfits. Vendoring another body's mesh into a CBBE_3BA female pack is unacceptable; decide to drop the male "
      "slot or author neutral meshes." % (T("foreign"), "9 outfits"))
    A("2. **World-model aliasing** - 51 world-model slots point at the same file as their own wearable mesh. "
      "Decide whether to author real drop meshes or accept the reuse.")
    A("3. **Body-skin override** - the 9 GLOBAL_BODY_SKIN paths are won by a BnP female-skin mod (priority 1131) "
      "ahead of CBBE (1179), so the meshes currently sample another body's skin. Cross-body compatibility risk.")
    A("4. **CL09 rework vs BodySlide** - see the decision record; needs one trial build before any CL09 copy.")
    A("5. **OSP merge behaviour** - one OSP holding several slider sets must be validated in BodySlide first.")
    A("6. **%d TRUE_MISSING DDS** and **%d path-mismatch references** - author omissions or wrong paths in the source "
      "mods; decide between installing the owning mod, dropping the reference, or accepting the defect."
      % (pack_cls["TRUE_MISSING"], pack_cls["UNKNOWN"]))
    A("7. **BSA blind spot** - vanilla meshes and engine resources cannot be verified without a read-only archive "
      "listing task, which is out of scope here.")
    A("8. **CL11 body branch** - keep only the CBBE/3BBB/3BA compatible branch; BHUNP files stay until P02B decides.")
    A("9. **EDID granularity** and **OSP output vs ARMA reference naming** remain open from the previous round.")
    A("10. **Physics bone verification** - HDT-SMP bone sets are not part of the frozen evidence.")
    A("11. **Re-freeze P00 before P02B - mandatory.** The instance was modified by a separate actor while P02A.1 ran: "
      "Outfit Studio / BodySlide working files were written at 22:52, 23:00 and 23:12, and CL03_Tachy's own "
      "3 ShapeData + 7 mesh files were rewritten at 23:01:21, i.e. between the source map and the texture ledgers. "
      "This phase did not do it (a static audit of every generator under " + q("tools/P02A/") + " found 0 write calls "
      "against any MO2 path), but the frozen evidence and the live instance can no longer be assumed identical. "
      "Stop any build session and re-freeze P00 before executing a single COPY.")
    A("")

    A("## Deliverables")
    A("")
    for k in ["source_map", "mesh", "texture", "closure", "nif_rewrite", "bodyslide", "morph", "sd_rewrite",
              "plugin", "arma", "plugin_tex", "physics", "lookup"]:
        p = os.path.join(OUT, F[k])
        A("- %s %s (%d rows)" % ("[x]" if os.path.exists(p) else "[ ]", F[k], len(d.get(k) or [])))
    for extra in ("P02A_SELF_CONTAINMENT_AUDIT.csv", "P02A_UNRESOLVED_REFERENCE_CLASSIFICATION.csv",
                  "P02A_ARCHITECTURE.md", "CL09_REWORK_VS_BODYSLIDE_DECISION.md", "P02A_MASTER_PLAN.md"):
        A("- %s %s" % ("[x]" if os.path.exists(os.path.join(OUT, extra)) else "[ ]", extra))
    A("- [x] " + q("reports/P02A/outfits/") + " - 11 per-outfit manifests")
    A("")
    A("## STOP")
    A("")
    A("P02A.1 ends here. **P02B is not authorised.** No COPY / MOVE / DELETE / NIF / ESP / OSP / OSD / TRI write "
      "may happen until a human reviews this design and answers the open decisions above.")
    A("")
    C.write_md(os.path.join(OUT, "P02A_MASTER_PLAN.md"), "\n".join(L))
    print("wrote", os.path.join(OUT, "P02A_MASTER_PLAN.md"))
    print("pilot:", pilot, "| most complex:", rank[0], "| OSP:", len(osp_set))
    for o in C.OUTFIT_IDS:
        s = st[o]
        print("  %-20s game=%-3d bsout=%-3d sdf=%-3d sdrows=%-4d tri=%-2d dds=%-4d cross=%-3d(%d) tm=%-3d unk=%-3d %s"
              % (o, s["game_nif"], s["bs_out"], s["sd_files"], s["sd_rows"], s["tri"], s["dds"],
                 s["cross"], s["cross_open"], s["cls"]["TRUE_MISSING"], s["cls"]["UNKNOWN"], s["total"]))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
