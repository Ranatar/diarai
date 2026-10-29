"""Обновить десятку рекордов «до шоссе» в NOTES.md из out/v2/report.txt (запускать после report.py)."""
s = open('NOTES.md').read()
a = s.index('- ', s.index('До шоссе — десятка лучших')); b = s.index('Самые длинные периоды шоссе:')
rep = open('out/v2/report.txt').read().split('Самые длинные периоды шоссе:')[0].strip().splitlines()[1:11]
lines = []
for l in rep:
    r, rest = l.strip().split(' (', 1); peg, rest = rest.split(', правил', 1)
    on = int(rest.split('начало ')[1].split(',')[0]); per = rest.split('период ')[1].split(',')[0]
    lines.append(f"- {r} (Пегг {peg}): {format(on, ',').replace(',', ' ')} шагов, период {per}")
open('NOTES.md', 'w').write(s[:a] + '\n'.join(lines) + '\n\n' + s[b:])
