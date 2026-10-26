"""Разворачивает экспорт Claude.ai (conversations.json, memories/*.json)
в человекочитаемые Markdown-файлы.

Запуск:
  python3 -I razvernut.py ВЫХОД conversations.json [conversations2.json ...] [--memories memories.json]

Что получается в ВЫХОД/:
  README.md                 — как читать, счёт
  index.md, index.tsv       — все разговоры по дате
  razgovory/ГГГГ-ММ/ДАТА_название_uuid8.md — по файлу на разговор
  razgovory/ГГГГ-ММ/ДАТА_название_uuid8.faily/ — итоговые версии файлов и артефактов,
                              собранные из вызовов create_file / Write / artifacts / str_replace / Edit
  pamyat/                   — память: общий текст и memory_files по их путям

Ветвление: у сообщения есть parent_message_uuid; при правке или перегенерации
у одного родителя бывает несколько детей. Главной считается ветвь с наибольшим
числом непустых сообщений (при равенстве — более поздняя). Остальные ветви
выводятся в конце файла в разделе «Другие ветви».
"""
import json, sys, os, re, collections

KOREN = '00000000-0000-4000-8000-000000000000'
OBREZ_REZ = 2000      # сколько знаков результата инструмента показывать
OBREZ_VHOD = 3000     # сколько знаков входа инструмента показывать


def slug(s, n=60):
    s = re.sub(r'[^\w\-]+', '-', s or '', flags=re.U).strip('-')
    return (s[:n].rstrip('-')) or 'bez-nazvaniya'


def obrez(s, n):
    if len(s) <= n:
        return s
    return s[:n] + f'\n… [обрезано: показано {n} из {len(s)} знаков]'


def zabor(s):
    """Ограда для блока кода, которой нет внутри текста."""
    z = '```'
    while z in s:
        z += '`'
    return z


def vremya(ts):
    return (ts or '')[:19].replace('T', ' ')


def pust(m):
    return not (m.get('text') or m.get('content') or m.get('attachments') or m.get('files'))


def tekst_rezultata(b):
    c = b.get('content')
    if isinstance(c, str):
        return c
    chasti = []
    for x in c or []:
        if isinstance(x, dict):
            if x.get('type') == 'text':
                chasti.append(x.get('text', ''))
            elif x.get('type') == 'image':
                chasti.append('[картинка]')
            else:
                t = x.get('text') or x.get('title') or x.get('url')
                chasti.append(str(t) if t else json.dumps(x, ensure_ascii=False)[:300])
        else:
            chasti.append(str(x))
    return '\n'.join(chasti)


def vhod_instrumenta(b):
    inp = b.get('input')
    name = b.get('name', '?')
    if not isinstance(inp, dict):
        return json.dumps(inp, ensure_ascii=False)
    if name in ('bash_tool', 'Bash') and 'command' in inp:
        opis = inp.get('description', '')
        return (f'# {opis}\n' if opis else '') + inp['command']
    if name == 'repl' and 'code' in inp:
        return inp['code']
    # длинные поля с содержимым файлов показываем коротко: сами файлы лежат в .faily/
    d = {}
    for k, v in inp.items():
        if k in ('content', 'file_text', 'new_str', 'old_str', 'new_string', 'old_string') and isinstance(v, str) and len(v) > 300:
            d[k] = f'[{len(v)} знаков]'
        else:
            d[k] = v
    return json.dumps(d, ensure_ascii=False, indent=1)


class Faily:
    """Собирает итоговые версии файлов из вызовов инструментов одного разговора."""

    def __init__(self):
        self.f = collections.OrderedDict()   # ключ -> (имя, текст)
        self.oshibki = 0

    def _zamena(self, kl, imya, old, new):
        if kl not in self.f:
            self.oshibki += 1
            return
        t = self.f[kl][1]
        if old in t:
            self.f[kl] = (imya, t.replace(old, new, 1))
        else:
            self.oshibki += 1

    def vyzov(self, b):
        inp = b.get('input')
        if not isinstance(inp, dict):
            return
        n = b.get('name')
        if n == 'create_file' and 'file_text' in inp:
            p = inp.get('path', 'bez-imeni')
            self.f[p] = (p, inp['file_text'])
        elif n == 'Write' and 'content' in inp:
            p = inp.get('file_path', 'bez-imeni')
            self.f[p] = (p, inp['content'])
        elif n == 'str_replace' and 'path' in inp:
            self._zamena(inp['path'], inp['path'], inp.get('old_str', ''), inp.get('new_str', ''))
        elif n == 'Edit' and 'file_path' in inp:
            p = inp['file_path']
            if inp.get('replace_all') and p in self.f:
                self.f[p] = (p, self.f[p][1].replace(inp.get('old_string', ''), inp.get('new_string', '')))
            else:
                self._zamena(p, p, inp.get('old_string', ''), inp.get('new_string', ''))
        elif n == 'artifacts':
            kl = 'artifact:' + str(inp.get('id'))
            imya = inp.get('title') or str(inp.get('id'))
            cmd = inp.get('command')
            if cmd in ('create', 'rewrite') and 'content' in inp:
                yaz = inp.get('language') or inp.get('type') or ''
                self.f[kl] = (imya + '|' + yaz, inp['content'])
            elif cmd == 'update':
                stroe = self.f.get(kl, (imya, ''))[0]
                self._zamena(kl, stroe, inp.get('old_str', ''), inp.get('new_str', ''))

    def zapisat(self, papka):
        if not self.f:
            return []
        os.makedirs(papka, exist_ok=True)
        imena = []
        zanyato = set()
        for kl, (imya, t) in self.f.items():
            if kl.startswith('artifact:'):
                nazv, _, yaz = imya.partition('|')
                rassh = rasshirenie(yaz)
                osn = slug(nazv, 50) + rassh
            else:
                osn = os.path.basename(imya.rstrip('/')) or 'bez-imeni'
            osn = re.sub(r'[^\w.\-]+', '_', osn)
            x, i = osn, 2
            while x in zanyato:
                k, r = os.path.splitext(osn)
                x = f'{k}_{i}{r}'; i += 1
            zanyato.add(x)
            with open(os.path.join(papka, x), 'w', encoding='utf-8') as fh:
                fh.write(t)
            imena.append((x, imya.partition('|')[0]))
        return imena


def rasshirenie(yaz):
    yaz = (yaz or '').lower()
    tabl = {'python': '.py', 'javascript': '.js', 'typescript': '.ts', 'html': '.html',
            'text/html': '.html', 'text/markdown': '.md', 'markdown': '.md',
            'application/vnd.ant.react': '.jsx', 'application/vnd.ant.code': '.txt',
            'image/svg+xml': '.svg', 'application/vnd.ant.mermaid': '.mmd',
            'lisp': '.lisp', 'json': '.json', 'css': '.css', 'latex': '.tex', 'bash': '.sh'}
    return tabl.get(yaz, '.txt')


def vetvi(msgs):
    """Главная ветвь и остальные. Возвращает (главная: список, другие: список списков)."""
    po_uuid = {m['uuid']: m for m in msgs}
    deti = collections.defaultdict(list)
    for m in msgs:
        p = m['parent_message_uuid']
        if p not in po_uuid:
            p = KOREN
        deti[p].append(m)
    for v in deti.values():
        v.sort(key=lambda m: m['created_at'])

    # лучший путь от узла вниз: (непустых, позднейшее время)
    luchshij = {}

    def ocenka(u):
        stek = [(u, False)]
        while stek:
            x, gotovo = stek.pop()
            if x in luchshij:
                continue
            if not gotovo:
                stek.append((x, True))
                for d in deti.get(x, []):
                    if d['uuid'] not in luchshij:
                        stek.append((d['uuid'], False))
                continue
            sam = 0 if x == KOREN else (0 if pust(po_uuid[x]) else 1)
            t = '' if x == KOREN else po_uuid[x]['created_at']
            best = (0, t, None)
            for d in deti.get(x, []):
                n, tt, _ = luchshij[d['uuid']]
                if (n, tt) > best[:2]:
                    best = (n, tt, d['uuid'])
            luchshij[x] = (best[0] + sam, max(best[1], t), best[2])

    ocenka(KOREN)

    def put_ot(u):
        p = []
        while u is not None:
            if u != KOREN:
                p.append(po_uuid[u])
            u = luchshij[u][2]
        return p

    glavnaya = put_ot(KOREN)
    na_glavnoj = {m['uuid'] for m in glavnaya}
    drugie = []
    # от каждого узла главной (и корня) — альтернативные дети
    ochered = [KOREN] + [m['uuid'] for m in glavnaya]
    vidimo = set(na_glavnoj)
    while ochered:
        u = ochered.pop(0)
        for d in deti.get(u, []):
            if d['uuid'] in vidimo:
                continue
            p = put_ot(d['uuid'])
            if all(pust(m) for m in p):
                for m in p:
                    vidimo.add(m['uuid'])
                continue
            drugie.append((u, p))
            for m in p:
                vidimo.add(m['uuid'])
                ochered.append(m['uuid'])
    return glavnaya, drugie, len(msgs) - len(vidimo)


def ponizit(t):
    """Заголовки внутри реплики опускаем на два уровня, чтобы они не спорили
    с заголовками реплик (##). Внутри блоков кода не трогаем."""
    out = []; v_kode = None
    for s in t.split('\n'):
        m = re.match(r'^\s{0,3}(`{3,}|~{3,})', s)
        if m:
            z = m.group(1)
            if v_kode is None:
                v_kode = z
            elif z.startswith(v_kode[0]) and len(z) >= len(v_kode):
                v_kode = None
        elif v_kode is None and re.match(r'^#{1,4}\s', s):
            s = '##' + s
        out.append(s)
    return '\n'.join(out)


def soobshchenie(m, out, faily, nomer):
    kto = '🧑 Человек' if m['sender'] == 'human' else '🤖 Claude'
    out.append(f'## {nomer}. {kto} · {vremya(m["created_at"])}\n')
    if pust(m):
        out.append('*(в экспорте сообщение пустое)*\n')
        return
    bloki = m.get('content') or []
    est_tekst = any(b.get('type') == 'text' for b in bloki)
    if not est_tekst and m.get('text'):
        out.append(ponizit(m['text'].strip()) + '\n')
    for b in bloki:
        t = b.get('type')
        if t == 'text':
            if b.get('text', '').strip():
                out.append(ponizit(b['text'].strip()) + '\n')
        elif t == 'thinking':
            th = (b.get('thinking') or '').strip()
            if th:
                out.append('<details><summary>размышление</summary>\n\n' + ponizit(th) + '\n\n</details>\n')
        elif t == 'tool_use':
            faily.vyzov(b)
            v = obrez(vhod_instrumenta(b), OBREZ_VHOD)
            z = zabor(v)
            out.append(f'**⚙ {b.get("name")}**\n\n{z}\n{v}\n{z}\n')
        elif t == 'tool_result':
            r = tekst_rezultata(b).strip()
            if not r:
                continue
            r = obrez(r, OBREZ_REZ)
            z = zabor(r)
            osh = ' (ошибка)' if b.get('is_error') else ''
            out.append(f'<details><summary>результат {b.get("name", "")}{osh}</summary>\n\n{z}\n{r}\n{z}\n\n</details>\n')
        elif t == 'image':
            out.append('*[картинка]*\n')
        elif t == 'document':
            out.append(f'*[документ: {b.get("title") or b.get("sandbox_upload_name") or b.get("file_uuid")}]*\n')
        elif t in ('token_budget', 'injected_prompt_block'):
            pass
        else:
            out.append(f'*[блок {t}]*\n')
    for a in m.get('attachments') or []:
        ec = a.get('extracted_content') or ''
        out.append(f'<details><summary>вложение: {a.get("file_name")} ({a.get("file_size")} байт)</summary>\n\n'
                   + (lambda s: f'{zabor(s)}\n{s}\n{zabor(s)}')(obrez(ec, 20000)) + '\n\n</details>\n')
    fl = [f.get('file_name') for f in m.get('files') or []]
    if fl:
        out.append('*Файлы (в экспорт не вошли):* ' + ', '.join(f'`{x}`' for x in fl) + '\n')


def razgovor(c, vyhod):
    data = c['created_at'][:10]
    nazv = c.get('name') or ''
    if not nazv:
        # без названия: берём начало первой непустой реплики человека
        for m in sorted(c['chat_messages'], key=lambda m: m['created_at']):
            t = m.get('text') or ' '.join(b.get('text', '') for b in m.get('content') or [] if b.get('type') == 'text')
            if m['sender'] == 'human' and t.strip():
                nazv = '«' + ' '.join(t.split())[:70] + '…»'
                break
    imya = f'{data}_{slug(nazv.strip("«»…"))}_{c["uuid"][:8]}'
    papka = os.path.join(vyhod, 'razgovory', data[:7])
    os.makedirs(papka, exist_ok=True)
    msgs = c['chat_messages']
    nepust = sum(not pust(m) for m in msgs)
    if nepust == 0 and not c.get('summary'):
        # пустая запись: ни названия, ни текста — файла не пишем
        return dict(data=data, nazv=nazv, uuid=c['uuid'], fail='', vsego=len(msgs),
                    nepust=0, vetvej=0, failov=0)
    glavnaya, drugie, poteryano = vetvi(msgs)
    faily = Faily()
    out = [f'# {nazv or "(без названия)"}\n',
           f'- создан: {vremya(c["created_at"])} UTC; обновлён: {vremya(c["updated_at"])} UTC',
           f'- uuid: `{c["uuid"]}`',
           f'- сообщений в экспорте: {len(msgs)}, непустых: {sum(not pust(m) for m in msgs)}; '
           f'в главной ветви: {len(glavnaya)}; других ветвей: {len(drugie)}\n']
    if c.get('summary'):
        out.append('**Краткое содержание (из экспорта):**\n\n' + c['summary'].strip() + '\n')
    out.append('---\n')
    for i, m in enumerate(glavnaya, 1):
        soobshchenie(m, out, faily, i)
    if drugie:
        out.append('\n---\n\n# Другие ветви\n\nПравки и перегенерации: альтернативные продолжения, '
                   'которые не вошли в главную ветвь.\n')
        nomer_po_uuid = {m['uuid']: i for i, m in enumerate(glavnaya, 1)}
        for j, (ot, p) in enumerate(drugie, 1):
            gde = ('от начала разговора' if ot == KOREN else
                   f'после реплики {nomer_po_uuid[ot]} главной ветви' if ot in nomer_po_uuid else
                   f'от другой ветви (`{ot[:8]}`)')
            out.append(f'\n## ⑂ Ветвь {j} — {gde}\n')
            for i, m in enumerate(p, 1):
                soobshchenie(m, out, Faily(), f'{j}.{i}')
    imena = faily.zapisat(os.path.join(papka, imya + '.faily'))
    if imena:
        out.insert(4, '**Файлы, собранные из вызовов инструментов** (последние версии): '
                   + ', '.join(f'[{x}]({imya}.faily/{x})' for x, _ in imena)
                   + (f' — правок, которые не удалось применить: {faily.oshibki}' if faily.oshibki else '') + '\n')
    with open(os.path.join(papka, imya + '.md'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out))
    return dict(data=data, nazv=nazv, uuid=c['uuid'], fail=f'razgovory/{data[:7]}/{imya}.md',
                vsego=len(msgs), nepust=nepust, vetvej=len(drugie), failov=len(imena))


def pamyat(path, vyhod):
    d = json.load(open(path, encoding='utf-8'))
    p = os.path.join(vyhod, 'pamyat')
    os.makedirs(p, exist_ok=True)
    with open(os.path.join(p, '00-obshchaya-pamyat.md'), 'w', encoding='utf-8') as fh:
        fh.write('# Общая память о разговорах (conversations_memory)\n\n' + (d.get('conversations_memory') or ''))
    n = 0
    for f in d.get('memory_files') or []:
        rel = (f.get('path') or f'bez-puti-{n}.md').lstrip('/')
        rel = os.path.normpath(rel)
        if rel.startswith('..'):
            continue
        cel = os.path.join(p, rel)
        os.makedirs(os.path.dirname(cel), exist_ok=True)
        with open(cel, 'w', encoding='utf-8') as fh:
            fh.write(f.get('content') or '')
            fh.write(f'\n\n<!-- обновлено: {f.get("updated_at")} -->\n')
        n += 1
    return n


def main():
    args = sys.argv[1:]
    mem = None
    if '--memories' in args:
        i = args.index('--memories'); mem = args[i + 1]; del args[i:i + 2]
    vyhod, vhody = args[0], args[1:]
    os.makedirs(vyhod, exist_ok=True)
    stroki = []
    for v in vhody:
        data = json.load(open(v, encoding='utf-8'))
        for c in data:
            stroki.append(razgovor(c, vyhod))
        del data
    stroki.sort(key=lambda r: r['data'])
    pustye = [r for r in stroki if not r['fail']]
    stroki = [r for r in stroki if r['fail']]
    with open(os.path.join(vyhod, 'pustye.tsv'), 'w', encoding='utf-8') as fh:
        fh.write('дата\tuuid\tсообщений (все пустые)\n')
        for r in pustye:
            fh.write(f'{r["data"]}\t{r["uuid"]}\t{r["vsego"]}\n')
    with open(os.path.join(vyhod, 'index.tsv'), 'w', encoding='utf-8') as fh:
        fh.write('дата\tназвание\tсообщений\tнепустых\tветвей\tфайлов\tфайл\n')
        for r in stroki:
            fh.write(f'{r["data"]}\t{r["nazv"]}\t{r["vsego"]}\t{r["nepust"]}\t{r["vetvej"]}\t{r["failov"]}\t{r["fail"]}\n')
    with open(os.path.join(vyhod, 'index.md'), 'w', encoding='utf-8') as fh:
        fh.write('# Разговоры по дате\n\nСтолбцы: дата · название · непустых сообщений из всех · других ветвей · собранных файлов\n')
        mes = None
        for r in stroki:
            if r['data'][:7] != mes:
                mes = r['data'][:7]; fh.write(f'\n## {mes}\n\n')
            fh.write(f'- {r["data"]} [{r["nazv"] or "(без названия)"}]({r["fail"]}) · {r["nepust"]}/{r["vsego"]}'
                     + (f' · ветвей {r["vetvej"]}' if r['vetvej'] else '')
                     + (f' · файлов {r["failov"]}' if r['failov'] else '') + '\n')
    npam = pamyat(mem, vyhod) if mem else 0
    vsego = sum(r['vsego'] for r in stroki); nep = sum(r['nepust'] for r in stroki)
    with open(os.path.join(vyhod, 'README.md'), 'w', encoding='utf-8') as fh:
        fh.write(f"""# Экспорт Claude.ai в читаемом виде

Сделано `proekty/json-export/razvernut.py` (репозиторий diarai).

- `index.md` — разговоры с содержимым по месяцам ({len(stroki)}); `index.tsv` — то же таблицей.
- `pustye.tsv` — записи без названия и без единого непустого сообщения ({len(pustye)}): в экспорте от них остались только даты и uuid.
- `razgovory/ГГГГ-ММ/*.md` — по файлу на разговор. Реплики — заголовки `##`; размышления, результаты
  инструментов и вложения свёрнуты в `<details>`; длинные результаты обрезаны (видно, сколько знаков было).
- `razgovory/ГГГГ-ММ/*.faily/` — последние версии файлов и артефактов, восстановленные из вызовов
  `create_file`, `Write`, `artifacts`, `str_replace`, `Edit` в главной ветви. Файлы, которые человек
  прикладывал, в экспорт не вошли — есть только их имена.
- `pamyat/` — память: общий текст (`00-obshchaya-pamyat.md`) и {npam} файлов памяти по их путям.

Время — UTC. Ветвление (правки, перегенерации): главная ветвь — та, где больше непустых сообщений;
остальные в конце файла, в разделе «Другие ветви».
""")
    print(f'разговоров с содержимым {len(stroki)}, пустых записей {len(pustye)} (см. pustye.tsv); '
          f'сообщений в разговорах с содержимым {vsego}, непустых {nep}; файлов памяти {npam}')


if __name__ == '__main__':
    main()
