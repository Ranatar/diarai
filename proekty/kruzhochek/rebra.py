"""Догадка: вдоль рёбер куба «куб + Мозер» собирает лишние (или недобирает) пиксели.
Мелкие клетки G×G на грани; отношение доли пикселей к доле площади отдельно для клеток,
примыкающих к ребру грани (u или v крайние), и внутренних. Шум счёта ~ 1/√(пикселей в клетке).
python3 -I rebra.py [R] [G] [N]
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iskazhenie as I  # noqa
import kub  # noqa
import kletki  # noqa

R = int(sys.argv[1]) if len(sys.argv) > 1 else 800
G = int(sys.argv[2]) if len(sys.argv) > 2 else 32
N = int(sys.argv[3]) if len(sys.argv) > 3 else 360
areas = kletki.cell_areas(G, sub=10)
r, w = kletki.check(I.Moser(N, 32, surf=kub.surf), kub.surf, R, G, areas)
r = r.reshape(3, 2, G, G)
u, v = np.meshgrid(np.arange(G), np.arange(G), indexing="ij")
ring = np.minimum(np.minimum(u, G - 1 - u), np.minimum(v, G - 1 - v))  # 0 — у ребра
print("пикселей на клетку в среднем: %.0f (шум ~%.1f%%)" % (np.pi * R * R / r.size, 100 / np.sqrt(np.pi * R * R / r.size)))
for k in range(4):
    m = np.broadcast_to(ring == k, r.shape)
    print("кольцо %d от ребра: клеток %4d, медиана r %.3f, среднее r %.3f" % (k, m.sum(), np.median(r[m]), r[m].mean()))
m = np.broadcast_to(ring >= 4, r.shape)
print("внутри (≥4):      клеток %4d, медиана r %.3f, среднее r %.3f" % (m.sum(), np.median(r[m]), r[m].mean()))
