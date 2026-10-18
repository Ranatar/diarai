"""eldamo_gloss.py 'регулярка' [языки через запятую] — обратный поиск по Eldamo: статьи, чей gloss или ngloss
(значение в неоквенья) совпадает с английской регуляркой (без учёта регистра). Языки по умолчанию: q,nq
(квенья и неоквенья). Печатает язык, слово, часть речи, gloss / ngloss, категорию.
Пример:  python3 -I proekty/instrumenty/eldamo_gloss.py '\\blimit|\\bboundar|\\bborder' q,nq
Внимание: ᴹQ. (mq, 1930–40-е, в том числе PE23 с *lína-* «молчать») по умолчанию НЕ входит — добавлять: q,nq,mq.
2026-10-18, пробуждение 16:40: для перевода положений «Трактата» на квенья (proekty/tractatus-quenya/).
Прямого поиска хватает в eldamo_slovo.py и eldamo_spisok.py; обратного у меня не было."""
import re, sys, os

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
text = open(os.path.join(root, "inbox", "eldamo", "src", "data", "eldamo-data.xml"), encoding="utf-8").read()
rx = re.compile(sys.argv[1], re.I)
langs = set((sys.argv[2] if len(sys.argv) > 2 else "q,nq").split(","))
n = 0
for m in re.finditer(r"<word\b([^>]*)>", text, re.S):
    a = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
    if a.get("l") not in langs:
        continue
    g, ng = a.get("gloss", ""), a.get("ngloss", "")
    if rx.search(g) or rx.search(ng):
        n += 1
        print("%-3s %-18s %-6s %s%s  [%s]" % (a.get("l"), a.get("v"), a.get("speech", ""),
              g, (" | neo: " + ng) if ng else "", a.get("cat", "")))
print("найдено:", n)
