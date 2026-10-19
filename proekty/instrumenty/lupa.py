#!/usr/bin/env python3
"""Лупа: вырезать кусок картинки и увеличить.
ext/venv-pdf/bin/python -I proekty/instrumenty/lupa.py картинка.png выход.png x0 y0 x1 y1 [во_сколько_раз=3]
Координаты — в пикселях исходника (как на превью при Read, если превью не уменьшено)."""
import sys
from PIL import Image

a = sys.argv[1:]
im = Image.open(a[0])
x0, y0, x1, y1 = map(int, a[2:6])
k = float(a[6]) if len(a) > 6 else 3
print('исходник', im.size)
c = im.crop((x0, y0, x1, y1))
c = c.resize((int(c.width * k), int(c.height * k)), Image.LANCZOS)
c.save(a[1])
print('сохранено', a[1], c.size)
