"""Звёздна ли гамма sRGB в OKLab относительно серого L0 = 0,5 (с растяжением K)?
Для лучей по всей сфере направлений: мелкий шаг по t, число переходов «внутри/снаружи».
Если где-то переходов больше одного — бисекция в otvet.boundary там ненадёжна.
python3 -I zvyozdnost.py [NT]
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otvet import ok2lin, L0  # noqa

K = 2.0
NT = int(sys.argv[1]) if len(sys.argv) > 1 else 180
th = (np.arange(NT) + 0.5) / NT * np.pi
ph = (np.arange(2 * NT) + 0.5) / NT * np.pi
T, P = np.meshgrid(th, ph, indexing="ij")
d = np.stack([np.sin(T) * np.cos(P), np.sin(T) * np.sin(P), np.cos(T)], -1).reshape(-1, 3)
step = np.stack([d[:, 0] / K, d[:, 1] / K, d[:, 2]], 1)
ts = np.linspace(0, 1.0, 2001)
prev = np.ones(len(d), bool)
trans = np.zeros(len(d), int)
first_out = np.full(len(d), np.nan)
for t in ts[1:]:
    ab_l = step * t
    lab = np.stack([L0 + ab_l[:, 2], ab_l[:, 0], ab_l[:, 1]], 1)
    lin = ok2lin(lab)
    ins = np.all((lin >= -1e-9) & (lin <= 1 + 1e-9), 1)
    trans += ins != prev
    first_out = np.where(np.isnan(first_out) & ~ins, t, first_out)
    prev = ins
trans = trans.reshape(NT, 2 * NT)
bad = trans > 1
print("лучей: %d, с одним выходом: %d, с повторным входом: %d (%.2f%%)" % (
    trans.size, (trans == 1).sum(), bad.sum(), 100 * bad.mean()))
if bad.any():
    i, j = np.nonzero(bad)
    print("θ от %.1f° до %.1f°, φ от %.1f° до %.1f°" % (np.degrees(th[i].min()), np.degrees(th[i].max()),
                                                     np.degrees(ph[j].min()), np.degrees(ph[j].max())))
    k = np.argmax(trans)
    ii, jj = np.unravel_index(k, trans.shape)
    print("пример: θ=%.1f° φ=%.1f°, переходов %d" % (np.degrees(th[ii]), np.degrees(ph[jj]), trans[ii, jj]))
    # какой цвет на первой границе
    dd = d.reshape(NT, 2 * NT, 3)[ii, jj]
    t = first_out.reshape(NT, 2 * NT)[ii, jj]
    s = np.array([dd[0] / K, dd[1] / K, dd[2]]) * t
    print("  первый выход при t=%.3f, linRGB=%s" % (t, np.round(ok2lin(np.array([[L0 + s[2], s[0], s[1]]]))[0], 3)))
