"""Каталог: одна строка на класс хода (canon3). Сводит все источники:
перепись (out/part*.csv, 10^6), рост (growth.csv до 2^24, out/growthC* до 2^26),
начало шоссе/петли (out/onsetA,E,F,D). Пишет catalog.csv и печатает сводку."""
import csv, glob, collections
from canon2 import CANON2
from canon3 import CANON3
from analyze import classify

def onset_rows():
    out = {}
    for f in sorted(glob.glob('out/onset[A-Z]*.txt')) + (['out/onsetD.txt'] if False else []):
        for l in open(f):
            p = l.split()
            if len(p) != 7: continue
            rule, t, esc, per, dx, dy, on = map(int, p)
            if per and (dx or dy):
                if esc and (t - on) / per * max(abs(dx), abs(dy)) >= 2000:
                    kind = 'highway'
                else:
                    continue  # край поля или незавершённое — не считаем
            elif per:
                kind = 'loop'
            else:
                continue
            prev = out.get(rule)
            if prev is None or t > prev[1]:  # более длинный прогон надёжнее
                out[rule] = (kind, t, per, dx, dy, on)
    return out

def growth_rows():
    g = {}
    for r in csv.DictReader(open('growth.csv')):
        if r['status'] == 'ok':
            g[int(r['rule'])] = (24, float(r['a_size']), float(r['b_ones']))
    for f in glob.glob('out/growthC*.txt'):
        for l in open(f):
            p = l.split()
            if len(p) != 20: continue
            v = [tuple(map(int, q.split(':'))) for q in p[1:]]
            s = {k + 8: v[k] for k in range(len(v))}
            if s[26][0] > 0:
                import math
                a = math.log2(s[26][0] / s[18][0]) / 8
                b = math.log2(max(s[26][1], 1) / max(s[18][1], 1)) / 8
                g[int(p[0])] = (26, a, b)
    return g

def build():
    census = {int(r['rule']): r for f in sorted(glob.glob('out/part*.csv')) for r in csv.DictReader(open(f))}
    ons, gro = onset_rows(), growth_rows()
    members = collections.defaultdict(list)
    for r in range(65536):
        members[CANON3[CANON2[r]]].append(r)
    cat = []
    for c, rs in sorted(members.items()):
        labs = collections.Counter(classify(census[r], 10 ** 6) for r in rs)
        o = next((ons[r] for r in rs if r in ons and ons[r][0] == 'highway'), None) or \
            next((ons[r] for r in rs if r in ons), None)
        g = next((gro[r] for r in rs if r in gro), None)
        kind = labs.most_common(1)[0][0]
        if o:
            kind = o[0]
        elif g:
            a = g[1]
            kind = 'counter' if a < 0.15 else 'slow' if a < 0.25 else 'chaotic' if a < 0.45 else 'ordered'
        elif kind == 'tiny':
            kind = 'cycle'
        elif kind == 'growing':
            kind = 'growing?'
        cat.append(dict(rep=c, raw=len(rs), kind=kind, census=labs.most_common(1)[0][0],
                        onset=o[5] if o else '', period=o[2] if o else '', dx=o[3] if o else '', dy=o[4] if o else '',
                        a=f'{g[1]:.3f}' if g else '', b=f'{g[2]:.3f}' if g else '', growth_to=g[0] if g else ''))
    return cat

if __name__ == '__main__':
    cat = build()
    with open('catalog.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(cat[0]))
        w.writeheader(); w.writerows(cat)
    cnt = collections.Counter(c['kind'] for c in cat)
    raw = collections.Counter()
    for c in cat: raw[c['kind']] += c['raw']
    print('классов хода:', len(cat))
    for k, v in cnt.most_common(): print(f'  {k:10s} {v:5d} классов, {raw[k]:6d} правил')
