"""SVG: сколько классов решается в каждом десятилетии — моя перепись и Еронимус (вики Golly)."""
import csv, math, collections, sys
c = collections.Counter()
for r in csv.DictReader(open('catalog2.csv')):
    if r['kind'] in ('highway', 'loop', 'double', 'wedge', 'unary') and r['onset']:
        c[max(0, math.ceil(math.log10(abs(int(r['onset'])) + 1)))] += 1
J = {4: 104, 5: 59, 6: 40, 7: 35, 8: 25, 9: 29, 10: 20, 11: 1, 12: 1, 13: 1}
ks = list(range(4, 14)); W, H, L, B, T = 760, 380, 60, 60, 50
ymax = 120; bw = 22; step = (W - L - 20) / len(ks)
y = lambda v: H - B - (H - B - T) * v / ymax
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="sans-serif" font-size="12">',
     f'<rect width="{W}" height="{H}" fill="#fcfcfb"/>',
     f'<text x="{L}" y="22" font-size="15" fill="#1d1d1b">Сколько классов 2×2 развязывается в каждом десятилетии времени</text>',
     f'<text x="{L}" y="40" fill="#5f5e5a">развязка = шоссе, петля, двойное шоссе, клин; столбец 10^k — начало в (10^(k−1), 10^k]</text>']
for v in range(0, ymax + 1, 20):
    o.append(f'<line x1="{L}" x2="{W-20}" y1="{y(v)}" y2="{y(v)}" stroke="#e4e3df" stroke-width="1"/>')
    o.append(f'<text x="{L-8}" y="{y(v)+4}" text-anchor="end" fill="#5f5e5a">{v}</text>')
for i, k in enumerate(ks):
    x0 = L + i * step + step / 2
    for j, (val, col) in enumerate([(c.get(k, 0), '#2a78d6'), (J.get(k), '#eb6834')]):
        if val is None: continue
        x = x0 - bw - 1 + j * (bw + 2)
        o.append(f'<rect x="{x}" y="{y(val)}" width="{bw}" height="{y(0)-y(val)}" rx="3" fill="{col}"><title>10^{k}: {val}</title></rect>')
        if val: o.append(f'<text x="{x+bw/2}" y="{y(val)-4}" text-anchor="middle" font-size="10" fill="#5f5e5a">{val}</text>')
    o.append(f'<text x="{x0}" y="{H-B+18}" text-anchor="middle" fill="#1d1d1b">10<tspan dy="-5" font-size="9">{k}</tspan></text>')
o.append(f'<text x="{x0+8 - step*1.5}" y="{H-12}" text-anchor="middle" fill="#5f5e5a">мой прогон пока до 2^30 ≈ 1,07·10^9</text>')
lx = W - 300
o.append(f'<rect x="{lx}" y="58" width="12" height="12" rx="2" fill="#2a78d6"/><text x="{lx+18}" y="69" fill="#1d1d1b">моя перепись (2825 классов хода)</text>')
o.append(f'<rect x="{lx}" y="78" width="12" height="12" rx="2" fill="#eb6834"/><text x="{lx+18}" y="89" fill="#1d1d1b">Еронимус, «уникальные» (вики Golly)</text>')
o.append('</svg>')
open(sys.argv[1], 'w').write('\n'.join(o))
