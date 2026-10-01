# -*- coding: utf-8 -*-
"""NIF BSShaderTextureSet path rewriter (P02B).

Why not parse the whole header
------------------------------
The NIF header field layout varies with version/userVersion, and guessing it is
fragile. The STRING TABLE, however, has a completely regular shape: it is a
contiguous array of entries, each [uint32 length][raw bytes], and it is preceded by
two uint32 fields: numStrings and maxStringLength.

So this module locates the table by evidence instead of by offset arithmetic:

  1. scan the file for candidate entries ([u32 len][printable bytes]);
  2. grow the maximal contiguous run of such entries that contains the texture paths;
  3. verify that the uint32 immediately before the run equals the run length
     (= numStrings). If it does not, the parse is rejected.

Rewriting then only touches the table: entry count and order are preserved, so every
string index referenced by BSShaderTextureSet blocks stays valid, and everything after
the table is copied through byte-for-byte.
"""
import os
import struct
import sys

PRINTABLE = set(range(0x20, 0x7f)) | {0x09}


class NifError(Exception):
    pass


def _entry_at(data, p, maxlen=1024):
    """Parse one table entry at p: [uint32 len][bytes]. Empty entries are legal."""
    if p + 4 > len(data):
        return None
    n = struct.unpack_from("<I", data, p)[0]
    if n > maxlen or p + 4 + n > len(data):
        return None
    body = data[p + 4:p + 4 + n]
    if any(b not in PRINTABLE for b in body):
        return None
    return n, body


def _table_around(data, anchor):
    """Expand a contiguous [len][bytes] table outward from an anchor position."""
    ent = _entry_at(data, anchor)
    if not ent:
        return None
    start, end = anchor, anchor + 4 + ent[0]
    # walk backwards
    while start - 4 >= 0:
        prev = _entry_at(data, start - 4 - 0)  # placeholder, replaced below
        break
    # backwards: an entry immediately before must satisfy prev_end == start
    while True:
        found = None
        for back in range(4, 4 + 1024 + 1):
            s = start - back
            if s < 0:
                break
            e = _entry_at(data, s)
            if e and s + 4 + e[0] == start:
                found = s
                break
        if found is None:
            break
        start = found
    # forwards
    while True:
        e = _entry_at(data, end)
        if not e:
            break
        end = end + 4 + e[0]
    strings = []
    p = start
    while p < end:
        e = _entry_at(data, p)
        if not e:
            return None
        strings.append(e[1])
        p += 4 + e[0]
    return start, end, strings


def find_string_table(data, must_include=None):
    """Return (table_start, table_end, [bytes,...], num_strings_field).

    Anchored on a known string when one is supplied; otherwise on the longest
    table found by scanning. The uint32 immediately before the table must equal
    the entry count (that is the numStrings header field) - the caller checks it.
    """
    must = [m.lower().encode("latin-1") for m in (must_include or [])]
    best = None
    for m in must:
        from_pos = 0
        while True:
            i = data.lower().find(m, from_pos)
            if i < 0:
                break
            t = _table_around(data, i - 4)
            if t and (best is None or len(t[2]) > len(best[2])):
                best = t
            from_pos = i + 1
    if best is None:
        p, limit = 0, min(len(data), 4 << 20)
        while p < limit:
            e = _entry_at(data, p)
            if e and b".dds" in e[1].lower():
                t = _table_around(data, p)
                if t and (best is None or len(t[2]) > len(best[2])):
                    best = t
                p += 4 + e[0]
            else:
                p += 1
    if best is None:
        raise NifError("no contiguous string table found")
    start, end, strings = best
    num_field = struct.unpack_from("<I", data, start - 4)[0] if start >= 4 else -1
    return start, end, strings, num_field


def rewrite(data, mapping, strict=True):
    """mapping: {old_path: new_path}. Returns (new_bytes, report)."""
    lowered = {k.strip().lower(): v for k, v in mapping.items()}
    start, end, strings, num_field = find_string_table(data, must_include=list(mapping)[:3])
    if num_field != len(strings):
        raise NifError("string table self-check failed: preceding uint32=%d but found %d entries"
                       % (num_field, len(strings)))
    applied, seen = {}, set()
    out = list(strings)
    for i, s in enumerate(strings):
        t = s.decode("latin-1").strip()
        key = t.lower()
        if key in lowered:
            out[i] = lowered[key].encode("latin-1")
            applied[t] = lowered[key]
            seen.add(key)
    missing = [k for k in mapping if k.strip().lower() not in seen]
    if strict and missing:
        raise NifError("requested path(s) not in the string table: %s" % missing[:5])
    new_table = bytearray()
    for s in out:
        new_table += struct.pack("<I", len(s)) + s
    new_data = data[:start] + bytes(new_table) + data[end:]
    # patch maxStringLength (the uint32 immediately before the table)
    msl = max((len(s) for s in out), default=0)
    new_data = new_data[:start - 8] + struct.pack("<I", msl) + new_data[start - 4:]
    # re-locate the table to confirm
    s2, e2, strings2, nf2 = find_string_table(new_data, must_include=list(mapping)[:1] if mapping else None)
    if nf2 != len(strings2):
        raise NifError("post-write self-check failed")
    report = dict(applied=len(applied), missing=missing, entries=len(strings),
                  old_size=len(data), new_size=len(new_data),
                  delta=len(new_data) - len(data), table_bytes=end - start,
                  num_strings_field=num_field, max_string_length=msl)
    return new_data, report


def verify(data):
    start, end, strings, num_field = find_string_table(data)
    return dict(entries=len(strings), num_strings_field=num_field,
                consistent=(num_field == len(strings)),
                table_bytes=end - start, size=len(data))


def texture_paths(data):
    _, _, strings, _ = find_string_table(data)
    return [s.decode("latin-1").strip() for s in strings
            if s.decode("latin-1").strip().lower().endswith(".dds")]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("rewrite(data, mapping) / verify(data) / texture_paths(data) / find_string_table(data)")
