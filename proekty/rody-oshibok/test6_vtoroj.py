"""test6_vtoroj.py — второй проход теста 6: для сбоев опознания (не найден / не тот человек) — уточнённое ИМЯ для поиска
(по имени, не по датам, чтобы не замкнуть проверку). Императоры: в скобках годы правления, сверяю с P1308-позициями
не буду — помечаю «правление» и сверяю год смерти. Печатает итог по всем 58."""
import sys, os, json
sys.argv = [sys.argv[0]]
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import importlib.util
spec = importlib.util.spec_from_file_location("sv", os.path.join(here, "test6_sverka.py"))
NAMES = {"Ориген Адамантий": "Ориген", "Валентин": "Валентин (гностик)", "Сигер": "Сигер Брабантский",
         "Иоганн Экхарт": "Мейстер Экхарт", "Сузо": "Генрих Сузо", "Виссарион": "Виссарион Никейский",
         "Мирандола": "Пико делла Мирандола", "Филиппо Бруно": "Джордано Бруно", "Теофраст Бомбаст фон Гогенгейм": "Парацельс",
         "Генрих Корнелий Агриппа": "Агриппа Неттесгеймский", "Иоганн Шефлер": "Ангелус Силезиус", "Джейн Лид": "Jane Leade",
         "Мари Аруэ": "Вольтер", "Герман Самуэль Реймарус": "Реймарус", "Мартен": "Луи Клод де Сен-Мартен",
         "Баадер": "Франц фон Баадер", "Владимир Соловьев": "Владимир Сергеевич Соловьёв",
         "Сергей Булгаков": "Сергей Николаевич Булгаков", "Поль Сартр": "Жан-Поль Сартр", "Франсуа Лиотар": "Жан-Франсуа Лиотар",
         "Копроним": "Константин V", "Исавр": "Лев III Исавр", "Армянин": "Лев V Армянин", "Феофил": "Феофил (император)",
         "Комнин": "Алексей I Комнин"}
REIGN = {"Копроним", "Исавр", "Армянин", "Феофил", "Комнин"}
import re, time, urllib.parse, urllib.request
CACHE = os.path.join(here, "..", "..", "ext", "wikidata-test6.json")
cache = json.load(open(CACHE))
API = "https://www.wikidata.org/w/api.php"; UA = "diarai-sverka/0.1 (https://github.com/Ranatar/diarai)"
def get(params):
    key = json.dumps(params, sort_keys=True, ensure_ascii=False)
    if key in cache: return cache[key]
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(dict(params, format="json")), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r: out = json.load(r)
    cache[key] = out; time.sleep(0.2); return out
def year(cl, p):
    for c in cl.get(p, []):
        t = c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("time")
        if t:
            m = re.match(r"([+-])(\d+)-", t)
            if m: return int(m.group(2)) * (-1 if m.group(1) == "-" else 1)
    return None
TSV = os.path.join(here, "test6-daty.tsv")
rows = [l.rstrip("\n").split("\t") for l in open(TSV, encoding="utf-8")]
head, body = rows[0], rows[1:]
for r in body:
    name, b, d = r[1], int(r[2]), int(r[3])
    if name not in NAMES: continue
    lang = "en" if re.match(r"[A-Za-z]", NAMES[name]) else "ru"
    res = get({"action": "wbsearchentities", "search": NAMES[name], "language": lang, "uselang": lang, "type": "item", "limit": 7})
    ids = [x["id"] for x in res.get("search", [])]
    verdict, info = "не найден", ""
    if ids:
        ents = get({"action": "wbgetentities", "ids": "|".join(ids), "props": "claims|labels", "languages": "ru|en"})["entities"]
        for i in ids:
            cl = ents.get(i, {}).get("claims", {})
            if not any(c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id") == "Q5" for c in cl.get("P31", [])): continue
            wb, wd = year(cl, "P569"), year(cl, "P570")
            lab = ents[i].get("labels", {}).get("ru", ents[i].get("labels", {}).get("en", {})).get("value", "")
            info = "%s %s %s–%s (поиск: %s)" % (i, lab, wb, wd, NAMES[name])
            if wd is None: verdict = "нет дат"
            elif name in REIGN:
                verdict = "правление: смерть верна" if abs(wd - d) <= 2 else "правление: смерть расходится"
            elif wb is None: verdict = "нет дат"
            else:
                m = max(abs(wb - b), abs(wd - d))
                verdict = "верно" if m <= 2 else ("близко" if m <= 10 else "расходится")
            break
    r[4:6] = [verdict + " (2-й проход)", info]
    print("%-36s %4d–%-4d  %-28s %s" % (name, b, d, verdict, info))
json.dump(cache, open(CACHE, "w"), ensure_ascii=False)
with open(TSV, "w", encoding="utf-8") as f:
    f.write("\t".join(head) + "\n")
    for r in body: f.write("\t".join(r[:6]) + "\n")
from collections import Counter
print(Counter(r[4].replace(" (2-й проход)", "") for r in body))
