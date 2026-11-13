# сравнение двух орбит стартов: какие правила растут со старта 100 (≡000) и 001
import sys
sys.path.insert(0,'.')
def load(f):
    d={}
    for l in open(f):
        p=l.split(); d[int(p[0])]=list(map(int,p[1:]))
    return d
def kind(v):
    n1,n2,n,b,e=v
    if e!=-1: return 'E'
    if n2==n: return 'F'
    return 'G' if n>1.25*n2 else 'F'
A=load('mc21_100.txt'); B=load('mc21_001.txt')
from collections import Counter
print(Counter((kind(A[c]),kind(B[c])) for c in A))
