"""Замер ровности: насколько различаются для глаза (ΔE в OKLab) соседние пиксели карты.

Сравниваются две карты, построенные одинаково (обратный ход, Ламберт, белое полушарие),
но с лучом в разных пространствах:
  ok  — луч из серого L=0.5 в OKLab (otvet.py),
  rgb — луч из (0.5,0.5,0.5) в sRGB-кубе, серая диагональ вертикально (как у автора).
Ровная карта: ΔE на шаг пикселя почти одинаковый всюду. Мера — отношение 95-го к 5-му процентилю
и коэффициент вариации.
python3 -I zamer.py
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otvet import hemisphere, lin2ok, ok2lin, boundary  # noqa

R = 256


def srgb2lin(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def rgb_hemisphere(R):
    s3, s2 = 1 / np.sqrt(3), 1 / np.sqrt(2)
    # базис: ось z — серая диагональ (белое вверх), как поворот в эскизах автора
    ez = np.array([s3, s3, s3])
    ex = np.array([s2, -s2, 0])
    ey = np.cross(ez, ex)
    yy, xx = np.mgrid[-R:R, -R:R] + 0.5
    X, Y = xx / R * np.sqrt(2), -yy / R * np.sqrt(2)
    rho2 = X ** 2 + Y ** 2
    ok = rho2 <= 2
    f = np.sqrt(np.clip(1 - rho2 / 4, 0, None))
    d = np.stack([(X * f)[ok], (Y * f)[ok], (1 - rho2 / 2)[ok]], 1)
    v = d[:, :1] * ex + d[:, 1:2] * ey + d[:, 2:] * ez
    t = 0.5 / np.max(np.abs(v), 1)  # луч из центра куба до грани
    srgb = 0.5 + v * t[:, None]
    lab = lin2ok(srgb2lin(np.clip(srgb, 0, 1)))
    return ok, lab


def dE_map(ok, lab):
    L = np.full(ok.shape + (3,), np.nan)
    L[ok] = lab
    dx = np.linalg.norm(L[:, 1:] - L[:, :-1], axis=2)[:-1]
    dy = np.linalg.norm(L[1:] - L[:-1], axis=2)[:, :-1]
    g = np.sqrt(dx ** 2 + dy ** 2)
    g = g[np.isfinite(g)]
    # отбросить складки (рёбра куба дают скачок производной, но не цвета) — нет, оставить всё
    return g


cases = {"rgb      ": rgb_hemisphere(R)}
for K in (1.0, 1.5, 2.0, 3.0, 4.0):
    for north in (True, False):
        cases["ok K=%.1f %s" % (K, "Б" if north else "Ч")] = hemisphere(R, K, north)[1:]
for name, (ok, lab) in cases.items():
    g = dE_map(ok, lab)
    p5, p50, p95 = np.percentile(g, [5, 50, 95])
    print("%s  медиана ΔE/пикс %.5f  p95/p5 %.2f  CV %.2f" % (name, p50, p95 / p5, g.std() / g.mean()))
