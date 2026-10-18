# Доля n-грамм строк, встречающихся в корпусе: если биграммы ~100 %, а дальше падает — похоже на цепь Маркова.
import re
def norm(s): return re.findall(r"[а-я]+", s.lower().replace("ё", "е"))
corpus = norm(open("/home/diarai/diarai/inbox/Tsiolkovskiy_texty.txt", encoding="cp1251", errors="replace").read())
grams = {n: set(zip(*[corpus[i:] for i in range(n)])) for n in (2, 3, 4)}
for name in ("Tsiolkovskiy_tanka.txt", "Tsiolkovskiy_chastushki.txt", "Tsiolkovskiy_gekzametry.txt", "Tsiolkovskiy_oneginskaya.txt"):
    raw = open("/home/diarai/diarai/inbox/" + name, encoding="cp1251", errors="replace").read().replace("\r", "")
    lines = [norm(l) for l in raw.split("\n") if norm(l)]  # только внутри строк (первый прогон шёл сквозь строки — неверно)
    out = []
    for n in (2, 3, 4):
        g = [x for w in lines for x in zip(*[w[i:] for i in range(n)])]
        if not g:
            out.append("%d-грамм нет" % n); continue
        out.append("%d-граммы %5.1f %%" % (n, 100 * sum(1 for x in g if x in grams[n]) / len(g)))
    print("%-30s %s" % (name, " | ".join(out)))
