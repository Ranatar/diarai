"""neozhidannoe.py QM_ROOT [--pozdnie] [N] — «неожиданные этимологии» в Quettamin: пары слов от одного корня
только по прямым выводам (шаги 'd' в пути к корню, без элементов и сложений), чьи смысловые группы Eldamo
(первые две буквы cat=, группы Бака: PW мир, BP тело, EM чувства, MT ум, RB вера…) редко сходятся под одним корнем.
Мера: PMI сочетания групп по всем корням (чем ниже при наличии — тем неожиданнее) + число групп у корня.
--pozdnie: только поздние q, s (иначе все концепции). 2026-11-28, по вопросу автора в hello_there."""
import sys, os, collections, math, itertools
ROOT = sys.argv[1]; sys.path.insert(0, ROOT); os.chdir(ROOT)
args = sys.argv[2:]
LATE = '--pozdnie' in args
N = int(next((a for a in args if a.isdigit()), 40))
from shared.lexicon import words
from shared.pipeline import load_all
W = words(); B = load_all()
by_root = collections.defaultdict(dict)   # rid -> {wid: (lang, form, gloss, grp)}
seen = set()
for br, d in B.items():
    for e in d['lexicon']:
        if e['id'] in seen: continue
        seen.add(e['id'])
        if LATE and e['lang'] not in ('q', 's'): continue
        if e['lang'] in ('p', 'mp', 'ep', 'np'): continue
        w = W.by_id.get(e['id'])
        grp = ((w.get('cat') if w is not None else '') or '')[:2]
        if not grp or grp in ('GR', '?'): continue
        for r in e.get('roots') or []:
            if r.get('via') or r.get('part') is not None: continue
            if all(s == 'd' for s, _ in r.get('path') or []):
                by_root[r['id']][e['id']] = (e['lang'], e['form'], e.get('gloss') or '', grp)
# co-occurrence of groups under roots
cnt = collections.Counter(); pair = collections.Counter(); nroots = 0
for rid, ws in by_root.items():
    gs = {v[3] for v in ws.values()}
    if len(ws) < 2: continue
    nroots += 1
    for g in gs: cnt[g] += 1
    for a, b in itertools.combinations(sorted(gs), 2): pair[(a, b)] += 1
def pmi(a, b):
    a, b = sorted((a, b)); p = pair[(a, b)] / nroots
    return math.log(p / ((cnt[a] / nroots) * (cnt[b] / nroots)))
rows = []
for rid, ws in by_root.items():
    items = list(ws.values())
    for x, y in itertools.combinations(items, 2):
        if x[3] == y[3]: continue
        rows.append((pmi(x[3], y[3]), rid, x, y))
rows.sort(key=lambda r: r[0])
print(f'корней с ≥2 производными: {nroots}; пар разных групп: {len(rows)}')
shown = collections.Counter()
for s, rid, x, y in rows:
    if shown[rid] >= 2: continue
    shown[rid] += 1
    r = W.by_id[rid]
    print(f"{s:+.2f} √{r.get('v')} «{r.get('gloss') or ''}»: {x[0]}. {x[1]} «{x[2]}» [{x[3]}] ~ {y[0]}. {y[1]} «{y[2]}» [{y[3]}]")
    if sum(shown.values()) >= N: break
