# -*- coding: utf-8 -*-
"""P02B0 incremental source-drift check.

Compares the frozen P00 evidence against the live MO2 instance for:
  * the modlist file hash,
  * the 11 Combat Latex source mods,
  * their PBR / rework support mods,
  * the BodySlide output mod.

READ-ONLY: the live tree is only stat-ed and hashed, never written.

Output: reports/P02B/P02B_SOURCE_DRIFT_CHECK.csv
        reports/P02B/P02B_SOURCE_DRIFT_SUMMARY.md
"""
import csv as _csv
import hashlib
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "P02A"))
import p02a_common as C

P = C.P00.get()
MODS = r"E:\SkyrimAE\mo2\mods"
MODLIST = r"E:\SkyrimAE\mo2\profiles\Default\modlist.txt"
OUTDIR = os.path.join(C.ROOT, "reports", "P02B")
OUT_CSV = os.path.join(OUTDIR, "P02B_SOURCE_DRIFT_CHECK.csv")
OUT_MD = os.path.join(OUTDIR, "P02B_SOURCE_DRIFT_SUMMARY.md")
BS_OUTPUT_MOD = "\u8f93\u51fa\u00b7BodySlide Output"
Q = chr(96)

HEADER = ["scope", "mod_id", "virtual_path", "p00_sha256", "current_sha256", "p00_size",
          "current_size", "p00_mtime", "current_mtime", "drift_class", "affects_outfit", "notes"]


def qi(s):
    return Q + str(s) + Q


def sha256_file(p):
    h = hashlib.sha256()
    try:
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
    except OSError:
        return ""
    return h.hexdigest()


def current_files(mod):
    root = os.path.join(MODS, mod)
    out = {}
    if not os.path.isdir(root):
        return out
    for dirpath, _dirs, names in os.walk(root):
        for n in names:
            p = os.path.join(dirpath, n)
            rel = os.path.relpath(p, root)
            try:
                st = os.stat(p)
            except OSError:
                continue
            out[C.norm(rel)] = (st.st_size, round(st.st_mtime))
    return out


def effective_providers(outfit):
    prov = set(P.mods_of_outfit(outfit))
    for name in ("P02A_MESH_MIGRATION.csv", "P02A_TEXTURE_MIGRATION.csv",
                 "P02A_NIF_TEXTURE_REWRITE.csv", "P02A_SHAPEDATA_TEXTURE_REWRITE.csv",
                 "P02A_BODYSLIDE_MIGRATION.csv", "P02A_GLOBAL_PROVIDER_LOOKUP.csv"):
        p = os.path.join(C.OUT, name)
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8-sig", newline="") as f:
            for r in _csv.DictReader(f):
                o = r.get("OUTFIT_ID") or ""
                if o != outfit and outfit not in (r.get("affected_outfits") or ""):
                    continue
                for k in ("winning_provider", "source_provider", "shapedata_nif_winning_provider",
                          "vfs_winning_provider", "current_provider"):
                    v = (r.get(k) or "").strip()
                    if v and v.upper() not in ("UNKNOWN", "NONE", "N/A"):
                        prov.add(v)
    return prov


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    rows = []

    frozen_sha = P.scope_evidence.get("modlist_sha256", "")
    frozen_lines = P.scope_evidence.get("modlist_lines", "")
    cur_sha = sha256_file(MODLIST)
    cur_lines = sum(1 for _ in open(MODLIST, encoding="utf-8", errors="replace"))
    rows.append(["MODLIST_SHA256", "-", "profiles/Default/modlist.txt", frozen_sha, cur_sha,
                 frozen_lines, cur_lines, "", "",
                 "UNCHANGED" if frozen_sha == cur_sha else "CHANGED", "ALL",
                 "frozen lines=%s current lines=%s" % (frozen_lines, cur_lines)])

    targets, seen = [], set()
    for o in C.OUTFIT_IDS:
        for m in P.mods_of_outfit(o):
            role = "BASE" if m == C.OUTFITS[o]["primary"] else \
                next((k for k, v in C.OUTFITS[o].get("support", {}).items() if v == m), "SUPPORT")
            key = ("SOURCE_MOD/" + role, m)
            if key in seen:
                continue
            seen.add(key)
            targets.append(("SOURCE_MOD/" + role, m, o))
    targets.append(("BODYSLIDE_OUTPUT_MOD", BS_OUTPUT_MOD, "ALL"))

    for scope, mod, outfit in targets:
        p00 = {}
        for f in P.files_of_mod.get(mod, []):
            p00[C.norm(f["vpath"])] = (f.get("sha256", ""), f.get("size", ""), round(f.get("mtime", 0)))
        cur = current_files(mod)
        for vp in sorted(set(p00) | set(cur)):
            a, b = p00.get(vp), cur.get(vp)
            if a and not b:
                cls, note = "REMOVED", "present in frozen P00, absent now"
            elif b and not a:
                cls, note = "NEW", "absent from frozen P00, present now"
            else:
                if str(a[1]) == str(b[0]) and str(a[2]) == str(b[1]):
                    cls, note = "UNCHANGED", "size+mtime identical"
                else:
                    cls, note = "CHANGED", "size %s to %s, mtime %s to %s" % (a[1], b[0], a[2], b[1])
            rows.append([scope, mod, vp, a[0] if a else "", "", a[1] if a else "", b[0] if b else "",
                         a[2] if a else "", b[1] if b else "", cls, outfit, note])
    C.write_csv(OUT_CSV, HEADER, rows)

    prov = effective_providers("CL06_ToxicCat")
    cl06_rows = [r for r in rows if r[1] in prov and r[0] != "MODLIST_SHA256"]
    counts = Counter(r[9] for r in cl06_rows)
    gate = "PASS" if counts.get("CHANGED", 0) == 0 and counts.get("REMOVED", 0) == 0 else "FAIL"

    per_outfit = defaultdict(Counter)
    for r in rows:
        if r[0] == "MODLIST_SHA256":
            continue
        for o in (r[10] or "").split(";"):
            if o:
                per_outfit[o][r[9]] += 1

    L = []
    A = L.append
    A("# P02B0 source-drift summary")
    A("")
    A("Incremental check only - P00 was **not** rescanned. The live tree is stat-ed and hashed, never written.")
    A("")
    A("## Modlist")
    A("")
    A("| field | frozen P00 | current |")
    A("|---|---|---|")
    A("| lines | %s | %s |" % (frozen_lines, cur_lines))
    A("| sha256 | " + qi(frozen_sha[:16]) + " | " + qi(cur_sha[:16]) + " |")
    A("| verdict | | **%s** |" % ("UNCHANGED" if frozen_sha == cur_sha else "CHANGED"))
    A("")
    A("## CL06 pilot gate")
    A("")
    A("Effective provider set for CL06_ToxicCat: %d mod(s)." % len(prov))
    A("")
    for m in sorted(prov):
        c = Counter(r[9] for r in rows if r[1] == m and r[0] != "MODLIST_SHA256")
        A("* " + qi(m) + " - " + (", ".join("%s=%d" % kv for kv in c.most_common()) or "no files compared"))
    A("")
    A("**CL06_PILOT_GATE = %s** (CHANGED=%d, REMOVED=%d)"
      % (gate, counts.get("CHANGED", 0), counts.get("REMOVED", 0)))
    A("")
    A("## Per-outfit drift")
    A("")
    A("| outfit | UNCHANGED | CHANGED | NEW | REMOVED |")
    A("|---|---|---|---|---|")
    for o in C.OUTFIT_IDS:
        c = per_outfit.get(o, Counter())
        A("| " + qi(o) + " | %d | %d | %d | %d |"
          % (c.get("UNCHANGED", 0), c.get("CHANGED", 0), c.get("NEW", 0), c.get("REMOVED", 0)))
    A("")
    A("Outfits other than CL06 are recorded only; their drift is refreshed locally when their turn comes.")
    A("")
    C.write_md(OUT_MD, "\n".join(L))

    print("rows:", len(rows))
    print("modlist:", "UNCHANGED" if frozen_sha == cur_sha else "CHANGED", "| lines", frozen_lines, "->", cur_lines)
    print("CL06 provider set (%d):" % len(prov))
    for m in sorted(prov):
        c = Counter(r[9] for r in rows if r[1] == m and r[0] != "MODLIST_SHA256")
        print("   %-58s %s" % (m[:58], dict(c)))
    print("CL06_PILOT_GATE =", gate)
    print("wrote", OUT_CSV)
    print("wrote", OUT_MD)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
