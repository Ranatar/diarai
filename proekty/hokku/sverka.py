"""Сверка моего словаря ударений (ext/udar-cache.tsv) с базой lleo_poet
(inbox/lleo_poet_bundle/bases/base_ru.txt: Koziev + WikiPron + генератор по Зализняку).

    python3 proekty/hokku/sverka.py [тексты...]

Печатает: общие слова, совпадения, расхождения (с примерами), и сколько слов
из данных текстов неизвестно каждому словарю.
"""
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import udar  # noqa: E402

ROOT = udar.ROOT
BASE = os.path.join(ROOT, "inbox", "lleo_poet_bundle", "bases", "base_ru.txt")


def load_base():
    b = {}
    for line in open(BASE, encoding="utf-8"):
        if line.startswith("#"):
            continue
        head = line.split("←")[0].strip()
        if "|" in head:
            w, n = head.split("|", 1)
            if n.isdigit():
                b.setdefault(w.lower(), set()).add(int(n))
        elif head:
            b.setdefault(head.lower(), set())
    return b


def main():
    mine = udar._load()
    base = load_base()
    common = [w for w in mine if w in base and base[w] and udar.nsyl(w) > 1 and "ё" not in w]
    agree = [w for w in common if mine[w] & base[w]]
    disagree = [w for w in common if not (mine[w] & base[w])]
    print("мой словарь:", len(mine), " база lleo_poet:", len(base))
    print("общих многосложных без ё:", len(common))
    print("совпадают (есть общий вариант): %d (%.1f%%)" % (len(agree), 100 * len(agree) / max(1, len(common))))
    print("расходятся:", len(disagree))
    random.seed(1)
    for w in random.sample(disagree, min(25, len(disagree))):
        print("   ", w, "мой", sorted(mine[w]), "база", sorted(base[w]))
    if sys.argv[1:]:
        words = []
        for p in sys.argv[1:]:
            words += re.findall(r"[а-яё]+", open(p, encoding="utf-8").read().lower())
        poly = {w for w in words if udar.nsyl(w) > 1 and "ё" not in w}
        nm = {w for w in poly if w not in mine}
        nb = {w for w in poly if not base.get(w)}
        print("\nв текстах многосложных слов (разных):", len(poly))
        print("неизвестно мне:", len(nm), " неизвестно базе:", len(nb), " обоим:", len(nm & nb))
        print("  только базе известны:", sorted(nm - nb)[:40])
        print("  никому:", sorted(nm & nb)[:60])


if __name__ == "__main__":
    main()
