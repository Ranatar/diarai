"""zagustit.py вход.json выход.json [шаг_в_градусах] — сгустить дуги TopoJSON: между соседними точками дуги
вставить промежуточные (линейно по долготе/широте), чтобы ни один отрезок не был длиннее шага (по умолчанию 0,5°).
Зачем: проверить, рисует ли движок глобуса автора отрезок данных прямой хордой без адаптивной передискретизации
(гипотеза о «клине» у звезды Бергхауса, 2026-10-19). Квантованные дуги остаются квантованными (дельты — целые)."""
import json, sys, math
src, dst = sys.argv[1], sys.argv[2]
step = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
d = json.load(open(src))
sx, sy = d["transform"]["scale"]
n_old = n_new = 0
arcs = []
for a in d["arcs"]:
    x = y = 0
    absq = []
    for dx, dy in a:
        x += dx; y += dy
        absq.append((x, y))
    out = [absq[0]]
    for (x0, y0), (x1, y1) in zip(absq, absq[1:]):
        dist = math.hypot((x1 - x0) * sx, (y1 - y0) * sy)
        k = max(1, math.ceil(dist / step))
        for i in range(1, k + 1):
            out.append((round(x0 + (x1 - x0) * i / k), round(y0 + (y1 - y0) * i / k)))
    # обратно в дельты, выбрасывая нулевые шаги
    deltas = [list(out[0])]
    px, py = out[0]
    for (qx, qy) in out[1:]:
        if (qx, qy) != (px, py):
            deltas.append([qx - px, qy - py]); px, py = qx, qy
    n_old += len(a); n_new += len(deltas)
    arcs.append(deltas)
d["arcs"] = arcs
json.dump(d, open(dst, "w"))
print("точек было", n_old, "стало", n_new)
