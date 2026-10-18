"""Тест 12: номера положений в inbox/Suite_.txt (перевод автора на квенья, 2022) против «Трактата».
Номер «6.5.2.2.» переписывается в «6.522». Печатает номер, квенья автора и немецкий текст положения.
Вердикт ставлю глазом по первой фразе (предрегистрация — дневник 2026-10-18-1807, запись 18:21)."""
import json, re
d = json.load(open('/home/diarai/diarai/ext/tractatus/tlp.json', encoding='utf-8'))
for line in open('/home/diarai/diarai/inbox/Suite_.txt', encoding='utf-8-sig'):
    m = re.match(r'\s*(\d+(?:\.\d+)*)\.?\s+(.*)', line.strip())
    if not m:
        continue
    cifry = m.group(1).split('.')
    n = cifry[0] + ('.' + ''.join(cifry[1:]) if len(cifry) > 1 else '')
    g = d.get(n, {}).get('G', '— НЕТ ТАКОГО')
    print(f'{n:8} | {m.group(2)[:110]}\n         | {g[:160]}\n')
