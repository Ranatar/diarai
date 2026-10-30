"""Круглость тела по миниатюре: центр масс, радиус-функция по 360 лучам. Печать: правило k r_ср σ(r)/r A/(π r_ср²) анизотропия (|r(0°)+r(90°)... - r(45°)...|)."""
import sys,glob,re,os,math
from PIL import Image
import numpy as np
for r in sys.argv[1:]:
    fs=sorted(glob.glob(f'th40/{r}-*.pgm'),key=lambda f:int(re.findall(r'-(\d+)\.pgm',f)[0]))
    for f in fs:
        a=np.array(Image.open(f)).astype(float); m=a<128; ys,xs=np.nonzero(m); cy,cx=ys.mean(),xs.mean()
        rr=[]
        for th in np.linspace(0,2*math.pi,360,endpoint=False):
            dx,dy=math.cos(th),math.sin(th); t=0
            while True:
                x,y=int(cx+dx*t),int(cy+dy*t)
                if not(0<=x<a.shape[1] and 0<=y<a.shape[0]) or not m[y,x]: break
                t+=0.5
            rr.append(t)
        rr=np.array(rr); R=rr.mean()
        ax=rr[[0,90,180,270]].mean(); dg=rr[[45,135,225,315]].mean()
        print(r, os.path.basename(f), 'R=%.0f σ/R=%.3f A/πR²=%.3f диаг/ось=%.3f'%(R,rr.std()/R,m.sum()/(math.pi*R*R),dg/ax))
