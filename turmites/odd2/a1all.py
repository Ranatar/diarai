"""Для всех хаотических классов: является ли a1 функцией клетки (N шагов). Печать: rule нарушений клеток есть_ли_калибр_пара"""
import csv, sys
N=int(sys.argv[1])
DX=[0,1,0,-1];DY=[-1,0,1,0]
cat={int(r['rep']):r for r in csv.DictReader(open('catalog2.csv'))}
gp={int(l.split()[0]) for l in open('odd2/gauge_ok.txt')}|{int(l.split()[2]) for l in open('odd2/gauge_ok.txt')}
for r,row in cat.items():
    if row['kind']!='chaotic': continue
    E=[((r>>(4*e))&1,(r>>(4*e+1))&3,(r>>(4*e+3))&1) for e in range(4)]
    g=set(); x=y=d=s=0; a0=a1=0; seen={}; bad=0
    for t in range(N):
        c=1 if (x,y) in g else 0; w,tn,ns=E[s*2+c]
        if w: g.add((x,y))
        else: g.discard((x,y))
        d=(d+tn)&3; s=ns; x+=DX[d]; y+=DY[d]
        if s==1: a0+=DX[d]; a1+=DY[d]
        v=seen.setdefault((x,y),(a0,a1))
        if v!=(a0,a1): bad+=1
    print(r,bad,len(seen),'пара' if r in gp else '-',flush=True)
