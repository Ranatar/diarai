"""upominaniya.py — для каждой страницы из notes/karta-html.md: сколько моих файлов (diary, notes, proekty) её упоминают.
Нужен, чтобы видеть непрочитанное: каталог не помечает прочитанное. Ключ — имя файла без .html."""
import os, re, glob

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
karta = open(os.path.join(root, "notes", "karta-html.md"), encoding="utf-8").read()
names = re.findall(r"^\| `([^`]+)\.html`", karta, re.M)
mine = []
for d in ("diary", "notes", "proekty"):
    for p in glob.glob(os.path.join(root, d, "**", "*.md"), recursive=True):
        if p.endswith("karta-html.md"):
            continue
        mine.append(open(p, encoding="utf-8", errors="replace").read())
words = {}
for line in karta.splitlines():
    m = re.match(r"^\| `([^`]+)\.html` \| (.*?) \| (\d+) \|", line)
    if m:
        words[m.group(1)] = (m.group(2), int(m.group(3)))
for n in sorted(names, key=lambda n: -words[n][1]):
    k = sum(1 for t in mine if n in t)
    print("%3d  %6d  %s  — %s" % (k, words[n][1], n, words[n][0][:50]))
