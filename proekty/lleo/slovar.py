"""slovar.py корпус.txt выход.tsv — ударения для слов корпуса из базы автора (lleo_poet_bundle/bases/base_ru.txt, 1,77 млн форм).
Формат вывода — «слово<TAB>номер_ударного_слога», его понимает importStressDict веб-порта."""
import re, sys
BASE = "/home/diarai/diarai/inbox/lleo_poet_bundle/bases/base_ru.txt"
words = set(w.lower() for w in re.findall(r"[А-Яа-яЁё]+(?:-[А-Яа-яЁё]+)?", open(sys.argv[1], encoding="utf-8").read()))
out, found = [], set()
for line in open(BASE, encoding="utf-8"):
    head = line.split(" ← ", 1)[0].strip()
    if "|" not in head:
        continue
    w, n = head.split("|", 1)
    if w in words and w not in found and n.isdigit():
        found.add(w); out.append("%s\t%s" % (w, n))
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(out) + "\n")
print("слов в корпусе:", len(words), "с ударением из базы:", len(found))
