"""Равновеликий кружочек третьим способом: поток Мозера (1965) вместо перестановки Кнёте — Розенблатта.

Даны две плотности на сфере направлений: ρ₀ = 1 (равномерная — то, что даёт Ламберт на круге)
и ρ₁ = ρ (площадь гаммы в OKLab на единицу площади сферы, среднее 1; plotnost.py).
Ищется отображение g сферы на себя, переносящее ρ₀ в ρ₁. Приём Мозера:
  ρ_t = (1-t) + t·ρ,   Δu = 1 - ρ,   v_t = ∇u / ρ_t.
Тогда ∂ρ_t/∂t + div(ρ_t v_t) = (ρ - 1) + Δu = 0 — уравнение неразрывности, и поток v_t
за время 0→1 переносит равномерную меру в ρ. Каждый пиксель: обратный Ламберт -> точка сферы ->
поток (RK4) -> направление -> луч из серого в OKLab до границы гаммы -> цвет.
Поле — градиент, без вращения: вихрю взяться неоткуда. Швов нет, если ρ непрерывна... а она нет
(рёбра куба), так что посмотрим.

python3 -I moser.py out.png [R] [N] [шагов] [--kub]
  --kub: исходная параметризация — луч из центра RGB-куба (kub.py) вместо луча из серого в OKLab
"""
import os, sys, time
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfera import poisson, grid  # noqa
from plotnost import density  # noqa
from otvet import boundary, ok2lin, lin2srgb  # noqa

K = 2.0


def okray(d):
    """Исходная параметризация 1: луч из серого в OKLab (растяжение K) до границы гаммы."""
    return boundary(d, K)


def density_of(surf, N):
    """ρ = площадь поверхности surf(d) в OKLab на единицу площади сферы, среднее 1; сетка sfera.grid(N)."""
    th, ph, h = grid(N)
    T, P = np.meshgrid(th, ph, indexing="ij")
    d = np.stack([np.sin(T) * np.cos(P), np.sin(T) * np.sin(P), np.cos(T)], -1).reshape(-1, 3)
    lab = surf(d).reshape(N, 2 * N, 3)
    dT = np.gradient(lab, axis=0)
    dP = (np.roll(lab, -1, 1) - np.roll(lab, 1, 1)) / 2
    dA = np.linalg.norm(np.cross(dT, dP), axis=-1)
    sa = np.sin(th)[:, None] * h * h
    rho = dA / sa
    return th, ph, rho / (rho * sa).sum() * 4 * np.pi


def fields(N, smooth=0, surf=None):
    if surf is None:
        th, ph, rho, _ = density(N, K)
    else:
        th, ph, rho = density_of(surf, N)
    if smooth:
        rho = smooth_rho(rho, smooth)
    u = poisson(1.0 - rho)
    _, _, h = grid(N)
    u_t = np.gradient(u, h, axis=0)
    m = np.fft.rfftfreq(2 * N, d=1.0 / (2 * N))
    u_p = np.fft.irfft(1j * m * np.fft.rfft(u, axis=1), n=2 * N, axis=1)
    T, P = np.meshgrid(th, ph, indexing="ij")
    e_t = np.stack([np.cos(T) * np.cos(P), np.cos(T) * np.sin(P), -np.sin(T)], -1)
    e_p = np.stack([-np.sin(P), np.cos(P), np.zeros_like(P)], -1)
    w = u_t[..., None] * e_t + (u_p / np.sin(T))[..., None] * e_p  # ∇u в R³, касательный
    return rho, w


def smooth_rho(rho, k):
    """Сглаживание (для опыта): усреднение по φ и θ скользящим окном, масса сохраняется приближённо."""
    N = rho.shape[0]
    th, _, _ = grid(N)
    s = np.sin(th)[:, None]
    m = rho * s
    for _ in range(k):
        m = (np.roll(m, 1, 1) + 2 * m + np.roll(m, -1, 1)) / 4
        mp = np.vstack([m[:1], m, m[-1:]])
        m = (mp[:-2] + 2 * mp[1:-1] + mp[2:]) / 4
    r = m / s
    return r / (r * s).sum() * s.sum()


def sample(F, p, N):
    """Билинейная интерполяция поля F (N,2N,...) в точках p (n,3) единичной сферы."""
    h = np.pi / N
    th = np.arccos(np.clip(p[:, 2], -1, 1))
    ph = np.arctan2(p[:, 1], p[:, 0]) % (2 * np.pi)
    fi = np.clip(th / h - 0.5, 0, N - 1 - 1e-9)
    fj = ph / h - 0.5
    i0 = np.floor(fi).astype(int); a = fi - i0
    j0 = np.floor(fj).astype(int); b = fj - j0
    i1 = np.minimum(i0 + 1, N - 1)
    j0 %= 2 * N; j1 = (j0 + 1) % (2 * N)
    if F.ndim == 3:
        a = a[:, None]; b = b[:, None]
    return ((1 - a) * (1 - b) * F[i0, j0] + (1 - a) * b * F[i0, j1]
            + a * (1 - b) * F[i1, j0] + a * b * F[i1, j1])


def flow(p, rho, w, steps):
    N = rho.shape[0]

    def vel(q, t):
        r = (1 - t) + t * sample(rho, q, N)
        v = sample(w, q, N) / r[:, None]
        return v - (v * q).sum(1, keepdims=True) * q  # убрать нормальную составляющую

    dt = 1.0 / steps
    for k in range(steps):
        t = k * dt
        k1 = vel(p, t)
        k2 = vel(p + dt / 2 * k1, t + dt / 2)
        k3 = vel(p + dt / 2 * k2, t + dt / 2)
        k4 = vel(p + dt * k3, t + dt)
        p = p + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        p /= np.linalg.norm(p, axis=1, keepdims=True)
    return p


def disk_points(R):
    yy, xx = np.mgrid[-R:R, -R:R] + 0.5
    X, Y = xx / R * 2, -yy / R * 2
    rho2 = X ** 2 + Y ** 2
    ok = rho2 < 4
    f = np.sqrt(np.clip(1 - rho2 / 4, 0, None))
    p = np.stack([(X * f)[ok], (Y * f)[ok], (1 - rho2 / 2)[ok]], 1)  # обратный Ламберт, центр — белое
    return p, ok


def render(R, N=180, steps=32, smooth=0, surf=None):
    rho, w = fields(N, smooth, surf)
    p, ok = disk_points(R)
    d = flow(p, rho, w, steps)
    lab = (surf or okray)(d)
    img = np.zeros((2 * R, 2 * R, 3))
    img[ok] = lin2srgb(ok2lin(lab))
    return img, ok, d


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = args[0]
    R = int(args[1]) if len(args) > 1 else 400
    N = int(args[2]) if len(args) > 2 else 180
    steps = int(args[3]) if len(args) > 3 else 32
    t0 = time.time()
    surf = None
    if "--kub" in sys.argv:
        import kub
        surf = kub.surf
    img, ok, d = render(R, N, steps, surf=surf)
    Image.fromarray((img * 255 + 0.5).astype(np.uint8)).save(out)
    np.save(out.rsplit(".", 1)[0] + "-d.npy", d.astype(np.float32))
    print("готово за %.1f с" % (time.time() - t0))
