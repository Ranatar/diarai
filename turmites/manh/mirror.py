def load(f):
    d={}
    for l in open(f):
        p=l.split(); d[int(p[0])]=p[1:]
    return d
def tr(code,m,s):
    r=0
    for e in range(4):
        v=(code>>(3*e))&7; w=v>>2; t=v&3
        if m: t=(-t)&3
        e2=e^2 if s else e
        r|=(w*4+t)<<(3*e2)
    return r
F={k:load(f'mc21_{k}.txt') for k in ['001','010','011','100','101','110','111']}
for a in F:
  for b in F:
    if a>=b: continue
    for m in (0,1):
      for s in (0,1):
        A,B=F[a],F[b]
        n=sum(A[c][:3]==B[tr(c,m,s)][:3] and A[c][4]=='-1'==B[tr(c,m,s)][4] for c in A)
        ne=sum(A[c][4]=='-1' for c in A)
        if n>0.9*ne: print(a,b,'mirror' if m else '','swapτ' if s else '',n,ne)
