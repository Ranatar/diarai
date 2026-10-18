"""cvet.py out.png in1.bin:W:подпись [in2.bin:W:подпись …] — раскрашивает растры (λ, φ) из raster.mjs
поверхностью RGB-куба, как у «Кружочка»: серая диагональ — ось сферы, белое — северный полюс, красный — λ = 0
(kub.cube_point). Склеивает в один лист с подписями."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import kub  # noqa

tiles = []
for arg in sys.argv[2:]:
    path, W, label = arg.split(":", 2)
    W = int(W)
    a = np.fromfile(path, dtype=np.float64).reshape(-1, W, 2)
    lam, phi = a[..., 0], a[..., 1]
    ok = np.isfinite(lam) & np.isfinite(phi)
    d = np.stack([np.cos(phi) * np.cos(lam), np.cos(phi) * np.sin(lam), np.sin(phi)], -1)
    img = np.full(lam.shape + (3,), 255, np.uint8)
    c = kub.cube_point(np.nan_to_num(d[ok]).reshape(-1, 3))
    img[ok] = np.clip(c * 255 + 0.5, 0, 255).astype(np.uint8)
    im = Image.fromarray(img)
    canvas = Image.new("RGB", (im.width, im.height + 22), "white")
    canvas.paste(im, (0, 22))
    try:
        from PIL import ImageFont
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except OSError:
        font = None
    ImageDraw.Draw(canvas).text((4, 4), label, fill="black", font=font)
    tiles.append(canvas)

cols = 3
w = max(t.width for t in tiles)
rows = [tiles[i:i + cols] for i in range(0, len(tiles), cols)]
H = sum(max(t.height for t in r) + 10 for r in rows)
sheet = Image.new("RGB", (cols * (w + 10), H), "white")
y = 0
for r in rows:
    for k, t in enumerate(r):
        sheet.paste(t, (k * (w + 10) + (w - t.width) // 2, y))
    y += max(t.height for t in r) + 10
sheet.save(sys.argv[1])
print(sys.argv[1], sheet.size)
