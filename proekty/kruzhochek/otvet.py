"""Ответ на «Кружочек»: то же цветовое тело на сфере и на плоскости, но в OKLab и обратным ходом.

Автор шёл прямым ходом: точки куба -> сфера -> плоскость; у белой вершины точки редели, оставались дыры.
Здесь наоборот: для каждого пикселя обратная проекция Ламберта даёт направление на сфере,
по этому направлению из средне-серого в OKLab идёт луч до границы гаммы sRGB, и берётся цвет на границе.
Два полушария рядом (как первый и последний эскизы автора): светлое с белым в центре и тёмное с чёрным.

OKLab: матрицы из статьи Б. Оттоссона (2020), https://bottosson.github.io/posts/oklab/ ;
обратное преобразование — обращением тех же матриц (numpy), а не по памяти.

python3 -I otvet.py out.png [K] [R]   K — растяжение a,b относительно L (по умолчанию 2), R — радиус круга
"""
import sys
import numpy as np
from PIL import Image

M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
               [0.2119034982, 0.6806995451, 0.1073969566],
               [0.0883024619, 0.2817188376, 0.6299787005]])
M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468],
               [1.9779984951, -2.4285922050, 0.4505937099],
               [0.0259040371, 0.7827717662, -0.8086757660]])
M1i, M2i = np.linalg.inv(M1), np.linalg.inv(M2)


def lin2ok(rgb):
    return np.cbrt(rgb @ M1.T) @ M2.T


def ok2lin(lab):
    return (lab @ M2i.T) ** 3 @ M1i.T


def lin2srgb(x):
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * x ** (1 / 2.4) - 0.055)


L0 = 0.5  # центр — серый с L = 0.5


def boundary(d, K):
    """d: (N,3) единичные направления в (a/K, b/K, L-L0)... т.е. луч c + t*(K*dx, K*dy, dz)."""
    lo = np.zeros(len(d))
    hi = np.full(len(d), 2.0)
    step = np.stack([d[:, 0] / K, d[:, 1] / K, d[:, 2]], 1)  # в OKLab: (a, b, L)
    for _ in range(40):
        mid = (lo + hi) / 2
        ab_l = step * mid[:, None]
        lab = np.stack([L0 + ab_l[:, 2], ab_l[:, 0], ab_l[:, 1]], 1)
        lin = ok2lin(lab)
        inside = np.all((lin >= -1e-9) & (lin <= 1 + 1e-9), 1)
        lo = np.where(inside, mid, lo)
        hi = np.where(inside, hi, mid)
    ab_l = step * lo[:, None]
    return np.stack([L0 + ab_l[:, 2], ab_l[:, 0], ab_l[:, 1]], 1)


def hemisphere(R, K, north=True):
    """Азимутальная равновеликая Ламберта, центр — полюс (белый или чёрный)."""
    yy, xx = np.mgrid[-R:R, -R:R] + 0.5
    X, Y = xx / R * np.sqrt(2), -yy / R * np.sqrt(2)  # полушарие -> круг радиуса √2
    rho2 = X ** 2 + Y ** 2
    ok = rho2 <= 2
    f = np.sqrt(np.clip(1 - rho2 / 4, 0, None))
    dx, dy, dz = X * f, Y * f, 1 - rho2 / 2  # обратная формула Ламберта
    if not north:
        dz, dx = -dz, -dx  # зеркально, чтобы оттенки на двух кругах шли навстречу
    d = np.stack([dx[ok], dy[ok], dz[ok]], 1)
    lab = boundary(d, K)
    img = np.zeros((2 * R, 2 * R, 3))
    img[ok] = lin2srgb(ok2lin(lab))
    return img, ok, lab


if __name__ == "__main__":
    out = sys.argv[1]
    K = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    R = int(sys.argv[3]) if len(sys.argv) > 3 else 384
    a, _, _ = hemisphere(R, K, True)
    b, _, _ = hemisphere(R, K, False)
    gap = R // 8
    canvas = np.zeros((2 * R, 4 * R + gap, 3))
    canvas[:, :2 * R] = a
    canvas[:, 2 * R + gap:] = b
    Image.fromarray((canvas * 255 + 0.5).astype(np.uint8)).save(out)
