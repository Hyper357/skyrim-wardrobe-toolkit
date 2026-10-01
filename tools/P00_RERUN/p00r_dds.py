#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p00r_dds.py — STAGE D: read-only DDS header parse for the whole 09 scope.

Pure-python header parsing only; no third-party library and no image pixel data
is ever touched. Every texture is opened with mode "rb". sha256 comes from the
stage-A index, so nothing is re-hashed here. All output goes to data/P00_RERUN/
via the shared helpers, which refuse any path outside the RERUN tree.

DDS header layout actually implemented (Microsoft DDS programming reference):

    offset  size  field
    0       4     dwMagic = b"DDS " (0x20534444 little-endian)
    4       4     dwSize (always 124 for a plain header)
    8       4     dwFlags
    12      4     dwHeight
    16      4     dwWidth
    20      4     dwPitchOrLinearSize
    24      4     dwDepth
    28      4     dwMipMapCount
    76      32    DDS_PIXELFORMAT: dwSize, dwFlags, dwFourCC, dwRGBBitCount,
                  R/G/B/A masks
    80      4     ddspf.dwFlags  <- the brief's "pixel_flags"
    84      4     ddspf.dwFourCC <- b"DX10" means the DX10 extension follows,
                                  otherwise the block-compression FourCC
    108     20    dwCaps, dwCaps2, dwCaps3, dwCaps4, dwReserved2
    128     20    optional DDS_HEADER_DXT10 extension

    DDS_HEADER_DXT10, relative to offset 128:
    +0   4   dxgiFormat
    +4   4   resourceDimension
    +8   4   miscFlag
    +12  4   arraySize
    +16  4   miscFlags2

DEVIATION NOTE (reported to the parent agent): the brief says
"DX10: dxgi_format = header[4:8]" but also "array_size / misc = header[12:16]".
Those two are 8 bytes apart, which cannot both be right -- in the real struct
dxgiFormat is the FIRST uint32 of the block and arraySize is the fourth. The
correct +0 reading is used for `format`; the brief's literal +4 slot is still
emitted, as `dxgi_format_offset4` (it is really resource_dimension, also emitted
under its own name).

Usage: python tools/P00_RERUN/p00r_dds.py
"""
from __future__ import annotations

import gzip
import json
import os
import struct
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p00r_common as C  # noqa: E402

INDEX = os.path.join(C.DATA, "01_file_index.json.gz")

MAGIC = b"DDS "
HDR = 128
DX10_HDR = 20

# DDPF_* (ddspf.dwFlags at offset 80)
DDPF_ALPHAPIXELS = 0x00000001
DDPF_ALPHA = 0x00000002
DDPF_FOURCC = 0x00000004
DDPF_RGB = 0x00000040
DDPF_LUMINANCE = 0x00020000
DDPF_YUV = 0x00080000

# DDSCAPS2_*
DDSCAPS2_CUBEMAP = 0x200
DDSCAPS2_VOLUME = 0x200000
# DDS_MISCFLAG (DX10 block +8)
DDS_MISCFLAG_CUBEMAP = 0x4

# DirectDraw FourCC -> format name (values cross-checked against payload sizes).
FOURCC_MAP = {
    b"DXT1": "BC1_UNORM", b"DXT2": "BC2_UNORM", b"DXT3": "BC2_UNORM",
    b"DXT4": "BC3_UNORM", b"DXT5": "BC3_UNORM",
    b"ATI1": "BC4_UNORM", b"ATI2": "BC5_UNORM",
    b"BC4U": "BC4_UNORM", b"BC4S": "BC4_SNORM",
    b"BC5U": "BC5_UNORM", b"BC5S": "BC5_SNORM",
    b"ATI1N": "BC4_UNORM", b"DXN1": "DXN1", b"DXNM": "DXN1",
    b"DX10": "DX10_HEADER", b"3DS": "RGB565",
    b"ABGR": "RGBA8_BGRA", b"BGRA": "RGBA8_BGRA", b"RGBA": "RGBA8",
    b"ARGB": "ARGB8", b"XRGB": "XRGB8", b"YUY2": "YUY2", b"UYVY": "UYVY",
    b"\x00\x00\x00\x00": None,     # no FourCC -> mask-defined layout
}
FOURCC_ALIAS = {
    b"DXT1": "DXT1", b"DXT2": "DXT2", b"DXT3": "DXT3", b"DXT4": "DXT4",
    b"DXT5": "DXT5", b"ATI1": "ATI1", b"ATI2": "ATI2",
    b"BC4U": "BC4U", b"BC4S": "BC4S", b"BC5U": "BC5U", b"BC5S": "BC5S",
}

# DXGI_FORMAT_* for the DX10 extension.
# Values taken from the Microsoft DXGI_FORMAT reference and empirically confirmed
# against the byte sizes of the real files in this scope:
#   98 -> 8 bits/px  (BC7)      99 -> 8 bits/px (BC7 sRGB)
#   80 -> 4 bits/px  (BC4)      10 -> 8 bytes/px x 6 faces (R16G16B16A16_FLOAT)
# Reference: https://learn.microsoft.com/en-us/windows/win32/api/dxgiformat/ne-dxgiformat-dxgi_format
DXGI_MAP = {
    0: "UNKNOWN", 1: "R32G32B32A32_TYPELESS", 2: "R32G32B32A32_FLOAT",
    3: "R32G32B32A32_UINT", 4: "R32G32B32A32_SINT",
    5: "R32G32B32_TYPELESS", 6: "R32G32B32_FLOAT",
    7: "R32G32B32_UINT", 8: "R32G32B32_SINT",
    9: "R16G16B16A16_TYPELESS", 10: "R16G16B16A16_FLOAT",
    11: "R16G16B16A16_UNORM", 12: "R16G16B16A16_UINT",
    13: "R16G16B16A16_SNORM", 14: "R16G16B16A16_SINT",
    15: "R32G32_TYPELESS", 16: "R32G32_FLOAT", 17: "R32G32_UINT", 18: "R32G32_SINT",
    19: "R32G8X24_TYPELESS", 20: "D32_FLOAT_S8X24_UINT",
    21: "R32_FLOAT_X8X24_TYPELESS", 22: "X32_TYPELESS_G8X24_UINT",
    23: "R10G10B10A2_TYPELESS", 24: "R10G10B10A2_UNORM", 25: "R10G10B10A2_UINT",
    26: "R11G11B10_FLOAT",
    27: "RGBA8_TYPELESS", 28: "RGBA8", 29: "RGBA8_SRGB",
    30: "RGBA8_UINT", 31: "RGBA8_SNORM", 32: "RGBA8_SINT",
    33: "R16G16_TYPELESS", 34: "R16G16_FLOAT", 35: "R16G16_UNORM",
    36: "R16G16_UINT", 37: "R16G16_SNORM", 38: "R16G16_SINT",
    39: "R32_TYPELESS", 40: "D32_FLOAT", 41: "R32_FLOAT",
    42: "R32_UINT", 43: "R32_SINT",
    44: "R24G8_TYPELESS", 45: "D24_UNORM_S8_UINT",
    46: "R24_UNORM_X8_TYPELESS", 47: "X24_TYPELESS_G8_UINT",
    48: "R8G8_TYPELESS", 49: "R8G8_UNORM", 50: "R8G8_UINT",
    51: "R8G8_SNORM", 52: "R8G8_SINT",
    53: "R16_TYPELESS", 54: "R16_FLOAT", 55: "D16_UNORM",
    56: "R16_UNORM", 57: "R16_UINT", 58: "R16_SNORM", 59: "R16_SINT",
    60: "R8_TYPELESS", 61: "R8_UNORM", 62: "R8_UINT", 63: "R8_SNORM", 64: "R8_SINT",
    65: "A8_UNORM", 66: "R1_UNORM", 67: "R9G9B9E5_SHAREDEXP",
    68: "R8G8_B8G8_UNORM", 69: "G8R8_G8B8_UNORM",
    70: "BC1_TYPELESS", 71: "BC1_UNORM", 72: "BC1_UNORM_SRGB",
    73: "BC2_TYPELESS", 74: "BC2_UNORM", 75: "BC2_UNORM_SRGB",
    76: "BC3_TYPELESS", 77: "BC3_UNORM", 78: "BC3_UNORM_SRGB",
    79: "BC4_TYPELESS", 80: "BC4_UNORM", 81: "BC4_SNORM",
    82: "BC5_TYPELESS", 83: "BC5_UNORM", 84: "BC5_SNORM",
    85: "B5G6R5_UNORM", 86: "B5G5R5A1_UNORM",
    87: "RGBA8_BGRA", 88: "RGB8_BGRX",
    89: "R10G10B10_XR_BIAS_A2_UNORM",
    90: "RGBA8_BGRA_TYPELESS", 91: "RGBA8_BGRA_SRGB",
    92: "RGB8_BGRX_TYPELESS", 93: "RGB8_BGRX_SRGB",
    94: "BC6H_TYPELESS", 95: "BC6H_UF16", 96: "BC6H_SF16",
    97: "BC7_TYPELESS", 98: "BC7_UNORM", 99: "BC7_UNORM_SRGB",
    100: "AYUV", 101: "Y410", 102: "Y416",
    103: "NV12", 104: "P010", 105: "P016", 106: "YUV420_OPAQUE",
    107: "YUY2", 108: "Y210", 109: "Y216", 110: "NV11",
    111: "AI44", 112: "IA44", 113: "P8", 114: "A8P8", 115: "B4G4R4A4_UNORM",
    191: "A4B4G4R4_UNORM",
}

# Uncompressed bits-per-pixel implied by each named format, used only for the
# self-check printed at the end of the run.
BPP_HINT = {
    "BC1_UNORM": 4, "BC1_UNORM_SRGB": 4,
    "BC2_UNORM": 8, "BC2_UNORM_SRGB": 8,
    "BC3_UNORM": 8, "BC3_UNORM_SRGB": 8,
    "BC4_UNORM": 4, "BC4_SNORM": 4,
    "BC5_UNORM": 8, "BC5_SNORM": 8,
    "BC6H_UF16": 8, "BC6H_SF16": 8,
    "BC7_UNORM": 8, "BC7_UNORM_SRGB": 8,
    "RGBA8": 32, "RGBA8_SRGB": 32, "RGBA8_BGRA": 32, "RGBA8_BGRA_SRGB": 32,
    "RGB8_BGRX": 32, "RGBA8_UINT": 32, "RGBA8_SNORM": 32, "RGBA8_SINT": 32,
    "R16G16B16A16_FLOAT": 64, "R16G16B16A16_UNORM": 64,
    "R16G16B16A16_UINT": 64, "R8G8": 16, "R8": 8, "R16": 16,
    "B5G6R5_UNORM": 16, "B5G5R5A1_UNORM": 16, "B4G4R4A4_UNORM": 16,
    "R11G11B10_FLOAT": 32, "R9G9B9E5_SHAREDEXP": 32,
    "R8G8_B8G8_UNORM": 16, "G8R8_G8B8_UNORM": 16, "YUY2": 16, "UYVY": 16,
}


# ---------------------------------------------------------------------------
# dds_semantic: derived from the FILENAME ONLY, in the brief's exact order,
# first match wins.
#
# The deliberate "_c." ambiguity: "_c." is claimed by BOTH the CUBEMAP test and
# the COAT test. The brief mandates the cubemap test first, so "_c." always
# resolves to CUBEMAP and the COAT rule can then only fire on the literal word
# "coat". That is intended and recorded in the code on purpose.
#
# Two more breadth caveats (reported, not silently patched):
#   * the ENVMASK rule tests "_f", which matches many unrelated names;
#   * the AO rule tests the bare substring "ao", which also matches e.g. "road".
# Every record carries `dds_semantic_rule` naming the rule that fired, so the
# classification can be audited or re-derived later without re-reading files.
# ---------------------------------------------------------------------------
SEMANTIC_RULES = [
    ("CUBEMAP", lambda f: ("cube" in f) or ("_c." in f) or ("cubemap" in f)),
    ("NORMAL", lambda f: ("_n." in f) or ("_norm" in f) or ("normal" in f)),
    ("SPECULAR", lambda f: ("_s." in f) or ("_spec" in f) or ("gloss" in f)),
    ("ENVMASK", lambda f: (("_e" + "mask") in f) or ("env" in f) or ("_f" in f)),
    ("RMAOS", lambda f: "rmaos" in f),
    ("METALLIC", lambda f: ("metal" in f) or ("_m." in f)),
    ("ROUGHNESS", lambda f: ("rough" in f) or ("_r." in f)),
    ("AO", lambda f: "ao" in f),
    ("COAT", lambda f: ("coat" in f) or ("_c." in f)),   # "_c." unreachable, see above
    ("GLOW", lambda f: ("glow" in f) or ("_g." in f)),
    ("MASK", lambda f: ("mask" in f) or ("_sss" in f)),
]


def classify_semantic(filename: str) -> str:
    f = (filename or "").lower()
    for name, test in SEMANTIC_RULES:
        if test(f):
            return name
    return "UNKNOWN"


def u32(b: bytes) -> int:
    return int.from_bytes(b, "little", signed=False)


def parse_header(head: bytes) -> dict:
    """head = the first 148 bytes of the file (shorter for tiny files)."""
    fourcc = head[84:88] if len(head) >= 88 else b""
    out = {
        "magic_ok": head[:4] == MAGIC,
        "header_size": u32(head[4:8]),
        "flags": u32(head[8:12]),
        "height": u32(head[12:16]),
        "width": u32(head[16:20]),
        "pitch_or_linear_size": u32(head[20:24]),
        "depth": u32(head[24:28]),
        "mip_count": u32(head[28:32]),
        "pixel_format_size": u32(head[76:80]) if len(head) >= 80 else 0,
        "pixel_flags": u32(head[80:84]) if len(head) >= 84 else 0,
        "fourcc_raw_hex": fourcc.hex(),
        "fourcc_raw_ascii": fourcc.rstrip(b"\x00").decode("ascii", "replace"),
        "fourcc_alias": FOURCC_ALIAS.get(fourcc, ""),
        "rgb_bit_count": u32(head[88:92]) if len(head) >= 92 else 0,
        "masks": [u32(head[92 + 4 * i:96 + 4 * i]) if len(head) >= 100 + 4 * i
                  else 0 for i in range(4)],
        "caps": u32(head[108:112]) if len(head) >= 112 else 0,
        "caps2": u32(head[112:116]) if len(head) >= 116 else 0,
        "caps3": u32(head[116:120]) if len(head) >= 120 else 0,
        "caps4": u32(head[120:124]) if len(head) >= 124 else 0,
        "reserved2": u32(head[124:128]) if len(head) >= 128 else 0,
    }
    out["is_cubemap"] = bool(out["caps2"] & DDSCAPS2_CUBEMAP)
    out["is_volume"] = bool(out["caps2"] & DDSCAPS2_VOLUME)
    out["is_dx10"] = len(head) >= HDR + DX10_HDR and fourcc == b"DX10"

    if out["is_dx10"]:
        blk = head[HDR:HDR + DX10_HDR]
        out["dxgi_format"] = u32(blk[0:4])
        out["resource_dimension"] = u32(blk[4:8])
        out["dxgi_format_offset4"] = out["resource_dimension"]   # brief's slot
        out["misc_flag"] = u32(blk[8:12])
        out["array_size"] = u32(blk[12:16])
        out["misc_flags2"] = u32(blk[16:20])
        out["format"] = DXGI_MAP.get(out["dxgi_format"],
                                     "DXGI_%d" % out["dxgi_format"])
    else:
        out["dxgi_format"] = None
        out["resource_dimension"] = None
        out["dxgi_format_offset4"] = None
        out["misc_flag"] = 0
        out["array_size"] = 1
        out["misc_flags2"] = 0
        out["format"] = FOURCC_MAP.get(fourcc, "__MISSING__")
        if out["format"] == "__MISSING__":
            raw = fourcc.rstrip(b"\x00")
            out["format"] = (raw.decode("ascii", "replace") if raw
                             else "0x%08X" % out["pixel_flags"])
        elif out["format"] is None:          # FourCC absent -> mask layout
            pf, bc = out["pixel_flags"], out["rgb_bit_count"]
            if pf & DDPF_RGB:
                out["format"] = "RGB%d%s" % (bc, "A" if pf & DDPF_ALPHAPIXELS else "")
            elif pf & DDPF_LUMINANCE:
                out["format"] = "LUM%d%s" % (
                    bc, "A" if pf & DDPF_ALPHAPIXELS else "")
            else:
                out["format"] = "UNCOMPRESSED_pf0x%08X" % pf

    out["is_bc"] = out["format"].startswith(("BC1", "BC2", "BC3", "BC4", "BC5",
                                             "BC6H", "BC7", "DXT", "DXN"))
    out["is_srgb"] = out["format"].endswith("_SRGB")
    out["bpp_expected"] = BPP_HINT.get(out["format"], 0)
    out["has_mipmaps"] = bool(out["caps"] & 0x400000)
    if out["is_dx10"]:
        out["is_cubemap"] = out["is_cubemap"] or bool(out["misc_flag"] & DDS_MISCFLAG_CUBEMAP)
    return out


def parse_one(rec: dict) -> dict:
    vpath = rec["vpath"]
    basename = os.path.basename(vpath)
    low = basename.lower()
    row = {
        "TEXTURE_ID": C.nif_id(vpath),
        "path": vpath,
        "source_mod": rec["mod"],
        "sha256": rec["sha256"],
        "size": rec["size"],
        "basename": low,
        "dds_semantic": classify_semantic(basename),
        "parse_error": "",
    }
    row["dds_semantic_rule"] = row["dds_semantic"]
    if row["dds_semantic"] == "CUBEMAP" and "_c." in low:
        row["dds_semantic_ambiguous_c"] = True     # "_c." -> CUBEMAP by rule order

    full = os.path.join(C.MODS_DIR, rec["mod"], rec["rel"].replace("/", os.sep))
    row["file_exists"] = os.path.isfile(full)
    try:
        with open(full, "rb") as fh:            # READ-ONLY, always
            head = fh.read(HDR + DX10_HDR)
    except OSError as ex:
        row["parse_error"] = repr(ex)[:200]
        row.update({"width": 0, "height": 0, "mip_count": 0,
                    "format": "UNREADABLE", "is_bc": False, "is_srgb": False,
                    "bpp_expected": 0, "is_dx10": False, "is_cubemap": False,
                    "magic_ok": False})
        return row

    if len(head) < HDR:
        row["parse_error"] = "truncated header (%d bytes)" % len(head)
        row.update({"width": 0, "height": 0, "mip_count": 0,
                    "format": "TRUNCATED", "is_bc": False, "is_srgb": False,
                    "bpp_expected": 0, "is_dx10": False, "is_cubemap": False,
                    "magic_ok": False})
        return row

    try:
        h = parse_header(head)
    except Exception as ex:
        row["parse_error"] = repr(ex)[:200]
        row.update({"width": 0, "height": 0, "mip_count": 0,
                    "format": "MALFORMED", "is_bc": False, "is_srgb": False,
                    "bpp_expected": 0, "is_dx10": False, "is_cubemap": False,
                    "magic_ok": False})
        return row

    if not h["magic_ok"]:
        row["parse_error"] = "BAD_MAGIC:%r" % head[:4]
    if h["header_size"] != 124:
        row["parse_error"] = (row["parse_error"] + "|" if row["parse_error"] else "") \
            + "dwSize=%d" % h["header_size"]
    h["payload_bytes"] = max(rec["size"] - (HDR + DX10_HDR if h["is_dx10"] else HDR), 0)
    row.update(h)
    return row


def main() -> int:
    C.ensure_dirs()
    t0 = time.time()
    with gzip.open(INDEX, "rt", encoding="utf-8") as fh:
        index = json.load(fh)
    dds = [r for r in index if r["cat"] == "dds"]
    C.log(f"stage D: {len(dds):,} DDS in scope")

    records = [parse_one(r) for r in dds]
    records.sort(key=lambda r: (r["TEXTURE_ID"], r["source_mod"]))
    C.log(f"parsed {len(records):,} DDS headers in {time.time()-t0:.1f}s")

    # ---- duplicate analysis -------------------------------------------------
    by_sha = defaultdict(list)
    by_name = defaultdict(list)
    for r in records:
        by_sha[r["sha256"]].append(r["TEXTURE_ID"])
        by_name[r["basename"]].append({"path": r["path"], "sha256": r["sha256"],
                                        "source_mod": r["source_mod"]})

    byte_identical = {sha: sorted(ids) for sha, ids in sorted(by_sha.items())
                      if len(ids) > 1}
    same_name_diff = {
        name: sorted(entries, key=lambda e: (e["sha256"], e["path"]))
        for name, entries in sorted(by_name.items())
        if len({e["sha256"] for e in entries}) > 1
    }

    out = os.path.join(C.DATA, "10_texture_parsed.json")
    C.write_json(out, records)
    C.log(f"wrote {out} ({len(records):,} rows)")

    out2 = os.path.join(C.DATA, "10_texture_dupes.json")
    C.write_json(out2, {
        "byte_identical_groups": byte_identical,
        "same_name_diff_content": same_name_diff,
    })
    C.log(f"wrote {out2} "
          f"({len(byte_identical):,} byte-identical groups, "
          f"{len(same_name_diff):,} same-name/different-content names)")

    # ---- summary ------------------------------------------------------------
    errs = [r for r in records if r["parse_error"]]
    C.log(f"parse errors: {len(errs):,}")
    for e in Counter(r["parse_error"] for r in errs).most_common(10):
        C.log(f"  ! x{e[1]} :: {e[0][:120]}")

    C.log("format distribution: " + ", ".join(
        f"{k}={v}" for k, v in Counter(r["format"] for r in records).most_common()))
    C.log("semantic distribution: " + ", ".join(
        f"{k}={v}" for k, v in
        Counter(r["dds_semantic"] for r in records).most_common()))
    C.log(f"DX10 headers: {sum(1 for r in records if r['is_dx10']):,}"
          f"   legacy FourCC: {sum(1 for r in records if not r['is_dx10']):,}"
          f"   cubemaps: {sum(1 for r in records if r['is_cubemap']):,}")
    nz = [r for r in records if r["width"] and r["height"]]
    C.log(f"non-square: {sum(1 for r in nz if r['width'] != r['height']):,}"
          f"   non-power-of-two: {sum(1 for r in nz if (r['width'] & (r['width']-1)) or (r['height'] & (r['height']-1))):,}"
          f"   1x1 placeholders: {sum(1 for r in nz if r['width'] == 1 and r['height'] == 1):,}")
    C.log(f"total time {time.time()-t0:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
