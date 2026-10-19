"""eldamo_statya.py слово [язык] — напечатать статью Eldamo целиком: открывающий тег <word … v="слово"…>,
заметки (notes, HTML снят) и ссылки ref (форма, источник, gloss). Язык по умолчанию q.
2026-10-18, пробуждение 16:40 (перевод положений «Трактата» на квенья)."""
import re, sys, os, html

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
text = open(os.path.join(root, "inbox", "eldamo", "src", "data", "eldamo-data.xml"), encoding="utf-8").read()
LIMIT = 1500
if "--polno" in sys.argv:   # --polno: заметки целиком (грамматические статьи длинные)
    sys.argv.remove("--polno"); LIMIT = None
v = sys.argv[1]
# Язык: если не указан — сначала q, а если в q нет — mq, nq, eq (19.10, 09:07: mauya- есть только в ᴹQ,
# и без языка я получил «нет статьи» — чуть не третий ложный «нет» за сутки).
langs = [sys.argv[2]] if len(sys.argv) > 2 else ["q", "mq", "nq", "eq"]
found = False
# 19.10, 21:56: раньше после первого найденного языка поиск обрывался, и ᴺQ valda- «to matter»,
# ᴱQ valda «worth» за q valda «excited, wild» были не видны — ложное «нет». Теперь в конце
# печатается список одноимённых статей во всех квенийских языках.
ALL = {"q", "mq", "nq", "eq"}
others = {}
shown = set()
for lang in langs:
    for m in re.finditer(r'<word\b([^>]*)>', text, re.S):
        a = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
        # омонимы с надстрочным номером (-sta¹, -eg¹) печатаются все, если номер не указан; 2026-10-19 — два ложных «нет» из-за этого
        av = a.get("v", "")
        # и необязательные буквы в скобках: ilvan(y)a находится и по ilvanya, и по ilvana (19.10; 524 таких заголовка)
        base = av.rstrip("¹²³⁴⁵⁶⁷⁸⁹")
        forms = {av, base, re.sub(r"\(([^)]*)\)", r"\1", base), re.sub(r"\([^)]*\)", "", base)}
        # и глагол с дефисом: valda находит valda- (19.10, 21:56: valda- «to matter» не нашёлся)
        forms |= {f.rstrip("-") for f in forms}
        if v not in forms:
            continue
        if a.get("l") != lang:
            if a.get("l") in ALL and (a.get("l"), av) not in others:
                others[(a.get("l"), av)] = (a.get("gloss", "") + " " + a.get("ngloss", "")).strip()
            continue
        found = True
        shown.add(a.get("l"))
        # конец статьи: следующий <word на том же или меньшем отступе.
        # Было «до 6000 знаков»: у грамматических статей (speech="grammar": genitive, elision…) заметки длиннее,
        # закрывающий ]]></notes> не попадал в окно, и статья печаталась пустой (19.10, 09:07, «elision»).
        nxt = re.compile(r'\n {0,6}<word\b').search(text, m.end())
        body = text[m.end(): nxt.start() if nxt else len(text)]
        print("==", a.get("l"), a.get("v"), "|", a.get("speech", ""), "|", a.get("gloss", ""), a.get("ngloss", ""))
        for n in re.findall(r"<notes><!\[CDATA\[(.*?)\]\]></notes>", body, re.S):
            print("ЗАМЕТКИ:", html.unescape(re.sub(r"<[^>]+>", "", n)).strip()[:LIMIT])
        for r in re.findall(r'<ref\b([^>]*)>', body):
            ra = dict(re.findall(r'([\w-]+)="([^"]*)"', r))
            print("  ref:", ra.get("v"), "|", ra.get("source"), "|", ra.get("gloss", ""))
    if found:
        break
others = {k: g for k, g in others.items() if k[0] not in shown}
if others:
    print("ЕЩЁ (одноимённые статьи в других языках; полностью — с языком вторым аргументом):")
    for (l, w), g in others.items():
        print("  ", l, w, "|", g)
if not found:
    print("— нет статьи %r в языках %s (омонимы с ¹²³ проверены; склонённых форм здесь нет)" % (v, ",".join(langs)))
