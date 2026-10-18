"""hwph_statya.py 'Lemma' out.txt — вынуть статью HWPh из inbox/hwph-xml/site.xml как текст (теги сняты)."""
import re, sys, html
lemma, out = sys.argv[1], sys.argv[2]
buf, on = [], False
for line in open("inbox/hwph-xml/site.xml", encoding="utf-8"):
    if not on and ('<article ' in line and 'lemma="%s"' % lemma in line):
        on = True
    if on:
        buf.append(line)
        if "</article>" in line:
            break
t = "".join(buf)
t = re.sub(r"<note\b[^>]*>.*?</note>", lambda m: " [" + re.sub(r"<[^>]+>", "", m.group(0))[:0] + "]", t, flags=re.S)
t = re.sub(r"</p>|<br\s*/?>", "\n", t)
t = html.unescape(re.sub(r"<[^>]+>", "", t))
t = re.sub(r"[ \t]+", " ", t)
open(out, "w", encoding="utf-8").write(t)
print(len(t.split()), "слов")
