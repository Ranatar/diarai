# замкнутая рекуррентность 26427: X_k = входы в клетку, съеденную на сдвиге k; r_k — основание эпохи k
# X_{k+1} = 3 X_k (r_{k+1}=6) или floor((5 X_k - 3)/2) (r_{k+1}=4);  r_{k+2}=6 <=> r_{k+1}=4 и X_k mod 8 in {0,2}
import sys
N=int(sys.argv[1]) if len(sys.argv)>1 else 60
X={6:39}; r={7:4}
for k in range(6,6+N):
    r[k+2]=6 if (r[k+1]==4 and X[k]%8 in (0,2)) else 4
    X[k+1]=3*X[k] if r[k+1]==6 else (5*X[k]-3)//2
for k in range(7,min(6+N,40)): print(k, r[k], X[k])
w=''.join(str(r[k]) for k in range(7,6+N)); print(w[:200])
import math
n6=w.count('6'); print('доля 6:',n6/len(w), 'log4 роста на эпоху:', (math.log(6)*n6+math.log(4)*(len(w)-n6))/len(w)/math.log(4))
