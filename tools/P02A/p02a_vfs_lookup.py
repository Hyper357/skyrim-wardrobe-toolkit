# -*- coding: utf-8 -*-
"""P02A.1-2 -- targeted global VFS provider lookup (manual-audit finding #3).

Resolves every distinct virtual_path listed in
reports/P02A/P02A_UNRESOLVED_REFERENCE_CLASSIFICATION.csv against the FULL MO2
instance (all 2253 mod directories) plus the game Data root.

The audit correction being applied: "not present in the frozen P00 TARGET09 index"
does NOT mean "absent from this MO2 instance". Only a complete provider lookup
that still finds nothing may be called TRUE_MISSING.

Two-stage read-only lookup
  stage 1  exact path   -- <mod>/<vp> exists?      (2253 mods + game Data root)
  stage 2  basename     -- for anything stage 1 misses, does ANY mod in the whole
                           instance carry a file with the same basename anywhere?
                           This separates "truly absent" from "author moved/renamed
                           the folder", which must not be reported as missing.

STRICT READ-ONLY
  * os.scandir / os.listdir / os.path.isfile / os.walk only;
  * NO .nif / .dds / .esp binary is ever opened or parsed;
  * nothing is created, copied, moved or deleted;
  * P00 / P01 are never rescanned; only the frozen scope evidence is read.

Writes exactly one file: reports/P02A/P02A_GLOBAL_PROVIDER_LOOKUP.csv
"""
import collections
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
import p02a_common as C  # noqa: E402

MODS_ROOT = "E:\\SkyrimAE\\mo2\\mods"
MODLIST = "E:\\SkyrimAE\\mo2\\profiles\\Default\\modlist.txt"
GAME_DATA = "E:\\SkyrimAE\\Data"
INPUT_CSV = os.path.join(C.OUT, "P02A_UNRESOLVED_REFERENCE_CLASSIFICATION.csv")
OUTPUT_CSV = os.path.join(C.OUT, "P02A_GLOBAL_PROVIDER_LOOKUP.csv")

HEADER = ["virtual_path", "providers_all", "n_providers", "winning_provider",
          "winning_priority", "winner_enabled", "provider_separator_if_known",
          "found_in_game_data", "lookup_scope", "lookup_method", "classification",
          "notes"]

N_MOD_DIRS = 2253
LOOKUP_SCOPE = ("all %d mod dirs under E:\\SkyrimAE\\mo2\\mods (exact-path check, then a "
                "whole-tree basename sweep for anything missed) + E:\\SkyrimAE\\Data loose "
                "files; BSA-packed contents NOT inspected -- this is a known blind spot and "
                "no result here proves absence inside a .bsa" % N_MOD_DIRS)
LOOKUP_METHOD = ("stage1 os.path.isfile(<mod>\\<vp>) per mod dir; stage2 os.walk basename "
                 "sweep over the whole mods tree; zero binary reads")

# Data top-level folders that need no synthetic "textures\" prefix.
DATA_ROOTS = ("textures", "meshes", "scripts", "shaders", "sound", "dialog", "skse",
              "skseedit", "misc", "fonts", "icon", "video", "_update", "strings",
              "sequence", "facegen", "lod", "interface", "documentation")

# --- classification families (exact literal prefix / basename tests) --------
# A basename-only hit is only considered when the stem is distinctive. Generic
# names such as d.dds / n.dds / s.dds / 8_d.dds collide constantly across unrelated
# mods, and calling one of those "the same asset" would be exactly the fuzzy
# matching this stage forbids.
MIN_DISTINCTIVE_STEM = 4


def distinctive(basename):
    stem = os.path.splitext(basename)[0].lower().strip()
    return len(stem) >= MIN_DISTINCTIVE_STEM


GLOBAL_BODY_SKIN_ROOTS = ("textures/actors/character/female/",)
GLOBAL_BODY_SKIN_BASENAMES = ("femalebody", "femalehands")
VANILLA_ENGINE_ROOTS = ("textures/cubemaps/", "textures/ghost/", "textures/effects/",
                        "textures/fx/", "textures/sound/", "textures/interface/",
                        "textures/fonts/", "textures/menus/", "textures/misc/")


def rel(vp):
    s = str(vp).replace("\\", "/").strip().strip('"').strip()
    while s.lower().startswith("data/"):
        s = s[4:]
    return s.lstrip("/").lower()


def candidate_rels(vp):
    r"""The path as written, plus the textures\ -prefixed form when the raw form is a
    bare Data-relative path (NIF texture slots always resolve under textures\)."""
    base = rel(vp)
    out = [base]
    if base.split("/", 1)[0] not in DATA_ROOTS and "/" in base:
        out.append("textures/" + base)
    seen, uniq = set(), []
    for x in out:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq


def read_modlist():
    """[(line_no, name, enabled, separator_band)] in modlist order."""
    with open(MODLIST, "r", encoding="utf-8-sig", errors="replace") as f:
        lines = f.read().splitlines()
    out, band, seps = [], "(above first separator)", []
    for i, ln in enumerate(lines, 1):
        t = ln.strip()
        if not t or t.startswith("#"):
            continue
        if t.startswith("+"):
            name, en = t[1:].strip(), True
        elif t.startswith("-"):
            name, en = t[1:].strip(), False
        else:
            name, en = t, True
        if name.lower().endswith("_separator"):
            band = name
            seps.append((i, name))
            continue
        out.append((i, name, en, band))
    return out, seps



# --- P02A.1 supplement: additional paths looked up with the identical method ---
# The SoftLighting siblings of the GLOBAL_BODY_SKIN family. They are referenced by
# the ShapeData texture table but were absent from the first lookup input, so
# bodyslide had to stop at UNRESOLVED. Same two-stage read-only method, same
# header, same lookup_scope / lookup_method wording, same classification rules.
SDTEX = os.path.join(C.OUT, "P02A_SHAPEDATA_TEXTURE_REWRITE.csv")
SUPPLEMENT_CLASS = "SUPPLEMENTAL_P02A1_2_SOFTLIGHTING_SIBLING"

EXTRA_PATHS = [
    "textures/actors/character/female/femalebody_1_sk.dds",
    "textures/actors/character/female/femalebody_etc_v2_1_sk.dds",
    "textures/actors/character/female/femalehands_1_sk.dds",
]


def referencing_outfits(paths):
    """Which Outfits reference these paths in the ShapeData texture table."""
    if not os.path.exists(SDTEX):
        return {}
    want = set(rel(p) for p in paths)
    hit = dict((p, set()) for p in paths)
    with open(SDTEX, "rb") as f:
        for r in csv.DictReader(io.StringIO(f.read().decode("utf-8-sig"))):
            n = rel(r.get("old_dds_path", ""))
            if n in want:
                hit[n].add(r.get("OUTFIT_ID", ""))
    return dict((p, ";".join(sorted(v))) for p, v in hit.items())



# The lookup table is CUMULATIVE. It must never shrink because the input file was
# repurposed by another table owner: once a path has been classified here it stays
# classified, even if the input stops listing it.
RESTORE_PATHS = [
    "armor/aokili/curiousadventurer/curiousadventurer_ebony_n.dds",
    "ghost/ghostcolour4_n.dds",
    "textures/armor/[d] bdor/hair/0alfa.dds",
    "textures/armor/[d] bdor/hair/0alfa_n.dds",
    "textures/armor/[d] bdor/hair/ppw/21/pem_00_hair_0001_hair.dds",
    "textures/armor/[d] bdor/hair/ppw/21/pem_00_hair_0001_hair_n.dds",
    "textures/armor/[d] bdor/hair/ppw/21/plw_00_hairdeco_0002.dds",
    "textures/armor/[d] bdor/hair/ppw/21/plw_00_hairdeco_0002_n.dds",
    "textures/cubemaps/dynamic1pxcubemap_black.dds",
    "textures/cubemaps/mirror_e.dds",
    "textures/devious/cubemaps/zad_shinycontrast_e.dds",
    "textures/devious/expansion/collarpostebonite_d.dds",
    "textures/devious/expansion/collarpostebonite_em.dds",
    "textures/devious/expansion/collarpostebonite_n.dds",
    "textures/kziitd/sack/env2.dds",
]


def baseline_paths():
    """Paths already classified in a previous run of THIS output table."""
    if not os.path.exists(OUTPUT_CSV):
        return []
    with open(OUTPUT_CSV, "rb") as f:
        return [r["virtual_path"].strip()
                for r in csv.DictReader(io.StringIO(f.read().decode("utf-8-sig")))
                if is_pathlike(r.get("virtual_path", "").strip())]



PATHLIKE_EXTS = (".dds", ".nif", ".osp", ".osd", ".xml", ".json", ".txt", ".ini")


def is_pathlike(vp):
    """Reject placeholder tokens such as 'unknown' that are not virtual paths."""
    if not vp:
        return False
    n = rel(vp)
    if "/" not in n and chr(92) not in vp:
        return False
    return n.endswith(PATHLIKE_EXTS)


def main():
    P00 = C.P00.get()
    modlist, seps = read_modlist()
    prio = {n: ln for ln, n, _e, _b in modlist}
    enabled = {n: e for _l, n, e, _b in modlist}
    band = {n: b for _l, n, _e, b in modlist}
    scope_members = set(P00.scope_evidence.get("scope_member_names") or [])

    with open(INPUT_CSV, "rb") as f:
        src = list(csv.DictReader(io.StringIO(f.read().decode("utf-8-sig"))))
    targets, seen = [], set()
    skipped = 0
    for r in src:
        vp = r["virtual_path"].strip()
        if not is_pathlike(vp):
            skipped += 1
            continue
        if rel(vp) in seen:
            continue
        seen.add(rel(vp))
        targets.append((vp, r.get("reference_class", ""), r.get("affected_outfits", "")))
    if skipped:
        print("skipped %d non-path placeholder row(s) from the input (e.g. %r)"
              % (skipped, "unknown"))
    targets.sort(key=lambda t: t[0].lower())

    # ---- supplement: fold in the P02A.1 SoftLighting siblings ---------------
    outfits_of = referencing_outfits(EXTRA_PATHS)
    added = 0
    for vp in EXTRA_PATHS:
        if rel(vp) in seen:
            continue
        seen.add(rel(vp))
        targets.append((vp, SUPPLEMENT_CLASS, outfits_of.get(rel(vp), "")))
        added += 1
    if added:
        print("supplement: %d additional path(s) folded into the same lookup" % added)

    # cumulative floor: paths classified in earlier runs must never be dropped
    for vp in RESTORE_PATHS + baseline_paths():
        if rel(vp) in seen:
            continue
        seen.add(rel(vp))
        targets.append((vp, "CARRIED_FORWARD", ""))
        added += 1
    if added:
        print("cumulative: %d path(s) added (supplement + carry-forward)" % added)

    # ---- stage 1: exact path, one pass over every mod directory ------------
    cand_of = {vp: candidate_rels(vp) for vp, _c, _a in targets}
    all_cands = sorted({c for cs in cand_of.values() for c in cs})
    top_of = {c: c.split("/", 1)[0] for c in all_cands}
    with os.scandir(MODS_ROOT) as it:
        mod_dirs = sorted((e.path, e.name) for e in it if e.is_dir())
    if len(mod_dirs) != N_MOD_DIRS:
        print("WARNING: mod dir count is %d, expected %d" % (len(mod_dirs), N_MOD_DIRS))

    exact = collections.defaultdict(list)      # candidate rel -> [mod name]
    exact_path_of = {}                          # (mod, candidate) -> candidate
    for md_path, md_name in mod_dirs:
        with os.scandir(md_path) as it:
            present = set(e.name.lower() for e in it if e.is_dir())
        for c in all_cands:
            if top_of[c] not in present:
                continue
            if os.path.isfile(os.path.join(md_path, *c.split("/"))):
                exact[c].append(md_name)
                exact_path_of[(md_name, c)] = c
    print("stage 1: %d mod directories x %d candidate relative paths" % (len(mod_dirs), len(all_cands)))

    in_game = {c: os.path.isfile(os.path.join(GAME_DATA, *c.split("/"))) for c in all_cands}
    n_bsa = len([f for f in os.listdir(GAME_DATA) if f.lower().endswith(".bsa")])
    game_has_loose_textures = os.path.isdir(os.path.join(GAME_DATA, "textures"))

    # ---- stage 2: whole-tree basename sweep, only for what stage 1 missed ---
    missed_basenames = set()
    for vp, _c, _a in targets:
        if not any(exact[c] or in_game[c] for c in cand_of[vp]):
            missed_basenames.add(os.path.basename(rel(vp)))
    by_basename = collections.defaultdict(list)
    n_files = 0
    if missed_basenames:
        for md_path, md_name in mod_dirs:
            for root, _dirs, files in os.walk(md_path):
                for fn in files:
                    n_files += 1
                    lf = fn.lower()
                    if lf in missed_basenames:
                        rp = os.path.relpath(os.path.join(root, fn), md_path).replace("\\", "/")
                        by_basename[lf].append((md_name, rp))
        for k in by_basename:
            by_basename[k].sort(key=lambda x: (prio.get(x[0], 99999), x[0]))
    print("stage 2: basename sweep over %d files for %d distinct basenames"
          % (n_files, len(missed_basenames)))

    # ---- assemble ----------------------------------------------------------
    rows = []
    for vp, ref_class, outfits in targets:
        n = rel(vp)
        cands = cand_of[vp]
        matched_form = ""
        exact_hits, loose = [], []
        for c in cands:
            if exact[c]:
                matched_form = c
                for mod in exact[c]:
                    exact_hits.append((prio.get(mod, 99999), mod, enabled.get(mod, True), c))
            if in_game[c]:
                loose.append(c)

        mismatch = []
        rejected = []
        if not exact_hits and not loose:
            base_now = os.path.basename(n)
            if distinctive(base_now):
                for mod, rp in by_basename.get(base_now, []):
                    mismatch.append((prio.get(mod, 99999), mod, enabled.get(mod, True), rp))
            else:
                rejected = by_basename.get(base_now, [])

        # de-duplicate providers across candidate forms
        def dedup(items):
            by = {}
            for pr, m, en, p in items:
                if m not in by or pr < by[m][0]:
                    by[m] = (pr, en, p)
            return sorted((pr, m, en, p) for m, (pr, en, p) in by.items())
        exact_hits = dedup(exact_hits)
        mismatch = dedup(mismatch)

        providers = ["%s#%d%s" % (m, pr, "" if en else "(disabled)")
                     for pr, m, en, _p in exact_hits]
        providers += ["%s#%d%s|PATH-MISMATCH:%s" % (m, pr, "" if en else "(disabled)", p)
                      for pr, m, en, p in mismatch]
        providers_all = ";".join(providers)

        en_pool = [x for x in exact_hits if x[2]] or exact_hits
        win_pool = en_pool or mismatch
        if win_pool:
            pr0, m0, e0, _p0 = win_pool[0]
            win_provider, win_prio, win_enabled, win_band = m0, pr0, e0, band.get(m0, "")
        else:
            win_provider = win_prio = win_enabled = win_band = ""

        found_game = "yes" if loose else "no"

        notes = ["input reference_class=%s" % (ref_class or "NA")]
        if outfits:
            notes.append("affected_outfits=%s" % outfits)
        notes.append("probed forms: %s" % " | ".join(cands))
        if matched_form and matched_form != n:
            notes.append("exact hit under Data-relative form '%s'" % matched_form)
        notes.append("loose game Data hit: %s" % (",".join(loose) if loose else "none"))
        if mismatch:
            notes.append("PATH MISMATCH: the referenced folder does not exist, but %d mod(s) in "
                         "this instance ship a file with the same basename elsewhere: %s"
                         % (len(mismatch), "; ".join("%s :: %s" % (m, p) for _pr, m, _e, p in mismatch[:6])))
            notes.append("NOT upgraded to EXTERNAL_PROVIDER_FOUND: no provider exists at the "
                         "referenced path, and a same-basename file elsewhere is NOT proof of the "
                         "same asset -- identity would be a fuzzy match, which this stage forbids. "
                         "Left UNKNOWN for human confirmation")
        if win_provider and not exact_hits:
            notes.append("winning provider is a PATH-MISMATCH provider, not a provider of the "
                         "referenced path")

        # ---- classification -------------------------------------------------
        canon = n
        for c in cands:
            if c.split("/", 1)[0] in DATA_ROOTS:
                canon = c
                break
        base = os.path.basename(canon)
        if canon != n:
            notes.append("classification keyed on canonical Data form '%s'" % canon)
        if canon.startswith(GLOBAL_BODY_SKIN_ROOTS) and base.startswith(GLOBAL_BODY_SKIN_BASENAMES):
            cls = "GLOBAL_BODY_SKIN"
            notes.append("AUDIT #4: Body/skin system texture of the canonical CBBE_3BA female "
                         "body -- keep the EXTERNAL reference, NEVER copy into "
                         "textures\\ZLJ\\CombatLatex\\<OUTFIT_ID>\\")
            if exact_hits:
                notes.append("NOTICE: this body texture is OVERRIDDEN in the live VFS by mod '%s' "
                             "(priority %s), so our meshes resolve against that body's skin, not "
                             "the stock CBBE_3BA texture -- a real cross-body compatibility risk"
                             % (exact_hits[0][1], exact_hits[0][0]))
        elif exact_hits:
            cls = "EXTERNAL_PROVIDER_FOUND"
            if not any(x[2] for x in exact_hits):
                notes.append("only DISABLED mod(s) provide this path; not live in this profile")
        elif loose:
            cls = "EXTERNAL_PROVIDER_FOUND"
        elif mismatch:
            cls = "UNKNOWN"
        elif canon.startswith(VANILLA_ENGINE_ROOTS):
            cls = "VANILLA_ENGINE_RESOURCE"
            notes.append("stock Skyrim Data root: a loose-file miss is NOT evidence of absence, "
                         "almost certainly BSA-packed. NOT verified by this lookup; a .bsa "
                         "contents check is required before treating it as missing")
        else:
            cls = "TRUE_MISSING"
            if rejected:
                notes.append("complete lookup: no provider at this path and no loose game Data "
                             "file. Same-basename files DO exist elsewhere (%d, e.g. %s) but the "
                             "stem '%s' is non-distinctive, so treating one of them as this asset "
                             "would be a fuzzy match; they are therefore NOT counted as providers"
                             % (len(rejected), rejected[0][0] + " :: " + rejected[0][1],
                                os.path.splitext(base_now)[0]))
            else:
                notes.append("complete lookup: no provider at this path, no loose game Data file, "
                             "and the basename occurs in NO mod dir of this instance")
            notes.append(".bsa-packed contents remain unverified and are a known blind spot")

        if win_provider:
            notes.append("winning provider is %s the frozen P00 TARGET09 scope"
                         % ("in" if win_provider in scope_members else "out"))
        notes.append("game Data root has no loose 'textures' folder and holds %d .bsa archives"
                     % n_bsa)

        rows.append([vp, providers_all, len(exact_hits) + len(mismatch), win_provider,
                     win_prio, ("yes" if win_enabled else "no") if win_provider else "",
                     win_band, found_game, LOOKUP_SCOPE, LOOKUP_METHOD, cls, "; ".join(notes)])

    rows.sort(key=lambda r: r[0].lower())
    C.write_csv(OUTPUT_CSV, HEADER, rows)
    print("wrote", OUTPUT_CSV, len(rows), "rows")

    # ---- statistics ---------------------------------------------------------
    cc = collections.Counter(r[10] for r in rows)
    print("")
    print("classification counts:", dict(cc))
    for cls in ("EXTERNAL_PROVIDER_FOUND", "TRUE_MISSING", "GLOBAL_BODY_SKIN",
                "VANILLA_ENGINE_RESOURCE", "UNKNOWN"):
        sel = [r for r in rows if r[10] == cls]
        if not sel:
            continue
        print("")
        print("=== %s (%d) ===" % (cls, len(sel)))
        for r in sel:
            extra = ""
            if "PATH-MISMATCH" in r[1]:
                extra = "  [PATH-MISMATCH]"
            print("  %-70s <- %s%s" % (r[0], r[3] or "(none)", extra))
    print("")
    def has_exact(r):
        return any("PATH-MISMATCH" not in p for p in r[1].split(";") if p)
    buckets = collections.Counter()
    for r in rows:
        if r[10] in ("GLOBAL_BODY_SKIN", "VANILLA_ENGINE_RESOURCE"):
            continue
        if has_exact(r):
            buckets["exact_path_provider"] += 1
        elif r[1]:
            buckets["basename_candidate_only"] += 1
        else:
            buckets["no_candidate_anywhere"] += 1
    print("")
    print("evidence buckets (excluding GLOBAL_BODY_SKIN / VANILLA_ENGINE_RESOURCE):")
    for k in ("exact_path_provider", "basename_candidate_only", "no_candidate_anywhere"):
        print("   %-26s %d" % (k, buckets[k]))
    print("game Data root: %d .bsa archives, loose 'textures' folder present: %s"
          % (n_bsa, game_has_loose_textures))
    print("modlist.txt: %d entries, %d separator pseudo-mods" % (len(modlist), len(seps)))


if __name__ == "__main__":
    main()
