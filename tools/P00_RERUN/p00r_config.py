#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p00r_config.py — STAGE 14: read-only external-reference + distribution-layer
scan of every config / script / asset-text file owned by the 09 scope.

WHAT IT IS
    The 09 (特殊服装) scope is mostly meshes and ESPs, so the interesting
    question is: do any of its *configuration* files smuggle in a behaviour
    layer that the plugin records themselves do not show?  This tool answers
    that by reading every ini/json/toml/yaml/xml/txt/psc/fomod/BodySlide-text
    file in the scope and looking for

        * distribution layers  (SPID / KID / BOS / outfit-def)
        * condition layers     (OAR / DAR)
        * framework config     (SKSE / PBRNifPatcher)
        * identifiers that point OUT of the scope (plugin / FormID / EditorID)

    and then resolving every identifier against the 47 in-scope plugins and
    the 3548 parsed records already produced by p00r_plugins.py.  Anything
    that does NOT resolve is reported, not hidden -- that is the point of the
    audit.

STRICTLY READ-ONLY
    Every game/config file is opened with mode "rb" and read at most
    MAX_READ_BYTES.  modlist.txt / plugins.txt / loadorder.txt are never
    opened at all.  The only writes are the three artefacts below, all of
    which are funnelled through p00r_common.assert_write_path():

        data/P00_RERUN/14_config_refs.json
        reports/P00_RERUN/13_EXTERNAL_REFERENCES.csv
        reports/P00_RERUN/17_EXTERNAL_REFERENCES.csv

INPUTS (already computed by earlier stages -- never recomputed here)
    data/P00_RERUN/01_file_index.json.gz     gzip UTF-8 JSON list
    data/P00_RERUN/02_plugin_index.json      47 in-scope plugins
    data/P00_RERUN/02_plugin_records.json    3548 parsed records

Usage:  python tools/P00_RERUN/p00r_config.py
"""
from __future__ import annotations

import datetime
import gzip
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p00r_common as C  # noqa: E402

# ------------------------------------------------------------------ params --
SCHEMA = "P00R-14-config_refs/1"

# The categories the brief mandates for this stage.
TARGET_CATS = ("ini", "json", "toml", "yaml", "xml", "txt", "script_psc",
               "fomod", "bodyslide_other")

MAX_READ = 512 * 1024          # read at most the first 512 KB of each file
BIN_PROBE = 4096               # NUL heuristic is evaluated on the first 4 KB
BIN_NUL_MAX = 0.10             # "more than 10% NUL bytes" == binary
ENCODINGS = ("utf-8-sig", "utf-8", "utf-16", "cp1252", "latin-1")
UTF16_NUL_MAX = 0.05           # sanity guard: reject a bogus utf-16 decode

REF_SAMPLE_CAP = 200           # per-file cap on each identifier list
EV_SNIP = 140                  # max chars of matched evidence kept per hit

# ref_kind values.  The first nine are the brief's enum verbatim.  OUTFIT is
# added because the brief also mandates an "outfit def" detection and gave it
# no enum slot; dropping it would silently lose a required detection, so it is
# emitted as a tenth clearly-named value instead of being hidden.
REF_KINDS = ("SPID", "KID", "BOS", "OAR", "DAR", "SKSE", "PGPATCHER",
             "OUTFIT", "PLUGIN_REF", "FORMID_REF", "EDID_REF")
BRIEF_ENUM = REF_KINDS[:8] + ("PLUGIN_REF", "FORMID_REF", "EDID_REF")

# --------------------------------------------------------------- detection --
# (kind, rule_id, rule_class, source, pattern, strength, guard, note)
#   rule_class "brief"           -> pattern taken verbatim from the brief
#   rule_class "brief_extension" -> added because the brief's literal pattern
#                                   demonstrably misses real files in this
#                                   corpus; every such rule is labelled so the
#                                   report can be audited against both views.
#   source "content" | "path"
#   strength "strong" (explicit marker) / "medium" (format evidence) /
#             "weak" (a bare word; also fires on prose and XML comments)
#   guard    None | "json"  (only fire when file_cat == guard)
D = "content"
P = "path"
RULES = (
    # ---- SPID: distribution type (ScriptInjection / StatInjection) -----------
    ("SPID", "SPID_SECTION_SCRIPTINJECTION", "brief", D,
     r"\[\s*ScriptInjection\s*\]", "strong", None,
     "brief: 'a [ScriptInjection] ... section'"),
    ("SPID", "SPID_SECTION_STATINJECTION", "brief", D,
     r"\[\s*StatInjection\s*\]", "strong", None,
     "brief: 'a [StatInjection] ... section'"),
    ("SPID", "SPID_KEY_DISTRIBUTIONTYPE", "brief", D,
     r"(?i)(?<![\w\\])Distribution\s*\\?\s*Type", "strong", None,
     "brief: key like DistributionType / Distribution\\Type"),
    ("SPID", "SPID_KEY_ACTOR_TO_HAVE_KEYWORD", "brief", D,
     r"(?i)Actor\s*\\?\s*to\s+have\s+keyword", "strong", None,
     "brief: key like 'Actor\\ to have keyword'"),
    ("SPID", "SPID_KEY_ACTOR_ASSIGN", "brief", D,
     r"(?i)\\Actor\s*=", "strong", None,
     "brief: key like '\\Actor ='"),
    ("SPID", "SPID_KEY_DUPLICATE_ASSIGN", "brief", D,
     r"(?i)(?<![\w\\])Duplicate\s*=", "strong", None,
     "brief: key like 'Duplicate ='"),
    ("SPID", "SPID_KEY_PACKAGENAME", "brief", D,
     r"(?i)(?<![\w\\])PackageName\b", "strong", None,
     "brief: key like PackageName"),
    ("SPID", "SPID_KEY_OUTFITS_ASSIGN", "brief", D,
     r"(?i)(?<![\w\\])Outfits?\s*=", "weak", None,
     "brief: key like 'Outfit(s)'; weak because a bare word also hits prose"),
    ("SPID", "SPID_KEY_OUTFIT_KEYWORD", "brief", D,
     r"(?i)\\Outfit\\Keyword", "strong", None,
     "brief: key like '\\Outfit\\Keyword'"),
    ("SPID", "SPID_KEY_OUTFIT_FILTER", "brief", D,
     r"(?i)\\Outfit\\Filter", "strong", None,
     "brief: key like '\\Outfit\\Filter'"),

    # ---- KID: keyword injector --------------------------------------------
    ("KID", "KID_SECTION_KEYWORDINJECTOR", "brief", D,
     r"\[\s*KeywordInjector\s*\]", "strong", None,
     "brief: '[KeywordInjector]'"),
    ("KID", "KID_KEY_KEYWORDITEMDISTRIBUTION", "brief", D,
     r"KeywordItemDistribution", "strong", None,
     "brief: 'KeywordItemDistribution'"),
    ("KID", "KID_KEY_KEYWORDDISTRIBUTION", "brief", D,
     r"KeywordDistribution", "strong", None,
     "brief: 'KeywordDistribution'"),
    ("KID", "KID_LINE_KEYWORD_ASSIGN", "brief_extension", D,
     r"(?im)^[ \t]*Keyword[ \t]*=[ \t]*\S", "medium", None,
     "EXTENSION: the brief's three literal KID patterns match NOTHING in this "
     "corpus; all 5 KID files instead use the injector LINE format "
     "'Keyword = <kw>|<category>|<formids>[+<plugin>]' with no section header. "
     "This rule is what actually finds them."),
    ("KID", "KID_PATH_FILENAME_KID", "brief_extension", P,
     r"(?i)(^|/)KID\.(ini|json|cfg)$", "medium", None,
     "EXTENSION: corroborating filename hint only, not proof of behaviour."),

    # ---- BOS: base object swap --------------------------------------------
    ("BOS", "BOS_SECTION_BOS", "brief", D,
     r"\[\s*BOS\s*\]", "strong", None, "brief: '[BOS]'"),
    ("BOS", "BOS_SECTION_BASEOBJECTSWAP", "brief", D,
     r"\[\s*BaseObjectSwap\s*\]", "strong", None, "brief: '[BaseObjectSwap]'"),
    ("BOS", "BOS_PATH_OBJECTS_BOS", "brief", P,
     r"(?i)(^|/)objects/bos/", "strong", None, "brief: 'objects/bos/'"),

    # ---- OAR: Open Animation Replacer conditions --------------------------
    ("OAR", "OAR_JSON_CONDITIONS_KEY", "brief", D,
     r"(?i)[\"']conditions[\"']\s*:", "strong", "json",
     "brief: 'json with \"conditions\" key' (guarded to cat=json)"),
    ("OAR", "OAR_CONTENT_CONDITIONS_KEY", "brief_extension", D,
     r"(?i)(?<![\w])[\"']?conditions[\"']?\s*[:=]", "weak", None,
     "EXTENSION: unguarded 'conditions' key outside json; weak, also fires on "
     "prose and on unrelated config schemas."),

    # ---- DAR: Display Animation Replacer conditions -----------------------
    ("DAR", "DAR_PATH_CONDITIONS_TXT", "brief", P,
     r"(?i)(^|/)_?conditions\.txt$", "strong", None,
     "brief: 'a *_conditions.txt'"),

    # ---- SKSE: framework config -------------------------------------------
    ("SKSE", "SKSE_PATH_SKSE_DIR", "brief", P,
     r"(?i)(^|/)skse/", "strong", None,
     "brief: 'path contains /skse/'. Anchored so that a mod-root 'SKSE/' "
     "directory counts too, not only a nested '/skse/'."),

    # ---- PBRNifPatcher ----------------------------------------------------
    ("PGPATCHER", "PGP_PATH_PBRNIFPATCHER", "brief", P,
     r"(?i)(^|/)pbrnifpatcher/", "strong", None,
     "brief: 'path contains pbrnifpatcher/'"),
    ("PGPATCHER", "PGP_JSON_RULE_KEY", "brief", D,
     r"(?i)[\"']rule[\"']\s*:", "strong", "json",
     "brief: 'the json has \"rule\"' (guarded to cat=json)"),

    # ---- outfit def --------------------------------------------------------
    ("OUTFIT", "OUTFIT_PATH_FILENAME", "brief", P,
     r"(?i)outfit", "strong", None,
     "brief: 'a filename ... match for outfit / outfit_'. NOTE: a physics "
     "bone-constraint xml can be NAMED outfit without being an outfit def."),
    ("OUTFIT", "OUTFIT_CONTENT_SECTION", "brief", D,
     r"(?im)^[ \t]*[\[<]\s*outfit|[\"']outfit[\"']\s*:", "strong", None,
     "brief: '\"outfit\" section' -- section header or json key."),
    ("OUTFIT", "OUTFIT_CONTENT_WORD", "brief", D,
     r"(?i)\boutfits?\b", "weak", None,
     "brief: 'content match for outfit'. WEAK: RealPhysics xml files carry a "
     "literal '<!-- Outfits -->' comment, so this fires on non-config text."),
)

# ------------------------------------------------------------- identifiers --
# plugin filename as a bare token: no spaces, no path separator
RE_PLUGIN_BARE = re.compile(
    r"(?<![A-Za-z0-9_.\-])"
    r"([A-Za-z0-9_][A-Za-z0-9_.\-]{0,63}\.(?:esp|esm|esl|espfe))"
    r"(?![A-Za-z0-9_])", re.IGNORECASE)
# plugin filename that legitimately contains a single space, e.g. "Heels Sound.esm"
RE_PLUGIN_SPACED = re.compile(
    r"(?<![A-Za-z0-9_.\-])"
    r"([A-Za-z0-9_][A-Za-z0-9_.\-]{2,40}(?: [A-Za-z0-9_][A-Za-z0-9_.\-]{2,40})?"
    r"\.(?:esp|esm|esl|espfe))"
    r"(?![A-Za-z0-9_])", re.IGNORECASE)
# 8-hex-digit FormID token, hex-boundary delimited
RE_FORMID = re.compile(r"(?<![0-9A-Fa-f])([0-9A-Fa-f]{8})(?![0-9A-Fa-f])")
# EditorID-shaped token: conservative -- starts with a letter, alnum+underscore
# only, 4..80 chars, no dot / no path separator / no space.
RE_EDID = re.compile(r"(?<![A-Za-z0-9_])([A-Za-z][A-Za-z0-9_]{2,78}[A-Za-z0-9])"
                     r"(?![A-Za-z0-9_])")
HEXISH = set("0123456789abcdefABCDEF")
# the injector line format, parsed structurally for evidence
RE_KID_LINE = re.compile(r"^[ \t]*Keyword[ \t]*=[ \t]*(\S.*?)[ \t]*$",
                         re.IGNORECASE | re.MULTILINE)
RE_SCRIPTISH = re.compile(
    r"(?i)(?:^|[\s\[\]<\"'()/\\])scripts?(?:ing)?\b")
RE_URL_HEAD = re.compile(r"(?i)\bhttps?://[^\s\"'<>]*$")
RE_XML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
# An http(s) URL is still running when one of these appears; a plugin token
# inside a URL is prose, not a dependency.
PROSE_MARKERS = ("nexusmods.com", "/users/", "skyrimspecialedition",
                 "specialedition/users", "images/", "mods/")

# A spaced plugin filename ("Heels Sound.esm") is real, but only when the
# leading word is part of the name.  "with Skyrim.esm" is prose.  These are the
# lowercase English words that showed up as false leaders in this corpus.
PROSE_LEADERS = {
    "with", "and", "use", "uses", "using", "install", "installed", "require",
    "requires", "required", "master", "masters", "from", "by", "the", "a",
    "an", "is", "are", "in", "on", "to", "for", "of", "plus", "or", "see",
    "via", "this", "that", "after", "before", "when", "while", "into", "out",
    "up", "down", "over", "under", "no", "not", "only", "also", "if", "as",
}


def url_context(text: str, start: int) -> bool:
    """True when the token at `start` sits inside an http(s) URL."""
    head = text[max(0, start - 200):start]
    if not RE_URL_HEAD.search(head):
        return False
    tail = text[max(0, start - 200):start].lower()
    return any(m in tail for m in PROSE_MARKERS)


def ref_context(text: str, start: int, name: str, rel: str) -> str:
    """Classify WHERE an extracted identifier token sits in its file.

    A plugin token in a Nexus description ("Merged the three plugins with
    Skyrim.esm as only master") is prose, not a load-order dependency, and the
    auditor needs to be able to tell the two apart.
    """
    if url_context(text, start):
        return "prose_url"
    low = rel.lower()
    if name.lower() in ("meta.ini", "desktop.ini") or \
            low.endswith(("readme.txt", "readme.md", "changelog.txt")):
        return "mod_metadata_prose"
    if in_spans(comment_spans(text), start):
        return "xml_comment"
    return "config_directive"


def comment_spans(text: str):
    return [(m.start(), m.end()) for m in RE_XML_COMMENT.finditer(text)]


def in_spans(spans, pos: int) -> bool:
    return any(a <= pos < b for a, b in spans)


def snip(s: str) -> str:
    s = re.sub(r"\s+", " ", s or "").strip()
    return s[:EV_SNIP] + ("..." if len(s) > EV_SNIP else "")


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def decode(blob: bytes):
    """Decode with the brief's fixed codec order; returns (text, encoding)."""
    for enc in ENCODINGS:
        try:
            txt = blob.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
        if enc.startswith("utf-16") and txt[:BIN_PROBE].count("\x00") > \
                BIN_PROBE * UTF16_NUL_MAX:
            # a random byte blob almost always "decodes" as utf-16; reject it
            continue
        return txt, enc
    return blob.decode("latin-1", "replace"), "latin-1(replace)"


def is_binary(head: bytes) -> bool:
    if not head:
        return False
    return (head.count(b"\x00") / len(head)) > BIN_NUL_MAX


def edid_shape(tok: str) -> str:
    """Cheap, honest confidence tag for an EDID-shaped token.

    Skyrim EditorIDs in this corpus are overwhelmingly either an ALLCAPS keyword
    (ORF_Sexy, SLA_KillerHeels) or a 2+ uppercase-letter prefix followed by
    MixedCase segments (SSE_TFD_Haley_Black_Suit, AE_Latex_Kitty_Body).  A
    MixedCase token that does NOT start with such a prefix is, in this corpus,
    overwhelmingly a Havok bone name, a desktop.ini parameter or a texture-map
    key -- reported, but tagged low confidence.
    """
    if tok.isupper():
        return "ALLCAPS_UNDERSCORE_keywordlike"
    head = tok.split("_", 1)[0]
    if len(head) >= 2 and head.isupper() and head.isalpha():
        return "UpperPrefix_MixedCase_edidlike"
    return "MixedCase_LOWCONF_not_an_edid"


def resolve_sets():
    with open(os.path.join(C.DATA, "02_plugin_index.json"),
              encoding="utf-8") as fh:
        plugins = json.load(fh)
    with open(os.path.join(C.DATA, "02_plugin_records.json"),
              encoding="utf-8") as fh:
        records = json.load(fh)

    in_scope_plugin = {}
    for p in plugins:
        in_scope_plugin[C.plugin_id(p["PLUGIN_ID"])] = {
            "PLUGIN_ID": C.plugin_id(p["PLUGIN_ID"]),
            "plugin_file": p.get("plugin_file"),
            "source_mod": p.get("source_mod"),
            "enabled": p.get("enabled"),
        }

    formid_to = {}
    edid_to = {}
    for r in records:
        fid = (r.get("formid") or "").upper()
        if fid:
            formid_to.setdefault(fid, []).append(
                {"record_type": r.get("record_type"),
                 "plugin_file": r.get("plugin_file"),
                 "PLUGIN_ID": C.plugin_id(r.get("plugin_file") or "")})
        for ed in (r.get("subrecords") or {}).get("EDID", []) or []:
            if isinstance(ed, str) and ed:
                edid_to.setdefault(ed, []).append(
                    {"record_type": r.get("record_type"),
                     "plugin_file": r.get("plugin_file"),
                     "PLUGIN_ID": C.plugin_id(r.get("plugin_file") or ""),
                     "formid": fid})
    return in_scope_plugin, formid_to, edid_to


def path_of(rec) -> str:
    """Absolute path of an indexed file. Read-only; never written."""
    return os.path.join(C.MODS_DIR, rec["mod"],
                        rec["rel"].replace("/", os.sep))


def scan_file(rec, in_scope_plugin, formid_to, edid_to, file_id):
    """Read one file with mode 'rb' and return its analysis record."""
    rel, vpath, cat = rec["rel"], rec["vpath"], rec["cat"]
    name = os.path.basename(rel)
    out = {
        "file_id": file_id,
        "source_mod": rec["mod"],
        "rel": rel,
        "vpath": vpath,
        "abspath": path_of(rec),
        "file_cat": cat,
        "size": rec.get("size"),
        "sha256": rec.get("sha256"),
        "is_binary": False,
        "encoding": None,
        "read_bytes": 0,
        "truncated": False,
        "parse_note": "",
        "detections": [],
        "plugin_refs": [],
        "formid_refs": [],
        "edid_refs": [],
        "counts": {},
    }

    full = out["abspath"]
    if not os.path.isfile(full):
        out["parse_note"] = "MISSING_ON_DISK"
        out["counts"] = dict(n_plugin_refs=0, n_formid_refs=0, n_edid_refs=0,
                             n_unresolved_plugin_refs=0,
                             n_unresolved_formid_refs=0,
                             n_unresolved_edid_refs=0, n_detections=0)
        return out

    try:
        with open(full, "rb") as fh:               # READ-ONLY, mode "rb"
            blob = fh.read(MAX_READ)
    except OSError as e:
        out["parse_note"] = f"READ_ERROR:{type(e).__name__}"
        out["counts"] = dict(n_plugin_refs=0, n_formid_refs=0, n_edid_refs=0,
                             n_unresolved_plugin_refs=0,
                             n_unresolved_formid_refs=0,
                             n_unresolved_edid_refs=0, n_detections=0)
        return out

    out["read_bytes"] = len(blob)
    out["truncated"] = bool(rec.get("size", 0) > len(blob))

    if is_binary(blob[:BIN_PROBE]):
        out["is_binary"] = True
        out["parse_note"] = (f"BINARY_SKIPPED(nul>{int(BIN_NUL_MAX*100)}% in "
                             f"first {BIN_PROBE}B; not parsed)")
        out["counts"] = dict(n_plugin_refs=0, n_formid_refs=0, n_edid_refs=0,
                             n_unresolved_plugin_refs=0,
                             n_unresolved_formid_refs=0,
                             n_unresolved_edid_refs=0, n_detections=0)
        return out

    text, enc = decode(blob)
    out["encoding"] = enc
    notes = [f"enc={enc}", f"read={len(blob)}B"]
    if out["truncated"]:
        notes.append(f"TRUNCATED(file {rec.get('size')}B > {MAX_READ}B cap)")

    # ------------------------------------------------------------ detections
    dets = out["detections"]
    spans = comment_spans(text)
    seen = set()
    for kind, rule_id, rule_class, source, pattern, strength, guard, note in RULES:
        if guard and cat != guard:
            continue
        subject = text if source == D else vpath.replace("\\", "/")
        rx = re.compile(pattern, re.IGNORECASE if "(?i)" not in pattern else 0)
        m = rx.search(subject)
        if not m:
            continue
        key = (kind, rule_id)
        if key in seen:
            continue
        seen.add(key)
        n_hits = len(rx.findall(subject))
        ev = snip(m.group(0))
        ctx = ""
        if source == D:
            pos = m.start()
            ev = f"L{line_of(text, pos)}: {ev}"
            # Where did a weak match actually land?  This is the difference
            # between "this config declares an outfit" and "this file contains
            # the word 'Outfits' in an XML comment or a Nexus description".
            if strength == "weak":
                if in_spans(spans, pos):
                    ctx = "xml_comment"
                elif url_context(text, pos):
                    ctx = "prose_url"
                elif name.lower() in ("meta.ini", "desktop.ini") or \
                        rel.lower().endswith(("readme.txt", "readme.md")):
                    ctx = "mod_metadata_prose"
                else:
                    ctx = "plain_text"
        dets.append({
            "kind": kind, "rule": rule_id, "rule_class": rule_class,
            "source": source, "strength": strength, "context_class": ctx,
            "n_matches": n_hits, "evidence": ev, "note": note,
        })

    # structural parse of the injector line format, when present
    kid_lines = []
    for m in RE_KID_LINE.finditer(text):
        parts = [p.strip() for p in m.group(1).split("|")]
        entry = {"line": line_of(text, m.start()), "raw": snip(m.group(1))}
        if len(parts) >= 3:
            entry["keywords"] = [k.strip() for k in parts[0].split(",")
                                 if k.strip()]
            entry["category"] = parts[1]
            entry["targets"] = snip(parts[2])
        kid_lines.append(entry)
    if kid_lines:
        out["kid_lines"] = kid_lines
        notes.append(f"injector_lines={len(kid_lines)}")

    # ----------------------------------------------------------- identifiers
    # plugin refs.  The spaced variant is matched FIRST and is then protected
    # two ways: its accepted SPANS are excluded from the bare pass (same
    # occurrence) and its accepted NAMES are excluded from the bare pass too
    # (a later "- Heels Sound.esm" line would otherwise contribute the
    # fragment "Sound.esm").
    seen_plug, taken_spans, spaced_names = {}, [], set()
    for m in RE_PLUGIN_SPACED.finditer(text):
        val = m.group(1)
        first = val.split(" ")[0].lower()
        if first in PROSE_LEADERS:
            continue                       # "with Skyrim.esm" is prose
        key = C.plugin_id(val)
        if key in seen_plug:
            continue
        taken_spans.append(m.span())
        spaced_names.add(key)
        hit = in_scope_plugin.get(key)
        seen_plug[key] = {
            "value": val, "PLUGIN_ID": key, "rule": "PLUGIN_SPACED_TOKEN",
            "line": line_of(text, m.start()),
            "context_class": ref_context(text, m.start(), name, rel),
            "resolves_in_scope_plugin": "yes" if hit else "no",
            "resolves_to": (f"{hit['source_mod']} :: {hit['plugin_file']}"
                            if hit else ""),
        }
    for m in RE_PLUGIN_BARE.finditer(text):
        if any(a <= m.start() < b for a, b in taken_spans):
            continue
        val = m.group(1)
        key = C.plugin_id(val)
        if key in seen_plug:
            continue
        if any(s.endswith(key) and len(key) < len(s) for s in spaced_names):
            continue                       # "Sound.esm" inside "Heels Sound.esm"
        hit = in_scope_plugin.get(key)
        seen_plug[key] = {
            "value": val, "PLUGIN_ID": key, "rule": "PLUGIN_BARE_TOKEN",
            "line": line_of(text, m.start()),
            "context_class": ref_context(text, m.start(), name, rel),
            "resolves_in_scope_plugin": "yes" if hit else "no",
            "resolves_to": (f"{hit['source_mod']} :: {hit['plugin_file']}"
                            if hit else ""),
        }
    out["plugin_refs"] = [seen_plug[k] for k in sorted(seen_plug)]

    # FormID refs
    seen_f = {}
    for m in RE_FORMID.finditer(text):
        val = m.group(1).upper()
        if val not in seen_f:
            seen_f[val] = (m.start(), ref_context(text, m.start(), name, rel))
    flist = sorted(seen_f)[:REF_SAMPLE_CAP]
    fdrop = len(seen_f) - len(flist)
    if fdrop:
        notes.append(f"formid_sample_truncated={fdrop}")
    for val in flist:
        pos, ctxt = seen_f[val]
        hit = formid_to.get(val)
        out["formid_refs"].append({
            "value": val, "rule": "FORMID_8HEX_TOKEN",
            "line": line_of(text, pos),
            "context_class": ctxt,
            "in_url_prose": "yes" if ctxt == "prose_url" else "no",
            "resolves_in_scope_record": "yes" if hit else "no",
            "resolves_to": (f"{hit[0]['plugin_file']} :: {hit[0]['record_type']} "
                            f":: {val}" if hit else ""),
        })

    # EditorID-shaped refs
    seen_e = {}
    for m in RE_EDID.finditer(text):
        tok = m.group(1)
        if "_" not in tok:
            continue
        if all(c in HEXISH for c in tok):
            continue                      # that is a FormID, not an EDID
        if tok not in seen_e:
            seen_e[tok] = m.start()
    elist = sorted(seen_e)[:REF_SAMPLE_CAP]
    edrop = len(seen_e) - len(elist)
    if edrop:
        notes.append(f"edid_sample_truncated={edrop}")
    for tok in elist:
        hit = edid_to.get(tok)
        ctxt = ref_context(text, seen_e[tok], name, rel)
        out["edid_refs"].append({
            "value": tok, "rule": "EDID_SHAPE_TOKEN",
            "shape": edid_shape(tok),
            "line": line_of(text, seen_e[tok]),
            "context_class": ctxt,
            "in_url_prose": "yes" if ctxt == "prose_url" else "no",
            "resolves_in_scope_edid": "yes" if hit else "no",
            "resolves_to": (f"{hit[0]['plugin_file']} :: {hit[0]['record_type']} "
                            f":: {hit[0]['formid']}" if hit else ""),
        })

    n_up = sum(1 for r in out["plugin_refs"]
               if r["resolves_in_scope_plugin"] == "no")
    n_uf = sum(1 for r in out["formid_refs"]
               if r["resolves_in_scope_record"] == "no")
    n_ue = sum(1 for r in out["edid_refs"]
               if r["resolves_in_scope_edid"] == "no")
    out["counts"] = {
        "n_plugin_refs": len(out["plugin_refs"]),
        "n_formid_refs": len(out["formid_refs"]),
        "n_edid_refs": len(out["edid_refs"]),
        "n_unresolved_plugin_refs": n_up,
        "n_unresolved_formid_refs": n_uf,
        "n_unresolved_edid_refs": n_ue,
        "n_detections": len(dets),
    }
    out["has_scripts"] = bool(
        cat == "script_psc" or RE_SCRIPTISH.search(text) or
        any(d["kind"] == "SPID" for d in dets))
    # A "distribution layer" has to be a real declaration.  A bare occurrence
    # of the word "outfit" inside a RealPhysics "<!-- Outfits -->" comment or a
    # Nexus description is NOT a layer, so only strong/medium detections count.
    out["has_distribution_layer"] = any(
        d["kind"] in ("SPID", "KID", "BOS", "OUTFIT") and d["strength"] != "weak"
        for d in dets)
    out["has_weak_word_match_only"] = bool(
        dets and not out["has_distribution_layer"] and
        any(d["strength"] == "weak" for d in dets))
    out["has_conditions"] = bool(
        any(d["kind"] in ("OAR", "DAR") for d in dets))
    out["parse_note"] = "; ".join(notes)
    return out


def rule_ledger():
    return [{"kind": k, "rule": r, "rule_class": cc, "source": s,
             "pattern": p, "strength": st, "guard": g, "note": nt}
            for k, r, cc, s, p, st, g, nt in RULES]


def main() -> int:
    C.ensure_dirs()

    with gzip.open(os.path.join(C.DATA, "01_file_index.json.gz"), "rt",
                   encoding="utf-8") as fh:
        index = json.load(fh)
    C.log(f"loaded file index: {len(index)} files")

    in_scope_plugin, formid_to, edid_to = resolve_sets()
    C.log(f"resolution sets: {len(in_scope_plugin)} in-scope plugins, "
          f"{len(formid_to)} formids, {len(edid_to)} editorids")

    selected = [r for r in index if r.get("cat") in TARGET_CATS]
    selected.sort(key=lambda r: (r["mod"].lower(), r["rel"].lower()))
    C.log(f"config-class files in scope: {len(selected)}")

    files, rows13, rows17 = [], [], []
    seq = 0
    n_binary = n_missing = n_error = 0

    for i, rec in enumerate(selected, start=1):
        file_id = f"F{i:05d}"
        info = scan_file(rec, in_scope_plugin, formid_to, edid_to, file_id)
        files.append(info)

        if info["is_binary"]:
            n_binary += 1
        if info["parse_note"].startswith("MISSING"):
            n_missing += 1
        if info["parse_note"].startswith("READ_ERROR"):
            n_error += 1

        dets = info["detections"]
        cn = info["counts"]
        plugin_n, formid_n, edid_n = (cn["n_plugin_refs"], cn["n_formid_refs"],
                                      cn["n_edid_refs"])

        def ref_resolves():
            tot = plugin_n + formid_n + edid_n
            res = (plugin_n - cn["n_unresolved_plugin_refs"]) + \
                  (formid_n - cn["n_unresolved_formid_refs"]) + \
                  (edid_n - cn["n_unresolved_edid_refs"])
            if tot == 0:
                return None
            return "yes" if res == tot else ("no" if res == 0 else "partial")

        # ---- CSV 13 : one row per detection, one row per identifier -------
        for d in dets:
            seq += 1
            agg = ref_resolves()
            # A weak match (a bare word in prose, an XML comment) carries no
            # identifier at all, so it can neither resolve nor fail to.  Say
            # so explicitly instead of letting it read as a failed lookup.
            no_id = (d["strength"] == "weak" and agg is None)
            if no_id:
                agg, rt = "partial", ""
                nhead = "weak_evidence_nothing_to_resolve"
            else:
                rt = (f"file-level refs: "
                      f"{plugin_n - cn['n_unresolved_plugin_refs']}"
                      f"/{plugin_n} plugin, "
                      f"{formid_n - cn['n_unresolved_formid_refs']}"
                      f"/{formid_n} formid, "
                      f"{edid_n - cn['n_unresolved_edid_refs']}"
                      f"/{edid_n} edid resolved")
                nhead = ""
            rows13.append({
                "ref_id": f"R{seq:06d}",
                "source_mod": info["source_mod"],
                "source_file": info["rel"],
                "file_cat": info["file_cat"],
                "ref_kind": d["kind"],
                "ref_value": d["evidence"],
                "rule": d["rule"],
                "resolves": agg or "partial",
                "resolves_to": rt,
                "note": (f"[{d['rule_class']}/{d['strength']}/"
                         f"{d['source']}match x{d['n_matches']}"
                         f"{'/' + d['context_class'] if d['context_class'] else ''}"
                         f"] {nhead} {d['note']}"),
            })

        ctx = "; ".join(sorted({d["kind"] for d in dets})) or "no_detection_ctx"
        for p in info["plugin_refs"]:
            seq += 1
            rows13.append({
                "ref_id": f"R{seq:06d}", "source_mod": info["source_mod"],
                "source_file": info["rel"], "file_cat": info["file_cat"],
                "ref_kind": "PLUGIN_REF", "ref_value": p["value"],
                "rule": p["rule"],
                "resolves": "yes" if p["resolves_in_scope_plugin"] == "yes"
                            else "no",
                "resolves_to": p["resolves_to"],
                "note": f"L{p['line']}; detection_ctx={ctx}; "
                        f"context={p['context_class']}; "
                        f"resolves_in_scope_plugin="
                        f"{p['resolves_in_scope_plugin']}",
            })
        for f in info["formid_refs"]:
            seq += 1
            rows13.append({
                "ref_id": f"R{seq:06d}", "source_mod": info["source_mod"],
                "source_file": info["rel"], "file_cat": info["file_cat"],
                "ref_kind": "FORMID_REF", "ref_value": f["value"],
                "rule": f["rule"],
                "resolves": "yes" if f["resolves_in_scope_record"] == "yes"
                            else "no",
                "resolves_to": f["resolves_to"],
                "note": f"L{f['line']}; detection_ctx={ctx}; bare 8-hex token; "
                        f"context={f['context_class']}; "
                        f"resolves_in_scope_record="
                        f"{f['resolves_in_scope_record']}",
            })
        for e in info["edid_refs"]:
            seq += 1
            rows13.append({
                "ref_id": f"R{seq:06d}", "source_mod": info["source_mod"],
                "source_file": info["rel"], "file_cat": info["file_cat"],
                "ref_kind": "EDID_REF", "ref_value": e["value"],
                "rule": e["rule"],
                "resolves": "yes" if e["resolves_in_scope_edid"] == "yes"
                            else "no",
                "resolves_to": e["resolves_to"],
                "note": f"L{e['line']}; detection_ctx={ctx}; shape="
                        f"{e['shape']}; context={e['context_class']}; "
                        f"resolves_in_scope_edid={e['resolves_in_scope_edid']}",
            })

        # ---- CSV 17 : one row per config file ------------------------------
        rows17.append({
            "file_id": file_id,
            "source_mod": info["source_mod"],
            "vpath": info["vpath"],
            "file_cat": info["file_cat"],
            "size": info["size"],
            "sha256": info["sha256"],
            "is_binary": "yes" if info["is_binary"] else "no",
            "has_distribution_layer": "yes" if info.get(
                "has_distribution_layer") else "no",
            "has_scripts": "yes" if info.get("has_scripts") else "no",
            "has_conditions": "yes" if info.get("has_conditions") else "no",
            "n_plugin_refs": plugin_n,
            "n_formid_refs": formid_n,
            "n_edid_refs": edid_n,
            "n_unresolved_plugin_refs": cn["n_unresolved_plugin_refs"],
            "n_unresolved_formid_refs": cn["n_unresolved_formid_refs"],
            "parse_note": info["parse_note"],
        })

    # ------------------------------------------------------------- summary --
    DET_KINDS = ("SPID", "KID", "BOS", "OAR", "DAR", "SKSE", "PGPATCHER",
                 "OUTFIT")
    det_files = {k: set() for k in DET_KINDS}
    det_hits = {k: 0 for k in DET_KINDS}
    det_by_rule = {}
    det_by_context = {}
    for info in files:
        for d in info["detections"]:
            det_files[d["kind"]].add(info["file_id"])
            det_hits[d["kind"]] += d["n_matches"]
            if d["context_class"]:
                det_by_context[d["context_class"]] = \
                    det_by_context.get(d["context_class"], 0) + d["n_matches"]
            det_by_rule.setdefault(d["rule"], {
                "kind": d["kind"], "rule": d["rule"],
                "rule_class": d["rule_class"], "strength": d["strength"],
                "files": set(), "matches": 0})
            det_by_rule[d["rule"]]["files"].add(info["file_id"])
            det_by_rule[d["rule"]]["matches"] += d["n_matches"]

    all_plug = [p for i in files for p in i["plugin_refs"]]
    all_form = [f for i in files for f in i["formid_refs"]]
    all_edid = [e for i in files for e in i["edid_refs"]]

    def agg(rows, key):
        res = [r for r in rows if r[key] == "yes"]
        unres = [r for r in rows if r[key] != "yes"]
        return {"total": len(rows), "resolved": len(res),
                "unresolved": len(unres),
                "distinct_resolved": sorted({r["value"] for r in res}),
                "distinct_unresolved": sorted({r["value"] for r in unres})}

    unres_plug = agg(all_plug, "resolves_in_scope_plugin")
    unres_form = agg(all_form, "resolves_in_scope_record")
    unres_edid = agg(all_edid, "resolves_in_scope_edid")

    def in_url(rows, key):
        return sum(1 for r in rows if r.get("in_url_prose") == "yes")

    brief_only = {}
    for k in DET_KINDS:
        brief_only[k] = {
            "brief_rules_only": sum(
                1 for i in files for d in i["detections"]
                if d["kind"] == k and d["rule_class"] == "brief"),
            "with_brief_extension": sum(
                1 for i in files for d in i["detections"]
                if d["kind"] == k and d["rule_class"] == "brief_extension"),
            "files_brief_rules_only": sorted({
                i["file_id"] for i in files for d in i["detections"]
                if d["kind"] == k and d["rule_class"] == "brief"}),
        }

    summary = {
        "files_in_scope": len(selected),
        "files_listed": len(files),
        "files_parsed": sum(1 for i in files if not i["is_binary"]),
        "files_binary_skipped": n_binary,
        "files_binary_skipped_list": sorted(
            f"{i['source_mod']} :: {i['rel']}" for i in files
            if i["is_binary"]),
        "files_missing_on_disk": n_missing,
        "files_read_error": n_error,
        "files_with_any_detection": sum(
            1 for i in files if i["detections"]),
        "files_with_distribution_layer": sum(
            1 for i in files if i.get("has_distribution_layer")),
        "files_with_weak_word_match_only": sum(
            1 for i in files if i.get("has_weak_word_match_only")),
        "files_with_scripts": sum(1 for i in files if i.get("has_scripts")),
        "files_with_conditions": sum(1 for i in files
                                     if i.get("has_conditions")),
        "detection_files_by_kind": {k: len(det_files[k]) for k in DET_KINDS},
        "detection_hits_by_kind": {k: v for k, v in det_hits.items() if v},
        "detection_hits_by_rule": {r: v["matches"]
                                   for r, v in sorted(det_by_rule.items())},
        "detection_weak_hits_by_context": dict(sorted(det_by_context.items())),
        "brief_vs_extension": brief_only,
        "plugin_refs": dict({kk: vv for kk, vv in unres_plug.items()
                             if not kk.startswith("distinct_")},
                            n_inside_http_url=in_url(all_plug, "value")),
        "formid_refs": dict({kk: vv for kk, vv in unres_form.items()
                             if not kk.startswith("distinct_")},
                            n_inside_http_url=in_url(all_form, "value"),
                            n_resolvable_pattern=sum(
                                1 for i in files for r in i["formid_refs"]
                                if r["in_url_prose"] == "no")),
        "edid_refs": dict({kk: vv for kk, vv in unres_edid.items()
                           if not kk.startswith("distinct_")},
                          n_inside_http_url=in_url(all_edid, "value")),
        "edid_shape_breakdown": {
            s: sum(1 for e in all_edid if e["shape"] == s)
            for s in sorted({e["shape"] for e in all_edid})},
    }

    doc = {
        "schema": SCHEMA,
        "generated_utc": datetime.datetime.now(datetime.timezone.utc)
                         .isoformat(timespec="seconds"),
        "tool": os.path.basename(__file__),
        "read_only_note": (
            "Every scanned file is opened with mode 'rb' and read at most "
            f"{MAX_READ} bytes. modlist.txt / plugins.txt / loadorder.txt are "
            "never opened. The only writes are 14_config_refs.json, "
            "13_EXTERNAL_REFERENCES.csv and 17_EXTERNAL_REFERENCES.csv, all "
            "funnelled through p00r_common.assert_write_path()."),
        "scope": {
            "separator_prefix": C.TARGET_SEPARATOR_PREFIX,
            "separator_hint": C.TARGET_SEPARATOR_HINT,
            "mo2_instance": C.MO2_INSTANCE,
            "mo2_profile": C.MO2_PROFILE,
            "mods_dir": C.MODS_DIR,
            "mod_count_in_config_files": len({i["source_mod"]
                                              for i in files}),
        },
        "inputs": {
            "01_file_index.json.gz": len(index),
            "02_plugin_index.json": len(in_scope_plugin),
            "02_plugin_records.json": len(formid_to),
            "02_plugin_records_edids": len(edid_to),
        },
        "params": {
            "target_cats": list(TARGET_CATS),
            "max_read_bytes": MAX_READ,
            "binary_probe_bytes": BIN_PROBE,
            "binary_nul_max": BIN_NUL_MAX,
            "encodings_tried_in_order": list(ENCODINGS),
            "utf16_nul_guard": UTF16_NUL_MAX,
            "ref_sample_cap_per_file": REF_SAMPLE_CAP,
            "abspath_template": "os.path.join(MODS_DIR, rec['mod'], "
                                "rec['rel'].replace('/', os.sep))",
        },
        "schema_notes": {
            "ref_kind_enum_used": list(REF_KINDS),
            "ref_kind_enum_from_brief": list(BRIEF_ENUM),
            "deviation": (
                "OUTFIT is a 10th ref_kind, not in the brief's enum. The brief "
                "mandates an 'outfit def' detection but gives it no ref_kind "
                "slot; emitting it under a clearly named value is preferred "
                "over silently dropping a required detection."),
            "resolves_semantics": {
                "PLUGIN_REF / FORMID_REF / EDID_REF":
                    "yes = resolves against 02_plugin_index / "
                    "02_plugin_records, no = does not.",
                "detection rows (SPID/KID/BOS/OAR/DAR/SKSE/PGPATCHER/OUTFIT)":
                    "yes/partial/no describe the FILE's own identifier set "
                    "(are all extracted refs resolved, some, or none). A weak "
                    "detection with no extractable identifier is reported as "
                    "partial with resolves_to empty and the note prefixed "
                    "weak_evidence_nothing_to_resolve -- it is not a failed "
                    "lookup, there was simply nothing to look up.",
            },
            "rule_class": {
                "brief": "pattern taken verbatim from the brief",
                "brief_extension": "added because the brief's literal pattern "
                                   "matched nothing in this corpus; every "
                                   "such rule is labelled in "
                                   "detection_hits_by_rule and "
                                   "brief_vs_extension",
            },
            "context_class": (
                "for weak content detections, WHERE the match landed: "
                "xml_comment (inside <!-- -->), prose_url (inside an http(s) "
                "URL), mod_metadata_prose (meta.ini / desktop.ini / README), "
                "plain_text. This is what separates a real declaration from a "
                "stray word."),
            "in_url_prose": (
                "for identifier rows, marks tokens extracted from inside an "
                "http(s) URL. In this corpus every 8-hex token found is a "
                "Nexus Mods user id or image hash in a meta.ini description, "
                "i.e. prose, not a FormID reference."),
            "has_distribution_layer":
                "yes when a STRONG or MEDIUM SPID / KID / BOS / OUTFIT "
                "detection fired. Weak bare-word matches do NOT count: the "
                "literal '<!-- Outfits -->' comment that every RealPhysics "
                "bone-constraint xml carries is a structural comment, not a "
                "distribution layer. Files whose only evidence is a weak word "
                "are flagged has_weak_word_match_only in the JSON instead.",
            "has_conditions": "yes when any OAR / DAR detection fired.",
            "has_scripts": "yes when cat==script_psc, or a script-ish token "
                           "appears in the text, or an SPID rule fired.",
            "edid_shape": (
                "ALLCAPS_UNDERSCORE_keywordlike = ORF_Sexy, SLA_KillerHeels. "
                "UpperPrefix_MixedCase_edidlike = SSE_TFD_Haley_Black_Suit, "
                "AE_Latex_Kitty_Body -- the EditorID convention this corpus "
                "actually uses. MixedCase_LOWCONF_not_an_edid = a Havok bone "
                "name, a desktop.ini parameter or a texture-map key: reported "
                "but low confidence."),
        },
        "detection_rules": rule_ledger(),
        "summary": summary,
        "in_scope_plugins": sorted(in_scope_plugin),
        "unresolved_index": {
            "note": "distinct unresolved values; this is the audit payload.",
            "plugin": unres_plug["distinct_unresolved"],
            "formid": unres_form["distinct_unresolved"],
            "edid": unres_edid["distinct_unresolved"][:400],
            "edid_distinct_unresolved_total": len(unres_edid["distinct_unresolved"]),
        },
        "resolved_index": {
            "plugin": unres_plug["distinct_resolved"],
            "formid": unres_form["distinct_resolved"],
            "edid": unres_edid["distinct_resolved"],
        },
        "files": files,
    }

    out_json = os.path.join(C.DATA, "14_config_refs.json")
    C.write_json(out_json, doc)

    cols13 = ["ref_id", "source_mod", "source_file", "file_cat", "ref_kind",
              "ref_value", "rule", "resolves", "resolves_to", "note"]
    # Numbering follows the P00_RERUN deliverable list:
    #   13 = 13_MO2_CONFLICT_MAP.csv   (owned by p00r_reports.py)
    #   17 = 17_EXTERNAL_REFERENCES.csv
    # Section 17 of the brief asks for the per-REFERENCE view (plugin name /
    # FormID / EditorID, for the future big-ESP merge), so the detailed table
    # takes the numbered name and the per-FILE roll-up becomes supplementary.
    out13 = os.path.join(C.REPORTS, "17_EXTERNAL_REFERENCES.csv")
    n13 = C.write_csv(out13, cols13, rows13)

    cols17 = ["file_id", "source_mod", "vpath", "file_cat", "size", "sha256",
              "is_binary", "has_distribution_layer", "has_scripts",
              "has_conditions", "n_plugin_refs", "n_formid_refs", "n_edid_refs",
              "n_unresolved_plugin_refs", "n_unresolved_formid_refs",
              "parse_note"]
    out17 = os.path.join(C.REPORTS, "17a_EXTERNAL_REFERENCES_BY_FILE.csv")
    n17 = C.write_csv(out17, cols17, rows17)

    C.log("=" * 68)
    C.log(f"config files scanned        : {len(files)}")
    C.log(f"  binary-skipped (NUL>10%)   : {n_binary}")
    C.log(f"  missing on disk            : {n_missing}")
    C.log(f"  read errors                : {n_error}")
    C.log(f"files with >=1 detection     : {summary['files_with_any_detection']}")
    C.log("detection hits by kind       : " + (
        ", ".join(f"{k}={v}" for k, v in summary["detection_hits_by_kind"].items())
        or "none"))
    C.log("detection FILES by kind      : " + (
        ", ".join(f"{k}={v}"
                  for k, v in summary["detection_files_by_kind"].items()) or "none"))
    zero = [k for k in ("SPID", "BOS", "OAR", "DAR") if det_hits[k] == 0]
    C.log(f"ZERO-PRESENCE VERDICT        : "
          + (", ".join(zero) + " = 0 matches across all "
             f"{len(files)} config files (confirms the 09 'zero' claim)"
             if zero else "none of SPID/BOS/OAR/DAR is zero -- SEE ABOVE"))
    C.log(f"plugin refs  total={summary['plugin_refs']['total']} "
          f"resolved={summary['plugin_refs']['resolved']} "
          f"unresolved={summary['plugin_refs']['unresolved']}")
    C.log(f"formid refs  total={summary['formid_refs']['total']} "
          f"resolved={summary['formid_refs']['resolved']} "
          f"unresolved={summary['formid_refs']['unresolved']}")
    C.log(f"edid refs    total={summary['edid_refs']['total']} "
          f"resolved={summary['edid_refs']['resolved']} "
          f"unresolved={summary['edid_refs']['unresolved']}")
    C.log(f"wrote {out_json}")
    C.log(f"wrote {out13}  rows={n13}")
    C.log(f"wrote {out17}  rows={n17}")
    C.log("=" * 68)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
