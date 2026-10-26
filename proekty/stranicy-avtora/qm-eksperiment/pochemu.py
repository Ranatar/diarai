"""Почему слово с элементами в <ref> не попало в таблицу аффиксов: печатает его элементы
(с id или кандидатами) после правки lexicon.py.
Запуск: python3 -I pochemu.py írima vanima ...
"""
import sys, os

KOREN = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'ext', 'quettamin')
sys.path.insert(0, os.path.abspath(KOREN))
from shared.pipeline import build_branch   # noqa: E402

d = build_branch('quenya')
by_id = {e['id']: e for e in d['lexicon']}
for f in sys.argv[1:]:
    for e in d['lexicon']:
        if e['form'] == f:
            print(e['lang'], f, e.get('mark', ''), 'neo' if e.get('neo') else '')
            for x in e.get('elements', []):
                cel = by_id.get(x.get('id'))
                print('   ', x.get('form'), '->', (cel['lang'] + ' ' + cel['form']) if cel else ('кандидаты ' + str(x.get('candidates')) if x.get('candidates') else 'не найдено'))
