"""patriarchs_chain.py [путь к patriarchs.html] — проверка «цепочки свидетелей» на inbox/patriarchs.html.

Повторяет на Python функции страницы compute(), link() и findChain() (строки ~213–224 и 378–401).
Для каждой редакции, каждой пары (от, к) и каждого порога возраста (0, 10, 20, 40) берёт цепочку,
которую нашла бы страница, и проверяет, исполнима ли она во времени. Каждый следующий должен услышать
от предыдущего не раньше, чем предыдущий сам услышал: t1 <= t2 <= … при ti внутри окна звена i.
Печатает число цепочек, число неисполнимых и до 10 примеров.
Также ищет, есть ли для неисполнимых пар исполнимая цепочка той же длины (перебором по слоям).
2026-10-20, пробуждение 18:20. Чужой код не запускается: данные PEOPLE читаются регулярными выражениями."""
import re, sys, itertools

path = sys.argv[1] if len(sys.argv) > 1 else "inbox/patriarchs.html"
src = open(path, encoding="utf-8").read()
block = src[src.index("const PEOPLE = ["):src.index("];", src.index("const PEOPLE = ["))]

def triple(s):
    d = {}
    for k, v in re.findall(r'(mt|sp|lxx):(null|\d+)', s):
        d[k] = None if v == "null" else int(v)
    return d

people = []
for line in block.split("\n"):
    m = re.search(r'\{id:"([^"]+)",name:"([^"]+)"', line)
    if not m:
        continue
    pid, name = m.group(1), m.group(2)
    fm = re.search(r'[{,]f:(\{[^}]*\}|"[^"]*")', line)   # не путать с ref:"…"
    if fm is None:
        f = None
    elif fm.group(1).startswith("{"):
        f = dict(re.findall(r'(mt|sp|lxx):"([^"]+)"', fm.group(1)))
    else:
        f = fm.group(1).strip('"')
    age = triple(re.search(r'age:\{([^}]*)\}', line).group(1))
    life = triple(re.search(r'life:\{([^}]*)\}', line).group(1))
    people.append(dict(id=pid, name=name, f=f, age=age, life=life))

def compute(v):
    m = {}
    out = []
    for p in people:
        if p["life"].get(v) is None:
            continue
        fid = p["f"].get(v) if isinstance(p["f"], dict) else p["f"]
        a = p["age"][v]
        born = m[fid]["born"] + a if fid else 0
        r = dict(id=p["id"], name=p["name"], born=born, death=born + p["life"][v])
        m[p["id"]] = r
        out.append(r)
    return out, m

def window(a, b, minAge):
    y = b if a["born"] <= b["born"] else a
    lo = max(a["born"], b["born"], y["born"] + minAge)
    hi = min(a["death"], b["death"])
    return lo, hi

def link(a, b, minAge):
    lo, hi = window(a, b, minAge)
    return max(0, hi - lo)

def find_chain(L, m, frm, to, minAge):
    if frm == to:
        return [frm]
    dist, best, prev = {frm: 0}, {frm: float("inf")}, {}
    layer = [m[frm]]
    while layer and to not in dist:
        nxt = {}
        for u in layer:
            for w in L:
                if w["id"] in dist and dist[w["id"]] <= dist[u["id"]]:
                    continue
                o = link(u, w, minAge)
                if not o:
                    continue
                bn = min(best[u["id"]], o)
                if w["id"] not in dist or bn > best[w["id"]]:
                    dist[w["id"]] = dist[u["id"]] + 1
                    best[w["id"]] = bn
                    prev[w["id"]] = u["id"]
                    nxt[w["id"]] = w
        layer = list(nxt.values())
    if to not in dist:
        return None
    p, c = [], to
    while c is not None:
        p.insert(0, c)
        c = prev.get(c)
    return p

def feasible(chain, m, minAge):
    t = float("-inf")
    for a, b in zip(chain, chain[1:]):
        lo, hi = window(m[a], m[b], minAge)
        t = max(t, lo)
        if t >= hi:          # окно открытое: link() требует hi - lo > 0
            return False
    return True

def any_feasible_same_len(L, m, frm, to, k, minAge):
    ids = [x["id"] for x in L if x["id"] not in (frm, to)]
    for mid in itertools.permutations(ids, k - 1):
        ch = [frm, *mid, to]
        if all(link(m[a], m[b], minAge) for a, b in zip(ch, ch[1:])) and feasible(ch, m, minAge):
            return ch
    return None

for v in ("mt", "sp", "lxx"):
    L, m = compute(v)
    total = bad = 0
    ex = []
    for a, b in itertools.permutations([x["id"] for x in L], 2):
        if m[a]["born"] > m[b]["born"]:
            continue   # только от старшего к младшему: кто от кого мог услышать
        for minAge in (0, 10, 20, 40):
            ch = find_chain(L, m, a, b, minAge)
            if not ch:
                continue
            total += 1
            if not feasible(ch, m, minAge):
                bad += 1
                if len(ex) < 10:
                    alt = any_feasible_same_len(L, m, a, b, len(ch) - 1, minAge) if len(ch) <= 5 else "не искал"
                    ex.append((minAge, [m[c]["name"] for c in ch], alt and ([m[c]["name"] for c in alt] if isinstance(alt, list) else alt)))
    print(f"{v}: цепочек {total}, неисполнимых во времени {bad}")
    for e in ex:
        print("   порог", e[0], " → ".join(e[1]), "| исполнимая той же длины:", " → ".join(e[2]) if isinstance(e[2], list) else e[2])

# сверка переноса со страницей: Адам → Авраам, порог 10 (на снимке страницы: МТ — Мафусал → Сим;
# СП — Ной → Евер → Рагав → Серух → Фарра; LXX — Каинан → Мафусал → Сим → Евер → Серух)
for v in ("mt", "sp", "lxx"):
    L, m = compute(v)
    print("сверка", v, " → ".join(m[c]["name"] for c in find_chain(L, m, "adam", "abraham", 10)))
