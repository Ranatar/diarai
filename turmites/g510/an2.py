# Для границы k|k+1 справа от опоры: последовательность пар (вход A/B, возврат C/D)
from tm510 import TAB, RIGHT
import sys, collections
K=int(sys.argv[1]); H=int(sys.argv[2])
tape={}; pos=0; s='A'; hi=0; t=0; seq=[]; pend=None
while hi<H:
    v=tape.get(pos,0); nv,s=TAB[(s,v)]; tape[pos]=nv
    np=pos+(1 if s in RIGHT else -1)
    if hi>=H-4:
        if pos==K and np==K+1: pend=s
        if pos==K+1 and np==K and pend: seq.append(pend+s); pend=None
    pos=np; hi=max(hi,pos)
print(len(seq), collections.Counter(seq))
print(' '.join(seq[:120]))
