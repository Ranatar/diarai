"""Манхэттенские: состояние = тип пересечённого ребра (по чётности линии). Ребро типа τ разбивает Z² на блоки 2×2
(линии другого типа — внутри блоков). Для каждого типа: доля ходов внутри блоков, идущих по часовой вокруг центра блока.
python3 manring.py N RULE..."""
import sys
DX=[0,1,0,-1];DY=[-1,0,1,0]
for r in map(int,sys.argv[2:]):
    N=int(sys.argv[1])
    E=[((r>>(4*e))&1,(r>>(4*e+1))&3,(r>>(4*e+3))&1) for e in range(4)]
    g=set();x=y=d=s=0;rec=[]
    for t in range(N):
        c=1 if (x,y) in g else 0; w,tn,ns=E[s*2+c]
        if w: g.add((x,y))
        else: g.discard((x,y))
        d=(d+tn)&3; s=ns; rec.append((x,y,d,s)); x+=DX[d]; y+=DY[d]
    # тип линии: для хода по x из x0 в x0+dx линия = min(x0,x1); тип = s после хода; найти чётность
    tx={};ty={}
    for x0,y0,d,s in rec:
        if d in (1,3): tx.setdefault((min(x0,x0+DX[d])%2),set()).add(s)
        else: ty.setdefault((min(y0,y0+DY[d])%2),set()).add(s)
    ok=all(len(v)==1 for v in list(tx.values())+list(ty.values()))
    res=[]
    for typ in (0,1):
        cw=ccw=0
        for x0,y0,d,s in rec:
            if s==typ: continue          # ход по ребру типа typ — между блоками; внутри — другой тип
            x1,y1=x0+DX[d],y0+DY[d]
            # центр блока: блоки ограничены линиями типа typ; ход внутри блока
            # центр = середина ребра +- полклетки перпендикулярно; находим по чётности
            if d in (1,3):
                lx=min(x0,x1)       # линия lx+1/2 внутри блока, блок по y: какая из строк y0, y0±1 в том же блоке
                # блок по y ограничен линиями y=m+1/2 типа typ: найдём m чётности py с типом typ
                py=[p for p,v in ty.items() if typ in v]
                if not py: continue
                cy= y0+0.5 if (y0%2)!=py[0] else y0-0.5   # линия типа typ проходит через y0+1/2, если y0%2==py → блок вниз? 
                cx=lx+0.5
            else:
                ly=min(y0,y1); px=[p for p,v in tx.items() if typ in v]
                if not px: continue
                cx= x0+0.5 if (x0%2)!=px[0] else x0-0.5
                cy=ly+0.5
            # знак векторного произведения (r0-c)×(r1-r0), экран y вниз: >0 — по часовой
            cr=(x0-cx)*(y1-y0)-(y0-cy)*(x1-x0)
            if cr>0: cw+=1
            elif cr<0: ccw+=1
        res.append(f'блоки по типу {typ}: по часовой {cw/(cw+ccw+1e-9):.3f}')
    print(r,'разметка ок' if ok else 'НЕ манхэттенский',*res)
