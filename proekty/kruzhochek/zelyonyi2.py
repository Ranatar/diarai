"""Быстрая проверка лечения: сгущение шагов к t = 1 (moser.GRADE). R=400, G=16 (~650 пикселей на клетку).
Печатает max/min r по всем клеткам и по клеткам у зелёной вершины, и взвешенную ошибку.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iskazhenie as I  # noqa
import kub  # noqa
import kletki  # noqa
import moser  # noqa

G = 16
areas = kletki.cell_areas(G, sub=20)
# центры клеток в sRGB -> близость к зелёному
cen = np.zeros((3, 2, G, G, 3))
for ax in range(3):
    o = [a for a in range(3) if a != ax]
    for s in range(2):
        u, v = np.meshgrid((np.arange(G) + .5) / G, (np.arange(G) + .5) / G, indexing="ij")
        cen[ax, s, ..., ax] = s; cen[ax, s, ..., o[0]] = u; cen[ax, s, ..., o[1]] = v
near = (np.linalg.norm(cen - np.array([0, 1, 0]), axis=-1) < 0.2).ravel()
N = int(sys.argv[1]) if len(sys.argv) > 1 else 360
runs = [tuple(float(x) for x in a.split(":")) for a in sys.argv[2:] if not a.startswith("--")] or [(1, 32), (2, 32), (3, 32)]
moser.FV = "--fv" in sys.argv
runs = [r for r in runs if r]
print("N=%d FV=%s" % (N, moser.FV), flush=True)
m = I.Moser(N, 32, surf=kub.surf)  # поле одно, меняется только интегрирование
for grade, st in runs:
    st = int(st)
    moser.GRADE = grade
    m.steps = st
    r, w = kletki.check(m, kub.surf, 400, G, areas)
    print("GRADE=%g шагов=%d: все клетки r∈[%.2f, %.2f], у зелёного r∈[%.2f, %.2f], взвеш. ошибка %.4f" % (
        grade, st, r.min(), r.max(), r[near].min(), r[near].max(), (w * np.abs(r - 1)).sum()), flush=True)
