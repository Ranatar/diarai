"""Сколько статей Eldamo имеют <element> только внутри <ref>, а не прямыми потомками <word>.
Quettamin (shared/lexicon.py) читает только прямые — такие слова для него без элементов.
Запуск: python3 -I elementy_v_ref.py [язык=q] [--primery N]
"""
import sys, os, collections
import xml.etree.ElementTree as ET

yaz = next((a for a in sys.argv[1:] if not a.startswith('--') and not a.isdigit()), 'q')
n_pr = int(sys.argv[sys.argv.index('--primery') + 1]) if '--primery' in sys.argv else 15
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
tree = ET.parse(os.path.join(root, 'inbox', 'eldamo', 'src', 'data', 'eldamo-data.xml'))
pryamye = tolko_ref = vsego = 0
s_ima = []
primery = []
slov = [0]
for w in tree.iter('word'):
    if w.get('l') != yaz:
        continue
    vsego += 1
    d = w.findall('element')
    r = [e for ref in w.findall('ref') for e in ref.findall('element')]
    if d:
        pryamye += 1
    elif r:
        tolko_ref += 1
        if ' ' not in (w.get('v') or ''):
            slov[0] += 1
        vs = sorted({e.get('v') for e in r})
        if len(primery) < n_pr:
            primery.append((w.get('v'), w.get('mark') or '', vs))
        if any((v or '').strip('-') in ('ima',) for v in vs):
            s_ima.append(w.get('v'))
print(f'язык {yaz}: статей {vsego}; с прямыми элементами {pryamye}; только внутри ref {tolko_ref}')
print('из них отдельных слов (без пробела):', slov[0])
print('из них с -ima:', ', '.join(s_ima))
for p in primery:
    print(' ', p)
