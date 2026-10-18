"""test8_itog.py — внести вердикты (test8-verdikty.txt, по строке на место выборки) в test8-vyborka.tsv и свести.
Источник места: «генератор» (html-generated, Synthesises), «ФилоСфера» (philosphaira, сверено по тексту), «HWPh» (hwph-xml)."""
import sys
from collections import Counter

V = [l.rstrip("\n").split("|", 1) for l in open("test8-verdikty.txt", encoding="utf-8") if l.strip()]
L = [l.rstrip("\n").split("\t") for l in open("test8-vyborka.tsv", encoding="utf-8")]
assert len(L) - 1 == len(V), (len(L), len(V))
for r, (a, b) in zip(L[1:], V):
    r[4], r[5] = a, b
with open("test8-vyborka.tsv", "w", encoding="utf-8") as f:
    for r in L:
        f.write("\t".join(r) + "\n")

def ist(path):
    if path.startswith("philosphaira"): return "ФилоСфера"
    if path.startswith("hwph-xml"): return "HWPh"
    return "генератор"

print("по знаменитости:", sorted(Counter((("знам" if r[3] == "1" else "незн"), r[4]) for r in L[1:]).items()))
print("по источнику:   ", sorted(Counter((ist(r[1]), r[4]) for r in L[1:]).items()))
