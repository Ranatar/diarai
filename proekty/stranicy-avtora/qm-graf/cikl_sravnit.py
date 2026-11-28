"""cikl_sravnit.py QM_ROOT — корни словаря до и после защиты от циклов в _root_groups.
Защита: слово, которое уже на стеке рекурсии, ничего не даёт (а не только пара (слово, глубина)).
Пишет различия: корни, via, длина путей. 2026-11-28."""
import sys, os, json, collections
ROOT = sys.argv[1]
sys.path.insert(0, ROOT); os.chdir(ROOT)
from shared import lexicon as L
from shared.model import build
from shared.languages import BRANCHES

def snap(lex):
    out = {}
    for e in lex:
        rs = e.get('roots') or []
        out[e['id']] = (e['lang'], e['form'],
                        tuple(sorted((r['id'], r.get('via', ''), r.get('part', 0)) for r in rs)),
                        tuple(sorted(len(r.get('path') or []) for r in rs)),
                        tuple(sorted(g['id'] for g in e.get('root_gaps') or [])))
    return out

orig = L._root_groups
stack = set()
def guarded(W, pid, memo, depth=L.ROOT_DEPTH):
    if pid in stack:
        return []
    stack.add(pid)
    try:
        return orig(W, pid, memo, depth)
    finally:
        stack.discard(pid)

res = {}
for b in BRANCHES:
    der = build(b)['derivations']
    L._root_groups = orig
    a = snap(L.build_lexicon(b, der))
    L._root_groups = guarded
    z = snap(L.build_lexicon(b, der))
    L._root_groups = orig
    diff = [(k, a[k], z.get(k)) for k in a if a[k] != z.get(k)]
    print(b, 'статей', len(a), 'различий', len(diff))
    kinds = collections.Counter()
    for k, x, y in diff:
        if x[2] and not y[2]: kinds['корни потеряны'] += 1
        elif not x[2] and y[2]: kinds['корни найдены'] += 1
        elif {r[0] for r in x[2]} != {r[0] for r in y[2]}: kinds['другие корни'] += 1
        elif x[2] != y[2]: kinds['те же корни, другая via/part'] += 1
        elif x[3] != y[3]: kinds['только длина пути'] += 1
        else: kinds['только пробелы (gaps)'] += 1
    print('  ', dict(kinds))
    for k, x, y in diff[:25]:
        print('   ', x[0], x[1], '|', x[2], x[3], '->', y[2] if y else None, y[3] if y else None)
