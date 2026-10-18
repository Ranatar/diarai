"""Уравнение Пуассона на единичной сфере, свой решатель (scipy нет).

Сетка широта-долгота с центрами клеток: θ_i = (i+½)h, φ_j = (j+½)h, h = π/N, по φ 2N точек.
По φ — БПФ (спектрально, m²), по θ — конечные объёмы:
  (1/(sinθ_i h²)) [ s_{i+½}(u_{i+1}-u_i) - s_{i-½}(u_i-u_{i-1}) ] - m²/sin²θ_i · u_i = f_i,
где s_{i±½} = sin θ на гранях клетки; на полюсах sin = 0, потока нет — граничных условий не нужно.
Для каждого m — трёхдиагональная система (прогонка, векторно по всем m).
m = 0 вырождено (константа); решается прямым интегрированием потока, среднее u = 0.
"""
import numpy as np


def grid(N):
    h = np.pi / N
    th = (np.arange(N) + 0.5) * h
    ph = (np.arange(2 * N) + 0.5) * h
    return th, ph, h


def thomas(a, b, c, d):
    """a — под, b — главная, c — над диагональю; все формы (n, M); решение по оси 0."""
    n = b.shape[0]
    cp = np.empty_like(d); dp = np.empty_like(d)
    cp[0] = c[0] / b[0]; dp[0] = d[0] / b[0]
    for i in range(1, n):
        den = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / den
        dp[i] = (d[i] - a[i] * dp[i - 1]) / den
    x = np.empty_like(d)
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


def poisson(f):
    """Решить Δu = f на сфере; f — (N, 2N). Среднее f по сфере вычитается (иначе решения нет)."""
    N = f.shape[0]
    th, ph, h = grid(N)
    s = np.sin(th)
    w = s / s.sum()
    f = f - (f.mean(1) * w).sum()  # среднее по площади = 0
    F = np.fft.rfft(f, axis=1)  # (N, M)
    M = F.shape[1]
    m = np.arange(M)
    sp = np.sin((np.arange(N + 1)) * h)  # sin на гранях, sp[0] = sp[N] = 0 (почти)
    sp[0] = sp[N] = 0.0
    U = np.zeros_like(F)
    # m >= 1: трёхдиагональная система
    a = (sp[:-1] / (s * h * h))[:, None] * np.ones((1, M - 1))
    c = (sp[1:] / (s * h * h))[:, None] * np.ones((1, M - 1))
    b = -(a + c) - (m[1:][None, :] ** 2) / (s[:, None] ** 2)
    U[:, 1:] = thomas(a.astype(complex), b.astype(complex), c.astype(complex), F[:, 1:])
    # m = 0: поток через грань i+½ равен интегралу f по шапке над ней
    g = F[:, 0].real  # (сумма по φ)
    flux = np.cumsum(g * s * h)  # = s_{i+½} (u_{i+1}-u_i)/h
    du = flux[:-1] * h / sp[1:-1]
    u0 = np.concatenate([[0.0], np.cumsum(du)])
    u0 -= (u0 * w).sum()
    U[:, 0] = u0
    return np.fft.irfft(U, n=2 * N, axis=1)


def laplacian(u):
    """Тот же дискретный оператор, для проверки невязки."""
    N = u.shape[0]
    th, ph, h = grid(N)
    s = np.sin(th)
    sp = np.sin(np.arange(N + 1) * h); sp[0] = sp[N] = 0.0
    up = np.vstack([u[:1], u, u[-1:]])
    lt = (sp[1:, None] * (up[2:] - up[1:-1]) - sp[:-1, None] * (up[1:-1] - up[:-2])) / (s[:, None] * h * h)
    m = np.fft.rfftfreq(2 * N, d=1.0 / (2 * N))
    lp = np.fft.irfft(-(m ** 2) * np.fft.rfft(u, axis=1), n=2 * N, axis=1) / s[:, None] ** 2
    return lt + lp


if __name__ == "__main__":
    for N in (45, 90, 180):
        th, ph, h = grid(N)
        T, P = np.meshgrid(th, ph, indexing="ij")
        tests = [
            ("Y10 cosθ, λ=-2", np.cos(T), -np.cos(T) / 2),
            ("Y20, λ=-6", 3 * np.cos(T) ** 2 - 1, -(3 * np.cos(T) ** 2 - 1) / 6),
            ("Y22, λ=-6", np.sin(T) ** 2 * np.cos(2 * P), -np.sin(T) ** 2 * np.cos(2 * P) / 6),
            ("Y31, λ=-12", (5 * np.cos(T) ** 2 - 1) * np.sin(T) * np.sin(P), -(5 * np.cos(T) ** 2 - 1) * np.sin(T) * np.sin(P) / 12),
        ]
        for name, f, exact in tests:
            u = poisson(f)
            err = np.abs(u - exact).max() / np.abs(exact).max()
            res = np.abs(laplacian(u) - f).max()
            print("N=%3d %-14s отн. ошибка %.2e   невязка %.1e" % (N, name, err, res))
