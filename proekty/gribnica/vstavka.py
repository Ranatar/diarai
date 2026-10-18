"""Вставить в сценарий автора событие «Тетрадь третьяго» (1936) сразу после дела 611-С.

python3 vstavka.py путь/к/scenario_rsfgr.json выход.json
Сценарий автора не копируется в репозиторий: вставка делается этим скриптом.
Документ: tetrad_1936.png рядом с render_archive.py (делается tetrad.py).
"""
import json, sys

src, dst = sys.argv[1], sys.argv[2]
s = json.load(open(src, encoding="utf-8"))
ev = {
    "id": "tetrad", "year": 1936, "kind": "Дневникъ", "pre": 0.8, "trans": 1.0, "hold": 6.5,
    "title": "Тетрадь третьяго",
    "text": "Изъ того же дѣла 611-С — школьная тетрадь въ клѣтку. Третій лаборантъ, слушавшій сушь, "
            "три недѣли пишетъ въ ней «я». Къ послѣднему листу онъ пишетъ безъ ятей и еровъ. "
            "Сданъ къ Корневищу, легъ и лежалъ до утра: Грибница не взяла.",
    "camera": [37.6, 55.8, 3.4],
    "docs": [{"file": "tetrad_1936.png",
              "caption": "Тетрадь третьяго лаборанта, л. 51. Дѣло № 611-С, 1936 · апокрифъ"}],
    "ops": [],
}
ids = [e.get("id") for e in s["events"]]
s["events"].insert(ids.index("case611") + 1, ev)

# 1973: у события «Протоколъ № 13/666» не было документа — добавить выписку (protokol.py)
for e in s["events"]:
    if e.get("id") == "protocol" and not e.get("docs"):
        e["docs"] = [{"file": "protokol_1973.png",
                      "caption": "Выписка изъ протокола № 13/666, 27.X.1973 · апокрифъ"}]
        e["hold"] = max(e.get("hold", 4.6), 6.0)
json.dump(s, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("вставлено событием", ids.index("case611") + 1, "→", dst)
