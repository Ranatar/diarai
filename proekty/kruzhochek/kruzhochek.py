"""Перенос на Python эскиза автора inbox/нян/Kruzhochek1_1.html (JS, 2017, «Molag»).

Поверхность RGB-куба -> поворот (серая диагональ вертикально) -> на сферу
(z сохраняется) -> азимутальная равновеликая проекция Ламберта -> круг.
Белое в центре, чёрное по краю.

Запуск: python3 kruzhochek.py out.png [--fill] [--n N]
  --fill  рисовать всю поверхность куба, а не только решётку через 32 и рёбра
"""
import sys
import numpy as np
from PIL import Image

W = H = 1024


def points(n=0, fill=False):
    a = np.arange(n, 256 - n)
    i, j, k = np.meshgrid(a, a, a, indexing="ij")
    i, j, k = i.ravel(), j.ravel(), k.ravel()
    lo, hi = n, 255 - n
    bord = lambda t: (t == lo) | (t == hi)
    latt = lambda s, t: (s % 32 == 0) | (t % 32 == 0)
    edge = lambda s, t: (s == hi) & (t == hi)
    if fill:
        sel = bord(i) | bord(j) | bord(k)
    else:
        sel = (bord(i) & latt(j, k)) | (bord(j) & latt(i, k)) | (bord(k) & latt(i, j)) \
            | edge(i, j) | edge(j, k) | edge(i, k)
    return i[sel], j[sel], k[sel]  # порядок как в тройном цикле JS


def project(x, y, z, n=0):
    s3, s2 = 1 / np.sqrt(3), 1 / np.sqrt(2)
    x3, y3, z3 = (s3 * 2 * (t - 255 / 2) / (255 - 2 * n) for t in (x, y, z))
    x4 = s2 * x3 - s2 * y3
    y4 = -s2 * s3 * x3 - s2 * s3 * y3 + (s3 / s2) * z3
    z4 = -s3 * x3 - s3 * y3 - s3 * z3
    with np.errstate(divide="ignore", invalid="ignore"):
        f = np.sqrt((1 - z4 ** 2) / (x4 ** 2 + y4 ** 2))
        x5, y5 = x4 * f, y4 * f
        g = np.sqrt(2 / (1 - z4))
    return (W / 4) * x5 * g + W / 2, (H / 4) * y5 * g + H / 2


def render(n=0, fill=False):
    i, j, k = points(n, fill)
    px, py = project(i.astype(float), j.astype(float), k.astype(float), n)
    ok = np.isfinite(px) & np.isfinite(py)
    px, py = np.round(px[ok]).astype(int), np.round(py[ok]).astype(int)
    rgb = np.stack([i[ok], j[ok], k[ok]], 1).astype(np.uint8)
    inb = (px >= 0) & (px < W) & (py >= 0) & (py < H)
    img = np.zeros((H, W, 3), np.uint8)
    img[py[inb], px[inb]] = rgb[inb]  # при совпадении побеждает последняя, как в JS
    return img


if __name__ == "__main__":
    args = sys.argv[1:]
    n = int(args[args.index("--n") + 1]) if "--n" in args else 0
    Image.fromarray(render(n, "--fill" in args)).save(args[0])
