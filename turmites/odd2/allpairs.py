"""Все пары с одинаковой подписью onesig: совпадают ли сжатые пути (без лепестков) с симметрией/сдвигом.
python3 allpairs.py N > skel_pairs.txt"""
import sys, itertools
from flips import run,SYM
from reduce import red_seq
def skel(r,N):
    _,t=run(r,N); return red_seq([(x,y) for x,y,*_ in t])
def best(ra,rb):
    b=(0,)
    for k,f in enumerate(SYM):
      for oa in range(4):
        for ob in range(4):
          if (oa and ob) or oa>=len(ra) or ob>=len(rb): continue
          p0=f(*ra[oa]); q0=rb[ob]; sx,sy=q0[0]-p0[0],q0[1]-p0[1]; m=0
          for p,q in zip(ra[oa:],rb[ob:]):
            X,Y=f(*p)
            if (X+sx,Y+sy)!=q: break
            m+=1
          b=max(b,(m,k,oa,ob,sx,sy))
    return b
if __name__=="__main__":
  N=int(sys.argv[1])
  g={}
  for l in open('../solid/onesig.txt'):
      w=l.split()
      if len(w)>2 and 'E' not in w and int(w[-1])>200: g.setdefault(tuple(w[1:]),[]).append(int(w[0]))
  for k,v in g.items():
      if len(v)<2: continue
      S={r:skel(r,N) for r in v}
      for a,b in itertools.combinations(v,2):
          m=best(S[a],S[b]); L=min(len(S[a]),len(S[b]))
          print(a,b,L,*m,'OK' if m[0]>=L-3 else '-',flush=True)
