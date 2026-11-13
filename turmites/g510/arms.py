# Множитель счётчика-креста: ./arms.py newt.txt  (строки t x y из newt)
# для каждой руки (±x, ±y; ширина руки |поперёк| <= W) — моменты, когда рука удлиняется;
# печатает длину руки и отношения моментов t(n)/t(n-1) для последних новых концов
import sys, math
W = 6
arms = {'+x': [], '-x': [], '+y': [], '-y': []}
ext = dict.fromkeys(arms, 0)
for l in open(sys.argv[1]):
    t, x, y = map(int, l.split())
    for a, (u, v) in {'+x': (x, y), '-x': (-x, y), '+y': (y, x), '-y': (-y, x)}.items():
        if abs(v) <= W and u > ext[a]:
            ext[a] = u; arms[a].append((u, t))
for a, L in arms.items():
    if len(L) < 8: print(a, 'коротко', L[-3:]); continue
    tail = L[-12:]
    r = ['%d:%.4f' % (tail[i][0], tail[i][1] / tail[i-1][1]) for i in range(1, len(tail)) if tail[i-1][1] > 0]
    # средний множитель на единицу длины по последней трети
    (u0, t0), (u1, t1) = L[len(L)*2//3], L[-1]
    print(a, 'длина', L[-1][0], 'μ на ед. длины %.5f' % math.exp(math.log(t1/t0)/(u1-u0)), ' '.join(r))
