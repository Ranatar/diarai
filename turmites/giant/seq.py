import sys
DX=[0,1,0,-1];DY=[-1,0,1,0]
def run(r,n):
    E=[((r>>(4*e))&1,(r>>(4*e+1))&3,(r>>(4*e+3))&1) for e in range(4)]
    g=set(); x=y=d=s=0; out=[]
    for t in range(n):
        c=1 if (x,y) in g else 0; w,tn,ns=E[s*2+c]
        out.append('abcd'[s*2+c])
        if w: g.add((x,y))
        else: g.discard((x,y))
        d=(d+tn)&3; s=ns; x+=DX[d]; y+=DY[d]
    return ''.join(out)
if __name__=='__main__':
    for r in sys.argv[2:]: print(r, run(int(r),int(sys.argv[1])))
