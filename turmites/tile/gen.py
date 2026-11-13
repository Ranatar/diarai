# Геометрия периодических паркетов -> таблица смежности для движка (tiling.h).
# Плитка: тип t в фундаментальной области; рёбра по часовой… нет — ПРОТИВ часовой, ребро j между вершинами j и j+1.
# Сосед через ребро j плитки t в ячейке (0,0): (тип t', сдвиг di,dj, ребро j').
import math, sys
def poly(c, n, R, a0):
    return [(c[0]+R*math.cos(a0+2*math.pi*j/n), c[1]+R*math.sin(a0+2*math.pi*j/n)) for j in range(n)]
def tiling(name):
    r3=math.sqrt(3); d=math.radians
    if name=='488':
        s=1+math.sqrt(2); a1=(s,0); a2=(0,s)
        prim=[((0,0),8,1/(2*math.sin(math.pi/8)),d(22.5))]
        sec=[((s/2,s/2),4,math.sqrt(2)/2)]
    elif name=='31212':
        D=2+r3; a1=(D,0); a2=(D/2,D*r3/2)
        prim=[((0,0),12,1/(2*math.sin(math.pi/12)),d(15))]
        c1=((a1[0]+a2[0])/3,(a1[1]+a2[1])/3); c2=(2*c1[0],2*c1[1])
        sec=[(c1,3,1/r3),(c2,3,1/r3)]
    elif name=='4612':
        D=3+r3; a1=(D,0); a2=(D/2,D*r3/2)
        prim=[((0,0),12,1/(2*math.sin(math.pi/12)),d(15))]
        c1=((a1[0]+a2[0])/3,(a1[1]+a2[1])/3); c2=(2*c1[0],2*c1[1])
        sec=[(c1,6,1.0),(c2,6,1.0),((a1[0]/2,a1[1]/2),4,math.sqrt(2)/2),((a2[0]/2,a2[1]/2),4,math.sqrt(2)/2),
             (((a2[0]-a1[0])/2+a1[0],(a2[1]-a1[1])/2+a1[1]),4,math.sqrt(2)/2)]
    elif name=='666':
        a1=(r3,0); a2=(r3/2,1.5)
        prim=[((0,0),6,1.0,d(30))]; sec=[]
    elif name=='3464':
        D=1+r3; a1=(D,0); a2=(D/2,D*r3/2)
        prim=[((0,0),6,1.0,d(30))]
        c1=((a1[0]+a2[0])/3,(a1[1]+a2[1])/3); c2=(2*c1[0],2*c1[1])
        sec=[(c1,3,1/r3),(c2,3,1/r3),((a1[0]/2,a1[1]/2),4,math.sqrt(2)/2),((a2[0]/2,a2[1]/2),4,math.sqrt(2)/2),
             (((a2[0]-a1[0])/2+a1[0],(a2[1]-a1[1])/2+a1[1]),4,math.sqrt(2)/2)]
    return a1,a2,prim,sec
def build(name):
    a1,a2,prim,sec=tiling(name)
    off=lambda c,i,j:(c[0]+i*a1[0]+j*a2[0],c[1]+i*a1[1]+j*a2[1])
    verts=[]
    for i in range(-3,4):
        for j in range(-3,4):
            for c,n,R,a0 in prim: verts+=poly(off(c,i,j),n,R,a0)
    tiles=[]  # (type, i, j, vertex list CCW)
    types=[]
    for c,n,R,a0 in prim: types.append((c,n,'p',(R,a0)))
    for c,n,R in sec: types.append((c,n,'s',R))
    for t,(c,n,kind,par) in enumerate(types):
        for i in range(-2,3):
            for j in range(-2,3):
                cc=off(c,i,j)
                if kind=='p': vs=poly(cc,n,*par)
                else:
                    vs=[v for v in verts if abs(math.dist(v,cc)-par)<1e-6]
                    u={}; 
                    for v in vs: u[(round(v[0],5),round(v[1],5))]=v
                    vs=sorted(u.values(),key=lambda v:math.atan2(v[1]-cc[1],v[0]-cc[0]))
                    assert len(vs)==n,(name,t,len(vs))
                tiles.append((t,i,j,vs))
    emap={}
    for (t,i,j,vs) in tiles:
        n=len(vs)
        for e in range(n):
            m=((vs[e][0]+vs[(e+1)%n][0])/2,(vs[e][1]+vs[(e+1)%n][1])/2)
            emap.setdefault((round(m[0],4),round(m[1],4)),[]).append((t,i,j,e))
    adj={}
    for k,lst in emap.items():
        if len(lst)!=2: continue
        for a,b in ((lst[0],lst[1]),(lst[1],lst[0])):
            if a[1]==0 and a[2]==0: adj[(a[0],a[3])]=(b[0],b[1],b[2],b[3])
    for t,(c,n,_,_) in enumerate(types):
        for e in range(n): assert (t,e) in adj,(name,t,e)
    return types,adj,a1,a2
if __name__=='__main__':
    name=sys.argv[1]; types,adj,a1,a2=build(name)
    print('/* сгенерировано gen.py %s */'%name)
    print('#define NT %d'%len(types)); print('static const int SIDES[NT]={%s};'%','.join(str(n) for (_,n,_,_) in types))
    print('static const int ADJ[NT][12][4]={')
    for t,(c,n,_,_) in enumerate(types):
        print(' {'+','.join('{%d,%d,%d,%d}'%adj[(t,e)] for e in range(n))+'},')
    print('};'); print('static const double A1[2]={%r,%r},A2[2]={%r,%r};'%(a1+a2))
    print('static const double CEN[NT][2]={%s};'%','.join('{%r,%r}'%c for (c,_,_,_) in types))
