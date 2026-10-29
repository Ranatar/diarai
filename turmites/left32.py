"""Остаток прогона 2^32: python3 left32.py SUFFIX -> out/v4/r32<SUFFIX>_[0-3] (по 4 потокам) и печать команды запуска.
Сделанным считается всё, что есть в out/v4/on32_*.txt и done_a.txt. Вход — out/v4/r32b_* и r32c_ (исходные списки)."""
import glob, sys
suf = sys.argv[1]
done = set()
for f in glob.glob('out/v4/on32_*.txt') + ['out/v4/done_a.txt']:
    done |= {int(l.split()[0]) for l in open(f) if len(l.split()) == 7}
todo = []
for f in sorted(glob.glob('out/v4/r32b_?')) + ['out/v4/r32c_']:
    todo += [int(l) for l in open(f) if l.strip() and int(l) not in done]
todo = sorted(set(todo))
print(f'# сделано {len(done)}, осталось {len(todo)}')
for k in range(4):
    open(f'out/v4/r32{suf}_{k}', 'w').write(''.join(f'{r}\n' for r in todo[k::4]))
print(f'for k in 0 1 2 3; do THUMBDIR=out/v4/thumbs ./onsetr16kPBT 4294967296 < out/v4/r32{suf}_$k > out/v4/on32_{suf}$k.txt 2> out/v4/st32_{suf}$k.txt & done; wait')
print('# (Bash с run_in_background: true; суффикс каждый раз новый)')
