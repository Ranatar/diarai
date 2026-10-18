"""Три равновеликих кружочка рядом, без округления до клеток сетки:
КР непрерывный (широта, потом долгота) | КР непрерывный (долгота, потом широта) | Мозер.
python3 -I sravnenie.py out.png [R] [N_мозер]
"""
import os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iskazhenie as I  # noqa
from otvet import boundary, ok2lin, lin2srgb  # noqa


def draw(fmap, R):
    yy, xx = np.mgrid[-R:R, -R:R] + 0.5
    X, Y = xx / R * 2, -yy / R * 2
    ok = X ** 2 + Y ** 2 < 4
    img = np.zeros((2 * R, 2 * R, 3))
    img[ok] = lin2srgb(ok2lin(boundary(fmap(X[ok], Y[ok]), I.K)))
    return img


if __name__ == "__main__":
    out = sys.argv[1]
    R = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    N = int(sys.argv[3]) if len(sys.argv) > 3 else 720
    kr = I.KR(); kr.blend = True
    imgs = [draw(kr.lat_first, R), draw(kr.lon_first, R), draw(I.Moser(N, 32), R)]
    gap = R // 10
    canvas = np.zeros((2 * R, 3 * 2 * R + 2 * gap, 3))
    for k, im in enumerate(imgs):
        canvas[:, k * (2 * R + gap):k * (2 * R + gap) + 2 * R] = im
        Image.fromarray((im * 255 + 0.5).astype(np.uint8)).save(out.rsplit(".", 1)[0] + "-%d.png" % k)
    Image.fromarray((canvas * 255 + 0.5).astype(np.uint8)).save(out)
