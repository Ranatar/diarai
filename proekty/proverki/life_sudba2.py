import sys, os
sys.argv = [sys.argv[0], "none"]  # чтобы life_check не запускал свои проверки
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from life_check import P, cells, step, norm

def show(s):
    f, _ = norm(s)
    w = max(x for x, _ in f) + 1; h = max(y for _, y in f) + 1
    return "\n".join("".join("o" if (x, y) in f else "." for x in range(w)) for y in range(h))

c0 = cells(P["clock"])
c1 = step(c0); c2 = step(c1); c3 = step(c2)
print("clock g0:\n" + show(c0)); print("g1:\n" + show(c1)); print("g2:\n" + show(c2))
print("g2 == g0 по форме:", norm(c2)[0] == norm(c0)[0], "; g3 == g1:", norm(c3)[0] == norm(c1)[0])

cur = cells(P["simkinGliderGun"])
for g in range(1, 3601):
    cur = step(cur)
    if g % 600 == 0:
        print("simkin, поколение", g, "популяция", len(cur))
