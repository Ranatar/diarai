"""Форма по миниатюрам каталога: k, w/h, заполненность рамки, σ(r)/R, диаг/ось. ./shapes.py DIR..."""
import sys,glob,re,math
from PIL import Image
import numpy as np
for D in sys.argv[1:]:
    print(D)
    for f in sorted(glob.glob(D+'/*.pgm'),key=lambda f:int(re.findall(r'-(\d+)\.pgm',f)[0])):
        a=np.array(Image.open(f))<128; ys,xs=np.nonzero(a); w=xs.ptp()+1; h=ys.ptp()+1; cy,cx=ys.mean(),xs.mean(); rr=[]
        for th in np.linspace(0,2*math.pi,360,endpoint=False):
            dx,dy=math.cos(th),math.sin(th); t=0
            while True:
                x,y=int(cx+dx*t),int(cy+dy*t)
                if not(0<=x<a.shape[1] and 0<=y<a.shape[0]) or not a[y,x]: break
                t+=0.5
            rr.append(t)
        rr=np.array(rr); R=rr.mean()
        print('  k=%s w/h=%.3f fill=%.3f σ/R=%.3f диаг/ось=%.3f'%(re.findall(r'-(\d+)\.pgm',f)[0],w/h,a.sum()/(w*h),rr.std()/R,rr[[45,135,225,315]].mean()/rr[[0,90,180,270]].mean()))
