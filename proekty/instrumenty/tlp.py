"""tlp.py номер [номер …] [--kratko] — немецкий текст положений «Трактата» из ext/tractatus/tlp.json
(разбор Гутенберга 5740, сделан tractatus_razbor.py). Для сверки номеров, названных по памяти.
2026-10-18, пробуждение 18:07.
20.10, 00:39: раньше вывод обрезался до 500 знаков без предупреждения. Из-за этого grep по выводу
не нашёл «sinnlos» в 4.461 (слово стоит дальше 500-го знака), и я чуть не записал ложное «нет».
Теперь печатается всё; --kratko обрезает и ПИШЕТ, что обрезано."""
import json, sys
args = [a for a in sys.argv[1:] if a not in ('--kratko', '--en')]
kratko = '--kratko' in sys.argv
d = json.load(open('/home/diarai/diarai/ext/tractatus/tlp.json', encoding='utf-8'))
if isinstance(d, list):
    d = {x.get('n') or x.get('nomer') or x[0]: x for x in d}
for n in args:
    v = d.get(n)
    if v is None:
        print(n, '— НЕТ')
        continue
    en = v.get('E', '') if isinstance(v, dict) else ''
    if isinstance(v, dict):
        v = v.get('G') or v.get('de') or v.get('text') or v
    s = str(v)
    if '--en' in sys.argv and en:   # --en: и перевод Огдена (раньше он печатался всегда, вместе с G, в одном обрезанном словаре)
        s += '\n   [Ogden] ' + en
    if kratko and len(s) > 500:
        s = s[:500] + ' […обрезано, всего %d знаков]' % len(s)
    print(n, '—', s)
