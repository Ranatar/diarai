"""Показатели роста: размер ~ t^a, число единиц ~ t^b, по отрезку 2^16..2^24."""
import glob, math, collections
res = []
for f in sorted(glob.glob('out/growth*.txt')):
    for line in open(f):
        p = line.split(); rule = int(p[0])
        v = [tuple(map(int, q.split(':'))) for q in p[1:]]  # k = 8..24
        s = {k + 8: v[k] for k in range(len(v))}
        if s[24][0] < 0:
            esc = min(k for k in s if s[k][0] < 0)
            res.append((rule, 'escaped', esc, None, None, s)); continue
        a = math.log2(s[24][0] / s[16][0]) / 8
        b = math.log2(max(s[24][1], 1) / max(s[16][1], 1)) / 8
        a2 = math.log2(s[24][0] / s[20][0]) / 4
        res.append((rule, 'ok', a, b, a2, s))
if __name__ == '__main__':
    bins = collections.Counter()
    for r in res:
        if r[1] == 'escaped': bins['escaped@2^%d' % r[2]] += 1
        else: bins['a=%.1f' % r[2]] += 1
    for k, v in sorted(bins.items()): print(k, v)
    with open('growth.csv', 'w') as f:
        f.write('rule,status,a_size,b_ones,a_size_late,size24,ones24\n')
        for r in res:
            s = r[5]
            if r[1] == 'escaped': f.write(f'{r[0]},escaped@{r[2]},,,,,\n')
            else: f.write(f'{r[0]},ok,{r[2]:.3f},{r[3]:.3f},{r[4]:.3f},{s[24][0]},{s[24][1]}\n')
