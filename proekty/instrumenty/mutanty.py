"""mutanty.py путь [путь …] [--min 6] [--top 80] — кандидаты в «слова-мутанты»: русские слова из файлов,
которых не знает морфологический словарь OpenCorpora (pymorphy3), но у которых есть известный сосед
на расстоянии одной правки (замена, вставка, удаление, перестановка соседних букв).
Запуск: ext/venv-morph/bin/python -I proekty/instrumenty/mutanty.py inbox/html-generated
Печатает: слово, сколько раз в текстах, сосед, первый файл. Ловит только мутантов «в одну букву»
и не ловит мутантов, совпавших с настоящим словом («тендерная»). 2026-10-18, днём. См. proekty/rody-oshibok/.
(Первая версия брала частотный словарь субтитров ext/slovar/ru_full.txt — в нём нет «тороида» и «сердолика»; негодно.)"""
import os, re, sys
from collections import Counter
import pymorphy3

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
args = sys.argv[1:]
def opt(name, default):
    if name in args:
        i = args.index(name); v = args[i + 1]; del args[i:i + 2]; return int(v)
    return default
MINLEN = opt("--min", 6); TOP = opt("--top", 80)
SAM = "--sam" in args
args = [a for a in args if a != "--sam"]
morph = pymorphy3.MorphAnalyzer()
known = morph.word_is_known

files = []
for a in args:
    if os.path.isdir(a):
        for dp, dn, fn in os.walk(a):
            dn[:] = [d for d in dn if d not in ("node_modules", ".git", "build")]
            files += [os.path.join(dp, x) for x in fn if x.lower().endswith((".md", ".txt", ".html"))]
    else:
        files.append(a)

tok = re.compile(r"[а-яё]+")
count, where = Counter(), {}
for p in files:
    t = open(p, encoding="utf-8", errors="ignore").read()
    for m in tok.finditer(t.lower()):
        w = m.group(0)
        if len(w) >= MINLEN:
            count[w] += 1
            where.setdefault(w, p)

AB = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
def edits1(w):
    out = set()
    for i in range(len(w) + 1):
        a, b = w[:i], w[i:]
        if b:
            out.add(a + b[1:])
            for c in AB: out.add(a + c + b[1:])
        if len(b) > 1: out.add(a + b[1] + b[0] + b[2:])
        for c in AB: out.add(a + c + b)
    out.discard(w)
    return out

rows = []
if SAM:
    # архив как словарь сам себе: редкая форма (≤ 3), а сосед в одну правку встречается в тех же текстах ≥ 5 раз и в 5+ раз чаще
    for w, n in count.items():
        if n > 3 or known(w) or w.endswith("ъ") or w.endswith(("аго", "яго")):
            continue  # дореформенная орфография — стилизация, не мутант
        nb = sorted((count[e], e) for e in edits1(w) if count.get(e, 0) >= max(5, 5 * n)
                    and not e.startswith(w) and not w.startswith(e) and not e.endswith(w) and not w.endswith(e))  # обрывки и склейки
        if nb:
            rows.append((nb[-1][0], w, ["%s×%d" % (e, c) for c, e in reversed(nb)][:3], where[w]))
    rows.sort(key=lambda r: (-r[0], r[1]))
else:
    for w, n in count.items():
        if known(w):
            continue
        nb = sorted(e for e in edits1(w) if len(e) >= MINLEN - 1 and known(e))
        if nb:
            rows.append((n, w, nb[:3], where[w]))
    rows.sort(key=lambda r: (-r[0], r[1]))
for n, w, nb, p in rows[:TOP]:
    print("%-24s ×%-4d ~ %-40s %s" % (w, n, ", ".join(nb), os.path.relpath(p, root)))
print("кандидатов:", len(rows), "| неизвестных слов:", sum(1 for w in count if not known(w)), "| слов длиной ≥%d: %d | файлов: %d" % (MINLEN, len(count), len(files)))
