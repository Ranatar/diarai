"""Quettamin: засвидетельствованные (в Eldamo) производные с данным аффиксом.
Запуск: python3 -I qm_affiks.py -enca [quenya|sindarin]
Читает ext/quettamin/branches/<ветвь>/data/affixes.json (копия inbox/quettamin).
"""
import json, sys, os

aff = sys.argv[1]
vetv = sys.argv[2] if len(sys.argv) > 2 else 'quenya'
koren = os.path.join(os.path.dirname(__file__), '..', '..', 'ext', 'quettamin', 'branches', vetv, 'data')
d = json.load(open(os.path.join(koren, 'affixes.json'), encoding='utf-8'))
n = 0
for c in d['cases']:
    if c.get('affix_form', '').rstrip('¹²³⁴⁵') == aff:
        n += 1
        print(f"{c['form']:<16} = {c['base_form']:<10} + {c['affix_form']:<8} фон.: {c['a']} + {c['b']} -> {c['c']}"
              f"  стык={c['junction']} конец={c['ending']} удл.={c['lengthened']}")
print('случаев:', n)
print('ключи верхнего уровня:', list(d.keys()))
