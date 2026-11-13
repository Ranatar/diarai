import sys; from sim import run
names={}
def nm(c):
    if c not in names: names[c]=len(names)
    return names[c]
def cb(n,k,tape,lo,hi):
    print(f'{n:>10} {hi:>3} |', ' '.join(f'{nm(tape.get(x,0)):>3}' for x in range(lo,hi+1)))
run(int(sys.argv[1]),cb=cb)
print(names)
