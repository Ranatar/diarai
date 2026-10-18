"""list_nomera.py spisok.txt от до out.png [размер] [столбцов] — лист картинок по номерам из списка list_hrono.py
(«номер\\tдата\\tимя»), крупнее, чем обзорные листы: по умолчанию 360 px, 5 в ряд, номер и дата на плитке.
Картинки берутся из inbox/gpt/. 2026-10-18, пробуждение 19:01: перепроверка серий, описанных с мелких листов."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
spisok, a, b, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
S = int(sys.argv[5]) if len(sys.argv) > 5 else 360
C = int(sys.argv[6]) if len(sys.argv) > 6 else 5
rows = [l.rstrip("\n").split("\t") for l in open(spisok, encoding="utf-8")]
rows = [r for r in rows if a <= int(r[0]) <= b]
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
except OSError:
    font = None
n = len(rows)
sheet = Image.new("RGB", (C * S, ((n + C - 1) // C) * S), "white")
for k, (num, when, name) in enumerate(rows):
    im = Image.open(os.path.join("/home/diarai/diarai/inbox/gpt", name)).convert("RGB")
    im.thumbnail((S, S))
    x, y = (k % C) * S, (k // C) * S
    sheet.paste(im, (x + (S - im.width) // 2, y + (S - im.height) // 2))
    ImageDraw.Draw(sheet).text((x + 4, y + 4), "%s  %s" % (num, when[5:]), fill="red", font=font)
sheet.save(out)
print(out, n)
