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
# 21.10, 09:30: ᴹQ и ᴱQ в Eldamo пишутся через k и без диерезы (talka), поздний Q — через c и ë (talca).
# Я искал talca и написал автору, что у Толкина его нет отдельным словом, а ᴹQ talka «*that much» (PE23/108)
# стояло рядом. Теперь сравнение идёт по ключу: c→k, ë→e, регистр не важен.
# 21.10, 09:44: и qu/kw→q — ᴹQ пишет ilqa, а автор и поздний Q — ilqua.
def key(w):
    return w.lower().replace("qu", "q").replace("kw", "q").replace("c", "k").replace("ë", "e")
want = {key(w) for w in args}
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
        for f in {key(x) for x in forms} & want:
            g = (a.get("ngloss") or a.get("gloss", ""))[:70]
            # 21.10, 09:08: пустая глосса у q walda — это ссылка <see v="valda"/> («excited, wild»);
            # письмо 20 автору ушло с «walda — пустая глосса». Теперь ссылка печатается.
            if not g:
                s = re.match(r'\s*<see\b([^>]*)/>', xml[m.end():m.end() + 300])
                if s:
                    sa = dict(re.findall(r'([\w-]+)="([^"]*)"', s.group(1)))
                    g = "→ см. %s %s" % (sa.get("l", "?"), sa.get("v", "?"))
            seen.setdefault(f, []).append("%s %s «%s»" % (a["l"], v0, g))
# 21.10, 10:20: ложное «нет» про tyen — формы нет как статьи, но есть ref «tyen | PE22/166 | to you» в статье tye.
# Теперь для слов без статьи ищутся ref-формы (склонённые, спряжённые) с родительской статьёй.
import bisect
_wpos = [(m.start(), m.group(1)) for m in re.finditer(r'<word\b([^>]*)>', xml)]
_starts = [p for p, _ in _wpos]
refhits = {}
_need = {key(w) for w in args}  # всегда: одноимённая статья другого языка (eq tyen «then») прятала q ref tyen «to you»
if _need:
    for m in re.finditer(r'<ref\b([^>]*)>', xml):
        ra = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
        k = key(ra.get("v", ""))
        if k in _need:
            i = bisect.bisect_right(_starts, m.start()) - 1
            pa = dict(re.findall(r'([\w-]+)="([^"]*)"', _wpos[i][1])) if i >= 0 else {}
            if pa.get("l") in langs:
                refhits.setdefault(k, []).append("ref в %s %s: %s «%s»" % (pa.get("l"), pa.get("v"), ra.get("source", ""), ra.get("gloss", "")[:40]))
# 21.10: было [:3], и q tenna¹ «until» пряталось за тремя другими tenna. Теперь все, с числом.
for w in args:
    if key(w) in refhits:
        h = refhits[key(w)]
        line = "; ".join(h[:4]) + ("  [%d]" % len(h) if len(h) > 4 else "")
        if key(w) not in seen:
            print("%-12s — статьи нет; %s" % (w, line))
            continue
        print("%-12s %s" % (w, "; ".join(seen[key(w)])))
        print("%-12s   + %s" % ("", line))
        continue
    hits = seen.get(key(w), ["—"])
    print("%-12s %s" % (w, "; ".join(hits)) + ("  [%d]" % len(hits) if len(hits) > 3 else ""))
