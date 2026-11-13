# Макромодель 510: каскад клеток-счётчиков по модулю 4. Вход: A = +1, B = −1.
# Выходы: A на 3→0 даёт BB; B: 0→3 ничего, 1→0 даёт A, 2→1 даёт BB, 3→2 даёт A.
# Проверяем: (1) ответ внешней части всегда A→D, B→C (тогда модель точна); (2) переходы назад b_e поровну по рёбрам.
import sys
from tm510 import TAB, RIGHT
H=int(sys.argv[1])
ST={0:0,3:1,4:2,7:3}
tape={}; pos=0; s='A'; hi=0; lo=0
bad=0; pend={}  # pend[k] = буква входа в клетку k+1 из k
f={}; b={}
cur={}
while hi<H:
    v=tape.get(pos,0); nv,s2=TAB[(s,v)]; tape[pos]=nv
    np=pos+(1 if s2 in RIGHT else -1)
    if pos>=0 and np==pos+1: pend[pos]=s2
    if pos>0 and np==pos-1 and (pos-1) in pend:
        e=pend.pop(pos-1)
        if (e,s2) not in (('A','D'),('B','C')): bad+=1
    s=s2; pos=np
    if pos>hi: hi=pos
print('нарушений A->D,B->C справа:',bad)
