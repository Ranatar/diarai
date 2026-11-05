"""Классы, у которых состояние при приходе — функция ориентированного ребра (манхэттенская решётка).
python3 odd2/manhattan.py N > odd2/manhattan.txt"""
import csv, sys, collections
N=int(sys.argv[1]); DX=[0,1,0,-1];DY=[-1,0,1,0]
cat={int(r['rep']):r for r in csv.DictReader(open('catalog2.csv'))}
for r,row in cat.items():
    E=[((r>>(4*e))&1,(r>>(4*e+1))&3,(r>>(4*e+3))&1) for e in range(4)]
    g=set(); x=y=d=s=0; T={}; ok=True; s1=0
    for t in range(N):
        c=1 if (x,y) in g else 0; w,tn,ns=E[s*2+c]
        if w: g.add((x,y))
        else: g.discard((x,y))
        d=(d+tn)&3; s=ns; x+=DX[d]; y+=DY[d]; s1+=s
        k=(0,x&1,DX[d]) if DX[d] else (1,y&1,DY[d])
        if T.setdefault(k,s)!=s: ok=False; break
    if ok and 0<s1<N: print(r,row['kind'],row['twin'] or '-',len(T),flush=True)
