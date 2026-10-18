"""Две исходные параметризации (луч из серого в OKLab / луч из центра куба), без выравнивания и с Мозером.
Печатает меры искажения и рисует out/sravnenie2.png (4 круга).
python3 -I sravnenie2.py [R] [N]
"""
import os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iskazhenie as I  # noqa
import kub  # noqa
from otvet import boundary, ok2lin, lin2srgb  # noqa

R = int(sys.argv[1]) if len(sys.argv) > 1 else 300
N = int(sys.argv[2]) if len(sys.argv) > 2 else 360
okray = lambda d: boundary(d, I.K)  # noqa: E731
variants = [
    ("OKLab-луч", I.lambert_inv, okray),
    ("OKLab-луч+Мозер", I.Moser(N, 32, surf=okray), okray),
    ("куб-луч", I.lambert_inv, kub.surf),
    ("куб-луч+Мозер", I.Moser(N, 32, surf=kub.surf), kub.surf),
]
keys = None
imgs = []
for name, f, s in variants:
    r = I.measure(f, 200, 3, surf=s)
    if keys is None:
        keys = list(r)
        print("%-17s" % "" + "".join("%14s" % k for k in keys))
    print("%-17s" % name + "".join("%14.3f" % r[k] for k in keys), flush=True)
    yy, xx = np.mgrid[-R:R, -R:R] + 0.5
    X, Y = xx / R * 2, -yy / R * 2
    ok = X ** 2 + Y ** 2 < 4
    img = np.zeros((2 * R, 2 * R, 3))
    img[ok] = lin2srgb(ok2lin(s(f(X[ok], Y[ok]))))
    imgs.append(img)
gap = R // 10
canvas = np.zeros((2 * R, 4 * 2 * R + 3 * gap, 3))
for k, im in enumerate(imgs):
    canvas[:, k * (2 * R + gap):k * (2 * R + gap) + 2 * R] = im
here = os.path.dirname(os.path.abspath(__file__))
Image.fromarray((canvas * 255 + 0.5).astype(np.uint8)).save(os.path.join(here, "out", "sravnenie2.png"))
Image.fromarray((imgs[3] * 255 + 0.5).astype(np.uint8)).save(os.path.join(here, "moser-kub.png"))
