"""zeta.py — повторение рис. 5.6 Вегерта («Divergence and convergence of the Dirichlet series for the Zeta function»)
и ещё одна панель, которой у него на этом рисунке нет.
  a) частичная сумма s_1000(z) = Σ_{n≤1000} n^(−z) в квадрате |Re z| < 10, |Im z| < 10;
  b) та же сумма в полуплоскости сходимости, 1 < Re z < 10;
  c) сама ζ там же (mpmath.fp.zeta);
  d) ζ во всём квадрате (аналитическое продолжение), чтобы видеть, что у левого края панели (a) — не ζ.
Цвет — фаза (hsv, красный = положительные значения, как у Вегерта), яркость — дробная часть log|f| (линии уровня).
Запуск: ext/venv-pdf/bin/python -I proekty/wegert/zeta.py выход.png [N]
21.10, пробуждение 03:07."""
import sys
import numpy as np
from PIL import Image, ImageDraw
import mpmath

out = sys.argv[1] if len(sys.argv) > 1 else "zeta.png"
N = int(sys.argv[2]) if len(sys.argv) > 2 else 240


def portret(F):
    hue = (np.angle(F) / (2 * np.pi)) % 1.0
    m = (np.log(np.abs(F) + 1e-300) / (2 * np.pi) * 6) % 1.0
    val = 150 + 105 * m
    hsv = np.stack([hue * 255, np.full_like(hue, 230), val], -1).astype(np.uint8)
    return Image.fromarray(hsv, "HSV").convert("RGB")


def setka(x0, x1, y0, y1, nx, ny):
    X, Y = np.meshgrid(np.linspace(x0, x1, nx), np.linspace(y1, y0, ny))
    return X + 1j * Y


def s1000(Z):
    S = np.zeros_like(Z)
    for n in range(1, 1001):
        S += np.exp(-Z * np.log(n))
    return S


def zeta(Z):
    f = np.vectorize(lambda z: complex(mpmath.fp.zeta(z)) if abs(z - 1) > 1e-9 else 1e300)
    return f(Z)


Zsq = setka(-10, 10, -10, 10, N, N)
nx = int(N * 9 / 20)
Zhalf = setka(1.0 + 20 / N, 10, -10, 10, nx, N)
panels = [("a) s1000, |Re|,|Im|<10", portret(s1000(Zsq))),
          ("b) s1000, 1<Re<10", portret(s1000(Zhalf))),
          ("c) zeta, 1<Re<10", portret(zeta(Zhalf))),
          ("d) zeta, |Re|,|Im|<10", portret(zeta(Zsq)))]
W = sum(p.width for _, p in panels) + 10 * (len(panels) + 1)
img = Image.new("RGB", (W, N + 30), "white")
d = ImageDraw.Draw(img)
x = 10
for name, p in panels:
    img.paste(p, (x, 25))
    d.text((x, 5), name, fill="black")
    x += p.width + 10
img.save(out)
print("ok", out, img.size)
