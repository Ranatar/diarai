"""kognaty.py — пары когнатов Eldamo (ребро cognates графа Quettamin): у скольких есть общий
источник по строгим связям происхождения (deriv, element, combine; и связи корней merged/filed/rootderiv).
Запуск: python3 -I kognaty.py [примеры]. Данные — кэш graf.py (ext/tmp/qm-graf.json). 2026-11-28."""
import json, collections, sys
g = json.load(open('/home/diarai/diarai/ext/tmp/qm-graf.json'))
N, E, R, ids = g['nodes'], g['edges'], g['rels'], g['ids']
STRICT = {'deriv', 'element', 'combine', 'merged', 'filed', 'rootderiv'}
up = collections.defaultdict(set)
for e in E:
    if R[e[2]] in STRICT: up[e[1]].add(e[0])
memo = {}
def anc(i):
    if i in memo: return memo[i]
    seen, todo = {i}, [i]
    while todo:
        for y in up[todo.pop()]:
            if y not in seen: seen.add(y); todo.append(y)
    memo[i] = seen; return seen
def nm(i): n = N[i]; return f"{n['l']}. {n['f']}"
pairs = [(e[0], e[1]) for e in E if R[e[2]] == 'cognates']
kinds = collections.Counter(); ex = collections.defaultdict(list)
for a, b in pairs:
    A, B = anc(a), anc(b)
    if N[a].get('cg') or N[b].get('cg'): k = 'один из пары вне ветвей (cg)'
    elif A & B: k = 'общий источник есть'
    elif not any(N[x]['k'] == 'root' for x in A) or not any(N[x]['k'] == 'root' for x in B): k = 'у одного нет корня'
    else: k = 'оба с корнями, общих нет'
    kinds[k] += 1; ex[k].append((a, b))
print('пар', len(pairs)); [print(' ', k, v) for k, v in kinds.most_common()]
if len(sys.argv) > 1:
    for a, b in ex['оба с корнями, общих нет'][:int(sys.argv[1])]:
        ra = sorted(N[x]['f'] for x in anc(a) if N[x]['k'] == 'root'); rb = sorted(N[x]['f'] for x in anc(b) if N[x]['k'] == 'root')
        print(f"  {nm(a)} {ra}  ~  {nm(b)} {rb}")
