"""Ищем моменты, когда поле A (после симметрии k) равно полю B (с точностью до сдвига). python3 tmatch.py A B N"""
import sys
from flips import dec,SYM,DX,DY
def grids(r,N):
    E=dec(r); g=set(); x=y=0; d=0; s=0; out=[]
    for t in range(N):
        out.append((frozenset(g),x,y,d,s))
        c=1 if (x,y) in g else 0; w,tn,ns=E[s*2+c]
        if w: g.add((x,y))
        else: g.discard((x,y))
        d=(d+tn)&3; s=ns; x+=DX[d]; y+=DY[d]
    return out
def norm(cells):
    if not cells: return frozenset()
    mx=min(x for x,y in cells); my=min(y for x,y in cells)
    return frozenset((x-mx,y-my) for x,y in cells)
A,B,N=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
ga=grids(A,N); gb=grids(B,N)
for k in range(8):
    f=SYM[k]
    hb={}
    for t,(g,*_ ) in enumerate(gb):
        if len(g)>8: hb.setdefault(norm(g),[]).append(t)
    pairs=[]
    for t,(g,*_ ) in enumerate(ga):
        if len(g)>8:
            n=norm({f(x,y) for x,y in g})
            if n in hb: pairs.append((t,hb[n][0],len(hb[n])))
    if pairs: print('sym',k,len(pairs),pairs[:6],pairs[-3:])
