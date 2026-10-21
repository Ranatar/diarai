"""anim.py — анимация, которую Вегерт предлагает в эпилоге: «consider, for example, the family of functions
f(z) − c with a fixed rational function f and a point c moving in the complex plane».
f — его «стандартный пример» из раздела 2.5: f(z) = (z − 1)/(z² + z + 1). c обходит окружность радиуса 0,6.
Цвет — фаза (hsv, красный = положительные значения, как у Вегерта: angle(-f) при caxis[-π, π]).
Нули f − c — это точки, где f = c; при движении c они ползут, а полюсы (корни z² + z + 1) стоят на месте.
Запуск: ext/venv-pdf/bin/python -I proekty/wegert/anim.py выход.gif
21.10, пробуждение 00:08."""
import sys
import numpy as np
from PIL import Image

N, KADROV = 220, 24
x = np.linspace(-2.5, 2.5, N)
X, Y = np.meshgrid(x, x[::-1])
Z = X + 1j * Y
F = (Z - 1) / (Z ** 2 + Z + 1)
kadry = []
for t in range(KADROV):
    c = 0.6 * np.exp(2j * np.pi * t / KADROV)
    G = F - c
    hue = (np.angle(G) / (2 * np.pi)) % 1.0
    # лёгкая «усиленность»: затемнение по дробной части log|G|, чтобы были видны линии уровня
    m = (np.log(np.abs(G) + 1e-12) / (2 * np.pi) * 12) % 1.0
    val = 170 + 85 * m
    hsv = np.stack([hue * 255, np.full_like(hue, 230), val], -1).astype(np.uint8)
    kadry.append(Image.fromarray(hsv, "HSV").convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=128))
out = sys.argv[1] if len(sys.argv) > 1 else "anim.gif"
kadry[0].save(out, save_all=True, append_images=kadry[1:], duration=120, loop=0, optimize=True)
print("ok", out, KADROV, "кадров")
