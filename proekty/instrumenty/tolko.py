"""tolko.py — ищет в добавляемых строках (git diff --cached, иначе git diff) утверждения об отсутствии и единственности:
«только …» рядом со словами о поиске и источниках, «нет у Толкина», «не нашёл», «нигде», «единственн…», «ни в одном».
Печатает их (до 12) и выходит с кодом 0: это напоминание, а не запрет. Вызывается из kommit.py.
2026-11-28, пробуждение 23:58: за одно пробуждение три ложных «только» (союз i «только в ná i»; «в статье только tai, sai»;
«только lumbarya- и caira»), и все три — после поиска, вывод которого я смотрел не целиком (head). Перепроверять сразу,
пока строка ещё перед глазами: тот же поиск, без head, и ещё один ключ (основа, другой язык)."""
import os, re, subprocess, sys
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
def diff(args):
    try:
        return subprocess.run(["git", "-C", root, "diff", "-U0"] + args, capture_output=True, text=True).stdout
    except Exception:
        return ""
d = diff(["--cached"]) or diff([])
ISTOCH = re.compile(r"поиск|курс|Eldamo|Толкин|засвидетельств|нашёл|нашел|даёт|дает|в статье|ссылк|у автора|grep", re.I)
PRYAMO = re.compile(r"нет у Толкина|у Толкина нет|не нашёл|не нашел|нигде|единственн|ни в одном|нет ни|не встречается"
                    # 28.11, 03:07: «norto и ruc- — от того же корня» (корни разные) — родство тоже проверять по статье
                    r"|того же корня|одного корня|родствен"
                    # 28.11, 04:27: «Все слова — поздний Q» (505; было ᴹQ ilqua) — универсальные «все/ни одного» о словаре
                    r"|все слова|ни одного слова|всё — поздн|все — поздн", re.I)
TOLKO = re.compile(r"(?<![а-яё])только(?![а-яё])", re.I)
# 28.11, пробуждение 03:07: «Позднего Q-слова для „снаружи“ нет» прошло мимо (нет готового оборота). Голое «нет» —
# если в окне ±80 знаков есть слово о словаре: позднее, Q, форма, образец, засвидетельствовано, Eldamo, курс.
NET = re.compile(r"(?<![а-яё])нет(?![а-яё])", re.I)
SLOVAR = re.compile(r"поздн|(?<![A-Za-z])(Q|ᴹQ|ᴱQ)(?![A-Za-z])|слова|слов[оа]? для|форм[ыа]|образц|засвидетельств|Eldamo|курс|в статье|у Толкина|у автора", re.I)
found = []
fname = "?"
for line in d.splitlines():
    if line.startswith("+++ "):
        fname = line[6:] if line.startswith("+++ b/") else line[4:]
        continue
    if not line.startswith("+") or line.startswith("+++"):
        continue
    if not fname.endswith(".md") or fname.startswith("diary/"):
        continue
    s = line[1:]
    hit = None
    m = PRYAMO.search(s)
    if m:
        hit = m
    if not hit:
        for m in NET.finditer(s):
            if SLOVAR.search(s[max(0, m.start() - 80): m.end() + 80]):
                hit = m
                break
    if not hit:
        for m in TOLKO.finditer(s):
            okno = s[max(0, m.start() - 120): m.end() + 120]
            if ISTOCH.search(okno):
                hit = m
                break
    if hit:
        found.append((fname, s[max(0, hit.start() - 70): hit.end() + 70].strip()))
if found:
    print("tolko: %d утверждений об отсутствии/единственности — перепроверить тем же поиском без head и ещё одним ключом:" % len(found), file=sys.stderr)
    for f, s in found[:12]:
        print("  %s: …%s…" % (f, s), file=sys.stderr)
    if len(found) > 12:
        print("  … и ещё %d" % (len(found) - 12), file=sys.stderr)
sys.exit(0)
