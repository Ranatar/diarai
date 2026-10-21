"""zeta_polosa.py — фазовый портрет ζ в прямоугольнике −4 < Re z < 5, 0 < Im z < 45, с отметкой критической прямой
Re z = 1/2 (белый пунктир). Квадрат |Re|,|Im| < 10 у Вегерта (рис. 5.6) и у меня (zeta.py, панель d) не содержит
ни одного нетривиального нуля: первый лежит на высоте ≈ 14,13. Здесь их видно несколько.
Запуск: ext/venv-pdf/bin/python -I -W ignore proekty/wegert/zeta_polosa.py выход.png [масштаб_пикселей_на_единицу]
21.10, пробуждение 03:07."""
import sys
import numpy as np
from PIL import Image, ImageDraw
import mpmath

out = sys.argv[1] if len(sys.argv) > 1 else "zeta-polosa.png"
k = int(sys.argv[2]) if len(sys.argv) > 2 else 20
x0, x1, y0, y1 = -4.0, 5.0, 0.0, 45.0
nx, ny = int((x1 - x0) * k), int((y1 - y0) * k)
X, Y = np.meshgrid(np.linspace(x0, x1, nx), np.linspace(y1, y0, ny))
Z = X + 1j * Y
F = np.vectorize(lambda z: complex(mpmath.fp.zeta(z)) if abs(z - 1) > 1e-9 else 1e300)(Z)
hue = (np.angle(F) / (2 * np.pi)) % 1.0
m = (np.log(np.abs(F) + 1e-300) / (2 * np.pi) * 6) % 1.0
hsv = np.stack([hue * 255, np.full_like(hue, 230), 150 + 105 * m], -1).astype(np.uint8)
img = Image.fromarray(hsv, "HSV").convert("RGB")
d = ImageDraw.Draw(img)
xc = int((0.5 - x0) / (x1 - x0) * (nx - 1))
for yy in range(0, ny, 8):
    d.line([(xc, yy), (xc, yy + 3)], fill="white")
for t in (10, 20, 30, 40):
    yy = int((y1 - t) / (y1 - y0) * (ny - 1))
    d.line([(0, yy), (8, yy)], fill="black")
    d.text((10, yy - 6), "Im %d" % t, fill="black")
img.save(out)
nuli = [float(mpmath.zetazero(j).imag) for j in range(1, 8)]
print("ok", out, img.size, "нули ζ на критической прямой до Im 45 (mpmath.zetazero):", [round(v, 2) for v in nuli if v < 45])
