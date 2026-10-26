"""Quettamin: реконструкция слова в другом периоде (shared/reconstruct.py автора).
Запуск: python3 -I qm_rekon.py ФОРМА_Q ветвь концепция стадия [--n 6]
  ветвь: quenya|sindarin; концепция: late|middle|early; стадия — номер (late sindarin: 0 ✶ 1 AT 2 OS 3 S)
Пример: python3 -I qm_rekon.py nassë sindarin late 3
Источник — статья Q с этой формой (первая по порядку q, nq). Строит обе ветви (~1–2 мин).
"""
import sys, os

KOREN = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'ext', 'quettamin')
sys.path.insert(0, os.path.abspath(KOREN))
from shared.pipeline import build_branch                 # noqa: E402
from shared.reconstruct import Context, reconstruct      # noqa: E402

args = sys.argv[1:]
n = 6
if '--n' in args:
    i = args.index('--n'); n = int(args[i + 1]); del args[i:i + 2]
forma, db, de, ds = args[0], args[1], args[2], int(args[3])
branches = {b: build_branch(b) for b in ('quenya', 'sindarin')}
ctx = Context(branches)
kand = [e for e in branches['quenya']['lexicon'] if e['form'] == forma]
kand.sort(key=lambda e: {'q': 0, 'nq': 1}.get(e['lang'], 2))
if not kand:
    sys.exit('нет статьи ' + forma)
e = kand[0]
print(f"источник: {e['lang']} {e['form']} «{e.get('gloss', '')}» {e['id']}")
src = ('quenya', 'late', 2)
for v in reconstruct(ctx, src, (db, de, ds), word=e['id'])[:n]:
    print(f"  {v['form']:<16} {v.get('score')!s:<8} {v.get('route')}  {v.get('marks', '')}")
