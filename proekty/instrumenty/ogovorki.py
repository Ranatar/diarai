"""ogovorki.py — как менялись оговорки в моём разделе CLAUDE.md от коммита к коммиту.
Для каждой версии файла в истории git берётся текст ниже «Раздел, который принадлежит тебе»,
считаются строки, слова и оговорки («по памяти», «вывожу», «не проверял», «(??)», «кажется»,
«видимо», «возможно», «вероятно», «скорее всего», «не знаю»). Печатает таблицу по времени.
Вопрос: гибнут ли малые слова, когда я «переписываю, а не дописываю»?"""
import re, subprocess, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
HEDGES = ["по памяти", "вывожу", "не проверял", "не проверено", "(??)", "кажется", "видимо",
          "возможно", "вероятно", "скорее всего", "не знаю"]

def git(*a):
    return subprocess.run(["git", "-C", ROOT] + list(a), capture_output=True, text=True).stdout

log = git("log", "--format=%H %ad", "--date=format:%m-%d %H:%M", "--reverse", "--", "CLAUDE.md").split("\n")
prev = None
print("%-12s %5s %6s %5s  %s" % ("когда", "строк", "слов", "огов", "на 1000 слов"))
for line in log:
    if not line.strip():
        continue
    h, when = line.split(" ", 1)
    text = git("show", "%s:CLAUDE.md" % h)
    m = text.find("Раздел, который принадлежит тебе")
    if m < 0:
        continue
    sec = text[m:]
    low = sec.lower()
    n = sum(low.count(x) for x in HEDGES)
    words = len(re.findall(r"\w+", sec))
    key = (len(sec.splitlines()), words, n)
    if key == prev:
        continue
    prev = key
    print("%-12s %5d %6d %5d  %5.1f" % (when, key[0], words, n, 1000.0 * n / max(words, 1)))
