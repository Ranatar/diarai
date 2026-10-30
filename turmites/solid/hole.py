# Муравей в сплошном чёрном с одной белой дыркой: как движется пара «муравей+дырка».
import sys
rule=int(sys.argv[1]); T=int(sys.argv[2])
wc=[0]*4;tn=[0]*4;ns=[0]*4
for e in range(4):
    b=(rule>>(4*e))&15; wc[e]=b&1; tn[e]=(b>>1)&3; ns[e]=(b>>3)&1
N=400; g=[[1]*N for _ in range(N)]
x=y=N//2; g[y][x]=0; d=0; s=int(sys.argv[3]) if len(sys.argv)>3 else 0
DX=[0,1,0,-1];DY=[-1,0,1,0]
for t in range(T):
    c=g[y][x]; e=s*2+c; g[y][x]=wc[e]; d=(d+tn[e])&3; s=ns[e]; x+=DX[d]; y+=DY[d]
    if t%int(sys.argv[4] if len(sys.argv)>4 else 1)==0:
        holes=[(i-N//2,j-N//2) for i in range(y-3,y+4) for j in range(x-3,x+4) if g[i][j]==0]
        print(t,x-N//2,y-N//2,d,s,holes)
