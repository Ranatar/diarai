"""Сколько сообщений совсем пусты (ни text, ни content, ни вложений);
есть ли в тексте mojibake (кириллица, прочитанная как latin-1/cp1252).
Запуск: python3 -I pustye.py conversations.json
"""
import json, sys, collections, re

data = json.load(open(sys.argv[1], encoding='utf-8'))
moj = re.compile('[ÐÑ][\u0080-¿‘-›Œ-Ÿ]')
greek = re.compile('[Ͱ-Ͽ]')
pust = 0; po_godam = collections.Counter(); vsego_po_godam = collections.Counter()
n_moj = 0; n_greek = 0; primer_moj = None; primer_greek = None
for c in data:
    for m in c['chat_messages']:
        mes = m['created_at'][:7]
        vsego_po_godam[mes] += 1
        if not m['text'] and not m['content'] and not m['attachments'] and not m['files']:
            pust += 1; po_godam[mes] += 1
        teksty = [m['text']] + [b.get('text') or b.get('thinking') or '' for b in m['content']]
        for t in teksty:
            if t and moj.search(t):
                n_moj += 1
                if primer_moj is None:
                    i = moj.search(t).start(); primer_moj = t[max(0, i-40):i+80]
            if t and greek.search(t):
                n_greek += 1
                if primer_greek is None:
                    i = greek.search(t).start(); primer_greek = t[max(0, i-40):i+80]
print('совсем пустых сообщений:', pust)
for k in sorted(vsego_po_godam):
    print(k, 'всего', vsego_po_godam[k], 'пустых', po_godam[k])
print('текстов с похожим на mojibake:', n_moj, repr(primer_moj))
print('текстов с греческими буквами:', n_greek, repr(primer_greek))
