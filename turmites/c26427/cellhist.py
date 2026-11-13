import sys; from sim import T
N=int(sys.argv[1]); W=list(map(int,sys.argv[2:])); tape={}; k=0; s=150; hist={w:[] for w in W}
for n in range(N):
    c=tape.get(k,0); side,ns,nc=T[(s,c)]
    if k in hist and nc!=c: hist[k].append((n,nc))
    tape[k]=nc; k+=1 if side else -1; s=ns
names={}
for w in W:
    h=hist[w]; seq=[]
    for n,c in h:
        if c not in names: names[c]=len(names)
        seq.append(names[c])
    print(w,len(seq),' '.join(map(str,seq[:300])))
