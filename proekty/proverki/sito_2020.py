# Проверка: нарезаны ли стихи Циолковского 2020 года ситом из корпуса inbox/Tsiolkovskiy_texty.txt
# (слова строфы идут в корпусе подряд, без перестановок). cp1251.
import re, sys
def words(path):
    t = open(path, encoding="cp1251", errors="replace").read().lower().replace("ё", "е")
    return re.findall(r"[а-я]+", t)
corpus = words("/home/diarai/diarai/inbox/Tsiolkovskiy_texty.txt")
cj = " " + " ".join(corpus) + " "
for name in ("Tsiolkovskiy_tanka.txt", "Tsiolkovskiy_gekzametry.txt", "Tsiolkovskiy_chastushki.txt", "Tsiolkovskiy_oneginskaya.txt"):
    raw = open("/home/diarai/diarai/inbox/" + name, encoding="cp1251", errors="replace").read().replace("\r", "")
    stanzas = [s for s in re.split(r"\n\s*\n", raw) if re.search(r"[а-яА-Я]", s)]
    found = 0
    for s in stanzas:
        w = re.findall(r"[а-я]+", s.lower().replace("ё", "е"))
        if w and (" " + " ".join(w) + " ") in cj:
            found += 1
    print("%-30s строф %3d, найдено подряд в корпусе: %3d" % (name, len(stanzas), found))
    if stanzas:
        print("   пример:", stanzas[0].strip().replace("\n", " / ")[:160])
