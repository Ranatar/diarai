import sys; from sim import T
N=int(sys.argv[1]); EVERY=int(sys.argv[2])
tape={}; k=0; s=150; hist={6:[],9:[]}
# соберём циклы A и B по клеткам 9 и 6
for n in range(3000000):
    c=tape.get(k,0); side,ns,nc=T[(s,c)]
    if k in hist and nc!=c: hist[k].append(nc)
    tape[k]=nc; k+=1 if side else -1; s=ns
A=hist[9][:20]; Bs=hist[6]; i=Bs.index(A[0],20)  # где-то в 6 есть B
seqB=[x for x in hist[6] if x not in A]
B=[]
for x in seqB:
    if x in B: break
    B.append(x)
print('A',len(set(A)),'B',len(B))
lab={}
for i,x in enumerate(A): lab[x]='abcdefghijklmnopqrst'[i]
for i,x in enumerate(B): lab[x]='ABCDEFGHIJKLMNOPQRST'[i%20]
tape={}; k=0; s=150; hi=0
for n in range(N):
    c=tape.get(k,0); side,ns,nc=T[(s,c)]; tape[k]=nc; k+=1 if side else -1; s=ns
    hi=max(hi,k)
    if n%EVERY==0 and k==-1: print(f'{n:>10} ',''.join(lab.get(tape.get(x,0),'.') for x in range(-1,hi+1)))
