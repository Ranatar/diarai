"""Как муравей обходит квадраты 4.8.8: при входе по стороне квадрата — квадрат справа или слева? python3 orient.py N RULE..."""
import sys
from graphrule import DX,DY
for r in map(int,sys.argv[2:]):
    N=int(sys.argv[1])
    E=[((r>>(4*e))&1,(r>>(4*e+1))&3,(r>>(4*e+3))&1) for e in range(4)]
    g=set();x=y=d=s=0;rec=[]
    for t in range(N):
        c=1 if (x,y) in g else 0; w,tn,ns=E[s*2+c]
        if w: g.add((x,y))
        else: g.discard((x,y))
        d=(d+tn)&3; s=ns; rec.append((x,y,d,s)); x+=DX[d]; y+=DY[d]
    for a,b in ((2,1),(1,2)):
        if len(set((a*x+b*y)%5 for x,y,_,_ in rec))==4: break
    h=(set(range(5))-set((a*x+b*y)%5 for x,y,_,_ in rec)).pop()
    hole=lambda x,y:(a*x+b*y)%5==h
    cnt={}
    for x0,y0,d,s in rec:
        x1,y1=x0+DX[d],y0+DY[d]
        # правая сторона от хода d: направление d+1
        rx,ry=DX[(d+1)&3],DY[(d+1)&3]
        R=not any(hole(*p) for p in ((x0,y0),(x1,y1),(x0+rx,y0+ry),(x1+rx,y1+ry)))
        L=not any(hole(*p) for p in ((x0,y0),(x1,y1),(x0-rx,y0-ry),(x1-rx,y1-ry)))
        k='справа' if R else ('слева' if L else 'восьм')
        cnt[k]=cnt.get(k,0)+1
    print(r,f'{a}x+{b}y≠{h}',cnt)
