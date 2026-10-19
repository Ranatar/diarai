"""sosedi.py [--k 12] [--filosof locke] — совпадают ли соседи философа в двух графах.

ΦilosΦaira: соседи философа X — философы, чьи концепции связаны (relations.json, любой тип)
с концепциями X; вес — число таких связей.
HWPh (читалка): соседи — лица, ближайшие по социтированию, как в cocited() из
ext/hwph-site/static_api.js:776: общие статьи (упоминание в тексте или примечаниях),
не меньше 2, балл = shared / sqrt(статей у X * статей у Y).
Сравниваются только соседи из числа 100 философов ΦilosΦaira (через
inbox/hwph-xml/bridge_out/philosophers_hwph.json; несколько лиц HWPh на философа сливаются).
Печатает для каждого: |пересечение верхних k| и ожидание при случайном выборе (k*k/99).
Третий, 19.10 (письмо автора: «в hwph есть графы, как в philosphaira»)."""
import json, os, sys, math, collections
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
D = os.path.join(ROOT, "ext", "hwph-site", "data")
def load(name):
    t = open(os.path.join(D, name), encoding="utf-8").read()
    return json.loads(t[t.index(",", t.index("HWPH.put(")) + 1:t.rindex(")")])
args = sys.argv[1:]
k = int(args[args.index("--k") + 1]) if "--k" in args else 12
odin = args[args.index("--filosof") + 1] if "--filosof" in args else None

ph = json.load(open(os.path.join(ROOT, "inbox/hwph-xml/bridge_out/philosophers_hwph.json"), encoding="utf-8"))
conc = json.load(open(os.path.join(ROOT, "inbox/philosphaira/app/data/concepts.json"), encoding="utf-8"))
rel = json.load(open(os.path.join(ROOT, "inbox/philosphaira/app/data/relations.json"), encoding="utf-8"))
kto = {c["id"]: c["philosopher"] for c in conc}

# граф ΦilosΦaira на уровне философов
F = collections.defaultdict(collections.Counter)
for r in rel:
    a, b = kto.get(r["source"]), kto.get(r["target"])
    if a and b and a != b:
        F[a][b] += 1; F[b][a] += 1

# HWPh: статьи каждого философа (слияние его лиц)
g = load("graph.js")
P = {p[0]: p for p in load("persons.js")}
lica = {f: set(v.get("hwph_persons") or []) for f, v in ph.items()}
art = collections.defaultdict(set)
pid2f = {}
for f, s in lica.items():
    for p in s: pid2f[p] = f
for r in g["cites"]:
    if r[2] + r[3] > 0 and r[1] in pid2f:
        art[pid2f[r[1]]].add(r[0])
H = {}
for f in ph:
    if not art[f]: continue
    sc = {}
    for o in ph:
        if o == f or not art[o]: continue
        sh = len(art[f] & art[o])
        if sh >= 2:
            sc[o] = sh / math.sqrt(len(art[f]) * len(art[o]))
    H[f] = sc

def top(c, n): return [x for x, _ in sorted(c.items(), key=lambda t: (-t[1], t[0]))[:n]]
rows = []
for f in sorted(ph):
    if f not in H or not F[f]: continue
    a, b = top(F[f], k), top(H[f], k)
    n = min(len(a), len(b))
    rows.append((f, len(set(a) & set(b)), n, a, b))
ozh = k * k / 99.0
sr = sum(r[1] for r in rows) / len(rows)
print("философов: %d; верхние %d; среднее пересечение %.2f; при случайном выборе ≈ %.2f" % (len(rows), k, sr, ozh))
# честнее (19.10): у ΦilosΦaira веса мелкие, и верхние k режут ничью по алфавиту (та же болезнь, что в nichya.py).
# Поэтому: ВСЕ соседи ΦilosΦaira против верхних k HWPh; ожидание = k * |соседей Ф| / 99.
nab = ozh_s = 0; m = 0
for f in sorted(ph):
    if f not in H or len(H[f]) < k or not F[f]: continue
    vse = set(F[f]); b = set(top(H[f], k))
    nab += len(vse & b); ozh_s += k * len(vse) / 99.0; m += 1
print("все соседи Ф против верхних %d HWPh (%d философов): совпало %d, при случайном ≈ %.0f, отношение %.2f" % (k, m, nab, ozh_s, nab / ozh_s))
polnye = [r for r in rows if r[2] >= k]
print("из них с полной дюжиной соседей в обоих графах: %d; среднее пересечение %.2f" % (len(polnye), sum(r[1] for r in polnye) / len(polnye)))
print("неполные (мало данных HWPh):", [(r[0], r[2]) for r in rows if r[2] < k])
rows = polnye
rows.sort(key=lambda r: r[1])
print("меньше всего общих:", [(r[0], r[1]) for r in rows[:8]])
print("больше всего общих:", [(r[0], r[1]) for r in rows[-8:]])
if odin:
    for r in rows:
        if r[0] == odin:
            print("ΦilosΦaira:", r[3]); print("HWPh:      ", r[4]); print("общие:", sorted(set(r[3]) & set(r[4])))
