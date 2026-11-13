# сжимает последовательность переходов верхней клетки в блоки «цикл длины p × число повторов»
import sys
T=[l.split()[1] for l in open(sys.argv[1])]
i=0; out=[]
while i<len(T):
    best=None
    for p in range(1,31):
        if i+2*p<=len(T) and T[i:i+p]==T[i+p:i+2*p]: best=p; break
    if best is None: out.append((1,1,T[i])); i+=1; continue
    p=best; j=i+p
    while j+p<=len(T) and T[j:j+p]==T[i:i+p]: j+=p
    # хвост частичного цикла
    k=0
    while j+k<len(T) and k<p and T[j+k]==T[i+k]: k+=1
    out.append((p,(j-i)//p, '+%d'%k if k else '')); i=j+k
for o in out: print(o)
