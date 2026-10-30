"""Сводка прогона fastglide: python3 summ.py DIR -> rule последний_2^k ones w h доля_глайдера показатель(последнее удвоение) [escape]"""
import sys,glob,re,math,os
rows=[]
for f in glob.glob(sys.argv[1]+'/*.txt'):
    r=int(os.path.basename(f)[:-4]); L=[l for l in open(f) if l.startswith('2^')]; esc=[l for l in open(f) if l.startswith('escape')]
    if not L: continue
    p=lambda l: dict(kv.split('=') for kv in l.split()[1:])
    a=p(L[-1]); k=int(L[-1].split()[0][2:])
    ex=math.log2(int(a['ones'])/int(p(L[-2])['ones'])) if len(L)>1 and int(p(L[-2])['ones'])>0 else 0
    rows.append((r,k,int(a['ones']),int(a['w']),int(a['h']),float(a['gl']),ex,esc[0].split()[2] if esc else ''))
rows.sort(key=lambda x:-x[5])
for r in rows: print('%6d 2^%d %9d %5d %5d %.3f %.2f %s'%r)
