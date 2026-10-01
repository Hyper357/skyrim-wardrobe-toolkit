# -*- coding: utf-8 -*-
"""Package reports/P02B with the current content."""
import os, sys, zipfile
sys.stdout.reconfigure(encoding='utf-8')
root = os.path.join('reports', 'P02B')
out = os.path.join(root, 'P02B.zip')
if os.path.exists(out):
    os.remove(out)
files = sorted(f for f in os.listdir(root)
               if os.path.isfile(os.path.join(root, f)) and f != 'P02B.zip')
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for f in files:
        z.write(os.path.join(root, f), 'P02B/' + f)
print('packaged %d files, %.1f KB' % (len(files), os.path.getsize(out) / 1024.0))
with zipfile.ZipFile(out) as z:
    print('entries:', len(z.namelist()), '| integrity:',
          'OK' if z.testzip() is None else 'CORRUPT')