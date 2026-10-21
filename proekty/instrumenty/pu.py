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
    import glob
    # 21.10: § 127 и § 133 я «открывал» трижды (19.10, 20.10 дважды, 21.10) с одними и теми же мыслями.
    # Теперь после текста — где этот § уже был в моих дневниках и заметках (только число и файлы, без пересказа).
    mine = sorted(glob.glob(os.path.join(root, "diary", "*.md")) + glob.glob(os.path.join(root, "notes", "*.md"))
                  + glob.glob(os.path.join(root, "proekty", "**", "*.md"), recursive=True))
    for k in a:
        k = k.strip("§")
        print("§ %s —" % k, d.get(k, "НЕТ"))
        rx = re.compile(r"§\s*%s(?![\d.])" % re.escape(k))
        gde = []
        for f in mine:
            try:
                c = len(rx.findall(open(f, encoding="utf-8", errors="replace").read()))
            except OSError:
                continue
            if c:
                gde.append("%s (%d)" % (os.path.relpath(f, root), c))
        print("   [у меня уже: %s]" % ("; ".join(gde) if gde else "нигде"))
