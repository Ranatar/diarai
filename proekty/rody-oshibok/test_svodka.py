# Сводка предрегистрированного теста: доля верных по форме (А факт, Б счёт по странице, В отождествление, Г атрибуция).
import csv, sys, os
from collections import Counter
f = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "test1-razmetka.tsv")
rows = list(csv.DictReader(open(f, encoding="utf-8"), delimiter="\t"))
c = Counter((r["форма"], r["вердикт"]) for r in rows)
for k in "АБВГ":
    tot = sum(v for (ff, _), v in c.items() if ff == k)
    if tot:
        print("%s: всего %2d | верно %2d | неверно %2d | прочее %d" % (k, tot, c[(k, "верно")], c[(k, "неверно")], tot - c[(k, "верно")] - c[(k, "неверно")]))
