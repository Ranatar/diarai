"""proba_sravnit.py ДО ПОСЛЕ — корни словаря (обе ветви) в двух копиях Quettamin, различия.
Каждая копия считается в своём процессе (свой shared/). Снимки — ext/tmp/qm-snap-*.json. 2026-11-28."""
import sys, os, json, subprocess, collections
SNAP = r'''
import sys, os, json
sys.path.insert(0, '.')
from shared import lexicon as L
from shared.model import build
from shared.languages import BRANCHES
out = {}
for b in BRANCHES:
    for e in L.build_lexicon(b, build(b)['derivations']):
        out[b + ':' + e['id']] = [e['lang'], e['form'],
            sorted([r['form'], r.get('via', ''), r.get('part', 0)] for r in e.get('roots') or []),
            sorted(g['form'] for g in e.get('root_gaps') or [])]
json.dump(out, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False)
'''
snaps = []
for k, root in enumerate(sys.argv[1:3]):
    f = f'/home/diarai/diarai/ext/tmp/qm-snap-{k}.json'
    if not (len(sys.argv) > 3 and sys.argv[3] == '--keep' and os.path.exists(f)):
        subprocess.run([sys.executable, '-B', '-c', SNAP, f], cwd=root, check=True)
    snaps.append(json.load(open(f, encoding='utf-8')))
a, z = snaps
diff = [(k, a[k], z.get(k)) for k in a if a[k] != z.get(k)]
print('статей', len(a), 'различий', len(diff))
kinds = collections.Counter()
for k, x, y in diff:
    rx, ry = {r[0] for r in x[2]}, {r[0] for r in y[2]}
    kinds['корни найдены' if not rx and ry else 'корни потеряны' if rx and not ry else
          'корни добавлены' if rx < ry else 'корни убраны' if ry < rx else
          'корни заменены' if rx != ry else 'via/part/gaps'] += 1
print(dict(kinds))
for k, x, y in diff:
    print(f"  {k.split(':')[0][:1]} {x[0]}. {x[1]}: {[r[0] for r in x[2]]} {x[3]} -> {[r[0] for r in y[2]]} {y[3]}")
