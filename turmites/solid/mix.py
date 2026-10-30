"""Мера перемешивания: по журналу прыжков (LOG) — медиана |сдвига поперечной координаты| между соседними
полётами одной ориентации, делённая на sqrt(единиц) (~ размер тела); и доля полётов, кончившихся у края (m*1 > 0.3 sqrt(A))."""
import sys,subprocess,statistics,math
for r in sys.argv[1:]:
    t0=1<<30
    out=subprocess.run(['./fastglide',r,f'tabs/{r}','34'],env={'LOG':str(t0),'LOGN':'2000'},capture_output=True,text=True,timeout=300).stdout
    J=[dict(kv.split('=') for kv in l.split()[1:]) for l in out.splitlines() if l.startswith('J ')]
    if len(J)<50: print(r,'мало прыжков',len(J)); continue
    A=int(J[-1]['ones']); L=math.sqrt(A)
    big=[j for j in J if int(j['m'])>0.05*L]
    last={}; ds=[]
    for j in big:
        vx,vy=map(int,j['v'].split(',')); o=0 if vy==0 else 1
        tr=int(j['y']) if o==0 else int(j['x'])
        if o in last: ds.append(abs(tr-last[o]))
        last[o]=tr
    trs=[]
    for j in big:
        vx,vy=map(int,j['v'].split(',')); trs.append(int(j['y']) if vy==0 else int(j['x']))
    W=30; sp=[]
    for o in (0,1):
        to=[int(j['y']) if o==0 else int(j['x']) for j in big if (j['v'].endswith(',0'))==(o==0)]
        sp+=[statistics.pstdev(to[i:i+W])/L for i in range(0,len(to)-W,W)]
    print(r, len(big), 'spread60=%.3f'%statistics.median(sp) if sp else 'spread60=-', 'mix=%.3f'%(statistics.median(ds)/L if ds else -1), 'long=%.2f'%(sum(int(j['m'])>0.5*L for j in big)/max(1,len(big))), 'A=%d'%A, flush=True)
