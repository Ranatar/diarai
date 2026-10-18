"""bigrammy.py стихи[:кодировка] корпус[:кодировка] — доля 1..4-грамм ВНУТРИ строк стихов, встречающихся в корпусе.
Подпись цепи Маркова первого порядка: слова ~100 %, биграммы ~97–100 %, триграммы резко ниже. Сито (нарезка без
перестановок) дало бы высокие доли на всех n. Обобщение sito_2020c/d.py, 2026-10-18."""
import re, sys
def norm(s): return re.findall(r"[а-я]+", s.lower().replace("ё", "е"))
def rd(arg):
    p, _, enc = arg.partition(":")
    return open(p, encoding=enc or "utf-8", errors="replace").read().replace("\r", "")
corpus = norm(rd(sys.argv[2]))
grams = {n: set(zip(*[corpus[i:] for i in range(n)])) for n in (1, 2, 3, 4)}
lines = [norm(l) for l in rd(sys.argv[1]).split("\n") if norm(l)]
out = []
for n in (1, 2, 3, 4):
    g = [x for w in lines for x in zip(*[w[i:] for i in range(n)])]
    out.append("%d: %5.1f %%" % (n, 100 * sum(1 for x in g if x in grams[n]) / max(1, len(g))))
print("корпус %d слов, строк %d | %s" % (len(corpus), len(lines), " | ".join(out)))
