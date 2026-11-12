import sys
# код манхэттенской модели из сырого правила 2x2: τ = s (или ¬s при флаге inv)
r=int(sys.argv[1]); inv=len(sys.argv)>2
code=0
for s in (0,1):
  for c in (0,1):
    e=2*s+c; v=(r>>(4*e))&15; w=v&1; t=(v>>1)&3
    tau=s^1 if inv else s
    code|=(w*4+t)<<(3*(2*tau+c))
print(code)
