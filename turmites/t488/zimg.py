"""Картинка турмита Z²: python zimg.py RULE N OUT [bg]  (bg=1 — старт на чёрном поле)"""
import sys
from PIL import Image
DX=[0,1,0,-1];DY=[-1,0,1,0]
r,N,out=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]; bg=len(sys.argv)>4
E=[((r>>(4*e))&1,(r>>(4*e+1))&3,(r>>(4*e+3))&1) for e in range(4)]
g={};x=y=d=s=0
for t in range(N):
    c=g.get((x,y),1 if bg else 0); w,tn,ns=E[s*2+c]; g[(x,y)]=w
    d=(d+tn)&3; s=ns; x+=DX[d]; y+=DY[d]
xs=[p[0] for p in g]; ys=[p[1] for p in g]; x0,y0=min(xs),min(ys)
im=Image.new('L',(max(xs)-x0+1,max(ys)-y0+1),200)
for (a,b),v in g.items(): im.putpixel((a-x0,b-y0),0 if v else 255)
s=400/max(im.size); im.resize((int(im.size[0]*s),int(im.size[1]*s))).save(out)
print(im.size)
