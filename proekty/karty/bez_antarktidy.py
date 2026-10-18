import json
src = "/home/diarai/diarai/inbox/html-generated/maps/data/world-110m.json"
d = json.load(open(src))
sx, sy = d["transform"]["scale"]; tx, ty = d["transform"]["translate"]

def arc_lats(i):
    a = d["arcs"][i if i >= 0 else ~i]
    x = y = 0; out = []
    for dx, dy in a:
        x += dx; y += dy
        out.append(y * sy + ty)
    return out

def min_lat(poly):
    return min(min(arc_lats(i)) for ring in poly for i in ring)

for name in ("land", "countries"):
    for g in d["objects"][name]["geometries"]:
        if g["type"] == "MultiPolygon":
            before = len(g["arcs"])
            g["arcs"] = [p for p in g["arcs"] if min_lat(p) > -60]
            if len(g["arcs"]) != before:
                print(name, (g.get("properties") or {}).get("name"), "многоугольников:", before, "->", len(g["arcs"]))
        elif g["type"] == "Polygon" and min_lat(g["arcs"]) <= -60:
            print(name, (g.get("properties") or {}).get("name"), "Polygon убран")
            g["type"] = None; g.pop("arcs")
json.dump(d, open("/home/diarai/diarai/ext/tmp/world-110m-noant.json", "w"))
