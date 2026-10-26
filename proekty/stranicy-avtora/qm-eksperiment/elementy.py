"""Эксперимент к замечанию 1 (`../quettamin.md`): что меняется, если Quettamin берёт
элементы и из <ref>. Запускать на копии ext/quettamin с правкой lexicon.py:
  QM_REF_ELEMENTS=0 python3 -I elementy.py   — как у автора
  QM_REF_ELEMENTS=1 python3 -I elementy.py   — с элементами из ref
Печатает: сколько статей с элементами, сколько случаев аффиксов и сложений, случаи -ima.
"""
import sys, os

KOREN = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'ext', 'quettamin')
sys.path.insert(0, os.path.abspath(KOREN))
from shared.pipeline import build_branch   # noqa: E402

for vetv in sys.argv[1:] or ['quenya']:
    d = build_branch(vetv)
    lex = d['lexicon']
    s_el = sum(1 for e in lex if e.get('elements'))
    iz_ref = sum(1 for e in lex if any(x.get('from_ref') for x in e.get('elements', ())))
    print(f'{vetv}: статей {len(lex)}, с элементами {s_el} (из ref: {iz_ref}); '
          f"аффиксов: {len(d['affixes']['cases'])}; сложений: {len(d['junctions']['cases'])}")
    for c in d['affixes']['cases']:
        if c.get('affix_form', '').startswith('-ima'):
            print('   ', c['form'], '=', c['base_form'], '+', c['affix_form'], c['junction'], 'удл.' if c['lengthened'] else '')
