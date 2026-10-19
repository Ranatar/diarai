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
for lang in langs:
    for m in re.finditer(r'<word\b([^>]*)>', text, re.S):
        a = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
        # омонимы с надстрочным номером (-sta¹, -eg¹) печатаются все, если номер не указан; 2026-10-19 — два ложных «нет» из-за этого
        av = a.get("v", "")
        if (av != v and av.rstrip("¹²³⁴⁵⁶⁷⁸⁹") != v) or a.get("l") != lang:
            continue
        found = True
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
if not found:
    print("— нет статьи %r в языках %s (омонимы с ¹²³ проверены; склонённых форм здесь нет)" % (v, ",".join(langs)))
