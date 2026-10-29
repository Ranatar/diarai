# Симуляция в нотации Пегга {{{w,t,n},{w,t,n}},{{...},{...}}}: t: 1 прямо, 2 направо, 4 разворот, 8 налево
import sys
TURN={1:0,2:1,4:2,8:3}
DX=[0,1,0,-1]; DY=[-1,0,1,0]
def parse(s):
    import re
    v=list(map(int,re.findall(r'\d+',s)))
    return [[v[0:3],v[3:6]],[v[6:9],v[9:12]]]
def run(rule,T):
    g={}; x=y=0; d=0; s=0; tr=[]
    for t in range(T):
        c=g.get((x,y),0); w,tu,n=rule[s][c]
        tr.append((x,y,d,s,c))
        g[(x,y)]=w; d=(d+TURN[tu])%4; s=n; x+=DX[d]; y+=DY[d]
    return g,tr
