"""Точная проверка «дырявости»: обход графа (φ, s, d), φ = (a·x+b·y) mod n, при обоих цветах клетки.
Если из старта (0, s0, север) достижимы не все φ — правило никогда не ступает на клетки с недостижимыми φ (при любой раскраске).
python3 holed.py < rules -> rule форма недостижимые_φ"""
import sys
DX=[0,1,0,-1]; DY=[-1,0,1,0]
FORMS=[(2,1,5),(1,2,5),(1,0,5),(0,1,5),(1,1,5),(1,4,5),(1,1,2),(1,1,3),(1,2,3),(1,1,4),(1,3,10),(3,1,10)]
def holes(r,a,b,n):
    T=[((r>>(4*e))&1,((r>>(4*e))>>1)&3,((r>>(4*e))>>3)&1) for e in range(4)]
    seen={(0,0,0)}; st=[(0,0,0)]
    while st:
        phi,s,d=st.pop()
        for col in (0,1):
            w,tn,ns=T[s*2+col]; d2=(d+tn)%4; p2=(phi+a*DX[d2]+b*DY[d2])%n; k=(p2,ns,d2)
            if k not in seen: seen.add(k); st.append(k)
    return sorted(set(range(n))-set(p for p,_,_ in seen))
for l in sys.stdin:
    r=int(l.split()[0]); out=[]
    for a,b,n in FORMS:
        h=holes(r,a,b,n)
        if h: out.append(f'{a}x+{b}y mod{n}:{h}')
    print(r,' '.join(out) if out else '-')
