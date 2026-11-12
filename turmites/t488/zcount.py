import sys
DX=[0,1,0,-1];DY=[-1,0,1,0]
r,lg=int(sys.argv[1]),int(sys.argv[2])
E=[((r>>(4*e))&1,(r>>(4*e+1))&3,(r>>(4*e+3))&1) for e in range(4)]
g=set();x=y=d=s=0
for t in range(1,(1<<lg)+1):
    c=1 if (x,y) in g else 0; w,tn,ns=E[s*2+c]
    if w: g.add((x,y))
    else: g.discard((x,y))
    d=(d+tn)&3; s=ns; x+=DX[d]; y+=DY[d]
    if t&(t-1)==0: print(t.bit_length()-1,len(g),end='; ')
print()
