# -*- coding: utf-8 -*-
"""P02A.1 CL09_Corrupted - Latex Rework vs BodySlide ShapeData evidence collector.

STRICT READ-ONLY. Reads the frozen P00 evidence plus two specific NIF/DDS file pairs
from the CL09 source mods to measure exactly what the Latex Rework changed.
Writes nothing except the evidence it prints.
"""
import collections
import gzip
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p02a_common as C

P = C.P00.get()
MODS = r'E:\SkyrimAE\mo2\mods'
BASE = next(m for m in P.priority if 'Corrupted' in m and 'Rework' not in m)
REWORK = next(m for m in P.priority if 'Corrupted' in m and 'Rework' in m)


def mod_file(mod, vpath):
    p = os.path.join(MODS, mod, vpath.replace('/', os.sep))
    return p if os.path.isfile(p) else None


def byte_diff(p1, p2):
    a = open(p1, 'rb').read()
    b = open(p2, 'rb').read()
    n = min(len(a), len(b))
    diff = sum(1 for i in range(n) if a[i] != b[i])
    sa = set(s.decode('latin1') for s in re.findall(rb'[ -~]{6,}', a))
    sb = set(s.decode('latin1') for s in re.findall(rb'[ -~]{6,}', b))
    return dict(size_base=len(a), size_rework=len(b), differing_bytes=diff,
                string_only_base=len(sa - sb), string_only_rework=len(sb - sa),
                identical=(a == b))


def nif_tex(vpath):
    nifs = json.load(gzip.open(os.path.join(C.DATA, '08_nif_parsed.json.gz'), 'rt', encoding='utf-8'))
    out = []
    for n in nifs:
        if C.norm(n['path']) == C.norm(vpath):
            out.append(('REWORK' if 'Latex Rework' in n['source_mod'] else 'BASE',
                        [(s['name'], {k: v for k, v in (s.get('textures') or {}).items() if v})
                         for s in n['shapes']]))
    return out


def main():
    print('BASE   priority', P.priority[BASE], BASE)
    print('REWORK priority', P.priority[REWORK], REWORK, '  <- VFS winner')
    print()
    print('--- 1. runtime meshes: base vs rework (same vpath) ---')
    fb = {C.norm(f['vpath']): f for f in P.files_of_mod[BASE]}
    fr = {C.norm(f['vpath']): f for f in P.files_of_mod[REWORK]}
    for v in sorted(set(fb) & set(fr)):
        if not v.startswith('meshes/'):
            continue
        pb, pr = mod_file(BASE, v), mod_file(REWORK, v)
        if pb and pr:
            d = byte_diff(pb, pr)
            print('  %-58s size %9d -> %9d  diff_bytes=%-6d strings -/+ %d/%d  identical=%s'
                  % (v.split('/')[-1], d['size_base'], d['size_rework'], d['differing_bytes'],
                     d['string_only_base'], d['string_only_rework'], d['identical']))
    print()
    print('--- 2. ShapeData: base data-folder vs rework flat copy ---')
    base_sd = {C.norm(f['vpath']): f for f in P.files_of_mod[BASE] if 'shapedata' in C.norm(f['vpath'])}
    rw_sd = {C.norm(f['vpath']): f for f in P.files_of_mod[REWORK] if 'shapedata' in C.norm(f['vpath'])}
    for v in sorted(rw_sd):
        name = v.rsplit('/', 1)[-1]
        match = [k for k in base_sd if k.rsplit('/', 1)[-1] == name]
        if not match:
            print('  %-46s NO base counterpart (orphan)' % name)
            continue
        pb, pr = mod_file(BASE, match[0]), mod_file(REWORK, v)
        d = byte_diff(pb, pr) if pb and pr else {}
        print('  %-46s vs base %-44s diff_bytes=%-5d identical=%s'
              % (name, match[0].split('shapedata/')[-1], d.get('differing_bytes', -1), d.get('identical')))
    print()
    print('--- 3. feet texture bindings (base runtime vs rework flat ShapeData) ---')
    for vp in ('meshes/ae_corruptedbodysuit/ae_corruptedbodysuit_feet_0.nif',
               'calientetools/bodyslide/shapedata/ae_corruptedbodysuit_feet.nif'):
        for who, shapes in nif_tex(vp):
            print('  %-8s %s' % (who, vp.rsplit('/', 1)[-1]))
            for sn, t in shapes:
                print('      %-22s %s' % (sn, t))
    return 0


if __name__ == '__main__':
    sys.exit(main())