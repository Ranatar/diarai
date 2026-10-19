"""eldamo_slova.py слово [слово …] [--l q,nq,mq,eq] — быстро: есть ли каждое слово в Eldamo (точная форма v),
с языком и значением. Для подстрочника чужого текста целиком. Нули печатаются: отсутствие — тоже результат,
но «нет» значит только «нет такой словарной формы»: склонённых и спряжённых форм здесь нет.
2026-10-19 (heredoc с фигурными скобками и кавычками Bash отклоняет — поэтому файлом)."""
import re, sys, os
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
args = sys.argv[1:]
langs = ["q", "nq", "mq", "eq"]
if "--l" in args:
    i = args.index("--l"); langs = args[i + 1].split(","); del args[i:i + 2]
xml = open(os.path.join(root, "inbox", "eldamo", "src", "data", "eldamo-data.xml"), encoding="utf-8").read()
want = set(args)
seen = {}
for m in re.finditer(r'<word\b([^>]*)>', xml):
    a = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
    v = a.get("v", "")
    if v in want and a.get("l") in langs:
        seen.setdefault(v, []).append("%s «%s»" % (a["l"], (a.get("ngloss") or a.get("gloss", ""))[:70]))
for w in args:
    print("%-12s %s" % (w, "; ".join(seen.get(w, ["—"])[:3])))
