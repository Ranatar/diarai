"""Скелет пути в крупной модели: путь по вершинам (узел, k), выбросить лепестки x->y->x (стеком). Сравнить два правила.
python3 skel.py RULE1 TAU1 RULE2 TAU2 N [BG1 BG2]"""
import sys
DX=[0,1,0,-1];DY=[-1,0,1,0]
def path(R,tau,N,bg=0):
    W=[[int(R[0]),int(R[2])],[int(R[4]),int(R[6])]]; E=[[int(R[1]),int(R[3])],[int(R[5]),int(R[7])]]
    f={};X=Y=0;k=0;sig=1;out=[(0,0,0)]
    for t in range(N):
        bits=f.get((X,Y),15 if bg else 0); c=(bits>>k)&1; w=W[tau][c]; e=E[tau][c]
        if w!=c: bits^=1<<k
        f[(X,Y)]=bits
        oct=0
        if tau==0:
            if e==0: oct=1
            else: sig=1 if e==1 else -1
        else:
            if e==2: oct=1
            elif e==0: sig=-sig
        if oct: X+=DX[k];Y+=DY[k];k=(k+2)&3;tau=0
        else: k=(k+sig)&3;tau=1
        out.append((X,Y,k))
    return out
def reduce(p):
    st=[]
    for v in p:
        if len(st)>=2 and st[-2]==v: st.pop()
        else: st.append(v)
    return st
a=sys.argv; N=int(a[5]); bg1=int(a[6]) if len(a)>6 else 0; bg2=int(a[7]) if len(a)>7 else 0
p=reduce(path(a[1],int(a[2]),N,bg1)); q=reduce(path(a[3],int(a[4]),N,bg2))
n=min(len(p),len(q)); same=0
while same<n and p[same]==q[same]: same+=1
print(f'скелеты: длины {len(p)} {len(q)}, совпадают первые {same}')
# с точностью до сдвига индекса 0..4
for sh in range(1,5):
    for P,Q,lab in ((p[sh:],q,'A сдвинут'),(p,q[sh:],'B сдвинут')):
        m=min(len(P),len(Q)); s=0
        while s<m and P[s]==Q[s]: s+=1
        if s>100: print(lab,sh,'совпадают',s)
