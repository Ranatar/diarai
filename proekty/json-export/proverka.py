"""Проверка полноты: для каждого непустого текстового блока (text, thinking)
ищем его кусок в .md разговора. Считаем пропуски.
Запуск: python3 -I proverka.py ВЫХОД conversations.json [...]
"""
import sys, os, json, re

vyhod = sys.argv[1]
po_uuid = {}
for kor, _, fs in os.walk(os.path.join(vyhod, 'razgovory')):
    if '.faily' in kor:
        continue
    for f in fs:
        if f.endswith('.md'):
            po_uuid[f[-11:-3]] = os.path.join(kor, f)
vsego = 0; propusk = 0; primery = []; bez_faila = 0
for put in sys.argv[2:]:
    for c in json.load(open(put, encoding='utf-8')):
        f = po_uuid.get(c['uuid'][:8])
        teksty = []
        for m in c['chat_messages']:
            if m['text'] and not any(b.get('type') == 'text' for b in m['content']):
                teksty.append(m['text'])
            for b in m['content']:
                if b.get('type') == 'text':
                    teksty.append(b.get('text', ''))
                elif b.get('type') == 'thinking':
                    teksty.append(b.get('thinking') or '')
        teksty = [t for t in teksty if t.strip()]
        if not teksty:
            continue
        if not f:
            bez_faila += 1
            continue
        md = open(f, encoding='utf-8').read()
        for t in teksty:
            # кусок из середины первой строки без разметки заголовков
            stroki = [s for s in t.strip().split('\n') if s.strip() and not s.lstrip().startswith('#')]
            if not stroki:
                continue
            kusok = stroki[0].strip()[:60]
            vsego += 1
            if kusok not in md:
                propusk += 1
                if len(primery) < 5:
                    primery.append((os.path.basename(f), kusok))
print('проверено кусков:', vsego, 'не найдено:', propusk, 'разговоров с текстом без файла:', bez_faila)
for p in primery:
    print(p)
