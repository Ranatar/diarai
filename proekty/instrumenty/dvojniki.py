"""dvojniki.py — одинаковые и почти одинаковые картинки в inbox под разными именами.

  ext/venv-pdf/bin/python -I proekty/instrumenty/dvojniki.py          — индекс (ext/tmp/dvojniki.npz) и группы двойников
  ext/venv-pdf/bin/python -I proekty/instrumenty/dvojniki.py ФАЙЛ     — ближайшие к одной картинке (5 лучших и все под порогом)
Подпись картинки — цветная миниатюра 16×16 (RGB, 768 чисел), центрированная и нормированная. Сходство —
корреляция, −1..1, нечувствительна к яркости и контрасту. «Двойник» — корреляция ≥ 0,95; для одной картинки
печатаются 5 ближайших (там же видны «родственники» — та же функция в другом окне).
Проверка: `complex_beauty/NE1cbXONtnY.jpg` и `complex_function_trinity.png` — одна функция в одном стиле,
но в разных окнах (корреляция 0,861; следующая картинка — 0,744). Первая версия (dHash 8×8) их не связала
и связала десятки посторонних тёмных картинок; средняя абсолютная разность дала 13,7 против 19,9 — без разрыва.
21.10, пробуждение 03:07: я «разгадал» NE1cbXONtnY.jpg как новую, а это была та же функция, что в иконе Троицы, разобранной мной 18.10.
chital.py ищет по имени и не может такое поймать.
Ограничение: зеркальные копии не ищет (`complex_function_2025-12-28T17-43-53.png` — икона Троицы, отражённая
слева направо, а корреляция всего 0,562). Проверка на зеркало — ext/tmp/zerkalo.py (сравнение тона)."""
import os, sys
import numpy as np
from PIL import Image

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
idx = os.path.join(root, "ext", "tmp", "dvojniki.npz")
EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp")
POROG = 0.95


def podpis(p):
    im = Image.open(p).convert("RGB").resize((16, 16), Image.BILINEAR)
    a = np.asarray(im, dtype=np.float32).reshape(-1)
    a = a - a.mean()
    return a / (np.linalg.norm(a) + 1e-9)


def postroit():
    paths, vecs = [], []
    for d, _, fs in os.walk(os.path.join(root, "inbox")):
        if "node_modules" in d:
            continue
        for f in sorted(fs):
            if f.lower().endswith(EXT):
                p = os.path.join(d, f)
                try:
                    vecs.append(podpis(p))
                    paths.append(os.path.relpath(p, root))
                except Exception:
                    pass
    V = np.stack(vecs)
    np.savez(idx, V=V, paths=np.array(paths))
    return paths, V


def zagruzit():
    if not os.path.exists(idx):
        return postroit()
    z = np.load(idx)
    return list(z["paths"]), z["V"]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        paths, V = zagruzit()
        v = podpis(sys.argv[1])
        cc = V @ v
        order = np.argsort(-cc)
        for k, i in enumerate(order):
            if k < 5 or cc[i] >= POROG:
                print("%.3f %s" % (cc[i], paths[i]))
            else:
                break
    else:
        paths, V = postroit()
        n = len(paths)
        used = np.zeros(n, bool)
        grupp = 0
        for i in range(n):
            if used[i]:
                continue
            cc = V[i + 1:] @ V[i]
            js = [i + 1 + j for j in np.nonzero(cc >= POROG)[0] if not used[i + 1 + j]]
            if js:
                grupp += 1
                print("== " + paths[i])
                for j in js:
                    used[j] = True
                    print("   %.3f %s" % (float(V[j] @ V[i]), paths[j]))
        print("картинок: %d; групп двойников: %d" % (n, grupp))
