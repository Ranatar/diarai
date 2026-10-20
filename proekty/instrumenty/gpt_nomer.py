"""gpt_nomer.py [НОМЕР …] — картинки корня inbox/gpt/ в порядке даты и времени из имени
(«ChatGPT Image 26 апр. 2025 г., 17_51_15.png»), с номерами, как в notes/gpt-koren.md.

20.10, пробуждение 21:07: по времени изменения файлов (mtime) порядок заметки не восстанавливается
(350 выходил 29 сентября, а в заметке это 15 октября). Без аргументов — сводка и файлы без даты в имени.
"""
import os, re, sys

MES = dict(янв=1, февр=2, мар=3, апр=4, мая=5, июн=6, июл=7, авг=8, сент=9, окт=10, нояб=11, дек=12)
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "inbox", "gpt")
RX = re.compile(r"(\d+) ([а-я]+)\.? (\d{4}) г\., (\d+)_(\d+)_(\d+)")

def klyuch(f):
    m = RX.search(f)
    if not m:
        return (9999, 0, 0, 0, 0, 0, f)
    dd, mon, yy, h, mi, s = m.groups()
    return (int(yy), MES.get(mon, 0), int(dd), int(h), int(mi), int(s), f)

fs = [f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f)) and re.search(r"\.(png|jpe?g|webp)$", f, re.I)]
fs.sort(key=klyuch)
if len(sys.argv) > 1:
    for a in sys.argv[1:]:
        i = int(a)
        print("%03d  %s" % (i, fs[i] if 0 <= i < len(fs) else "— нет такого номера"))
else:
    bez = [f for f in fs if klyuch(f)[0] == 9999 or klyuch(f)[1] == 0]
    print("картинок: %d; без распознанной даты: %d" % (len(fs), len(bez)))
    for f in bez:
        print("   ", f)
