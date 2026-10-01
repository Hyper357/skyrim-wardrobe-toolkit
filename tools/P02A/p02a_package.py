# -*- coding: utf-8 -*-
"""P02A.1 full-package builder + deliverable gate.

Packages the ENTIRE reports/P02A/ tree (never a summary subset) and refuses to
produce a zip unless every mandated deliverable exists. READ-ONLY with respect to
mod/game files; the only output is the zip plus a stdout verification report.
"""
import hashlib
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p02a_common as C

REQUIRED = [
    'P02A_ARCHITECTURE.md',
    'P02A_MASTER_PLAN.md',
    'P02A_EFFECTIVE_SOURCE_MAP.csv',
    'P02A_MESH_MIGRATION.csv',
    'P02A_TEXTURE_MIGRATION.csv',
    'P02A_CROSS_OUTFIT_TEXTURE_CLOSURE.csv',
    'P02A_NIF_TEXTURE_REWRITE.csv',
    'P02A_BODYSLIDE_MIGRATION.csv',
    'P02A_BODYSLIDE_MORPH_MIGRATION.csv',
    'P02A_SHAPEDATA_TEXTURE_REWRITE.csv',
    'P02A_PLUGIN_RECORD_MIGRATION.csv',
    'P02A_ARMA_MODEL_REWRITE.csv',
    'P02A_PLUGIN_TEXTURE_REWRITE.csv',
    'P02A_PHYSICS_MIGRATION.csv',
    'P02A_SELF_CONTAINMENT_AUDIT.csv',
    'P02A_UNRESOLVED_REFERENCE_CLASSIFICATION.csv',
    'P02A_GLOBAL_PROVIDER_LOOKUP.csv',
    'CL09_REWORK_VS_BODYSLIDE_DECISION.md',
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    root = C.OUT
    odir = os.path.join(root, 'outfits')
    have = os.listdir(root) if os.path.isdir(root) else []
    manifests = sorted(os.listdir(odir)) if os.path.isdir(odir) else []
    missing = [f for f in REQUIRED if f not in have]
    missing += ['outfits/' + o + '.md' for o in C.OUTFIT_IDS if o + '.md' not in manifests]
    print('mandated deliverables: %d present, %d missing' % (len(REQUIRED) - len([m for m in missing if '/' not in m]), len(missing)))
    for m in missing:
        print('   MISSING', m)
    if missing:
        print('REFUSING to package an incomplete P02A.')
        return 2

    files = []
    for dirpath, _dirs, names in os.walk(root):
        for n in sorted(names):
            files.append(os.path.join(dirpath, n))
    files.sort()
    out_zip = os.path.join(C.ROOT, 'P02A_MIGRATION_DESIGN_PACKAGE.zip')
    if os.path.exists(out_zip):
        os.remove(out_zip)
    base = os.path.dirname(root)
    with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in files:
            z.write(p, os.path.relpath(p, base).replace(os.sep, '/'))
    print()
    print('packaged %d files, %.2f MB -> %s' % (len(files), os.path.getsize(out_zip) / 1048576.0, out_zip))
    print()
    print('%-64s %10s  %s' % ('entry', 'bytes', 'sha256[:16]'))
    for p in files:
        print('%-64s %10d  %s' % (os.path.relpath(p, base).replace(os.sep, '/'),
                                   os.path.getsize(p), sha256(p)[:16]))
    with zipfile.ZipFile(out_zip) as z:
        bad = z.testzip()
    print()
    print('zip integrity:', 'OK' if bad is None else 'CORRUPT ' + str(bad))
    return 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())