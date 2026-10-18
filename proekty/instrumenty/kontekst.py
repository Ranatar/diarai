"""kontekst.py файл слово [слово …] — где в тексте встречаются слова (без учёта регистра), с контекстом ±70 знаков.
Печатает и число вхождений каждого слова, включая нули: отсутствие — тоже результат.
Нужен потому, что здешний grep (ugrep) не тянет длинных `.{0,80}` с кириллицей. 2026-10-18."""
import re, sys

text = open(sys.argv[1], encoding="utf-8").read()
low = text.lower()
W = 70
for w in sys.argv[2:]:
    hits = [m.start() for m in re.finditer(re.escape(w.lower()), low)]
    print("== %s: %d" % (w, len(hits)))
    for h in hits[:6]:
        s = text[max(0, h - W):h + len(w) + W].replace("\n", " ")
        print("   …%s…" % s)
