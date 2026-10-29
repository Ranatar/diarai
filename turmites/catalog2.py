"""Каталог v2: строка на класс хода (canon3), только чистые данные.
- out/v2/onset8k_*.txt — onset (с MINW) до 2^24 на поле 8192 для всех представителей canon3;
- out/v2/onset4k_*.txt — тот же onset на поле 4096 для шоссе с началом > 10^6 (проверка края);
- out/v2/deep28.txt — догонка нерешённых до 2^28 (onsetr на двух полях);
- growth.csv, out/growth[A-Z]*.txt — показатели роста (их ошибка с периодом не касалась).
Виды: highway, loop, counter, slow, chaotic, ordered (растёт упорядоченно / упёрся в край без шоссе), unknown.
Пишет catalog2.csv, печатает сводку. Нужные прогоны — см. NOTES.md."""
import os, csv, glob, collections, math
from canon2 import CANON2
from canon3 import CANON3

def rows(pattern):
    out = {}
    for f in sorted(glob.glob(pattern)):
        for l in open(f):
            p = l.split()
            if len(p) == 7: out[int(p[0])] = list(map(int, p))
    return out

def deep_rows():
    """out/v2/deep28.txt: секции «поле 8192» и «поле 4096» (строки onset)."""
    o8, o4, cur = {}, {}, None
    for l in open('out/v2/deep28.txt').readlines() + open('out/v3/deep30.txt').readlines():
        if l.startswith('#'):
            cur = (o4 if ('4096' in l or 'проверочное' in l) else
                   o8 if ('8192' in l or 'основное' in l) else cur)
            continue
        p = l.split()
        if len(p) == 7 and cur is not None: cur[int(p[0])] = list(map(int, p))
    return o8, o4

def growth_rows():
    g = {}
    for r in csv.DictReader(open('growth.csv')):
        if r['status'] == 'ok': g[int(r['rule'])] = (24, float(r['a_size']), float(r['b_ones']))
    for f in sorted(glob.glob('out/growth[A-Z]*.txt')):
        for l in open(f):
            p = l.split()
            v = [tuple(map(int, q.split(':'))) for q in p[1:]]
            s = {k + 8: v[k] for k in range(len(v))}
            K = max(s) if s else 0
            if len(v) < 12 or s[K][0] <= 0: continue
            a = math.log2(s[K][0] / s[K - 8][0]) / 8
            b = math.log2(max(s[K][1], 1) / max(s[K - 8][1], 1)) / 8
            r = int(p[0])
            if r not in g or g[r][0] < K: g[r] = (K, a, b)
    return g

def kind_by_growth(a):
    return 'counter' if a < 0.15 else 'slow' if a < 0.25 else 'chaotic' if a < 0.45 else 'ordered'

def build():
    o8, o4, gro = rows('out/v2/onset8k_*.txt'), rows('out/v2/onset4k_*.txt'), growth_rows()
    d8, d4 = deep_rows()
    o8.update(d8); o4.update(d4)   # догонка до 2^28 важнее прогона до 2^24
    members = collections.defaultdict(list)
    for r in range(65536): members[CANON3[CANON2[r]]].append(r)
    comp = {}
    if os.path.exists('cmp/ordered_compress.txt'):
        for l in open('cmp/ordered_compress.txt'):
            p = l.split(); comp[int(p[0])] = (int(p[1]), int(p[2]), float(p[4]))
    manual = {int(r['rep']): r for r in csv.DictReader(open('kinds_manual.csv'))} if os.path.exists('kinds_manual.csv') else {}
    cat = []
    for c, rs in sorted(members.items()):
        o = o8.get(c)
        g = next((gro[r] for r in [c] + rs if r in gro), None)
        rec = dict(rep=c, raw=len(rs), kind='unknown', onset='', period='', dx='', dy='', checked4k='',
                   a=f'{g[1]:.3f}' if g else '', b=f'{g[2]:.3f}' if g else '', growth_to=g[0] if g else '')
        if o is None:
            cat.append(rec); continue
        _, t, esc, p, dx, dy, on = o
        if p and (dx or dy) and esc:
            real = True
            if on > 10 ** 6:
                q = o4.get(c)
                if q is None: real = None
                else: real = (q[3] == p and q[6] == on); rec['checked4k'] = int(real)
            if real is None:
                rec['kind'] = 'highway?'
            elif real:
                rec['kind'] = 'highway'
            else:
                rec['kind'] = 'ordered'   # упёрся в край без настоящего шоссе
            if real is not False:
                rec.update(onset=on, period=p, dx=dx, dy=dy)
        elif p and not (dx or dy) and not esc:
            rec.update(kind='loop', onset=on, period=p)
        elif esc:
            # вышел без шоссе: упорядоченная фигура — или хаотическое пятно, которому мало поля
            rec['kind'] = 'chaotic' if g and g[1] < 0.45 else 'ordered'
        else:
            rec['kind'] = kind_by_growth(g[1]) if g else 'unknown'
        # «упорядоченный», но узор не сжимается (cmp/compress.py, 2^22 шагов) — это хаос
        z = comp.get(c)
        if rec['kind'] == 'ordered' and z and min(z[0], z[1]) >= 20 and z[2] >= 0.4:
            rec['kind'] = 'chaotic'
        # исходы, которых onsetr не видит (двойное шоссе, челнок, клин): kinds_manual.csv
        if c in manual:
            rec['kind'] = manual[c]['kind']; rec['onset'] = manual[c]['onset']
        cat.append(rec)
    return cat

if __name__ == '__main__':
    cat = build()
    with open('catalog2.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(cat[0])); w.writeheader(); w.writerows(cat)
    cnt, raw = collections.Counter(), collections.Counter()
    for c in cat: cnt[c['kind']] += 1; raw[c['kind']] += c['raw']
    print('классов хода:', len(cat))
    for k, v in cnt.most_common(): print(f'  {k:10s} {v:5d} классов, {raw[k]:6d} правил')
