"""test10_izvlech.py — перепись к тесту 10: места у генератора, где «§N» (N ≤ 693) стоит рядом (±300) с названием
«Философских исследований». Без philosphaira, hwph-xml, «исихаста»; номера внутри диапазонов пропускаются.
Запуск: python3 -I test10_izvlech.py inbox > test10-perepis.tsv   (контекст ±200 — в столбце 5)"""
import sys, os, re, html

root = sys.argv[1]
ZNAM = set("1 2 7 11 18 19 23 43 65 66 67 68 109 115 116 118 119 123 124 133 199 201 202 241 243 258 265 293 "
           "304 309 329 373".split())
KEY = re.compile(r"Исследовани|ФИ\b|\bPU\b|\bPI\b|Untersuchungen|Philosophical Investigations")
# §, §§, или «ФИ 43» / «PU 43» без знака
NUM = re.compile(r"(?:§§?\s?|(?:ФИ|PU|PI),?\s(?:§§?\s?)?)(\d{1,3})(?!\d|\.\d|\s?[–\-—]\s?\d)")

def text_of(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    if path.endswith((".html", ".htm", ".xml")):
        raw = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", raw)
        raw = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    if path.endswith(".json"):
        raw = raw.replace("\\n", " ").replace('\\"', '"')
    return re.sub(r"\s+", " ", raw)

print("id\tфайл\tномер\tзнам\tконтекст\tвердикт\tкомментарий")
seen, k = set(), 0
for dp, dn, fn in os.walk(root):
    if "philosphaira" in dp or "hwph-xml" in dp or "wittgenstein-hesychasm" in dp:
        continue
    for f in sorted(fn):
        if not f.endswith((".html", ".htm", ".md", ".txt", ".json", ".mjs", ".js")):
            continue
        p = os.path.join(dp, f)
        t = text_of(p)
        for m in NUM.finditer(t):
            n = m.group(1)
            if not 1 <= int(n) <= 693:
                continue
            if re.search(r"\d\s?[–\-—]\s?$", t[max(0, m.start() - 3):m.start(1)]):
                continue  # конец диапазона
            if not KEY.search(t[max(0, m.start() - 300): m.end() + 300]):
                continue
            ctx = t[max(0, m.start() - 200): m.end() + 200].replace("\t", " ")
            key = (n, re.sub(r"\W", "", ctx)[120:260])
            if key in seen:
                continue
            seen.add(key)
            print("%d\t%s\t%s\t%d\t%s\t\t" % (k, os.path.relpath(p, root), n, n in ZNAM, ctx))
            k += 1
