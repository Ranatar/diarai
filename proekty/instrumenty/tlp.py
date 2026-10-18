"""tlp.py номер [номер …] — немецкий текст положений «Трактата» из ext/tractatus/tlp.json
(разбор Гутенберга 5740, сделан tractatus_razbor.py). Для сверки номеров, названных по памяти.
2026-10-18, пробуждение 18:07."""
import json, sys
d = json.load(open('/home/diarai/diarai/ext/tractatus/tlp.json', encoding='utf-8'))
if isinstance(d, list):
    d = {x.get('n') or x.get('nomer') or x[0]: x for x in d}
for n in sys.argv[1:]:
    v = d.get(n)
    if v is None:
        print(n, '— НЕТ')
        continue
    if isinstance(v, dict):
        v = v.get('de') or v.get('text') or v
    print(n, '—', str(v)[:500])
