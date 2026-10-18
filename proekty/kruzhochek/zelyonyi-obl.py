"""Перепроверка «аномалии у зелёной вершины» замером, устойчивым к шуму счёта.
Мелкие клетки у вершины содержат 0,3–1,3 ожидаемых пикселя, их r — шум. Здесь клетки у вершины
объединяются в области по граням (грань G=1, грань R=0, грань B=0; расстояние до зелёного < D),
и для каждой области сравнивается доля пикселей с долей площади. Плюс те же области у красной и синей вершин
для сравнения. R=400, G=32 (клетки мелкие, области — сотни и тысячи пикселей).
python3 -I zelyonyi-obl.py [N] [--fv]
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iskazhenie as I  # noqa
import kub  # noqa
import kletki  # noqa
import moser  # noqa

args = [a for a in sys.argv[1:] if not a.startswith("--")]
N = int(args[0]) if args else 360
moser.FV = "--fv" in sys.argv
G, R = 32, 400
areas = kletki.cell_areas(G, sub=10)
cen = np.zeros((3, 2, G, G, 3))
for ax in range(3):
    o = [a for a in range(3) if a != ax]
    for s in range(2):
        u, v = np.meshgrid((np.arange(G) + .5) / G, (np.arange(G) + .5) / G, indexing="ij")
        cen[ax, s, ..., ax] = s; cen[ax, s, ..., o[0]] = u; cen[ax, s, ..., o[1]] = v
face = np.zeros((3, 2, G, G), int)
for ax in range(3):
    for s in range(2):
        face[ax, s] = 2 * ax + s  # 0: R=0, 1: R=1, 2: G=0, 3: G=1, 4: B=0, 5: B=1
names = ["R=0", "R=1", "G=0", "G=1", "B=0", "B=1"]
m = I.Moser(N, 32, surf=kub.surf)
tot_pix = None
for grade in (1, 2):
    moser.GRADE = grade
    yy, xx = np.mgrid[-R:R, -R:R] + 0.5
    X, Y = xx / R * 2, -yy / R * 2
    ok = X ** 2 + Y ** 2 < 4
    srgb = kletki.lin2srgb(kletki.ok2lin(kub.surf(m(X[ok], Y[ok]))))
    ax, s, u, v = kletki.cell_of(srgb, G)
    cnt = np.zeros_like(areas)
    np.add.at(cnt, (ax, s, u, v), 1)
    print("GRADE=%d (N=%d, FV=%s)" % (grade, N, moser.FV))
    for vname, vert in (("зелёная", (0, 1, 0)), ("красная", (1, 0, 0)), ("синяя", (0, 0, 1))):
        for D in (0.15, 0.3):
            near = np.linalg.norm(cen - np.array(vert), axis=-1) < D
            parts = []
            for f in range(6):
                msk = near & (face == f)
                if msk.sum() == 0:
                    continue
                exp = areas[msk].sum() / areas.sum() * cnt.sum()
                parts.append("%s: %d/%.0f=%.2f" % (names[f], cnt[msk].sum(), exp, cnt[msk].sum() / exp))
            print("  %-8s D<%.2f  %s" % (vname, D, "   ".join(parts)), flush=True)
