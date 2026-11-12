"""Грубая классификация переписи: край -> 'beg' (уход), узлы не растут -> 'fin', рост узлов 2^20->2^24 показатель p."""
import sys,math
for l in open(sys.argv[1]):
    R,t0,n1,n2,n3,b,e=l.split(); n1,n2,n3,e=int(n1),int(n2),int(n3),int(e)
    if e>=0: k='beg'
    elif n3==n2: k='fin'
    else:
        p=math.log(n3/n1)/math.log(16); k=f'grow{p:.2f}'
    print(R,t0,k,n3,b,e)
