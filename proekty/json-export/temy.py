"""Тематический указатель: области памяти (pamyat/areas, pamyat/topics) ->
разговоры, где упоминаются их name/aliases.
Запуск: python3 -I temy.py ВЫХОД   (ВЫХОД — папка, сделанная razvernut.py)
Пишет ВЫХОД/temy.md.
"""
import sys, os, re, collections

vyhod = sys.argv[1]
oblasti = []
for pod in ('areas', 'topics'):
    p = os.path.join(vyhod, 'pamyat', pod)
    if not os.path.isdir(p):
        continue
    for f in sorted(os.listdir(p)):
        t = open(os.path.join(p, f), encoding='utf-8').read()
        m = re.match(r'---\n(.*?)\n---', t, re.S)
        if not m:
            continue
        shapka = m.group(1)
        name = re.search(r'^name:\s*(.+)$', shapka, re.M)
        desc = re.search(r'^description:\s*(.+)$', shapka, re.M)
        al = re.search(r'^aliases:\s*\[(.*)\]', shapka, re.M)
        klyuchi = set()
        if name:
            klyuchi.add(name.group(1).strip())
        if al:
            klyuchi |= {a.strip().strip('"\'') for a in al.group(1).split(',') if a.strip()}
        klyuchi = {k for k in klyuchi if len(k) >= 4}
        oblasti.append((pod, f, desc.group(1).strip() if desc else '', klyuchi))

# тексты разговоров: название + всё содержимое
razg = []
for kor, _, fs in os.walk(os.path.join(vyhod, 'razgovory')):
    if '.faily' in kor:   # и вложенные .faily/vetv-N/
        continue
    for f in fs:
        if f.endswith('.md'):
            put = os.path.join(kor, f)
            t = open(put, encoding='utf-8').read()
            razg.append((os.path.relpath(put, vyhod), t.split('\n', 1)[0][2:], t.lower()))

out = ['# Темы памяти и разговоры\n',
       'Для каждой области памяти — разговоры, где встречаются её имя или псевдонимы '
       '(в скобках — сколько раз). Показаны до 12 разговоров с наибольшим счётом (не меньше 3 упоминаний), по дате: получается хронология работы над темой.\n']
for pod, f, desc, klyuchi in oblasti:
    sch = collections.Counter()
    for put, nazv, t in razg:
        n = sum(t.count(k.lower()) for k in klyuchi)
        if n >= 3:
            sch[(put, nazv)] = n
    out.append(f'\n## {pod}/{f}\n\n{desc}\n\nключи: ' + ', '.join(f'`{k}`' for k in sorted(klyuchi)) + '\n')
    if not sch:
        out.append('- (не найдено)\n')
    # 12 самых насыщенных разговоров, но в хронологическом порядке (дата — начало имени файла)
    for (put, nazv), n in sorted(sch.most_common(12), key=lambda x: os.path.basename(x[0][0])):
        out.append(f'- {os.path.basename(put)[:10]} [{nazv}]({put}) ({n})')
with open(os.path.join(vyhod, 'temy.md'), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(out) + '\n')
print('областей:', len(oblasti), 'разговоров просмотрено:', len(razg))
