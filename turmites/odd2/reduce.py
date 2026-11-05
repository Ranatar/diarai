"""Сжимаем путь: убираем «лепестки» x->y->x (стек). Сравниваем сжатые пути двух правил с симметрией и сдвигом.
python3 reduce.py A B N"""
import sys
from flips import run,SYM
def red(tr):
    st=[]
    for p in tr:
        if len(st)>=2 and st[-2]==p: st.pop()
        elif st and st[-1]==p: pass
        else: st.append(p)
    return st
def red_seq(tr):
    # не стек, а один проход: удалять возвраты, но сохранять порядок без схлопывания всего дерева
    out=[]
    for p in tr:
        if len(out)>=2 and out[-2]==p: out.pop()
        else: out.append(p)
    return out
if __name__=="__main__":
  A,B,N=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
  fa,ta=run(A,N); fb,tb=run(B,N)
  pa=[(x,y) for x,y,*_ in ta]; pb=[(x,y) for x,y,*_ in tb]
  ra=red_seq(pa); rb=red_seq(pb)
  print(len(ra),len(rb)); print(ra[:20]); print(rb[:20])
  for k,f in enumerate(SYM):
      for sx in range(-2,3):
          for sy in range(-2,3):
              m=0
              for p,q in zip(ra,rb):
                  X,Y=f(*p)
                  if (X+sx,Y+sy)!=q: break
                  m+=1
              if m>5: print(k,sx,sy,m)
  print('со сдвигом индекса:')
  for k,f in enumerate(SYM):
    for oa in range(3):
      for ob in range(3):
        p0=f(*ra[oa]); q0=rb[ob]; sx,sy=q0[0]-p0[0],q0[1]-p0[1]
        m=0
        for p,q in zip(ra[oa:],rb[ob:]):
          X,Y=f(*p)
          if (X+sx,Y+sy)!=q: break
          m+=1
        if m>5: print(k,oa,ob,(sx,sy),m,'из',min(len(ra),len(rb)))
