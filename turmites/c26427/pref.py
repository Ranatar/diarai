# сколько разных содержимых префикса [-1..m-1] (с состоянием) при выходе головки из m-1 в m
from sim import T
import sys
N=int(sys.argv[1]); tape={}; k=0; s=150; seen={}; cntx={}
for n in range(N):
    c=tape.get(k,0); side,ns,nc=T[(s,c)]; tape[k]=nc; k2=k+(1 if side else -1)
    if side and k>=0:
        m=k2; key=(ns,tuple(tape.get(x,0) for x in range(-1,m)))
        seen.setdefault(m,set()).add(key); cntx[m]=cntx.get(m,0)+1
    k=k2; s=ns
for m in sorted(seen): print(m, len(seen[m]), cntx[m])
