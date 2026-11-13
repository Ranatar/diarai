# матрица: сколько общих отпечатков у пар (паркет/старт)
import sys, collections, glob, os, itertools
D=sys.argv[1]; MIN=int(sys.argv[2]); NF=int(sys.argv[3])
g=collections.defaultdict(set)
for fn in glob.glob(f'{D}/*_e*.txt'):
    til,e=os.path.basename(fn)[:-4].split('_e')
    for l in open(fn):
        p=l.split()
        if len(p)<4 or int(p[2])<NF or int(p[-1])<MIN: continue
        g[p[1]].add(f'{til}/{e}')
keys=sorted({k for s in g.values() for k in s}, key=lambda k:(len(k),k))
tot=collections.Counter(k for s in g.values() for k in s)
M=collections.Counter()
for s in g.values():
    for a,b in itertools.combinations(sorted(s),2): M[(a,b)]+=1
print('классов (отпечатков) у паркета/старта:',dict(tot))
for (a,b),n in sorted(M.items(),key=lambda x:-x[1]): print(f'{a:10s} {b:10s} {n}')
