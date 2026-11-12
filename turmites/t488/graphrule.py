"""Абстрактное правило на 4.8.8: вход (тип пройденного ребра τ: 1=сторона квадрата, 0=между восьмиугольниками; цвет c)
-> (запись, выход). Выход: 0 = назад, 1 = первое из оставшихся рёбер по часовой (на экране, y вниз), 2 = второе.
python3 graphrule.py N RULE...   печатает правило в виде строки 'τc:w,выход' и число нарушений"""
import sys
DX=[0,1,0,-1];DY=[-1,0,1,0]
def analyze(r,N):
    E=[((r>>(4*e))&1,(r>>(4*e+1))&3,(r>>(4*e+3))&1) for e in range(4)]
    g=set();x=y=d=s=0;rec=[]
    for t in range(N):
        c=1 if (x,y) in g else 0; w,tn,ns=E[s*2+c]
        if w: g.add((x,y))
        else: g.discard((x,y))
        d2=(d+tn)&3
        rec.append((x,y,d,c,w,d2))
        d=d2; s=ns; x+=DX[d]; y+=DY[d]
    for a,b in ((2,1),(1,2)):
        used=set((a*x+b*y)%5 for x,y,*_ in rec)
        if len(used)==4: break
    else: return None
    h=(set(range(5))-used).pop()
    hole=lambda x,y:(a*x+b*y)%5==h
    def sqedge(x0,y0,dd):
        x1,y1=x0+DX[dd],y0+DY[dd]
        sides=[(1,0),(-1,0)] if x0==x1 else [(0,1),(0,-1)]
        for ex,ey in sides:
            if not any(hole(*p) for p in ((x0,y0),(x1,y1),(x0+ex,y0+ey),(x1+ex,y1+ey))): return 1
        return 0
    tab={};bad=0
    for (x,y,d,c,w,d2) in rec[1:]:
        back=(d+2)&3
        tau=sqedge(x,y,back)
        free=[k for k in (1,2,3) if not hole(x+DX[(back+k)&3],y+DY[(back+k)&3])]
        off=(d2-back)&3
        ex=0 if off==0 else 1+free.index(off)
        key=(tau,c); v=(w,ex)
        if key in tab and tab[key]!=v: bad+=1
        tab.setdefault(key,v)
    return f'{a}x+{b}y≠{h}',tab,bad
if __name__=='__main__':
    for r in map(int,sys.argv[2:]):
        res=analyze(r,int(sys.argv[1]))
        if res is None: print(r,'не дырявый'); continue
        f,tab,bad=res
        print(r,f,' '.join(f'{k[0]}{k[1]}:{v[0]}{v[1]}' for k,v in sorted(tab.items())),'нарушений',bad)
