"""Сводка и рекорды по catalog2.csv -> печать (для NOTES.md)."""
import csv, collections
from pegg import to_pegg
cat = list(csv.DictReader(open('catalog2.csv')))
P = lambda c: f"{c['rep']} ({to_pegg(int(c['rep']))}, правил: {c['raw']})"
h = [c for c in cat if c['kind'] == 'highway']
l = [c for c in cat if c['kind'] == 'loop']
print('Дольше всех до шоссе:')
for c in sorted(h, key=lambda c: -int(c['onset']))[:12]:
    print(f"  {P(c)}: {int(c['onset']):,} шагов, период {c['period']}, смещение ({c['dx']},{c['dy']})".replace(',', ' ', 1) if False else f"  {P(c)}: начало {int(c['onset'])}, период {c['period']}, смещение ({c['dx']},{c['dy']})")
print('Самые длинные периоды шоссе:')
for c in sorted(h, key=lambda c: -int(c['period']))[:8]:
    print(f"  {P(c)}: период {c['period']}, смещение ({c['dx']},{c['dy']}), начало {c['onset']}")
print('Дольше всех до петли:')
for c in sorted(l, key=lambda c: -int(c['onset']))[:8]:
    print(f"  {P(c)}: начало {c['onset']}, период {c['period']}")
print('Периоды шоссе (классов):', collections.Counter(int(c['period']) for c in h).most_common(12))
print('Начало шоссе, классов по порядку величины:', sorted(collections.Counter(len(c['onset']) if c['onset'] != '0' else 0 for c in h).items()))
