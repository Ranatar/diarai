from sim import *
A=parse("{{{0,2,1}, {1,4,0}}, {{1,4,1}, {0,1,0}}}")
B=parse("{{{0,2,1}, {0,4,0}}, {{1,1,0}, {1,4,1}}}")
T=60
ga,ta=run(A,T); gb,tb=run(B,T)
for i in range(T):
    print(i, ta[i], tb[i])
