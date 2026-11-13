# Для клеток справа от опоры: сколько раз буква входа застаёт клетку в каждом из состояний 0,3,4,7
import sys, collections
from tm510 import TAB, RIGHT
H=int(sys.argv[1]); G=int(sys.argv[2])
tape={}; pos=0; s='A'; hi=0
cnt=collections.defaultdict(collections.Counter)
while hi<H:
    v=tape.get(pos,0); nv,s2=TAB[(s,v)]
    if hi>=H-G and s in RIGHT and pos>=1: cnt[pos][(s,v)]+=1
    tape[pos]=nv; pos+=1 if s2 in RIGHT else -1; s=s2; hi=max(hi,pos)
print('k   A@0 A@3 A@4 A@7 | B@0 B@3 B@4 B@7   (за последние',G,'приростов)')
for k in sorted(cnt):
    c=cnt[k]; row=[c[('A',x)] for x in (0,3,4,7)]+[c[('B',x)] for x in (0,3,4,7)]
    other=sum(c.values())-sum(row)
    if k<=20 or k%5==0: print(k,*row,'' if not other else 'other %d'%other)
