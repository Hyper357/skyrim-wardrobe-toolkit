#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p01_drift_check.py — did the 09 scope survive MO2's modlist rewrite?

P00 froze on modlist SHA256 5f03db69... and explicitly recorded that modlist
mtime is meaningless (MO2 rewrites the file atomically on every exit), so the
hash is the decision input. MO2 was restarted at 16:20 and rewrote the file,
so the hash no longer matches and the real question is narrower and more
useful: are the SAME 56 mods still inside the 09 separator?

This reads the live modlist, re-derives the scope by the same rule P00 used
(separator owns (nearest separator below + 1) .. (itself - 1)), and diffs the
member set against the frozen 01_MOD_INVENTORY. Read-only; writes nothing.
"""
import csv
import hashlib
import json
import os
import sys

PKT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ML = r"E:\SkyrimAE\mo2\profiles\Default\modlist.txt"
INV = os.path.join(PKT, "reports", "P00_RERUN", "01_MOD_INVENTORY.csv")
EV = os.path.join(PKT, "data", "P00_RERUN", "00_scope_evidence.json")
FROZEN_SHA = "5f03db69574ba916d358f12fff7ec6aff06b212e89e0c0dec982af3b8cc4ab4f"

sys.path.insert(0, os.path.join(PKT, "tools", "P00_RERUN"))


def main():
    raw = open(ML, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    for enc in ("utf-8-sig", "utf-8", "cp936", "utf-8-le"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    lines = text.splitlines()

    # An MO2 separator is a DISABLED MOD whose name ends in "_separator", not
    # a "#" comment. It owns the mods between the next separator above it (a
    # LARGER line number) and itself.
    seps = [i for i, l in enumerate(lines) if "_separator" in l]
    idx09 = [i for i, l in enumerate(lines)
             if "_separator" in l and l.lstrip("+- ").startswith("09")]
    if not idx09:
        print("FATAL: no 09 separator found in the live modlist")
        return 2
    s = idx09[0]
    below = max([i for i in seps if i < s], default=-1)
    lo, hi = below + 1, s - 1

    live = []
    for l in lines[lo:hi + 1]:
        m = l.strip()
        if not m or m.startswith("#"):
            continue
        if m[0] in "+-":
            m = m[1:]
        if m:
            live.append(m)

    with open(INV, encoding="utf-8-sig", newline="") as fh:
        frozen = [r["MOD_ID"] for r in csv.DictReader(fh)]
    ev = json.load(open(EV, encoding="utf-8"))

    fs, ls = set(frozen), set(live)
    added, removed = sorted(ls - fs), sorted(fs - ls)

    print("=" * 74)
    print("MODLIST DRIFT CHECK  (09 separator scope)")
    print("=" * 74)
    print("  modlist SHA256 now      : %s" % sha)
    print("  frozen SHA256 (P00)     : %s" % FROZEN_SHA)
    print("  hash match              : %s" % ("YES" if sha == FROZEN_SHA
                                              else "NO - file was rewritten"))
    print("  frozen scope lines      : L%s..L%s" % (ev["scope_first_line"],
                                                    ev["scope_last_line"]))
    print("  live    scope lines     : L%s..L%s" % (lo + 1, hi + 1))
    print("")
    print("  frozen member count     : %d" % len(fs))
    print("  live   member count     : %d" % len(ls))
    print("  ADDED (in live, not frozen)   : %d" % len(added))
    for m in added:
        print("      + %s" % m)
    print("  REMOVED (in frozen, not live) : %d" % len(removed))
    for m in removed:
        print("      - %s" % m)
    print("")
    same = not added and not removed
    print("  VERDICT: %s" % ("the 56-mod scope is INTACT - P00 conclusions still hold"
                            if same else
                            "SCOPE MEMBER SET CHANGED - P00 must be re-examined"))
    print("=" * 74)
    return 0 if same else 1


if __name__ == "__main__":
    raise SystemExit(main())
