"""Проверка ravnaya.py двумя независимыми путями.
 1. Площадь поверхности гаммы в OKLab прямо по граням sRGB-куба (сетка треугольников), без лучей и θ/φ.
 2. Доля пикселей круга по полосам светлоты против доли площади поверхности (по сетке куба).
python3 -I proverka.py ravnaya.png
"""
import os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otvet import lin2ok  # noqa


def srgb2lin(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


N = 600
t = np.linspace(0, 1, N + 1)
U, V = np.meshgrid(t, t, indexing="ij")
tot = 0.0
bands = np.zeros(4)
for axis in range(3):
    for val in (0.0, 1.0):
        pts = np.zeros((N + 1, N + 1, 3))
        others = [a for a in range(3) if a != axis]
        pts[..., axis] = val
        pts[..., others[0]] = U
        pts[..., others[1]] = V
        lab = lin2ok(srgb2lin(pts).reshape(-1, 3)).reshape(N + 1, N + 1, 3)
        a, b, c, d = lab[:-1, :-1], lab[1:, :-1], lab[:-1, 1:], lab[1:, 1:]
        ar = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=-1) + 0.5 * np.linalg.norm(np.cross(b - d, c - d), axis=-1)
        Lc = (a[..., 0] + d[..., 0]) / 2
        tot += ar.sum()
        for k, (lo, hi) in enumerate(((0, .25), (.25, .5), (.5, .75), (.75, 1.01))):
            bands[k] += ar[(Lc >= lo) & (Lc < hi)].sum()
print("площадь по граням куба: %.4f" % tot)

img = np.asarray(Image.open(sys.argv[1])).astype(float) / 255
R = img.shape[0] // 2
yy, xx = np.mgrid[-R:R, -R:R] + 0.5
inside = (xx ** 2 + yy ** 2) < (R - 1.5) ** 2  # без краевого кольца
L = lin2ok(srgb2lin(img[inside]))[:, 0]
for k, (lo, hi) in enumerate(((0, .25), (.25, .5), (.5, .75), (.75, 1.01))):
    pix = ((L >= lo) & (L < hi)).mean()
    print("L в [%.2f, %.2f): площадь %.1f%%  пикселей круга %.1f%%" % (lo, hi, 100 * bands[k] / tot, 100 * pix))
