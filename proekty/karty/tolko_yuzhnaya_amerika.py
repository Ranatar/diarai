"""Копия world-110m.json, где в land и countries оставлены только многоугольники Южной Америки
(все точки в долготах −92…−30, широтах −57…14). Пишет ext/tmp/world-110m-sa.json. Для проверки шва у Бергхауса."""
import json
src = "/home/diarai/diarai/inbox/html-generated/maps/data/world-110m.json"
d = json.load(open(src))
sx, sy = d["transform"]["scale"]; tx, ty = d["transform"]["translate"]

def pts(i):
    a = d["arcs"][i if i >= 0 else ~i]
    x = y = 0
    for dx, dy in a:
        x += dx; y += dy
        yield x * sx + tx, y * sy + ty

def v_sa(poly):
    P = [p for ring in poly for i in ring for p in pts(i)]
    return all(-92 <= lo <= -30 and -57 <= la <= 14 for lo, la in P)

ostalos = 0
for name in ("land", "countries"):
    for g in d["objects"][name]["geometries"]:
        if g["type"] == "MultiPolygon":
            g["arcs"] = [p for p in g["arcs"] if v_sa(p)]
            ostalos += len(g["arcs"])
        elif g["type"] == "Polygon":
            if not v_sa(g["arcs"]):
                g["arcs"] = []
                g["type"] = "MultiPolygon"
            else:
                ostalos += 1
print("многоугольников осталось:", ostalos)
json.dump(d, open("/home/diarai/diarai/ext/tmp/world-110m-sa.json", "w"))
