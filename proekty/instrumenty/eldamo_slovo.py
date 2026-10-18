"""eldamo_slovo.py слово [язык] — найти в inbox/eldamo/src/data/eldamo-data.xml словарные статьи <word v="…">,
чьё v начинается со «слово» (без учёта регистра и диакритики), и напечатать язык, v, gloss и первые cite.
2026-10-18. Нужен для разбора имён (например, «Ránatar Maivandion»)."""
import re, sys, unicodedata, os

def bare(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
path = os.path.join(root, "inbox", "eldamo", "src", "data", "eldamo-data.xml")
q = bare(sys.argv[1])
lang = sys.argv[2] if len(sys.argv) > 2 else None
text = open(path, encoding="utf-8").read()
n = 0
for m in re.finditer(r'<word\b([^>]*)>', text):
    attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
    v = attrs.get("v", "")
    if not bare(v).startswith(q):
        continue
    if lang and attrs.get("l") != lang:
        continue
    chunk = text[m.end():m.end() + 1500]
    refs = re.findall(r'<ref\b[^>]*v="([^"]*)"[^>]*source="([^"]*)"', chunk)[:3]
    print("%-5s %-20s %-30s %s" % (attrs.get("l", "?"), v, attrs.get("gloss", ""), "; ".join("%s (%s)" % r for r in refs)))
    n += 1
    if n >= 25:
        break
print("найдено (до 25):", n)
