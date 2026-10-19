"""elf_poisk.py [папка] [--top N] [--min K] — где в архиве эльфийские тексты: для каждого текстового файла
(.md .txt .html .json .xml, кроме самого eldamo/) считает латинские слова от 4 букв, совпадающие с формами
Eldamo (квенья и синдарин всех периодов и нео-), и печатает файлы по числу РАЗНЫХ совпавших форм, с образцами.
Чтобы английский не тонул в ложных совпадениях (*man*, *sorn*…), слово засчитывается, только если оно
(а) с эльфийской диакритикой (áéíóúëâêîôû…), или (б) длиной от 6 и не входит в частотный английский/немецкий/
латинский словник самого архива (слово, которое встречается в >40 файлах, считается обычным языком).
Ложные совпадения всё равно будут: это сито, а не приговор — смотреть файл глазами.
2026-10-19 (автор: «найди в архиве ещё что-нибудь на эльфийском»)."""
import os, re, sys, glob, unicodedata, html
from collections import Counter, defaultdict

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
args = sys.argv[1:]
TOP, MIN = 40, 3
if "--top" in args:
    i = args.index("--top"); TOP = int(args[i + 1]); del args[i:i + 2]
if "--min" in args:
    i = args.index("--min"); MIN = int(args[i + 1]); del args[i:i + 2]
base = args[0] if args else os.path.join(root, "inbox")

LANGS = {"q", "nq", "mq", "eq", "s", "ns", "ns", "n", "en", "g", "eq", "t", "at", "p", "ilk", "dor", "nan", "tel"}
xml = open(os.path.join(root, "inbox", "eldamo", "src", "data", "eldamo-data.xml"), encoding="utf-8").read()
lex = defaultdict(set)
for m in re.finditer(r'<word\b([^>]*)>', xml):
    a = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
    v, l = a.get("v", ""), a.get("l", "")
    if l in LANGS and v:
        for w in re.split(r"[\s\-]+", v.lower()):
            w = w.strip("¹²³⁴⁵*?()[]!.,")
            if len(w) >= 4 and re.fullmatch(r"[a-zà-ÿ]+", w):
                lex[w].add(l)
for m in re.finditer(r'<ref\b[^>]*\bv="([^"]+)"', xml):
    for w in re.split(r"[\s\-]+", m.group(1).lower()):
        w = w.strip("¹²³⁴⁵*?()[]!.,")
        if len(w) >= 4 and re.fullmatch(r"[a-zà-ÿ]+", w):
            lex[w].add("ref")

DIA = set("áéíóúëäöüâêîôûñ")
files = []
for dp, dn, fn in os.walk(base):
    # 19.10: раньше выбрасывался весь eldamo/, а в нём полное зеркало Elvish Composition
    # Archive (39 сочинений) и elvish-essays: ложное «прочитан весь (11)». Теперь режем
    # только базу (src/data) и сборку (build).
    dn[:] = [d for d in dn if d not in ("node_modules", ".git", "hwph-xml", "build")
             and not (d == "data" and dp.endswith(os.path.join("eldamo", "src")))]
    for f in fn:
        if f.lower().endswith((".md", ".txt", ".html", ".htm", ".json", ".xml")):
            files.append(os.path.join(dp, f))

tok = re.compile(r"[A-Za-zÀ-ÿ]+")
docfreq = Counter()
per = {}
for p in files:
    try:
        t = open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        continue
    if p.endswith((".html", ".htm")):
        t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    ws = Counter(w.lower() for w in tok.findall(t))
    per[p] = ws
    docfreq.update(ws.keys())

rows = []
for p, ws in per.items():
    hits = {}
    for w, c in ws.items():
        if w not in lex:
            continue
        dia = any(ch in DIA for ch in w)
        if dia or (len(w) >= 6 and docfreq[w] <= 40):
            hits[w] = c
    if len(hits) >= MIN:
        rows.append((len(hits), sum(hits.values()), p, sorted(hits, key=lambda w: -hits[w])[:12]))
rows.sort(reverse=True)
for n, s, p, sample in rows[:TOP]:
    print("%4d форм %5d вх.  %s\n          %s" % (n, s, os.path.relpath(p, root), ", ".join(sample)))
print("файлов с ≥%d формами: %d (из %d)" % (MIN, len(rows), len(files)))
