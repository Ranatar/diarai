"""put.py ОТ ДО — кратчайший путь в графе ΦilosΦaira, как в приложении (inbox/philosphaira/app/modules/paths/).
Два режима: невзвешенный (BFS) и взвешенный (Дейкстра, стоимость ребра 4 − weight, как в shortest-path.js).
Хронология — режим «без разрывов» (chronology.js: stepWithoutGap): годы рождения философов
вдоль пути не идут назад; внутри одного философа ход свободен; рёбра проходимы в обе стороны.
Типологические связи (typological, typological_opposition) — с ними и без них (настройка skipTypologicalInPaths).
ОТ и ДО — id понятий (например harmony_spheres rhizome)."""
import heapq, json, os, sys, collections

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "inbox", "philosphaira", "app", "data")
C = {c["id"]: c for c in json.load(open(os.path.join(D, "concepts.json"), encoding="utf-8"))}
P = {p["id"]: p for p in json.load(open(os.path.join(D, "philosophers.json"), encoding="utf-8"))}
R = json.load(open(os.path.join(D, "relations.json"), encoding="utf-8"))
TYPO = {"typological", "typological_opposition"}


def birth(cid):
    p = P.get(C[cid].get("philosopher"))
    for k in ("birth", "born", "birthYear"):
        if p and isinstance(p.get(k), (int, float)):
            return p[k]
    return None


def ok_step(a, b, last, step):
    if C[a].get("philosopher") == C[b].get("philosopher"):
        return True
    y = birth(b)
    if y is None or last is None:
        return True
    return y >= last if step > 0 else y <= last


def graph(skip_typo):
    g = collections.defaultdict(list)
    for r in R:
        s, t = r["source"], r["target"]
        if s == t or (skip_typo and r["type"] in TYPO):
            continue
        cost = 4 - (r.get("weight") or 2)
        g[s].append((t, cost, r["type"]))
        g[t].append((s, cost, r["type"]))
    return g


def search(a, b, g, weighted):
    ya, yb = birth(a), birth(b)
    step = -1 if (ya is not None and yb is not None and yb < ya) else 1
    dist, prev, heap, done = {a: 0}, {a: None}, [(0, a)], set()
    while heap:
        d, x = heapq.heappop(heap)
        if x in done:
            continue
        done.add(x)
        if x == b:
            break
        last = birth(x)
        for y, cost, _ in g[x]:
            if y in done or not ok_step(x, y, last, step):
                continue
            nd = d + (cost if weighted else 1)
            if nd < dist.get(y, 1e9):
                dist[y], prev[y] = nd, x
                heapq.heappush(heap, (nd, y))
    if b not in prev:
        return None, None
    path, x = [], b
    while x:
        path.append(x)
        x = prev[x]
    return path[::-1], dist[b]


def name(cid):
    p = P.get(C[cid].get("philosopher"), {})
    return "%s (%s)" % (C[cid]["label"], p.get("name", "?"))


a, b = sys.argv[1], sys.argv[2]
for skip in (False, True):
    g = graph(skip)
    for weighted in (False, True):
        path, d = search(a, b, g, weighted)
        tag = ("взвеш." if weighted else "невзв.") + (", без типологических" if skip else ", все связи")
        if path is None:
            print(tag, ": пути нет")
        else:
            print("%s: %d шагов, стоимость %s\n   %s" % (tag, len(path) - 1, d, " → ".join(name(x) for x in path)))
