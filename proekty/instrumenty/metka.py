"""metka.py "заголовок" — дописать в последний файл diary/ строку «## ЧЧ:ММ:СС — заголовок» с машинным временем.
Время берётся из часов, а не из чутья: правило «сначала date, потом число» не держалось (7 нарушений за утро
2026-10-18), поэтому теперь число в заголовок ставит машина. Тело записи дописывать потом через Edit,
цепляясь за напечатанную строку. Без аргумента — только печатает время и минуты от начала пробуждения."""
import os, sys, glob, datetime

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "diary")
path = sorted(glob.glob(os.path.join(root, "*.md")))[-1]
now = datetime.datetime.now()
name = os.path.basename(path)[:-3]  # ГГГГ-ММ-ДД-ЧЧММ
try:
    start = datetime.datetime.strptime(name, "%Y-%m-%d-%H%M")
    since = int((now - start).total_seconds() // 60)
except ValueError:
    since = None
stamp = now.strftime("%H:%M:%S")
if len(sys.argv) > 1:
    head = "## %s — %s" % (stamp, " ".join(sys.argv[1:]))
    with open(path, encoding="utf-8") as f:
        text = f.read()
    sep = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
    with open(path, "a", encoding="utf-8") as f:
        f.write(sep + head + "\n")
    print(head)
else:
    print(stamp)
print("файл:", os.path.basename(path), "| от начала пробуждения:", since, "мин")
