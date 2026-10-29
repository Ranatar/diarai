"""Сжимаемость узора: python3 cmp/compress.py STEPS < rules -> rule w h ones bits_per_cell
bits_per_cell = 8*len(zlib(lzma) упакованных бит цвета) / площадь рамки. Хаос ~0.5–1, порядок << 0.1."""
import sys, subprocess, os, tempfile, lzma
import numpy as np
from PIL import Image
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
steps = sys.argv[1]
tmp = tempfile.mkdtemp()
for l in sys.stdin:
    r = int(l.split()[0]); p = os.path.join(tmp, 'x.pgm')
    subprocess.run([os.path.join(here, 'render'), str(r), steps, p], check=True, capture_output=True)
    a = np.array(Image.open(p)) < 100
    h, w = a.shape
    z = len(lzma.compress(np.packbits(a).tobytes(), preset=6))
    print(r, w, h, int(a.sum()), f'{8 * z / (w * h):.4f}', flush=True)
