#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p00r_balance.py — rebuild 19_CURRENT_BALANCE_VALUES.csv.

CORRECTED. The previous version emitted only raw_u32 / raw_f32 and declined to
name the fields. That refusal was over-cautious: the Skyrim ARMO schema is
established and is now applied.

  ARMO.DATA  8 bytes : uint32 value, float32 weight
  ARMO.DNAM  4 bytes : uint32 armor rating

The raw bytes are kept alongside as provenance, and an implausible weight is
flagged rather than dropped, so nothing is lost either way.
"""
from __future__ import annotations

import json
import math
import os
import struct
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p00r_common as C  # noqa: E402

OUT = os.path.join(C.REPORTS, "19_CURRENT_BALANCE_VALUES.csv")

COLS = ["PART_ID", "PLUGIN_ID", "plugin_file", "MOD_ID", "priority",
        "EDID", "FULL", "ARMO_formid", "part_category", "slot_names",
        "value", "weight", "armor_rating", "data_raw_hex", "dnam_raw_hex",
        "weight_sanity", "provenance", "note"]

# a wearable armour piece in this corpus is nowhere near these; anything
# outside is reported with its raw value plus a flag
WEIGHT_MIN, WEIGHT_MAX = 0.0, 1000.0


def main():
    C.ensure_dirs()
    with open(os.path.join(C.DATA, "02_plugin_records.json"),
              encoding="utf-8") as fh:
        recs = json.load(fh)
    parts_path = os.path.join(C.DATA, "04_parts.json")
    cat_by_part = {}
    if os.path.isfile(parts_path):
        with open(parts_path, encoding="utf-8") as fh:
            blob = json.load(fh)
        # stage G writes {"stats": {...}, "parts": [...]} ; tolerate a bare list
        plist = blob.get("parts", []) if isinstance(blob, dict) else blob
        for p in plist:
            if isinstance(p, dict):
                cat_by_part[p.get("PART_ID")] = p.get("part_category", "")

    rows = []
    n_flag = 0
    for r in recs:
        if r["record_type"] != "ARMO":
            continue
        subs = r.get("subrecords") or {}
        a = r.get("armo") or {}
        data = subs.get("DATA")
        dnam = subs.get("DNAM")

        # DATA: prefer the 8 raw bytes, fall back to the pre-split values
        raw8 = ""
        value = a.get("DATA_u32")
        weight = a.get("DATA_f32")
        if isinstance(data, list) and data:
            d0 = data[0]
            if isinstance(d0, dict):
                # stage B stores DATA as {"u32": value, "f32": weight}
                value = d0.get("u32", value)
                weight = d0.get("f32", weight)
            elif isinstance(d0, str) and len(d0) == 16:
                # raw 8 bytes, when the payload was kept verbatim
                raw8 = d0
                try:
                    value = struct.unpack_from("<I", bytes.fromhex(d0), 0)[0]
                    weight = struct.unpack_from("<f", bytes.fromhex(d0), 4)[0]
                except Exception:                       # noqa: BLE001
                    pass
        elif isinstance(data, dict):
            value = data.get("u32", value)
            weight = data.get("f32", weight)

        raw4 = ""
        if isinstance(dnam, list) and dnam and isinstance(dnam[0], str) \
                and len(dnam[0]) == 8:
            raw4 = dnam[0]
            try:
                rating = struct.unpack_from(
                    "<I", bytes.fromhex(raw4), 0)[0]
            except Exception:                           # noqa: BLE001
                rating = None
        elif isinstance(dnam, int):
            rating = dnam
        else:
            rating = a.get("DNAM_u32")

        sanity = "ok"
        if weight is None:
            sanity = "absent"
        elif isinstance(weight, float) and (math.isnan(weight)
                                            or math.isinf(weight)):
            sanity = "nan_or_inf"
        elif not (WEIGHT_MIN <= weight <= WEIGHT_MAX):
            sanity = "out_of_range"
        if sanity not in ("ok", "absent"):
            n_flag += 1

        edid = subs.get("EDID")
        full = subs.get("FULL")
        edid = edid[0] if isinstance(edid, list) and edid else ""
        full = full[0] if isinstance(full, list) and full else ""
        pid = f"PART::{C.plugin_id(r['plugin_file'])}::{r['formid']}"

        rows.append({
            "PART_ID": pid,
            "PLUGIN_ID": r.get("PLUGIN_ID", ""),
            "plugin_file": r.get("plugin_file", ""),
            "MOD_ID": r.get("MOD_ID", ""),
            "priority": r.get("priority", ""),
            "EDID": edid,
            "FULL": full,
            "ARMO_formid": r["formid"],
            "part_category": cat_by_part.get(pid, ""),
            "slot_names": ";".join(a.get("slot_names") or []),
            "value": value if value is not None else "UNKNOWN",
            "weight": (f"{weight:.4f}" if isinstance(weight, float)
                       else (weight if weight is not None else "UNKNOWN")),
            "armor_rating": rating if rating is not None else "UNKNOWN",
            "data_raw_hex": raw8,
            "dnam_raw_hex": raw4,
            "weight_sanity": sanity,
            "provenance": "ARMO.DATA=uint32 value + float32 weight; "
                          "ARMO.DNAM=uint32 armor rating; raw bytes retained",
            "note": ("weight outside the plausible wearable range - raw value "
                     "kept, flagged" if sanity in ("out_of_range",
                                                    "nan_or_inf") else ""),
        })

    n = C.write_csv(OUT, COLS, rows)
    have3 = sum(1 for r in rows
                if str(r["value"]) != "UNKNOWN"
                and str(r["weight"]) != "UNKNOWN"
                and str(r["armor_rating"]) != "UNKNOWN")
    C.log(f"19_CURRENT_BALANCE_VALUES.csv = {n} rows")
    C.log(f"  all three of value/weight/armor_rating decoded : {have3}/{n}")
    C.log("  weight_sanity : " + ", ".join(
        f"{k}={v}" for k, v in Counter(r["weight_sanity"]
                                       for r in rows).most_common()))
    C.log(f"  flagged rows  : {n_flag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
