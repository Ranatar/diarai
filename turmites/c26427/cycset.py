# различные циклы (как множества переходов) по файлам переходов клеток
import sys
allc={}
for fn in sys.argv[1:]:
    T=[l.split()[1] for l in open(fn)]; i=0; seen=set()
    while i<len(T):
        best=None
        for p in (20,12,8):
            if i+2*p<=len(T) and T[i:i+p]==T[i+p:i+2*p]: best=p; break
        if best is None: i+=1; continue
        p=best; key=frozenset(T[i:i+p]); j=i+p
        while j+p<=len(T) and T[j:j+p]==T[i:i+p]: j+=p
        seen.add((p,key)); i=j
    for c in seen: allc.setdefault(c,set()).add(fn.split('_')[-1])
    print(fn.split('/')[-1], 'циклов:', len(seen))
print('всего различных:', len(allc))
from collections import Counter
print(Counter(p for p,k in allc))
