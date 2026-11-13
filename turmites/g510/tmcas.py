# Каскадный анализ извлечённой машины: ./tmcas.py tm319.txt START STEPS
# Проверяет: зависит ли возврат из правой (левой) части только от состояния входа; печатает макро-переходы клеток.
import sys, collections
T={}
for l in open(sys.argv[1]):
    s,c,side,ns,nc,_=map(int,l.split()); T[(s,c)]=(side,ns,nc)
st=int(sys.argv[2]); N=int(sys.argv[3])
tape=collections.defaultdict(int); pos=0
pend={}; resp=collections.defaultdict(collections.Counter); lresp=collections.defaultdict(collections.Counter); lp={}
rightstates=set(); leftstates=set()
for n in range(N):
    side,ns,nc=T[(st,tape[pos])]; tape[pos]=nc
    np=pos+(1 if side else -1)
    (rightstates if side else leftstates).add(ns)
    if np==pos+1 and pos>=0: pend[pos]=ns
    if np==pos-1 and pos>0 and (pos-1) in pend: resp[pend.pop(pos-1)][ns]+=1
    if np==pos-1 and pos<=0: lp[pos]=ns
    if np==pos+1 and pos<0 and (pos+1) in lp: lresp[lp.pop(pos+1)][ns]+=1
    pos=np; st=ns
print('вправо входят:',sorted(rightstates),' влево:',sorted(leftstates))
print('ответ правой части на вход:',{k:dict(v) for k,v in resp.items()})
print('ответ левой части на вход:',{k:dict(v) for k,v in lresp.items()})
