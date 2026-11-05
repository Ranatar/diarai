"""Калибровка направления: поворот' = поворот + g(новое) - g(старое), g(0)=0, g(1)=k.
Для каждого класса каталога — в какой класс попадает калиброванное правило.
python3 odd2/gauge.py > odd2/gauge.txt   (из turmites/)"""
import csv, collections, sys, os
sys.path.insert(0, os.getcwd())
from analyze import entries, pack
from canon2 import CANON2
from canon3 import CANON3
cat = {int(r['rep']): r for r in csv.DictReader(open('catalog2.csv'))}
def gauge(r, k):
    g = (0, k); e = entries(r)
    return pack([(w, (t + g[n] - g[s]) & 3, n) for (s, (w, t, n)) in zip((0, 0, 1, 1), e)])
cls = lambda r: CANON3.get(CANON2[r], CANON2[r])
par = {}
def find(a):
    while par.setdefault(a, a) != a: a = par[a]
    return a
for r in cat:
    for k in (1, 2, 3):
        c = cls(gauge(r, k))
        if c != r:
            print(r, k, c, cat[r]['kind'], cat.get(c, {}).get('kind', '-'))
            a, b = find(r), find(c)
            if a != b: par[max(a, b)] = min(a, b)
G = collections.defaultdict(list)
for r in cat: G[find(r)].append(r)
print('# классов', len(cat), '-> после калибровки', len(G))
K = collections.Counter(cat[r]['kind'] for r in G)
print('#', dict(K))
