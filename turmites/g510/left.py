# Левая половина: вход в клетку k−1 из k (C/D), ответ (A/B); состояния клеток при входе
import sys, collections
from tm510 import TAB, RIGHT
H=int(sys.argv[1])
tape={}; pos=0; s='A'; hi=0; pend={}; resp=collections.Counter(); st=collections.Counter(); g=collections.Counter()
while hi<H:
    v=tape.get(pos,0); nv,s2=TAB[(s,v)]
    if pos<=-1 and s not in RIGHT: st[(s,v)]+=1
    if pos>=-1 and pos<=1: g[(pos,s,v)]+=1
    tape[pos]=nv
    np=pos+(1 if s2 in RIGHT else -1)
    if pos<=0 and np==pos-1: pend[pos]=s2
    if pos<0 and np==pos+1 and (pos+1) in pend: resp[(pend.pop(pos+1),s2)]+=1
    s=s2; pos=np; hi=max(hi,pos)
print(resp); print(sorted(st.items())); print(sorted(g.items()))
