"""chuzhie_elementy.py QM_ROOT — слова, чьи элементы Quettamin берёт из ссылки с ДРУГОЙ формой
(_ref_elements: «else from all»), и есть ли у той ссылки <inflect> (форма слова: интенсив, мн. ч....).
Пример: ᴹQ tára ← ref antara (intensive) = an- → корни приставки an-. 2026-11-28."""
import sys, os, collections
ROOT = sys.argv[1]; sys.path.insert(0, ROOT); os.chdir(ROOT)
from shared import lexicon as L
W = L.words()
cnt = collections.Counter(); ex = collections.defaultdict(list)
for pid, w in W.by_id.items():
    if L._is_root(w) or [e for e in w.findall('element') if L._live_in(e, w)]:
        continue
    refs = [r for r in w.findall('ref') if L._live_in(r, w) and r.findall('element') and not L._names_itself(r, w)]
    if not refs: continue
    own = [r for r in refs if L._ref_key(r.get('v')) == L._ref_key(w.get('v'))]
    if own: cnt['своя форма'] += 1; continue
    most = max(len(r.findall('element')) for r in refs)
    r = next(r for r in refs if len(r.findall('element')) == most)
    k = 'чужая форма, с inflect' if r.findall('inflect') else 'чужая форма, без inflect'
    cnt[k] += 1
    ex[k].append(f"{w.get('l')}. {w.get('v')} ← {r.get('v')} [{','.join(i.get('form') or '' for i in r.findall('inflect'))}] = {' + '.join(e.get('v') or '?' for e in r.findall('element'))}")
print(dict(cnt))
for k in ex:
    print('==', k, len(ex[k]))
    for s in ex[k][:int(sys.argv[2]) if len(sys.argv) > 2 else 15]: print('  ', s)
