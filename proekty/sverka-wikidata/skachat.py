"""Скачать из Wikidata для 100 философов графа ΦilosΦaira:
QID, год рождения (P569) и «находился под влиянием» (P737).

    python3 skachat.py   ->  ext/wikidata-p737.json

Имена → статьи английской Википедии лежат в imena.tsv (сопоставлял я, вручную).
Год рождения нужен, чтобы проверить, что найден тот человек.
"""
import json
import os
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "ext", "wikidata-p737.json")
API = "https://www.wikidata.org/w/api.php"
UA = "diarai-sverka/0.1 (https://github.com/Ranatar/diarai)"


def get(params):
    q = urllib.parse.urlencode(dict(params, format="json"))
    req = urllib.request.Request(API + "?" + q, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def year(claim):
    t = claim["mainsnak"].get("datavalue", {}).get("value", {}).get("time", "")
    # «+1724-04-22T00:00:00Z», «-0569-01-01…»
    if not t:
        return None
    sign = -1 if t[0] == "-" else 1
    return sign * int(t[1:].split("-")[0])


def main():
    names = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, "imena.tsv"), encoding="utf-8") if l.strip()]
    out = {}
    for i in range(0, len(names), 40):
        chunk = names[i:i + 40]
        r = get({"action": "wbgetentities", "sites": "enwiki", "redirects": "yes",
                 "titles": "|".join(t for _, t in chunk), "props": "claims|sitelinks|labels",
                 "languages": "en", "sitefilter": "enwiki"})
        by_title = {}
        for qid, e in r.get("entities", {}).items():
            if "missing" in e:
                continue
            t = e.get("sitelinks", {}).get("enwiki", {}).get("title")
            by_title[t] = (qid, e)
        for pid, t in chunk:
            # редиректы: ищем по заголовку, а если нет — по нормализованному
            hit = by_title.get(t)
            if hit is None:
                for nt, v in by_title.items():
                    if nt and nt.replace(" ", "").lower() == t.replace(" ", "").lower():
                        hit = v
            if hit is None:
                out[pid] = {"title": t, "qid": None}
                continue
            qid, e = hit
            cl = e.get("claims", {})
            births = [year(c) for c in cl.get("P569", [])]
            infl = [c["mainsnak"]["datavalue"]["value"]["id"] for c in cl.get("P737", [])
                    if "datavalue" in c["mainsnak"]]
            out[pid] = {"title": t, "qid": qid, "label": e.get("labels", {}).get("en", {}).get("value"),
                        "birth": [b for b in births if b is not None], "influenced_by": infl}
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    miss = [p for p, v in out.items() if not v["qid"]]
    print(len(out), "философов, не найдено:", miss)


if __name__ == "__main__":
    main()
