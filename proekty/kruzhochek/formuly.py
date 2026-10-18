"""Какие проекции и цветовые модели используют эскизы (по живым, не закомментированным строкам).

python3 -I formuly.py  -> out/formuly.tsv и сводка по годам
Сигнатуры — характерные куски формул; это грубый поиск, не разбор кода.
"""
import os, re, collections, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "inbox", "нян")

SIG = {
    "Ламберт азимут.": r"sqrt\(\s*2\s*/\s*\(\s*1\s*-",
    "Бонн": r"1/Math\.tan\(phi1\)\s*\+\s*phi1\s*-\s*phi",
    "поликоническая": r"lambda\*Math\.sin\(phi\)",
    "Молльвейде/итерация θ": r"Math\.sin\(2\*th|2\*theta",
    "Меркатор": r"Math\.log\(Math\.tan",
    "стереографическая": r"/\s*\(\s*1\s*-\s*z\d\s*\)",
    "октаэдр |x|+|y|+|z|": r"Math\.abs\(x\d\)\s*\+\s*Math\.abs\(y\d\)",
    "atan2 (долгота)": r"Math\.atan2",
    "HSL/HSV (хрома)": r"M\s*-\s*m\b|Math\.max\(R,\s*G,\s*B\)",
    "RGB-куб (255-2*n)": r"255\s*-\s*2\*n",
}


def live(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return "\n".join(l.split("//")[0] for l in text.splitlines())


rows = []
for f in os.listdir(SRC):
    if not f.endswith(".html"):
        continue
    p = os.path.join(SRC, f)
    code = live(open(p, encoding="utf-8", errors="replace").read())
    year = datetime.datetime.fromtimestamp(os.path.getmtime(p), datetime.timezone.utc).strftime("%Y-%m-%d")
    hits = [k for k, rx in SIG.items() if re.search(rx, code)]
    rows.append((year, f, hits))
rows.sort()
with open(os.path.join(HERE, "out", "formuly.tsv"), "w") as fh:
    for d, f, h in rows:
        fh.write("%s\t%s\t%s\n" % (d, f, ", ".join(h)))

by = collections.defaultdict(collections.Counter)
tot = collections.Counter()
for d, f, h in rows:
    y = d[:4]
    tot[y] += 1
    for k in h:
        by[k][y] += 1
years = sorted(tot)
print("%-24s" % "", *("%5s" % y for y in years))
print("%-24s" % "всего", *("%5d" % tot[y] for y in years))
for k in SIG:
    print("%-24s" % k, *("%5d" % by[k][y] for y in years))
