"""Глайдеры в сплошном фоне цвета c: муравей + конечный набор «дырок» (клеток не цвета фона),
которые повторяются со сдвигом. Затравки: пустая, одна дырка в клетке муравья или рядом, две дырки.
python3 glider.py [c] < rules  ->  rule  s:seed:период:(dx,dy):число_дырок  (первый найденный на затравку)"""
import sys
DX=[0,1,0,-1];DY=[-1,0,1,0]
def dec(r):
    return [((r>>(4*e))&1, (r>>(4*e+1))&3, (r>>(4*e+3))&1) for e in range(4)]
NB=[(0,0),(0,-1),(1,0),(0,1),(-1,0)]
SEEDS=[()]+[(p,) for p in NB]+[(p,q) for i,p in enumerate(NB) for q in NB[i+1:]]
def run(E,c,s,seed,T=600,H=12):
    holes=set(seed); x=y=0; d=0; seen={}
    for t in range(T):
        key=(s,d,frozenset((hx-x,hy-y) for hx,hy in holes))
        if key in seen:
            t0,x0,y0=seen[key]
            if (x,y)!=(x0,y0): return (t-t0,x-x0,y-y0,len(holes))
            return None
        seen[key]=(t,x,y)
        col=(1-c) if (x,y) in holes else c
        wc,tn,ns=E[s*2+col]
        if wc==c: holes.discard((x,y))
        else: holes.add((x,y))
        if len(holes)>H: return None
        d=(d+tn)&3; s=ns; x+=DX[d]; y+=DY[d]
        if holes and max(abs(hx-x)+abs(hy-y) for hx,hy in holes)>8: return None
    return None
if __name__=='__main__':
    c=int(sys.argv[1]) if len(sys.argv)>1 else 1
    for l in sys.stdin:
        r=int(l.split()[0]); E=dec(r); out=[]
        found=set()
        for s in (0,1):
            for k,seed in enumerate(SEEDS):
                g=run(E,c,s,seed)
                if g and (g[0],abs(g[1])+abs(g[2]),g[3]) not in found:
                    found.add((g[0],abs(g[1])+abs(g[2]),g[3]))
                    out.append(f's{s}:{k}:{g[0]}:({g[1]},{g[2]}):{g[3]}')
        if out: print(r,' '.join(out))
