# пространство-время зоны за эпоху: строка = клетка (bd-1 сверху), x = время, цвет = тип цикла (B=20, C/D=12, E=8)
import sys, os
from PIL import Image, ImageDraw, ImageFont
t0, t1 = int(sys.argv[1]), int(sys.argv[2]); files = sys.argv[3:-1]; out = sys.argv[-1]
W, RH, GAP, LM, TM = 1200, 46, 6, 90, 40
COL = {20: (0x2a,0x78,0xd6), 12: (0xeb,0x68,0x34), 8: (0x1b,0xaf,0x7a)}
def periods(T):
    per = [0]*len(T); i = 0
    while i < len(T):
        best = None
        for p in (20, 12, 8):
            if i+2*p <= len(T) and T[i:i+p] == T[i+p:i+2*p]: best = p; break
        if best is None: i += 1; continue
        p = best; j = i+p
        while j+p <= len(T) and T[j:j+p] == T[i:i+p]: j += p
        for k in range(i, j): per[k] = p
        i = j
    return per
H = TM + len(files)*(RH+GAP) + 50
img = Image.new('RGB', (LM+W+20, H), (0xfc,0xfc,0xfb)); d = ImageDraw.Draw(img)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
except: f = ImageFont.load_default()
for r, fn in enumerate(files):
    L = [l.split() for l in open(fn)]; T = [a[1] for a in L]; N = [int(a[0]) for a in L]
    per = periods(T)
    cnt = [dict() for _ in range(W)]
    for n, p in zip(N, per):
        x = min(W-1, int((n-t0)/(t1-t0)*W)); cnt[x][p] = cnt[x].get(p, 0)+1
    y = TM + r*(RH+GAP)
    for x in range(W):
        if not cnt[x]: continue
        p = max(cnt[x], key=cnt[x].get)
        d.line([(LM+x, y), (LM+x, y+RH)], fill=COL.get(p, (0xb0,0xb0,0xa8)))
    d.text((8, y+RH//2-8), 'bd−%d' % (r+1), fill=(0x0b,0x0b,0x0b), font=f)
d.text((LM, 10), 'эпоха 13 правила 26427: время →, клетки зоны ↓', fill=(0x0b,0x0b,0x0b), font=f)
lx = LM; ly = H-35
for p, name in ((20, 'B (20 переходов, пропуск 1/4)'), (12, 'C/D (12, пропуск 1/2)'), (8, 'E (8)')):
    d.rectangle([lx, ly, lx+14, ly+14], fill=COL[p]); d.text((lx+20, ly-2), name, fill=(0x52,0x51,0x4e), font=f); lx += 300
img.save(out)
