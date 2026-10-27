"""pryamougolnik.py R C [--nado a,b] [--max K] [--yazyki q] — словесные прямоугольники по Eldamo: R строк по C букв,
каждая строка — слово длины C, каждый столбец — слово длины R. Отбор слов — как в kvadrat.py (без имён, фраз,
аффиксов; диакритика снимается для сравнения; «†» — статья с <deprecated>).
27.10.2026: квадрата с «если» и «следовательно» из Q-слов не нашлось; прямоугольник даёт больше места
(например, cenai «if it be that» строкой и etta «therefore» столбцом)."""
import os
import re
import sys
import unicodedata

args = sys.argv[1:]
R, C = int(args[0]), int(args[1])
YAZ = args[args.index("--yazyki") + 1].split(",") if "--yazyki" in args else ["q"]
MAXK = int(args[args.index("--max") + 1]) if "--max" in args else 30
NADO = args[args.index("--nado") + 1].split(",") if "--nado" in args else []

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
xml = open(os.path.join(root, "inbox", "eldamo", "src", "data", "eldamo-data.xml"), encoding="utf-8").read()


def bare(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


words = {}
for m in re.finditer(r'<word ([^>]*)>', xml):
    a = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', m.group(1)))
    l, v = a.get("l"), a.get("v", "")
    sp = a.get("speech", "")
    if l not in YAZ or "name" in sp or "phrase" in sp or "-" in v or " " in v or not v:
        continue
    v2 = v.rstrip("¹²³⁴⁵")
    b = bare(v2)
    if not re.fullmatch(r"[a-z]+", b) or len(b) not in (R, C):
        continue
    tail = xml[m.end():m.end() + 3000]
    nxt = tail.find("<word ")
    dep = "<deprecated" in (tail if nxt < 0 else tail[:nxt])
    if b not in words or (words[b][3] and not dep):
        words[b] = (v2, a.get("gloss", ""), l, dep)

rows_w = sorted(w for w in words if len(w) == C)
cols_w = set(w for w in words if len(w) == R)
pref = set()
for w in cols_w:
    for k in range(R + 1):
        pref.add(w[:k])
print("строк-слов (%d букв): %d, столбцов-слов (%d букв): %d" % (C, len(rows_w), R, len(cols_w)), file=sys.stderr)

found = []


def rec(rows):
    if len(found) >= 50000:
        return
    if len(rows) == R:
        cols = ["".join(r[j] for r in rows) for j in range(C)]
        if all(c in cols_w for c in cols) and all(n in rows or n in cols for n in NADO):
            found.append((list(rows), cols))
        return
    for w in rows_w:
        if all("".join(r[j] for r in rows) + w[j] in pref for j in range(C)):
            rec(rows + [w])


rec([])


def show(w):
    o, g, l, d = words[w]
    return "%s%s «%s»" % (o, "†" if d else "", g)


found.sort(key=lambda fc: sum(words[w][3] for w in fc[0] + fc[1]))
print("прямоугольников: %d" % len(found))
for rows, cols in found[:MAXK]:
    print()
    for r in rows:
        print("   " + " ".join(r.upper()))
    print("   строки:  " + "; ".join(show(w) for w in rows))
    print("   столбцы: " + "; ".join(show(w) for w in cols))
