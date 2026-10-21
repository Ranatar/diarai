"""log_spiral.py — проверка фразы из `complex-variables-philosophy-essay-full.md` (стр. 121): «Спиралевидные
структуры, возникающие при визуализации комплексного логарифма вокруг начала координат».
Рисую фазовые портреты (как у Вегерта: цвет — аргумент, яркость — дробная часть log|f|) трёх функций
в квадрате |Re|,|Im| < 1: log z (главная ветвь), z^i = exp(i log z), z^(1+i).
Запуск: ext/venv-pdf/bin/python -I proekty/wegert/log_spiral.py выход.png
21.10, пробуждение 03:07."""
import sys
import numpy as np
from PIL import Image, ImageDraw

N = 260
x = np.linspace(-1, 1, N)
X, Y = np.meshgrid(x, x[::-1])
Z = X + 1j * Y
Z[Z == 0] = 1e-12
L = np.log(Z)


def portret(F):
    hue = (np.angle(F) / (2 * np.pi)) % 1.0
    m = (np.log(np.abs(F) + 1e-300) / (2 * np.pi) * 6) % 1.0
    hsv = np.stack([hue * 255, np.full_like(hue, 230), 150 + 105 * m], -1).astype(np.uint8)
    return Image.fromarray(hsv, "HSV").convert("RGB")


panels = [("log z", portret(L)), ("z^i", portret(np.exp(1j * L))), ("z^(1+i)", portret(np.exp((1 + 1j) * L)))]
img = Image.new("RGB", (3 * N + 40, N + 30), "white")
d = ImageDraw.Draw(img)
for k, (name, p) in enumerate(panels):
    img.paste(p, (10 + k * (N + 10), 25))
    d.text((10 + k * (N + 10), 5), name, fill="black")
out = sys.argv[1] if len(sys.argv) > 1 else "log-spiral.png"
img.save(out)
print("ok", out)
