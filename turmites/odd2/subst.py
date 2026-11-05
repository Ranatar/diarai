"""Проверка: B = зеркало(A) (или A) с заменой пар XY->YX. python3 subst.py A B N"""
import sys,itertools
from turns import turns,rel
A,B,N=map(int,sys.argv[1:4])
ta=rel(turns(A,N)); tb=rel(turns(B,N))
for mir in (0,1):
    s=ta.translate(str.maketrans('LR','RL')) if mir else ta
    for x,y in itertools.permutations('NLRU',2):
        t=s.replace(x+y,y+x)
        for o in range(-2,3):
            p,q=(t[o:],tb) if o>=0 else (t,tb[-o:])
            m=next((i for i,(u,v) in enumerate(zip(p,q)) if u!=v),min(len(p),len(q)))
            if m>50: print('зеркало' if mir else 'прямо',x+y,'->',y+x,'сдвиг',o,'совпало',m,'из',min(len(p),len(q)))
