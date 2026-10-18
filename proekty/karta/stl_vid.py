"""stl_vid.py out.png файл.stl [файл.stl …] — посмотреть ASCII-STL: три вида на каждую модель
(спереди-сверху, сбоку, сверху), плоская заливка по нормали, алгоритм художника. Печатает число граней и габариты."""
import sys, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def load(p):
    t = open(p, encoding="utf-8", errors="replace").read()
    v = np.array(re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", t), dtype=float)
    return v.reshape(-1, 3, 3)

def rot(ax, ay):
    cx, sx, cy, sy = np.cos(ax), np.sin(ax), np.cos(ay), np.sin(ay)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    return Rx @ Ry

def vid(T, ax, ay, S=320):
    c = T.reshape(-1, 3)
    T = (T - (c.min(0) + c.max(0)) / 2) @ rot(ax, ay).T
    r = np.abs(T.reshape(-1, 3)[:, :2]).max() or 1
    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    svet = np.array([0.3, 0.5, 0.8]); svet /= np.linalg.norm(svet)
    sh = np.abs(n @ svet)  # нормали в STL бывают перевёрнуты — берём модуль
    im = Image.new("RGB", (S, S), "white")
    d = ImageDraw.Draw(im)
    for k in np.argsort(T[:, :, 2].mean(1)):  # от дальних к ближним (z к зрителю растёт)
        pts = [(S / 2 + 0.45 * S * x / r, S / 2 - 0.45 * S * y / r) for x, y, _ in T[k]]
        g = int(60 + 180 * sh[k])
        d.polygon(pts, fill=(g, int(g * 0.9), int(g * 0.75)))
    return im

out, files = sys.argv[1], sys.argv[2:]
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
except OSError:
    font = None
S = 320
sheet = Image.new("RGB", (3 * S, len(files) * (S + 20)), "white")
for i, f in enumerate(files):
    T = load(f)
    c = T.reshape(-1, 3)
    print("%s: граней %d, габариты %s" % (f, len(T), np.round(c.max(0) - c.min(0), 2)))
    for j, (ax, ay) in enumerate([(-0.6, 0.5), (0, np.pi / 2), (-np.pi / 2, 0)]):
        sheet.paste(vid(T, ax, ay, S), (j * S, i * (S + 20) + 20))
    ImageDraw.Draw(sheet).text((4, i * (S + 20) + 3), f.split("/")[-1] + "  (%d граней)" % len(T), fill="black", font=font)
sheet.save(out)
print(out)
