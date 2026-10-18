"""Локальные искажения карт «круг -> поверхность гаммы в OKLab», без квантования картинки.

Для каждой карты — функция: точки круга (X, Y в [-2, 2]) -> направление d на сфере.
Цвет = луч из серого до границы (otvet.boundary). Якобиан — конечными разностями (ε в долях пикселя).
Меры на выборке пикселей (сетка с шагом):
  площадь: A_lab / A_круг, нормировано на медиану -> доля пикселей, где отклонение > 10%, и p5..p95;
  анизотропия: σ₁/σ₂ якобиана 2x3 (1 = сохраняет форму малых кружков) -> медиана, p90.
Карты: «ламберт» (без выравнивания), «КР» (Кнёте — Розенблатт, широта, потом долгота — вихрь),
«КР-дол» (долгота, потом широта — швы), «Мозер» (поток).

python3 -I iskazhenie.py [R] [шаг]
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ravnaya  # noqa
import moser  # noqa
from otvet import boundary  # noqa

K = 2.0


def lambert_inv(X, Y):
    r2 = X ** 2 + Y ** 2
    f = np.sqrt(np.clip(1 - r2 / 4, 0, None))
    return np.stack([X * f, Y * f, 1 - r2 / 2], 1)


def sph(th, ph):
    return np.stack([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)], 1)


class KR:
    """Те же построения, что в ravnaya.py, но с дробными индексами (без округления до клетки)."""

    def __init__(self, NT=720):
        ravnaya.NT, ravnaya.NP = NT, 2 * NT
        self.NT, self.NP = NT, 2 * NT
        th, ph, lab, Frow, Fcol, dA = ravnaya.build(K)
        self.Frow, self.Fcol, self.dA = Frow, Fcol, dA
        col = dA.sum(0)
        self.Fc = np.concatenate([[0], np.cumsum(col)]) / col.sum()
        self.Fr = np.concatenate([np.zeros((1, self.NP)), np.cumsum(dA, 0)], 0) / col[None, :]

    blend = False  # True: условные доли смешиваются между соседними рядами (непрерывная версия)

    @staticmethod
    def _cond(x, idx, F, n_out, frac, blend, axis):
        """Обратить условную функцию распределения: ряд idx (или смесь idx и idx+1 с весом frac)."""
        out = np.empty_like(x)
        nmax = (F.shape[0] if axis == 0 else F.shape[1]) - 1
        for r in np.unique(idx):
            m = idx == r
            row = F[r] if axis == 0 else F[:, r]
            y0 = np.interp(x[m], row, np.arange(n_out + 1))
            if blend:
                r1 = min(r + 1, nmax) if axis == 0 else (r + 1) % nmax
                row1 = F[r1] if axis == 0 else F[:, r1]
                y1 = np.interp(x[m], row1, np.arange(n_out + 1))
                out[m] = (1 - frac[m]) * y0 + frac[m] * y1
            else:
                out[m] = y0
        return out

    def lat_first(self, X, Y):
        u = (X ** 2 + Y ** 2) / 4
        v = (np.arctan2(Y, X) % (2 * np.pi)) / (2 * np.pi)
        ti = np.interp(u, self.Frow, np.arange(self.NT + 1))
        c = np.clip(ti - 0.5, 0, self.NT - 1 - 1e-9) if self.blend else ti  # центры рядов
        i = np.clip(c.astype(int), 0, self.NT - 1)
        pj = self._cond(v, i, self.Fcol, self.NP, c - i, self.blend, 0)
        return sph(ti * np.pi / self.NT, pj * 2 * np.pi / self.NP)

    def lon_first(self, X, Y):
        u = (X ** 2 + Y ** 2) / 4
        v = (np.arctan2(Y, X) % (2 * np.pi)) / (2 * np.pi)
        pj = np.interp(v, self.Fc, np.arange(self.NP + 1))
        c = (pj - 0.5) % self.NP if self.blend else pj
        j = np.clip(c.astype(int), 0, self.NP - 1)
        ti = self._cond(u, j, self.Fr, self.NT, c - j, self.blend, 1)
        return sph(ti * np.pi / self.NT, pj * 2 * np.pi / self.NP)


class Moser:
    def __init__(self, N=180, steps=32, smooth=0, surf=None):
        self.rho, self.w = moser.fields(N, smooth, surf)
        self.steps = steps

    def __call__(self, X, Y):
        return moser.flow(lambert_inv(X, Y), self.rho, self.w, self.steps)


def measure(fmap, R=200, step=3, eps=0.25, surf=None):
    if surf is None:
        surf = lambda d: boundary(d, K)  # noqa: E731
    yy, xx = np.mgrid[-R:R:step, -R:R:step] + 0.5
    X, Y = (xx / R * 2).ravel(), (-yy / R * 2).ravel()
    keep = X ** 2 + Y ** 2 < (2 * (R - 3) / R) ** 2
    X, Y = X[keep], Y[keep]
    e = eps / R * 2
    P0 = surf(fmap(X, Y))
    Px = surf(fmap(X + e, Y))
    Py = surf(fmap(X, Y + e))
    J1, J2 = (Px - P0) / e, (Py - P0) / e  # столбцы якобиана в R³
    g11, g12, g22 = (J1 * J1).sum(1), (J1 * J2).sum(1), (J2 * J2).sum(1)
    area = np.sqrt(np.clip(g11 * g22 - g12 ** 2, 0, None))
    tr, det = g11 + g22, g11 * g22 - g12 ** 2
    disc = np.sqrt(np.clip(tr ** 2 / 4 - det, 0, None))
    s1, s2 = np.sqrt(tr / 2 + disc), np.sqrt(np.clip(tr / 2 - disc, 1e-30, None))
    an = s1 / s2
    a = area / np.median(area)
    return {
        "площадь p5": np.percentile(a, 5), "p95": np.percentile(a, 95),
        "|откл|>10%": 100 * (np.abs(a - 1) > 0.1).mean(),
        "аниз. медиана": np.median(an), "аниз. p90": np.percentile(an, 90),
        "аниз. ср. ln": np.log(an).mean(),
    }


if __name__ == "__main__":
    R = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    step = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    kr = KR()
    krb = KR(); krb.blend = True
    maps = [("ламберт", lambda X, Y: lambert_inv(X, Y)), ("КР (вихрь)", kr.lat_first),
            ("КР-дол (швы)", kr.lon_first), ("КР непрер.", krb.lat_first),
            ("КР-дол непр.", krb.lon_first), ("Мозер", Moser())]
    keys = None
    for name, f in maps:
        r = measure(f, R, step)
        if keys is None:
            keys = list(r)
            print("%-14s" % "" + "".join("%15s" % k for k in keys))
        print("%-14s" % name + "".join("%15.3f" % r[k] for k in keys))
