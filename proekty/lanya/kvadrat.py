"""kvadrat.py N [--sim] [--yazyki q] [--max K] — словесные квадраты (ткань из слов) по Eldamo.

Строки — уток, столбцы — основа: каждая строка и каждый столбец квадрата N×N — слово квенья из Eldamo.
--sim: только симметричные (строка i = столбец i), иначе — любые («двойные»).
Слова: статьи <word l="..." v="..."> заданных языков (по умолчанию q), без имён (speech содержит name),
без фраз, аффиксов (дефис), с пробелами — тоже нет; диакритика снимается для сравнения букв
(á = a, ë = e), но печатается исходное написание. Статьи, внутри которых есть <deprecated .../>,
помечаются «†» (по схеме Eldamo это значит: устарела сама статья) — но не выбрасываются.
Печатает до K квадратов (по умолчанию 40) и их число.
27.10.2026 — к эссе proekty/esse/lanya.md (PU § 414: «пустой станок» — нужен настоящий сотканный текст)."""
import re, sys, os, unicodedata
from collections import defaultdict

args = sys.argv[1:]
N = int(args[0])
SIM = "--sim" in args
YAZ = args[args.index("--yazyki") + 1].split(",") if "--yazyki" in args else ["q"]
MAXK = int(args[args.index("--max") + 1]) if "--max" in args else 40
# --nado a,b — в квадрате (строки или столбцы) должны быть все эти слова (без диакритики)
NADO = args[args.index("--nado") + 1].split(",") if "--nado" in args else []

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
xml = open(os.path.join(root, "inbox", "eldamo", "src", "data", "eldamo-data.xml"), encoding="utf-8").read()


def bare(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


words = {}  # bare -> (orig, gloss, lang, deprecated)
for m in re.finditer(r'<word ([^>]*)>', xml):
    attrs = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', m.group(1)))
    l, v = attrs.get("l"), attrs.get("v", "")
    if l not in YAZ:
        continue
    sp = attrs.get("speech", "")
    if "name" in sp or "phrase" in sp or "-" in v or " " in v or not v:
        continue
    v2 = v.rstrip("¹²³⁴⁵")
    b = bare(v2)
    if not re.fullmatch(r"[a-z]+", b) or len(b) != N:
        continue
    # устарела ли статья: ищем <deprecated в её теле до следующего <word
    tail = xml[m.end():m.end() + 3000]
    nxt = tail.find("<word ")
    body = tail if nxt < 0 else tail[:nxt]
    dep = "<deprecated" in body
    gl = attrs.get("gloss", "")
    if b not in words or (words[b][3] and not dep):
        words[b] = (v2, gl, l, dep)

W = sorted(words)
pref = set()
for w in W:
    for k in range(N + 1):
        pref.add(w[:k])
print("слов длины %d (%s): %d" % (N, ",".join(YAZ), len(W)), file=sys.stderr)

found = []


def rec(rows):
    if len(found) >= 100000:
        return
    i = len(rows)
    if i == N:
        cols = ["".join(r[j] for r in rows) for j in range(N)]
        if all(c in words for c in cols) and all(n in rows or n in cols for n in NADO):
            found.append((list(rows), cols))
        return
    for w in W:
        if SIM:
            # строка i должна начинаться с уже известных букв столбца i
            if any(w[j] != rows[j][i] for j in range(i)):
                continue
        ok = True
        for j in range(N):
            if "".join(r[j] for r in rows) + w[j] not in pref:
                ok = False
                break
        if ok:
            rec(rows + [w])


rec([])


def show(w):
    o, g, l, d = words[w]
    return "%s%s «%s»" % (o, "†" if d else "", g)


# сначала квадраты без устаревших слов и с меньшим числом повторов
def score(fc):
    rows, cols = fc
    allw = rows + cols
    return (sum(words[w][3] for w in allw), len(allw) - len(set(allw)))


found.sort(key=score)
print("квадратов: %d" % len(found))
for rows, cols in found[:MAXK]:
    print()
    for r in rows:
        print("   " + " ".join(r.upper()))
    print("   строки:  " + "; ".join(show(w) for w in rows))
    if not SIM:
        print("   столбцы: " + "; ".join(show(w) for w in cols))
