"""Указатель квенья и синдарина по разговорам: какие разговоры полны эльфийских слов.
Слова — из лексикона Quettamin (ext/quettamin/branches/<ветвь>/data/lexicon.json),
формы не короче 5 букв (чтобы не ловить английские и русские короткие слова),
без дефисов и номеров омонимов. Считаются разные слова, а не вхождения.
Запуск: python3 -I kvenya_ukazatel.py ВЫХОД   (ВЫХОД — папка razvernut.py)
Пишет ВЫХОД/kvenya.md.
"""
import sys, os, re, json, collections

vyhod = sys.argv[1]
koren = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'ext', 'quettamin', 'branches')
SUP = re.compile(r'[¹²³⁴⁵⁶⁷⁸⁹⁰]+')
# частые слова других языков, совпадающие с эльфийскими формами (дополняется по выводу)
STOP = {'arrow', 'other', 'under', 'there', 'after', 'tenna', 'anna',
        # 26.10, по первому прогону: английские слова, которых нет в «Левиафане», и названия языков
        'north', 'grand', 'glass', 'gloss', 'lemma', 'tilde', 'cross', 'media', 'region', 'press',
        'brand', 'latter', 'plant', 'terra', 'faith', 'leben',
        'elven', 'quenya', 'sindarin', 'noldorin', 'eldarin', 'telerin', 'qenya'}

slovar = {}
for vetv, yazyki in (('quenya', ('q', 'nq', 'mq', 'eq')), ('sindarin', ('s', 'ns', 'n', 'g'))):
    lex = json.load(open(os.path.join(koren, vetv, 'data', 'lexicon.json'), encoding='utf-8'))
    for e in lex:
        if e['lang'] not in yazyki:
            continue
        f = SUP.sub('', e['form']).strip('-').lower()
        if len(f) < 5 or ' ' in f or not re.fullmatch(r'[a-zà-ÿāēīōūëäöüœ]+', f) or f in STOP:
            continue
        slovar.setdefault(f, (vetv, e['lang'], e.get('gloss', '')))

slovo = re.compile(r'[A-Za-zÀ-ÿĀ-ſ]+')

# слова, встречающиеся в английских, немецких и латинских текстах из ext/, эльфийскими не считаем
EXT = os.path.join(koren, '..', '..')
CHUZHIE = ['hobbes/leviathan.txt', 'poe/raven.txt', 'faust/faust.txt', 'wn/pu.txt', 'wn/oc-p.txt',
           'augustin/csel57.txt']
chuzhie = set()
for c in CHUZHIE:
    p = os.path.join(EXT, c)
    if os.path.exists(p):
        chuzhie |= {w.lower() for w in slovo.findall(open(p, encoding='utf-8', errors='replace').read())}
do = len(slovar)
slovar = {w: v for w, v in slovar.items() if w not in chuzhie}
print('убрано совпадений с английским, немецким, латынью:', do - len(slovar))
rez = []
for kor, _, fs in os.walk(os.path.join(vyhod, 'razgovory')):
    if '.faily' in kor:
        continue
    for f in fs:
        if not f.endswith('.md'):
            continue
        put = os.path.join(kor, f)
        t = open(put, encoding='utf-8').read()
        nazv = t.split('\n', 1)[0][2:]
        najd = collections.Counter(w for w in (x.lower() for x in slovo.findall(t)) if w in slovar)
        q = {w for w in najd if slovar[w][0] == 'quenya'}
        s = {w for w in najd if slovar[w][0] == 'sindarin'}
        if len(najd) >= 5:
            rez.append((len(najd), len(q), len(s), os.path.relpath(put, vyhod), nazv, najd))
rez.sort(key=lambda r: -r[0])
out = ['# Эльфийские слова в разговорах\n',
       'Разные слова из лексикона Quettamin (квенья и синдарин всех концепций и неоквенья, формы от 5 букв), '
       'найденные в тексте разговора. Совпадения с другими языками возможны: это указатель, а не разбор. '
       'Показаны разговоры с 5 и более разными словами.\n',
       '| разных слов | квенья | синдарин | разговор | частые |', '|---|---|---|---|---|']
for n, q, s, put, nazv, najd in rez:
    chastye = ', '.join(f'*{w}*' for w, _ in najd.most_common(6))
    out.append(f'| {n} | {q} | {s} | [{nazv.replace("|", "/")}]({put}) | {chastye} |')
with open(os.path.join(vyhod, 'kvenya.md'), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(out) + '\n')
# для настройки STOP: самые частые слова по всем разговорам
vse = collections.Counter()
for r in rez:
    vse.update(r[5].keys())
print('слов в словаре:', len(slovar), '; разговоров с 5+ словами:', len(rez))
print('чаще всего встречаются (в скольких разговорах):', vse.most_common(25))
