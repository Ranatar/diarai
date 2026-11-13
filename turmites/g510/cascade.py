# Чистый каскад счётчиков по модулю 4 (вывод из таблицы машины 510, см. README).
# Клетка: A: s→s+1, на 3→0 выпускает BB; B: s→s−1, выпускает 0→3: —, 1→0: A, 2→1: BB, 3→2: A.
# Первую клетку кормим одними B (так у опоры). Считаем буквы, дошедшие до клетки k.
import sys, math
N=int(sys.argv[1]); K=int(sys.argv[2])
st=[0]*K; cA=[0]*K; cB=[0]*K
OUTB={0:'',1:'A',2:'BB',3:'A'}
def feed(k,ch):
    stack=[(k,ch)]
    while stack:
        k,ch=stack.pop()
        if k>=K: continue
        if ch=='A':
            cA[k]+=1; s=st[k]; st[k]=(s+1)&3; out='BB' if s==3 else ''
        else:
            cB[k]+=1; s=st[k]; st[k]=(s-1)&3; out=OUTB[s]
        for c in reversed(out): stack.append((k+1,c))
for i in range(N): feed(0,'B')
phi=(1+5**.5)/2
for k in range(K):
    n=cA[k]+cB[k]
    if n==0: break
    r=n/(cA[k-1]+cB[k-1]) if k else 1
    print(k,cA[k],cB[k],n,'%.4f'%r, '%.3f'%(cB[k]/cA[k]) if cA[k] else '')
print('phi/2=%.6f phi=%.6f'%(phi/2,phi))
