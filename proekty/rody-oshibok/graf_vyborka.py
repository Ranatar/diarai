"""graf_vyborka.py — тест 4: 12 межсистемных связей philosophy_graph (исходник против правленого).
Зерно фиксировано (20261018), выбор до чтения описаний. Печатает пары описаний для разметки."""
import json, random, re
B = "/home/diarai/diarai/inbox/Synthesises-of-concepts/philosophy-graph-descriptions/"
data = json.load(open(B + "data.json", encoding="utf-8"))
phil = {c["id"]: c["philosopher"] for c in data["concepts"]}

def rels(path):
    t = open(path, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r'\{\s*source:\s*"([^"]+)",\s*target:\s*"([^"]+)",\s*type:\s*"([^"]+)"[^}]*?description:\s*"((?:[^"\\]|\\.)*)"', t):
        out[(m.group(1), m.group(2), m.group(3))] = m.group(4)
    return out

src = rels(B + "source/philosophy_graph.SOURCE.html")
dst = rels(B + "dist/philosophy_graph.html")
print("связей с описанием: исходник", len(src), "правленый", len(dst))
inter = [k for k in src if k in dst and phil.get(k[0]) and phil.get(k[1]) and phil[k[0]] != phil[k[1]]
         and k[2] in ("influence", "develop", "critique", "oppose", "dialogue", "synthesize")]
print("межсистемных исторических в обоих:", len(inter))
random.seed(20261018)
pick = random.sample(sorted(inter), 12)
for i, k in enumerate(pick, 1):
    print("\n#%d %s → %s [%s] (%s → %s)" % (i, k[0], k[1], k[2], phil[k[0]], phil[k[1]]))
    print("  ИСХ:", src[k])
    print("  ПРВ:", dst[k])
