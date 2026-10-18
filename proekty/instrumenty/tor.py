"""Проверка места из inbox/cartesian-product-part2.md («Окружность × Окружность»):
гауссова кривизна тора в R^3 численно (квадратичные формы, конечные разности) и метрика произведения в R^4."""
import numpy as np

R, r, h = 2.0, 1.0, 1e-4


def X(u, v):
    return np.array([(R + r * np.cos(v)) * np.cos(u), (R + r * np.cos(v)) * np.sin(u), r * np.sin(v)])


def K(u, v):
    Xu = (X(u + h, v) - X(u - h, v)) / (2 * h)
    Xv = (X(u, v + h) - X(u, v - h)) / (2 * h)
    Xuu = (X(u + h, v) - 2 * X(u, v) + X(u - h, v)) / h ** 2
    Xvv = (X(u, v + h) - 2 * X(u, v) + X(u, v - h)) / h ** 2
    Xuv = (X(u + h, v + h) - X(u + h, v - h) - X(u - h, v + h) + X(u - h, v - h)) / (4 * h * h)
    n = np.cross(Xu, Xv); n /= np.linalg.norm(n)
    E, F, G = Xu @ Xu, Xu @ Xv, Xv @ Xv
    L, M, N = Xuu @ n, Xuv @ n, Xvv @ n
    return (L * N - M * M) / (E * G - F * F), E, G


for v, name in ((0.0, "v=0"), (np.pi, "v=π")):
    k, E, G = K(0.3, v)
    print("%s точка %s  |X|=%.2f  K=%.4f  формула cos v/(r(R+r cos v))=%.4f  E=%.3f G=%.3f"
          % (name, np.round(X(0.0, v), 2), np.linalg.norm(X(0.0, v)[:2]), k,
             np.cos(v) / (r * (R + r * np.cos(v))), E, G))

# произведение окружностей в R^4: метрика
r1, r2 = 2.0, 1.0
Y = lambda a, b: np.array([r1 * np.cos(a), r1 * np.sin(a), r2 * np.cos(b), r2 * np.sin(b)])
for a, b in ((0.1, 0.2), (1.5, 2.9)):
    Ya = (Y(a + h, b) - Y(a - h, b)) / (2 * h)
    Yb = (Y(a, b + h) - Y(a, b - h)) / (2 * h)
    print("R^4: E=%.4f F=%.4f G=%.4f (постоянны => K=0, тор плоский)" % (Ya @ Ya, Ya @ Yb, Yb @ Yb))
