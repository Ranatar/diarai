"""Последний лист «Дневника третьего лаборанта» как документ для фильма.

python3 tetrad.py out.png   (нужен FONTCONFIG_FILE со шрифтами автора; см. zapusk.py)
Тетрадь в клетку на тёмном столе, чернила, карандашная пагинация, лиловый штамп и резолюция.
"""
import math, os, random, sys
os.environ.setdefault("FONTCONFIG_FILE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts.conf"))
import cairo
import numpy as np
from PIL import Image, ImageFilter

W, H = 1180, 1500
R = random.Random(611)
out = sys.argv[1] if len(sys.argv) > 1 else "tetrad.png"

s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
c = cairo.Context(s)

# стол
c.set_source_rgb(0.16, 0.14, 0.12); c.paint()

# лист: чуть повёрнут, с неровным краем
c.save()
c.translate(W / 2, H / 2); c.rotate(-0.012); c.translate(-W / 2, -H / 2)
PX, PY, PW, PH = 110, 70, 960, 1360
c.move_to(PX, PY)
for x in range(PX, PX + PW + 1, 20):
    c.line_to(x, PY + R.uniform(-1.5, 1.5))
for y in range(PY, PY + PH + 1, 20):
    c.line_to(PX + PW + R.uniform(-1.5, 1.5), y)
for x in range(PX + PW, PX - 1, -20):
    c.line_to(x, PY + PH + R.uniform(-1.5, 1.5))
c.close_path()
c.set_source_rgb(0.90, 0.87, 0.79); c.fill_preserve()
c.clip()

# клетка
c.set_line_width(1.0)
c.set_source_rgba(0.35, 0.50, 0.70, 0.35)
STEP = 30
for x in range(PX, PX + PW, STEP):
    c.move_to(x + 0.5, PY); c.line_to(x + 0.5, PY + PH); c.stroke()
for y in range(PY, PY + PH, STEP):
    c.move_to(PX, y + 0.5); c.line_to(PX + PW, y + 0.5); c.stroke()
# поле
c.set_source_rgba(0.75, 0.25, 0.25, 0.55); c.set_line_width(1.6)
c.move_to(PX + PW - 120, PY); c.line_to(PX + PW - 120, PY + PH); c.stroke()


def font(size, italic=True, bold=False, face="Old Standard TT"):
    c.select_font_face(face, cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)


def hand(text, x, y, size=34, rgb=(0.12, 0.16, 0.38), alpha=0.92, tilt=-0.02):
    """Строка «от руки»: каждая буква чуть гуляет по высоте и наклону."""
    font(size)
    c.set_source_rgba(*rgb, alpha)
    for ch in text:
        c.save()
        c.translate(x, y + R.uniform(-1.2, 1.2))
        c.rotate(tilt + R.uniform(-0.03, 0.03))
        c.move_to(0, 0); c.show_text(ch)
        c.restore()
        x += c.text_extents(ch).x_advance * R.uniform(0.97, 1.04)
    return x


LINES = [
    ("25 марта.", True),
    ("", False),
    ("Пришли за тетрадью. Пока ждут", False),
    ("в коридоре, допишу.", False),
    ("", False),
    ("Меня зовут не номером. Номер у меня", False),
    ("есть, и он правильный, его можно", False),
    ("проверить по книге. Но если меня", False),
    ("растворят, номер останется в книге,", False),
    ("а того, кто считал гифы и ошибался", False),
    ("на полчаса вперёд, не будет. Этого", False),
    ("нет ни в какой книге, кроме этой", False),
    ("тетради.", False),
    ("", False),
    ("Чья это тетрадь? Моя.", False),
]
y = PY + 2 * STEP + 22
for text, head in LINES:
    if text:
        hand(text, PX + 40 + R.uniform(-3, 3), y, size=38 if head else 35)
    y += 2 * STEP
# подчёркнуто
c.set_source_rgba(0.12, 0.16, 0.38, 0.85); c.set_line_width(2.2)
yy = y - 2 * STEP + 10
c.move_to(PX + 40, yy)
for k in range(1, 36):
    c.line_to(PX + 40 + k * 11, yy + math.sin(k * 0.9) * 1.3)
c.stroke()

# карандаш: лист
font(30); c.set_source_rgba(0.35, 0.35, 0.37, 0.75)
c.move_to(PX + PW - 100, PY + 50); c.show_text("л. 51")

# лиловый круглый штамп
cx, cy, rr = PX + 230, PY + PH - 300, 125
c.set_source_rgba(0.42, 0.28, 0.58, 0.62)
c.new_path(); c.set_line_width(4); c.arc(cx, cy, rr, 0, 2 * math.pi); c.stroke()
c.new_path(); c.set_line_width(2); c.arc(cx, cy, rr - 38, 0, 2 * math.pi); c.stroke()
font(24, italic=False, bold=True)
ring = "НАРКОМАТЪ · ЗДОРОВАГО · БЕЗУМІЯ ·"
ang = -math.pi * 0.95
step = 2 * math.pi / (len(ring) + 1)
for ch in ring:
    c.save(); c.translate(cx + (rr - 27) * math.cos(ang), cy + (rr - 27) * math.sin(ang))
    c.rotate(ang + math.pi / 2); c.move_to(-c.text_extents(ch).x_advance / 2, 0); c.show_text(ch); c.restore()
    ang += step
# спираль в середине
c.new_path(); c.set_line_width(3)
for k in range(220):
    t = k / 220 * 5.5 * math.pi
    r = 4 + t * 3.8
    px, py = cx + r * math.cos(t), cy + r * math.sin(t)
    c.line_to(px, py) if k else c.move_to(px, py)
c.stroke()

# резолюция зам. наркома — другими чернилами, наискось, по-старому
c.save()
c.translate(PX + 410, PY + PH - 330); c.rotate(-0.16)
hand("Почерки не сличать.", 0, 0, size=44, rgb=(0.10, 0.25, 0.62), tilt=0)
hand("Тетрадь не сжигать.", 40, 62, size=44, rgb=(0.10, 0.25, 0.62), tilt=0)
c.set_source_rgba(0.10, 0.25, 0.62, 0.9); c.set_line_width(2.5)
c.move_to(330, 110)
c.curve_to(360, 60, 390, 140, 420, 90); c.curve_to(440, 60, 470, 120, 520, 95)
c.stroke()
c.restore()

c.restore()
s.write_to_png(out)

# старение: пятна и зерно
im = Image.open(out).convert("RGB")
a = np.asarray(im).astype(np.float32)
rng = np.random.default_rng(611)
yy, xx = np.mgrid[0:H, 0:W]
stain = np.zeros((H, W), np.float32)
for _ in range(7):
    sx, sy, sr = rng.uniform(150, W - 150), rng.uniform(150, H - 150), rng.uniform(80, 260)
    stain += np.exp(-((xx - sx) ** 2 + (yy - sy) ** 2) / (2 * sr ** 2)) * rng.uniform(0.03, 0.08)
grain = rng.normal(0, 4.0, (H, W)).astype(np.float32)
a = a * (1 - stain[..., None] * np.array([0.6, 0.9, 1.4])) + grain[..., None]
im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
im = im.crop((75, 40, W - 75, H - 30))  # стола оставить узкую кайму
im.save(out)
print(out, im.size)
