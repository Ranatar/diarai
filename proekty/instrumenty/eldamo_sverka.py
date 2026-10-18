"""Сверка эльфийских слов текста со словарём Eldamo автора.

python3 -I eldamo_sverka.py inbox/eldamo/src/data/eldamo-data.xml текст.txt [мин_частота]
Берёт из текста слова с эльфийскими диакритиками (áéíóúëäö…) и слова через дефис,
части через дефис проверяет по отдельности. Для каждого: есть ли в Eldamo
(язык, глосса), и если нет — ближайшие формы того же начала.
"""
import re, sys, unicodedata
from collections import Counter, defaultdict

xml, txt = sys.argv[1], sys.argv[2]
minf = int(sys.argv[3]) if len(sys.argv) > 3 else 1

LANG = {"q": "Q", "nq": "NQ", "mq": "MQ", "eq": "EQ", "s": "S", "ns": "NS", "n": "N", "en": "EN", "p": "P", "t": "T"}
lex = defaultdict(list)
for m in re.finditer(r'<word\b[^>]*?\bl="([a-z]+)"[^>]*?\bv="([^"]+)"[^>]*?>', open(xml, encoding="utf-8").read()):
    l, v = m.group(1), m.group(2)
    if l not in LANG:
        continue
    g = re.search(r'gloss="([^"]*)"', m.group(0))
    lex[v.lower()].append((LANG[l], g.group(1) if g else ""))


def strip(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


bare = defaultdict(list)
for k in lex:
    bare[strip(k)].append(k)

t = open(txt, encoding="utf-8").read()
terms = re.findall(r"\b[a-zA-Z]*[áéíóúëäöïâêîôû][a-zA-Z\-áéíóúëäöïâêîôû]*\b|\b[a-z]+-[a-záéíóúë]+\b", t)
cnt = Counter(x.lower() for x in terms)
parts = Counter()
for w, n in cnt.items():
    for p in w.split("-"):
        if len(p) >= 2:
            parts[p] += n

found, near, none = [], [], []
for p, n in sorted(parts.items(), key=lambda x: -x[1]):
    if n < minf:
        continue
    if p in lex:
        found.append((p, n, lex[p][:2]))
    elif strip(p) in bare:
        near.append((p, n, [(k, lex[k][0]) for k in bare[strip(p)][:3]]))
    else:
        pref = [k for k in lex if k.startswith(p[:4])][:4] if len(p) >= 4 else []
        none.append((p, n, [(k, lex[k][0][1][:30]) for k in pref]))

print(f"## Есть в Eldamo ({len(found)})")
for p, n, g in found:
    print(f"- {p} ×{n}: " + "; ".join(f"{l} «{gl}»" for l, gl in g))
print(f"\n## Есть, но с другими диакритиками ({len(near)})")
for p, n, k in near:
    print(f"- {p} ×{n}: в Eldamo " + "; ".join(f"{kk} ({l} «{gl}»)" for kk, (l, gl) in k))
print(f"\n## Нет в Eldamo ({len(none)})")
for p, n, k in none:
    print(f"- {p} ×{n}" + (": близкие " + ", ".join(f"{kk} «{g}»" for kk, g in k) if k else ""))
