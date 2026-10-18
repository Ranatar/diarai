"""test7_izvlech.py — тест 7: в PS-3504 места, где рядом с номером «Лунь юй» стоят иероглифы. → test7-lunyu.tsv
Проверка — по первоисточнику (ctext.org), не по памяти: стоят ли эти иероглифы в параграфе с этим номером."""
import re, os
here = os.path.dirname(os.path.abspath(__file__))
t = open("/home/diarai/diarai/ext/tmp/ps3504.txt", encoding="utf-8").read()
rows, seen = [], set()
for m in re.finditer(r"«Лунь юй»,?\s*(\d{1,2}\.\d{1,2})", t):
    win = t[max(0, m.start() - 60): m.end() + 60]  # только иероглифы прямо при номере (250 захватывало соседей таблицы)
    for h in re.findall(r"[一-鿿]{2,}", win):
        key = (m.group(1), h)
        if key not in seen:
            seen.add(key); rows.append(key)
with open(os.path.join(here, "test7-lunyu.tsv"), "w", encoding="utf-8") as f:
    f.write("номер\tиероглифы\tвердикт\tисточник\n")
    for n, h in rows: f.write("%s\t%s\t\t\n" % (n, h))
for r in rows: print(*r)
