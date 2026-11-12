# стрелки поля дрейфа из vfield: python arrows.py OUT.png файл1 [файл2 ...]
import sys
from PIL import Image, ImageDraw
files=sys.argv[2:]; S=360; pad=20
im=Image.new('RGB',(len(files)*(S+pad)+pad,S+2*pad+20),'white'); dr=ImageDraw.Draw(im)
for f_i,fn in enumerate(files):
    rows=[l.split() for l in open(fn)]; B=int(max(int(r[0]) for r in rows))+1
    vs=[(int(r[0]),int(r[1]),float(r[2]),float(r[3]),int(r[4])) for r in rows]
    inn=sorted((vx*vx+vy*vy)**.5 for i,j,vx,vy,n in vs if n>10**5 and 1<i<B-2 and 1<j<B-2); mx=inn[int(len(inn)*0.9)] if inn else 1
    ox=pad+f_i*(S+pad); oy=pad
    dr.rectangle([ox,oy,ox+S,oy+S],outline='gray')
    c=S/B
    for i,j,vx,vy,n in vs:
        if n<10**5: continue
        cx,cy=ox+(i+.5)*c,oy+(j+.5)*c; k=0.45*c/mx
        L=(vx*vx+vy*vy)**.5*k
        if L>0.9*c: vx,vy=vx*0.9*c/L,vy*0.9*c/L
        ex,ey=cx+vx*k,cy+vy*k
        dr.line([cx,cy,ex,ey],fill='black',width=2); dr.ellipse([ex-2,ey-2,ex+2,ey+2],fill='red')
    dr.text((ox,oy+S+5),fn.replace('vf','').replace('.txt','')+'  scale %.4f'%mx,fill='black')
im.save(sys.argv[1])
