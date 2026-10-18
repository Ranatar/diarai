"""Семилинейный стан иасского письма по § 4.4 спецификации (inbox/html-generated/iass-spec.html).
Линии снизу вверх: Р М Т В У Ж Г. Залитый круг — эмиссивный (⁺), контурный — отражательный (⁻),
контурный ромб — пол М; поляризация — штрих (| = ( ) %), модуляция — хвост (. точка сверху,
: зигзаг, / штрих вверх, \\ штрих вниз). Столбцы аккорда связаны тонким стержнем (лигатура),
граница слова — пунктир. python3 stan.py out.png"""
import sys
from PIL import Image, ImageDraw, ImageFont

REG = "РМТВУЖГ"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# (строка, [(регистр, инт, пол, мод), ...], подпись[, доплер "up"/"down"]); инт "+~" — широкий эмиссивный
SONGS = {
    "tretiy": [  # «Третий при видимом» (proekty/iass/tretiy.md)
        (1, [("Т", "+", "", ".")], "тепло"),
        (1, [("Т", "+", "", ".")], "тепло"),
        (1, [("Р", "+", "", ""), ("М", "0", "", "")], "тви·Т"),
        (2, [("Р", "+", "", ""), ("Т", "+", "", "")], "сэ·В"),
        (3, [("В", "-", "=", "")], "отблеск"),
        (4, [("В", "-", "=", "")], "взаймы"),
        (5, [("М", "0", "", ""), ("Т", "-", "", "")], "мо-тэль⁻"),
        (6, [("М", "0", "", "")], "мо"),
    ],
    "motel": [  # «Мо и тэль» из спецификации § 9.2 — для сверки с образцом автора
        (1, [("М", "0", "", "")], "мо"),
        (2, [("Т", "+", "", "/")], "тэль-са"),
        (2, [("Т", "+", "", ".")], "тэль·"),
        (3, [("Т", "+~", "", ""), ("В", "-", "", ""), ("У", "+", "", "")], "тэльвэ-виг", "up"),
        (4, [("Т", "+", "", "\\")], "тэль-ша\\", "down"),
        (5, [("М", "0", "", ""), ("Т", "-", "", "")], "мо-тэль⁻"),
    ],
}

def main(out, name="tretiy"):
    SONG = SONGS[name]
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
    for k, (line, chord, label, *rest) in enumerate(SONG):
        x = L0 + DX * k + DX // 2
        if prev is not None and prev != line:  # пунктир — граница строки; слова внутри строки — просто пробел (как в образце)
            xb = x - DX // 2
            for yy in range(TOP - 15, TOP + DY * 6 + 15, 8):
                d.line((xb, yy, xb, yy + 3), fill=(120, 110, 95), width=1)
        if prev != line:
            d.text((x - 5, 12), str(line), font=f, fill=(120, 60, 40))
        prev = line
        # стержня внутри аккорда у автора нет (сверено с образцом в iass-spec.html, svg_razbor.py)
        for r, inten, pol, mod in chord:
            yy, R = y[r], 9
            if inten == "0":  # пол М — контурный ромб
                d.polygon([(x, yy - R - 2), (x + R + 2, yy), (x, yy + R + 2), (x - R - 2, yy)],
                          outline=ink, fill=(246, 241, 228), width=2)
                d.ellipse((x - 2, yy - 2, x + 2, yy + 2), fill=ink)  # точка в ромбе, как у автора
            elif inten == "+~":  # широкий — вытянутая линза
                d.ellipse((x - 2 * R, yy - R, x + 2 * R, yy + R), fill=ink)
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
            elif mod in ("/", "\\"):  # хвост со стрелкой, как в образце автора
                s = -1 if mod == "/" else 1
                x2, y2 = x + R + 14, yy + s * (R + 14)
                d.line((x + R - 2, yy + s * (R - 4), x2, y2), fill=ink, width=2)
                d.line((x2, y2, x2 - 7, y2), fill=ink, width=2)
                d.line((x2, y2, x2, y2 - s * 7), fill=ink, width=2)
        if rest:  # Доплер: ▲ синий (приближение), ▼ красный (удаление), сбоку от столбца
            tx, ty = x + 26, TOP + DY * 3
            if rest[0] == "up":
                d.polygon([(tx, ty - 8), (tx + 8, ty + 6), (tx - 8, ty + 6)], fill=(60, 110, 190))
            else:
                d.polygon([(tx, ty + 8), (tx + 8, ty - 6), (tx - 8, ty - 6)], fill=(190, 70, 60))
        tw = d.textlength(label, font=fs)
        d.text((x - tw / 2, TOP + DY * 6 + 22), label, font=fs, fill=ink)
    title = {"tretiy": "Третий при видимом", "motel": "Мо и тэль (§ 9.2, для сверки)"}[name]
    d.text((L0 - 10, H - 40), title + " · стан по § 4.4 и образцу § 9.2 · пунктир — границы строк", font=fs, fill=(110, 100, 85))
    im.save(out)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "tretiy")
