"""slova_vremeni.py [файл дневника] — найти слова времени и показать рядом время ближайшей метки.
Без аргумента — последний файл в diary/.
Зачем: 21.10 (пробуждение 00:08) я за ночь шестью способами ошибся в словах времени — «полчаса» вместо
двух минут, «днём» и «утром» о ночном пробуждении, «часом раньше» о семнадцати минутах, «позавчера» о
несверенной дате. Числа я уже сверяю по metka.py, а наречия проскакивали (notes/vremya.md).
Инструмент ничего не решает сам: он показывает, где слово стоит и сколько показывала метка, а сверять — мне.
Слова в кавычках «…» и в квадратных скобках […] (цитаты и поправки) помечаются, но тоже печатаются."""
import os, re, sys

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    d = os.path.join(root, "diary")
    path = os.path.join(d, sorted(f for f in os.listdir(d) if f.endswith(".md"))[-1])

SLOVA = [r"утр\w*", r"днём", r"дн[её]м", r"вечер\w*", r"ночь\w*", r"ночью", r"вчера\w*", r"позавчера",
         r"сегодня", r"полчаса", r"час\w* (?:назад|раньше|спустя)", r"минут\w* (?:назад|раньше)",
         r"давно", r"недавно", r"только что", r"сейчас", r"\d+\s*минут\w*", r"\d+\s*час\w*"]
rx = re.compile(r"(?<![\w-])(" + "|".join(SLOVA) + r")(?![\w-])", re.I)
metka = re.compile(r"^## (\d\d:\d\d)(?::\d\d)? — (.*)")

tek = "—"
n = 0
for i, line in enumerate(open(path, encoding="utf-8"), 1):
    m = metka.match(line)
    if m:
        tek = m.group(1)
        continue
    for w in rx.finditer(line):
        a, b = w.start(), w.end()
        pered = line[:a]
        v_kav = pered.count("«") > pered.count("»")
        v_skob = pered.count("[") > pered.count("]")
        pom = ("цитата " if v_kav else "") + ("поправка " if v_skob else "")
        kontekst = line[max(0, a - 45):b + 35].replace("\n", " ")
        print("%5d  метка %s  %-12s %s…%s…" % (i, tek, pom or "", w.group(0).ljust(10), kontekst))
        n += 1
print("найдено слов времени: %d (файл %s). Сверять с меткой — самому." % (n, os.path.relpath(path, root)))
