"""Последовательность поворотов пути (по клеткам): сравнить два правила со сдвигом индекса и заменой L<->R.
python3 turns.py A B N"""
import sys
from flips import run
def turns(r,N):
    _,tr=run(r,N); return ''.join('NRUL'[t[2]] for t in tr)  # абсолютное направление прихода
def rel(ds):
    D='NRUL'; return ''.join(D[(D.index(b)-D.index(a))%4] for a,b in zip(ds,ds[1:]))
if __name__=='__main__':
    A,B,N=map(int,sys.argv[1:4])
    ta=rel(turns(A,N)); tb=rel(turns(B,N))
    sw=ta.translate(str.maketrans('LR','RL'))
    print(ta[:60]); print(tb[:60])
    for name,s in (('прямо',ta),('зеркально',sw)):
        for o in range(-4,5):
            x,y=(s[o:],tb) if o>=0 else (s,tb[-o:])
            m=next((i for i,(p,q) in enumerate(zip(x,y)) if p!=q),min(len(x),len(y)))
            if m>20: print(name,o,m)
