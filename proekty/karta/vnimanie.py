"""vnimanie.py — «карта внимания»: квадратная диаграмма (treemap) архива inbox/ по upominaniya.tsv.
Плитка — единица (как в karta.md), площадь — число файлов без служебных (или байты: --bajty),
цвет — доля файлов по статусам: полностью (тёмно-зелёный) / частично / бегло / ? / не упомянут (серый).
python3 -I proekty/karta/vnimanie.py [--bajty]  → proekty/karta/vnimanie.png"""
import os, sys, collections
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
BAJTY = "--bajty" in sys.argv
CV = {"полностью": (40, 120, 70), "частично": (120, 180, 100), "бегло": (200, 210, 120),
      "нет": (230, 200, 190), "?": (225, 225, 225), "упомянут, статус не поставлен": (225, 225, 225), "не упомянут": (200, 200, 200)}
PORYADOK = ["полностью", "частично", "бегло", "упомянут, статус не поставлен", "нет", "не упомянут"]

def unit(rel):
    p = rel.split("/")
    if len(p) == 1:
        return "(корень)"
    if p[0] in ("gpt", "Synthesises-of-concepts", "html-generated", "Доклад") and len(p) > 2:
        return p[0] + "/" + p[1]
    return p[0]

U = collections.defaultdict(collections.Counter)
for line in open(os.path.join(HERE, "upominaniya.tsv"), encoding="utf-8"):
    if line.startswith("#"):
        continue
    f = line.rstrip("\n").split("\t")
    if f[2] == "служебное":
        continue
    U[unit(f[0])][f[2]] += int(f[1]) if BAJTY else 1
items = sorted(((sum(c.values()), u, c) for u, c in U.items()), reverse=True)
items = [it for it in items if it[0] > 0]

W, H = 1400, 900
im = Image.new("RGB", (W, H + 40), "white")
d = ImageDraw.Draw(im)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
except OSError:
    font = big = None

def worst(row, side):
    s = sum(r[0] for r in row)
    return max(max(side * side * r[0] / (s * s), s * s / (side * side * r[0])) for r in row)

def squarify(items, x, y, w, h):
    # простая «squarified» раскладка (Bruls и др.): ряд растёт, пока не ухудшает пропорции
    total = sum(i[0] for i in items)
    if not items:
        return
    scale = w * h / total
    rest = [(i[0] * scale, i) for i in items]
    while rest:
        side = min(w, h)
        row = [rest.pop(0)]
        while rest and worst(row + [rest[0]], side) <= worst(row, side):
            row.append(rest.pop(0))
        s = sum(r[0] for r in row)
        if w >= h:
            cw = s / h
            yy = y
            for a, it in row:
                ch = a / cw
                plitka(it, x, yy, cw, ch)
                yy += ch
            x += cw; w -= cw
        else:
            ch = s / w
            xx = x
            for a, it in row:
                cw = a / ch
                plitka(it, xx, y, cw, ch)
                xx += cw
            y += ch; h -= ch

def plitka(it, x, y, w, h):
    n, name, c = it
    # полосы статусов по горизонтали, пропорционально числу файлов
    xx = x
    for st in PORYADOK:
        if c[st]:
            ww = w * c[st] / n
            d.rectangle([xx, y, xx + ww, y + h], fill=CV[st])
            xx += ww
    d.rectangle([x, y, x + w, y + h], outline="white", width=2)
    if w > 60 and h > 18:
        label = name if len(name) * 7 < w else name[: max(3, int(w / 7) - 1)] + "…"
        d.text((x + 4, y + 3), label, fill="black", font=font)
    if w > 60 and h > 34:
        d.text((x + 4, y + 18), str(n) + (" Б" if BAJTY else " ф."), fill=(60, 60, 60), font=font)

squarify(items, 0, 40, W, H)
x = 6
d.text((x, 4), "Карта внимания: inbox/ по статусам прочтения (%s)" % ("байты" if BAJTY else "файлы, без служебных"), fill="black", font=big)
x = 6
for st in PORYADOK:
    d.rectangle([x, 24, x + 14, 36], fill=CV[st])
    d.text((x + 18, 23), st, fill="black", font=font)
    x += 30 + 8 * len(st)
out = os.path.join(HERE, "vnimanie-bajty.png" if BAJTY else "vnimanie.png")
im.save(out)
print(out)
