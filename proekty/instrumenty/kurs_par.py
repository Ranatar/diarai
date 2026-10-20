"""kurs_par.py НОМЕР [НОМЕР…] [--n строк] — напечатать параграф курса квенья по номеру (например 5.2.1.2),
из текста ext/tmp/qfull.txt (вторая, основная копия — после оглавления). По умолчанию 8 строк.
2026-10-18, пробуждение 21:20 (перевод «Завесы» на квенья)."""
import sys, re, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
args = sys.argv[1:]
n = 8
if "--n" in args:
    i = args.index("--n"); n = int(args[i + 1]); del args[i:i + 2]
t = open(os.path.join(ROOT, "ext", "tmp", "qfull.txt"), encoding="utf-8").read().split("\n")
for num in args:
    hits = [i for i, l in enumerate(t) if re.match(re.escape(num) + r"[\s:]", l)]
    if not hits:
        print("== %s: не найдено" % num); continue
    i = hits[-1] if len(hits) > 1 else hits[0]
    print("== %s (строка %d, всего вхождений %d)" % (num, i + 1, len(hits)))
    for l in t[i:i + n]:
        # 20.10: раньше строка обрезалась до 900 знаков молча; теперь с пометкой
        print(l[:900] + (" […обрезано: строка %d знаков; читать ext/tmp/qfull.txt]" % len(l) if len(l) > 900 else ""))
