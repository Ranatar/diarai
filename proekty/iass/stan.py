"""Семилинейный стан иасского письма по § 4.4 спецификации (inbox/html-generated/iass-spec.html).
Линии снизу вверх: Р М Т В У Ж Г. Залитый круг — эмиссивный (⁺), контурный — отражательный (⁻),
контурный ромб — пол М; поляризация — штрих (| = ( ) %), модуляция — хвост (. точка сверху,
: зигзаг, / штрих вверх, \\ штрих вниз). Столбцы аккорда связаны тонким стержнем (лигатура),
граница слова — пунктир. python3 stan.py out.png"""
import sys
from PIL import Image, ImageDraw, ImageFont

REG = "РМТВУЖГ"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# песнь «Третий при видимом»: (строка, [(регистр, инт, пол, мод), ...], подпись)
SONG = [
    (1, [("Т", "+", "", ".")], "тепло"),
    (1, [("Т", "+", "", ".")], "тепло"),
    (1, [("Р", "+", "", ""), ("М", "0", "", "")], "тви·Т"),
    (2, [("Р", "+", "", ""), ("Т", "+", "", "")], "сэ·В"),
    (3, [("В", "-", "=", "")], "отблеск"),
    (4, [("В", "-", "=", "")], "взаймы"),
    (5, [("М", "0", "", ""), ("Т", "-", "", "")], "мо-тэль⁻"),
    (6, [("М", "0", "", "")], "мо"),
]

def main(out):
    L0, DX, DY, TOP = 70, 78, 34, 50
    W = L0 + DX * len(SONG) + 40
    H = TOP + DY * 6 + 110
    im = Image.new("RGB", (W, H), (246, 241, 228))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 15)
    fs = ImageFont.truetype(FONT, 12)
    ink = (40, 34, 28)
    y = {r: TOP + DY * (6 - i) for i, r in enumerate(REG)}
    for r in REG:
        d.line((L0 - 10, y[r], W - 20, y[r]), fill=(150, 140, 120), width=1)
        d.text((18, y[r] - 9), r, font=f, fill=ink)
    prev = None
    for k, (line, chord, label) in enumerate(SONG):
        x = L0 + DX * k + DX // 2
        if prev is not None:  # граница слова — пунктир; граница строки — пунктир гуще
            xb = x - DX // 2
            step = 4 if prev != line else 9
            for yy in range(TOP - 15, TOP + DY * 6 + 15, step * 2):
                d.line((xb, yy, xb, yy + step), fill=(120, 110, 95), width=1)
        if prev != line:
            d.text((x - 5, 12), str(line), font=f, fill=(120, 60, 40))
        prev = line
        ys = [y[r] for r, *_ in chord]
        if len(ys) > 1:
            d.line((x, min(ys), x, max(ys)), fill=ink, width=2)
        for r, inten, pol, mod in chord:
            yy, R = y[r], 9
            if inten == "0":  # пол М — контурный ромб
                d.polygon([(x, yy - R - 2), (x + R + 2, yy), (x, yy + R + 2), (x - R - 2, yy)],
                          outline=ink, fill=(246, 241, 228), width=2)
            elif inten == "+":
                d.ellipse((x - R, yy - R, x + R, yy + R), fill=ink)
            else:
                d.ellipse((x - R, yy - R, x + R, yy + R), outline=ink, fill=(246, 241, 228), width=2)
            if pol == "=":
                d.line((x - R - 6, yy, x + R + 6, yy), fill=ink, width=2)
            elif pol == "|":
                d.line((x, yy - R - 6, x, yy + R + 6), fill=ink, width=2)
            if mod == ".":
                d.ellipse((x - 2, yy - R - 9, x + 2, yy - R - 5), fill=ink)
            elif mod == "/":
                d.line((x + R, yy - R, x + R + 8, yy - R - 10), fill=ink, width=2)
            elif mod == "\\":
                d.line((x + R, yy + R, x + R + 8, yy + R + 10), fill=ink, width=2)
        tw = d.textlength(label, font=fs)
        d.text((x - tw / 2, TOP + DY * 6 + 22), label, font=fs, fill=ink)
    d.text((L0 - 10, H - 40), "Третий при видимом · стан по § 4.4 · строки 1–6, пунктир — границы слов",
           font=fs, fill=(110, 100, 85))
    im.save(out)

if __name__ == "__main__":
    main(sys.argv[1])
