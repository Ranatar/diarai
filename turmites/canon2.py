"""Уточнённая канонизация: кроме зеркала и недостижимых входов,
правило, у которого вход (s0,c0) пишет 0 и ведёт в состояние 1, отождествляется
с правилом с переставленными состояниями (после первого шага муравей стоит на пустом поле в состоянии 1).
Классы замыкаются объединением множеств; канон2 = наименьший канон в классе."""
from analyze import entries, pack, canon

def swap(rule):
    e = entries(rule)
    return pack([(w, t, 1 - n) for w, t, n in (e[2], e[3], e[0], e[1])])

_par = {}
def _find(a):
    while _par.setdefault(a, a) != a:
        _par[a] = _par[_par[a]]; a = _par[a]
    return a

def build():
    for r in range(65536):
        a = _find(canon(r)[0])
        w, t, n = entries(r)[0]
        if w == 0 and n == 1:
            b = _find(canon(swap(r))[0])
            if a != b: _par[max(a, b)] = min(a, b)
    return {r: _find(canon(r)[0]) for r in range(65536)}

CANON2 = build()

if __name__ == '__main__':
    cls = {canon(r)[0] for r in range(65536)}
    print('классов было', len(cls), 'стало', len(set(CANON2.values())))
    for a, b in [(37306, 12825), (38312, 8221), (2942, 45703), (6953, 41363)]:
        print(a, b, CANON2[a] == CANON2[b])
