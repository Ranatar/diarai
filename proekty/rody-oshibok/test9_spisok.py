"""test9_spisok.py — перепись для теста 9: все места из test8-mesta.tsv, написанные генератором
(не philosphaira, не hwph-xml, не wittgenstein-hesychasm — там вымышленный трактат с настоящими номерами),
где номер стоит точечно, а не концом диапазона («§2.1–2.225»). Печатает TSV для разметки."""
import re

rows = [l.rstrip("\n").split("\t") for l in open("test8-mesta.tsv", encoding="utf-8")][1:]
print("id\tфайл\tномер\tзнам\tвердикт\tкомментарий")
for i, (f, n, z, ctx) in enumerate(rows):
    if f.startswith(("philosphaira", "hwph-xml")) or "wittgenstein-hesychasm" in f:
        continue
    k = ctx.find(n, 140)  # номер стоит около позиции 160
    before, after = ctx[max(0, k - 2):k], ctx[k + len(n):k + len(n) + 2]
    if re.search(r"[–\-—]", before) or re.search(r"^\s?[–\-—]", after):
        continue
    print("%d\t%s\t%s\t%s\t\t" % (i, f, n, z))
