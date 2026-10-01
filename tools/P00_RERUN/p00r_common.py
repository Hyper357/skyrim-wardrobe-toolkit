#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p00r_common.py — ZLJ Wardrobe Collection · P00 CLEAN RE-RUN shared core.

STRICTLY READ-ONLY with respect to the game install. Every open() in this
toolchain that is not explicitly a write is mode "rb". Write targets are
asserted to live under RERUN_ROOT and nowhere else.

Ground truth is the CURRENT MO2 profile. Scope is decided by modlist SHA256 +
separator parsing only -- mtime is never used as a scope signal, because MO2
atomically replaces modlist.txt on every exit and refreshes mtime even when the
content is byte-identical.

MO2 priority model (verified on this install, see reports/HANDOFF/):
  * modlist.txt lists the left pane in REVERSE. Line 1 = bottom row of the left
    pane = HIGHEST overwrite priority.
  * A separator is a HEADER; its members are the rows BELOW it in the left pane,
    i.e. the rows with a SMALLER modlist line number.
  * => a mod on line L belongs to the nearest separator at a LARGER line number.
  * Separator at line S owns (nearest_separator_below_S + 1) .. (S - 1).
"""
from __future__ import annotations

import csv
import datetime
import gzip
import hashlib
import json
import os
import re
import struct
import sys

# ----------------------------------------------------------------- paths ----
MO2_INSTANCE = r"E:\SkyrimAE\mo2"
MO2_PROFILE = "Default"
MODLIST = os.path.join(MO2_INSTANCE, "profiles", MO2_PROFILE, "modlist.txt")
PLUGINS_TXT = os.path.join(MO2_INSTANCE, "profiles", MO2_PROFILE, "plugins.txt")
MODS_DIR = os.path.join(MO2_INSTANCE, "mods")
GAME_DATA = r"E:\SkyrimAE\Data"

PROJECT = r"E:\SkyrimAE\opencode工作目录\5-latex-wardrobe-collection"
RERUN_ROOT = os.path.join(PROJECT, "P00_RERUN_ROOT")
TOOLS = os.path.join(PROJECT, "tools", "P00_RERUN")
DATA = os.path.join(PROJECT, "data", "P00_RERUN")
REPORTS = os.path.join(PROJECT, "reports", "P00_RERUN")

# The separator under audit. Matched by prefix so a renumber/reword of the
# prefix does not silently change scope; uniqueness is asserted downstream.
TARGET_SEPARATOR_PREFIX = "09"
TARGET_SEPARATOR_HINT = "特殊服装"

# ------------------------------------------------------------------- io -----
PLUGIN_EXT = (".esp", ".esm", ".esl", ".espfe")

# Additional write roots, opt-in and per-process. P01 needs to emit its own
# curation tables, but the guarantee that matters is that a P00 tool can never
# write outside its tree -- so P00 never calls this, and a P01 module must
# name its own directory explicitly rather than getting a blanket exemption.
_EXTRA_WRITE_ROOTS: list = []


def allow_extra_write_root(path: str) -> str:
    """Opt this process into one more writable root (used by P01 only)."""
    ap = os.path.abspath(path)
    if ap not in _EXTRA_WRITE_ROOTS:
        _EXTRA_WRITE_ROOTS.append(ap)
    return ap


def assert_write_path(path: str) -> str:
    """Fail loudly if any tool ever tries to write outside its tree."""
    ap = os.path.abspath(path)
    allowed = (os.path.abspath(DATA), os.path.abspath(REPORTS),
               os.path.abspath(TOOLS)) + tuple(_EXTRA_WRITE_ROOTS)
    if not any(ap.startswith(a + os.sep) or ap == a for a in allowed):
        raise SystemExit(f"REFUSED WRITE outside P00_RERUN tree: {ap}")
    return ap


def ensure_dirs():
    for d in (DATA, REPORTS, TOOLS):
        os.makedirs(d, exist_ok=True)


def sha256_file(path: str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def write_json(path: str, obj) -> None:
    path = assert_write_path(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def write_json_gz(path: str, obj) -> None:
    path = assert_write_path(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with gzip.open(path, "wt", encoding="utf-8", compresslevel=4) as fh:
        json.dump(obj, fh, ensure_ascii=False)


def write_csv(path: str, columns, rows) -> int:
    path = assert_write_path(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=columns, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in columns})
    os.replace(tmp, path)
    return len(rows)


def read_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


# --------------------------------------------------------------- modlist ----
class Entry:
    __slots__ = ("line_no", "state", "name", "is_sep", "raw")

    def __init__(self, line_no, raw):
        self.line_no = line_no
        self.raw = raw
        if raw.startswith("+"):
            self.state, name = "enabled", raw[1:]
        elif raw.startswith("-"):
            self.state, name = "disabled", raw[1:]
        else:
            self.state, name = "comment", raw.lstrip("#").strip()
        self.name = name
        self.is_sep = bool(re.search(r"_separator\s*$", name, re.IGNORECASE))

    def __repr__(self):
        return f"<L{self.line_no} {self.state} {self.name!r}>"


def read_modlist(path: str = MODLIST):
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        raw = fh.read()
    lines = [ln.rstrip("\r\n") for ln in raw.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return [Entry(i + 1, ln) for i, ln in enumerate(lines)]


def resolve_scope(entries, hint=TARGET_SEPARATOR_HINT, prefix=TARGET_SEPARATOR_PREFIX):
    """Resolve the target separator. Uniqueness is a hard requirement."""
    cands = [e for e in entries
             if e.is_sep and hint in e.name and e.name.strip().startswith(prefix)]
    if len(cands) != 1:
        seps = "\n  ".join(sorted(e.name for e in entries if e.is_sep))
        raise SystemExit(
            f"target separator matched {len(cands)}x (need exactly 1).\n"
            f"all separators:\n  {seps}")
    sep = cands[0]
    below = [e for e in entries if e.is_sep and e.line_no < sep.line_no]
    lower = max(below, key=lambda e: e.line_no) if below else None
    above = min((e for e in entries if e.is_sep and e.line_no > sep.line_no),
                key=lambda e: e.line_no, default=None)
    lo = (lower.line_no if lower else 0) + 1
    hi = sep.line_no - 1
    members = [e for e in entries if lo <= e.line_no <= hi
               and e.state in ("enabled", "disabled")]
    return sep, lower, above, lo, hi, members


def owner_separator(entries, line_no):
    cand = [e for e in entries if e.is_sep and e.line_no > line_no]
    return min(cand, key=lambda e: e.line_no).name if cand else "<none>"


# --------------------------------------------------------- file iteration ---
def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace("\\", "/")
            try:
                size = os.path.getsize(full)
            except OSError:
                size = -1
            yield rel, full, size


# ------------------------------------------------------------ ID helpers ----
def plugin_id(filename: str) -> str:
    return filename.lower()


def record_id(formid: int) -> str:
    return "%08X" % formid


def nif_id(vpath: str) -> str:
    return vpath.replace("/", "\\").lower()


# ---------------------------------------------------- body-type classifier --
BODY_TAG_RE = re.compile(r"【体型[·・]([^】]*)】")
# Separators used when tokenising body-type evidence out of free text.
# CORRECTED: brackets and parentheses are separators too. Without them,
# "(BHUNP)" and "[SE]3BA" never yield BHUNP / 3BA, so 6 of the 62
# family-named BodySlide projects fell through to UNKNOWN for a purely
# punctuation reason.
BODY_TOKEN_RE = re.compile(
    r"[+/_\-\[\](){}|,;·、，。；：]+"      # ascii + CJK punctuation
    r"|[【】〔〕「」『』（）〈〉《》［］]"  # CJK brackets
    r"|\s+")
BODY_FAMILIES = ("CBBE", "3BA", "BHUNP", "HIMBO", "UBE", "SOS", "TNG", "UNP",
                 "TBD", "SLIM", "VANILLA")
GENERIC_TAGS = {"多体型", "MULTI", "MULTI BODY", "VARIOUS", "混合"}


def body_tokens(text: str):
    out = set()
    for part in BODY_TOKEN_RE.split((text or "").upper()):
        for tok in (p.strip() for p in part.split()):
            if tok:
                out.add(tok)
    return out


def classify_body(tokens):
    """(candidate, families, family_flag) from a token set.

    Candidates are exactly the vocabulary the re-run brief mandates:
    CBBE / CBBE_3BA / BHUNP / OTHER / UNKNOWN

    CORRECTED (audit finding #4): a CBBE-only token set is CBBE, not OTHER.
    The first P00_RERUN pass collapsed CBBE-only to OTHER, which silently
    discarded a real body type. 3BA (with or without CBBE) is CBBE_3BA.
    """
    fam = sorted(tokens & set(BODY_FAMILIES))
    has3ba = "3BA" in tokens
    hascbbe = "CBBE" in tokens
    hasbh = "BHUNP" in tokens
    if has3ba and hasbh:
        cand, flag = "OTHER", "MIXED_3BA_BHUNP"
    elif has3ba and hascbbe:
        cand, flag = "CBBE_3BA", "CBBE_3BA"
    elif has3ba:
        cand, flag = "CBBE_3BA", "CBBE_3BA_3BA_ONLY"
    elif hasbh:
        cand, flag = "BHUNP", "BHUNP_ONLY"
    elif hascbbe:
        cand, flag = "CBBE", "CBBE_ONLY"
    elif fam:
        cand, flag = "OTHER", "OTHER"
    else:
        return "UNKNOWN", fam, "UNKNOWN"
    return cand, fam, flag


def body_candidate_from_name(name: str):
    """Evidence source 1+2: the structured 【体型·…】 tag, then the raw name."""
    m = BODY_TAG_RE.search(name)
    tag = m.group(1).strip() if m else ""
    if tag and tag.upper() not in GENERIC_TAGS and "多体型" not in tag:
        cand, fam, flag = classify_body(body_tokens(tag))
        if cand != "UNKNOWN":
            return cand, tag, fam, flag, "name_tag"
    rest = BODY_TAG_RE.sub(" ", name)
    cand, fam, flag = classify_body(body_tokens(rest))
    if cand != "UNKNOWN":
        return cand, tag, fam, flag, ("name_scan" if tag else "name_scan(notag)")
    return "UNKNOWN", tag, fam, "UNKNOWN", "none"


def body_candidate_from_assets(osp_names, shapedata_names, set_names,
                               nif_shape_names=()):
    """Evidence source 3: BodySlide project / ShapeData / OSP / OSD / NIF shape
    names. Every token must come from an actual file name or NIF shape name --
    nothing is guessed."""
    toks = set()
    for coll in (osp_names, shapedata_names, set_names, nif_shape_names):
        for n in coll or ():
            toks |= body_tokens(n)
    return classify_body(toks)


# ------------------------------------------------------------------ misc ----
def log(msg: str) -> None:
    print(f"[{datetime.datetime.now():%H:%M:%S}] {msg}", flush=True)


def stats_block(values):
    """min / median / mean / max / outlier for a numeric column."""
    vals = sorted(v for v in values
                  if isinstance(v, (int, float)) and not isinstance(v, bool))
    if not vals:
        return {}
    n = len(vals)
    med = (vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2)
    mean = sum(vals) / n
    q1 = vals[max(0, int(n * 0.25))]
    q3 = vals[min(n - 1, int(n * 0.75))]
    iqr = q3 - q1
    lo_f, hi_f = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outl = [v for v in vals if v < lo_f or v > hi_f]
    return {"min": vals[0], "median": med, "mean": round(mean, 3),
            "max": vals[-1], "n": n, "n_outlier": len(outl),
            "outliers": outl[:20]}


if __name__ == "__main__":
    ensure_dirs()
    entries = read_modlist()
    sep, lower, above, lo, hi, members = resolve_scope(entries)
    print(f"modlist sha256 : {sha256_file(MODLIST)}")
    print(f"modlist lines  : {len(entries)}")
    print(f"profile        : {MO2_PROFILE}")
    print(f"separator      : {sep.name}  (L{sep.line_no})")
    print(f"lower bound    : L{lower.line_no if lower else '-'} "
          f"{lower.name if lower else ''}")
    print(f"upper bound    : L{above.line_no if above else '-'} "
          f"{above.name if above else ''}")
    print(f"scope          : L{lo}..L{hi}  members={len(members)}")
