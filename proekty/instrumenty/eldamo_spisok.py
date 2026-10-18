"""eldamo_spisok.py слово [слово …] — для каждого слова: точные статьи Eldamo (v совпадает без учёта диакритики),
иначе — статьи, чьё v начинается с первых 4 букв слова. Язык и gloss. 2026-10-18 (проверка «Vinya maitaren»)."""
import re, sys, unicodedata, os
def bare(s): return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower().strip("-¹²³")
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
text = open(os.path.join(root, "inbox", "eldamo", "src", "data", "eldamo-data.xml"), encoding="utf-8").read()
words = []
for m in re.finditer(r'<word\b([^>]*)>', text):
    a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
    if a.get("l") in ("q", "nq", "mq", "eq"):
        words.append((bare(a.get("v", "")), a.get("l"), a.get("v", ""), a.get("gloss", "")))
for w in sys.argv[1:]:
    b = bare(w)
    exact = [x for x in words if x[0] == b]
    if exact:
        print("%-12s ТОЧНО: %s" % (w, "; ".join("%s %s «%s»" % (l, v, g) for _, l, v, g in exact[:3])))
    else:
        near = [x for x in words if x[0].startswith(b[:4])][:4]
        print("%-12s нет; близкие: %s" % (w, "; ".join("%s %s «%s»" % (l, v, g) for _, l, v, g in near) or "—"))
