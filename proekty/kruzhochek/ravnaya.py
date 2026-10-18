"""Кружочек, равновеликий для глаза: равные площади круга = равные площади поверхности гаммы sRGB в OKLab.

Форма — как у первого эскиза автора (Kruzhochek1_1): вся сфера в один круг Ламберта, белое в центре, чёрное по краю.
Построение:
 1. Поверхность гаммы параметризуется направлением (θ от белого полюса, φ — долгота): луч из серого в OKLab
    до границы (otvet.boundary). Это лишь исходный порядок точек.
 2. Элемент площади поверхности в метрике OKLab: |P_θ × P_φ| dθ dφ (конечные разности).
 3. Перестановка Кнёте — Розенблатта: θ' выбирается так, чтобы доля сферы над θ' равнялась доле площади гаммы
    над θ; внутри каждой «широты» φ' так же выравнивается по условной доле. Отображение сфера -> гамма
    становится равновеликим (с точностью сетки).
 4. Сфера -> круг азимутальной равновеликой Ламберта (тоже сохраняет площадь).
Итог: площадь на круге пропорциональна площади в OKLab. Формы искажены сильно — это плата.

python3 -I ravnaya.py out.png [R] [K]
"""
import os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otvet import boundary, ok2lin, lin2srgb  # noqa

NT, NP = 720, 1440  # сетка по θ и φ


def surface(K):
    th = (np.arange(NT) + 0.5) / NT * np.pi
    ph = (np.arange(NP) + 0.5) / NP * 2 * np.pi
    T, P = np.meshgrid(th, ph, indexing="ij")
    d = np.stack([np.sin(T) * np.cos(P), np.sin(T) * np.sin(P), np.cos(T)], -1).reshape(-1, 3)
    lab = boundary(d, K).reshape(NT, NP, 3)  # (L, a, b)
    return th, ph, lab


def area_element(lab):
    dT = np.gradient(lab, axis=0)
    dP = (np.roll(lab, -1, 1) - np.roll(lab, 1, 1)) / 2  # φ замкнута
    return np.linalg.norm(np.cross(dT, dP), axis=-1)  # площадь клетки сетки в OKLab


def build(K=2.0):
    th, ph, lab = surface(K)
    dA = area_element(lab)
    row = dA.sum(1)
    Frow = np.concatenate([[0], np.cumsum(row)]) / row.sum()  # доля площади над границей ряда
    Fcol = np.concatenate([np.zeros((NT, 1)), np.cumsum(dA, 1)], 1) / row[:, None]
    return th, ph, lab, Frow, Fcol, dA


def render(R, K=2.0):
    th, ph, lab, Frow, Fcol, dA = build(K)
    yy, xx = np.mgrid[-R:R, -R:R] + 0.5
    X, Y = xx / R * 2, -yy / R * 2  # вся сфера -> круг радиуса 2
    rho2 = X ** 2 + Y ** 2
    ok = rho2 < 4
    # обратный Ламберт, центр — северный полюс (белое)
    cos_t = 1 - rho2[ok] / 2
    u = (1 - cos_t) / 2  # доля сферы над θ' (0..1)
    v = (np.arctan2(Y[ok], X[ok]) % (2 * np.pi)) / (2 * np.pi)
    # θ: обратить Frow (по границам рядов), дробный номер ряда
    edges = np.arange(NT + 1)
    ti = np.interp(u, Frow, edges)
    i = np.clip(ti.astype(int), 0, NT - 1)
    # φ: обратить условную долю в ряду i
    pj = np.empty_like(v)
    for r in np.unique(i):
        m = i == r
        pj[m] = np.interp(v[m], Fcol[r], np.arange(NP + 1))
    j = np.clip(pj.astype(int), 0, NP - 1)
    img = np.zeros((2 * R, 2 * R, 3))
    img[ok] = lin2srgb(ok2lin(lab[i, j]))
    return img, (th, ph, lab, Frow, Fcol, dA)


if __name__ == "__main__":
    out = sys.argv[1]
    R = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    K = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
    img, (th, ph, lab, Frow, Fcol, dA) = render(R, K)
    Image.fromarray((img * 255 + 0.5).astype(np.uint8)).save(out)
    tot = dA.sum()
    L = lab[..., 0]
    print("площадь гаммы в OKLab: %.4f" % tot)
    for lo, hi in ((0, .25), (.25, .5), (.5, .75), (.75, 1.01)):
        m = (L >= lo) & (L < hi)
        print("  L в [%.2f, %.2f): %.1f%% площади" % (lo, hi, 100 * dA[m].sum() / tot))
