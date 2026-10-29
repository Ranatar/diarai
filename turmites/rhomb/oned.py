# Одномерная хорда 2845: после поворота в m муравей в s1 входит в клетку 0 (чёрную), клетки 1..n-1 чёрные, n белая.
# Ищем: где следующее событие s1-на-белом (позиция k), в каком направлении муравей туда пришёл, сколько шагов.
def run(n):
    c={i:1 for i in range(0,n)}; c[n]=0
    x=0; dr=1; s=1; t=0
    # правило: (s,col)->(write,turn,ns): turn 0=прямо,2=разворот; s1 W - поворот направо (выход)
    while True:
        col=c.get(x,0)
        if s==1 and col==0: return x,dr,t
        if s==0 and col==0: c[x]=1; dr=-dr; s=1
        elif s==0 and col==1: pass
        elif s==1 and col==1: c[x]=0; s=0
        x+=dr; t+=1
        if x<-1: return None
for n in range(1,25):
    k,dr,t=run(n); print(n,k,'+' if dr>0 else '-',t, round(t/(n*n),3))
