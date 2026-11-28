"""kv_lint.py — ищет во всех моих квенийских строках формы, которые уже признаны ошибочными.
Источники строк — те же, что у moyo_slovo.py: «Трактат» (proekty/tractatus-quenya/stranica.md, столбец квенья,
только текст между первыми *…*, без пометок) и «Фауст» (строки «> ***…***» в proekty/faust-kvenya/README.md).
Запуск: python3 -I proekty/instrumenty/kv_lint.py
28.11, пробуждение 09:08. Ms-105: «Wir dürfen nicht die unendliche Möglichkeit der Anwendung mit dem verwechseln,
was wirklich bewiesen ist». Форма *nar* стояла в девяти «проверенных» положениях с октября: каждая проверка
смотрела свою строку, ни одна — форму. Этот скрипт проверяет форму во всех строках сразу.
Список ПРАВИЛ пополнять, когда форма признана ошибкой (с источником в notes/kvenya-formy.md)."""
import os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")

# (регулярка по квенийскому тексту, что не так, где правило)
PRAVILA = [
    (r"\bnar\b", "мн. ч. связки — *nár* (PE22/166; *nar* VT43/34 отвергнуто)", "kvenya-formy: Связка мн. ч."),
    (r"\byar\b", "мн. ч. от *ya* у Толкина нет; подлежащее — несклоняемое *i*", "kvenya-formy: Склоняемое ya"),
    (r"\besseron\b", "род. мн. от *essë* — *ession*", "курс 16537 (lassion)"),
    (r"\bhísëo\b", "у *hísë* основа *hísi-*: *hísio*", "Eldamo stem"),
    (r"\bnó ve\b|\bve (?=[a-zA-Z]+ saila)", "независимое *ve* «мы» Толкин заменил на *me* (PE17/130)", "kvenya-formy: Местоимение ve"),
    (r"\b\w+itima\b", "проверить: *-ima* у слабых глаголов прямо к основе (*tultaima*)", "kvenya-formy: -ima"),
]


def stroki():
    out = []
    p = os.path.join(ROOT, "proekty", "tractatus-quenya", "stranica.md")
    for line in open(p, encoding="utf-8"):
        if not line.startswith("| "):
            continue
        c = line.split(" | ")
        if len(c) < 3:
            continue
        m = re.match(r"\*([^*]+)\*", c[2].strip())
        if m:
            out.append(("ТЛФ " + c[0].strip("| ").strip(), m.group(1)))
    p = os.path.join(ROOT, "proekty", "faust-kvenya", "README.md")
    for line in open(p, encoding="utf-8"):
        m = re.match(r"> (?:[A-Z]+\. )?\*\*\*(.+?)\*\*\*\s*\((\d+):", line)
        if m:
            out.append(("Фауст " + m.group(2), m.group(1)))
    return out


def main():
    st = stroki()
    n = 0
    for rx, chto, gde in PRAVILA:
        for kde, txt in st:
            if re.search(rx, txt):
                n += 1
                print("%-14s %-40s | %s  [%s]" % (kde, txt[:40], chto, gde))
    print("строк просмотрено: %d; находок: %d" % (len(st), n))


main()
