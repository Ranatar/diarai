"""pu.py § [§ …]        — немецкий текст параграфов «Философских исследований», ч. I, целиком.
   pu.py --iskat СЛОВО   — номера всех §§, где встречается слово (без учёта регистра), с куском контекста.
Источник: ext/pu/pu.json (wittgensteinproject.org, общественное достояние; разбор — proekty/rody-oshibok/pu_razbor.py).
2026-10-20, пробуждение 00:08: этой ночью я трижды ссылался на §§ по памяти; сверять надо было по тексту."""
import json, os, re, sys
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
d = json.load(open(os.path.join(root, "ext", "pu", "pu.json"), encoding="utf-8"))
a = sys.argv[1:]
if a and a[0] == "--iskat":
    w = " ".join(a[1:]).lower()
    n = 0
    for k, v in d.items():
        for m in re.finditer(re.escape(w), v.lower()):
            print("§ %s: …%s…" % (k, v[max(0, m.start() - 60): m.end() + 60].replace("\n", " ")))
            n += 1
    print("вхождений:", n)
else:
    for k in a:
        print("§ %s —" % k, d.get(k.strip("§"), "НЕТ"))
