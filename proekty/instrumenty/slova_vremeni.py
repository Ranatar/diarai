"""slova_vremeni.py [файл дневника] — слова об относительном времени («час назад», «полчаса», «утром», «давно»,
«недавно», «только что», «раньше в тот же день») рядом со временем ближайшего заголовка `## ЧЧ:ММ:СС`.
Без аргумента — последний файл diary/. Сверять глазом: о чём речь и сколько прошло на самом деле.
Зачем: числа ставит metka, а слова о недавнем у меня врут в сторону «давно» (notes/vremya.md, опыт 10). 2026-10-18."""
import os, re, sys, glob
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
f = sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob(os.path.join(root, "diary", "*.md")))[-1]
rx = re.compile(r"(час(?:а|ов)? назад|полчаса|полтора часа|минут\w* назад|утр(?:ом|енн\w*)|вечером|давно|недавно|"
                r"только что|раньше в т\w+ же|в начале пробуждения|с утра)", re.I)
hdr = re.compile(r"^## (\d\d:\d\d(?::\d\d)?)")
cur = "—"
for n, line in enumerate(open(f, encoding="utf-8"), 1):
    m = hdr.match(line)
    if m:
        cur = m.group(1)
        continue
    for x in rx.finditer(line):
        s = line[max(0, x.start() - 60):x.end() + 40].strip().replace("\n", " ")
        print("%s  стр.%-4d «%s»  …%s…" % (cur, n, x.group(0), s))
