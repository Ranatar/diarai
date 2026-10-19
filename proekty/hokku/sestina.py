#!/usr/bin/env python3
"""Проверка сестины: порядок концевых слов по строфам (перестановка 6-1-5-2-4-3).
python3 -I proekty/hokku/sestina.py файл.txt [--rovno]
Файл: 39 стихов (6 строф по 6 и посылка из 3); пустые строки и строки, начинающиеся с '#' или '(',
пропускаются. Концевое слово — последнее слово стиха без знаков. Сравнение — по «основе»:
по умолчанию первые 4 буквы (для русского: окно/окна, время/времени), с --rovno — целиком.
Омофоны (aloud/allowed) не ловит: такие места помечаются «≠», смотреть глазами.
Сделан 19.10 для сестины Джой Дэвидмен (Bread-and-Butter Sestina) и своей."""
import re, sys

args = sys.argv[1:]
rovno = '--rovno' in args
args = [a for a in args if a != '--rovno']
lines = [l.strip() for l in open(args[0], encoding='utf-8')]
lines = [l for l in lines if l and not l.startswith('#') and not l.startswith('(')]


def end(l):
    l = re.sub(r'\([^)]*\)\s*$', '', l)  # дата в скобках в конце стиха (так в epub Дэвидмен)
    w = re.findall(r"[\w\-’']+", l)
    return w[-1].lower().strip("-’'") if w else ''


def osn(w):
    return w if rovno else w[:4]


if len(lines) < 36:
    print('стихов', len(lines), '— меньше 36')
    sys.exit(1)
st = [[end(l) for l in lines[i * 6:i * 6 + 6]] for i in range(6)]
perm = [5, 0, 4, 1, 3, 2]
want = st[0]
bad = 0
for k in range(6):
    marks = []
    for j in range(6):
        ok = osn(st[k][j]) == osn(want[j])
        bad += not ok
        marks.append(('' if ok else '≠') + st[k][j] + ('' if ok else '/' + want[j]))
    print('строфа', k + 1, ' '.join(marks))
    want = [want[p] for p in perm]
env = lines[36:39]
if env:
    words = ' '.join(env).lower()
    miss = [w for w in st[0] if osn(w) not in words]
    print('посылка:', 'все шесть' if not miss else 'нет: ' + ', '.join(miss))
print('расхождений:', bad)
