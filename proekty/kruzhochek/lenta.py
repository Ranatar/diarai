"""Лента миниатюр по датам из out/spisok.tsv: python3 -I lenta.py out.png [с_даты] [по_дату] [размер]"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1]
lo = sys.argv[2] if len(sys.argv) > 2 else "0000"
hi = sys.argv[3] if len(sys.argv) > 3 else "9999"
S = int(sys.argv[4]) if len(sys.argv) > 4 else 128
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, "out", "spisok.tsv"))]
rows = [r for r in rows if lo <= r[0] <= hi + "~" and r[3] in ("ok", "кэш")]
cols = 12
L = 22
sheet = Image.new("RGB", (cols * S, ((len(rows) + cols - 1) // cols) * (S + L)), (16, 16, 16))
d = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("DejaVuSans.ttf", 9)
except OSError:
    font = ImageFont.load_default()
for n, (date, f, _, _) in enumerate(rows):
    t = os.path.join(HERE, "out", "thumbs", f[:-5] + ".png")
    if not os.path.exists(t):
        continue
    im = Image.open(t).convert("RGB")
    x, y = (n % cols) * S, (n // cols) * (S + L)
    im.thumbnail((S - 4, S - 4))
    sheet.paste(im, (x + (S - im.width) // 2, y + 2))
    d.text((x + 2, y + S), date, fill=(150, 150, 150), font=font)
    d.text((x + 2, y + S + 10), f[10:-5][:22], fill=(110, 110, 110), font=font)
sheet.save(out)
print(len(rows), sheet.size)
