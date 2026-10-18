"""Готовая правка слов вперемешку кириллица/латиница: таблица замен, inbox не трогается.

python3 -I smesh_fix.py корень файл1 [файл2 …] > замены.tsv
Строки таблицы: файл <TAB> было <TAB> стало <TAB> сколько раз. Что чинить нельзя без человека,
печатается в stderr с пометкой «вручную».

Правило. Двойники — буквы, одинаковые на вид (a c e o p x y A B C E H K M O P T X и их
кириллические пары; кириллическая ё в латинском слове — это ë квенья). Если буквы одной
письменности в слове все двойники, а у другой есть хоть одна без двойника — переводим первые
во вторую. Если двойники обе, переводим меньшинство. Иначе — вручную (склейки вроде «напримерAlso»).
"""
import os, re, sys
from collections import Counter

LAT2CYR = dict(zip("aceopxyABCEHKMOPTX", "асеорхуАВСЕНКМОРТХ"))
CYR2LAT = {v: k for k, v in LAT2CYR.items()}
CYR2LAT["ё"] = "ë"
# кириллическую «р» в латинском слове набирают по звуку, а не по виду: «раsura» = rasura, «реserved» = reserved
CYR2LAT["р"], CYR2LAT["Р"] = "r", "R"
MIX = re.compile(r"\b(?=[^\W\d_]*[а-яёА-ЯЁ])(?=[^\W\d_]*[a-zA-Z])[^\W\d_]+\b")


def is_lat(ch):
    return "a" <= ch.lower() <= "z"


def fix_word(w):
    lat = [ch for ch in w if is_lat(ch)]
    cyr = [ch for ch in w if not is_lat(ch) and ch.isalpha() and ("а" <= ch.lower() <= "я" or ch in "ёЁ")]
    lat_twins = all(ch in LAT2CYR for ch in lat)
    cyr_twins = all(ch in CYR2LAT for ch in cyr)
    to_cyr = lambda: "".join(LAT2CYR.get(ch, ch) for ch in w)
    to_lat = lambda: "".join(CYR2LAT.get(ch, ch) if not is_lat(ch) else ch for ch in w)
    if lat_twins and not cyr_twins:
        return to_cyr()
    if cyr_twins and not lat_twins:
        return to_lat()
    if lat_twins and cyr_twins:
        return to_cyr() if len(cyr) >= len(lat) else to_lat()
    return None


root = sys.argv[1]
for rel in sys.argv[2:]:
    t = open(os.path.join(root, rel), encoding="utf-8").read()
    reps, manual = Counter(), Counter()
    for m in MIX.finditer(t):
        w = m.group(0)
        f = fix_word(w)
        if f is None:
            manual[w] += 1
        else:
            reps[(w, f)] += 1
    for (w, f), n in sorted(reps.items()):
        print(f"{rel}\t{w}\t{f}\t{n}")
    for w, n in sorted(manual.items()):
        print(f"вручную: {rel}: {w} ×{n}", file=sys.stderr)
