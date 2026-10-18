"""Сходимость Мозера по сетке N и числу шагов RK4 (iskazhenie.measure)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iskazhenie as I  # noqa

for N, st in ((180, 64), (360, 32), (360, 64), (720, 64)):
    r = I.measure(I.Moser(N, st), 200, 3)
    print(N, st, {k: round(float(v), 3) for k, v in r.items()}, flush=True)
