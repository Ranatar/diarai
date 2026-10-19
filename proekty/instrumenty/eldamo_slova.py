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
    v0 = a.get("v", "")
    # надстрочные номера омонимов (-sta¹, -sta²…) не мешают: ложное «нет» 2026-10-19 вышло именно так
    v = v0.rstrip("¹²³⁴⁵⁶⁷⁸⁹")
    # необязательные буквы в скобках: ilvan(y)a — это и ilvana, и ilvanya (19.10, 09:07: «—» на ilvanya, а статья есть)
    forms = {v}
    if "(" in v:
        forms = {re.sub(r"\(([^)]*)\)", r"\1", v), re.sub(r"\([^)]*\)", "", v)}
    if a.get("l") in langs:
        for f in forms & want:
            seen.setdefault(f, []).append("%s %s «%s»" % (a["l"], v0, (a.get("ngloss") or a.get("gloss", ""))[:70]))
for w in args:
    print("%-12s %s" % (w, "; ".join(seen.get(w, ["—"])[:3])))
