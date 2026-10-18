"""test8_itog.py — внести вердикты (test8-verdikty.txt, по строке на место выборки) в test8-vyborka.tsv и свести.
Источник места: «генератор» (html-generated, Synthesises), «ФилоСфера» (philosphaira, сверено по тексту), «HWPh» (hwph-xml)."""
import sys
from collections import Counter

VF = sys.argv[1] if len(sys.argv) > 1 else "test8-verdikty.txt"   # тест 9: test9-verdikty.txt test9-perepis.tsv
TF = sys.argv[2] if len(sys.argv) > 2 else "test8-vyborka.tsv"
V = [l.rstrip("\n").split("|", 1) for l in open(VF, encoding="utf-8") if l.strip()]
L = [l.rstrip("\n").split("\t") for l in open(TF, encoding="utf-8")]
assert len(L) - 1 == len(V), (len(L), len(V))
# столбцы вердикта ищем по заголовку: в test10-perepis.tsv перед ними стоит контекст
# (2026-10-18: первая версия писала в 4 и 5 и затёрла контекст теста 10; восстановлено из git)
iv = L[0].index("вердикт")
for r, (a, b) in zip(L[1:], V):
    r[iv], r[iv + 1] = a, b
with open(TF, "w", encoding="utf-8") as f:
    for r in L:
        f.write("\t".join(r) + "\n")

def ist(path):
    if path.startswith("philosphaira"): return "ФилоСфера"
    if path.startswith("hwph-xml"): return "HWPh"
    return "генератор"

print("по знаменитости:", sorted(Counter((("знам" if r[3] == "1" else "незн"), r[iv]) for r in L[1:]).items()))
print("по источнику:   ", sorted(Counter((ist(r[1]), r[iv]) for r in L[1:]).items()))
