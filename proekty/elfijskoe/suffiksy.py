"""suffiksy.py [языки] — все суффиксы (speech="suf") квенья из Eldamo: форма, значение, сколько у статьи примеров (ref).
Языки по умолчанию q,nq,mq. Печатает TSV: язык, форма, gloss, число ref. Для прогулки, не для ревизии (19.10)."""
import re, sys
P = "/home/diarai/diarai/inbox/eldamo/src/data/eldamo-data.xml"
langs = set((sys.argv[1] if len(sys.argv) > 1 else "q,nq,mq").split(","))
t = open(P, encoding="utf-8").read()
starts = [m for m in re.finditer(r'<word\b([^>]*)>', t)]
rows = []
for i, m in enumerate(starts):
    a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
    if a.get("speech") != "suf" or a.get("l") not in langs:
        continue
    end = starts[i + 1].start() if i + 1 < len(starts) else len(t)
    body = t[m.end():end]
    nref = len(re.findall(r'<ref\b', body))
    rows.append((a.get("l"), a.get("v", ""), a.get("gloss", "") or a.get("ngloss", ""), nref))
for r in rows:
    print("%s\t%s\t%s\t%d" % r)
print("всего:", len(rows), file=sys.stderr)
