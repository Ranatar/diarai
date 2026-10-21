"""portret.py — фазовый портрет sin z с наложенными орбитами маятника (к сноске 3 Вегерта, notes/wegert.md).
Запуск: ext/venv-pdf/bin/python -I proekty/wegert/portret.py выход.png
Цвет — аргумент sin z (цветовой круг HSV). Чёрные линии — уровни |sin z|, то есть cosh p − cos q = c
при q = 2x, p = 2y. Белые линии — орбиты маятника p²/2 − cos q = c − 1 с теми же уровнями.
Около вещественной оси чёрное и белое совпадают, дальше расходятся (cosh p − 1 растёт быстрее p²/2).
21.10, пробуждение 00:08."""
import sys
import numpy as np
from PIL import Image

W, H = 800, 600
X0, X1, Y0, Y1 = -4.0, 4.0, -3.0, 3.0
x = np.linspace(X0, X1, W)
y = np.linspace(Y1, Y0, H)  # сверху вниз
X, Y = np.meshgrid(x, y)
Z = np.sin(X + 1j * Y)

# цвет по аргументу
hue = (np.angle(Z) / (2 * np.pi)) % 1.0
hsv = np.stack([hue * 255, np.full_like(hue, 200), np.full_like(hue, 235)], axis=-1).astype(np.uint8)
img = np.array(Image.fromarray(hsv, "HSV").convert("RGB"))

q, p = 2 * X, 2 * Y
modul = np.cosh(p) - np.cos(q)          # = 2|sin z|²
mayatnik = p ** 2 / 2 - np.cos(q) + 1   # энергия маятника, сдвинутая так, чтобы минимумы совпали (0)
assert np.allclose(modul, 2 * np.abs(Z) ** 2)

levels = [0.25, 0.75, 1.5, 2.0, 3.0, 5.0, 9.0]   # 2.0 — сепаратриса (через сёдла x = ±π/2)
def linii(F, c, tol):
    return np.abs(F - c) < tol * (1 + c)
for c in levels:
    img[linii(modul, c, 0.012)] = (0, 0, 0)
    img[linii(mayatnik, c, 0.012)] = (255, 255, 255)

Image.fromarray(img).save(sys.argv[1] if len(sys.argv) > 1 else "portret.png")
print("ok", W, H, "уровни:", levels)
