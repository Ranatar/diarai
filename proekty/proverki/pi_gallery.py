# Проверка формул pi-gallery.html.
import math
from fractions import Fraction

# 1. Бильярд Гальперина: прямой счёт ударов в точной арифметике (скорости рациональны).
def galperin(ratio):
    # Fraction на 100^3 и выше раздувается (проверено: >2 мин), поэтому float; для k ≤ 4 счёт ударов устойчив.
    m, M = 1.0, float(ratio)
    v1, v2 = 0.0, -1.0  # малый шар покоится, большой летит к стене (влево)
    n = 0
    while True:
        if v2 < v1:  # большой догоняет малый (оба влево, большой быстрее) — удар шар о шар
            v1, v2 = ((m - M) * v1 + 2 * M * v2) / (m + M), ((M - m) * v2 + 2 * m * v1) / (m + M)
            n += 1
        elif v1 < 0:  # малый летит к стене
            v1 = -v1
            n += 1
        else:
            return n

for k in range(5):
    r = 100 ** k
    th = math.atan(math.sqrt(1 / r))
    print("M/m=%-10d удары=%-6d floor(pi/θ)=%-6d ceil(pi/θ)-1=%d" % (r, galperin(r), math.floor(math.pi / th), math.ceil(math.pi / th) - 1))

# 2. Мандельброт, Болл: c = -0.75 + εi, N·ε -> π
for k in range(1, 6):
    eps = 10.0 ** -k
    c = complex(-0.75, eps)
    z, n = 0j, 0
    while abs(z) <= 2:
        z = z * z + c
        n += 1
    print("ε=1e-%d  N=%d  N·ε=%.6f" % (k, n, n * eps))
