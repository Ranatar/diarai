"""Последовательность перекрашиваний двух правил; ищем симметрию g и сдвиг, при которых она совпадает.
python3 flips.py A B STEPS"""
import sys
DX=[0,1,0,-1];DY=[-1,0,1,0]
def dec(r): return [((r>>(4*e))&1, (r>>(4*e+1))&3, (r>>(4*e+3))&1) for e in range(4)]
def run(r,N):
    E=dec(r); g={}; x=y=0; d=0; s=0; fl=[]; tr=[]
    for t in range(N):
        c=g.get((x,y),0); w,tn,ns=E[s*2+c]
        tr.append((x,y,d,s,c))
        if w!=c: g[(x,y)]=w; fl.append((t,x,y,w))
        d=(d+tn)&3; s=ns; x+=DX[d]; y+=DY[d]
    return fl,tr
SYM=[lambda x,y:(x,y),lambda x,y:(-y,x),lambda x,y:(-x,-y),lambda x,y:(y,-x),
     lambda x,y:(-x,y),lambda x,y:(y,x),lambda x,y:(x,-y),lambda x,y:(-y,-x)]
if __name__=='__main__':
    A,B,N=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
    fa,ta=run(A,N); fb,tb=run(B,N)
    print('flips',len(fa),len(fb))
    for k,f in enumerate(SYM):
        for sx in range(-2,3):
            for sy in range(-2,3):
                m=0
                for (t,x,y,w),(t2,x2,y2,w2) in zip(fa,fb):
                    X,Y=f(x,y)
                    if (X+sx,Y+sy,w)!=(x2,y2,w2): break
                    m+=1
                if m>20: print('sym',k,'shift',sx,sy,'совпало подряд',m,'из',min(len(fa),len(fb)))
