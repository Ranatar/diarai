"""[27.11: помечает «⚠УСТАРЕЛО→ лучше»; если слова нет — ищет в заметках Eldamo.] eldamo_slovo.py слово [язык] — найти в inbox/eldamo/src/data/eldamo-data.xml словарные статьи <word v="…">,
чьё v начинается со «слово» (без учёта регистра и диакритики), и напечатать язык, v, gloss и первые cite.
2026-10-18. Нужен для разбора имён (например, «Ránatar Maivandion»).
28.11: разбор через ElementTree; ссылки и «устарело» — только прямые потомки статьи; у нкв. без своих ссылок — «основа: …»
(вложенное исходное слово). До 28.11 третья колонка цепляла ссылки соседей (nq ehten ← «ehtar (Ety/EK)»)."""
import re, sys, unicodedata, os

def bare(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
path = os.path.join(root, "inbox", "eldamo", "src", "data", "eldamo-data.xml")
q = bare(sys.argv[1])
lang = sys.argv[2] if len(sys.argv) > 2 else None
text = open(path, encoding="utf-8").read()
# 28.11: разбор настоящим XML-парсером. Регулярками (до 28.11) граница статьи бралась «до первого вложенного <word>»,
# и у статей, где вложенные слова стоят раньше своих <ref>/<deprecated>, ссылки пропадали (q lanya-²), а раньше —
# брались из соседей (nq ehten получал «ehtar (Ety/EK)»). Теперь — только прямые потомки статьи.
import xml.etree.ElementTree as ET
_root = ET.fromstring(text.encode("utf-8"))
def _refs(w, k):
    return [(r.get("v", ""), r.get("source", "")) for r in w.findall("ref")][:k]
n = 0
for w in _root.iter("word"):
    v = w.get("v", "")
    if not bare(v).startswith(q):
        continue
    if lang and w.get("l") != lang:
        continue
    refs = _refs(w, 3)
    osnova = ""
    if not refs:
        # у нкв. статей своих ссылок нет: внутри вложено исходное слово (часто ᴱQ), ссылки — его. Показать как «основа».
        ch = w.find("word")
        if ch is not None:
            r2 = _refs(ch, 2)
            osnova = "основа: %s %s%s" % (ch.get("l", "?"), ch.get("v", ""), (" — " + "; ".join("%s (%s)" % r for r in r2)) if r2 else "")
    dep = [(d.get("l", "?"), d.get("v", "—")) for d in w.findall("deprecated")]
    ust = ("  ⚠УСТАРЕЛО→ " + ", ".join("%s %s" % d for d in dep)) if dep else ""
    print("%-5s %-20s %-30s %s%s" % (w.get("l", "?"), v, w.get("gloss", ""), "; ".join("%s (%s)" % r for r in refs) or osnova or "(своих ссылок нет)", ust))
    n += 1
    if n >= 25:
        break
print("найдено (до 25):", n)

# 2026-11-27: если среди слов ничего нет — искать слово в заметках (<notes>) Eldamo. Повод: *lanina* «woven»
# стоит только в заметке к нкв. *vírina* («Another possibility is lanina…»), и Quettali его знает, а я не нашёл.
if n == 0:
    w = sys.argv[1]
    k = 0
    for m in re.finditer(r'<word\b([^>]*)>(.*?)</word>', text, re.S):
        body = m.group(2)
        nm = re.search(r'<notes><!\[CDATA\[(.*?)\]\]></notes>', body, re.S)
        if not nm:
            continue
        plain = re.sub(r"<[^>]+>", "", nm.group(1))
        hit = re.search(r"\b%s\b" % re.escape(w), plain, re.I)
        if not hit:
            continue
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        a = max(0, hit.start() - 80)
        print("  в заметке к %s %s «%s»: …%s…" % (attrs.get("l", "?"), attrs.get("v", ""), attrs.get("gloss", ""),
                                                 plain[a:hit.end() + 80].replace("\n", " ")))
        k += 1
        if k >= 10:
            break
    print("в заметках:", k)
