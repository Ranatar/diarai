"""«Куб + Мозер» в форме первого и последнего эскизов автора: два полушария (белое и чёрное) рядом.
Ламберт по каждому полушарию равновелик, так что выравнивание площади сохраняется: на обоих кругах
площадь ∝ площади поверхности гаммы в OKLab. Чёрное полушарие зеркально, как в otvet.py.
python3 -I dva.py out.png [R] [N]
"""
import os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moser  # noqa
import kub  # noqa
from otvet import ok2lin, lin2srgb  # noqa


def hemi_points(R, north):
    yy, xx = np.mgrid[-R:R, -R:R] + 0.5
    X, Y = xx / R * np.sqrt(2), -yy / R * np.sqrt(2)
    r2 = X ** 2 + Y ** 2
    ok = r2 < 2
    f = np.sqrt(np.clip(1 - r2 / 4, 0, None))
    dx, dy, dz = X * f, Y * f, 1 - r2 / 2
    if not north:
        dz, dx = -dz, -dx
    return np.stack([dx[ok], dy[ok], dz[ok]], 1), ok


if __name__ == "__main__":
    out = sys.argv[1]
    R = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    N = int(sys.argv[3]) if len(sys.argv) > 3 else 360
    rho, w = moser.fields(N, 0, kub.surf)
    gap = R // 8
    canvas = np.zeros((2 * R, 4 * R + gap, 3))
    for k, north in enumerate((True, False)):
        p, ok = hemi_points(R, north)
        d = moser.flow(p, rho, w, 32)
        img = np.zeros((2 * R, 2 * R, 3))
        img[ok] = lin2srgb(ok2lin(kub.surf(d)))
        canvas[:, k * (2 * R + gap):k * (2 * R + gap) + 2 * R] = img
    Image.fromarray((canvas * 255 + 0.5).astype(np.uint8)).save(out)
