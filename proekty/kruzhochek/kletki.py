"""Проверка равновеликости без производных: грани куба режутся на G×G клеток (6G² клеток),
площадь каждой клетки в OKLab считается мелкой триангуляцией, пиксели круга раскладываются по клеткам
по своему цвету (OKLab -> sRGB -> ближайшая грань). Отношение (доля пикселей)/(доля площади) по клеткам.
Складки не мешают: клетки не пересекают рёбер куба.
python3 -I kletki.py [R] [G] [N]
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iskazhenie as I  # noqa
import kub  # noqa
from otvet import boundary, ok2lin, lin2ok, lin2srgb  # noqa


def cell_areas(G, sub=40):
    n = G * sub
    t = np.linspace(0, 1, n + 1)
    U, V = np.meshgrid(t, t, indexing="ij")
    out = np.zeros((3, 2, G, G))
    for ax in range(3):
        o = [a for a in range(3) if a != ax]
        for s, val in enumerate((0.0, 1.0)):
            p = np.zeros((n + 1, n + 1, 3))
            p[..., ax] = val; p[..., o[0]] = U; p[..., o[1]] = V
            lab = lin2ok(kub.srgb2lin(p).reshape(-1, 3)).reshape(n + 1, n + 1, 3)
            a, b, c, d = lab[:-1, :-1], lab[1:, :-1], lab[:-1, 1:], lab[1:, 1:]
            ar = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=-1) + 0.5 * np.linalg.norm(np.cross(b - d, c - d), axis=-1)
            out[ax, s] = ar.reshape(G, sub, G, sub).sum((1, 3))
    return out


def cell_of(srgb, G):
    dist = np.minimum(srgb, 1 - srgb)
    ax = np.argmin(dist, 1)
    idx = np.arange(len(srgb))
    s = (srgb[idx, ax] > 0.5).astype(int)
    o0 = np.where(ax == 0, 1, 0)
    o1 = np.where(ax == 2, 1, 2)
    u = np.clip((srgb[idx, o0] * G).astype(int), 0, G - 1)
    v = np.clip((srgb[idx, o1] * G).astype(int), 0, G - 1)
    return ax, s, u, v


def check(fmap, surf, R, G, areas):
    yy, xx = np.mgrid[-R:R, -R:R] + 0.5
    X, Y = xx / R * 2, -yy / R * 2
    ok = X ** 2 + Y ** 2 < 4
    lab = surf(fmap(X[ok], Y[ok]))
    srgb = lin2srgb(ok2lin(lab))  # lin2srgb обрезает в [0,1]
    ax, s, u, v = cell_of(srgb, G)
    cnt = np.zeros_like(areas)
    np.add.at(cnt, (ax, s, u, v), 1)
    ratio = (cnt / cnt.sum()) / (areas / areas.sum())
    return ratio.ravel(), areas.ravel() / areas.sum()


if __name__ == "__main__":
    R = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    G = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    N = int(sys.argv[3]) if len(sys.argv) > 3 else 360
    areas = cell_areas(G)
    okray = lambda d: boundary(d, I.K)  # noqa: E731
    kr = I.KR(); kr.blend = True
    variants = [("OKLab-луч", I.lambert_inv, okray), ("КР непрер.", kr.lat_first, okray),
                ("КР-дол непр.", kr.lon_first, okray),
                ("OKLab+Мозер", I.Moser(N, 32, surf=okray), okray),
                ("куб-луч", I.lambert_inv, kub.surf), ("куб+Мозер", I.Moser(N, 32, surf=kub.surf), kub.surf)]
    print("клеток %d, пикселей в среднем на клетку %.0f" % (areas.size, np.pi * R * R / areas.size))
    print("%-14s %8s %8s %8s %12s %14s" % ("", "p5", "медиана", "p95", "|r-1|>10%", "взвеш.|r-1|"))
    for name, f, s in variants:
        r, w = check(f, s, R, G, areas)
        print("%-14s %8.3f %8.3f %8.3f %11.1f%% %14.3f" % (name, *np.percentile(r, [5, 50, 95]),
                                                       100 * (np.abs(r - 1) > 0.1).mean(), (w * np.abs(r - 1)).sum()), flush=True)
