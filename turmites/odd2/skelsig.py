"""Подпись по скелету: строка поворотов сжатого пути (без лепестков), окна длины W при сдвигах 0..8, с зеркалом.
python3 odd2/skelsig.py N W > odd2/skelsig.txt — пары классов с общим окном"""
import sys, csv, collections
sys.path.insert(0, 'odd2')
from allpairs import skel
N, W = int(sys.argv[1]), int(sys.argv[2])
cat = {int(r['rep']): r for r in csv.DictReader(open('catalog2.csv'))}
D = {(0,-1):0,(1,0):1,(0,1):2,(-1,0):3}
by = collections.defaultdict(set)
for r, row in cat.items():
    if row['kind'] not in ('chaotic', 'ordered', 'counter', 'slow'): continue
    p = skel(r, N)
    ds = [D.get((b[0]-a[0], b[1]-a[1])) for a, b in zip(p, p[1:])]
    if None in ds or len(ds) < W + 12: continue
    t = ''.join('NRUL'[(b-a) & 3] for a, b in zip(ds, ds[1:]))
    m = t.translate(str.maketrans('LR', 'RL'))
    for o in range(9):
        by[t[o:o+W]].add(r); by[m[o:o+W]].add(r)
pairs = set()
for k, rs in by.items():
    rs = sorted(rs)
    for x in rs[1:]: pairs.add((rs[0], x))
for a, b in sorted(pairs):
    print(a, b, cat[a]['kind'], cat[b]['kind'], cat[a]['twin'] or '-', cat[b]['twin'] or '-')
