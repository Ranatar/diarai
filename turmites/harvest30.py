"""Разбор прогона 2^30 (out/v3/onsetr30_8k_*.txt): кто вышел за поле или нашёл период и ещё не разобран.
python3 harvest30.py  -> строки «rule ...» для проверки на большем поле:
    python3 harvest30.py | cut -d' ' -f1 | ./onsetr16kPB 1073741824
Совпало начало и период на 8192 и 16384 → шоссе, дописать в out/v3/deep30.txt (секции «основное»/«проверочное»).
Не совпало / нет периода → render16k на 2^30 и смотреть глазами (двойное шоссе, квадрат из граней…) → kinds_manual.csv.
Ещё печатает остаток: сколько правил прогон не успел (их входы — out/v3/r30_0*)."""
import glob, re, csv

done = {}
for f in sorted(glob.glob('out/v3/onsetr30_8k_*.txt')):
    for l in open(f):
        p = l.split()
        if len(p) == 7: done[int(p[0])] = p
handled = set()
for l in open('out/v3/deep30.txt'):
    handled.update(int(x) for x in re.findall(r'\b(\d{2,5})\b', l.split('#')[-1]) if l.startswith('#') and 'ЛОЖН' in l)
    p = l.split()
    if len(p) == 7 and not l.startswith('#'): handled.add(int(p[0]))
handled |= {int(r['rep']) for r in csv.DictReader(open('kinds_manual.csv'))}
for r, p in done.items():
    if (p[1] != '1073741824' or p[3] != '0') and r not in handled:
        print(' '.join(p))
todo = set()
for f in sorted(glob.glob('out/v3/t30_0*')):
    todo.update(int(l.split()[0]) for l in open(f) if l.strip())
left = sorted(todo - set(done))
print(f'# сделано {len(done)} из {len(todo)}; осталось {len(left)}', flush=True)
open('out/v3/left30.txt', 'w').write(''.join(f'{r}\n' for r in left))
