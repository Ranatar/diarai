# классы итогов переписи вантов 4.8.8; зеркало: поворот t -> -t
import sys
from collections import Counter
def load(f):
    d={}
    for l in open(f):
        p=list(map(int,l.split())); d[p[0]]=p[1:]
    return d
def mir(c):
    To=[c&7,(c>>3)&7]; Ts=[(c>>6)&3,(c>>8)&3]
    To=[(-t)&7 for t in To]; Ts=[(-t)&3 for t in Ts]
    return To[0]+8*To[1]+64*Ts[0]+256*Ts[1]
def kind(v):
    n1,n2,n,b,e=v
    if e!=-1: return 'E'
    if n==n2: return 'F'
    return 'G'
for f in sys.argv[1:]:
    d=load(f); reps=[c for c in d if c<=mir(c)]
    K=Counter(kind(d[c]) for c in reps)
    print(f,len(reps),dict(K))
    G=[c for c in reps if kind(d[c])=='G']
    import math
    out=[]
    for c in G:
        n1,n2,n,b,e=d[c]
        a=math.log(n/n2)/math.log(4) if n2 else 0
        out.append((a,c,n,b))
    out.sort()
    for a,c,n,b in out: print(f"  {c:5d} To={c&7},{(c>>3)&7} Ts={2*((c>>6)&3)},{2*((c>>8)&3)} cells={n} black={b} рост~t^{a:.2f}")
