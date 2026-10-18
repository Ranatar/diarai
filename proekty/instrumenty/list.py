"""Обзорный лист картинок папки: python3 -I list.py папка out.png [столбцов] [размер] [с] [по]"""
import os, sys
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 10
S = int(sys.argv[4]) if len(sys.argv) > 4 else 128
a = int(sys.argv[5]) if len(sys.argv) > 5 else 0
b = int(sys.argv[6]) if len(sys.argv) > 6 else 10 ** 9
files = sorted(f for f in os.listdir(src) if f.lower().endswith((".jpg", ".jpeg", ".png")))[a:b]
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * S, rows * S), (20, 20, 20))
for n, f in enumerate(files):
    try:
        im = Image.open(os.path.join(src, f)).convert("RGB")
    except Exception:
        continue
    im.thumbnail((S - 2, S - 2))
    sheet.paste(im, ((n % cols) * S + (S - im.width) // 2, (n // cols) * S + (S - im.height) // 2))
sheet.save(out)
print(len(files), sheet.size)
