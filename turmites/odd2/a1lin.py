"""Проверка: a1 (сумма шагов, сделанных с приходом в состояние 1) — функция клетки P? линейная?
python3 a1lin.py RULE N"""
import sys
import numpy as np
DX=[0,1,0,-1];DY=[-1,0,1,0]
r,N=int(sys.argv[1]),int(sys.argv[2])
E=[((r>>(4*e))&1,(r>>(4*e+1))&3,(r>>(4*e+3))&1) for e in range(4)]
g=set(); x=y=d=s=0; a1=[0,0]; seen={}; bad=0; P=[];A=[]
for t in range(N):
    c=1 if (x,y) in g else 0; w,tn,ns=E[s*2+c]
    if w: g.add((x,y))
    else: g.discard((x,y))
    d=(d+tn)&3; s=ns; x+=DX[d]; y+=DY[d]
    if s==1: a1[0]+=DX[d]; a1[1]+=DY[d]
    k=(x,y); v=tuple(a1)
    if k in seen and seen[k]!=v: bad+=1
    seen.setdefault(k,v); P.append((x,y,1)); A.append(v)
print('клеток',len(seen),'нарушений функции',bad)
P=np.array(P,float); A=np.array(A,float)
M,res,_,_=np.linalg.lstsq(P,A,rcond=None)
print('a1 ≈ M·(x,y,1):'); print(np.round(M.T,4)); print('макс. ошибка',np.abs(P@M-A).max())
