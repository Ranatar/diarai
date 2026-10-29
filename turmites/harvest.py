"""Беглецы из out/growthM*.txt (growth 2^28), ещё не записанные в out/v2/deep28.txt -> печать номеров."""
import glob
done = set()
for l in open('out/v2/deep28.txt'):
    if not l.startswith('#') and l.strip(): done.add(l.split()[0])
for f in sorted(glob.glob('out/growthM*.txt')):
    for l in open(f):
        p = l.split()
        if len(p) != 22: continue
        v = [int(q.split(':')[0]) for q in p[1:]]
        if v[-1] < 0 and p[0] not in done: print(p[0])
