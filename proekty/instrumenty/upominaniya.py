"""upominaniya.py [папка] [--all] — что в папке inbox ещё не упомянуто в моих файлах (diary, notes, proekty).
Без аргумента — страницы из notes/karta-html.md (как раньше). С папкой — все текстовые файлы в ней
(.md .txt .html .json), по убыванию числа слов; ключ — имя файла без расширения.
Печатает только неупомянутые; --all — все, с числом упоминаний.
Примеры:  python3 proekty/instrumenty/upominaniya.py
          python3 proekty/instrumenty/upominaniya.py inbox/Synthesises-of-concepts"""
import os, re, sys, glob

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
mine = []
for d in ("diary", "notes", "proekty"):
    for p in glob.glob(os.path.join(root, d, "**", "*.md"), recursive=True):
        if p.endswith("karta-html.md"):
            continue
        mine.append(open(p, encoding="utf-8", errors="replace").read())
show_all = "--all" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]

rows = []
if not args:
    karta = open(os.path.join(root, "notes", "karta-html.md"), encoding="utf-8").read()
    for line in karta.splitlines():
        m = re.match(r"^\| `([^`]+)\.html` \| (.*?) \| (\d+) \|", line)
        if m:
            rows.append((m.group(1), int(m.group(3)), m.group(2)[:50]))
else:
    base = args[0]
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if d not in ("node_modules", ".git", "build")]
        for f in fn:
            if not f.lower().endswith((".md", ".txt", ".html", ".json")):
                continue
            p = os.path.join(dp, f)
            try:
                w = len(open(p, encoding="utf-8", errors="ignore").read().split())
            except OSError:
                continue
            rows.append((os.path.splitext(f)[0], w, os.path.relpath(p, base)))

seen = 0
for stem, words, label in sorted(rows, key=lambda r: -r[1]):
    keys = [stem]
    m = re.match(r"^(PS-\d+)-", stem)  # в заметках пишу коротко: «PS-6933» (поправка 2026-10-18 днём)
    if m:
        keys.append(m.group(1))
    k = sum(1 for t in mine if any(re.search(re.escape(x) + r"(?!\d)", t) for x in keys))
    seen += k > 0
    if show_all or k == 0:
        print("%3d  %7d  %s" % (k, words, label))
print("всего %d, упомянуто %d, не упомянуто %d" % (len(rows), seen, len(rows) - seen))
