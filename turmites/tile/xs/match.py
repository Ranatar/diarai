# группы одинаковых отпечатков между паркетами: ./match.py [MINTILES]
import glob, collections, sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
MIN=int(sys.argv[1]) if len(sys.argv)>1 else 500
g=collections.defaultdict(list); full=0
for fn in sorted(glob.glob('*_e*.txt')):
    til,e=fn[:-4].split('_e')
    for l in open(fn):
        p=l.split()
        if len(p)<4: continue
        c,h,n,nv=p; n=int(n); nv=int(nv)
        if n<100000 or nv<MIN: continue
        g[h].append((til,int(e),int(c),nv)); full+=1
print('правил-стартов с полным отпечатком и ≥',MIN,'плиток:',full,'; различных отпечатков:',len(g))
cross=[(h,v) for h,v in g.items() if len(set(x[0] for x in v))>1]
print('общих для разных паркетов:',len(cross))
for h,v in sorted(cross,key=lambda x:-x[1][0][3]):
    d=collections.defaultdict(list)
    for til,e,c,nv in v: d[(til,e)].append(c)
    print(v[0][3],'плиток:',' | '.join(f'{t}/e{e}: '+','.join(map(str,cs[:6]))+('…%d'%len(cs) if len(cs)>6 else '') for (t,e),cs in sorted(d.items())))
