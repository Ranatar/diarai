"""sblizheniya.py [N] — «сближения» в графе Quettamin: пары поздних слов (q, s; можно и q~q, s~s), похожих
и формой (SequenceMatcher по свёрнутой форме ≥ 0,75), и глоссой (общее содержательное английское слово),
у которых НЕТ общего источника по строгим связям (deriv, element, combine, merged, filed, rootderiv)
и нет связи-когната. Кандидаты в «народную этимологию» внутри мира или в забытое родство.
Данные — кэш graf.py (ext/tmp/qm-graf.json). 2026-11-28."""
import json, collections, sys, re, difflib, unicodedata
g = json.load(open('/home/diarai/diarai/ext/tmp/qm-graf.json'))
Nn, E, R = g['nodes'], g['edges'], g['rels']
STRICT = {'deriv', 'element', 'combine', 'merged', 'filed', 'rootderiv'}
up = collections.defaultdict(set); cog = set()
for e in E:
    if R[e[2]] in STRICT: up[e[1]].add(e[0])
    if R[e[2]] in ('cognates', 'cognate', 'see', 'instead'): cog.add((e[0], e[1])); cog.add((e[1], e[0]))
memo = {}
def anc(i):
    if i in memo: return memo[i]
    s, t = {i}, [i]
    while t:
        for y in up[t.pop()]:
            if y not in s: s.add(y); t.append(y)
    memo[i] = s; return s
STOP = set('a an the of to in on for with by from as at or and be (lit.) lit thing one that which is make cause made'.split())
def fold(f):
    f = unicodedata.normalize('NFD', f.lower()); f = ''.join(c for c in f if not unicodedata.combining(c))
    return re.sub(r'[^a-zþðŋ]', '', f).replace('k', 'c').replace('ph', 'f')
def gw(gl): return {w for w in re.findall(r"[a-z]+", (gl or '').lower()) if w not in STOP and len(w) > 2}
late = [i for i, n in enumerate(Nn) if n['l'] in ('q', 's') and n['k'] == 'word' and not n.get('x') and n.get('g')]
byk = collections.defaultdict(list)
for i in late:
    for w in gw(Nn[i]['g']): byk[w].append(i)
pairs = set()
for w, ids in byk.items():
    if len(ids) > 60: continue          # слишком общие слова глосс
    for a in ids:
        for b in ids:
            if a < b and (a, b) not in pairs:
                fa, fb = fold(Nn[a]['f']), fold(Nn[b]['f'])
                if min(len(fa), len(fb)) < 3: continue
                r = difflib.SequenceMatcher(None, fa, fb).ratio()
                if r >= 0.75 and fa != fb and (a, b) not in cog and not (anc(a) & anc(b)):
                    pairs.add((a, b))
rows = sorted(pairs, key=lambda p: -difflib.SequenceMatcher(None, fold(Nn[p[0]]['f']), fold(Nn[p[1]]['f'])).ratio())
print('пар:', len(rows))
def roots(i): return sorted(Nn[x]['f'] for x in anc(i) if Nn[x]['k'] == 'root') or ['—']
for a, b in rows[:int(sys.argv[1]) if len(sys.argv) > 1 else 40]:
    print(f"  {Nn[a]['l']}. {Nn[a]['f']} «{Nn[a]['g']}» {roots(a)}  ~  {Nn[b]['l']}. {Nn[b]['f']} «{Nn[b]['g']}» {roots(b)}")
