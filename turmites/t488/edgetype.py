"""Дырявые индекса 5 = муравей на паркете 4.8.8? Проверка: состояние при приходе — функция типа ребра
(квадратное / между восьмиугольниками). python3 edgetype.py N RULE..."""
import sys
DX=[0,1,0,-1];DY=[-1,0,1,0]
def run(r,N):
    E=[((r>>(4*e))&1,(r>>(4*e+1))&3,(r>>(4*e+3))&1) for e in range(4)]
    g=set();x=y=d=s=0;steps=[]
    for t in range(N):
        c=1 if (x,y) in g else 0; w,tn,ns=E[s*2+c]
        if w: g.add((x,y))
        else: g.discard((x,y))
        d=(d+tn)&3; ox,oy=x,y; s=ns; x+=DX[d]; y+=DY[d]
        steps.append((ox,oy,x,y,d,s))
    return steps
def kap(x,y,a,b): return (a*x+b*y)%5
for r in map(int,sys.argv[2:]):
    st=run(r,int(sys.argv[1]))
    for a,b in ((2,1),(1,2)):
        used=set(kap(x,y,a,b) for _,_,x,y,_,_ in st)
        if len(used)==4: break
    else:
        print(r,'не дырявый'); continue
    h=(set(range(5))-used).pop()
    def hole(x,y): return kap(x,y,a,b)==h
    def sqedge(x0,y0,x1,y1):
        # ребро граничит с единичным квадратом без дырок?
        if x0==x1: sides=[(1,0),(-1,0)]
        else: sides=[(0,1),(0,-1)]
        for ex,ey in sides:
            if not any(hole(*p) for p in ((x0,y0),(x1,y1),(x0+ex,y0+ey),(x1+ex,y1+ey))): return 1
        return 0
    tab={};bad=0
    for x0,y0,x1,y1,d,s in st:
        k=sqedge(x0,y0,x1,y1)
        if k in tab and tab[k]!=s: bad+=1
        tab.setdefault(k,s)
    print(r,f'{a}x+{b}y≠{h}','тип→сост',tab,'нарушений',bad,'из',len(st))
