# сводка: on25 + подписи пути (sig) -> классы поведения, шоссе, нерешённые
import sys
from collections import defaultdict
for D in (0,1):
    sig={}
    for l in open(f'sig_d{D}.txt'):
        c,h=l.split(); sig[int(c)]=h
    res={}
    for l in open(f'on25_d{D}.txt'):
        p=list(map(int,l.split())); res[p[0]]=p[1:]
    cls=defaultdict(list)
    for c in res: cls[sig[c]].append(c)
    hw=[];un=[];slow=[];bad=[]
    for h,cs in cls.items():
        c=min(cs); e,P,on,dx,dy,cells=res[c]
        if e<0: (slow if cells<2000 else un).append((cells,c,len(cs)))
        elif P<0 or on==-1: bad.append((c,e))
        else: hw.append((on,c,P,dx,dy,len(cs)))
    hw.sort()
    print(f'D0={D}: классов (нефинитных на 2^22) {len(cls)}; шоссе {len(hw)}, растут без края {len(un)}, медленные (<2000 клеток) {len(slow)}, без периода {len(bad)}')
    print('  шоссе с началом > 10^4:',[(on,c,P,(dx,dy)) for on,c,P,dx,dy,n in hw if on>1e4])
    print('  нулевое начало:',sum(1 for x in hw if x[0]<100),' периоды:',sorted(set(x[2] for x in hw))[:40])
    print('  без края:',sorted(un,reverse=True)[:60])
    print('  без периода:',bad)
