"""metr.py файл [--metr u-u] — проверка русских строк на любой силлабо-тонический размер по словарю udar.py.
Метр: «-» сильное место, «u» слабое, повторяется по кругу (ямб u-, хорей -u, дактиль -uu, амфибрахий u-u,
анапест uu-). Строка годится, если ударение каждого многосложного слова МОЖЕТ стоять на сильном месте
(омографы — любой из вариантов), односложные — где угодно. Незнакомое слово — «?» и отказ.
Строки берутся до первой «---», пустые и начинающиеся с # или * пропускаются.
2026-10-19 (перевод квенийского «Essë» автора амфибрахием; yamb.py умеет только ямб).
Запуск без -I (нужен соседний udar.py): python3 proekty/hokku/metr.py стихи.md --metr u-u"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from udar import stress, nsyl

args = sys.argv[1:]
metr = "u-u"
if "--metr" in args:
    i = args.index("--metr"); metr = args[i + 1]; del args[i:i + 2]
text = open(args[0], encoding="utf-8").read().split("\n---")[0]
ok_all = 0; n_all = 0
for line in text.splitlines():
    L = line.strip()
    if not L or L.startswith("#") or L.startswith("*"):
        continue
    words = re.findall(r"[а-яёА-ЯЁ]+", L)
    if not words or L.startswith(">"):  # цитата подлинника и строки без кириллицы — не считаем (иначе «OK, 0 слогов»)
        continue
    pos, bad, marks = 0, [], ""
    for w in words:
        n = nsyl(w)
        if n == 0:
            continue
        if n == 1:
            marks += "?"; pos += 1; continue
        s = stress(w)
        if not s:
            bad.append(w + "(?)"); marks += "x" * n; pos += n; continue
        good = [k for k in s if metr[(pos + k - 1) % len(metr)] == "-"]
        if not good:
            bad.append(w)
        k0 = (good or sorted(s))[0]
        marks += "".join("-" if j == k0 else "u" for j in range(1, n + 1))
        pos += n
    n_all += 1; ok_all += not bad
    print("%s %2d %-18s %s%s" % ("OK" if not bad else "--", pos, marks, L, ("   СБОЙ: " + ", ".join(bad)) if bad else ""))
print("%d из %d" % (ok_all, n_all))
