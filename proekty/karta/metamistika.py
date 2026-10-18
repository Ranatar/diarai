"""metamistika.py — как рос «Расширенный словарь метафилософско-метамистической концепции»
(inbox/metamystic-dictionary-extended/, 18 файлов, апрель 2025): число статей «**АББР - Имя**», слов, новые и пропавшие аббревиатуры."""
import os, re
D = "/home/diarai/diarai/inbox/metamystic-dictionary-extended"
def key(f):
    m = re.search(r"-(\d+)(\(1\))?\.txt$", f)
    return (int(m.group(1)), bool(m.group(2))) if m else (0, False)
prev = set()
for f in sorted(os.listdir(D), key=key):
    t = open(os.path.join(D, f), encoding="utf-8", errors="replace").read()
    ab = re.findall(r"\*\*([A-ZА-Я0-9]{1,6})\s*[-–—]\s*([^*]+)\*\*", t)
    s = {a for a, _ in ab}
    nov = sorted(s - prev)
    print("%-42s статей %3d  слов %5d  новые: %s%s" % (f, len(ab), len(t.split()), " ".join(nov[:8]), " …" if len(nov) > 8 else ""))
    prev = s
