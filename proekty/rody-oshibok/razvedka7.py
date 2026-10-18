"""razvedka7.py — РАЗВЕДКА к тесту 7 (не тест, не предрегистрировано): цитаты в «ёлочках» (≥ 6 слов) не дальше 300
знаков от «Хайдеггер» в inbox/**/*.md|html|txt — есть ли их слова подряд в inbox/lleo_dip/heid.txt («Вопрос о технике»).
Печатает: найдено подряд / найдено ≥ 80 % слов по порядку в окне / нет. Цель — понять, сколько цитат вообще
из этого текста, чтобы поставить честный тест."""
import re, glob, os
def norm(s): return re.findall(r"[а-я]+", s.lower().replace("ё", "е"))
heid = norm(open("/home/diarai/diarai/inbox/lleo_dip/heid.txt", encoding="cp866", errors="replace").read())
hj = " " + " ".join(heid) + " "
pos = {}
for i, w in enumerate(heid): pos.setdefault(w, []).append(i)
files = [p for ext in ("md", "html", "txt") for p in glob.glob("/home/diarai/diarai/inbox/**/*." + ext, recursive=True)
         if "node_modules" not in p and "lleo_dip" not in p]
found = []
for p in files:
    try: t = open(p, encoding="utf-8").read()
    except Exception: continue
    for m in re.finditer(r"Хайдеггер", t):
        win = t[max(0, m.start() - 300): m.end() + 300]
        for q in re.findall(r"«([^«»]{30,400})»", win):
            w = norm(q)
            if len(w) < 6: continue
            exact = (" " + " ".join(w) + " ") in hj
            # доля слов цитаты, которые есть в корпусе вообще
            share = sum(1 for x in w if x in pos) / len(w)
            found.append((exact, round(share, 2), os.path.relpath(p, "/home/diarai/diarai/inbox"), q[:90]))
seen = set(); uniq = []
for f in found:
    if f[3] in seen: continue
    seen.add(f[3]); uniq.append(f)
print("цитат рядом с «Хайдеггер»:", len(uniq), "| дословно в «Вопросе о технике»:", sum(1 for f in uniq if f[0]))
for f in sorted(uniq, key=lambda x: (-x[0], -x[1]))[:25]:
    print("%-5s %.2f  %-45s %s" % ("ДА" if f[0] else "—", f[1], f[2][:45], f[3]))
