#!/usr/bin/env python3
"""p00_common.py — shared config + MO2 modlist/priority model for P00.

READ-ONLY. Nothing in this module ever opens a file under mo2\\mods for writing.

MO2 priority model (verified against this install, do not re-derive from memory):

  * modlist.txt lists the left pane in REVERSE. modlist line 1 == the LAST
    row of the left pane == the bottom row == HIGHEST overwrite priority.
    (Corroborated by: 输出·BodySlide Output sits at line 33 and the
     `-99 工具生成输出` separator at line 36; the handbook requires the
     generator-output block to be the bottom-most block in the left pane.)
  * A separator is a HEADER. Its members are the rows BELOW it in the left
    pane, i.e. the rows with a SMALLER modlist line number.
  * Therefore: a mod belongs to the nearest separator at a LARGER modlist
    line number than the mod's own line. Equivalently, separator at line S
    owns the lines (nearest_separator_below_S + 1) .. (S - 1).
  * Leading `+` = enabled, `-` = disabled (present in modlist, absent from the
    VFS), `#` = comment. Anything else is a malformed line.

Virtual-path conflict resolution: scan the enabled mods from modlist line 1
downwards; the first mod that provides a given virtual path wins.
"""
from __future__ import annotations

import hashlib
import json
import os
import re

# ----------------------------------------------------------------- paths ----
MO2_INSTANCE = r"E:\SkyrimAE\mo2"
MO2_PROFILE = "Default"
MODLIST = os.path.join(MO2_INSTANCE, "profiles", MO2_PROFILE, "modlist.txt")
MODS_DIR = os.path.join(MO2_INSTANCE, "mods")
PLUGINS_TXT = os.path.join(MO2_INSTANCE, "profiles", MO2_PROFILE, "plugins.txt")
GAME_DATA = r"E:\SkyrimAE\Data"

PROJECT = r"E:\SkyrimAE\opencode工作目录\5-latex-wardrobe-collection"
TOOLS = os.path.join(PROJECT, "tools")
DATA = os.path.join(PROJECT, "data")
REPORTS = os.path.join(PROJECT, "reports", "P00")

# The separator this audit is scoped to, spelled WITHOUT the leading +/- state
# marker, because ModlistEntry.name is already stripped of it.
# Scope = the modlist lines with a SMALLER line number than this separator.
TARGET_SEPARATOR = "09 特殊服装与NSFW 装备_separator"

# The example mod list from the project brief, used purely as a cross-check
# that the resolved scope is the intended one (see 00_SCOPE.md).
BRIEF_EXAMPLE_HINTS = [
    "Predator", "TRX", "Zap", "AE_HoodST", "AE_VRC_Bunny_Nurse",
    "AE_Vtaw_DarkNurse", "AE_Latex_Kitty", "AE_Once_Medic",
    "AE_Stellablade_Tachy", "AE_TFD_Haley_Black_Suit", "AE_TFD_Valby_Nano",
    "AE_Toxic_Cat", "AE_Wuthering_Waves_Lupa", "SSE_Kakugo_LatexNun",
    "SSE_Latex_Nun", "SSE_VRC_Latex_Servant", "SSE_VRC_SOURYO",
    "SpearHead", "Brastia", "Angeli", "J3 Bodysuit", "J3 Latex", "Nye",
    "Latex Lover", "EvilFall", "FO4TOAEAngeli", "Silent Code",
    "Corrupted", "H2135", "Haley", "Nyes Latex",
]

SEP_RE = re.compile(r"_separator\s*$", re.IGNORECASE)


# --------------------------------------------------------------- helpers ----
def sha256_file(path: str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


class ModlistEntry:
    __slots__ = ("line_no", "state", "name", "is_separator", "raw",
                 "lower_bound_separator")

    def __init__(self, line_no: int, raw: str):
        self.line_no = line_no
        self.raw = raw
        self.lower_bound_separator = None
        if raw.startswith("+"):
            self.state = "enabled"
            name = raw[1:]
        elif raw.startswith("-"):
            self.state = "disabled"
            name = raw[1:]
        else:
            self.state = "comment"
            name = raw.lstrip("#").strip()
        self.is_separator = bool(SEP_RE.search(name))
        self.name = name

    def __repr__(self):
        return f"<ModlistEntry L{self.line_no} {self.state} {self.name!r}>"


def read_modlist(path: str = MODLIST) -> list[ModlistEntry]:
    # newline="" keeps the raw bytes visible, so CRLF must be stripped by hand;
    # leaving a trailing "\r" on every name silently breaks every filesystem
    # lookup built from it.
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        raw = fh.read()
    lines = [ln.rstrip("\r\n") for ln in raw.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return [ModlistEntry(i + 1, ln) for i, ln in enumerate(lines)]


def all_separators(entries: list[ModlistEntry]) -> list[ModlistEntry]:
    return [e for e in entries if e.is_separator]


def section_of(entries: list[ModlistEntry], entry: ModlistEntry) -> str:
    """Name of the separator block a mod belongs to (nearest separator with a
    LARGER modlist line number)."""
    best = None
    for s in all_separators(entries):
        if s.line_no > entry.line_no:
            if best is None or s.line_no < best.line_no:
                best = s
    return best.name if best else "<none>"


def resolve_scope(entries: list[ModlistEntry], separator_name: str):
    """Return (separator_entry, first_line, [member entries]) for one separator.

    separator_name is compared case-insensitively against the state-stripped
    name, so pass it WITHOUT the leading '+'/'-'.
    """
    want = separator_name.strip().lower()
    seps = [e for e in entries if e.is_separator and e.name.strip().lower() == want]
    if not seps:
        avail = "\n  ".join(sorted({e.name for e in all_separators(entries)}))
        raise SystemExit(
            f"separator not found: {separator_name!r}\navailable:\n  {avail}")
    if len(seps) > 1:
        raise SystemExit(f"separator appears {len(seps)}x: {separator_name!r}")
    sep = seps[0]
    # Members are the rows BELOW the header in the left pane. Because modlist
    # is reversed, "below in the left pane" == "smaller modlist line number".
    # The block therefore runs from just after the nearest separator that sits
    # below the header, up to sep.line_no - 1.
    below = [e for e in all_separators(entries) if e.line_no < sep.line_no]
    lower = max(below, key=lambda e: e.line_no) if below else None
    lo = (lower.line_no if lower else 1) + 1
    hi = sep.line_no - 1
    members = [e for e in entries if lo <= e.line_no <= hi
               and e.state in ("enabled", "disabled")]
    sep.lower_bound_separator = lower
    return sep, lo, members


def mod_dir(name: str) -> str:
    return os.path.join(MODS_DIR, name)


def iter_files(root: str):
    """Yield (relpath_with_forward_slashes, absolute_path, size)."""
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


# ------------------------------------------------------- body-type guessing --
BODY_TAG_RE = re.compile(r"【体型[·・]([^】]*)】")
BODY_TOKEN_RE = re.compile(r"[+/_\-]|\s+")
BODY_FAMILIES = ("CBBE", "3BA", "BHUNP", "TBD", "UNP", "HIMBO", "UBE", "SOS")
# 【体型·多体型】 means "supports several"; it says nothing specific, so it must
# NOT be treated as a real answer — fall through to the next evidence source.
GENERIC_TAGS = {"多体型", "MULTI", "MULTI BODY", "VARIOUS", "混合"}


def body_tokens(text: str) -> set:
    """Split a body-type string into an uppercased token set.

    'CBBE+3BA' -> {'CBBE','3BA'};  'BHUNP 3BBB - CBBE 3BBB' -> {'BHUNP','CBBE','3BBB'}
    Substring matching is deliberately avoided: '3BA' must not match inside
    '3BBB', and 'CBBE+3BA' must not be read as containing BHUNP.
    """
    out = set()
    for part in BODY_TOKEN_RE.split((text or "").upper()):
        for tok in (p.strip() for p in part.split()):
            if tok:
                out.add(tok)
    return out


def classify_body(tokens: set) -> tuple:
    """(body_type_guess, sorted_token_list, body_family_flag) from a token set."""
    fam = sorted(tokens & set(BODY_FAMILIES))
    has3ba = "3BA" in tokens
    hascbbe = "CBBE" in tokens
    hasbh = "BHUNP" in tokens

    if has3ba and hasbh:
        label = "3BA+BHUNP"
    elif has3ba and hascbbe:
        label = "CBBE 3BA"
    elif has3ba:
        label = "3BA"
    elif hasbh:
        label = "BHUNP"
    elif hascbbe:
        label = "CBBE"
    elif fam:
        label = fam[0]
    else:
        # '3BBB' / '2B' / no recognised token at all
        others = sorted(t for t in tokens if t.isalnum() and len(t) <= 6)
        return "unknown", fam, "UNKNOWN"

    extra = [t for t in fam if t not in ("CBBE", "3BA", "BHUNP")]
    if extra:
        label += " + " + "+".join(extra)

    if has3ba and hasbh:
        flag = "MIXED_3BA_BHUNP"
    elif hasbh:
        flag = "BHUNP_ONLY"
    elif has3ba or hascbbe:
        flag = "CBBE_3BA"
    elif fam:
        flag = "OTHER"
    else:
        flag = "UNKNOWN"
    return label, fam, flag


def body_type_from_name(name: str):
    """Evidence source 1: the structured 【体型·…】 tag on the folder name.

    Returns (label, tag, token_list, flag, source). A generic 多体型 tag or a
    missing tag falls through to the rest of the folder name.
    """
    m = BODY_TAG_RE.search(name)
    tag = (m.group(1).strip() if m else "")
    if tag and tag.upper() not in GENERIC_TAGS and "多体型" not in tag:
        toks = body_tokens(tag)
        label, fam, flag = classify_body(toks)
        if label != "unknown":
            return label, tag, fam, flag, "name_tag"

    # Evidence source 2: the whole folder name (English part often carries it).
    rest = BODY_TAG_RE.sub(" ", name)
    toks = body_tokens(rest)
    label, fam, flag = classify_body(toks)
    if label != "unknown":
        return label, tag, fam, flag, ("name_scan" if tag else "name_scan(notag)")
    return "unknown", tag, [], "UNKNOWN", "none"


def body_type_from_assets(shapedata_names, set_names):
    """Evidence source 3: BodySlide project / ShapeData names.

    Only consulted when neither the tag nor the folder name is decisive.
    """
    toks = set()
    for n in list(shapedata_names) + list(set_names):
        toks |= body_tokens(n)
    label, fam, flag = classify_body(toks)
    if label == "unknown":
        return "unknown", [], "UNKNOWN"
    return label, fam, flag


# ------------------------------------------------------------- json helper --
def write_json(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)


def read_json(path: str):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)
