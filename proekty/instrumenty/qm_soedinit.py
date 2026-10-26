"""Quettamin (автор, inbox/quettamin; копия в ext/quettamin): соединить два элемента
на последней стадии (сложение или основа + аффикс) и показать ранжированные варианты.

Запуск: python3 -I qm_soedinit.py ПЕРВЫЙ ВТОРОЙ [ПЕРВЫЙ ВТОРОЙ ...] [--vetv sindarin] [--n 8]
Элемент — форма как в Eldamo (taima, -enca, quetta). При омонимах берётся статья
языка q, затем nq, затем остальные; все кандидаты печатаются.
Сборка ветви занимает ~30 с.
"""
import sys, os

KOREN = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'ext', 'quettamin')
sys.path.insert(0, os.path.abspath(KOREN))
from shared.pipeline import build_branch          # noqa: E402
from shared.sequencer import Sequencer            # noqa: E402
from shared import compound, junctions, affixes   # noqa: E402

args = sys.argv[1:]
vetv = 'quenya'; n = 8
if '--vetv' in args:
    i = args.index('--vetv'); vetv = args[i + 1]; del args[i:i + 2]
if '--n' in args:
    i = args.index('--n'); n = int(args[i + 1]); del args[i:i + 2]

data = build_branch(vetv)
seq = Sequencer(data)
lexicon = {e['id']: e for e in data['lexicon']}
table = junctions.learn(data['junctions']['cases'])
amodel = affixes.learn(data['affixes']['cases'])
PORYADOK = {'q': 0, 's': 0, 'nq': 1, 'ns': 1}


def najti(forma):
    c = [e for e in data['lexicon'] if e['form'] == forma]
    c.sort(key=lambda e: PORYADOK.get(e['lang'], 2))
    return c


for k in range(0, len(args) - 1, 2):
    a, b = args[k], args[k + 1]
    ca, cb = najti(a), najti(b)
    print(f'\n=== {a} + {b}')
    for nm, cc in ((a, ca), (b, cb)):
        print(f'  {nm}: ' + '; '.join(f"{e['lang']} «{e.get('gloss', '')}» {e['id']}" for e in cc) or '  нет в лексиконе')
    if not ca or not cb:
        continue
    vs = compound.predict(lexicon, seq, [ca[0]['id'], cb[0]['id']], 'late', 99, table=table, affix_model=amodel)
    for v in vs[:n]:
        dop = ''
        if v.get('junction') and v['junction'] != [0, 0, '']:
            dop += f" стык={v['junction']}"
        if v.get('ending') and v['ending'] != [0, '']:
            dop += f" конец={v['ending']}"
        if v.get('adjustments'):
            dop += ' попр.=' + ','.join(x['rule'] for x in v['adjustments'])
        if v.get('analogues'):
            dop += ' аналоги=' + ','.join(str(x) for x in v['analogues'][:4])
        print(f"  {v['form']:<20} {v.get('score', '')!s:<7} из {v.get('elements')} {dop}")
