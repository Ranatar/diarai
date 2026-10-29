"""Разбор переписи: канонизация правил и классификация поведения."""
import csv, glob, sys, collections, math

def entries(rule):
    return [((rule >> (4 * e)) & 1, (rule >> (4 * e + 1)) & 3, (rule >> (4 * e + 3)) & 1) for e in range(4)]

def pack(ent):
    r = 0
    for e, (w, t, n) in enumerate(ent):
        r |= (w | (t << 1) | (n << 3)) << (4 * e)
    return r

def reachable(rule):
    ent = entries(rule)
    states, colors = {0}, {0}
    used = set()
    while True:
        new = {(s, c) for s in states for c in colors} - used
        if not new:
            return used
        used |= new
        for s, c in new:
            w, t, n = ent[s * 2 + c]
            states.add(n); colors.add(w)

def canon(rule):
    used = reachable(rule)
    ent = entries(rule)
    ent = [ent[e] if (e // 2, e % 2) in used else (0, 0, 0) for e in range(4)]
    mirror = [(w, {1: 3, 3: 1}.get(t, t), n) for w, t, n in ent]
    return min(pack(ent), pack(mirror)), len(used)

def classify(r, steps):
    run = int(r['steps_run']); p = int(r['period'])
    dx, dy = int(r['pdx']), int(r['pdy'])
    w = int(r['maxx']) - int(r['minx']) + 1; h = int(r['maxy']) - int(r['miny']) + 1
    if p and (dx or dy):
        return 'highway'
    if p and w * h <= 4:
        return 'tiny'          # ходит на месте / почти ничего не меняет
    if p:
        return 'cycle'
    if int(r['escaped']):
        return 'escaped-aperiodic'
    if int(r['last_growth']) < run // 2:
        return 'bounded'
    size = max(w, h)
    # рост размера ~ t^a: оценим a по одному концу (грубо)
    return 'growing'

def load():
    rows = []
    for f in sorted(glob.glob('out/part*.csv')):
        rows += list(csv.DictReader(open(f)))
    return rows

if __name__ == '__main__':
    rows = load()
    steps = 1_000_000
    classes = {}
    for r in rows:
        rule = int(r['rule'])
        c, nused = canon(rule)
        if c not in classes:
            classes[c] = (r, nused)
    print('всего правил', len(rows), 'классов эквивалентности', len(classes))
    cnt = collections.Counter()
    by = collections.defaultdict(list)
    for c, (r, nused) in classes.items():
        k = classify(r, steps)
        cnt[k] += 1
        by[k].append((c, r, nused))
    for k, v in cnt.most_common():
        print(f'{k:20s} {v}')
    # периоды шоссе
    per = collections.Counter(int(r['period']) for c, r, n in by['highway'])
    print('\nпериоды шоссе (топ 25):', per.most_common(25))
    print('самые длинные периоды:', sorted(per)[-15:])
    with open('classes.csv', 'w', newline='') as f:
        wr = csv.writer(f)
        wr.writerow(['canon', 'class', 'used_entries', 'period', 'pdx', 'pdy', 'steps_run', 'w', 'h', 'ones', 'last_growth'])
        for k, lst in by.items():
            for c, r, n in sorted(lst, key=lambda z: z[0]):
                wr.writerow([c, k, n, r['period'], r['pdx'], r['pdy'], r['steps_run'],
                             int(r['maxx']) - int(r['minx']) + 1, int(r['maxy']) - int(r['miny']) + 1,
                             r['ones'], r['last_growth']])
