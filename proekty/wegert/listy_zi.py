"""listy_zi.py — Вегерт, гл. 7.3, рис. 7.10–7.11: у z^i все листы римановой поверхности дают один фазовый портрет,
а у z^i − 1 листы различаются. На листе k: z^i = exp(i(Log z + 2πik)) = e^(−2πk) · exp(i Log z) — множитель
положителен, фаза та же. Верхний ряд — z^i на листах k = −1, 0, 1; нижний — z^i − 1 на тех же листах.
Квадрат |Re|, |Im| < 2, как у Вегерта. Цвет — фаза (hsv), яркость — дробная часть log|f|.
Запуск: ext/venv-pdf/bin/python -I proekty/wegert/listy_zi.py выход.png
21.10, пробуждение 03:07."""
import sys
import numpy as np
from PIL import Image, ImageDraw

N = 200
x = np.linspace(-2, 2, N)
X, Y = np.meshgrid(x, x[::-1])
Z = X + 1j * Y
Z[Z == 0] = 1e-12
L = np.log(Z)


def portret(F):
    hue = (np.angle(F) / (2 * np.pi)) % 1.0
    m = (np.log(np.abs(F) + 1e-300) / (2 * np.pi) * 6) % 1.0
    hsv = np.stack([hue * 255, np.full_like(hue, 230), 150 + 105 * m], -1).astype(np.uint8)
    return Image.fromarray(hsv, "HSV").convert("RGB")


img = Image.new("RGB", (3 * N + 40, 2 * N + 50), "white")
d = ImageDraw.Draw(img)
for col, k in enumerate((-1, 0, 1)):
    F = np.exp(1j * (L + 2j * np.pi * k))
    img.paste(portret(F), (10 + col * (N + 10), 20))
    img.paste(portret(F - 1), (10 + col * (N + 10), N + 40))
    d.text((10 + col * (N + 10), 5), "z^i, k=%d" % k, fill="black")
    d.text((10 + col * (N + 10), N + 25), "z^i - 1, k=%d" % k, fill="black")
out = sys.argv[1] if len(sys.argv) > 1 else "listy-zi.png"
img.save(out)
print("ok", out)
