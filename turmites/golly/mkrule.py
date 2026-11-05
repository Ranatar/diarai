"""Правило Golly (@TABLE) для турмита 2×2 по моему коду: python3 mkrule.py RULE > T2_RULE.rule
Состояния: 0,1 — цвет без муравья; 2 + c + 2*s + 4*d — муравей на клетке цвета c в состоянии s, смотрит d (0=N 1=E 2=S 3=W).
Шаг Golly = шаг муравья: на клетке муравья — записанный цвет; в клетку, куда он уходит, — муравей."""
import sys
r = int(sys.argv[1])
E = [((r >> (4*e)) & 1, (r >> (4*e+1)) & 3, (r >> (4*e+3)) & 1) for e in range(4)]
OPP = [2, 3, 0, 1]
out = [f'@RULE T2_{r}', '', '@TABLE', 'n_states:18', 'neighborhood:vonNeumann', 'symmetries:none']
for i in range(4): out.append(f'var a{i}={{' + ','.join(map(str, range(18))) + '}')
for c in (0, 1):
    for s in (0, 1):
        for d in range(4):
            st = 2 + c + 2*s + 4*d
            w, tn, ns = E[2*s + c]
            # клетка муравья -> записанный цвет
            out.append(f'{st},a0,a1,a2,a3,{w}')
            nd = (d + tn) & 3
            # муравей уходит в соседа по nd; для того соседа муравей — с противоположной стороны OPP[nd]
            pos = OPP[nd]           # где стоит муравей относительно новой клетки (0=N 1=E 2=S 3=W)
            for k in (0, 1):
                nb = ['a0', 'a1', 'a2', 'a3']; nb[pos] = str(st)
                out.append(f'{k},' + ','.join(nb) + f',{2 + k + 2*ns + 4*nd}')
print('\n'.join(out))
