"""Рекорды шоссе по out/onsetA*.txt: фильтр артефактов края (после начала шоссе путь >= 2000 клеток)."""
import glob, collections
rows = [list(map(int, l.split())) for f in sorted(glob.glob('out/onsetA*.txt')) for l in open(f) if len(l.split()) == 7]
real, edge, other = [], [], []
for r in rows:
    rule, t, esc, p, dx, dy, on = r
    if esc and p and (t - on) / p * max(abs(dx), abs(dy)) >= 2000: real.append(r)
    elif esc: edge.append(r)
    else: other.append(r)
if __name__ == '__main__':
    print('всего', len(rows), 'настоящих шоссе', len(real), 'край/без периода', len(edge), 'не вышли за 4M', len(other))
    c = collections.Counter()
    for r in real:
        o = r[6]; c[0 if o == 0 else len(str(o))] += 1
    print('начало шоссе: число цифр ->', sorted(c.items()))
    print('\nдольше всех хаос до шоссе:')
    for r in sorted(real, key=lambda r: -r[6])[:15]: print('  rule %6d  начало %9d  период %6d  смещение (%d,%d)' % (r[0], r[6], r[3], r[4], r[5]))
    print('\nсамые длинные периоды:')
    for r in sorted(real, key=lambda r: -r[3])[:12]: print('  rule %6d  период %6d  смещение (%d,%d)  начало %d' % (r[0], r[3], r[4], r[5], r[6]))
    pc = collections.Counter(r[3] for r in real)
    print('\nчастые периоды:', pc.most_common(20))
    print('различных периодов:', len(pc))
