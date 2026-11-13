# то же, что markov.py, но степенным методом (разреженно); m до 18
import numpy as np
for m in (3,4,5,6,8,10,12,14,16,18):
    M=1<<m; x=np.arange(M)
    six=(3*x)%M                       # из (x,6) -> (3x,4)
    y0=((5*x-3)//2)%M; y1=((5*(x+M)-3)//2)%M
    r2=np.isin(x%8,(0,2))
    p4=np.full(M,1.0/M); p6=np.zeros(M)
    for it in range(400):
        n4=np.zeros(M); n6=np.zeros(M)
        np.add.at(n4,six,p6)
        w4=np.where(r2,0,p4)*0.5; w6=np.where(r2,p4,0)*0.5
        np.add.at(n4,y0,w4); np.add.at(n4,y1,w4); np.add.at(n6,y0,w6); np.add.at(n6,y1,w6)
        p4,p6=n4,n6
    a,b=p4.sum(),p6.sum(); print(m,'доля 6 %.6f'%b,'P(6|4) %.6f'%(b/a),flush=True)
