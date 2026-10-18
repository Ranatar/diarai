"""Domain coloring для w(z) = (z^3 - i)/z, как в complex_trinity.html:
оттенок = arg w, яркость L = exp(-|w|). Плюс отметки нулей, полюса и седловых точек (w' = 0).
python3 trinity_dc.py out.png [размер] [радиус]"""
import sys
import numpy as np
from PIL import Image, ImageDraw

out = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 700
R = float(sys.argv[3]) if len(sys.argv) > 3 else 1.8
x = np.linspace(-R, R, N)
X, Y = np.meshgrid(x, -x)
Z = X + 1j * Y
with np.errstate(all="ignore"):
    W = (Z**3 - 1j) / Z
H = (np.angle(W) / (2 * np.pi)) % 1.0
L = np.exp(-np.abs(W))
L = np.nan_to_num(L)

def hsl2rgb(h, s, l):
    c = (1 - np.abs(2 * l - 1)) * s
    hp = h * 6
    xx = c * (1 - np.abs(hp % 2 - 1))
    z = np.zeros_like(h)
    r, g, b = [np.select([(hp >= k) & (hp < k + 1) for k in range(6)], v) for v in (
        [c, xx, z, z, xx, c], [xx, c, c, xx, z, z], [z, z, xx, c, c, xx])]
    m = l - c / 2
    return np.stack([r + m, g + m, b + m], -1)

rgb = (np.clip(hsl2rgb(H, np.ones_like(H), L), 0, 1) * 255).astype(np.uint8)
im = Image.fromarray(rgb)
d = ImageDraw.Draw(im)
def px(z):
    return ((z.real + R) / (2 * R) * (N - 1), (R - z.imag) / (2 * R) * (N - 1))
for k in range(3):
    zero = np.exp(1j * (np.pi / 2 + 2 * np.pi * k) / 3)
    sad = 2 ** (-1 / 3) * np.exp(1j * (-np.pi / 2 + 2 * np.pi * k) / 3)  # z^3 = -i/2
    for z, col in ((zero, (0, 0, 0)), (sad, (255, 255, 255))):
        u, v = px(z)
        d.ellipse((u - 4, v - 4, u + 4, v + 4), outline=col, width=2)
    print("ноль", np.round(zero, 4), " седло", np.round(sad, 4),
          "|w| в седле", round(abs((sad**3 - 1j) / sad), 4), "L", round(np.exp(-abs((sad**3 - 1j) / sad)), 4))
# уровень |w| = 0.7 (L = 0.5): где он лежит
for k in range(3):
    zero = np.exp(1j * (np.pi / 2 + 2 * np.pi * k) / 3)
    ts = np.linspace(0, 2 * np.pi, 7)[:-1]
    rs = []
    for t in ts:
        lo, hi = 0.0, 0.6
        for _ in range(50):
            m = (lo + hi) / 2
            z = zero + m * np.exp(1j * t)
            if abs((z**3 - 1j) / z) < 0.7: lo = m
            else: hi = m
        rs.append(lo)
    print("контур |w|=0.7 вокруг нуля", k, "радиусы", np.round(rs, 3))
# направление обхода оттенка вокруг нуля и вокруг полюса
for name, c in (("ноль z0", np.exp(1j * np.pi / 6)), ("полюс 0", 0)):
    ts = np.linspace(0, 2 * np.pi, 2001)
    z = c + 0.05 * np.exp(1j * ts)
    a = np.unwrap(np.angle((z**3 - 1j) / z))
    print(name, ": приращение arg w при обходе против часовой =", round((a[-1] - a[0]) / (2 * np.pi), 3), "оборота")
im.save(out)
