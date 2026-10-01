# -*- coding: utf-8 -*-
import sys, gzip, json, collections
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'tools/P02A')
import p02a_common as C
nifs = json.load(gzip.open(r'data/P00_RERUN/08_nif_parsed.json.gz', 'rt', encoding='utf-8'))
idx = collections.defaultdict(list)
for n in nifs:
    idx[C.norm(n['path'])].append(n)
targets = [
    'meshes/ae_corruptedbodysuit/ae_corruptedbodysuit_feet_0.nif',
    'calientetools/bodyslide/shapedata/ae_corruptedbodysuit_feet/ae_corruptedbodysuit_feet.nif',
    'calientetools/bodyslide/shapedata/ae_corruptedbodysuit_feet.nif',
    'calientetools/bodyslide/shapedata/ae_corruptedbodysuit/ae_corruptedbodysuit.nif',
    'calientetools/bodyslide/shapedata/ae_corruptedbodysuit.nif',
]
for vp in targets:
    print('==', vp)
    for n in idx[C.norm(vp)]:
        mod = 'REWORK' if 'Latex Rework' in n['source_mod'] else 'BASE'
        print('  ', mod, '| class=', n.get('nif_class'), '| shapes=', [s['name'] for s in n['shapes']])
        for s in n['shapes']:
            t = {k: v for k, v in (s.get('textures') or {}).items() if v}
            if t:
                print('       ', s['name'], '->', t)
    print()