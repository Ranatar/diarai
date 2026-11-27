"""periody.py файл_со_строками_квенья — «ложные друзья между периодами»: для каждого слова строки ищет в Eldamo
статьи с той же леммой в ᴹQ (mq) и в позднем Q (q) и печатает слова глоссы ᴹQ, которых нет ни в одной глоссе Q (то есть значение, которое поздний читатель не услышит). Повод — 27.11: ᴹQ *lanya-*
«weave» поздний читатель слышит как Q *lanya-¹* «bound»; ᴹQ *armar* «goods» — как Q *arma* «ray of sunlight»;
ᴹQ *usqe* «reek» — как Q *usquë* «dusk»; *rossë*: ᴹQ «dew», Q «rain; foam».
Основу ищу грубо: само слово и слово без частых окончаний (-r, -i, -n, -nen, -inen, -ssë, -ssen, -llo, -nna, -o, -on,
-ron, -va, -uva(n), -nya, -tya, -rya, -lya, -ina, -inë, -ë→-a и т. п.). Это эвристика: она может пропустить форму
и может найти лишнее. Решает человек.
Шумный: он не знает, в каком значении я взял слово. На всех 87 строках «Фауста» (27.11) — 91 лемма. Полезен на одну-две
свежие строки: глазами найти там слова, которые я взял из ᴹQ, и посмотреть, что услышит поздний читатель.
Запуск: python3 -I proekty/instrumenty/periody.py ext/tmp/stroki.txt
2026-11-27, пробуждение 20:32."""
import os, re, sys, unicodedata

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
xml = open(os.path.join(root, "inbox", "eldamo", "src", "data", "eldamo-data.xml"), encoding="utf-8").read()


def norm(s):
    s = unicodedata.normalize("NFC", s.lower())
    s = re.sub(r"[¹²³⁴⁵-]", "", s)
    s = s.replace("k", "c").replace("ë", "e").replace("q", "qu").replace("quu", "qu")
    return s


lex = {}   # нормализованная основа → [(язык, v, gloss)]
for m in re.finditer(r'<word\b([^>]*)>', xml):
    a = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
    if a.get("l") not in ("q", "mq") or not a.get("gloss"):
        continue
    lex.setdefault(norm(a["v"]), []).append((a["l"], a["v"], a["gloss"]))

KONCY = ["inen", "nen", "ssen", "ssë", "sse", "llo", "lo", "nna", "uvan", "uva", "nya", "tya", "rya", "lya", "ron",
         "on", "ina", "inë", "ine", "ar", "or", "ir", "er", "r", "i", "n", "o", "va", "ë", "e"]


KONCY += ["ea", "ya"]


def snyat(w0):
    out = set()
    for k in KONCY:
        k = norm(k)
        if w0.endswith(k) and len(w0) - len(k) >= 2:
            b = w0[:-len(k)]
            out |= {b, b + "a", b + "e", b + "o"}
    return out


def osnovy(w):
    """слово и слово без одного или двух окончаний (притяжательный суффикс + падеж: rosse-tya-sse)"""
    w0 = norm(w)
    odin = snyat(w0)
    dva = set()
    for b in odin:
        dva |= snyat(b)
    return {w0} | odin | dva


STOP = {"the", "and", "of", "to", "a", "an", "in", "on", "or", "be", "lit", "esp", "for", "with", "that", "as", "by", "is"}


def slova(g):
    return {w for w in re.findall(r"[a-z]+", g.lower()) if w not in STOP and len(w) > 2}


nashel = 0
vidano = set()
for line in open(sys.argv[1], encoding="utf-8"):
    for tok in re.findall(r"[A-Za-zÁÉÍÓÚáéíóúëäöñ']+", line):
        if len(tok) <= 3:      # служебные (ar, i, na, ya…) дают шум
            continue
        for b in sorted(osnovy(tok)):
            ent = lex.get(b, [])
            mq = [(v, g) for l, v, g in ent if l == "mq"]
            q = [(v, g) for l, v, g in ent if l == "q"]
            if not (mq and q):
                continue
            qslova = set().union(*(slova(g) for v, g in q))
            for v, g in mq:
                net = slova(g) - qslova
                if net and (b, v) not in vidano:
                    vidano.add((b, v))
                    nashel += 1
                    print("%-14s ᴹQ %s «%s» — в позднем Q нет: %s" % (tok, v, g, ", ".join(sorted(net))))
                    print("%-14s  Q %s" % ("", "; ".join("%s «%s»" % x for x in q)))
print("лемм, у которых в ᴹQ есть значение, которого нет в Q:", nashel)
