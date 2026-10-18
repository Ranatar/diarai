"""Вытащить встроенные SVG из iass-spec.html и вывести сводку элементов второго (стан «Мо и тэль»).
python3 svg_razbor.py iass-spec.html out_dir"""
import sys, re, os, collections
import xml.etree.ElementTree as ET

html = open(sys.argv[1], encoding="utf-8").read()
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
svgs = re.findall(r"<svg.*?</svg>", html, re.S)
for i, s in enumerate(svgs):
    open(os.path.join(out, "plate%d.svg" % i), "w", encoding="utf-8").write(s)
print(len(svgs), "svg")
root = ET.fromstring(svgs[1])
ns = "{http://www.w3.org/2000/svg}"
cnt = collections.Counter(el.tag.replace(ns, "") for el in root.iter())
print(dict(cnt))
for el in root.iter():
    tag = el.tag.replace(ns, "")
    if tag in ("circle", "ellipse", "polygon", "path", "line", "text", "rect", "g", "use"):
        a = {k: v for k, v in el.attrib.items() if k in ("cx", "cy", "r", "rx", "ry", "points", "d", "x", "y", "x1", "y1", "x2", "y2", "fill", "stroke", "class", "transform", "href", "{http://www.w3.org/1999/xlink}href")}
        txt = (el.text or "").strip()
        print(tag, a, txt[:40])
