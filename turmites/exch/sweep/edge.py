# 16234 как одно-состоянийный муравей: состояние после шага = тип пересечённого ребра?
import sys
r=int(sys.argv[1]); T=int(sys.argv[2])
wc=[0]*4;tn=[0]*4;ns=[0]*4
for e in range(4):
    b=(r>>(4*e))&15; wc[e]=b&1; tn[e]=(b>>1)&3; ns[e]=(b>>3)&1
DX=[0,1,0,-1];DY=[-1,0,1,0]
g={};x=y=d=s=0
tab={}
bad=0
for t in range(T):
    c=g.get((x,y),0); e=s*2+c
    g[(x,y)]=wc[e]; d=(d+tn[e])&3; s=ns[e]
    nx,ny=x+DX[d],y+DY[d]
    # ребро: вертикальное между столбцами min(x,nx),+1 -> ключ ('v', min(x,nx) mod 2); горизонтальное ('h', min(y,ny) mod 2)
    k=('v',min(x,nx)%2) if nx!=x else ('h',min(y,ny)%2)
    if k in tab and tab[k]!=s: bad+=1
    tab.setdefault(k,s)
    x,y=nx,ny
print(r,'map',tab,'violations',bad)
print('table:',[(e>>1,e&1,'write',wc[e],'turn','NRUL'[tn[e]],'new',ns[e]) for e in range(4)])
