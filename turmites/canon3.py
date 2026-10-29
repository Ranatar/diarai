"""Эквивалентность по ходу: два класса canon2 склеиваются, если их строки хода (traj 8 4008)
совпадают на окне длины 4000 при сдвигах 0..8. Это «одинаковый ход муравья», начиная с первых шагов."""
import collections
W = 4000
par = {}
def find(a):
    while par.setdefault(a, a) != a:
        par[a] = par[par[a]]; a = par[a]
    return a
seqs = {}
for l in open('out/traj.txt'):
    r, s = l.split(); seqs[int(r)] = s
by = collections.defaultdict(list)
for r, s in seqs.items():
    for o in range(9):
        by[s[o:o + W]].append(r)
for k, rs in by.items():
    for r in rs[1:]:
        a, b = find(rs[0]), find(r)
        if a != b: par[max(a, b)] = min(a, b)
CANON3 = {r: find(r) for r in seqs}
if __name__ == '__main__':
    groups = collections.defaultdict(list)
    for r, c in CANON3.items(): groups[c].append(r)
    print('классов canon2', len(seqs), '-> по ходу', len(groups))
    big = sorted(groups.values(), key=len, reverse=True)
    print('крупнейшие группы:', [len(g) for g in big[:15]])
    for g in big[:6]: print(sorted(g)[:10], seqs[min(g)][:30])
    print(CANON3.get(6953) == CANON3.get(41363))
