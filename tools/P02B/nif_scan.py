# -*- coding: utf-8 -*-
"""Scan a NIF for every inline sized-string texture path (the real storage)."""
import os, struct, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'tools/P02B'); sys.path.insert(0, 'tools/P02A')
import p02a_common as C
PRINT = set(range(0x20, 0x7f)) | {0x09}
def all_tex(data):
    out = []
    for p in range(len(data) - 5):
        n = struct.unpack_from('<I', data, p)[0]
        if 8 <= n <= 260 and p + 4 + n <= len(data):
            body = data[p+4:p+4+n]
            if body[:9].lower() == b'textures\\' and body[-4:].lower() == b'.dds' and all(b in PRINT for b in body):
                out.append(body.decode('latin-1'))
    return out
ST = os.path.join('staging', 'ZLJ Combat Latex Pack - P02B Pilot')
tot_old = tot_new = tot_body = 0
for dp, _d, ns in os.walk(ST):
    for n in sorted(ns):
        if not n.lower().endswith('.nif'):
            continue
        p = os.path.join(dp, n)
        d = open(p, 'rb').read()
        tex = all_tex(d)
        old = [t for t in tex if t.lower().startswith('textures\\ae_toxic_cat\\')]
        new = [t for t in tex if t.lower().startswith('textures\\zlj\\combatlatex\\cl06_toxiccat\\')]
        body = [t for t in tex if t.lower().startswith('textures\\actors\\')]
        other = [t for t in tex if t not in old + new + body]
        tot_old += len(old); tot_new += len(new); tot_body += len(body)
        print('%-34s total=%-3d OLD_ae_toxic_cat=%-2d NEW_zlj=%-2d body=%-2d other=%s' %
              (n[:34], len(tex), len(old), len(new), len(body), other if other else 'none'))
print()
print('TOTALS  old_outfit_refs=%d  new_namespace_refs=%d  global_body_skin_refs=%d' % (tot_old, tot_new, tot_body))
print('old_refs_zero =', tot_old == 0)
