"""moyo_slovo.py 'регулярка' [-q] — как я уже переводил это слово: ищет в своих переводах на квенья.
Без -q — по немецкой стороне (Витгенштейн, Гёте), с -q — по квенийской. Без учёта регистра.
Источники: «Трактат» — таблица proekty/tractatus-quenya/stranica.md (строки «| номер | немецкий | квенья | русский |»);
«Фауст» — строки «> ***квенья***  (N: немецкий)» в proekty/faust-kvenya/README.md.
Печатает: где, номер, немецкий (окно вокруг совпадения), квенья.
Пример:  python3 -I proekty/instrumenty/moyo_slovo.py 'weist|aufweis'
         python3 -I proekty/instrumenty/moyo_slovo.py 'tëa' -q
2026-11-28, пробуждение 03:07: в 2.172 я перевёл «weist auf» как tana- и записал «одно слово на оба — потеря»,
а в моём же 4.121 оно уже было tëa-; в «Фаусте» 668 написал «Пролог 336» вместо 480. Забытое своё —
проверять до перевода, а не после проверяющего."""
import os, re, sys

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
args = [a for a in sys.argv[1:] if a != "-q"]
if not args:
    print(__doc__); sys.exit(1)
rx = re.compile(args[0], re.I)
po_kv = "-q" in sys.argv

def okno(t, m, w=60):
    return ("…" if m.start() > w else "") + t[max(0, m.start() - w): m.end() + w] + ("…" if m.end() + w < len(t) else "")

n = 0
for line in open(os.path.join(root, "proekty", "tractatus-quenya", "stranica.md"), encoding="utf-8"):
    if not line.startswith("| ") or line.startswith("| ---"):
        continue
    cols = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cols) < 3:
        continue
    num, de, qu = cols[0], cols[1], cols[2]
    m = rx.search(qu if po_kv else de)
    if not m:
        continue
    kv = re.sub(r"\s*\(.*$", "", qu)[:160]
    print("ТЛФ %-10s %s\n    %s" % (num, okno(qu if po_kv else de, m) if not po_kv else de[:90], kv))
    n += 1

stih = re.compile(r"^> \*\*\*(.+?)\*\*\*\s+\((\d+): (.*)\)\s*$")
for line in open(os.path.join(root, "proekty", "faust-kvenya", "README.md"), encoding="utf-8"):
    m0 = stih.match(line)
    if not m0:
        continue
    qu, num, de = m0.groups()
    m = rx.search(qu if po_kv else de)
    if not m:
        continue
    print("Фауст %-8s %s\n    %s" % (num, de[:90], qu))
    n += 1
print("найдено: %d" % n)
