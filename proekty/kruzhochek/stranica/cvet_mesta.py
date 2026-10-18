"""cvet_mesta.py — цвет точки Земли в цветовом теле «Кружочка» (RGB-куб, белое — север, красный — λ = 0, kub.cube_point),
то есть какого цвета место на странице «Кружочек через атлас» при аспекте «белое — на север»."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import kub  # noqa

MESTA = {"Самара": (50.15, 53.20), "Саратов": (46.03, 51.53), "Оксфорд": (-1.26, 51.75), "Вена": (16.37, 48.21),
         "Кембридж": (0.12, 52.21), "Иона (остров)": (-6.41, 56.33), "Северный полюс": (0, 90), "Южный полюс": (0, -90)}
for name, (lon, lat) in MESTA.items():
    l, p = np.radians(lon), np.radians(lat)
    d = np.array([[np.cos(p) * np.cos(l), np.cos(p) * np.sin(l), np.sin(p)]])
    c = kub.cube_point(d)[0]
    print("%-16s %7.2f %6.2f  →  #%02x%02x%02x" % (name, lon, lat, *[int(round(255 * v)) for v in c]))
