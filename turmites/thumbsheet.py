"""Листы из готовых миниатюр прогона 2^32: python3 thumbsheet.py [dir] -> img/t32/sheet-N.png
Подпись: номер, единиц, рамка. Порядок — по номеру правила; 7×6 на лист."""
import sys, os, glob
from PIL import Image, ImageDraw
d = sys.argv[1] if len(sys.argv) > 1 else 'out/v4/thumbs'
st = {}
for f in glob.glob('out/v4/st32_*.txt'):
    for l in open(f):
        p = l.split()
        if len(p) == 4: st[int(p[0])] = p[1:]
res = {}
for f in glob.glob('out/v4/on32_*.txt'):
    for l in open(f):
        p = l.split()
        if len(p) == 7: res[int(p[0])] = p
rules = sorted(int(os.path.basename(f)[:-4]) for f in glob.glob(d + '/*.pgm') if int(os.path.basename(f)[:-4]) in res)
T, cols, rows = 200, 7, 6
os.makedirs('img/t32', exist_ok=True)
for n in range(0, len(rules), cols * rows):
    chunk = rules[n:n + cols * rows]
    sh = Image.new('L', (cols * T, ((len(chunk) + cols - 1) // cols) * (T + 28)), 255)
    dr = ImageDraw.Draw(sh)
    for i, r in enumerate(chunk):
        im = Image.open(f'{d}/{r}.pgm'); w, h = im.size
        k = (T - 8) / max(w, h)
        im = im.resize((max(1, int(w * k)), max(1, int(h * k))), Image.NEAREST if k >= 1 else Image.LANCZOS)
        cx, cy = (i % cols) * T, (i // cols) * (T + 28)
        sh.paste(im, (cx + (T - im.size[0]) // 2, cy + (T - im.size[1]) // 2))
        p = res[r]; s = st.get(r, ['?', '?', '?'])
        flag = ' ВЫХОД' if p[2] == '1' else (f' P{p[3]}' if p[3] != '0' else '')
        dr.text((cx + 4, cy + T), f'{r}{flag}', fill=0)
        dr.text((cx + 4, cy + T + 12), f'{s[0]} ед, {s[1]}x{s[2]}', fill=90)
    sh.save(f'img/t32/sheet-{n // (cols * rows) + 1}.png')
print(len(rules), 'миниатюр')
