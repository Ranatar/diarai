"""Какие правила развязок реализуются сырыми турмитами 2×2: перебор 65536, дырявые индекса 5 (ровно одна дыра),
внутренняя запись по 4000 шагов. -> realize.txt: raw внутр. нарушений старт_τ"""
import sys
sys.path.insert(0,'.')
from intrinsic import intrinsic
DX=[0,1,0,-1];DY=[-1,0,1,0]
def holes(r,a,b,n=5):
    T=[((r>>(4*e))&1,((r>>(4*e))>>1)&3,((r>>(4*e))>>3)&1) for e in range(4)]
    seen={(0,0,0)}; st=[(0,0,0)]
    while st:
        phi,s,d=st.pop()
        for col in (0,1):
            w,tn,ns=T[s*2+col]; d2=(d+tn)%4; p2=(phi+a*DX[d2]+b*DY[d2])%n; k=(p2,ns,d2)
            if k not in seen: seen.add(k); st.append(k)
    return sorted(set(range(n))-set(p for p,_,_ in seen))
out=open('realize.txt','w')
for r in range(65536):
    if any(len(holes(r,a,b))==1 for a,b in ((2,1),(1,2))):
        res=intrinsic(r,4000)
        if res: out.write(f'{r} {res[0].replace(" ","")} {res[1]} {res[2]}\n')
