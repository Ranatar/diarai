"""Какие инструменты вызывались, с какими ключами input; ветвление деревьев сообщений.
Запуск: python3 -I instrumenty_vyzovy.py conversations.json
"""
import json, sys, collections

data = json.load(open(sys.argv[1], encoding='utf-8'))
names = collections.Counter(); ikeys = collections.defaultdict(collections.Counter)
vetv = 0; max_deti = 0; summ = 0; att_types = collections.Counter()
for c in data:
    if c.get('summary'):
        summ += 1
    deti = collections.Counter(m['parent_message_uuid'] for m in c['chat_messages'])
    if deti and max(deti.values()) > 1:
        vetv += 1; max_deti = max(max_deti, max(deti.values()))
    for m in c['chat_messages']:
        for a in m['attachments']:
            att_types[a.get('file_type')] += 1
        for b in m['content']:
            if b['type'] == 'tool_use':
                names[b['name']] += 1
                if isinstance(b['input'], dict):
                    ikeys[b['name']].update(b['input'].keys())
print('разговоров с summary:', summ)
print('разговоров с ветвлением:', vetv, 'макс. детей у узла:', max_deti)
print('типы вложений:', dict(att_types))
for n, k in names.most_common(40):
    print(k, n, dict(ikeys[n]))
