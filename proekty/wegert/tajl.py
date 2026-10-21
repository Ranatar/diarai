"""tajl.py — опыт к загадке Вегерта о тайле D (notes/wegert.md): сколько сторон у тайла вокруг седла.
f(z) = z^k + a, у f′ в нуле нуль кратности k−1. Сетка «усиленного» портрета: n изохром (arg f = 2πj/n)
и линии уровня log|f| с тем же шагом 2π/n (равная плотность, как у Вегерта). Чёрные линии — сетка.
Запуск: ext/venv-pdf/bin/python -I proekty/wegert/tajl.py выход.png
21.10, пробуждение 00:08."""
import sys
import numpy as np
from PIL import Image

N, n = 500, 12
a = 0.37 * np.exp(1j * 0.4)      # значение в седле — не на линиях сетки
panels = []
for k in (2, 3):
    x = np.linspace(-1.2, 1.2, N)
    X, Y = np.meshgrid(x, x[::-1])
    F = (X + 1j * Y) ** k + a
    ph = np.angle(F) / (2 * np.pi) * n
    lm = np.log(np.abs(F)) / (2 * np.pi) * n
    hue = (np.angle(F) / (2 * np.pi)) % 1.0
    hsv = np.stack([hue * 255, np.full_like(hue, 170), np.full_like(hue, 240)], -1).astype(np.uint8)
    img = np.array(Image.fromarray(hsv, "HSV").convert("RGB"))
    def line(G):
        fr = G - np.round(G)
        return np.abs(fr) < 0.06
    img[line(ph) | line(lm)] = (0, 0, 0)
    c = N // 2
    img[c - 2:c + 3, c - 2:c + 3] = (255, 255, 255)   # седло (z = 0) — белая точка
    panels.append(img)
out = np.concatenate([panels[0], np.full((N, 10, 3), 255, np.uint8), panels[1]], axis=1)
Image.fromarray(out).save(sys.argv[1] if len(sys.argv) > 1 else "tajl.png")
print("ok: слева k=2 (f′ простой нуль), справа k=3 (двойной)")
