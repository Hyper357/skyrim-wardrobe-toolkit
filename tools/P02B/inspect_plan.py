# -*- coding: utf-8 -*-
import csv, sys
sys.stdout.reconfigure(encoding='utf-8')
rows = list(csv.DictReader(open('reports/P02B/P02B_CL06_PILOT_PLUGIN_PLAN.csv', encoding='utf-8-sig')))
def show(pred, label, n=3):
    print('==', label)
    sel = [r for r in rows if pred(r)][:n]
    for r in sel:
        print('   %-24s %-5s %-30s' % (r['edid'][:24], r['slot_field'], r['change_class']))
        print('        old_value                  = %s' % r['old_value'])
        print('        new_value                  = %s' % (r['new_value'] or '(EMPTY)'))
        print('        target_virtual_mesh_path   = %s' % (r['target_virtual_mesh_path'] or '(n/a)'))
        print('        target_plugin_model_path   = %s' % (r['target_plugin_model_path'] or '(n/a)'))
show(lambda r: r['change_class'] == 'MODEL_PATH_REPOINT' and r['slot_field'] == 'MOD5', 'female 3P/1P shared (MOD5)')
show(lambda r: r['change_class'] == 'GENDER_NEUTRAL_SHARED_REPOINT', 'gender-neutral shared', 2)
show(lambda r: r['change_class'] == 'MALE_SLOT_EMPTY', 'external male -> empty', 2)
show(lambda r: r['change_class'] == 'ARMO_WORLD_NO_CHANGE', 'ARMO world model', 1)
show(lambda r: r['change_class'] == 'TXST_REPOINT', 'TXST repoint', 2)
