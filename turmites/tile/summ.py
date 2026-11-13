# сводка onset: ./summ.py on25_e6.txt [...] — классы по подписи пути (первые 10^5 шагов), шоссе, нерешённые
import sys
from collections import defaultdict
for fn in sys.argv[1:]:
    cls=defaultdict(list)
    for l in open(fn):
        p=l.split(); c=int(p[0]); e,P,on,di,dj,cells=map(int,p[1:7]); cls[p[7]].append((c,e,P,on,di,dj,cells))
    hw=[];un=[];bad=[]
    for h,lst in cls.items():
        c,e,P,on,di,dj,cells=min(lst)
        if e<0: un.append((cells,c,len(lst)))
        elif P<0: bad.append((c,e,cells))
        else: hw.append((on,c,P,di,dj,cells,len(lst)))
    hw.sort()
    print(f'{fn}: правил {sum(len(v) for v in cls.values())}, классов {len(cls)}: шоссе {len(hw)} (с нуля <100: {sum(1 for x in hw if x[0]<100)}), без края {len(un)}, у края без периода {len(bad)}')
    print('  шоссе с началом > 10^5 (начало, правило, период, сдвиг, плиток):'); 
    for on,c,P,di,dj,cells,n in hw:
        if on>1e5: print('   ',on,c,P,(di,dj),cells)
    print('  без периода:',bad[:20])
    print('  без края (плиток, правило):',sorted(un,reverse=True)[:15], '...', len(un))
