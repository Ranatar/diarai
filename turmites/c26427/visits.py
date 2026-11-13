import sys; from sim import T
N=int(sys.argv[1]); tape={}; k=0; s=150; vis={}
for n in range(N):
    c=tape.get(k,0); side,ns,nc=T[(s,c)]; tape[k]=nc; vis[k]=vis.get(k,0)+1; k+=1 if side else -1; s=ns
for x in sorted(vis): print(x, vis[x], f'{vis[x]/vis.get(x+1,1):.3f}' if x+1 in vis else '')
