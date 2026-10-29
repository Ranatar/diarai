"""Сверка с вики Golly (Ed Pegg's Busy Beaver Turmite Challenge, 2s2c).
python3 cmp/jeronimus.py WIKI_DIR -> печатает для каждого чужого правила мой класс и мою судьбу."""
import sys, re, csv, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pegg import from_pegg
from canon3 import CANON3
from canon2 import CANON2
wiki = sys.argv[1]
cat = {int(r['rep']): r for r in csv.DictReader(open('catalog2.csv'))}
def rules_in(text):
    out = []
    for m in re.finditer(r'\{\{\{(\d),(\d),(\d)\},\s*\{(\d),(\d),(\d)\}\},\s*\{\{(\d),(\d),(\d)\},\s*\{(\d),(\d),(\d)\}\}\}?', text):
        out.append(''.join(m.groups()))
    for m in re.finditer(r't22r(\d{12})\b', text):
        out.append(m.group(1))
    return out
main = open(os.path.join(wiki, 'EdPeggsBusyBeaverTurmiteChallenge.md')).read()
a, b = main.index('Resolved 2-state 2-color'), main.index('Resolved 2-state 3-color')
u = main.index('Unresolved 2-state 2-color')
sec = {'resolved': main[a:b], 'unres_main': main[u:u+20000].split('<h3>')[1] if '<h3>' in main[u+5:u+20000] else main[u:u+20000]}
sec['unres_sub'] = open(os.path.join(wiki, 'UnresolvedTurmites2States2Colors.md')).read()
for name, text in sec.items():
    seen = {}
    for p in rules_in(text):
        r = from_pegg(p); c = CANON3.get(CANON2[r], CANON2[r])
        seen.setdefault(c, []).append(p)
    print(f'## {name}: правил {sum(map(len,seen.values()))}, моих классов {len(seen)}')
    for c, ps in seen.items():
        row = cat.get(c, {})
        print(c, ps[0], row.get('kind'), row.get('onset'), row.get('period'), row.get('growth_to'), sep='\t')
