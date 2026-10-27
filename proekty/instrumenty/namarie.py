"""namarie.py ВЫХОД — выписать из Eldamo фразы q, у которых есть ссылка на LotR/0377 или LotR/0378 (там напечатана
«Намариэ»), упорядочив по номеру ссылки; печатает строку, ссылку и пометку о номере строки из заметок (если есть).
27.10.2026 — для сверки слогов русского перевода автора («ударения и количества слогов полностью соответствуют
оригиналу»). Первая версия искала строки внутри статьи «Namárië» — их там нет, они отдельными статьями."""
import os
import re
import sys

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
xml = open(os.path.join(root, "inbox", "eldamo", "src", "data", "eldamo-data.xml"), encoding="utf-8").read()
out = []
for m in re.finditer(r'<word ([^>]*)>', xml):
    a = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', m.group(1)))
    if a.get("l") != "q" or a.get("speech") != "phrase":
        continue
    tail = xml[m.end():m.end() + 6000]
    nxt = re.search(r'<word ', tail)
    body = tail if not nxt else tail[:nxt.start()]
    refs = re.findall(r'source="(LotR/037[78]\.\d+)"', body)
    if not refs:
        continue
    note = re.search(r'([A-Z][a-z]+(?:-[a-z]+)?) lines?\b', body)
    out.append((min(refs), a["v"], note.group(0) if note else ""))
out.sort()
with open(sys.argv[1], "w", encoding="utf-8") as f:
    for ref, v, note in out:
        f.write(v + "\n")
        print("%-16s %-14s %s" % (ref, note, v))
print(len(out), "фраз ->", sys.argv[1])
