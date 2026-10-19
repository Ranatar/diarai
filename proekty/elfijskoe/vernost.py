"""vernost.py — проверка предрегистрированной гипотезы (korko.md): длинные строки «Ворона» Luinyelle ближе к По?
Мера: доля значимых слов строки По (основы по первым 5 буквам), найденных в английском подстрочнике той же строки.
Запуск без -I (нужен соседний kv_udar из proekty/instrumenty): python3 proekty/elfijskoe/vernost.py
Входы: ext/poe/raven.txt (Gutenberg #1065), ext/tmp/eca/luinyelle__i-korko.txt (html2txt)."""
import re, sys, os, statistics
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, os.path.join(R, "proekty", "instrumenty"))
import kv_udar as K

poe = [l.strip() for l in open(os.path.join(R, "ext", "poe", "raven.txt"), encoding="utf-8").read().splitlines()[36:161] if l.strip()]
assert len(poe) == 108, len(poe)
L = open(os.path.join(R, "ext", "tmp", "eca", "luinyelle__i-korko.txt"), encoding="utf-8").read().splitlines()
q, en = [], []
for i, l in enumerate(L):
    if re.match(r"^\d+\) ", l):
        for k in range(6):
            q.append(L[i + 2 * k]); en.append(L[i + 12 + 2 * k])
assert len(q) == 108 and len(en) == 108

STOP = set("a an the and or of to in on at by for with from as is it its i me my he him his she her you your thou thy thee we our they them this that these those be been was were am are but not no nor so then there here what which who whom whose when while if than till until into upon over still more nothing only just".split())
def stems(s):
    return {w[:5] for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP and len(w) > 2}

rows = []
for j in range(108):
    pos = j % 6 + 1
    if pos not in (2, 3, 4, 5):
        continue
    n, _, bad = K.check(q[j])
    P, E = stems(poe[j]), stems(en[j])
    share = len(P & E) / len(P) if P else 0
    rows.append((n, share, pos, poe[j][:60], en[j][:60]))

long_ = [r[1] for r in rows if r[0] >= 17]
even = [r[1] for r in rows if r[0] == 16]
print("строк 2–5: %d; 16 слогов: %d, 17+: %d" % (len(rows), len(even), len(long_)))
print("средняя доля общих основ: 16 слогов %.3f (медиана %.3f); 17+ %.3f (медиана %.3f)" % (
    statistics.mean(even), statistics.median(even), statistics.mean(long_), statistics.median(long_)))
print("разница (17+ минус 16): %+.3f" % (statistics.mean(long_) - statistics.mean(even)))
# перестановочный тест: насколько часто случайное деление даёт разницу не меньше наблюдаемой
import random
random.seed(1)
allv = long_ + even
obs = statistics.mean(long_) - statistics.mean(even)
cnt = 0
for _ in range(20000):
    random.shuffle(allv)
    a, b = allv[:len(long_)], allv[len(long_):]
    if statistics.mean(a) - statistics.mean(b) >= obs:
        cnt += 1
print("перестановочный тест (одностор.): p ≈ %.3f" % (cnt / 20000))
if "-v" in sys.argv:
    for r in sorted(rows):
        print("%2d %.2f  %s | %s" % (r[0], r[1], r[3], r[4]))
