"""mertvye.py — в каких эскизах формула проекции (x6/y6) есть в живом коде, но холст её не использует:
живые присваивания x7/y7 не ссылаются на x6/y6. Тогда метка в out/formuly.tsv («поликоническая» и т. п.)
описывает мёртвый код. Найдено 2026-10-18 (пробуждение 19:01): первый живой снимок в браузере эскиза
Kruzhochek1-5-6-1 (2023) показал два ортографических полушария, а таблица называла его поликоническим.
python3 -I proekty/kruzhochek/mertvye.py"""
import os, re, csv
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "inbox", "нян")

def live(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return [l.split("//")[0] for l in text.splitlines() if l.split("//")[0].strip()]

metki = {}
for row in csv.reader(open(os.path.join(HERE, "out", "formuly.tsv"), encoding="utf-8"), delimiter="\t"):
    if len(row) >= 3:
        metki[row[1]] = row[2]

itog = []
for f in sorted(os.listdir(SRC)):
    if not f.endswith(".html"):
        continue
    L = live(open(os.path.join(SRC, f), encoding="utf-8", errors="replace").read())
    x6 = [l for l in L if re.search(r"\b[xy]6\s*=", l)]
    x7 = [l for l in L if re.search(r"\b[xy]7\s*=", l)]
    if not x6 or not x7:
        continue
    if not any(re.search(r"\b[xy]6(_\w+)?\b", l) for l in x7):  # x6_1, x6_2 — тоже проекция
        uses = x7[0].strip()[:90]
        itog.append((f, metki.get(f, ""), uses))

for f, m, u in itog:
    print("%s\tметка: %s\tхолст из: %s" % (f, m[:70], u))
print("всего эскизов с мёртвой x6/y6:", len(itog))
