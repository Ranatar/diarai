"""Для каждого класса и k=1..3: читает ли калиброванное правило те же цвета, что исходное, N шагов.
python3 odd2/gauge_check.py N > odd2/gauge_ok.txt"""
import csv, sys, os
sys.path.insert(0, os.getcwd())
from odd2gauge import gauge, cls, cat
DX=[0,1,0,-1];DY=[-1,0,1,0]
def reads(r,N):
    E=[((r>>(4*e))&1,(r>>(4*e+1))&3,(r>>(4*e+3))&1) for e in range(4)]
    g=set(); x=y=d=s=0; out=bytearray(N)
    for t in range(N):
        c=1 if (x,y) in g else 0; out[t]=c+2*s; w,tn,ns=E[s*2+c]
        if w: g.add((x,y))
        else: g.discard((x,y))
        d=(d+tn)&3; s=ns; x+=DX[d]; y+=DY[d]
    return bytes(out)
N=int(sys.argv[1])
for r in cat:
    A=reads(r,N)
    for k in (1,2,3):
        b=gauge(r,k); c=cls(b)
        if c==r: continue
        B=reads(b,N)
        m=next((i for i in range(N) if A[i]!=B[i]),N)
        if m==N: print(r,k,c,cat[r]['kind'],cat.get(c,{}).get('kind','-'),flush=True)
