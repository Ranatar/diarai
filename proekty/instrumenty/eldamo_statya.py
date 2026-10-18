"""eldamo_statya.py слово [язык] — напечатать статью Eldamo целиком: открывающий тег <word … v="слово"…>,
заметки (notes, HTML снят) и ссылки ref (форма, источник, gloss). Язык по умолчанию q.
2026-10-18, пробуждение 16:40 (перевод положений «Трактата» на квенья)."""
import re, sys, os, html

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
text = open(os.path.join(root, "inbox", "eldamo", "src", "data", "eldamo-data.xml"), encoding="utf-8").read()
v, lang = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "q")
for m in re.finditer(r'<word\b([^>]*)>', text, re.S):
    a = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
    if a.get("v") != v or a.get("l") != lang:
        continue
    # конец статьи: следующий <word на том же или меньшем отступе — грубо берём до 6000 знаков
    body = text[m.end(): m.end() + 6000]
    nxt = re.search(r'\n {0,6}<word\b', body)
    body = body[: nxt.start()] if nxt else body
    print("==", a.get("l"), a.get("v"), "|", a.get("speech", ""), "|", a.get("gloss", ""), a.get("ngloss", ""))
    for n in re.findall(r"<notes><!\[CDATA\[(.*?)\]\]></notes>", body, re.S):
        print("ЗАМЕТКИ:", html.unescape(re.sub(r"<[^>]+>", "", n)).strip()[:1500])
    for r in re.findall(r'<ref\b([^>]*)>', body):
        ra = dict(re.findall(r'([\w-]+)="([^"]*)"', r))
        print("  ref:", ra.get("v"), "|", ra.get("source"), "|", ra.get("gloss", ""))
