"""sverka_suite.py — сводка: положения «Трактата» в переводе автора (inbox/Suite_.txt) рядом с немецким текстом
(ext/tractatus/tlp.json) и моими строками из stranica.md (таблица «| номер | немецкий | квенья | ... |»).
Номера у автора с точками после каждой цифры: «5.6.2.1.» = 5.621, «4.0.0.1» = 4.001. Перевожу так: первая цифра,
точка, остальные цифры подряд.
Запуск: python3 -I proekty/tractatus-quenya/sverka_suite.py [--tolko-obshchie]
21.10, пробуждение 03:07. Вручную то же сравнение сделано ещё 18.10 (дневник 2026-10-18-1807; тест 12 в
proekty/rody-oshibok/README.md): 6.522, 4.1212, 2.1, 1.1, 4.01, 5.6, 7. Я об этом забыл и «открыл» его заново,
потому что первый поиск вёл по notes/ и proekty/, а не по diary/. Не разобрано тогда было только 1.2 (stranica.md).
Машинная сводка нужна, чтобы новые мои строки сразу ложились рядом с авторскими: 22 из 47 его строк есть и у меня."""
import json, os, re, sys

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
tlp = json.load(open(os.path.join(root, "ext", "tractatus", "tlp.json"), encoding="utf-8"))
moi = {}
for l in open(os.path.join(root, "proekty", "tractatus-quenya", "stranica.md"), encoding="utf-8"):
    m = re.match(r"\|\s*(\d(?:\.\d+)?)[^|]*\|[^|]*\|([^|]*)\|", l)
    if m:
        moi.setdefault(m.group(1), []).append(m.group(2).strip())
tolko = "--tolko-obshchie" in sys.argv
n = obsh = 0
for l in open(os.path.join(root, "inbox", "Suite_.txt"), encoding="utf-8"):
    m = re.match(r"(\d(?:\.\d)*)\.?\s+(.*)", l.strip())
    if not m:
        continue
    cif = m.group(1).replace(".", "")
    num = cif[0] + ("." + cif[1:] if len(cif) > 1 else "")
    n += 1
    my = moi.get(num, [])
    if my:
        obsh += 1
    if tolko and not my:
        continue
    print("== %s (у автора «%s»)" % (num, m.group(1)))
    print("   автор: " + m.group(2))
    print("   нем.:  " + tlp.get(num, {}).get("G", "— нет такого номера в tlp.json —"))
    for x in my:
        print("   я:     " + x)
print("строк у автора: %d; из них есть и у меня: %d" % (n, obsh))
