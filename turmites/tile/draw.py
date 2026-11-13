# ./vtXXX dump ... | python3 draw.py TILING out.png [size]
import sys, math
from PIL import Image, ImageDraw
sys.path.insert(0, __file__.rsplit('/',1)[0])
import gen
name=sys.argv[1]; out=sys.argv[2]; S=int(sys.argv[3]) if len(sys.argv)>3 else 1000
a1,a2,prim,sec=gen.tiling(name)
types,adj,_,_=gen.build(name)
# форма каждого типа: вершины относительно центра (берём из build через повтор геометрии)
shapes=[]
import itertools
verts=[]
for i in range(-2,3):
    for j in range(-2,3):
        for c,n,R,a0 in prim: verts+=gen.poly((c[0]+i*a1[0]+j*a2[0],c[1]+i*a1[1]+j*a2[1]),n,R,a0)
for c,n,kind,par in types:
    if kind=='p': vs=gen.poly(c,n,*par)
    else:
        u={}
        for v in verts:
            if abs(math.dist(v,c)-par)<1e-6: u[(round(v[0],5),round(v[1],5))]=v
        vs=sorted(u.values(),key=lambda v:math.atan2(v[1]-c[1],v[0]-c[0]))
    shapes.append([(v[0]-c[0],v[1]-c[1]) for v in vs])
cells=[]; ant=None
for l in sys.stdin:
    p=l.split()
    if p[0]=='A': ant=tuple(map(int,p[1:])); continue
    cells.append(tuple(map(int,p)))
def cen(t,i,j):
    c=types[t][0]; return (c[0]+i*a1[0]+j*a2[0], c[1]+i*a1[1]+j*a2[1])
pts=[cen(t,i,j) for t,i,j,_ in cells]
x0=min(p[0] for p in pts)-3; x1=max(p[0] for p in pts)+3; y0=min(p[1] for p in pts)-3; y1=max(p[1] for p in pts)+3
sc=S/max(x1-x0,y1-y0); W=int((x1-x0)*sc); H=int((y1-y0)*sc)
im=Image.new('RGB',(W,H),(255,255,255)); dr=ImageDraw.Draw(im)
COL={0:(235,225,190),1:(20,20,60)}
for (t,i,j,c),p in zip(cells,pts):
    poly=[((p[0]+v[0]-x0)*sc,(y1-(p[1]+v[1]))*sc) for v in shapes[t]]
    dr.polygon(poly,fill=COL[c],outline=(150,150,150) if sc>6 else None)
if ant:
    p=cen(*ant); r=max(3,sc*0.5); X=(p[0]-x0)*sc; Y=(y1-p[1])*sc; dr.ellipse([X-r,Y-r,X+r,Y+r],fill=(220,30,30))
im.save(out); print(len(cells),'tiles',W,H)
