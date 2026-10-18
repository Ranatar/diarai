"""eldamo_slovo.py регэксп [язык] — слова Eldamo, чья форма v целиком подходит под регэксп (по умолчанию все языки).
python3 eldamo_slovo.py "t[aá]ra?" q"""
import re, sys, os

xml = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "inbox", "eldamo", "src", "data", "eldamo-data.xml")
pat = re.compile(sys.argv[1] + r"$")
lang = sys.argv[2] if len(sys.argv) > 2 else None
for m in re.finditer(r'<word\b[^>]*>', open(xml, encoding="utf-8").read()):
    tag = m.group(0)
    v = re.search(r'\bv="([^"]+)"', tag)
    l = re.search(r'\bl="([^"]+)"', tag)
    if not v or not l or (lang and l.group(1) != lang):
        continue
    if pat.match(v.group(1)):
        g = re.search(r'gloss="([^"]*)"', tag)
        print(l.group(1), v.group(1), "—", g.group(1) if g else "")
