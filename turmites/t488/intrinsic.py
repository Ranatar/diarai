"""Внутренняя запись дырявого правила как муравья на 4.8.8.
Вход: τ (0 — пришёл по ребру восьм.–восьм., 1 — по стороне квадрата), цвет c.
Выход при τ=0: 0 назад, 1 на квадрат по часовой (экран), 2 — против часовой;
при τ=1: 0 назад (разворот на квадрате), 1 дальше по квадрату, 2 — уйти по ребру восьм.
Печатает 'w e' для (τ,c)=00,01,10,11 и стартовое состояние после первого шага.
python3 intrinsic.py N RULE..."""
import sys
DX=[0,1,0,-1];DY=[-1,0,1,0]
def trace(r,N):
    E=[((r>>(4*e))&1,(r>>(4*e+1))&3,(r>>(4*e+3))&1) for e in range(4)]
    g=set();x=y=d=s=0;rec=[]
    for t in range(N):
        c=1 if (x,y) in g else 0; w,tn,ns=E[s*2+c]
        if w: g.add((x,y))
        else: g.discard((x,y))
        d2=(d+tn)&3; rec.append((x,y,d,c,w,d2)); d=d2; s=ns; x+=DX[d]; y+=DY[d]
    for a,b in ((2,1),(1,2)):
        if len(set((a*x+b*y)%5 for x,y,*_ in rec))==4: break
    else: return None
    h=(set(range(5))-set((a*x+b*y)%5 for x,y,*_ in rec)).pop()
    return rec,a,b,h
def intrinsic(r,N):
    T=trace(r,N)
    if T is None: return None
    rec,a,b,h=T
    hole=lambda x,y:(a*x+b*y)%5==h
    def side(x0,y0,dd):   # +1 квадрат справа от хода, -1 слева, 0 — ребро восьм.
        x1,y1=x0+DX[dd],y0+DY[dd]; rx,ry=DX[(dd+1)&3],DY[(dd+1)&3]
        if not any(hole(*p) for p in ((x0,y0),(x1,y1),(x0+rx,y0+ry),(x1+rx,y1+ry))): return 1
        if not any(hole(*p) for p in ((x0,y0),(x1,y1),(x0-rx,y0-ry),(x1-rx,y1-ry))): return -1
        return 0
    tab={};bad=0
    for (x,y,d,c,w,d2) in rec[1:]:
        sin=side(x-DX[d],y-DY[d],d); tau=1 if sin else 0
        sout=side(x,y,d2)
        if d2==(d+2)&3: e=0
        elif tau==0: e=1 if sout==1 else 2
        else: e=2 if sout==0 else 1
        k=(tau,c)
        if k in tab and tab[k]!=(w,e): bad+=1
        tab.setdefault(k,(w,e))
    x,y,d,c,w,d2=rec[1]
    s0=side(x-DX[d],y-DY[d],d)
    return ' '.join(f'{tab.get(k,("?","?"))[0]}{tab.get(k,("?","?"))[1]}' for k in ((0,0),(0,1),(1,0),(1,1))),bad,s0
if __name__=='__main__':
    for r in map(int,sys.argv[2:]):
        res=intrinsic(r,int(sys.argv[1]))
        print(r,*res) if res else print(r,'не дырявый')
