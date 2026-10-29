"""Разбор выводов fastfly/fastfly2: python3 escapes.py DIR [N=16384]
Подозрительные — вышли за край, а рамка на последней контрольке < 0,7·N (тело так быстро не дорастёт: кандидат в шоссе).
Кандидата перепроверить на поле 32768 (тот же момент выхода ± расстояние/скорость → шоссе) и onsetr."""
import sys, glob, os, re
d = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 16384
for f in sorted(glob.glob(os.path.join(d, '*.txt')), key=lambda p: int(re.sub(r'\D', '', os.path.basename(p)) or 0)):
    L = open(f).read().split('\n'); r = os.path.basename(f)[:-4]
    cps = [l for l in L if l.startswith('2^')]; esc = [l for l in L if l.startswith('escape')]
    last = cps[-1] if cps else ''
    m = re.search(r'w=(\d+) h=(\d+)', last); w, h = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    tag = ''
    if esc:
        tag = 'ПОДОЗР' if max(w, h) < 0.7 * N else 'край'
    print(f"{r:>6} {tag:7} {last[:70]:70} {esc[0] if esc else ''}")
