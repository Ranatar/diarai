"""Прогнать все эскизы inbox/нян/*.html через run.js, сделать миниатюры и ленту по датам.

python3 -I vse.py  -> out/thumbs/*.png, out/spisok.tsv (дата, файл, размер, статус)
"""
import os, subprocess, sys, datetime
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "inbox", "нян")
OUT = os.path.join(HERE, "out")
TH = os.path.join(OUT, "thumbs")
os.makedirs(TH, exist_ok=True)

files = sorted((f for f in os.listdir(SRC) if f.endswith(".html")),
               key=lambda f: (os.path.getmtime(os.path.join(SRC, f)), f))
rows = []
for f in files:
    p = os.path.join(SRC, f)
    date = datetime.datetime.fromtimestamp(os.path.getmtime(p), datetime.timezone.utc).strftime("%Y-%m-%d")
    base = f[:-5]
    thumb = os.path.join(TH, base + ".png")
    if os.path.exists(thumb):
        rows.append((date, f, "", "кэш")); continue
    ppm = os.path.join(OUT, "tmp.ppm")
    try:
        r = subprocess.run(["node", "--max-old-space-size=1024", os.path.join(HERE, "run.js"), p, ppm],
                           capture_output=True, text=True, timeout=90)
        st = "ok" if r.returncode == 0 else "ошибка: " + (r.stderr.strip().splitlines() or ["?"])[-1][:80]
    except subprocess.TimeoutExpired:
        st = "таймаут"
    size = ""
    if st == "ok":
        try:
            im = Image.open(ppm); size = "%dx%d" % im.size
            im.thumbnail((256, 256), Image.LANCZOS); im.save(thumb)
        except Exception as e:
            st = "ошибка PIL: %s" % str(e)[:60]
        os.remove(ppm)
    rows.append((date, f, size, st))
    print(date, f, size, st, flush=True)

with open(os.path.join(OUT, "spisok.tsv"), "w") as fh:
    for row in rows:
        fh.write("\t".join(row) + "\n")
