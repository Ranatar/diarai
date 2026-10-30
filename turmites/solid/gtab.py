"""Таблица глайдеров правила для fastglide: python3 gtab.py RULE > tab
Строка: c s d p vx vy nH (hx hy)* nF (fx fy)*  — фон c, муравей (s,d), дырки H и прочитанные за период клетки F
(относительно муравья), за период p сдвиг (vx,vy) по оси. Все фазы цикла, все 4 направления, оба фона."""
import sys
DX=[0,1,0,-1];DY=[-1,0,1,0]
def dec(r): return [((r>>(4*e))&1, (r>>(4*e+1))&3, (r>>(4*e+3))&1) for e in range(4)]
NB=[(0,0),(0,-1),(1,0),(0,1),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)]
SEEDS=[()]+[(p,) for p in NB]+[(p,q) for i,p in enumerate(NB) for q in NB[i+1:]]
def step(E,c,st):
    s,d,x,y,holes=st; col=(1-c) if (x,y) in holes else c
    wc,tn,ns=E[s*2+col]; holes=set(holes)
    if wc==c: holes.discard((x,y))
    else: holes.add((x,y))
    d=(d+tn)&3; return (ns,d,x+DX[d],y+DY[d],frozenset(holes))
def find(E,c,s,d,seed,T=400,H=12):
    st=(s,d,0,0,frozenset(seed)); seen={}
    for t in range(T):
        s_,d_,x,y,h=st
        key=(s_,d_,frozenset((a-x,b-y) for a,b in h))
        if key in seen:
            t0,st0=seen[key]
            if (x,y)!=(st0[2],st0[3]): return st0,t-t0,x-st0[2],y-st0[3]
            return None
        seen[key]=(t,st); st=step(E,c,st)
        if len(st[4])>H or any(abs(a-st[2])+abs(b-st[3])>8 for a,b in st[4]): return None
    return None
def main():
    r=int(sys.argv[1]); E=dec(r); out={}
    for c in (0,1):
        for s in (0,1):
            for d in range(4):
                for seed in SEEDS:
                    g=find(E,c,s,d,seed)
                    if not g: continue
                    st,p,vx,vy=g
                    if vx and vy: continue
                    # фазы
                    traj=[st]
                    for i in range(2*p): traj.append(step(E,c,traj[-1]))
                    for i in range(p):
                        s_,d_,x,y,h=traj[i]
                        H=tuple(sorted((a-x,b-y) for a,b in h))
                        key=(c,s_,d_,H)
                        if key in out: continue
                        F=sorted({(traj[j][2]-x,traj[j][3]-y) for j in range(i,i+p)})
                        out[key]=(p,vx,vy,F)
    for (c,s,d,H),(p,vx,vy,F) in out.items():
        print(c,s,d,p,vx,vy,len(H),' '.join(f'{a} {b}' for a,b in H),len(F),' '.join(f'{a} {b}' for a,b in F))
main()
