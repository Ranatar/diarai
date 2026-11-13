# Макропереходы клетки каскада: для правой половины. ./macro2.py tm.txt RIGHTRESP (напр. "23:45,0:52,1:43")
import sys, collections, itertools
T={}
for l in open(sys.argv[1]):
    s,c,side,ns,nc,_=map(int,l.split()); T[(s,c)]=(side,ns,nc)
RR={int(a):int(b) for a,b in (x.split(':') for x in sys.argv[2].split(','))}
ins=list(RR)
syms=sorted({c for (s,c) in T})
def macro(letter,sym):
    st=letter; c=sym; out=[]
    for _ in range(100):
        if (st,c) not in T: return None
        side,ns,nc=T[(st,c)]; c=nc
        if side==0: return (c,out,ns)
        out.append(ns); st=RR[ns]   # ушла вправо — вернулась с ответом
    return 'loop'
rest=set(); todo=[0]; M={}
while todo:
    s=todo.pop()
    if s in rest: continue
    rest.add(s)
    for a in ins:
        r=macro(a,s)
        if r and r!='loop':
            M[(a,s)]=r; todo.append(r[0])
for (a,s),(c,out,ex) in sorted(M.items()): print(f'вход {a:2d} в {s:3d} -> {c:3d}, выпуск {out}, выход {ex}')
# матрица счёта (в предположении равномерности состояний — для сравнения)
