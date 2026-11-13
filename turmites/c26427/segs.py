# разбивает переходы клетки на «сеансы» (между уходами вправо) и печатает сжатые блоки каждого сеанса
import sys
from itertools import groupby
T=[l.split()[1] for l in open(sys.argv[1])]
def blocks(T):
    i=0; out=[]
    while i<len(T):
        best=None
        for p in range(2,31):
            if i+2*p<=len(T) and T[i:i+p]==T[i+p:i+2*p]: best=p; break
        if best is None: i+=1; continue
        p=best; j=i+p
        while j+p<=len(T) and T[j:j+p]==T[i:i+p]: j+=p
        out.append('%d×%d'%(p,(j-i)//p)); i=j
    return out
segs=[]; cur=[]
for t in T:
    cur.append(t)
    if t.split('/')[0].endswith('R'):   # уход вправо через L..R? формат: L147R/xx
        pass
    if t[0]=='L' and t.split('/')[0][-1]=='R' and not t.startswith('L150') and not t.startswith('L147'):
        segs.append(cur); cur=[]
if cur: segs.append(cur)
desc=[' '.join(blocks(s)) for s in segs]
print(len(segs),'сеансов')
for d,g in groupby(desc): print(len(list(g)),'×', d)
