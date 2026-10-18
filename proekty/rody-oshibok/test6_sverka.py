"""test6_sverka.py — сверка test6-daty.tsv с Wikidata. Для каждого имени: wbsearchentities (ru), первый результат,
который является человеком (P31 = Q5); его P569/P570 (год). Кандидата НЕ подбираю по совпадению дат — это сделало бы
проверку замкнутой. |Δ| ≤ 2 года по обоим — «верно», ≤ 10 — «близко», иначе «расходится»; нет человека — «не найден».
Пишет вердикты обратно в tsv и кэш ответов в ext/wikidata-test6.json."""
import json, os, re, time, urllib.parse, urllib.request
here = os.path.dirname(os.path.abspath(__file__))
TSV = os.path.join(here, "test6-daty.tsv")
CACHE = os.path.join(here, "..", "..", "ext", "wikidata-test6.json")
API = "https://www.wikidata.org/w/api.php"
UA = "diarai-sverka/0.1 (https://github.com/Ranatar/diarai)"
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

def get(params):
    key = json.dumps(params, sort_keys=True, ensure_ascii=False)
    if key in cache: return cache[key]
    q = urllib.parse.urlencode(dict(params, format="json"))
    req = urllib.request.Request(API + "?" + q, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.load(r)
    cache[key] = out
    time.sleep(0.2)
    return out

def year(claims, p):
    for c in claims.get(p, []):
        v = c.get("mainsnak", {}).get("datavalue", {}).get("value", {})
        t = v.get("time")
        if t:
            m = re.match(r"([+-])(\d+)-", t)
            if m: return int(m.group(2)) * (-1 if m.group(1) == "-" else 1)
    return None

rows = [l.rstrip("\n").split("\t") for l in open(TSV, encoding="utf-8")]
head, body = rows[0], rows[1:]
for r in body:
    part, name, b, d = r[0], r[1], int(r[2]), int(r[3])
    res = get({"action": "wbsearchentities", "search": name, "language": "ru", "uselang": "ru", "type": "item", "limit": 7})
    ids = [x["id"] for x in res.get("search", [])]
    verdict, info = "не найден", ""
    if ids:
        ents = get({"action": "wbgetentities", "ids": "|".join(ids), "props": "claims|labels", "languages": "ru|en"})["entities"]
        for i in ids:
            e = ents.get(i, {}); cl = e.get("claims", {})
            if not any(c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id") == "Q5" for c in cl.get("P31", [])):
                continue
            wb, wd = year(cl, "P569"), year(cl, "P570")
            lab = e.get("labels", {}).get("ru", e.get("labels", {}).get("en", {})).get("value", "")
            info = "%s %s %s–%s" % (i, lab, wb, wd)
            if wb is None or wd is None:
                verdict = "нет дат"
            else:
                db, dd = abs(wb - b), abs(wd - d)
                verdict = "верно" if max(db, dd) <= 2 else ("близко" if max(db, dd) <= 10 else "расходится")
            break
    r[4:6] = [verdict, info]
    print("%-6s %-38s %4d–%-4d  %-10s %s" % (part, name[:38], b, d, verdict, info))
json.dump(cache, open(CACHE, "w"), ensure_ascii=False)
with open(TSV, "w", encoding="utf-8") as f:
    f.write("\t".join(head) + "\n")
    for r in body: f.write("\t".join(r[:6]) + "\n")
from collections import Counter
print(Counter(r[4] for r in body))
