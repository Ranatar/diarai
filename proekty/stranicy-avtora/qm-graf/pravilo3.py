"""pravilo3.py QM_ROOT — слова, где правило 3 (_root_groups: один элемент с корнем) отбрасывает
корни из вывода через праформу/слово (правило 4), и эти корни НЕ совпадают с корнем элемента.
Пример: ᴹQ tára = [an-] (из ref antara) → A, N-; а вывод < ✶tārā → √TĀ. 2026-11-28."""
import sys, os
ROOT = sys.argv[1]; sys.path.insert(0, ROOT); os.chdir(ROOT)
from shared import lexicon as L
W = L.words(); memo = {}
rows = []
for pid, w in W.by_id.items():
    if L._is_root(w): continue
    parts = L._part_groups(W, pid, memo, L.ROOT_DEPTH)
    real = [g for g in parts if L._real(g)]
    if len(real) != 1: continue
    derived = L._derived_from(W, w, elements=False)
    if any(L._is_root(W.by_id[d]) for d in derived): continue
    inter = set()
    for d in derived:
        for g in L._root_groups(W, d, memo, L.ROOT_DEPTH - 1):
            inter |= {r['form'] for r in L._real(g)}
    el = {r['form'] for r in L._real(real[0])}
    if inter and not (inter & el):
        eid = real[0][0].get('path', [[None, None]])[0][1]
        ew = W.by_id.get(eid)
        rows.append(f"{w.get('l')}. {w.get('v')} “{w.get('gloss') or ''}”: элемент {ew.get('l') + '. ' + ew.get('v') if ew is not None else '?'} → {sorted(el)}; вывод → {sorted(inter)}")
print('слов:', len(rows))
for r in rows: print(' ', r)
