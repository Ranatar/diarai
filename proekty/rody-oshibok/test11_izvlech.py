"""test11_izvlech.py — перепись ссылок на Библию в inbox для теста 11; жанр («цитата» / «опора») — механически.
Запуск: python3 -I test11_izvlech.py inbox > test11-perepis.tsv"""
import sys, os, re, html

KN = {"Быт": "gn", "Исх": "ex", "Лев": "lv", "Чис": "nm", "Втор": "dt", "Нав": "js", "Суд": "jz", "Руф": "rt",
      "Иов": "jó", "Пс": "sl", "Притч": "pv", "Еккл": "ec", "Песн": "ct", "Ис": "is", "Иер": "jr", "Плач": "lm",
      "Иез": "ez", "Дан": None, "Есф": None, "Ос": "os", "Иоил": "jl", "Ам": "am", "Мих": "mq", "Авв": "hc",
      "Зах": "zc", "Мал": "ml", "Мф": "mt", "Мк": "mc", "Лк": "lc", "Ин": "jo", "Деян": "atos", "Рим": "rm",
      "1 Кор": "1co", "2 Кор": "2co", "1Кор": "1co", "2Кор": "2co", "Гал": "gl", "Еф": "ef", "Флп": "fp",
      "Кол": "cl", "1 Фес": "1ts", "1 Тим": "1tm", "2 Тим": "2tm", "Евр": "hb", "Иак": "tg", "1 Пет": "1pe",
      "2 Пет": "2pe", "1 Ин": "1jo", "1Ин": "1jo", "Откр": "ap", "Апок": "ap"}
names = sorted(KN, key=len, reverse=True)
REF = re.compile(r"(?<![А-Яа-яЁё0-9])(" + "|".join(re.escape(n) for n in names) +
                 r")\.?\s?(\d{1,3}):(\d{1,3})(?:\s?[–\-—]\s?(\d{1,3}))?")
QUOTE = re.compile(r"«([^«»]{3,400})»|\"([^\"]{3,400})\"|„([^„“]{3,400})“")

def text_of(p):
    raw = open(p, encoding="utf-8", errors="replace").read()
    if p.endswith((".html", ".htm")):
        raw = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", raw)
        raw = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    if p.endswith(".json"):
        raw = raw.replace("\\n", " ").replace('\\"', '"')
    return re.sub(r"\s+", " ", raw)

def zhanr(t, a, b):
    win = t[max(0, a - 200): b + 60]
    for m in QUOTE.finditer(win):
        s = next(g for g in m.groups() if g)
        if len(s.split()) >= 4:
            return "цитата"
    return "опора"

print("id\tфайл\tссылка\tкнига\tглава\tстих\tпо\tжанр\tконтекст\tвердикт\tкомментарий")
seen, k = set(), 0
for dp, dn, fn in sorted(os.walk(sys.argv[1])):
    for f in sorted(fn):
        if not f.endswith((".html", ".htm", ".md", ".txt", ".json")):
            continue
        p = os.path.join(dp, f)
        t = text_of(p)
        for m in REF.finditer(t):
            kn, gl, st, po = m.group(1), m.group(2), m.group(3), m.group(4) or ""
            key = (kn, gl, st, re.sub(r"\W", "", t[max(0, m.start() - 80): m.end() + 40]))
            if key in seen:
                continue
            seen.add(key)
            ctx = t[max(0, m.start() - 250): m.end() + 150].replace("\t", " ")
            print("\t".join([str(k), os.path.relpath(p, sys.argv[1]), m.group(0), str(KN[kn]), gl, st, po,
                             zhanr(t, m.start(), m.end()), ctx, "", ""]))
            k += 1
