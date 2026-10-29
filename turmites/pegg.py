"""Перевод нотации Пегга/Golly (12 цифр: s0c0 s0c1 s1c0 s1c1 по тройкам write,turn,next; turn 1=N 2=R 4=U 8=L) в мой код и обратно."""
import sys
T2M = {1: 0, 2: 1, 4: 2, 8: 3}; M2T = {v: k for k, v in T2M.items()}
def from_pegg(s):
    d = [int(c) for c in s]; r = 0
    for e in range(4):
        w, t, n = d[3*e:3*e+3]
        r |= (w | T2M[t] << 1 | n << 3) << (4*e)
    return r
def to_pegg(r):
    out = ''
    for e in range(4):
        b = (r >> 4*e) & 15
        out += f'{b&1}{M2T[(b>>1)&3]}{(b>>3)&1}'
    return out
if __name__ == '__main__':
    for a in sys.argv[1:]:
        print(a, from_pegg(a) if len(a) == 12 else to_pegg(int(a)))
