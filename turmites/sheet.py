"""Лист с миниатюрами: python3 sheet.py out.png STEPS rule1 rule2 ..."""
import sys, subprocess, os, tempfile
from PIL import Image, ImageDraw

out, steps, rules = sys.argv[1], sys.argv[2], [int(r) for r in sys.argv[3:]]
T, cols = 220, 6
here = os.path.dirname(os.path.abspath(__file__))
rows = (len(rules) + cols - 1) // cols
sheet = Image.new('L', (cols * T, rows * (T + 16)), 255)
dr = ImageDraw.Draw(sheet)
with tempfile.TemporaryDirectory() as tmp:
    for i, r in enumerate(rules):
        p = os.path.join(tmp, f'{r}.pgm')
        subprocess.run([os.path.join(here, os.environ.get('RENDER', 'render')), str(r), steps, p], check=True, capture_output=True)
        im = Image.open(p)
        w, h = im.size
        k = (T - 8) / max(w, h)
        im = im.resize((max(1, int(w * k)), max(1, int(h * k))), Image.LANCZOS if k < 1 else Image.NEAREST)
        cx, cy = (i % cols) * T, (i // cols) * (T + 16)
        sheet.paste(im, (cx + (T - im.size[0]) // 2, cy + (T - im.size[1]) // 2))
        dr.text((cx + 4, cy + T), f'{r}  {w}x{h}', fill=0)
sheet.save(out)
