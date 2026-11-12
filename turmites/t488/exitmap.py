import sys
from graphrule import DX,DY
# для вложения 2x+y≠h и x+2y≠h: при входе по ребру типа τ, какой тип у выхода 1 и 2, и с какой стороны квадрат
for a,b in ((2,1),(1,2)):
  for h in range(5):
    hole=lambda x,y:(a*x+b*y)%5==h
    def sq(x0,y0,dd):
        x1,y1=x0+DX[dd],y0+DY[dd]
        sides=[(1,0),(-1,0)] if x0==x1 else [(0,1),(0,-1)]
        return int(any(not any(hole(*p) for p in ((x0,y0),(x1,y1),(x0+ex,y0+ey),(x1+ex,y1+ey))) for ex,ey in sides))
    m={}
    for x in range(-6,7):
      for y in range(-6,7):
        if hole(x,y): continue
        for back in range(4):
          if hole(x+DX[back],y+DY[back]): continue
          tau=sq(x,y,back)
          free=[k for k in (1,2,3) if not hole(x+DX[(back+k)&3],y+DY[(back+k)&3])]
          outs=tuple((sq(x,y,(back+k)&3),k) for k in free)
          m.setdefault(tau,set()).add(outs)
    print(a,b,h,{t:sorted(v) for t,v in m.items()})
