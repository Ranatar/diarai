# цепь на (X mod 2^m, rn): верхние биты считаем равномерными (мера Хаара); стационарная доля "6 после 4"
import numpy as np, sys
for m in (4,6,8,10,12):
    M=1<<m; S=2*M; P=np.zeros((S,S))
    for x in range(M):
        # rn=6: X<-3X, rn<-4 (обратимо mod 2^m)
        P[M+x, (3*x)%M]=1
        # rn=4
        r2 = 1 if x%8 in (0,2) else 0
        for top in (0,1):
            xx=x+top*M  # mod 2^(m+1)
            y=((5*xx-3)//2)%M
            P[x, r2*M+y]+=0.5
    w,v=np.linalg.eig(P.T); i=np.argmin(abs(w-1)); pi=np.real(v[:,i]); pi/=pi.sum()
    p4=pi[:M].sum(); p6=pi[M:].sum()
    print(m, 'доля 6', p6, ' P(6|4)', p6/p4)
