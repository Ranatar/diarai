"""ppf.py ЛИСТ [ЛИСТ …]   — заметки «Philosophie der Psychologie – Ein Fragment» (PU ч. II, MS 144) по номеру листа:
                             ppf.py 19v[3]  или  ppf.py 19v  (все заметки листа 19v).
   ppf.py --iskat СЛОВО     — все заметки, где встречается слово (без учёта регистра), с контекстом.
   ppf.py --razdel xi       — первая заметка раздела (i … xiv) и её номер.
Источник: ext/wn/ppf.txt (wittgensteinnachlass.com/w-ppf/ → html2txt.py; как скачать — notes/tehnika.md, «Источники текстов»).
Текст — по рукописи MS 144, не по печатному изданию: «&» вместо «und», нумерация — листы рукописи, а не §§ издания.
2026-10-21, пробуждение 12:08: чтобы цитировать часть II так же, как часть I через pu.py, а не по памяти."""
import os, re, sys
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
txt = open(os.path.join(root, "ext", "wn", "ppf.txt"), encoding="utf-8").read()
# блоки: "### §Ms-144 \n<ids через ' &\n'>\n\n<текст>"
bloki = []
for b in re.split(r"\n### §Ms-144 *\n", "\n" + txt)[1:]:
    head, _, body = b.partition("\n\n")
    ids = [x.strip() for x in head.replace("&", "\n").split("\n") if x.strip()]
    body = body.strip()
    m = re.match(r"^([ivx]{1,5}) (?=\S)", body)
    razdel = m.group(1) if m else None
    bloki.append((ids, razdel, body))
a = sys.argv[1:]
if not a:
    print(__doc__); sys.exit()
if a[0] == "--iskat":
    w = " ".join(a[1:]).lower(); n = 0
    for ids, _, body in bloki:
        for m in re.finditer(re.escape(w), body.lower()):
            print("%s: …%s…" % ("+".join(ids), body[max(0, m.start() - 60): m.end() + 60].replace("\n", " ")))
            n += 1
    print("найдено:", n)
elif a[0] == "--razdel":
    for ids, r, body in bloki:
        if r == a[1]:
            print("+".join(ids), "—", body[:200]); break
    else:
        print("раздел не найден")
else:
    for q in a:
        hit = [(ids, body) for ids, _, body in bloki
               if any(i == q or (("[" not in q) and i.split("[")[0] == q) for i in ids)]
        if not hit:
            print(q, "— нет такого листа/заметки")
        for ids, body in hit:
            print("== %s\n%s\n" % ("+".join(ids), body))
