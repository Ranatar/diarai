"""qt_razbor.py ФАЙЛ|- [--vse] — разбор квенийских строк через API Quettali (quettali.org, /api/v1/dissect).

Каждая непустая строка файла — отдельный пункт. Печатает для каждого слова: лемму, перевод, теги формы;
слова, которых Quettali не знает, помечает «??». С --vse печатает все варианты, иначе первые три.
Один POST на весь файл (вежливость к чужому серверу). Ответ кладётся в ext/tmp/qt-last.json и в ФАЙЛ.qt.json.
Quettali — чужой инструмент (chaered, Vinyë Lambengolmor), alpha; его «??» — не приговор слову,
а повод посмотреть в Eldamo; его «match» — не доказательство, что форма толкиновская
(в словаре есть NQ/UQ и модели парадигм)."""
import json
import sys
import urllib.request

URL = "https://quettali.org/api/v1/dissect"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    vse = "--vse" in sys.argv
    src = sys.stdin if not args or args[0] == "-" else open(args[0], encoding="utf-8")
    lines = [l.strip() for l in src if l.strip()]
    req = {"input": [{"items": [{"text": l} for l in lines]}]}
    r = urllib.request.Request(URL, data=json.dumps(req).encode("utf-8"),
                               headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=60) as f:
        data = json.load(f)
    # ответ сохраняется и в qt-last.json, и рядом с входным файлом (ФАЙЛ.qt.json), чтобы следующий прогон
    # его не затёр (27.10: ответ по -ima пропал именно так — нашёл проверяющий)
    outs = ["ext/tmp/qt-last.json"] + ([args[0] + ".qt.json"] if args and args[0] != "-" else [])
    for o in outs:
        with open(o, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
    neizv = 0
    vsego = 0
    nez = set()
    for block in data.get("analysis", []):
        for it in block.get("items", []):
            print("\n>>", it.get("text"))
            for m in it.get("match", []):
                vsego += 1
                if m.get("mode") == "again":  # слово уже было выше; Quettali даёт ссылку "seen"
                    print("   %s: (было выше%s)" % (m.get("word"), ", не узнано" if m.get("word") in nez else ""))
                    neizv += m.get("word") in nez
                    continue
                found = m.get("found") or []
                if m.get("mode") != "match" or not found:
                    neizv += 1
                    nez.add(m.get("word"))
                    print("   ?? %s  (mode=%s)" % (m.get("word"), m.get("mode")))
                    continue
                vars_ = []
                for fd in found:
                    tags = ";".join(t for fm in fd.get("forms", []) for t in fm.get("tags", []))
                    vars_.append("%s «%s» [%s]" % (fd.get("lemma"), fd.get("trans"), tags))
                if not vse:
                    vars_ = vars_[:3] + (["…+%d" % (len(found) - 3)] if len(found) > 3 else [])
                print("   %s: %s" % (m.get("word"), " | ".join(vars_)))
        break  # блок 0 — «Literal»; остальные блоки (если есть) — иные режимы разбора
    print("\nслов: %d, не узнано: %d" % (vsego, neizv))


main()
