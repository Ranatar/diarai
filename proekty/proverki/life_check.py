# Проверка фигур «Цветной Игры „Жизнь“» (game-life-color-imp.html) по правилу B3/S23 на бесконечной плоскости.
# Фигуры извлечены из кода страницы в life_patterns.json (без изменений).
import json, os, sys
from collections import Counter

here = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(here, "life_patterns.json")))

def cells(rows):
    return frozenset((x, y) for y, r in enumerate(rows) for x, v in enumerate(r) if v)

def step(s):
    c = Counter((x + dx, y + dy) for x, y in s for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy)
    return frozenset(p for p, n in c.items() if n == 3 or (n == 2 and p in s))

def norm(s):
    if not s:
        return (frozenset(), (0, 0))
    mx, my = min(x for x, _ in s), min(y for _, y in s)
    return frozenset((x - mx, y - my) for x, y in s), (mx, my)

def period(s, limit=200):
    """Возвращает (период, сдвиг) первого возврата формы (с точностью до сдвига) или None."""
    f0, o0 = norm(s)
    cur = s
    for g in range(1, limit + 1):
        cur = step(cur)
        f, o = norm(cur)
        if f == f0:
            return g, (o[0] - o0[0], o[1] - o0[1])
    return None

def lifespan(s, limit):
    """Поколение, после которого популяция больше не меняется в окне 60 поколений (грубо: стабилизация), и популяция."""
    hist = []
    cur = s
    for g in range(limit + 1):
        hist.append(len(cur))
        if not cur:
            return g, 0
        cur = step(cur)
    return None, len(cur)

which = sys.argv[1:] or ["osc", "ships", "still", "guns", "meth"]
if "osc" in which or "still" in which or "ships" in which:
    for name in ["blinker", "toad", "beacon", "clock", "pulsar", "pentadecathlon", "block", "beehive", "loaf", "boat", "tub", "pond", "glider", "lwss", "mwss", "hwss", "loafer"]:
        print("%-15s %s" % (name, period(cells(P[name]))))
if "guns" in which:
    for name, n in (("gliderGun", 300), ("simkinGliderGun", 600)):
        s = cells(P[name])
        pops = []
        cur = s
        for g in range(n):
            pops.append(len(cur))
            cur = step(cur)
        # период ружья: популяция растёт скачками; печатаем популяцию через каждые 30 / 120
        print(name, "популяция в 0, 30, 60, …:", pops[0:n:30][:10], "в 0,120,240,…:", pops[0:n:120])
if "meth" in which:
    s = cells(P["diehard"])
    print("diehard: исчезает в поколении", lifespan(s, 200))
    for name, gen in (("rpentomino", 1103), ("acorn", 5206)):
        cur = cells(P[name])
        for g in range(gen):
            cur = step(cur)
        print(name, "популяция в поколении", gen, "=", len(cur))
