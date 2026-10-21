"""peresmotr_net.py — пересмотр моих «в Eldamo нет».
Собирает строки в notes/, proekty/, diary/, где сказано, что слова в Eldamo нет, берёт из них курсивные
латинские слова (*слово*) и печатает их списком через пробел (для eldamo_slova.py).
С --gde печатает файл:строку для каждого слова.
2026-10-21, 12:2x: после ложного «нет» про maura/cimba (дефис глагольного заголовка)."""
import os, re, sys
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
PAT = re.compile(r"(в Eldamo нет|нет в Eldamo|в Eldamo не наш|Eldamo: нет|в Eldamo такого слова нет|в Eldamo — нет)")
WORD = re.compile(r"\*\\?\*?([A-Za-záéíóúëäöüñÁÉÍÓÚ-]{3,})\*")
gde = "--gde" in sys.argv
words = {}
for top in ("notes", "proekty", "diary"):
    for d, _, fs in os.walk(os.path.join(root, top)):
        for f in fs:
            if not f.endswith((".md", ".tsv")):
                continue
            p = os.path.join(d, f)
            for n, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
                if PAT.search(line):
                    for w in WORD.findall(line):
                        words.setdefault(w, []).append("%s:%d" % (os.path.relpath(p, root), n))
if gde:
    for w in sorted(words):
        print(w, " ".join(words[w][:3]))
else:
    print(" ".join(sorted(words)))
