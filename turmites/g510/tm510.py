# Машина Тьюринга, извлечённая из ванта 510 на 4.8.8 (tm.c). Клетка v = T + 2B + 4S; A,B — идут вправо, C,D — влево.
TAB = {
 ('A',0):(3,'D'),('A',1):(6,'C'),('A',3):(4,'D'),('A',4):(7,'D'),('A',5):(0,'B'),('A',7):(2,'B'),
 ('B',0):(7,'C'),('B',1):(0,'A'),('B',2):(5,'D'),('B',3):(2,'A'),('B',4):(1,'B'),('B',5):(4,'A'),('B',6):(3,'B'),('B',7):(6,'A'),
 ('C',0):(4,'B'),('C',1):(5,'B'),('C',2):(6,'B'),('C',3):(7,'B'),('C',4):(2,'C'),('C',5):(3,'C'),('C',6):(0,'D'),('C',7):(1,'D'),
 ('D',0):(3,'A'),('D',2):(0,'C'),('D',3):(1,'C'),('D',4):(7,'A'),('D',6):(4,'C'),('D',7):(5,'C'),
}
RIGHT = {'A','B'}
def run(nmax, start='A', show=None):
    tape = {}; pos = 0; s = start; lo = hi = 0; ev = []; t = 0
    while len(ev) < nmax:
        v = tape.get(pos, 0); nv, s = TAB[(s, v)]; tape[pos] = nv; t += 1
        pos += 1 if s in RIGHT else -1
        if pos > hi: hi = pos; ev.append((t, 'R', lo, hi))
        if pos < lo: lo = pos; ev.append((t, 'L', lo, hi))
    return ev, tape
if __name__ == '__main__':
    ev, _ = run(80)
    for e in ev[-10:]: print(*e)
