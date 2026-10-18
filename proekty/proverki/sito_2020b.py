# Уточнение: строки по отдельности — есть ли подряд в корпусе? Строфа — упорядоченная подпоследовательность в окне?
import re, bisect
from collections import defaultdict
def norm(s): return re.findall(r"[а-я]+", s.lower().replace("ё", "е"))
corpus = norm(open("/home/diarai/diarai/inbox/Tsiolkovskiy_texty.txt", encoding="cp1251", errors="replace").read())
cj = " " + " ".join(corpus) + " "
pos = defaultdict(list)
for i, w in enumerate(corpus):
    pos[w].append(i)
print("слов в корпусе:", len(corpus))

def subseq_window(ws, W=400):
    """Есть ли такое начало, что слова идут по порядку и все укладываются в W слов корпуса."""
    for start in pos.get(ws[0], [])[:2000]:
        cur, ok = start, True
        for w in ws[1:]:
            L = pos.get(w)
            if not L: return None
            j = bisect.bisect_right(L, cur)
            if j == len(L) or L[j] - start > W:
                ok = False; break
            cur = L[j]
        if ok: return start, cur - start
    return False

for name in ("Tsiolkovskiy_tanka.txt", "Tsiolkovskiy_chastushki.txt", "Tsiolkovskiy_gekzametry.txt"):
    raw = open("/home/diarai/diarai/inbox/" + name, encoding="cp1251", errors="replace").read().replace("\r", "")
    stanzas = [s for s in re.split(r"\n\s*\n", raw) if re.search(r"[а-яА-Я]", s)]
    lines = [l for s in stanzas for l in s.split("\n") if norm(l)]
    lc = sum(1 for l in lines if (" " + " ".join(norm(l)) + " ") in cj)
    res = [subseq_window(norm(s)) for s in stanzas[:20]]
    print("%-28s строк подряд в корпусе: %d из %d; строф-подпоследовательностей в окне 400 слов (из первых 20): %d; пример: %s"
          % (name, lc, len(lines), sum(1 for r in res if r), next((r for r in res if r), None)))
