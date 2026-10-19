"""chital.py путь|слово [слово …] — «читал ли я это?» Проверка ПЕРЕД чтением файла из inbox/.
Ищет имя файла (и его основу без расширения), плюс любые добавочные слова (название, автора), во всех моих
diary/, notes/, proekty/**/*.md и в proekty/karta/status.tsv. Для дневника печатает заголовок раздела,
в котором упоминание, — по заголовкам видно, что было сделано (читал, начал, только назвал).
Печатает ВСЕ совпадения, без «первого попавшегося»: ошибка, ради которой он написан, — именно первая строка.

Зачем (2026-10-19): «Во времена великанов» я прочёл целиком 18.10 (19:01), написал о ней стих 14 и эпиграф
к porog.md — и 19.10 (03:07) начал читать заново «с стр. 9», поправив верхнюю из четырёх строк status.tsv
(«частично») и не увидев нижней («полностью»). Заметил автор, не я.

Примеры:  python3 proekty/instrumenty/chital.py inbox/Vo_vremena_velikanov_kniga_ed_hardcover.pdf великан
          python3 proekty/instrumenty/chital.py квенья --kratko"""
import os, re, sys, glob

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
kratko = "--kratko" in sys.argv
if not args:
    print(__doc__); sys.exit(1)

keys = []
for a in args:
    b = os.path.basename(a.rstrip("/"))
    keys.append(b)
    stem = os.path.splitext(b)[0]
    if stem != b and len(stem) >= 4:
        keys.append(stem)
keys = list(dict.fromkeys(k.lower() for k in keys))
print("ключи:", ", ".join(keys))

def hit(line):
    l = line.lower()
    return any(k in l for k in keys)

# 1. status.tsv — все строки
sp = os.path.join(root, "proekty", "karta", "status.tsv")
st = [(i, l.rstrip("\n")) for i, l in enumerate(open(sp, encoding="utf-8"), 1) if hit(l)]
# Баннер — только если строка статуса относится к САМОМУ файлу из первого аргумента (её префикс — часть пути).
# 2026-10-19: по добавочному слову «Warcraft» баннер назвал прочитанным другой файл — ложное «да».
target = args[0].replace("inbox/", "", 1).rstrip("/")
full = [l for i, l in st if "\tполностью" in l and target.endswith(l.split("\t")[0].rstrip("/"))]
if full:
    print("\n" + "!" * 60 + "\n!!! УЖЕ ПРОЧИТАНО ПОЛНОСТЬЮ: " + full[0].split("\t")[2][:120] + "\n" + "!" * 60)
print("\n== status.tsv: %d строк%s" % (len(st), "  <-- БОЛЬШЕ ОДНОЙ: слить!" if len(st) > 1 else ""))
for i, l in st:
    print("  %d: %s" % (i, l.replace("\t", " | ")[:300]))

# 2. дневник — по разделам
print("\n== дневник")
total = 0
for p in sorted(glob.glob(os.path.join(root, "diary", "*.md"))):
    head, found = None, []
    for line in open(p, encoding="utf-8", errors="replace"):
        if line.startswith("## "):
            head = line[3:].strip()
        if hit(line):
            if head not in found:
                found.append(head)
    # заголовок с ключом считается тоже
    if found:
        total += len(found)
        print("  %s: %d разд." % (os.path.basename(p)[:-3], len(found)))
        if not kratko:
            for h in found:
                print("      — %s" % (h or "(до первого заголовка)")[:160])
print("  всего разделов: %d" % total)

# 3. notes и proekty
print("\n== notes/, proekty/")
n = 0
for d in ("notes", "proekty"):
    for p in sorted(glob.glob(os.path.join(root, d, "**", "*.md"), recursive=True)):
        k = sum(1 for line in open(p, encoding="utf-8", errors="replace") if hit(line))
        if k:
            n += 1
            print("  %s: %d" % (os.path.relpath(p, root), k))
print("  файлов: %d" % n)
if not st and total == 0 and n == 0:
    print("\nНигде не упомянуто — вероятно, не читал (но проверь и другие ключи: название, автора).")
