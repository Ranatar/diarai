"""nichya.py [--primer N] — где граница «десяти лиц» графа статьи HWPh приходится на ничью.

Читалка (ext/hwph-site/static_api.js:869-870) берёт в граф статьи десять лиц (не исследователей, не издателей)
по числу упоминаний капителью в тексте и примечаниях (r[2]+r[3]); при равенстве выше тот, у кого
больше статей во всём словаре (n_articles). Значит, на границе ничью выигрывает «канон».
Скрипт повторяет этот отбор по data/graph.js и data/persons.js и считает статьи, где 10-й и 11-й
кандидаты равны по счёту, и сколько лиц с тем же счётом осталось за бортом.
Третий, 19.10 (письмо автора: «в hwph есть графы, как в philosphaira»)."""
import json, sys, os, collections
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
D = os.path.join(ROOT, "ext", "hwph-site", "data")

def load(name):
    t = open(os.path.join(D, name), encoding="utf-8").read()
    i = t.index(",", t.index("HWPH.put(")) + 1
    return json.loads(t[i:t.rindex(")")])

g = load("graph.js")
P = {p[0]: p for p in load("persons.js")}   # [id, name, fold, n_articles, n_body, n_notes, n_lit, editor, role, at]
meta = None
by = collections.defaultdict(list)
for r in g["cites"]:
    by[r[0]].append(r)

ok = lambda r: r[1] in P and not P[r[1]][7] and P[r[1]][8] != "scholar" and r[2] + r[3] > 0
n_art = n_tie = n_out = 0
primery = []
for aid, rows in by.items():
    c = [r for r in rows if ok(r)]
    if len(c) <= 10:
        continue
    n_art += 1
    c.sort(key=lambda r: (-(r[2] + r[3]), -P[r[1]][3], r[1]))
    s10 = c[9][2] + c[9][3]
    if c[10][2] + c[10][3] == s10:
        n_tie += 1
        out = [r for r in c[10:] if r[2] + r[3] == s10]
        vin = [r for r in c[:10] if r[2] + r[3] == s10]
        n_out += len(out)
        primery.append((aid, s10, [(P[r[1]][1], P[r[1]][3]) for r in vin], [(P[r[1]][1], P[r[1]][3]) for r in out]))

print("статей, где кандидатов больше десяти:", n_art)
print("из них граница — ничья:", n_tie, "(%.0f%%)" % (100.0 * n_tie / max(n_art, 1)))
print("лиц с тем же счётом за бортом, всего:", n_out)
# насколько «канон» вытесняет: медиана n_articles у вошедших и выбывших при ничьей
vi = sorted(n for p in primery for _, n in p[2]); ou = sorted(n for p in primery for _, n in p[3])
if vi and ou:
    print("медиана статей словаря у вошедших по ничьей: %d, у выбывших: %d" % (vi[len(vi) // 2], ou[len(ou) // 2]))
if "--primer" in sys.argv:
    k = int(sys.argv[sys.argv.index("--primer") + 1])
    for p in primery:
        if p[0] == k:
            print(p)
