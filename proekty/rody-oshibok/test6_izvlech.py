"""test6_izvlech.py — тест 6: все пары «Имя (ГГГГ–ГГГГ)» из inbox/gnostic-treatise-part1..8.md → test6-daty.tsv.
Проверка — машиной по Wikidata (test6_sverka.py), не памятью. Предсказание (до сверки): даты держатся (≥ 90 %)."""
import re, glob, os
here = os.path.dirname(os.path.abspath(__file__))
rx = re.compile(r"((?:[А-ЯЁ][а-яё\-]+ (?:(?:фон|де|ван|да|ди|ибн) )?){0,3}[А-ЯЁ][а-яё\-]+) ?\((?:ок\. ?|около ?|ca?\. ?)?(\d{3,4}) ?[-–—] ?(?:ок\. ?)?(\d{2,4})\)")
STOP = {"Хронологически", "Эволюция", "Света", "Нового", "Завета"}
rows, seen = [], set()
for p in sorted(glob.glob("/home/diarai/diarai/inbox/gnostic-treatise-part*.md")):
    t = open(p, encoding="utf-8").read()
    for m in rx.finditer(t):
        name, b, d = m.group(1).strip(), m.group(2), m.group(3)
        name = " ".join(w for w in name.split() if w not in STOP)
        if len(d) == 2: d = b[:2] + d
        key = (name, b, d)
        if key in seen: continue
        seen.add(key)
        rows.append((os.path.basename(p).replace("gnostic-treatise-", "").replace(".md", ""), name, b, d))
with open(os.path.join(here, "test6-daty.tsv"), "w", encoding="utf-8") as f:
    f.write("часть\tимя\tрожд\tсмерть\tвердикт\tWikidata\n")
    for r in rows:
        f.write("\t".join(r) + "\t\t\n")
print(len(rows))
for r in rows[:80]:
    print("\t".join(r))
