# Судьба фигур, не прошедших проверку периода: популяция по поколениям и итог.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from life_check import P, cells, step, period, norm

for name, n in (("clock", 60), ("loafer", 400), ("simkinGliderGun", 1200), ("rabbits", 0)):
    if n == 0:
        continue
    cur = cells(P[name])
    pops = []
    for g in range(n + 1):
        pops.append(len(cur))
        cur = step(cur)
    print(name, "популяция:", pops[:12], "…", pops[-5:])
    print("   период итога (если стабилен):", period(cur, 300))

# Rabbits из кода и Rabbits по памяти (RLE o3b3o$3o2bo$bo!)
mine = [[1, 0, 0, 0, 1, 1, 1], [1, 1, 1, 0, 0, 1, 0], [0, 1, 0, 0, 0, 0, 0]]
for label, rows in (("rabbits (код)", P["rabbits"]), ("rabbits (по памяти)", mine)):
    cur = cells(rows)
    for g in range(3000):
        cur = step(cur)
    print(label, "популяция в 3000:", len(cur))
