"""Тело из Kruzhochek10.scad (единственный файл, где эта формула живая): точки поверхности куба (центр — серый) радиально
нормированы делением на D = xz/y + yx/z + zy/x. D однородна степени 1, поэтому образ лежит на D = 1, т.е.
x²y² + y²z² + z²x² = xyz — римская поверхность Штейнера (образ проективной плоскости).
D нечётна: точка и противоположная (цвет и его дополнение 1−c) попадают в одно место.
В OpenSCAD оба кубика стоят там друг в друге. Здесь — два вида: светлая половина куба (R+G+B > 3/2) и тёмная.
Поворот — как у автора (x5, y5, z5: серая диагональ на ось z). Рендер точками с z-буфером, ортографический.
python3 -I rimskaya.py out.png [S]
"""
import sys
import numpy as np
from PIL import Image

n = 400
t = (np.arange(n) + 0.5) / n
U, V = np.meshgrid(t, t, indexing="ij")
pts = []
for ax in range(3):
    o = [a for a in range(3) if a != ax]
    for val in (0.0, 1.0):
        p = np.zeros((n, n, 3))
        p[..., ax] = val; p[..., o[0]] = U; p[..., o[1]] = V
        pts.append(p.reshape(-1, 3))
col = np.concatenate(pts)  # цвета sRGB
q = 2 * col - 1  # x3: куб [-1,1]³
x, y, z = q.T
with np.errstate(divide="ignore", invalid="ignore"):
    D = x * z / y + y * x / z + z * y / x
ok = np.isfinite(D) & (np.abs(D) > 1e-9)
col, q, D = col[ok], q[ok], D[ok]
r = q / D[:, None]  # x4
s2, s3 = np.sqrt(2), np.sqrt(3)
x4, y4, z4 = r.T
x5 = x4 / s2 - y4 / s2  # поворот автора
y5 = -x4 / s2 / s3 - y4 / s2 / s3 + (1 / s3) / (1 / s2) * z4
z5 = -(x4 + y4 + z4) / s3
P = np.stack([x5, y5, z5], 1)


def view(P, col, S, rot):
    Q = P @ rot.T
    m = S / 2 * 0.9 / np.abs(Q[:, :2]).max()
    px = (Q[:, 0] * m + S / 2).astype(int)
    py = (-Q[:, 1] * m + S / 2).astype(int)
    order = np.argsort(Q[:, 2])  # дальние сначала, ближние перезаписывают
    img = np.zeros((S, S, 3))
    img[py[order], px[order]] = col[order]
    return img


def rot(ax, ay):
    ca, sa, cb, sb = np.cos(ax), np.sin(ax), np.cos(ay), np.sin(ay)
    Rx = np.array([[1, 0, 0], [0, ca, -sa], [0, sa, ca]])
    Ry = np.array([[cb, 0, sb], [0, 1, 0], [-sb, 0, cb]])
    return Rx @ Ry


if __name__ == "__main__":
    out = sys.argv[1]
    S = int(sys.argv[2]) if len(sys.argv) > 2 else 360
    light = col.sum(1) > 1.5
    R1 = rot(-0.5, 0.4)
    R2 = rot(0.0, 0.0)  # сверху вдоль серой оси (z5)
    tiles = [view(P[light], col[light], S, R1), view(P[~light], col[~light], S, R1),
             view(P[light], col[light], S, R2), view(P[~light], col[~light], S, R2)]
    canvas = np.zeros((2 * S, 2 * S, 3))
    canvas[:S, :S], canvas[:S, S:], canvas[S:, :S], canvas[S:, S:] = tiles
    Image.fromarray((canvas * 255 + 0.5).astype(np.uint8)).save(out)
