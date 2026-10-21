"""eldamo_statya.py слово [язык] — напечатать статью Eldamo целиком: открывающий тег <word … v="слово"…>,
заметки (notes, HTML снят) и ссылки ref (форма, источник, gloss). Язык по умолчанию q.
2026-10-18, пробуждение 16:40 (перевод положений «Трактата» на квенья)."""
import re, sys, os, html

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
text = open(os.path.join(root, "inbox", "eldamo", "src", "data", "eldamo-data.xml"), encoding="utf-8").read()
LIMIT = 1500
if "--polno" in sys.argv:   # --polno: заметки целиком (грамматические статьи длинные)
    sys.argv.remove("--polno"); LIMIT = None
v = sys.argv[1]
# Язык: если не указан — сначала q, а если в q нет — mq, nq, eq (19.10, 09:07: mauya- есть только в ᴹQ,
# и без языка я получил «нет статьи» — чуть не третий ложный «нет» за сутки).
# 20.10, 22:31: «p,mp» раньше считалось одним языком «p,mp», и выходило «нет статьи» при «НО ЕСТЬ в … mp, p».
langs = [x.strip() for x in sys.argv[2].split(",") if x.strip()] if len(sys.argv) > 2 else ["q", "mq", "nq", "eq"]
found = False
# 19.10, 21:56: раньше после первого найденного языка поиск обрывался, и ᴺQ valda- «to matter»,
# ᴱQ valda «worth» за q valda «excited, wild» были не видны — ложное «нет». Теперь в конце
# печатается список одноимённых статей во всех квенийских языках.
ALL = {"q", "mq", "nq", "eq"}
others = {}
shown = set()
# 20.10, 00:58: список «ЕЩЁ» печатался в конце, и мой же `| head -6` его отрезал (láma: позднее q не увидел).
# Теперь первая строка вывода — все квенийские языки, где есть статья с этим именем.
_seen = []
_names = []
for _m in re.finditer(r'<word\b([^>]*)>', text):
    _a = dict(re.findall(r'([\w-]+)="([^"]*)"', _m.group(1)))
    _v = _a.get("v", "").rstrip("¹²³⁴⁵⁶⁷⁸⁹")
    _q = v.rstrip("¹²³⁴⁵⁶⁷⁸⁹")  # 20.10: запрос с надстрочной цифрой (orta-²) давал «ЕСТЬ В: —»
    if (_a.get("l") in ALL or _a.get("l") in langs) and _q in {_v, _v.rstrip("-"), re.sub(r"\(([^)]*)\)", r"\1", _v), re.sub(r"\([^)]*\)", "", _v)}:
        # 21.10: и в явно спрошенных языках (s, p…), иначе «статей: 0» при найденной статье
        if _a.get("l") in ALL:
            _seen.append(_a.get("l"))
        # если в запросе есть номер омонима (alla²), считаем только его (проверка 21.10)
        if v == _q or _a.get("v", "") == v:
            _names.append("%s %s" % (_a.get("l"), _a.get("v", "")))
# 21.10, 00:51: `| head -5` отрезал вторую статью (mq yú adv «too» после mq yú- «both»), и вышла ложная тревога.
# Теперь первая строка называет все одноимённые статьи — её не срежет никакой head.
print("ЕСТЬ В:", ", ".join(sorted(set(_seen), key=["q", "mq", "nq", "eq"].index)) or "—", "| спрошено:", ",".join(langs),
      "| статей: %d%s" % (len(_names), (" (" + "; ".join(_names) + ")") if 1 < len(_names) <= 12 else
                          (" в спрошенных и квенийских языках; другие — в конце вывода" if not _names else "")))
for lang in langs:
    for m in re.finditer(r'<word\b([^>]*)>', text, re.S):
        a = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
        # омонимы с надстрочным номером (-sta¹, -eg¹) печатаются все, если номер не указан; 2026-10-19 — два ложных «нет» из-за этого
        av = a.get("v", "")
        # и необязательные буквы в скобках: ilvan(y)a находится и по ilvanya, и по ilvana (19.10; 524 таких заголовка)
        base = av.rstrip("¹²³⁴⁵⁶⁷⁸⁹")
        forms = {av, base, re.sub(r"\(([^)]*)\)", r"\1", base), re.sub(r"\([^)]*\)", "", base)}
        # и глагол с дефисом: valda находит valda- (19.10, 21:56: valda- «to matter» не нашёлся)
        forms |= {f.rstrip("-") for f in forms}
        if v not in forms:
            continue
        if a.get("l") != lang:
            if a.get("l") in ALL and (a.get("l"), av) not in others:
                others[(a.get("l"), av)] = (a.get("gloss", "") + " " + a.get("ngloss", "")).strip()
            continue
        found = True
        shown.add(a.get("l"))
        # конец статьи: следующий <word на том же или меньшем отступе.
        # Было «до 6000 знаков»: у грамматических статей (speech="grammar": genitive, elision…) заметки длиннее,
        # закрывающий ]]></notes> не попадал в окно, и статья печаталась пустой (19.10, 09:07, «elision»).
        nxt = re.compile(r'\n {0,6}<word\b').search(text, m.end())
        body = text[m.end(): nxt.start() if nxt else len(text)]
        print("==", a.get("l"), a.get("v"), "|", a.get("speech", ""), "|", a.get("gloss", ""), a.get("ngloss", ""))
        # 20.10, 21:07: атрибут created (кто составил неологизм) раньше не печатался, и я написал
        # про atsinta- «Eldamo не говорит, кто составил», а там created="Helge Fauskanger, NQNT".
        if a.get("created") or a.get("neo-version"):
            print("СОСТАВИЛ:", a.get("created", "—"), "| neo-version:", a.get("neo-version", "—"))
        for n in re.findall(r"<notes><!\[CDATA\[(.*?)\]\]></notes>", body, re.S):
            s = html.unescape(re.sub(r"<[^>]+>", "", n)).strip()
            # 20.10: раньше обрезалось молча; теперь пишется, что обрезано (как в tlp.py)
            cut = LIMIT is not None and len(s) > LIMIT
            print("ЗАМЕТКИ:", s[:LIMIT] + (" […обрезано: %d из %d знаков; целиком — --polno]" % (LIMIT, len(s)) if cut else ""))
        # 20.10: элементы слова (<element> прямо в статье) и корни (<deriv> в ссылках) раньше не печатались.
        # Из-за этого я назвал «догадкой» засвидетельствованное ruc- + -ima в rúcima. Теперь печатаются.
        els = [dict(re.findall(r'([\w-]+)="([^"]*)"', e)) for e in re.findall(r'<element\b([^>]*)/?>', body)]
        if els:
            print("ЭЛЕМЕНТЫ:", ", ".join("%s %s" % (e.get("l", ""), e.get("v", "")) for e in els))
        ders = sorted({(d.get("v", ""), d.get("source", "")) for d in
                       [dict(re.findall(r'([\w-]+)="([^"]*)"', x)) for x in re.findall(r'<deriv\b([^>]*)/?>', body)]})
        if ders:
            print("ПРОИСХОЖДЕНИЕ (deriv):", "; ".join("%s (%s)" % d for d in ders))
        for r in re.findall(r'<ref\b([^>]*)>', body):
            ra = dict(re.findall(r'([\w-]+)="([^"]*)"', r))
            print("  ref:", ra.get("v"), "|", ra.get("source"), "|", ra.get("gloss", ""))
        # <deprecated> — по eldamo-schema.xsd: «a word is out-of-date, optionally with a link to a word that might be better».
        # То есть <deprecated v="X"/> внутри статьи W значит: W устарело, лучше X (мнение Стрэка).
        # 20.10, 00:33: и я, и проверяющий субагент прочли тег в статье panyalë наоборот (будто устарело tëalë).
        # Берём только теги этой статьи, до первой вложенной <word.
        own = re.split(r'<word\b', body, 1)[0]
        dep = re.findall(r'<deprecated\b([^>]*)/?>', own)
        if dep:
            better = [dict(re.findall(r'([\w-]+)="([^"]*)"', d)) for d in dep]
            print("  УСТАРЕЛО (по Eldamo); лучше:", ", ".join("%s %s" % (b.get("l", "?"), b.get("v", "—")) for b in better))
        # обратная ссылка: какие статьи устарели в пользу этой (вложенные <word> ищем по ближайшему открывающему тегу)
        for d in re.finditer(r'<deprecated\b[^>]*\bl="%s"[^>]*\bv="%s"' % (re.escape(a.get("l", "")), re.escape(av)), text):
            w = text.rfind("<word", 0, d.start())
            wa = dict(re.findall(r'([\w-]+)="([^"]*)"', text[w:text.find(">", w)]))
            print("  ВМЕСТО устаревшего:", wa.get("l"), wa.get("v"), "|", wa.get("gloss", ""))
    if found:
        break
others = {k: g for k, g in others.items() if k[0] not in shown}
if others:
    print("ЕЩЁ (одноимённые статьи в других языках; полностью — с языком вторым аргументом):")
    for (l, w), g in others.items():
        print("  ", l, w, "|", g)
if not found:
    print("— нет статьи %r в языках %s (омонимы с ¹²³ проверены; склонённых форм здесь нет)" % (v, ",".join(langs)))
    # 20.10, 21:07: проверяющий спросил корни SAN, STAN, TEL без языка и получил «нет статьи», а они есть
    # в p/mp. Теперь при пустом поиске печатаются ВСЕ языки, где статья с таким именем есть.
    _any = set()
    for _m in re.finditer(r'<word\b([^>]*)>', text):
        _a = dict(re.findall(r'([\w-]+)="([^"]*)"', _m.group(1)))
        _b = _a.get("v", "").rstrip("¹²³⁴⁵⁶⁷⁸⁹")
        if v.rstrip("¹²³⁴⁵⁶⁷⁸⁹") in {_b, _b.rstrip("-")}:
            _any.add(_a.get("l"))
    if _any:
        print("  НО ЕСТЬ в других языках:", ", ".join(sorted(_any)), "— спроси вторым аргументом (корни: p, mp, ep)")
    else:
        print("  и ни в одном другом языке Eldamo с точно таким именем тоже нет")
