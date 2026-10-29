"""Поиск «ползков»: одномерных циклов из k входов (только прямо/разворот), которые на однородной линии цвета c
сдвигают муравья на +1 с тем же состоянием и направлением и восстанавливают цвет. k=1 — прозрачный вход."""
import sys
def dec(r):
    return [((r>>(4*e))&1, (r>>(4*e+1))&3, (r>>(4*e+3))&1) for e in range(4)]
def crawls(r, K=8):
    E=dec(r); out=[]
    for s0 in (0,1):
        for c in (0,1):
            cells={}; x=0; dr=1; s=s0
            for k in range(1,K+1):
                col=cells.get(x,c); wc,tn,ns=E[s*2+col]
                if tn in (1,3): break
                cells[x]=wc; 
                if tn==2: dr=-dr
                s=ns; x+=dr
                if x==1 and dr==1 and s==s0 and all(v==c for v in cells.values()):
                    out.append((s0,c,k)); break
                if abs(x)>3: break
    return out
if __name__=='__main__':
    for l in sys.stdin:
        r=int(l); cr=crawls(r)
        if cr: print(r, ' '.join(f's{s}{"WB"[c]}:{k}' for s,c,k in cr))
