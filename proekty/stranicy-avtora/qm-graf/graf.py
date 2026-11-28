"""graf.py — данные графа происхождения Quettamin (shared/graph_page.build) для разбора.
Запуск: python3 -I proekty/stranicy-avtora/qm-graf/graf.py [QM_ROOT] команда ...
  stat                 — сводка: узлы по видам, связи по отношениям
  slovo ФОРМА          — узлы с этой формой и их связи (вход/выход)
QM_ROOT по умолчанию ext/qm324. Кэш графа — ext/tmp/qm-graf.json.
2026-11-28 (пробуждение 12:07)."""
import sys, json, os, collections
ROOT = '/home/diarai/diarai/ext/qm324'
args = sys.argv[1:]
if args and os.path.isdir(args[0]):
    ROOT = args.pop(0)
CACHE = '/home/diarai/diarai/ext/tmp/qm-graf.json'

def load():
    if os.path.exists(CACHE) and os.path.getmtime(CACHE) > os.path.getmtime(ROOT + '/app/graph.html'):
        return json.load(open(CACHE, encoding='utf-8'))
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    from shared.pipeline import load_all
    from shared.graph_page import build
    g = build(load_all())
    json.dump(g, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False)
    return g

g = load()
N, E, R = g['nodes'], g['edges'], g['rels']
def name(i):
    n = N[i]; return f"{n['l']}. {n['f']}" + (f" “{n['g']}”" if n.get('g') else '') + f" [{g['ids'][i]}]"
cmd = args[0] if args else 'stat'
if cmd == 'stat':
    print('узлов', len(N), collections.Counter(n['k'] for n in N))
    print('связей', len(E), collections.Counter(R[e[2]] for e in E))
    print('nr (не доходят до корня):', sum(1 for n in N if n.get('nr')), '; из них с ds:', sum(1 for n in N if n.get('ds')))
    print('когнаты вне ветвей (cg):', sum(1 for n in N if n.get('cg')))
elif cmd == 'slovo':
    f = args[1]
    def fold(s): return s.lower().replace('k', 'c')
    hits = [i for i, n in enumerate(N) if fold(n['f']) == fold(f)]
    for i in hits:
        print('==', name(i), {k: v for k, v in N[i].items() if k not in ('f', 'l', 'g')})
        for e in E:
            if e[1] == i: print('   <-', R[e[2]], name(e[0]), e[3] if len(e) > 3 else '')
        for e in E:
            if e[0] == i: print('   ->', R[e[2]], name(e[1]), e[3] if len(e) > 3 else '')
