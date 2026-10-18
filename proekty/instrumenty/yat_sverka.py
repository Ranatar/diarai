"""yat_sverka.py файл.md [корень_inbox]
Сверяет дореформенное написание слов файла со словарём, собранным из inbox:
для каждого слова берётся «нормальная» форма (ѣ→е, і→и, ѳ→ф, ѵ→и, конечный ъ снят),
и если в inbox та же нормальная форма встречается только в другом написании — печатается.
Смотрит лишь на слова, которые в inbox записаны по-старому (с ѣ, і, ѳ или конечным ъ)."""
import sys, os, re, collections

def norm(w):
    w = w.lower().replace('ѣ', 'е').replace('і', 'и').replace('ѳ', 'ф').replace('ѵ', 'и')
    return w[:-1] if w.endswith('ъ') else w

OLD = re.compile(r'[ѣіѳѵ]|ъ$')
WORD = re.compile(r'[а-яёѣіѳѵ]+', re.I)

root = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), '..', '..', 'inbox')
seen = collections.defaultdict(collections.Counter)
for d, _, fs in os.walk(root):
    for f in fs:
        if not f.endswith(('.html', '.txt', '.md', '.json', '.js')):
            continue
        try:
            t = open(os.path.join(d, f), encoding='utf-8', errors='ignore').read()
        except OSError:
            continue
        for w in WORD.findall(t):
            w = w.lower()
            if OLD.search(w):
                seen[norm(w)][w] += 1

mine = open(sys.argv[1], encoding='utf-8').read()
bad, ok, unknown = [], 0, 0
for w in sorted(set(x.lower() for x in WORD.findall(mine))):
    n = norm(w)
    if n in seen:
        if w in seen[n]:
            ok += 1
        else:
            bad.append((w, seen[n].most_common(3)))
    else:
        unknown += 1
for w, c in bad:
    print(w, '→', ', '.join('%s (%d)' % x for x in c))
print('совпало:', ok, 'расхождений:', len(bad), 'нет в словаре:', unknown, 'словарь:', len(seen))
