# -*- coding: utf-8 -*-
"""NIF texture-path rewriter for P02B, driven by the vendored PyNifly.

PyNifly (E:/SkyrimAE/Tools/pynifly) is the same read/write NIF library the P00
pipeline used for parsing, so it handles the NIF header, block table and string
storage correctly - no hand-rolled header arithmetic.

The source file is opened read-only by nifly.load(); the result is written to the
caller-supplied staging path. Original mod assets are never modified.
"""
import os
import sys

PYNIFLY_ROOT = r"E:\SkyrimAE\Tools\pynifly"
if PYNIFLY_ROOT not in sys.path:
    sys.path.insert(0, PYNIFLY_ROOT)

_NifFile = None


def _load_lib():
    global _NifFile
    if _NifFile is None:
        from pyn.pynifly import NifFile           # noqa: E402
        _NifFile = NifFile
    return _NifFile


def read_textures(src):
    """{shape_name: {slot: path}} for every shape in a NIF."""
    NifFile = _load_lib()
    nif = NifFile(src)
    out = {}
    for sh in nif.shapes:
        try:
            out[sh.name] = {k: v for k, v in (sh.textures or {}).items() if v}
        except Exception as ex:
            out[sh.name] = {"__error__": str(ex)}
    return out


def rewrite_file(src, dst, mapping, dry_run=False):
    """Copy src to dst, replacing texture paths per mapping {old: new}.

    Returns a report dict. Raises on a NIF that cannot be opened.
    """
    NifFile = _load_lib()
    lowered = {k.strip().lower(): v for k, v in mapping.items()}
    nif = NifFile(src)
    applied, missing, seen = {}, [], set()
    for sh in nif.shapes:
        try:
            tex = sh.textures or {}
        except Exception:
            continue
        for slot, cur in list(tex.items()):
            if not cur:
                continue
            key = str(cur).strip().lower()
            if key in lowered:
                new = lowered[key]
                if not dry_run:
                    sh.set_texture(slot, new)
                applied["%s:%s" % (sh.name, slot)] = new
                seen.add(key)
    missing = [k for k in mapping if k.strip().lower() not in seen]
    if not dry_run:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        nif.filepath = dst
        nif.save()
    return dict(src=src, dst=dst, applied=len(applied), missing=missing,
                details=applied, shapes=len(nif.shapes))


def verify(dst, mapping):
    """Re-open the written NIF and confirm every mapping landed."""
    after = read_textures(dst)
    flat = {str(v).strip().lower() for slots in after.values() for v in slots.values()}
    want_new = {v.strip().lower() for v in mapping.values()}
    want_old = {k.strip().lower() for k in mapping}
    return dict(new_present=len(want_new & flat), new_expected=len(want_new),
                old_remaining=len(want_old & flat), shapes=len(after))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("read_textures(src) / rewrite_file(src, dst, mapping) / verify(dst, mapping)")
