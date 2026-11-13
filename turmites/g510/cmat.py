# Эмпирическая матрица счёта каскада: ./cmat.py tm.txt START STEPS
# M[a][b] = сколько букв b клетка k выпускает в k+1 за макрошаг, открытый буквой a (усреднено по клеткам справа, k ≥ 3)
import sys, collections, numpy as np
T={}
for l in open(sys.argv[1]):
    s,c,side,ns,nc,_=map(int,l.split()); T[(s,c)]=(side,ns,nc)
st=int(sys.argv[2]); N=int(sys.argv[3])
tape=collections.defaultdict(int); pos=0; opened={}
cnt=collections.Counter(); M=collections.Counter(); hi=0
for n in range(N):
    side,ns,nc=T[(st,tape[pos])]; tape[pos]=nc
    np_=pos+(1 if side else -1)
    if np_==pos+1:
        if pos>=3 and pos in opened: M[(opened[pos],ns)]+=1
        opened[np_]=ns; cnt[(np_,ns)]+=1
    else:
        opened.pop(pos,None)
    pos=np_; st=ns; hi=max(hi,pos)
let=sorted({a for (a,b) in M}|{b for (a,b) in M})
tot=collections.Counter()
for (p,a),c in cnt.items():
    if p>=3: tot[a]+=c
A=np.array([[M[(a,b)]/tot[a] if tot[a] else 0 for a in let] for b in let])
w=np.linalg.eigvals(A); lam=max(abs(w))
print('буквы',let); print(np.round(A,4)); print('λ = %.6f, 1/λ = %.6f'%(lam,1/lam))
