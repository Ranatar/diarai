"""Картинка: тело турмита 6990 в Z² (вершины графа 4.8.8: синие рёбра — стороны квадратов-колец, оранжевые — между кольцами;
серые квадратики — дыры) и то же тело в крупной модели — тетракис (каждый узел — квадрат из 4 треугольников).
python draw488.py N OUT.png"""
import sys
from PIL import Image, ImageDraw
DX=[0,1,0,-1];DY=[-1,0,1,0]
N=int(sys.argv[1]); out=sys.argv[2]
r=6990; R='01001112'
E=[((r>>(4*e))&1,(r>>(4*e+1))&3,(r>>(4*e+3))&1) for e in range(4)]
g=set();vis=set();x=y=d=s=0
for t in range(N):
    c=1 if (x,y) in g else 0; w,tn,ns=E[s*2+c]
    if w: g.add((x,y))
    else: g.discard((x,y))
    vis.add((x,y)); d=(d+tn)&3; s=ns; x+=DX[d]; y+=DY[d]
a,b,h=1,2,1
hole=lambda x,y:(a*x+b*y)%5==h
xs=[p[0] for p in vis]; ys=[p[1] for p in vis]
x0,x1,y0,y1=min(xs)-1,max(xs)+1,min(ys)-1,max(ys)+1
S=22
W=(x1-x0+1)*S; H=(y1-y0+1)*S
im=Image.new('RGB',(W,H),'white'); D=ImageDraw.Draw(im)
def cen(x,y): return ((x-x0)*S+S//2,(y-y0)*S+S//2)
def sq(X0,Y0,X1,Y1):
    sides=[(1,0),(-1,0)] if X0==X1 else [(0,1),(0,-1)]
    return any(not any(hole(*p) for p in ((X0,Y0),(X1,Y1),(X0+ex,Y0+ey),(X1+ex,Y1+ey))) for ex,ey in sides)
for X in range(x0,x1+1):
    for Y in range(y0,y1+1):
        if hole(X,Y): continue
        for dx,dy in ((1,0),(0,1)):
            if X+dx>x1 or Y+dy>y1 or hole(X+dx,Y+dy): continue
            D.line([cen(X,Y),cen(X+dx,Y+dy)],fill=(40,90,220) if sq(X,Y,X+dx,Y+dy) else (240,140,30),width=3)
for X in range(x0,x1+1):
    for Y in range(y0,y1+1):
        cx,cy=cen(X,Y)
        if hole(X,Y): D.rectangle([cx-3,cy-3,cx+3,cy+3],fill=(170,170,170)); continue
        col=(0,0,0) if (X,Y) in g else ((255,255,255) if (X,Y) in vis else (235,235,235))
        D.ellipse([cx-6,cy-6,cx+6,cy+6],fill=col,outline=(0,0,0) if (X,Y) in vis else (190,190,190))
# крупная модель
W2=[[int(R[0]),int(R[2])],[int(R[4]),int(R[6])]]; X2=[[int(R[1]),int(R[3])],[int(R[5]),int(R[7])]]
f={};X=Y=0;k=0;tau=0;sig=1;nodes={(0,0)}
for t in range(N):
    bits=f.get((X,Y),0); c=(bits>>k)&1; w=W2[tau][c]; e=X2[tau][c]
    if w!=c: f[(X,Y)]=bits^(1<<k)
    oct=0
    if tau==0:
        if e==0: oct=1
        else: sig=1 if e==1 else -1
    else:
        if e==2: oct=1
        elif e==0: sig=-sig
    if oct: X+=DX[k];Y+=DY[k];k=(k+2)&3;tau=0;nodes.add((X,Y))
    else: k=(k+sig)&3;tau=1
nx=[p[0] for p in nodes]; ny=[p[1] for p in nodes]
T=44; ox,oy=min(nx)-1,min(ny)-1
W3=(max(nx)-ox+2)*T; H3=(max(ny)-oy+2)*T
im2=Image.new('RGB',(W3,H3),'white'); D2=ImageDraw.Draw(im2)
for (X,Y) in nodes:
    bx,by=(X-ox)*T,(Y-oy)*T; c=(bx+T/2,by+T/2)
    corners=[(bx,by),(bx+T,by),(bx+T,by+T),(bx,by+T)]
    tri={0:[corners[0],corners[1]],1:[corners[1],corners[2]],2:[corners[2],corners[3]],3:[corners[3],corners[0]]}
    bits=f.get((X,Y),0)
    for kk in range(4):
        D2.polygon([c]+tri[kk],fill=(0,0,0) if (bits>>kk)&1 else (255,255,255),outline=(150,150,150))
    D2.rectangle([bx,by,bx+T,by+T],outline=(240,140,30),width=2)
Hh=max(H,H3); full=Image.new('RGB',(W+W3+30,Hh),'white'); full.paste(im,(0,0)); full.paste(im2,(W+30,0)); full.save(out)
print(W,H,W3,H3,len(vis),len(nodes))
