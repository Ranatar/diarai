from tm510 import TAB, RIGHT
import collections
tape={}; pos=0; s='A'; lo=hi=0; t=0; vis=collections.Counter(); n=0
while True:
    v=tape.get(pos,0); nv,s=TAB[(s,v)]; tape[pos]=nv; t+=1
    if hi>=30: vis[(pos,s)]+=1
    pos+=1 if s in RIGHT else -1
    if pos>hi:
        hi=pos
        if hi==31: break
    lo=min(lo,pos)
print(lo,hi)
for p in range(lo,hi+1): print(p, vis[(p,'A')],vis[(p,'B')],vis[(p,'C')],vis[(p,'D')], ''.join('.' for _ in range(0)))
