# цепь на (Y mod 2^m, r) в рациональных числах (Y-форма: Y->floor(5Y/2) | 3Y+2; условие Y = ±1 mod 8)
from fractions import Fraction as F
def solve(A,b):
    n=len(A); M=[row[:]+[b[i]] for i,row in enumerate(A)]
    for c in range(n):
        p=next(r for r in range(c,n) if M[r][c]!=0); M[c],M[p]=M[p],M[c]
        for r in range(n):
            if r!=c and M[r][c]!=0:
                f=M[r][c]/M[c][c]; M[r]=[x-f*y for x,y in zip(M[r],M[c])]
    return [M[i][n]/M[i][i] for i in range(n)]
for m in (3,4,5,6):
    M=1<<m; n=2*M; P=[[F(0)]*n for _ in range(n)]
    for y in range(M):
        P[M+y][(3*y+2)%M]+=1
        r2=1 if y%8 in (1,7) else 0
        for top in (0,1): P[y][r2*M+((5*(y+top*M))//2)%M]+=F(1,2)
    # pi P = pi, sum pi = 1: заменяем последнее уравнение нормировкой
    A=[[P[j][i]-(1 if i==j else 0) for j in range(n)] for i in range(n)]; b=[F(0)]*n
    A[-1]=[F(1)]*n; b[-1]=F(1)
    pi=solve(A,b); p6=sum(pi[M:]); print(m,'доля 6 =',p6,' P(6|4) =',p6/(1-p6))
