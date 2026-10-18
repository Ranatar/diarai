"""Где у «куб-луч + Мозер» ошибка площади: по светлоте точки и по близости к вершинам куба. И max ρ по N."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iskazhenie as I  # noqa
import moser  # noqa
import kub  # noqa

for N in (180, 360, 720):
    th, ph, rho = moser.density_of(kub.surf, N)
    i, j = np.unravel_index(np.argmax(rho), rho.shape)
    d = np.array([[np.sin(th[i]) * np.cos(ph[j]), np.sin(th[i]) * np.sin(ph[j]), np.cos(th[i])]])
    print("N=%d max ρ=%.1f в точке куба %s; доля массы в клетках с ρ>10: %.3f" % (
        N, rho.max(), np.round(kub.cube_point(d)[0], 3),
        (rho * np.sin(th)[:, None])[rho > 10].sum() / (rho * np.sin(th)[:, None]).sum()))

R, step, e = 200, 3, 0.25 / 200 * 2
m = I.Moser(720, 32, surf=kub.surf)
yy, xx = np.mgrid[-R:R:step, -R:R:step] + 0.5
X, Y = (xx / R * 2).ravel(), (-yy / R * 2).ravel()
keep = X ** 2 + Y ** 2 < (2 * (R - 3) / R) ** 2
X, Y = X[keep], Y[keep]
d0 = m(X, Y)
P0, Px, Py = kub.surf(d0), kub.surf(m(X + e, Y)), kub.surf(m(X, Y + e))
J1, J2 = (Px - P0) / e, (Py - P0) / e
area = np.linalg.norm(np.cross(J1, J2), axis=1)
a = area / np.median(area)
bad = np.abs(a - 1) > 0.1
c = kub.cube_point(d0)
L = P0[:, 0]
print("плохих: %.1f%%" % (100 * bad.mean()))
for lo, hi in ((0, .2), (.2, .4), (.4, .6), (.6, .8), (.8, 1.01)):
    s = (L >= lo) & (L < hi)
    print("  L в [%.1f,%.1f): точек %5d, плохих %.1f%%, медиана a %.3f" % (lo, hi, s.sum(), 100 * bad[s].mean(), np.median(a[s])))
# близость к ребру куба: две координаты на границе
edge = (np.isclose(c, 0, atol=0.02) | np.isclose(c, 1, atol=0.02)).sum(1) >= 2
print("  у рёбер куба (2 коорд. у границы): точек %d, плохих %.1f%%; вдали: плохих %.1f%%" % (
    edge.sum(), 100 * bad[edge].mean(), 100 * bad[~edge].mean()))
