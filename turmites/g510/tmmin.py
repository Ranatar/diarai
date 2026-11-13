# Минимизация извлечённой машины по символам: ./tmmin.py tm.txt — символы эквивалентны, если при каждом
# состоянии дают ту же сторону, то же новое состояние и эквивалентный новый символ (неопределённое = особое значение)
import sys
T={}
for l in open(sys.argv[1]):
    s,c,side,ns,nc,_=map(int,l.split()); T[(s,c)]=(side,ns,nc)
S=sorted({s for s,c in T}); C=sorted({c for s,c in T}|{v[2] for v in T.values()})
cls={c:0 for c in C}
while True:
    sig={c:(cls[c],)+tuple((T[(s,c)][0],T[(s,c)][1],cls[T[(s,c)][2]]) if (s,c) in T else None for s in S) for c in C}
    ids={}; new={c:ids.setdefault(sig[c],len(ids)) for c in C}
    if len(ids)==len(set(cls.values())): break
    cls=new
print('состояний',len(S),'символов',len(C),'классов символов',len(ids))
