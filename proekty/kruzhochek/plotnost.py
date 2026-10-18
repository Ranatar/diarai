"""Плотность площади гаммы (OKLab) относительно площади сферы направлений: ρ(θ,φ), среднее 1.
Это ρ₁ для потока Мозера. Сохраняет out/rho.npy и печатает распределение.

python3 -I plotnost.py [NT] [K]
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ravnaya  # noqa


def density(NT=180, K=2.0):
    ravnaya.NT, ravnaya.NP = NT, 2 * NT
    th, ph, lab = ravnaya.surface(K)
    dA = ravnaya.area_element(lab)
    dth, dph = np.pi / NT, np.pi / NT
    sph = np.sin(th)[:, None] * dth * dph  # площадь клетки на единичной сфере
    rho = dA / sph
    rho = rho / (rho * sph).sum() * 4 * np.pi  # среднее по сфере = 1
    return th, ph, rho, lab


if __name__ == "__main__":
    NT = int(sys.argv[1]) if len(sys.argv) > 1 else 180
    K = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    th, ph, rho, lab = density(NT, K)
    q = np.percentile(rho, [0, 1, 5, 25, 50, 75, 95, 99, 100])
    print("ρ перцентили 0,1,5,25,50,75,95,99,100:", np.round(q, 3))
    print("по широте (среднее по долготе), каждые 15°:")
    for i in range(0, NT, NT // 12):
        print("  θ=%5.1f°  ρ=%.3f  max=%.3f" % (np.degrees(th[i]), rho[i].mean(), rho[i].max()))
    here = os.path.dirname(os.path.abspath(__file__))
    np.save(os.path.join(here, "out", "rho-%d.npy" % NT), rho)
