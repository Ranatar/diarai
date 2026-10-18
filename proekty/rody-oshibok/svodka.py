# Сводка reestr.tsv: по родам — сколько верно и неверно; и по способу проверки.
import csv, os
from collections import Counter
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reestr.tsv")
rows = list(csv.DictReader(open(p, encoding="utf-8"), delimiter="\t"))
by = Counter((r["род"], r["вердикт"]) for r in rows)
for k in ["1", "2", "3", "4", "шов"]:
    v, n = by[(k, "верно")], by[(k, "неверно")]
    print("род %-4s верно %2d  неверно %2d" % (k, v, n))
print("всего строк:", len(rows))
m = Counter((r["как проверено"], r["вердикт"]) for r in rows)
for k in sorted({r["как проверено"] for r in rows}):
    print("%-8s верно %2d  неверно %2d" % (k, m[(k, "верно")], m[(k, "неверно")]))
