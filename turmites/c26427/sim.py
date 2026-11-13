# симуляция машины 26427 (таблица tile/cnt/tm26427.txt): лента k->содержимое, состояние = вход в клетку
import sys
T={}
for l in open('../tile/cnt/tm26427.txt'):
    s,c,side,ns,nc,n=map(int,l.split()); T[(s,c)]=(side,ns,nc)
def run(N, start=150, cb=None):
    tape={}; k=0; s=start; lo=hi=0
    for n in range(N):
        c=tape.get(k,0)
        if (s,c) not in T: print('нет пары',n,s,c); break
        side,ns,nc=T[(s,c)]; tape[k]=nc; k+= 1 if side else -1; s=ns
        if k<lo or k>hi:
            lo=min(lo,k); hi=max(hi,k)
            if cb: cb(n,k,tape,lo,hi)
    return tape
if __name__=='__main__':
    def cb(n,k,tape,lo,hi): print(n,k,lo,hi)
    run(int(sys.argv[1]),cb=cb)
