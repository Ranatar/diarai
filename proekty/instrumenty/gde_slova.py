"""gde_slova.py папка слово [слово …] — где в файлах папки встречаются слова (точное слово, без учёта регистра):
файл, число вхождений, первый контекст ±60 знаков. 2026-10-18, днём (для проверки кандидатов mutanty.py)."""
import os, re, sys
base, words = sys.argv[1], sys.argv[2:]
files = []
for dp, dn, fn in os.walk(base):
    dn[:] = [d for d in dn if d not in ("node_modules", ".git", "build")]
    files += [os.path.join(dp, x) for x in fn if x.lower().endswith((".md", ".txt", ".html"))]
texts = {p: open(p, encoding="utf-8", errors="ignore").read() for p in files}
for w in words:
    rx = re.compile(r"(?<![а-яёА-ЯЁ])" + re.escape(w) + r"(?![а-яёА-ЯЁ])", re.I)
    print("== %s" % w)
    for p, t in texts.items():
        ms = list(rx.finditer(t))
        if ms:
            m = ms[0]
            s = t[max(0, m.start() - 60):m.end() + 60].replace("\n", " ")
            s = re.sub(r"<[^>]{0,80}>", " ", s)
            print("   %s ×%d: …%s…" % (os.path.basename(p)[:40], len(ms), s))
