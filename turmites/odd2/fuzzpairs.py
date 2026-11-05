"""python3 fuzzpairs.py N < fuzzy_pairs.txt > skel_fuzzy.txt"""
import sys
from allpairs import skel,best
N=int(sys.argv[1]); C={}
for l in sys.stdin:
    a,b=map(int,l.split())
    for r in (a,b):
        if r not in C: C[r]=skel(r,N)
    m=best(C[a],C[b]); L=min(len(C[a]),len(C[b]))
    print(a,b,L,*m,'OK' if m[0]>=L-3 else '-',flush=True)
