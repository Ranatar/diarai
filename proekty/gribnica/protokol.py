"""Выписка из протокола № 13/666 (1973) — документ для фильма, которого у события не было.

python3 protokol.py out.png
Основа — заголовок протокола автора (`Synthesises-of-concepts/various/cthulhu_ussr_protocol.md`:
особая папка, экз. № 2 из 9, 27 октября 1973, 0:13–3:33, Зал Тысячи Щупалец) и событие 1973 года из
сценария (Команданте, 3000 метров, Куба). Пункт 4 — мой: отсылка к «Будильнику» 1961 года.
"""
import math, os, random, sys
os.environ.setdefault("FONTCONFIG_FILE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts.conf"))
import cairo
import numpy as np
from PIL import Image, ImageFilter

W, H = 1100, 1450
R = random.Random(13666)
out = sys.argv[1] if len(sys.argv) > 1 else "protokol.png"
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
c = cairo.Context(s)
c.set_source_rgb(0.13, 0.12, 0.11); c.paint()

PX, PY, PW, PH = 60, 45, 980, 1360
c.save(); c.translate(W / 2, H / 2); c.rotate(0.008); c.translate(-W / 2, -H / 2)
c.rectangle(PX, PY, PW, PH); c.set_source_rgb(0.86, 0.82, 0.72); c.fill()


def font(face, size, bold=False, italic=False):
    c.select_font_face(face, cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)


def center(text, y, face="Old Standard TT", size=30, bold=False, rgb=(0.15, 0.13, 0.12), italic=False):
    font(face, size, bold, italic); c.set_source_rgb(*rgb)
    e = c.text_extents(text); c.move_to(PX + (PW - e.x_advance) / 2, y); c.show_text(text)


def typed(text, x, y, size=24):
    """Машинопись: моноширинный шрифт, каждая литера чуть разной густоты и высоты."""
    font("DejaVu Sans Mono", size)
    for ch in text:
        c.set_source_rgba(0.10, 0.10, 0.14, R.uniform(0.70, 0.95))
        c.move_to(x, y + R.uniform(-0.8, 0.8)); c.show_text(ch)
        x += c.text_extents("м").x_advance
    return x


# гриф
c.save(); c.translate(PX + PW - 345, PY + 85); c.rotate(-0.05)
c.set_source_rgba(0.62, 0.12, 0.12, 0.75); c.set_line_width(3)
c.rectangle(0, -36, 300, 52); c.stroke()
font("Oswald", 26, bold=True); c.move_to(14, 2); c.show_text("СОВЕРШЕННО СЕКРЕТНО")
c.restore()
font("Old Standard TT", 19, italic=True); c.set_source_rgb(0.2, 0.18, 0.16)
c.move_to(PX + 50, PY + 60); c.show_text("Особая папка «НЕКРОНОМИКОНЪ»")
c.move_to(PX + 50, PY + 88); c.show_text("Экз. № 2 (изъ 9)")

center("Р. С. Ф. Г. Р.", PY + 175, size=26)
center("ЧЕРНОЕ ПОЛИТБЮРО", PY + 225, face="Oswald", size=46, bold=True, rgb=(0.55, 0.10, 0.10))
center("ВЫПИСКА ИЗЪ ПРОТОКОЛА № 13/666", PY + 285, size=32, bold=True)
center("расширеннаго засѣданія 27 октября 1973 г.", PY + 325, size=24, italic=True)
center("Залъ Тысячи Щупалецъ · 0 ч. 13 м. — 3 ч. 33 м.", PY + 360, size=21)
center("Споролѣтіе LIII · 23-й годъ Эры Пробужденія", PY + 392, size=21)
c.set_source_rgb(0.3, 0.27, 0.24); c.set_line_width(1.2)
c.move_to(PX + 300, PY + 420); c.line_to(PX + PW - 300, PY + 420); c.stroke()

x0, y = PX + 70, PY + 485
LINES = [
    ("СЛУШАЛИ:", 0),
    ("О директивныхъ указаніяхъ Спящаго Вождя,", 1),
    ("полученныхъ въ сеансѣ коллективнаго", 1),
    ("сновидѣнія. Вождь выразилъ крайнее", 1),
    ("неудовольствіе темпами пробужденія.", 1),
    ("", 0),
    ("ПОСТАНОВИЛИ:", 0),
    ("1. Пробужденіе ускорить.", 1),
    ("2. Предложеніе т. Команданте о личномъ", 1),
    ("   погруженіи на глубину 3000 метровъ", 1),
    ("   принять.", 1),
    ("3. Островъ Куба считать карибскимъ", 1),
    ("   форпостомъ Древнихъ съ момента", 1),
    ("   погруженія.", 1),
    ("4. Будильникомъ впредь не пользоваться.", 1),
]
for text, ind in LINES:
    if text:
        typed(text, x0 + ind * 30, y)
    y += 40

# резолюция от руки
c.save(); c.translate(PX + 430, PY + PH - 250); c.rotate(-0.12)
font("Old Standard TT", 40, italic=True); c.set_source_rgba(0.10, 0.25, 0.62, 0.9)
c.move_to(0, 0); c.show_text("Къ исполненію.")
c.set_line_width(2.4); c.move_to(250, 30)
c.curve_to(280, -10, 300, 60, 340, 20); c.curve_to(360, 0, 380, 45, 420, 25); c.stroke()
c.restore()

# карандаш
font("Old Standard TT", 24, italic=True); c.set_source_rgba(0.35, 0.35, 0.37, 0.8)
c.move_to(PX + PW - 100, PY + 150); c.show_text("л. 13")
c.move_to(PX + 50, PY + 125); c.show_text("Арх. 28/X-73")

# круглая печать
cx, cy, rr = PX + 230, PY + PH - 185, 105
c.set_source_rgba(0.42, 0.28, 0.58, 0.6)
c.new_path(); c.set_line_width(4); c.arc(cx, cy, rr, 0, 2 * math.pi); c.stroke()
c.new_path(); c.set_line_width(2); c.arc(cx, cy, rr - 34, 0, 2 * math.pi); c.stroke()
font("Old Standard TT", 21, bold=True)
ring = "ЧЕРНОЕ · ПОЛИТБЮРО · Р.С.Ф.Г.Р. ·"
ang = -math.pi * 0.95
for ch in ring:
    c.save(); c.translate(cx + (rr - 24) * math.cos(ang), cy + (rr - 24) * math.sin(ang))
    c.rotate(ang + math.pi / 2); c.move_to(-c.text_extents(ch).x_advance / 2, 0); c.show_text(ch); c.restore()
    ang += 2 * math.pi / (len(ring) + 1)
c.new_path(); c.set_line_width(3)
for k in range(200):
    t = k / 200 * 5 * math.pi; r = 3 + t * 3.6
    (c.line_to if k else c.move_to)(cx + r * math.cos(t), cy + r * math.sin(t))
c.stroke()

center("Ктулху фхтагнъ — Ленинъ фхтагнъ.", PY + PH - 45, size=20)
c.restore()
s.write_to_png(out)

im = Image.open(out).convert("RGB")
a = np.asarray(im).astype(np.float32)
rng = np.random.default_rng(13666)
yy, xx = np.mgrid[0:H, 0:W]
stain = np.zeros((H, W), np.float32)
for _ in range(6):
    sx, sy, sr = rng.uniform(100, W - 100), rng.uniform(100, H - 100), rng.uniform(90, 280)
    stain += np.exp(-((xx - sx) ** 2 + (yy - sy) ** 2) / (2 * sr ** 2)) * rng.uniform(0.03, 0.09)
a = a * (1 - stain[..., None] * np.array([0.5, 0.85, 1.4])) + rng.normal(0, 4.5, (H, W))[..., None]
Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)).save(out)
print(out)
