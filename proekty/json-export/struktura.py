"""Обзор структуры экспорта Claude.ai: ключи, типы content-блоков, счёт.
Запуск: python3 -I struktura.py conversations.json
"""
import json, sys, collections

path = sys.argv[1]
data = json.load(open(path, encoding='utf-8'))
print('разговоров:', len(data))
keys = collections.Counter(); mkeys = collections.Counter(); ctypes = collections.Counter()
ckeys = collections.defaultdict(collections.Counter); senders = collections.Counter()
att = collections.Counter(); files = collections.Counter()
nmsg = 0; empty_text = 0; dates = []; empty_conv = 0
for c in data:
    keys.update(c.keys()); dates.append(c['created_at'][:10])
    if not c['chat_messages']:
        empty_conv += 1
    for m in c['chat_messages']:
        nmsg += 1; mkeys.update(m.keys()); senders[m['sender']] += 1
        if not m.get('text'):
            empty_text += 1
        for b in m.get('content') or []:
            t = b.get('type'); ctypes[t] += 1; ckeys[t].update(b.keys())
        for a in m.get('attachments') or []:
            att.update(a.keys())
        for f in m.get('files') or []:
            files.update(f.keys())
print('пустых разговоров:', empty_conv)
print('сообщений:', nmsg, 'пустой text:', empty_text, 'отправители:', dict(senders))
print('даты:', min(dates), '—', max(dates))
print('ключи разговора:', dict(keys))
print('ключи сообщения:', dict(mkeys))
print('типы блоков:', dict(ctypes))
for t, k in ckeys.items():
    print(' ', t, dict(k))
print('attachments:', dict(att))
print('files:', dict(files))
