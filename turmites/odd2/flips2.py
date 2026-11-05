import sys
from flips import run,SYM
A,B,N=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
fa,ta=run(A,N); fb,tb=run(B,N)
print(fa[:8]); print(fb[:8])
best=[]
for k,f in enumerate(SYM):
  for oa in range(0,4):
    for ob in range(0,4):
      for sx in range(-2,3):
        for sy in range(-2,3):
          m=0
          for (t,x,y,w),(t2,x2,y2,w2) in zip(fa[oa:],fb[ob:]):
            X,Y=f(x,y)
            if (X+sx,Y+sy,w)!=(x2,y2,w2): break
            m+=1
          best.append((m,k,oa,ob,sx,sy))
best.sort(reverse=True); print(best[:3])
