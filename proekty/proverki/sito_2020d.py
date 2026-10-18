# То же, что sito_2020c.py, для Хайдеггера: стихи inbox/Khaydegger_*.txt (cp1251) против корпуса
# inbox/lleo_dip/heid.txt («Вопрос о технике», cp866). n-граммы только внутри строк.
import re
def norm(s): return re.findall(r"[а-я]+", s.lower().replace("ё", "е"))
corpus = norm(open("/home/diarai/diarai/inbox/lleo_dip/heid.txt", encoding="cp866", errors="replace").read())
print("слов в корпусе:", len(corpus))
grams = {n: set(zip(*[corpus[i:] for i in range(n)])) for n in (1, 2, 3, 4)}
for name in ("Khaydegger_chastushki.txt", "Khaydegger_khokku.txt", "Khaydegger_sinkveyn.txt"):
    raw = open("/home/diarai/diarai/inbox/" + name, encoding="cp1251", errors="replace").read().replace("\r", "")
    lines = [norm(l) for l in raw.split("\n") if norm(l)]
    out = []
    for n in (1, 2, 3, 4):
        g = [x for w in lines for x in zip(*[w[i:] for i in range(n)])]
        out.append("%d: %5.1f %%" % (n, 100 * sum(1 for x in g if x in grams[n]) / max(1, len(g))))
    print("%-28s %s" % (name, " | ".join(out)))
