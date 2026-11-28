"""vkladka_dannye.py QM_ROOT [OUT.json] — черновик данных для вкладки «неожиданные этимологии» графа Quettamin
(по просьбе автора, hello_there 28.11: «да, можно сделать черновик»). Страницу не делает, только данные.

Устройство (письмо 35): от выбранного корня, три вида раздельно.
  roots[rid].unusual — производные корня (только прямые выводы: шаги 'd' в пути, без элементов и сложений), чья
      смысловая группа (cat-group Eldamo, по Баку) реже всего сходится под одним корнем с группами остальных его
      производных; score = средний PMI группы производного с группами прочих производных (меньше — неожиданнее).
  roots[rid].explained — производные, у чьих статей заметки Eldamo объясняют название («so called», «because»,
      «probably», «(lit.)» в глоссе) — вид (в), самый надёжный.
  words[wid].converge — сближения: похожие форма (≥ 0,75) и глосса, общего корня нет (по корням, которые находит
      сам Quettamin, со всеми правилами), у обоих корни есть.
У каждой записи: id, форма, язык, глосса, группа, правило поиска корня (via), путь (id) — чтобы рисовать на графе.
Только словарь перечней без имён и без заменённых; ранние концепции включены, язык помечен (фильтр — на странице).
2026-11-28."""
import sys, os, json, re, math, collections, itertools, difflib, unicodedata
ROOT = sys.argv[1]; OUT = sys.argv[2] if len(sys.argv) > 2 else '/home/diarai/diarai/proekty/stranicy-avtora/qm-graf/neozhidannoe.json'
sys.path.insert(0, ROOT); os.chdir(ROOT)
from shared.lexicon import words
from shared.pipeline import load_all
from shared.source import root as xml_root
W = words(); B = load_all()
GROUPS = {c.get('id'): c.get('label') for c in xml_root().iter('cat-group')}
CATS = {c.get('id'): c.get('label') for c in xml_root().iter('cat')}
PRIM = ('p', 'mp', 'ep', 'np')

ent, seen = {}, set()
for br, d in B.items():
    for e in d['lexicon']:
        if e['id'] in seen: continue
        seen.add(e['id']); ent[e['id']] = e

def info(e):
    w = W.by_id.get(e['id']); cat = (w.get('cat') if w is not None else '') or ''
    return {'id': e['id'], 'f': e['form'], 'l': e['lang'], 'g': e.get('gloss') or '', 'grp': cat[:2], 'cat': cat}

by_root = collections.defaultdict(dict)
for wid, e in ent.items():
    if e['lang'] in PRIM: continue
    w = W.by_id.get(wid)
    if w is None or (w.get('speech') or '').endswith('name') or w.find('deprecated') is not None: continue
    x = info(e)
    if not x['grp'] or x['grp'] == 'GR': continue
    for r in e.get('roots') or []:
        if r.get('via') or r.get('part') is not None: continue
        p = r.get('path') or []
        if p and all(s == 'd' for s, _ in p):
            by_root[r['id']][wid] = dict(x, path=[i for _, i in p], via='deriv')

cnt, pair, n = collections.Counter(), collections.Counter(), 0
for rid, ws in by_root.items():
    gs = {v['grp'] for v in ws.values()}
    if len(ws) < 2: continue
    n += 1
    for g in gs: cnt[g] += 1
    for a, b in itertools.combinations(sorted(gs), 2): pair[(a, b)] += 1
def pmi(a, b):
    if a == b: return 1.0
    a, b = sorted((a, b)); c = pair[(a, b)]
    return math.log(max(c, 0.5) / n / ((cnt[a] / n) * (cnt[b] / n)))

EXPL = re.compile(r'so called|because|probably named|\(lit\.\)|literally', re.I)
roots_out = {}
for rid, ws in by_root.items():
    items = list(ws.values())
    if len(items) < 3 or len({v['grp'] for v in items}) < 2: continue
    un = []
    for x in items:
        others = [y['grp'] for y in items if y is not x]
        s = sum(pmi(x['grp'], g) for g in others) / len(others)
        if s < 0: un.append(dict(x, score=round(s, 2)))
    un.sort(key=lambda v: v['score'])
    ex = []
    for x in items:
        w = W.by_id.get(x['id']); notes = (w.findtext('notes') or '') if w is not None else ''
        if EXPL.search(x['g']) or re.search(r'so called|because', notes):
            ex.append(x)
    if un or ex:
        r = W.by_id[rid]
        roots_out[rid] = {'f': r.get('v'), 'l': r.get('l'), 'g': r.get('gloss') or '', 'n': len(items),
                          'unusual': un[:6], 'explained': ex[:6]}

def fold(f):
    f = unicodedata.normalize('NFD', f.lower()); f = ''.join(c for c in f if not unicodedata.combining(c))
    return re.sub(r'[^a-zþðŋ]', '', f).replace('k', 'c').replace('ph', 'f')
STOP = set('a an the of to in on for with by from as at or and be lit thing one that which is make cause made not'.split())
def gw(g): return {t for t in re.findall(r'[a-z]+', g.lower()) if t not in STOP and len(t) > 2}
late = [e for e in ent.values() if e['lang'] in ('q', 's') and e.get('gloss') and e.get('roots')]
rootset = {e['id']: {r['id'] for r in e['roots']} | {r['form'] for r in e['roots']} for e in late}
byw = collections.defaultdict(list)
for e in late:
    for t in gw(e['gloss']): byw[t].append(e)
words_out = collections.defaultdict(list); done = set()
for t, es in byw.items():
    if len(es) > 60: continue
    for a, b in itertools.combinations(es, 2):
        k = tuple(sorted((a['id'], b['id'])))
        if k in done: continue
        done.add(k)
        fa, fb = fold(a['form']), fold(b['form'])
        if min(len(fa), len(fb)) < 3 or fa == fb: continue
        if difflib.SequenceMatcher(None, fa, fb).ratio() < 0.75: continue
        if rootset[a['id']] & rootset[b['id']]: continue
        for x, y in ((a, b), (b, a)):
            words_out[x['id']].append(dict(info(y), roots=sorted({r['form'] for r in y['roots']}),
                                           via=sorted({r.get('via') or 'deriv' for r in y['roots']})))
out = {'about': __doc__.split('\n\n')[0], 'groups': GROUPS, 'cats': CATS, 'roots': roots_out,
       'words': {k: {'f': ent[k]['form'], 'l': ent[k]['lang'], 'g': ent[k].get('gloss') or '',
                     'roots': sorted({r['form'] for r in ent[k]['roots']}), 'converge': v} for k, v in words_out.items()}}
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(f"корней: {len(roots_out)} (с unusual: {sum(1 for v in roots_out.values() if v['unusual'])}, "
      f"с explained: {sum(1 for v in roots_out.values() if v['explained'])}); слов со сближениями: {len(words_out)}; "
      f"файл: {os.path.getsize(OUT) // 1024} КБ")
