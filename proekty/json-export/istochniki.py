"""Пробует сопоставить метки [s:xxxxxxxxxxxxxxxx] из памяти с разговорами:
хэши (md5, sha1, sha256) от uuid разговора и сообщений, начало и конец uuid.
Запуск: python3 -I istochniki.py папка_pamyat conversations.json [...]
"""
import sys, os, re, json, hashlib

metki = set()
for kor, _, fs in os.walk(sys.argv[1]):
    for f in fs:
        metki |= set(re.findall(r'\[s:([0-9a-f]+)\]', open(os.path.join(kor, f), encoding='utf-8').read()))
print('меток:', len(metki), sorted(metki)[:5])
naideno = {}
for put in sys.argv[2:]:
    for c in json.load(open(put, encoding='utf-8')):
        kandidaty = [('conv', c['uuid'])] + [('msg', m['uuid']) for m in c['chat_messages']]
        for vid, u in kandidaty:
            for s in (u, u.replace('-', '')):
                for h in ('md5', 'sha1', 'sha256'):
                    d = hashlib.new(h, s.encode()).hexdigest()
                    for x in (d[:16], d[-16:]):
                        if x in metki:
                            naideno[x] = (vid, h, c['uuid'], c.get('name'))
                if s.replace('-', '')[:16] in metki:
                    naideno[s.replace('-', '')[:16]] = (vid, 'prefix', c['uuid'], c.get('name'))
print('сопоставлено:', len(naideno))
for k, v in naideno.items():
    print(k, v)
