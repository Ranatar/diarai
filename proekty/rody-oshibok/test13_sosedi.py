"""test13_sosedi.py — первые 160 знаков каждого § в окне ±5 вокруг номеров теста 13 (для вердикта «сосед»).
Запуск: python3 -I proekty/rody-oshibok/test13_sosedi.py  (источник — ext/pu/pu.json, как у pu.py)."""
import json, os
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
d = json.load(open(os.path.join(root, "ext", "pu", "pu.json"), encoding="utf-8"))
if isinstance(d, dict):
    get = lambda n: d.get(str(n)) or d.get(n)
else:
    m = {}
    for x in d:
        m[int(x.get("n", x.get("nr", 0)))] = x.get("text", x.get("t", ""))
    get = lambda n: m.get(n)
for c in [372, 418, 493, 512, 545]:
    print("==", c)
    for n in range(c - 5, c + 6):
        t = get(n)
        if isinstance(t, dict):
            t = t.get("text", "")
        print(" ", n, (t or "—").replace("\n", " ")[:160])
