"""korpus.py — собрать корпуса для программы-поэта Каганова (веб-порт, inbox/lleo_poet_bundle).
  avtor: все версии hello_there из git (уникальные абзацы)
  tretij: мой дневник (diary/*.md), без заголовков и путей
Пишет proekty/lleo/korpus-avtor.txt и korpus-tretij.txt (в .gitignore не надо: малые)."""
import subprocess, re, glob, os
ROOT = "/home/diarai/diarai"
os.chdir(ROOT)

def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True).stdout

seen, avtor = set(), []
for h in git("log", "--format=%H", "--", "hello_there").split():
    for par in git("show", h + ":hello_there").split("\n"):
        p = par.strip()
        if p and p not in seen:
            seen.add(p); avtor.append(p)

def chist(t):
    t = re.sub(r"`[^`]*`", " ", t)          # пути и код
    t = re.sub(r"\*+|_+|~~[^~]*~~", " ", t)
    t = re.sub(r"https?://\S+", " ", t)
    return t

tretij = []
for f in sorted(glob.glob("diary/*.md")):
    for line in open(f, encoding="utf-8"):
        if line.startswith("#") or line.startswith("файл:"):
            continue
        s = chist(line).strip()
        if s:
            tretij.append(s)

for name, data in (("avtor", avtor), ("tretij", tretij)):
    path = "proekty/lleo/korpus-%s.txt" % name
    open(path, "w", encoding="utf-8").write("\n".join(data) + "\n")
    print(name, len(data), "абзацев,", sum(len(x.split()) for x in data), "слов")
