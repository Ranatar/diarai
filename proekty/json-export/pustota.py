"""По index.tsv: сколько разговоров без содержимого, по месяцам; примеры названий.
Запуск: python3 -I pustota.py index.tsv
"""
import sys, collections, random

stroki = [l.rstrip('\n').split('\t') for l in open(sys.argv[1], encoding='utf-8')][1:]
vsego = collections.Counter(); pust = collections.Counter(); s_nazv = collections.Counter()
primery = []
for d, nazv, vs, nep, vet, fai, f in stroki:
    mes = d[:7]; vsego[mes] += 1
    if nep == '0':
        pust[mes] += 1
        if nazv:
            s_nazv[mes] += 1
            primery.append((d, nazv, vs))
for m in sorted(vsego):
    print(m, 'всего', vsego[m], 'пустых', pust[m], 'из них с названием', s_nazv[m])
random.seed(1)
for p in random.sample(primery, min(10, len(primery))):
    print(p)
