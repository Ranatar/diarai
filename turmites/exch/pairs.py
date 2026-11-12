# доля 2-циклов среди сдвинутых жетонов; картинка доминошек; модель на питоне (медленно, малые t)
import sys
r=int(sys.argv[1]); T=int(sys.argv[2])
wc=[0]*4;tn=[0]*4;ns=[0]*4
for e in range(4):
    b=(r>>(4*e))&15; wc[e]=b&1; tn[e]=(b>>1)&3; ns[e]=b>>3
DX=[0,1,0,-1];DY=[-1,0,1,0]
g={};idm={};x=y=d=s=0;hand=None
par=lambda p:(p[0]+p[1])&1
for t in range(T):
    p=(x,y);c=g.get(p,0);e=s*2+c;g[p]=wc[e];d=(d+tn[e])&3;s=ns[e]
    tok=idm.get(p,p)
    hp=0 if hand is None else par(hand)
    if hp!=par(tok):
        idm[p]=hand if hand is not None else (10**6,0); hand=tok
    x+=DX[d];y+=DY[d]
mv=[(p,h) for p,h in idm.items() if h!=p]
two=sum(1 for p,h in mv if idm.get(h,h)==p)
print('visited',len(g),'moved',len(mv),'2-cycles',two)
from PIL import Image
xs=[p[0] for p in g];ys=[p[1] for p in g];X0,Y0=min(xs),min(ys);W=max(xs)-X0+1;H=max(ys)-Y0+1
S=8;im=Image.new('RGB',(W*S,H*S),(0,0,0))
from PIL import ImageDraw
dr=ImageDraw.Draw(im)
for p in g:
    col=(90,90,90) if g[p] else (200,200,200)
    dr.rectangle([(p[0]-X0)*S,(p[1]-Y0)*S,(p[0]-X0)*S+S-2,(p[1]-Y0)*S+S-2],fill=col)
for p,h in mv:
    if h[0]<10**5: dr.line([((p[0]-X0)*S+3,(p[1]-Y0)*S+3),((h[0]-X0)*S+3,(h[1]-Y0)*S+3)],fill=(255,60,60),width=2)
im.save(sys.argv[3])
