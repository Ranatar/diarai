# Разбор кандидатов в счётчики: ./cntan.py VT E LOG2N < census.txt  (строки censusl: code n1 n2 n3 black edge)
# отбор: не к краю, n3 < 3000, рост логарифмический (приращения за ×4 времени примерно равны);
# для каждого: моменты новых плиток до 2^LOG2N, множитель на плитку λ по второй половине,
# q = 1/log2(λ) — плиток на удвоение времени; печатает code n3 λ q и ближайшую простую дробь к q
import sys, subprocess, math
from fractions import Fraction
vt, e, lg = sys.argv[1], sys.argv[2], sys.argv[3]
for l in sys.stdin:
    c, n1, n2, n3, b, edge = map(int, l.split())
    if edge != -1 or n3 >= 3000 or n3 <= n2 or n2 <= n1 or n1 < 10: continue
    r = (n3 - n2) / (n2 - n1)
    if not 0.6 < r < 1.6: continue
    out = subprocess.run([vt, 'new', str(c), e, lg], capture_output=True, text=True).stdout.split('\n')
    T = [int(s.split()[1]) for s in out if s]
    if len(T) < 40 or T[-1] < 2**(int(lg) - 3): print(c, len(T), 'мало/рано'); continue
    if len(T) > 4000: print(c, len(T), 'растёт'); continue
    best = None
    for p in range(1, 80):
        if len(T) < 4 * p + 10: break
        rs = [T[n] / T[n - p] for n in range(len(T) - 2 * p, len(T))]
        if max(rs) / min(rs) < 1.002 and rs[-1] > 1.3: best = (p, rs[-1]); break
    if best: print(c, len(T), 'p=%d' % best[0], 'R=%.5f' % best[1], 'λ=%.5f' % best[1] ** (1 / best[0]), flush=True)
    else:
        lo = len(T) // 2; lam = (T[-1] / T[lo]) ** (1 / (len(T) - 1 - lo))
        print(c, len(T), 'период не найден, λ≈%.5f' % lam, '  <-- ?', flush=True)
