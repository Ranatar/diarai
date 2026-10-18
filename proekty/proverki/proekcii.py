# Проверка формул inbox/html-generated/maps/map-projections-formulae.html (раздел «Псевдоцилиндрические»).
# Формулы перенесены со страницы как записаны, R = 1. Равновеликость: |∂(x,y)/∂(λ,φ)| / cos φ должно быть
# постоянно (и = 1 при правильной нормировке). Тест 3 в proekty/rody-oshibok/ (предрегистрация 3d5af3d).
from math import sin, cos, tan, asin, sqrt, pi, log, radians, degrees

def newton(f, df, x0, n=60):
    x = x0
    for _ in range(n):
        d = df(x)
        if d == 0: break
        x -= f(x) / d
    return x

def th_moll(p):
    if abs(abs(p) - pi / 2) < 1e-12: return p
    return newton(lambda t: 2 * t + sin(2 * t) - pi * sin(p), lambda t: 2 + 2 * cos(2 * t), p)

P = {}
P["Синусоидальная"] = lambda l, p: (l * cos(p), p)
def moll(l, p):
    t = th_moll(p); return (2 * sqrt(2) / pi * l * cos(t), sqrt(2) * sin(t))
P["Молльвейде"] = moll
def e4(l, p):
    t = newton(lambda t: t + sin(t) * cos(t) + 2 * sin(t) - (2 + pi / 2) * sin(p), lambda t: 1 + cos(2 * t) + 2 * cos(t), p / 2)
    return (2 / sqrt(pi * (4 + pi)) * l * (1 + cos(t)), 2 * sqrt(pi / (4 + pi)) * sin(t))
P["Эккерт IV"] = e4
def e6(l, p):
    t = newton(lambda t: t + sin(t) - (1 + pi / 2) * sin(p), lambda t: 1 + cos(t), p)
    return (l * (1 + cos(t)) / sqrt(2 + pi), 2 * t / sqrt(2 + pi))
P["Эккерт VI"] = e6
P["Каврайский VII"] = lambda l, p: (1.5 * l * sqrt(1 / 3 - (p / pi) ** 2), p)
P["Вагнер VI"] = lambda l, p: (l * sqrt(1 - 3 * (p / pi) ** 2), p)
P["Коллиньон"] = lambda l, p: (2 * l / sqrt(pi) * sqrt(1 - sin(p)), sqrt(pi) * (1 - sqrt(1 - sin(p))))
P["Крастер"] = lambda l, p: (sqrt(3 / pi) * l * (2 * cos(2 * p / 3) - 1), sqrt(3 * pi) * sin(p / 3))
def boggs(l, p):
    if abs(abs(p) - pi / 2) < 1e-9: return (0.0, 0.49931 * (p + sqrt(2) * sin(p)))
    t = newton(lambda t: 2 * t + sin(2 * t) - pi * sin(p), lambda t: 2 + 2 * cos(2 * t), p / 2)
    return (2.00276 * l / (1 / cos(p) + 1.11072 / cos(t)), 0.49931 * (p + sqrt(2) * sin(t)))
P["Боггс"] = boggs
P["Квартатная"] = lambda l, p: (l * cos(p) / cos(p / 2), 2 * sin(p / 2))
k1 = 2 * sqrt(2 / (3 * pi))
P["Эккерт I"] = lambda l, p: (k1 * l * (1 - abs(p) / pi), k1 * p)
P["Эккерт II"] = lambda l, p: (2 * l * sqrt(4 - 3 * sin(abs(p))) / sqrt(6 * pi), sqrt(2 * pi / 3) * (2 - sqrt(4 - 3 * sin(abs(p)))) * (1 if p >= 0 else -1))
d3 = sqrt(4 * pi + pi ** 2)
P["Эккерт III"] = lambda l, p: (2 * (1 + sqrt(max(0.0, 1 - (2 * p / pi) ** 2))) * l / d3, 4 * p / d3)
P["Эккерт V"] = lambda l, p: (l * (1 + cos(p)) / sqrt(2 + pi), 2 * p / sqrt(2 + pi))
CW4 = (4 * pi + 3 * sqrt(3)) / 6
def w4(l, p):
    t = newton(lambda t: 2 * t + sin(2 * t) - CW4 * sin(p), lambda t: 2 + 2 * cos(2 * t), p / 2)
    return (0.86310 * l * cos(t), 1.56548 * sin(t))
P["Вагнер IV"] = w4
def hatano(l, p):
    C, cy = (2.67595, 1.75859) if p >= 0 else (2.43763, 1.93052)
    t = newton(lambda t: 2 * t + sin(2 * t) - C * sin(p), lambda t: 2 + 2 * cos(2 * t), p / 2)
    return (0.85 * l * cos(t), cy * sin(t))
P["Хатано"] = hatano
c6 = sqrt(6 / (4 + pi))
def mtfs_t(p): return newton(lambda t: t / 2 + sin(t) - (1 + pi / 4) * sin(p), lambda t: 0.5 + cos(t), p)
P["МТ плоскополюсная синусоидальная"] = lambda l, p: (c6 * (0.5 + cos(mtfs_t(p))) * l / 1.5, c6 * mtfs_t(p))
def mtfpp(l, p):
    t = asin(7 / 3 * sin(p) / sqrt(6))
    return (sqrt(6) * l * (2 * cos(2 * t / 3) - 1) / sqrt(7), 9 * sin(t / 3) / sqrt(7))
P["МТ плоскополюсная параболическая"] = mtfpp
def mtfq(l, p):
    t = newton(lambda t: sin(t / 2) + sin(t) - (1 + sqrt(2) / 2) * sin(p), lambda t: 0.5 * cos(t / 2) + cos(t), p)
    return (l * (1 + 2 * cos(t) / cos(t / 2)) / sqrt(3 * sqrt(2) + 6), 2 * sqrt(3) * sin(t / 2) / sqrt(2 + sqrt(2)))
P["МТ плоскополюсная квартатная"] = mtfq
P["Путниньш P5"] = lambda l, p: (1.01346 * l * (2 - sqrt(1 + 12 * p * p / pi ** 2)), 1.01346 * p)
A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
def ee(l, p):
    t = asin(sqrt(3) / 2 * sin(p))
    return (2 * sqrt(3) * l * cos(t) / (3 * (9 * A4 * t ** 8 + 7 * A3 * t ** 6 + 3 * A2 * t ** 2 + A1)), A4 * t ** 9 + A3 * t ** 7 + A2 * t ** 3 + A1 * t)
P["Равная Земля"] = ee

def area_ratio(f, l, p, h=1e-6):
    x1, y1 = f(l + h, p); x0, y0 = f(l - h, p)
    x3, y3 = f(l, p + h); x2, y2 = f(l, p - h)
    J = ((x1 - x0) * (y3 - y2) - (x3 - x2) * (y1 - y0)) / (4 * h * h)
    return abs(J) / cos(p)

pts = [(radians(L), radians(F)) for L in (10, 60, 150) for F in (-75, -50, -20, 5, 30, 55, 80)]
print("%-34s %10s %10s %10s  %s" % ("проекция", "мин", "макс", "разброс", "вывод"))
for name, f in P.items():
    r = [area_ratio(f, l, p) for l, p in pts]
    spread = (max(r) - min(r)) / max(r)
    print("%-34s %10.5f %10.5f %10.2e  %s" % (name, min(r), max(r), spread, "равновеликая" if spread < 1e-4 else "НЕ равновеликая"))

print("\n— геометрия —")
x_eq, _ = moll(pi, 0); _, y_pole = moll(0, pi / 2)
print("Молльвейде: полуось x / полуось y =", x_eq / y_pole)
for name, f in (("Эккерт IV", e4), ("Вагнер VI", P["Вагнер VI"]), ("Эккерт III", P["Эккерт III"])):
    print("%s: длина полюсной линии / экватора = %.6f" % (name, f(pi, pi / 2 - 1e-9)[0] / f(pi, 0)[0]))
print("Каврайский VII / Вагнер VI по x (должно быть постоянно):", [round(P["Каврайский VII"](1, p)[0] / P["Вагнер VI"](1, p)[0], 9) for p in (0, 0.5, 1.2)], "√3/2 =", sqrt(3) / 2)

print("\n— обратные (страница) —")
def inv_moll(x, y):
    t = asin(y / sqrt(2)); return (pi * x / (2 * sqrt(2) * cos(t)), asin((2 * t + sin(2 * t)) / pi))
def inv_e4(x, y):
    t = asin(y / 2 * sqrt((4 + pi) / pi)); return (sqrt(pi * (4 + pi)) * x / (2 * (1 + cos(t))), asin((t + sin(t) * cos(t) + 2 * sin(t)) / (2 + pi / 2)))
def inv_e6(x, y):
    t = y * sqrt(2 + pi) / 2; return (x * sqrt(2 + pi) / (1 + cos(t)), asin((t + sin(t)) / (1 + pi / 2)))
def inv_cr(x, y):
    p = 3 * asin(y / sqrt(3 * pi)); return (x / (sqrt(3 / pi) * (2 * cos(2 * p / 3) - 1)), p)
def inv_e2(x, y):
    w = 2 - abs(y) / sqrt(2 * pi / 3); p = (1 if y >= 0 else -1) * asin((4 - w * w) / 3); return (x / (2 / sqrt(6 * pi) * w), p)
def inv_mtfpp(x, y):
    t = 3 * asin(y * sqrt(7) / 9); return (x * sqrt(7) / (sqrt(6) * (2 * cos(2 * t / 3) - 1)), asin(3 * sqrt(6) * sin(t) / 7))
for name, f, g in (("Молльвейде", moll, inv_moll), ("Эккерт IV", e4, inv_e4), ("Эккерт VI", e6, inv_e6), ("Крастер", P["Крастер"], inv_cr), ("Эккерт II", P["Эккерт II"], inv_e2), ("МТ плоскополюсная параболическая", mtfpp, inv_mtfpp)):
    err = max(max(abs(a - b) for a, b in zip(g(*f(l, p)), (l, p))) for l, p in pts)
    print("%-34s макс. ошибка обращения %.2e" % (name, err))

print("\n— сшивки —")
# Гуд: где совпадают длины параллелей синусоидальной и Молльвейде (x-масштаб)
fx = lambda p: cos(p) - 2 * sqrt(2) / pi * cos(th_moll(p))
lo, hi = 0.5, 1.0
for _ in range(80):
    mid = (lo + hi) / 2
    if fx(lo) * fx(mid) <= 0: hi = mid
    else: lo = mid
print("Гуд: φ*, где равны длины параллелей = %.4f° (страница: 40.7437° и 40°44′ = %.4f°)" % (degrees(lo), 40 + 44 / 60))
# Макбрайд S3: непрерывность y на 55°51′
pb = radians(55 + 51 / 60)
print("S3: синусоидальная y(φb) = %.6f; плоскополюсная y = %.6f" % (pb, c6 * mtfs_t(pb) - 0.069065))

print("\n— Естественная Земля I: y′ из y —")
print([round(3 * 0.015085, 6), round(7 * 0.044475, 6), round(9 * 0.028874, 6), round(11 * 0.005916, 6)], "страница: 0.045255, 0.311325, 0.259866, 0.065076")
