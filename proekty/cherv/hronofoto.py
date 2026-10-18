"""Хронофотография червя в духе Марея: средние линии тела в несколько моментов
на одной картинке, плюс след головы. Читает frames.bin прогона Wormlisp.

    python3 hronofoto.py ext/wormlisp/runs/moi-1 proekty/cherv/moi-1.svg [кольца]

Формат frames.bin — из ext/wormlisp/src/io/frames.lisp (заголовок 64 байта,
кадры постоянного размера, little-endian). Узлы идут кольцами: кольцо за
кольцом, в кольце K узлов; средняя линия — центр каждого кольца.
"""
import json
import os
import struct
import sys


def read_frames(path):
    with open(path, "rb") as f:
        head = f.read(64)
        sig, ver, flags, n, m, q, size, count = struct.unpack("<IHHIIIIQ", head[:32])
        assert sig == 0x534D5257, "не frames.bin"
        data = f.read()
    count = len(data) // size
    frames = []
    for i in range(count):
        fr = data[i * size:(i + 1) * size]
        t = struct.unpack_from("<d", fr, 16)[0]
        xyz = struct.unpack_from("<%df" % (3 * n), fr, 32)
        frames.append((t, xyz))
    return n, m, q, frames


def centerline(xyz, n, rings):
    k = n // rings
    pts = []
    for r in range(rings):
        xs = xyz[3 * r * k:3 * (r + 1) * k:3]
        ys = xyz[3 * r * k + 1:3 * (r + 1) * k:3]
        pts.append((sum(xs) / k, sum(ys) / k))
    return pts


def main():
    run, out = sys.argv[1], sys.argv[2]
    n, m, q, frames = read_frames(os.path.join(run, "frames.bin"))
    rings = int(sys.argv[3]) if len(sys.argv) > 3 else None
    if rings is None:
        meta = json.load(open(os.path.join(run, "meta.json")))
        rings = meta.get("rings") or meta.get("n_rings") or 50
    lines = [(t, centerline(x, n, rings)) for t, x in frames]
    # моменты: каждые 0,5 с, начиная с 4-й (после разгона)
    opt = dict(a[2:].split("=") for a in sys.argv if a.startswith("--") and "=" in a)
    nxt, shag = float(opt.get("ot", 4.0)), float(opt.get("shag", 0.5))
    picks = []
    for t, l in lines:
        if t >= nxt - 1e-9:
            picks.append((t, l))
            nxt += shag
    if "--lesenka" in sys.argv:  # каждый момент ниже предыдущего, как у Марея на полосе
        step = float(os.environ.get("LESENKA_MM", "0.12"))
        picks = [(t, [(x, y - i * step) for x, y in l]) for i, (t, l) in enumerate(picks)]
        lines = [(t, l) for t, l in lines if False] or [(picks[0][0], picks[0][1][:1])]
    allp = [p for _, l in lines for p in l] + [p for _, l in picks for p in l]
    x0, x1 = min(p[0] for p in allp), max(p[0] for p in allp)
    y0, y1 = min(p[1] for p in allp), max(p[1] for p in allp)
    pad = 0.1
    W = 900
    sc = W / (x1 - x0 + 2 * pad)
    H = int((y1 - y0 + 2 * pad) * sc) + 40
    tx = lambda x: (x - x0 + pad) * sc
    ty = lambda y: H - 30 - (y - y0 + pad) * sc
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
           'style="background:#fbfaf6">' % (W, H)]
    head = " ".join("%.1f,%.1f" % (tx(l[0][0]), ty(l[0][1])) for _, l in lines)
    svg.append('<polyline points="%s" fill="none" stroke="#c9b48a" stroke-width="1"/>' % head)
    for i, (t, l) in enumerate(picks):
        a = 0.25 + 0.75 * i / max(1, len(picks) - 1)
        pts = " ".join("%.1f,%.1f" % (tx(x), ty(y)) for x, y in l)
        svg.append('<polyline points="%s" fill="none" stroke="#2b3a42" stroke-opacity="%.2f" '
                   'stroke-width="5" stroke-linecap="round"/>' % (pts, a))
    svg.append('<text x="10" y="%d" font-family="serif" font-size="13" fill="#555">'
               '%s: средняя линия каждые %s с, с %.1f по %.1f с; '
               '1 мм = %.0f px</text>' % (H - 10, os.path.basename(run.rstrip("/")), shag,
                                         picks[0][0] if picks else 0,
                                         picks[-1][0] if picks else 0, sc))
    svg.append("</svg>")
    open(out, "w").write("\n".join(svg))
    try:  # PNG рядом — чтобы посмотреть самому (PIL есть в системе)
        from PIL import Image, ImageDraw
        img = Image.new("RGB", (W, H), (251, 250, 246))
        d = ImageDraw.Draw(img)
        d.line([(tx(l[0][0]), ty(l[0][1])) for _, l in lines], fill=(201, 180, 138), width=1)
        for i, (t, l) in enumerate(picks):
            a = 0.25 + 0.75 * i / max(1, len(picks) - 1)
            c = tuple(int(251 - (251 - v) * a) for v in (43, 58, 66))
            d.line([(tx(x), ty(y)) for x, y in l], fill=c, width=5, joint="curve")
            hx, hy = tx(l[0][0]), ty(l[0][1])
            d.ellipse([hx - 3, hy - 3, hx + 3, hy + 3], fill=(170, 60, 50))
        img.save(out.rsplit(".", 1)[0] + ".png")
    except ImportError:
        pass
    hx = [l[0] for _, l in lines]
    print("кадров", len(frames), "узлов", n, "колец", rings, "мышц", m, "нейронов", q)
    print("голова: от (%.3f, %.3f) до (%.3f, %.3f) мм" % (hx[0][0], hx[0][1], hx[-1][0], hx[-1][1]))


if __name__ == "__main__":
    main()
