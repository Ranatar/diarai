"""python3 odd2/skelverify.py N < pairs -> a b L m sym ... OK/-"""
import sys; sys.path.insert(0,'odd2')
from allpairs import skel,best
N=int(sys.argv[1])
for l in sys.stdin:
    w=l.split(); a,b=int(w[0]),int(w[1])
    A=skel(a,N); B=skel(b,N); m=best(A,B); L=min(len(A),len(B))
    print(a,b,L,*m,'OK' if m[0]>=L-3 else '-',flush=True)
