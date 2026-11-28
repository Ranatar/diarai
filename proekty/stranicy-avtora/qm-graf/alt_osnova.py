"""alt_osnova.py QM_ROOT — основа нео-слова (alt_word, 3.24: alt_source) против слова, на которое
указывают заметки Eldamo (<see-notes>), когда это слово вложено в статью нео-слова и у него есть ссылки.
Пример: ᴺQ. yaxë: alt_word → ᴱQ. mui (заменён на yaxë), see-notes → ᴱQ. yaksi (сам источник). 2026-11-28."""
import sys, os, collections
ROOT = sys.argv[1]; sys.path.insert(0, ROOT); os.chdir(ROOT)
from shared import lexicon as L
W = L.words()
cnt = collections.Counter(); ex = []
for pid, w in W.by_id.items():
    a = L.alt_word(w)
    if a is None: continue
    sn = w.find('see-notes')
    if sn is None: cnt['без see-notes'] += 1; continue
    if (sn.get('l'), sn.get('v')) == (a.get('l'), a.get('v')): cnt['совпадает'] += 1; continue
    nested = [x for x in w.iter('word') if x is not w and (x.get('l'), x.get('v')) == (sn.get('l'), sn.get('v')) and x.find('ref') is not None]
    if nested:
        cnt['see-notes — другое вложенное слово'] += 1
        ex.append(f"{w.get('l')}. {w.get('v')} “{w.get('gloss')}”: alt → {a.get('l')}. {a.get('v')} “{a.get('gloss')}”; see-notes → {sn.get('l')}. {sn.get('v')} “{nested[0].get('gloss')}”")
    else:
        cnt['see-notes — не вложено'] += 1
print(dict(cnt))
for s in ex[:int(sys.argv[2]) if len(sys.argv) > 2 else 40]: print(' ', s)
