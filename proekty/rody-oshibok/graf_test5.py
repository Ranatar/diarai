"""graf_test5.py — тест 5: межсистемные исторические связи philosophy_graph, правленая версия.
Группа А — описание переписано целиком (последнее предложение исходника не сохранилось в правленом);
группа Б — заменён только зачин (последнее предложение исходника сохранилось дословно).
По 10 из каждой, зерно 5. Печатает только правленые описания (их и проверяю)."""
import random, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
B = "/home/diarai/diarai/inbox/Synthesises-of-concepts/philosophy-graph-descriptions/"
import json
data = json.load(open(B + "data.json", encoding="utf-8"))
phil = {c["id"]: c["philosopher"] for c in data["concepts"]}

def rels(path):
    t = open(path, encoding="utf-8").read()
    return {(m.group(1), m.group(2), m.group(3)): m.group(4) for m in re.finditer(
        r'\{\s*source:\s*"([^"]+)",\s*target:\s*"([^"]+)",\s*type:\s*"([^"]+)"[^}]*?description:\s*"((?:[^"\\]|\\.)*)"', t)}

src, dst = rels(B + "source/philosophy_graph.SOURCE.html"), rels(B + "dist/philosophy_graph.html")
inter = sorted(k for k in src if k in dst and phil.get(k[0]) and phil.get(k[1]) and phil[k[0]] != phil[k[1]]
               and k[2] in ("influence", "develop", "critique", "oppose", "dialogue", "synthesize"))
def last_sentence(s):
    parts = re.split(r"(?<=[.!?])\s+", s.strip())
    return parts[-1] if parts else s
A = [k for k in inter if last_sentence(src[k]) not in dst[k]]
Bg = [k for k in inter if last_sentence(src[k]) in dst[k]]
print("всего", len(inter), "| А (переписано целиком):", len(A), "| Б (только зачин):", len(Bg))
random.seed(5)
for name, g in (("А", A), ("Б", Bg)):
    for i, k in enumerate(random.sample(g, 10), 1):
        print("\n%s%d %s → %s [%s] (%s → %s)\n  %s" % (name, i, k[0], k[1], k[2], phil[k[0]], phil[k[1]], dst[k]))
