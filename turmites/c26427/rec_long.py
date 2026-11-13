import sys, math
N=int(sys.argv[1]); X=39; rn=4  # X_6, r_7
w=[]
prev4=True
for k in range(6,6+N):
    # r_{k+2} needs r_{k+1} and X_k
    r2=6 if (rn==4 and X%8 in (0,2)) else 4
    X=3*X if rn==6 else (5*X-3)//2
    w.append(rn); rn=r2
s=''.join(map(str,w)); n6=s.count('6')
print('N',N,'доля 6',n6/N,'показатель (log4 на эпоху)',(n6*math.log(6)+(N-n6)*math.log(4))/N/math.log(4))
# пары
from collections import Counter
print('после 4:', s.count('46')/s.count('4'), ' 66:', s.count('66'))
open('word_rec.txt','w').write(s+'\n')
