"""test11_verdikty.py — пишет test11-verdikty.txt (по строке на место переписи) и сводит по жанру.
Вердикты выставлены чтением (test11_smotr.py); здесь — только исключения из «верно»."""
import sys
from collections import Counter

N = 111
V = ["верно|"] * N
V[4] = "верно|«со Христом распялся»: в синодальном делении — конец 2:19, в греческом и KJV — 2:20"
V[18] = "верно|стихи — те; но «отсутствует в древнейших манускриптах» неточно: есть везде, у части западных перенесены после 14:40 (по памяти)"
V[34] = "верно|«Царь царствующих»; отнесено к Сыну — толкование"
V[64] = "верно|лояльно: «испытание духов» — тема; сам призыв испытывать — 1 Ин 4:1"
V[102] = "верно|у синод. «первенец», в греч. ἀπαρχή — «начаток»"
for i in list(range(76, 94)) + [94, 95, 96]:
    V[i] = "дубль|html-копия md-файла, уже посчитана"
open("test11-verdikty.txt", "w", encoding="utf-8").write("\n".join(V) + "\n")

L = [l.rstrip("\n").split("\t") for l in open("test11-perepis.tsv", encoding="utf-8")]
assert len(L) - 1 == N
iv, iz = L[0].index("вердикт"), L[0].index("жанр")
for r, v in zip(L[1:], V):
    r[iv], r[iv + 1] = v.split("|", 1)
with open("test11-perepis.tsv", "w", encoding="utf-8") as f:
    for r in L:
        f.write("\t".join(r) + "\n")
print(sorted(Counter((r[iz], r[iv]) for r in L[1:]).items()))
