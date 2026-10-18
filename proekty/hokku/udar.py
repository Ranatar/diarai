"""Словарь ударений, сведённый из четырёх чужих источников (лежат в ext/).

Источники, по убыванию доверия:
  ext/openrussian/*.csv           — OpenRussian (CC BY-SA 4.0), все словоформы, ударение — «'» после гласной
  ext/stressrnn/exception_dictionary.txt — из StressRNN (Зализняк), «+» после гласной
  ext/espeak/ru_listx             — espeak-ng, «слово $N», N — номер ударного слога
  ext/classic-ai/words_accent.json.bz2 — бейзлайн Сбера, {слово: номер слога}
  inbox/lleo_poet_bundle/bases/base_ru.txt — база автора, «СЛОВО|N», запасной источник

Откуда брать (raw.githubusercontent.com, ветка master):
  Badestrand/russian-dictionary/{nouns,verbs,adjectives,others}.csv
  dbklim/StressRNN/stressrnn/dicts/exception_dictionary.txt
  espeak-ng/espeak-ng/dictsource/extra/ru_listx
  sberbank-ai/classic-ai/examples/phonetic-baseline/data/words_accent.json.bz2

Ударение храню как номер слога с 1. У слова может быть несколько вариантов
(за'мок/замо'к, разные источники) — храню множество.
Кэш собирается один раз в ext/udar-cache.tsv.

    from udar import stress
    stress("дневника")  -> {3}
    stress("кот")       -> {1}   (односложные — всегда 1)
    stress("ёлка")      -> {1}   (ё всегда ударна)
    stress("хокку")     -> None  (неизвестно)
"""
import bz2
import csv
import json
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
EXT = os.path.join(ROOT, "ext")
CACHE = os.path.join(EXT, "udar-cache.tsv")
VOWELS = set("аеёиоуыэюя")


def nsyl(w):
    return sum(c in VOWELS for c in w.lower())


def _from_marked(form, mark):
    """'сказа'ть' -> ('сказать', 3). Несколько отметок — несколько вариантов."""
    form = form.strip().lower()
    if not form or " " in form:
        return None, set()
    bare = form.replace(mark, "")
    out, syl = set(), 0
    for i, c in enumerate(form):
        if c in VOWELS:
            syl += 1
        elif c == mark and syl:
            out.add(syl)
    return bare, out


def _build():
    d = {}

    def add(w, ss, override=False):
        if not w or not ss or not re.fullmatch(r"[а-яё-]+", w):
            return
        if w in d and not override:
            return
        d.setdefault(w, set()).update(ss)

    # 1. OpenRussian: все формы. Добавляем, объединяя варианты.
    for name in ("nouns", "verbs", "adjectives", "others"):
        p = os.path.join(EXT, "openrussian", name + ".csv")
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8") as f:
            r = csv.reader(f, delimiter="\t")
            head = next(r)
            skip = {i for i, h in enumerate(head)
                    if h in ("bare", "translations_en", "translations_de",
                             "gender", "partner", "animate", "indeclinable",
                             "sg_only", "pl_only", "aspect")}
            for row in r:
                for i, cell in enumerate(row):
                    if i in skip:
                        continue
                    for form in re.split(r"[,;/]", cell):
                        form = form.replace("*", "").replace("(", "").replace(")", "")
                        bare, ss = _from_marked(form, "'")
                        if bare and ss:
                            d.setdefault(bare, set()).update(ss)
    # 2. StressRNN
    p = os.path.join(EXT, "stressrnn", "exception_dictionary.txt")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            bare, ss = _from_marked(line, "+")
            add(bare, ss)
    # 3. espeak
    p = os.path.join(EXT, "espeak", "ru_listx")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            m = re.match(r"(\S+)\s+\$(\d+)", line)
            if m:
                add(m[1], {int(m[2])})
    # 4. classic-ai
    p = os.path.join(EXT, "classic-ai", "words_accent.json.bz2")
    if os.path.exists(p):
        for w, s in json.load(bz2.open(p, "rt", encoding="utf-8")).items():
            add(w, {int(s)})
    # 5. база lleo_poet из inbox (Koziev + WikiPron + генератор по Зализняку).
    #    Только как запасной: при расхождениях мои источники чаще правы
    #    (сверка 2026-10-18: совпадение 98,8%, в спорных словах база ошибается
    #    чаще — «берушами|3», «шакьямуни|1»), но в ней есть «буду», «нами», «обе».
    p = os.path.join(ROOT, "inbox", "lleo_poet_bundle", "bases", "base_ru.txt")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            head = line.split("←")[0].strip()
            if "|" in head and not head.startswith("#"):
                w, n = head.split("|", 1)
                if n.isdigit():
                    add(w.lower(), {int(n)})
    with open(CACHE, "w", encoding="utf-8") as f:
        for w in sorted(d):
            f.write(w + "\t" + ",".join(map(str, sorted(d[w]))) + "\n")
    return d


_D = None


def _load():
    global _D
    if _D is None:
        if os.path.exists(CACHE):
            _D = {}
            for line in open(CACHE, encoding="utf-8"):
                w, s = line.rstrip("\n").split("\t")
                _D[w] = set(map(int, s.split(",")))
        else:
            _D = _build()
        # свои дополнения поверх всего: «слово|номер ударного слога» (svoi_udareniya.txt рядом)
        own = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svoi_udareniya.txt")
        if os.path.exists(own):
            for line in open(own, encoding="utf-8"):
                line = line.split("#")[0].strip()
                if "|" in line:
                    w, n = line.split("|", 1)
                    _D[w.strip().lower()] = {int(n)}
    return _D


def stress(word):
    w = word.lower()
    n = nsyl(w)
    if n == 0:
        return set()
    if n == 1:
        return {1}
    if "ё" in w:
        return {nsyl(w[: w.index("ё") + 1])}
    d = _load()
    if w in d:
        return {s for s in d[w] if 1 <= s <= n} or None
    return None


if __name__ == "__main__":
    import sys
    if "--build" in sys.argv:
        print(len(_build()), "слов")
    for w in sys.argv[1:]:
        if not w.startswith("--"):
            print(w, stress(w))
