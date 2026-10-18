"""ochered.py [слово] — очередь проверок: все оговорки «по памяти», «не проверял», «не проверено», «не сверял»,
«(??)» в notes/ и proekty/**/README.md, с файлом, строкой и куском контекста.
Оговорка честна, пока за ней стоит невыполненная проверка (правило 2026-10-18): эта очередь — то, что можно проверить.
С аргументом — только строки, где есть это слово (например: ochered.py Толкин)."""
import os, re, sys, glob

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
HEDGE = re.compile(r"по памяти|не проверял|не проверено|не сверял|не сверено|\(\?\?\)")
flt = sys.argv[1].lower() if len(sys.argv) > 1 else None
files = sorted(glob.glob(os.path.join(root, "notes", "*.md")) +
               glob.glob(os.path.join(root, "proekty", "**", "README.md"), recursive=True))
total = 0
for p in files:
    rel = os.path.relpath(p, root)
    for i, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
        for m in HEDGE.finditer(line):
            ctx = line[max(0, m.start() - 90): m.end() + 30].replace("\n", " ").strip()
            if flt and flt not in ctx.lower():
                continue
            total += 1
            print("%s:%d  …%s…" % (rel, i, ctx))
print("всего оговорок:", total)
