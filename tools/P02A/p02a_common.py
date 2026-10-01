
# -*- coding: utf-8 -*-
"""P02A shared READ-ONLY base layer.

Loads the frozen P00_RERUN evidence set and exposes:
  * MO2 VFS resolution (winner / shadowed providers) by virtual path
  * the frozen 11-outfit registry (ZLJ Combat Latex Pack)
  * NIF / texture / plugin / bodyslide accessors

STRICT READ-ONLY. This module never writes into MO2, Skyrim, or any mod folder.
"""
import csv
import gzip
import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA = os.path.join(ROOT, "data", "P00_RERUN")
REPORTS = os.path.join(ROOT, "reports")
OUT = os.path.join(REPORTS, "P02A")

PACK_ID = "ZLJ_COMBAT_LATEX"
DISPLAY_NAME = "ZLJ Combat Latex Pack"
TARGET_PLUGIN = "ZLJ_CombatLatex.esp"
CANONICAL_BODY = "CBBE_3BA"
MESH_ROOT = "meshes\\ZLJ\\CombatLatex\\"
TEX_ROOT = "textures\\ZLJ\\CombatLatex\\"
SD_ROOT = "CalienteTools\\BodySlide\\ShapeData\\ZLJ_Combat_Latex\\"
OSP_ROOT = "CalienteTools\\BodySlide\\SliderSets\\"

# --- frozen outfit registry -------------------------------------------------
# keys: primary mod (owns ARMO/ARMA + plugin), support mods (PBR / rework / physics)
OUTFITS = {
    "CL01_LatexKitty": {
        "display": "makaron-COSPLAY - AE_Latex_Kitty",
        "primary": "makaron-COSPLAY - AE_Latex_Kitty \u2014 \u3010\u670d\u88c5\u00b7\u88c5\u5907\u3011\u3010\u6765\u6e90\u00b7\u672c\u5730\u3011",
        "plugin": "AE_Latex_Kitty.esp",
        "support": {},
    },
    "CL02_OnceMedic": {
        "display": "makaron-COSPLAY - AE_Once_Medic",
        "primary": "makaron-COSPLAY - AE_Once_Medic \u2014 \u3010\u670d\u88c5\u00b7\u88c5\u5907\u3011\u3010\u6765\u6e90\u00b7\u672c\u5730\u3011",
        "plugin": "AE_Once_Medic.esp",
        "support": {},
    },
    "CL03_Tachy": {
        "display": "makaron-COSPLAY - AE_Stellablade_Tachy",
        "primary": "makaron-COSPLAY - AE_Stellablade_Tachy \u2014 \u3010\u670d\u88c5\u00b7\u88c5\u5907\u3011\u3010\u6765\u6e90\u00b7\u672c\u5730\u3011",
        "plugin": "AE Stellablade Tachy.esp",
        "support": {},
    },
    "CL04_Haley": {
        "display": "makaron-COSPLAY - AE_TFD_Haley_Black_Suit",
        "primary": "makaron-COSPLAY - AE_TFD_Haley_Black_Suit \u2014 \u3010\u670d\u88c5\u00b7\u88c5\u5907\u3011\u3010\u6765\u6e90\u00b7\u672c\u5730\u3011",
        "plugin": "SSE_TFD_Haley_Black_Suit.esp",
        "support": {"PBR_PATCH": "Haley Black Suit PBR"},
    },
    "CL05_Valby": {
        "display": "makaron-COSPLAY - AE_TFD_Valby_Nano_Suit",
        "primary": "makaron-COSPLAY - AE_TFD_Valby_Nano_Suit \u2014 \u3010\u670d\u88c5\u00b7\u88c5\u5907\u3011\u3010\u6765\u6e90\u00b7\u672c\u5730\u3011",
        "plugin": "AE_TFD_Valby_Nano_Suit.esp",
        "support": {},
    },
    "CL06_ToxicCat": {
        "display": "makaron-COSPLAY - AE_Toxic_Cat",
        "primary": "makaron-COSPLAY - AE_Toxic_Cat \u2014 \u3010\u670d\u88c5\u00b7\u88c5\u5907\u3011\u3010\u6765\u6e90\u00b7\u672c\u5730\u3011",
        "plugin": "AE_Toxic_Cat.esp",
        "support": {},
    },
    "CL07_Lupa": {
        "display": "makaron-COSPLAY - AE_Wuthering_Waves_Lupa",
        "primary": "makaron-COSPLAY - AE_Wuthering_Waves_Lupa \u2014 \u3010\u670d\u88c5\u00b7\u88c5\u5907\u3011\u3010\u6765\u6e90\u00b7\u672c\u5730\u3011",
        "plugin": "AE_Wuthering_Waves_Lupa.esp",
        "support": {},
    },
    "CL08_SpearHead": {
        "display": "SpearHead Catsuit CBBE 3BA BS",
        "primary": "\u77db\u5934\u7d27\u8eab\u8863 \u2014 SpearHead Catsuit CBBE 3BA BS \u2014 \u3010\u4f53\u578b\u00b7CBBE+3BA\u3011\u3010\u6765\u6e90\u00b7\u672c\u5730\u3011",
        "plugin": "BBD_CatsuitSpearhead.esp",
        "support": {},
    },
    "CL09_Corrupted": {
        "display": "AE Corrupted Body Suit",
        "primary": "\u5815\u843d\u7d27\u8eab\u8863 \u2014 AE Corrupted Body Suit \u2014 \u3010\u670d\u88c5\u00b7\u88c5\u5907\u3011\u3010\u8eab\u4f53\u00b7\u7269\u7406\u3011\u3010\u4f53\u578b\u00b7CBBE+3BA\u3011\u3010\u6765\u6e90\u00b7\u672c\u5730\u3011",
        "plugin": "AE_CorruptedBodySuit.esp",
        "support": {"LATEX_REWORK": "\u5815\u843d\u7d27\u8eab\u8863\u00b7\u4e73\u80f6\u91cd\u5236 \u2014 AE Corrupted Body Suit - Latex Rework \u2014 \u3010\u670d\u88c5\u00b7\u88c5\u5907\u3011\u3010\u8eab\u4f53\u00b7\u7269\u7406\u3011\u3010\u4f53\u578b\u00b7CBBE+3BA\u3011\u3010\u6765\u6e90\u00b7\u672c\u5730\u3011"},
    },
    "CL10_HoodST": {
        "display": "AE_HoodST",
        "primary": "AE_HoodST \u2014 \u3010\u6765\u6e90\u00b7\u672c\u5730\u3011",
        "plugin": "AE_HoodST.esp",
        "support": {},
    },
    "CL11_SkimpyAssassin": {
        "display": "Skimpy Assassin Outfit - BHUNP 3BBB - CBBE 3BBB",
        "primary": "Skimpy Assassin \u670d\u88c5 - BHUNP 3BBB - CBBE 3BBB \u2014 Skimpy Assassin Outfit - BHUNP 3BBB - CBBE 3BBB \u2014 \u3010\u670d\u88c5\u00b7\u88c5\u5907\u3011\u3010\u4f53\u578b\u00b7\u591a\u4f53\u578b\u3011",
        "plugin": "BBD Skimpy Assassin Outfit.esp",
        "support": {"NON_CANONICAL_BODY": "BHUNP_3BBB"},
    },
}

OUTFIT_IDS = list(OUTFITS.keys())


def norm(vp):
    """Normalise a virtual path to lower-case forward slashes, no data/ prefix."""
    if vp is None:
        return ""
    s = str(vp).replace("\\", "/").strip().strip('"').strip()
    s = re.sub(r"^data/", "", s, flags=re.I)
    return s.lower()


def win_path(vp):
    """Windows-style canonical virtual path (lower-case not enforced)."""
    s = str(vp or "").replace("/", "\\").strip('"')
    s = re.sub(r"^data\\\\", "", s, flags=re.I)
    if not s.lower().startswith("data\\\\"):
        s = "data\\\\" + s
    return s


def _load(name, gz=False):
    p = os.path.join(DATA, name)
    if gz:
        with gzip.open(p, "rt", encoding="utf-8") as f:
            return json.load(f)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


class P00:
    """Frozen P00 evidence, indexed."""

    _inst = None

    def __init__(self):
        self.file_index = _load("01_file_index.json.gz", gz=True)
        self.mod_aggs = _load("01_mod_aggregates.json")
        self.plugin_index = _load("02_plugin_index.json")
        self.plugin_records = _load("02_plugin_records.json")
        self.parts = _load("04_parts.json")["parts"]
        self.bs_projects = _load("07_bodyslide_projects.json")
        self.bs_slidersets = _load("07_bodyslide_slidersets.json")
        self.bs_shapedata = _load("07_bodyslide_shapedata.json")
        self.bs_vfs_summary = _load("07_bodyslide_vfs_summary.json")
        self.nifs = _load("08_nif_parsed.json.gz", gz=True)
        self.textures = _load("10_texture_parsed.json")
        self.config_refs = _load("14_config_refs.json")
        self.scope_evidence = _load("00_scope_evidence.json")

        # mod priority: LOWER number = higher MO2 priority = VFS winner
        self.priority = {m["MOD_ID"]: m["priority"] for m in self.mod_aggs}
        self.row = {m["MOD_ID"]: m["mo2_leftpane_row"] for m in self.mod_aggs}

        # VFS index
        self.vfs = defaultdict(list)
        for f in self.file_index:
            self.vfs[norm(f["vpath"])].append(f)
        for k in self.vfs:
            self.vfs[k].sort(key=lambda f: self.priority.get(f["mod"], 99999))

        # nif index by vpath (winning entry first)
        self.nif_by_path = defaultdict(list)
        for n in self.nifs:
            self.nif_by_path[norm(n["path"])].append(n)
        for k in self.nif_by_path:
            self.nif_by_path[k].sort(key=lambda n: self.priority.get(n["source_mod"], 99999))

        self.tex_by_path = defaultdict(list)
        for t in self.textures:
            self.tex_by_path[norm(t["path"])].append(t)
        for k in self.tex_by_path:
            self.tex_by_path[k].sort(key=lambda t: self.priority.get(t["source_mod"], 99999))

        # files owned by a mod, by extension
        self.files_of_mod = defaultdict(list)
        for f in self.file_index:
            self.files_of_mod[f["mod"]].append(f)

        # plugin records by plugin file
        self.records_of_plugin = defaultdict(list)
        for r in self.plugin_records:
            self.records_of_plugin[r["plugin_file"]].append(r)

        # bodyslide projects keyed by owning mod
        self.bs_of_mod = defaultdict(list)
        for p in self.bs_projects:
            self.bs_of_mod[p["MOD_ID"]].append(p)

    @classmethod
    def get(cls):
        if cls._inst is None:
            cls._inst = cls()
        return cls._inst

    # -- VFS helpers ------------------------------------------------------
    def winner(self, vp):
        lst = self.vfs.get(norm(vp))
        return lst[0] if lst else None

    def providers(self, vp):
        return self.vfs.get(norm(vp), [])

    def shadowed(self, vp):
        lst = self.vfs.get(norm(vp), [])
        return [f["mod"] for f in lst[1:]]

    def winning_mod(self, vp):
        f = self.winner(vp)
        return f["mod"] if f else ""

    def sha(self, vp):
        f = self.winner(vp)
        return f.get("sha256", "") if f else ""

    def exists(self, vp):
        return norm(vp) in self.vfs

    # -- NIF helpers ------------------------------------------------------
    def nif(self, vp):
        lst = self.nif_by_path.get(norm(vp))
        if lst:
            return lst[0]
        f = self.winner(vp)
        if f and f["ext"] == ".nif":
            return {"path": vp, "source_mod": f["mod"], "shapes": [], "parse_error": "not_in_p00_nif_index"}
        return None

    def nif_tex_rows(self, vp, nif=None):
        """[(shape, slot, dds_vpath_raw, exists_flag)] for a NIF's BSShaderTextureSet."""
        n = nif if nif is not None else self.nif(vp)
        if not n:
            return []
        rows = []
        for sh in n.get("shapes", []) or []:
            tex = sh.get("textures") or {}
            for slot in ("Diffuse", "Normal", "Specular", "EnvMask", "EnvMap", "Glowmap",
                         "Glow", "Detail", "Ramp", "Alpha", "Bump", "Emissive"):
                v = tex.get(slot)
                if v and str(v).strip():
                    rows.append((sh.get("name", ""), slot, str(v).strip()))
        return rows

    # -- plugin helpers ---------------------------------------------------
    def plugin_for_outfit(self, outfit_id):
        return OUTFITS[outfit_id]["plugin"]

    def mods_of_outfit(self, outfit_id):
        o = OUTFITS[outfit_id]
        mods = [o["primary"]] + list(o.get("support", {}).values())
        return [m for m in mods if m in self.priority]


def semantic_type(slot, dds_id=None):
    s = (slot or "").upper()
    base = ""
    if dds_id:
        b = os.path.basename(str(dds_id).replace("/", "\\")).lower()
        for tag in ("_d", "_n", "_s", "_m", "_e", "_g", "_r", "_b", "_a", "_p", "_f", "_sss", "_spec",
                    "_diffuse", "_normal", "_specular", "_env", "_glow", "_parallax", "_height", "_ao",
                    "_albedo", "_rough", "_metal", "_c", "_h", "_alpha", "_bump", "_detail"):
            if b.endswith(tag + ".dds"):
                base = tag
                break
    return (s or "UNSET") + ("|" + base if base else "")


def ui_name(outfit_id, part_label):
    return "[ZLJ Combat Latex] %s - %s" % (short_name(outfit_id), part_label)


def short_name(outfit_id):
    """Human label used inside BodySlide UI names."""
    return outfit_id.split("_", 1)[1]


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(header)
        for r in rows:
            w.writerow(["" if v is None else str(v) for v in r])
    return path


def write_md(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    p = P00.get()
    print("file_index", len(p.file_index), "nifs", len(p.nifs), "tex", len(p.textures))
    for oid in OUTFIT_IDS:
        mods = p.mods_of_outfit(oid)
        n_nif = sum(1 for m in mods for f in p.files_of_mod[m] if f["ext"] == ".nif")
        n_dds = sum(1 for m in mods for f in p.files_of_mod[m] if f["ext"] == ".dds")
        n_bs = len(p.bs_of_mod[oid].__class__ and p.bs_of_mod.get(oid, []))
        print(oid, "| mods", len(mods), "| nif", n_nif, "| dds", n_dds,
              "| osp", sum(1 for m in mods for f in p.files_of_mod[m] if f["ext"] == ".osp"),
              "| osd", sum(1 for m in mods for f in p.files_of_mod[m] if f["ext"] == ".osd"),
              "| xml", sum(1 for m in mods for f in p.files_of_mod[m] if f["ext"] == ".xml"),
              "| recs", len(p.records_of_plugin.get(OUTFITS[oid]["plugin"], [])))
