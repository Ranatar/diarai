"""Калибровка по всем сырым правилам, чей класс в группах двойников (или в каталоге).
python3 odd2/gauge_all.py N > odd2/gauge_all.txt"""
import sys, os
sys.path.insert(0, os.getcwd())
from odd2gauge import gauge, cls, cat
exec(open('odd2/gauge_check.py').read().split('N=int')[0].split('from odd2gauge')[1].split('\n',1)[1])
N=int(sys.argv[1])
groups=[list(map(int,l.split(':')[1].split())) for l in open('solid/twins.txt') if ':' in l and not l.startswith('#')]
tw={r for g in groups for r in g}
seen=set()
for r in range(65536):
    c=cls(r)
    if c not in tw: continue
    A=None
    for k in (1,2,3):
        b=gauge(r,k); cb=cls(b)
        if cb==c or (c,cb) in seen: continue
        if A is None: A=reads(r,N)
        if reads(b,N)==A: seen.add((c,cb)); seen.add((cb,c)); print(c,k,cb,r,b,flush=True)
