"""Quettamin: статьи лексикона по форме (подстрока или точное совпадение).
Запуск: python3 -I qm_slovo.py ФОРМА [--sub] [quenya|sindarin]
Печатает язык, форму, значение, часть речи, родителей/элементы.
"""
import json, sys, os

args = [a for a in sys.argv[1:] if not a.startswith('--')]
sub = '--sub' in sys.argv
forma = args[0]
vetv = args[1] if len(args) > 1 else 'quenya'
koren = os.path.join(os.path.dirname(__file__), '..', '..', 'ext', 'quettamin', 'branches', vetv, 'data')
lex = json.load(open(os.path.join(koren, 'lexicon.json'), encoding='utf-8'))
n = 0
for e in lex:
    f = e.get('form', '')
    if (forma in f) if sub else (f == forma):
        n += 1
        rod = ', '.join(f"{p['lang']} {p['form']}" for p in e.get('parents', []))
        el = ', '.join(f"{p['lang']} {p['form']}" for p in e.get('elements', []))
        print(f"{e['lang']:<4} {f:<18} «{e.get('gloss','')}» {e.get('speech','')} {e.get('mark','')}"
              + (f" | от: {rod}" if rod else '') + (f" | элементы: {el}" if el else ''))
print('статей:', n)
