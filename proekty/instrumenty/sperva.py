"""sperva.py заметка.md [--top 15] — «сначала notes/»: что уже есть в моих notes/, diary/, proekty/**/README.md
об опорных словах этой заметки. Опорные: имена файлов в `обратных кавычках`, латинские слова от 5 букв,
слова с заглавной (кроме начала предложения) и термины в «ёлочках». Для каждого — сколько других моих файлов
его содержат и где первое вхождение. Чем меньше файлов, тем ценнее совпадение (редкое слово).
Зачем: правило «сначала искать в своих notes/» трижды нарушено 2026-10-18 (Эрхарт, «сито», …) — пока оно было
прогоном, а не проверкой (notes/proverka-i-progon.md). Калибровка — в конце файла."""
import os, re, sys, glob
from collections import Counter
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
args = sys.argv[1:]
TOP = 15
if "--top" in args:
    i = args.index("--top"); TOP = int(args[i + 1]); del args[i:i + 2]
skip = set()
if "--bez" in args:  # исключить ещё файл (например, нынешнюю версию той же заметки при калибровке на старой)
    i = args.index("--bez"); skip.add(os.path.abspath(args[i + 1])); del args[i:i + 2]
me = os.path.abspath(args[0])
skip.add(me)
# дневник текущего пробуждения — эхо самой заметки; ценное лежит в старых файлах (калибровка 2026-10-18:
# без этого «эрхарт → kontinuum.md» тонул за пределами первых 15 строк)
diaries = sorted(glob.glob(os.path.join(root, "diary", "*.md")))
if diaries and "--s-dnevnikom" not in args:
    skip.add(os.path.abspath(diaries[-1]))
args = [a for a in args if a != "--s-dnevnikom"]
# файлы, созданные в этом же пробуждении, — тоже эхо: отсекаем по времени первого коммита (git) против имени дневника
import subprocess, datetime
if diaries and "--vse" not in args:
    stem = os.path.basename(diaries[-1])[:15]  # ГГГГ-ММ-ДД-ЧЧММ
    try:
        start = datetime.datetime.strptime(stem, "%Y-%m-%d-%H%M").replace(tzinfo=datetime.timezone.utc).timestamp()
        out = subprocess.run(["git", "-C", root, "log", "--diff-filter=A", "--name-only", "--format=@%ct"],
                             capture_output=True, text=True).stdout
        born, t0 = {}, None
        for line in out.splitlines():
            if line.startswith("@"):
                t0 = int(line[1:])
            elif line.strip():
                born[os.path.abspath(os.path.join(root, line.strip()))] = t0  # log идёт от новых к старым: останется самое раннее
        for p in list(born):
            if born[p] is not None and born[p] >= start:
                skip.add(p)
        # ещё не закоммиченные новые файлы тоже из этого пробуждения
        new = subprocess.run(["git", "-C", root, "ls-files", "--others", "--exclude-standard"], capture_output=True, text=True).stdout
        skip |= {os.path.abspath(os.path.join(root, x)) for x in new.split()}
    except ValueError:
        pass
args = [a for a in args if a != "--vse"]
mine = [p for d in ("notes", "diary") for p in glob.glob(os.path.join(root, d, "*.md"))]
mine += glob.glob(os.path.join(root, "proekty", "**", "README.md"), recursive=True)
mine = [p for p in mine if os.path.abspath(p) not in skip]
texts = {p: open(p, encoding="utf-8", errors="ignore").read().lower() for p in mine}
t = open(me, encoding="utf-8").read()

keys = set()
keys |= {m.lower() for m in re.findall(r"`([^`\s/]{4,})`", t)}
keys |= {os.path.basename(m).lower() for m in re.findall(r"`([^`\s]+/[^`\s]+)`", t)}
keys |= {m.lower() for m in re.findall(r"\b[A-Za-z][A-Za-z_-]{4,}\b", t)}
keys |= {m.lower() for m in re.findall(r"(?<=[а-яё,;:] )[А-ЯЁ][а-яё]{3,}", t)}
keys |= {m.lower() for m in re.findall(r"«([^»]{4,30})»", t)}
stop = set("notes diary proekty readme python inbox html https".split())
keys = {k for k in keys if k not in stop}

rows = []
for k in keys:
    hits = [p for p, x in texts.items() if k in x]
    if hits:
        rows.append((len(hits), k, os.path.relpath(sorted(hits)[0], root)))
rows.sort()
for n, k, p in rows[:TOP]:
    print("%3d  %-34s %s" % (n, k[:34], p))
print("опорных слов: %d, найдено в моих файлах: %d" % (len(keys), len(rows)))
# Калибровка 2026-10-18 (мутационная: на версиях заметок В МОМЕНТ ошибки):
#  1) git show ec91f8a:notes/slova-mutanty.md (до поправки про Эрхарта), --bez notes/slova-mutanty.md:
#     «эрхарт → notes/kontinuum.md» на 8-м месте по умолчанию. ПРОЙДЕНО. Первые две версии инструмента
#     НЕ прошли: строка тонула в эхе текущего дневника и новых заметок — отсюда два отсечения выше.
#  2) восстановленная по памяти версия notes/sito-2020.md (до «поправки к поправке»): наверху
#     «iconv → notes/karta-inbox.md» (там «Генеративная поэзия») и proekty/hokku/README.md (Каганов). ПРОЙДЕНО (слабее).
