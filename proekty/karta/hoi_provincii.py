"""hoi_provincii.py — сколько провинций на inbox/HoI maps/provinces.png (одна провинция = один цвет)
и какова средняя площадь провинции по широтным поясам и по долготным полосам (в пикселях).
2026-10-18, пробуждение 19:01: из очереди «не упомянут» карты архива."""
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
a = np.asarray(Image.open("/home/diarai/diarai/inbox/HoI maps/provinces.png").convert("RGB")).astype(np.int64)
H, W, _ = a.shape
code = (a[..., 0] << 16) | (a[..., 1] << 8) | a[..., 2]
u, inv, cnt = np.unique(code, return_inverse=True, return_counts=True)
inv = inv.reshape(H, W)
print("размер %dx%d, цветов (провинций) %d" % (W, H, len(u)))
print("площадь провинции, пикс.: медиана %d, мин %d, макс %d" % (np.median(cnt), cnt.min(), cnt.max()))
# суша/море — грубо: «морские» цвета синие (B велико, R и G малы)
r, g, b = (u >> 16) & 255, (u >> 8) & 255, u & 255
more = (b > 150) & (g < 80)
print("синих («морских»?) %d, прочих %d" % (more.sum(), (~more).sum()))
# плотность: сколько разных провинций в каждой клетке сетки 6×8 (только «сухопутные»)
rows, cols = 6, 8
print("сухопутных провинций в клетке (строки — с севера на юг):")
for i in range(rows):
    line = []
    for j in range(cols):
        blk = inv[i * H // rows:(i + 1) * H // rows, j * W // cols:(j + 1) * W // cols]
        ids = np.unique(blk)
        line.append("%5d" % (~more[ids]).sum())
    print(" ".join(line))
