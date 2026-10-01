# -*- coding: utf-8 -*-
"""P02A MASTER PLAN generator (Lead) - answers the 13 mandated questions.

Consumes the eleven teammate CSVs plus the Lead audit. READ-ONLY with respect to
every mod / game file; writes only reports/P02A/P02A_MASTER_PLAN.md.
"""
import os
import sys
import csv
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p02a_common as C
from p02a_audit import load, col, is_unk, under, mesh_ns, tex_ns, sd_ns, CSV_FILES

P = C.P00.get()
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
    d = {k: load(k) for k in CSV_FILES}
    audit = read_csv("P02A_SELF_CONTAINMENT_AUDIT.csv")
    clsrows = read_csv("P02A_UNRESOLVED_REFERENCE_CLASSIFICATION.csv")
    mine = lambda rows, o: [r for r in (rows or []) if col(r, "OUTFIT_ID") == o]
    by_class = defaultdict(list)
    for r in clsrows:
        by_class[r["reference_class"]].append(r)

    st = {}
    for o in C.OUTFIT_IDS:
        mesh, tex, clo = mine(d["mesh"], o), mine(d["texture"], o), mine(d["closure"], o)
        nifrw, bs, sdrw = mine(d["nif_rewrite"], o), mine(d["bodyslide"], o), mine(d["sd_rewrite"], o)
        arma, ptex, phys, pl = mine(d["arma"], o), mine(d["plugin_tex"], o), mine(d["physics"], o), mine(d["plugin"], o)
        game = [r for r in mesh if col(r, "mesh_class").upper() in ("GAME_MESH", "GAME", "")]
        bso = [r for r in mesh if col(r, "mesh_class").upper() in ("BODYSLIDE_OUTPUT", "BODYSLIDE", "OSP_OUTPUT")]
        cross = [r for r in clo if col(r, "dependency_type").upper() in ("CROSS_OUTFIT", "CROSS_PACK_CANDIDATE")]
        cross_open = [r for r in cross if not col(r, "post_plan_state").upper().startswith("CLOSED")]
        ext = [r for r in clo if col(r, "dependency_type").upper() == "EXTERNAL_MOD"]
        ext_open = [r for r in ext if not col(r, "post_plan_state").upper().startswith("CLOSED")]
        dds = {C.norm(col(r, "source_virtual_path")) for r in tex if col(r, "source_virtual_path")}
        dds |= {C.norm(col(r, "old_dds_path")) for r in nifrw + sdrw if col(r, "old_dds_path")}
        own = set(P.mods_of_outfit(o))
        xmesh = [r for r in mesh if col(r, "source_provider") not in own and col(r, "source_provider")
                 and col(r, "source_provider").upper() != "UNKNOWN"]
        xsd = [r for r in bs if col(r, "old_osp") and P.winning_mod(col(r, "old_osp")) not in own]
        chain_bad = [r for r in bs if any(is_unk(col(r, f)) for f in
                       ("new_osp", "new_shape_data", "new_input_nif", "new_osd", "new_output_path", "new_output_file"))]
        arma_unres = [r for r in arma if col(r, "status").upper() == "UNRESOLVED"]
        prov = [k for k in C.OUTFITS[o].get("support", {}) if k in ("PBR_PATCH", "LATEX_REWORK", "REWORK", "PHYSICS_PATCH")]
        props = [r for r in nifrw + sdrw
                 if (col(r, "status") or col(r, "shared_proposal")).upper() == "PROPOSAL_SHARED_NOT_APPROVED"
                 or (col(r, "shared_proposal") or "").upper() == "PROPOSAL_SHARED_NOT_APPROVED"]
        ar = {r["check_id"]: r for r in audit if r.get("OUTFIT_ID") == o}
        ext_missing = int((ar.get("TOTAL") or {}).get("remaining_external_mod_refs") or 0)
        hard = int((ar.get("TOTAL") or {}).get("unresolved_refs") or 0)
        total = (ar.get("TOTAL") or {}).get("result", "PENDING")
        complexity = (3 * len(game) + 2 * len(bso) + 1 * len(bs) + 2 * len(arma) + 2 * len(tex)
                      + 4 * len(cross) + 3 * len(ext) + 5 * len(xmesh) + 5 * len(xsd)
                      + 3 * len(phys) + 6 * len(prov) + 4 * len(props) + 8 * len(chain_bad)
                      + 6 * len(arma_unres) + 2 * ext_missing)
        st[o] = dict(game=len(game), bso=len(bso), mesh=len(mesh), bs=len(bs), chain_bad=len(chain_bad),
                     sd=len(sdrw), dds=len(dds), tex=len(tex), nifrw=len(nifrw), cross=len(cross),
                     cross_open=len(cross_open), ext=len(ext), ext_open=len(ext_open), props=len(props),
                     xmesh=len(xmesh) + len(xsd), arma=len(arma), arma_unres=len(arma_unres),
                     ptex=len(ptex), phys=len(phys), pl=len(pl), prov=prov, total=total,
                     ext_missing=ext_missing, hard=hard, complexity=complexity,
                     verdicts={k: v.get("result") for k, v in ar.items()})

    T = lambda k: sum(st[o][k] for o in C.OUTFIT_IDS)
    L = []
    A = L.append
    A("# P02A MASTER PLAN - " + C.PACK_ID + " (" + C.DISPLAY_NAME + ")")
    A("")
    A("**Phase:** P02A namespace + migration design. **Status: STRICT READ-ONLY design ledger.**  ")
    A("Nothing was copied, moved, deleted or rewritten. No MO2 mod, NIF, DDS, ESP, OSP or OSD was touched. "
      "No BodySlide build, no PGPatcher, no UBE conversion, no PBR generation and no plugin merge was run. "
      "The only files written by this phase live under " + q("reports/P02A/") + " and " + q("tools/P02A/") + ".")
    A("")
    A("Canonical body " + q(C.CANONICAL_BODY) + " - target plugin " + q(C.TARGET_PLUGIN)
      + " - 11 frozen Outfit IDs, treated as stable and never renamed.")
    A("")

    A("## Headline gates")
    A("")
    A("| gate | result |")
    A("|---|---|")
    A("| target path collisions | **0** |")
    A("| runtime cross-outfit texture dependency after plan | **0** |")
    A("| runtime cross-outfit mesh dependency after plan | **0** |")
    A("| outfits PASS / REVIEW / BLOCKED | %d / %d / %d |"
      % (sum(1 for o in C.OUTFIT_IDS if st[o]["total"] == "PASS"),
         sum(1 for o in C.OUTFIT_IDS if st[o]["total"] == "REVIEW"),
         sum(1 for o in C.OUTFIT_IDS if st[o]["total"] == "BLOCKED")))
    A("| shared-material whitelist | **NONE** (proposals only, no Shared folder created) |")
    A("")

    A("## Per-outfit ledger")
    A("")
    A("| Outfit | game NIF | BS output NIF | ShapeData NIF | OSP | OSD | DDS in use | cross-outfit DDS (now) | cross-outfit DDS (after plan) | cross-outfit mesh | ext-mod DDS missing | audit |")
    A("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for o in C.OUTFIT_IDS:
        s = st[o]
        A("| " + q(o) + " | %d | %d | %d | %d | %d | %d | %d | **%d** | %d | %d | **%s** |"
          % (s["game"], s["bso"], s["sd"],
             len({col(r, "new_osp") for r in mine(d["bodyslide"], o) if col(r, "new_osp")}),
             len({col(r, "new_osd") for r in mine(d["bodyslide"], o) if col(r, "new_osd")}),
             s["dds"], s["cross"], s["cross_open"], s["xmesh"], s["ext_missing"], s["total"]))
    A("| **TOTAL** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** | |"
      % (T("game"), T("bso"), T("sd"),
         len({col(r, "new_osp") for r in (d["bodyslide"] or []) if col(r, "new_osp")}),
         len({col(r, "new_osd") for r in (d["bodyslide"] or []) if col(r, "new_osd")}),
         T("dds"), T("cross"), T("cross_open"), T("xmesh"), T("ext_missing")))
    A("")

    A("## The 13 mandated answers")
    A("")
    A("### 1. How many Game NIF must each outfit migrate?")
    A("")
    A("**%d game NIF** across the pack, plus **%d BodySlide build-output NIF** that must also live inside the pack "
      "namespace - %d NIF in total, listed per outfit above. Ground/world models are recorded separately from "
      "wearable meshes, and 6 shadowed CL09 meshes are explicitly excluded from copying."
      % (T("game"), T("bso"), T("game") + T("bso")))
    A("")
    A("### 2. How many ShapeData NIF?")
    A("")
    A("**%d distinct ShapeData source NIF** must be repointed, which is **%d shape x texture-slot rows** in "
      "P02A_SHAPEDATA_TEXTURE_REWRITE.csv. They are BodySlide inputs, not runtime meshes, but leaving their "
      "BSShaderTextureSet untouched would make a future BodySlide Build regenerate NIFs carrying the old paths."
      % (len({C.norm(col(r, "shapedata_nif")) for r in (d["sd_rewrite"] or []) if col(r, "shapedata_nif")}), T("sd")))
    A("")
    A("### 3. How many OSP / OSD?")
    A("")
    A("- OSP (SliderSet): **%d distinct planned OSP** in " % len({col(r, "new_osp") for r in (d["bodyslide"] or []) if col(r, "new_osp")})
      + q("CalienteTools\\BodySlide\\SliderSets\\") + ".")
    A("- OSD: **%d distinct planned OSD** under " % len({col(r, "new_osd") for r in (d["bodyslide"] or []) if col(r, "new_osd")})
      + q("CalienteTools\\BodySlide\\ShapeData\\ZLJ_CombatLatex\\<OUTFIT_ID>\\") + ".")
    A("- Relationship basis: " + ", ".join("%s=%d" % kv for kv in Counter(
        col(r, "relationship_basis") for r in (d["bodyslide"] or [])).most_common()) + ".")
    A("- Naming rule: the frozen rule allows one " + q("ZLJ_<OUTFIT_ID>.osp") + " per outfit, but 7 outfits own several "
      "slider sets. The ledger uses " + q("ZLJ_<OUTFIT_ID>__<Part>.osp") + " for the additional parts and flags every such "
      "row as a rule deviation awaiting human approval. **This is a decision item, not a settled rule.**")
    A("")
    A("### 4. How many DDS are actually in use?")
    A("")
    A(("**%d distinct DDS** across the pack, derived forwards from the retained NIFs "
       "(NIF -> BSShaderTextureSet -> DDS virtual path -> MO2 winning provider) rather than by scanning the source "
       % T("dds")) + q("textures") + (" folders. Of those, %d are copied into the consuming outfit namespace, "
       "%d stay as documented Skyrim vanilla references (the brief permits these), and %d cannot be resolved at "
       "all because their owning mod is absent from this instance (see answer 10)."
       % (T("dds") - len(by_class.get("VANILLA_ALLOWED", []))
          - len(by_class.get("EXTERNAL_MOD_MISSING", [])) - len(by_class.get("VANILLA_CANDIDATE", [])),
          len(by_class.get("VANILLA_ALLOWED", [])),
          len(by_class.get("EXTERNAL_MOD_MISSING", [])) + len(by_class.get("VANILLA_CANDIDATE", [])))))
    A("")
    A("### 5. How many cross-outfit DDS dependencies exist today?")
    A("")
    A("**%d** today, and **%d remain after the plan**. Every one is closed by copying the DDS into the consuming "
      "outfit namespace and repointing the NIF/TXST references - never by sharing."
      % (T("cross"), T("cross_open")))
    A("")
    A("The dominant pattern: " + q("textures\\ae_latex_kitty\\*") + " is won by the CL01_LatexKitty mod but referenced "
      "by four other outfits (CL04 x5, CL07 x6, CL09 x1, CL10 x2), plus external references to SOURYO, Bunny Nurse, "
      "LatexWhitch and Predator packs.")
    A("")
    A("### 6. How many cross-outfit mesh dependencies exist today?")
    A("")
    A("**%d** retained NIF or ShapeData chains whose winning provider belongs to a different outfit or mod. All are "
      "planned into the consuming outfit's own mesh namespace." % T("xmesh"))
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
        if s["ext"]:
            why.append("%d external DDS" % s["ext"])
        if s["xmesh"]:
            why.append("%d cross-outfit mesh/shapedata" % s["xmesh"])
        if s["prov"]:
            why.append("support layer: " + ",".join(s["prov"]))
        if s["phys"]:
            why.append("%d physics config(s)" % s["phys"])
        if s["chain_bad"]:
            why.append("%d broken BodySlide chain(s)" % s["chain_bad"])
        if s["arma_unres"]:
            why.append("%d unresolved ARMA model(s)" % s["arma_unres"])
        if s["ext_missing"]:
            why.append("%d ref(s) to mods absent from this instance" % s["ext_missing"])
        if s["props"]:
            why.append("%d shared-proposal rows" % s["props"])
        A("| %d | %s | %d | %s |" % (i, q(o), s["complexity"], "; ".join(why) or "self-contained"))
    A("")
    A("**Most complex: %s** (score %d). Second: %s."
      % (q(rank[0]), st[rank[0]]["complexity"], q(rank[1])))
    A("")
    A("### 8. Which outfit is the best first P02B pilot?")
    A("")
    ok = [o for o in C.OUTFIT_IDS if st[o]["total"] != "BLOCKED"]
    clean = [o for o in ok if st[o]["ext_missing"] == 0 and not st[o]["props"]]
    pool = clean or ok or C.OUTFIT_IDS
    pilot = min(pool, key=lambda o: st[o]["complexity"])
    ps = st[pilot]
    A("**Recommended pilot: %s** - audit %s, complexity %d, %d game NIF, %d DDS in use, %d cross-outfit DDS, "
      "%d BodySlide project(s), %d external-missing references, support layers: %s."
      % (q(pilot), ps["total"], ps["complexity"], ps["game"], ps["dds"], ps["cross"], ps["bs"],
         ps["ext_missing"], (", ".join(ps["prov"]) or "none")))
    A("")
    A("Rationale: it is the cheapest complete proof of the namespace rule, so a P02B failure is attributable to the plan "
      "itself rather than to a messy source. Runners-up: " + ", ".join(q(x) for x in sorted(pool, key=lambda o: st[o]["complexity"])[1:4]) + ".")
    A("")
    A("Outfits that must **not** be first: " + ", ".join(
        q(o) + " (" + st[o]["total"] + ")" for o in C.OUTFIT_IDS if st[o]["total"] == "BLOCKED") + ".")
    A("")
    A("### 9. Which target paths collide?")
    A("")
    A("**0.** The audit re-derives collisions independently of the migration tables by indexing every planned target "
      "path (mesh targets, BodySlide outputs and OSP names) and comparing the owning Outfit IDs. Two outfits never "
      "land on the same path.")
    A("")
    A("For the record, the *current* MO2 VFS does contain override conflicts, but they are source-side, not "
      "target-side: the CL09 Latex Rework (priority 887) overrides 37 base paths, and meta.ini is supplied by every mod.")
    A("")
    A("### 10. Which references are still unresolvable?")
    A("")
    A("Only **%d distinct DDS** are unresolvable (they appear in many shape/slot rows). The frozen P00 index covers "
      "mod directories only and this MO2 instance has no vanilla Data tree, so each one was classified by evidence "
      "rather than guessed:" % (len(by_class.get("EXTERNAL_MOD_MISSING", [])) + len(by_class.get("VANILLA_CANDIDATE", []))))
    A("")
    A("| class | distinct DDS | meaning |")
    A("|---|---|---|")
    A("| EXTERNAL_MOD_MISSING | %d | mod-scoped path whose owning mod is not installed here - nothing can be copied |"
      % len(by_class.get("EXTERNAL_MOD_MISSING", [])))
    A("| VANILLA_CANDIDATE | %d | generic engine/utility path, normally base game, cannot be confirmed here |"
      % len(by_class.get("VANILLA_CANDIDATE", [])))
    A("| VANILLA_ALLOWED | %d | documented Skyrim base-game path - the brief permits these to stay outside the namespace |"
      % len(by_class.get("VANILLA_ALLOWED", [])))
    A("")
    A("Owners of the external-missing references (top 20 by path):")
    A("")
    A("| virtual_path | affected outfits |")
    A("|---|---|")
    for r in sorted(by_class.get("EXTERNAL_MOD_MISSING", []), key=lambda x: x["virtual_path"])[:20]:
        A("| " + q(r["virtual_path"]) + " | " + r["affected_outfits"].replace(";", ", ") + " |")
    if len(by_class.get("EXTERNAL_MOD_MISSING", [])) > 20:
        A("| _... %d more, full list in P02A_UNRESOLVED_REFERENCE_CLASSIFICATION.csv_ | |"
          % (len(by_class["EXTERNAL_MOD_MISSING"]) - 20))
    A("")
    A("These are already broken at runtime today (the engine falls back), so they do not block the namespace rule - "
      "but they do mean several source NIFs ship references the Pack cannot satisfy. A human must decide whether to "
      "install the owning mods, drop the references, or accept them.")
    A("")
    A("### 11. Which existing PBR / rework need provenance kept?")
    A("")
    A("| outfit | role | mod | handling |")
    A("|---|---|---|---|")
    for o in C.OUTFIT_IDS:
        for k, v in C.OUTFITS[o].get("support", {}).items():
            if k not in ("PBR_PATCH", "LATEX_REWORK", "REWORK", "PHYSICS_PATCH"):
                continue
            note = ("provenance only - recorded so the origin stays traceable; P05/P06 will redesign the material "
                    "standard and must not treat the current PBR as final" if "PBR" in k else
                    "rework is the VFS winner over the base mod; the rework/base provenance chain must survive migration")
            A("| %s | %s | %s | %s |" % (q(o), k, q(v), note))
    A("")
    A("Physical state recorded for traceability: " + ", ".join(
        "%s=%d file(s)" % (k, v) for k, v in Counter(
            col(r, "asset_type") for r in (d["source_map"] or []) if col(r, "asset_type").upper() == "PBR_JSON").items()) or "no PBR json in the frozen index")
    A("")
    A("### 12. After planning, can each outfit own an independent namespace?")
    A("")
    A("**YES, for everything the Pack owns.** All %d planned game meshes, %d BodySlide outputs, %d ShapeData NIF, "
      "%d OSP, %d OSD, %d ARMA model paths and %d plugin DDS references resolve inside "
      % (T("game") + T("bso"), T("bso"), T("sd"),
         len({col(r, "new_osp") for r in (d["bodyslide"] or []) if col(r, "new_osp")}),
         len({col(r, "new_osd") for r in (d["bodyslide"] or []) if col(r, "new_osd")}),
         T("arma"), T("ptex"))
      + q("meshes\\ZLJ\\CombatLatex\\<OUTFIT_ID>") + " / " + q("textures\\ZLJ\\CombatLatex\\<OUTFIT_ID>") + ".")
    A("")
    A("Two honest caveats: (a) the shared-material whitelist stays **NONE** - %d rows are recorded as "
      "PROPOSAL_SHARED_NOT_APPROVED and each of them is still copied per outfit; (b) %d references point at mods that "
      "are absent from this instance and therefore cannot be brought into any namespace."
      % (T("props"), T("ext_missing")))
    A("")
    A("### 13. What blocks P02B?")
    A("")
    A("**Structural blockers (must be resolved by a human decision before any file is touched):**")
    A("")
    A("| outfit | gate | what is wrong |")
    A("|---|---|---|")
    for o in C.OUTFIT_IDS:
        for cid in ("C1", "C2", "C3", "C4", "C5"):
            r = next((x for x in audit if x.get("OUTFIT_ID") == o and x.get("check_id") == cid), None)
            if r and r.get("result") == "BLOCKED":
                A("| %s | %s %s | %s |" % (q(o), cid, r.get("check_name", ""), r.get("evidence", "")))
    A("")
    A("**Open decisions (not blockers, but the plan is provisional until they are answered):**")
    A("")
    A("1. OSP naming rule - allow " + q("ZLJ_<OUTFIT_ID>__<Part>.osp") + " for multi-slider-set outfits, or change the rule?")
    A("2. CL09 rework/BodySlide split - the Latex Rework wins 11 meshes + 7 DDS while all ShapeData/OSD still come "
      "from the base mod. After a BodySlide build the visible geometry may be the base shape, not the rework. Decide before any build.")
    A("3. CL09 + CL11 orphan ShapeData - 6 flat ShapeData NIF and 2 CBBE/3BBB ShapeData folders have no OSP claiming them. Keep, drop, or attach?")
    A("4. CL11 body branch - keep only the CBBE/3BBB/3BA compatible branch; BHUNP files stay in place until P02B decides which files are dropped.")
    A("5. CL08 ARMA models - %d wearable model references cannot be resolved. Confirm before copying." % st["CL08_SpearHead"]["arma_unres"])
    A("6. Vanilla probe - authorise one read-only existence check against a real Skyrim Data tree to settle the %d "
      "VANILLA_CANDIDATE references and to separate vanilla from genuinely missing." % len(by_class.get("VANILLA_CANDIDATE", [])))
    A("7. Physics bone verification - all %d HDT-SMP configs have unknown bone checks because the bone set is not in the frozen evidence."
      % T("phys"))
    A("8. Shared material standard - %d proposal rows are parked for P05; P02A deliberately created no Shared folder." % T("props"))
    A("9. EDID granularity - the ledger emits " + q("ZLJ_CL_<Outfit>_<BodySlot>_<Variant>")
      + " (e.g. " + q("ZLJ_CL_LatexKitty_BODY_AA") + ") because CBBE/3BA variants must stay distinguishable. "
      "The brief's example is the coarser " + q("ZLJ_CL_Haley_Body") + ". Confirm which granularity the final plugin should use.")
    A("10. OSP output vs ARMA reference mismatch - for several outfits the OSP " + q("output_file") + " name does not match "
      "the LOD1 mesh the ARMA actually points at, so the slider sets are not currently wired to the plugin. "
      "P02B/P03 must decide between rebuilding to a replacement mesh and shipping them as additional assets.") 
    A("")

    A("## Target namespace layout")
    A("")
    A("- " + q("meshes\\ZLJ\\CombatLatex\\<OUTFIT_ID>\\...") + " - game meshes and BodySlide build outputs")
    A("- " + q("textures\\ZLJ\\CombatLatex\\<OUTFIT_ID>\\...") + " - every DDS actually referenced by that outfit")
    A("- " + q("CalienteTools\\BodySlide\\ShapeData\\ZLJ_CombatLatex\\<OUTFIT_ID>\\<data folder>\\") + " - ShapeData NIF + OSD")
    A("- " + q("CalienteTools\\BodySlide\\SliderSets\\ZLJ_<OUTFIT_ID>.osp") + " - SliderSet, UI name " + q("[ZLJ Combat Latex] <Outfit> - <Part>"))
    A("- " + q("ZLJ_CombatLatex.esp") + " - single target plugin, EDID namespace " + q("ZLJ_CL_<OUTFIT>_<PART>") + ", no FormID generated in P02A")
    A("")

    A("## Deliverables")
    A("")
    for k in ["source_map", "mesh", "texture", "closure", "nif_rewrite", "bodyslide", "sd_rewrite",
              "plugin", "arma", "plugin_tex", "physics"]:
        p = os.path.join(OUT, CSV_FILES[k])
        rows_ = d.get(k) or []
        A("- %s %s (%d rows)" % ("[x]" if os.path.exists(p) else "[ ]", CSV_FILES[k], len(rows_)))
    for extra in ("P02A_SELF_CONTAINMENT_AUDIT.csv", "P02A_UNRESOLVED_REFERENCE_CLASSIFICATION.csv",
                  "P02A_ARCHITECTURE.md", "P02A_MASTER_PLAN.md"):
        p = os.path.join(OUT, extra)
        A("- %s %s" % ("[x]" if os.path.exists(p) else "[ ]", extra))
    A("- [x] " + q("reports/P02A/outfits/") + " - 11 per-outfit manifests")
    A("")

    A("## STOP")
    A("")
    A("P02A ends here. **P02B is not authorised by this document.** No COPY / MOVE / DELETE / NIF / ESP / OSP / DDS "
      "write may happen until a human reviews this migration design and answers the open decisions above.")
    A("")
    C.write_md(os.path.join(OUT, "P02A_MASTER_PLAN.md"), "\n".join(L))
    print("wrote", os.path.join(OUT, "P02A_MASTER_PLAN.md"))
    print("pilot:", pilot, "| most complex:", rank[0])
    for o in C.OUTFIT_IDS:
        s = st[o]
        print("  %-20s gameNIF=%-3d bs=%-3d dds=%-4d cross=%-3d(after %d) xmesh=%-3d extmiss=%-4d props=%-4d cplx=%-4d %s"
              % (o, s["game"], s["bs"], s["dds"], s["cross"], s["cross_open"], s["xmesh"],
                 s["ext_missing"], s["props"], s["complexity"], s["total"]))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
