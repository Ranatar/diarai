"""Сверка ссылок на параграфы курса Eldamo (intro-quenya) в моём тексте.

Для каждой строки с «§N.N…» берёт курсивные слова (*…*) той же строки
и ищет их в тексте раздела курса (раздел = от заголовка «N.N…» до следующего
заголовка того же или более высокого уровня; подразделы включаются).
Печатает: есть ли раздел, и какие из слов строки в нём нашлись.

python3 -I proekty/instrumenty/sverka_paragrafov.py proekty/tractatus-quenya/perevod.md
"""
import re
import sys
import unicodedata
from pathlib import Path

KURS = Path('/home/diarai/diarai/inbox/eldamo/src/main/webapp/l10n/ru/sources/intro-quenya')
ZAG = re.compile(r'^(\d+(?:\.\d+)+)\s+\S')


def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn')


def razdely():
    """номер -> текст (с подразделами). Берём последнее вхождение заголовка
    (первые — оглавление)."""
    nachala = {}
    stroki = []
    for f in sorted(KURS.glob('eldamo-intro-quenya-*.html.txt')):
        for line in f.read_text(encoding='utf-8').splitlines():
            m = ZAG.match(line)
            if m:
                nachala[m.group(1)] = len(stroki)
            stroki.append(line)
    tekst = {}
    for nom, i in nachala.items():
        uroven = nom.count('.')
        j = i + 1
        while j < len(stroki):
            m = ZAG.match(stroki[j])
            if m and m.group(1).count('.') <= uroven and not m.group(1).startswith(nom + '.'):
                break
            j += 1
        tekst[nom] = norm('\n'.join(stroki[i:j]))
    return tekst


def main(put):
    tekst = razdely()
    for n, line in enumerate(Path(put).read_text(encoding='utf-8').splitlines(), 1):
        ssylki = re.findall(r'§(\d+(?:\.\d+)*)', line)
        if not ssylki:
            continue
        slova = set()
        for k in re.findall(r'\*{1,3}([^*]+?)\*{1,3}', line):
            for w in re.findall(r"[^\s.,;:!?«»()\[\]—…·]+", k):
                if len(w) > 2:
                    slova.add(w)
        for s in ssylki:
            s = s.rstrip('.')
            if s not in tekst:
                print(f'{n}: §{s} — РАЗДЕЛА НЕТ')
                continue
            est = sorted(w for w in slova if norm(w) in tekst[s])
            print(f'{n}: §{s} — есть; слова строки в разделе: {", ".join(est) or "—"}')


if __name__ == '__main__':
    main(sys.argv[1])
