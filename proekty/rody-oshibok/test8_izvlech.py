"""test8_izvlech.py — места в inbox, где стоит номер «Трактата» (есть в tlp.json) и рядом (±400 знаков)
Витгенштейн / Трактат / Tractatus / TLP. Печатает TSV: файл, номер, знаменит(1/0), контекст ±160.
Запуск: python3 -I test8_izvlech.py inbox ext/tractatus/tlp.json > test8-mesta.tsv"""
import sys, os, re, json, html

root, tlp = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
ZNAM = set("1 1.1 2.1 2.12 3.203 4.0031 4.01 4.022 4.1212 4.112 4.116 5.6 5.61 5.62 5.63 5.632 5.641 "
           "6.371 6.4311 6.432 6.44 6.45 6.52 6.521 6.522 6.53 6.54 7".split())
KEY = re.compile(r"Витгенштейн|Wittgenstein|Трактат|Tractatus|TLP|Логико-философск", re.I)
NUM = re.compile(r"(?<![\d.,/:\-])([1-7]\.\d{1,5})(?![\d,]|\.\d)")

def text_of(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    if path.endswith((".html", ".htm", ".svg", ".xml")):
        raw = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", raw)
        raw = re.sub(r"<[^>]+>", " ", raw)
        raw = html.unescape(raw)
    if path.endswith(".json"):
        raw = raw.replace("\\n", " ").replace('\\"', '"')
    return re.sub(r"\s+", " ", raw)

seen = set()
print("файл\tномер\tзнам\tконтекст")
for dp, dn, fn in os.walk(root):
    for f in sorted(fn):
        if not f.endswith((".html", ".htm", ".md", ".txt", ".json", ".mjs", ".js", ".xml")):
            continue
        p = os.path.join(dp, f)
        try:
            t = text_of(p)
        except Exception:
            continue
        for m in NUM.finditer(t):
            n = m.group(1)
            if n not in tlp:
                continue
            a, b = max(0, m.start() - 400), m.end() + 400
            if not KEY.search(t[a:b]):
                continue
            ctx = t[max(0, m.start() - 160): m.end() + 160].replace("\t", " ")
            k = (n, re.sub(r"\W", "", ctx)[100:220])
            if k in seen:
                continue
            seen.add(k)
            print("%s\t%s\t%d\t%s" % (os.path.relpath(p, root), n, n in ZNAM, ctx))
