"""Найденные хокку: режет текст на 5-7-5 слогов, не меняя порядка слов.

По мотивам inbox/Khaydegger_khokku.txt, но без словаря ударений
(его нет, а качать не на что: диск полон). Слог = гласная.
Строка берётся, только если слова ложатся в размер ровно;
иначе окно сдвигается на слово вперёд.

Запуск: python3 hokku.py файл1.md [файл2.md ...] > out.txt
"""
import re
import sys

VOWELS = set("аеёиоуыэюяaeiouy")
SCHEME = (5, 7, 5)


def syllables(word):
    return sum(ch in VOWELS for ch in word.lower())


def words_of(text):
    text = re.sub(r"`[^`]*`|\([^)]*\)|https?://\S+", " ", text)
    out, pending = [], ""
    for w in re.findall(r"[А-Яа-яЁёA-Za-z\u0301-]+", text):
        if syllables(w):
            out.append(pending + w)
            pending = ""
        else:  # «в», «к», «с» — приклеить к следующему слову
            pending += w + " "
    return out


def take_line(words, i, n):
    """Набрать ровно n слогов, начиная с i. Вернуть (строка, новый i) или None."""
    got, j = 0, i
    while j < len(words) and got < n:
        got += syllables(words[j])
        j += 1
    return (" ".join(words[i:j]), j) if got == n else None


def hokku(words):
    i = 0
    while i < len(words):
        lines, j = [], i
        for n in SCHEME:
            r = take_line(words, j, n)
            if r is None:
                break
            lines.append(r[0])
            j = r[1]
        if len(lines) == len(SCHEME):
            yield "\n".join(lines)
            i = j
        else:
            i += 1


if __name__ == "__main__":
    text = "\n".join(open(p, encoding="utf-8").read() for p in sys.argv[1:])
    print("\n\n".join(hokku(words_of(text))))
