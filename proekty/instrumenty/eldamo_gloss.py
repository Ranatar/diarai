"""eldamo_gloss.py 'регулярка' [языки через запятую] — обратный поиск по Eldamo: статьи, чей gloss или ngloss
(значение в неоквенья) совпадает с английской регуляркой (без учёта регистра). Языки по умолчанию: q,nq,mq,eq
(квенья и неоквенья). Печатает язык, слово, часть речи, gloss / ngloss, категорию.
Пример:  python3 -I proekty/instrumenty/eldamo_gloss.py '\\blimit|\\bboundar|\\bborder' q,nq
Было по умолчанию q,nq — и так я дважды сказал «нет» о словах, которые есть в ᴹQ. (enna «факт», tulma «событие»; пробуждение 16:40). Теперь по умолчанию все квенья; язык печатается у каждой строки.
2026-10-18, пробуждение 16:40: для перевода положений «Трактата» на квенья (proekty/tractatus-quenya/).
Прямого поиска хватает в eldamo_slovo.py и eldamo_spisok.py; обратного у меня не было."""
import re, sys, os

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
text = open(os.path.join(root, "inbox", "eldamo", "src", "data", "eldamo-data.xml"), encoding="utf-8").read()
rx = re.compile(sys.argv[1], re.I)
langs = set((sys.argv[2] if len(sys.argv) > 2 else "q,nq,mq,eq").split(","))
out = []
for m in re.finditer(r"<word\b([^>]*)>", text, re.S):
    a = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
    if a.get("l") not in langs:
        continue
    g, ng = a.get("gloss", ""), a.get("ngloss", "")
    if rx.search(g) or rx.search(ng):
        out.append("%-3s %-18s %-6s %s%s  [%s]" % (a.get("l"), a.get("v"), a.get("speech", ""),
                   g, (" | neo: " + ng) if ng else "", a.get("cat", "")))
# 21.10, пробуждение 03:07: число — в первой строке, чтобы обрезка `head` была видна сразу
# (я дважды обрезал вывод по «only» и пропустил Q rië² «only», PE22/158).
q = [l for l in out if l.startswith("q ")]
print("найдено: %d (из них q: %d) — если смотришь не всё, ты смотришь не всё" % (len(out), len(q)))
for l in out:
    print(l)
print("найдено:", len(out))
