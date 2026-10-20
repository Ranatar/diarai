"""slogi.py файл — число слогов (гласных) в каждой строке русского текста. Ударения не ставит.
Строки, начинающиеся с '#', '-', '>' или '|', и пустые пропускает. 2026-10-20 (перевод Lacrimosa хореем)."""
import sys
V = set("аеёиоуыэюяАЕЁИОУЫЭЮЯ")
for line in open(sys.argv[1], encoding="utf-8"):
    s = line.rstrip("\n")
    if not s.strip() or s.lstrip()[:1] in "#->|*":
        continue
    print(f"{sum(ch in V for ch in s):3d}  {s}")
