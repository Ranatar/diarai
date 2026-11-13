import sys; from sim import T
from collections import defaultdict
N=int(sys.argv[1]); tape={}; k=0; s=150; G=defaultdict(lambda: defaultdict(int))
for n in range(N):
    c=tape.get(k,0); side,ns,nc=T[(s,c)]
    if nc!=c: G[c][nc]+=1
    tape[k]=nc; k+=1 if side else -1; s=ns
nodes=set(G)|{d for c in G for d in G[c]}
br=[c for c in G if len(G[c])>1]
print('узлов',len(nodes),'ветвлений',len(br))
for c in br: print(c, dict(G[c]))
import pickle; pickle.dump({c:dict(G[c]) for c in G},open('graph.pkl','wb'))
