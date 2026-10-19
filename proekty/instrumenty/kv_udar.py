"""kv_udar.py — ударение в квенья и проверка метра строк.

  python3 -I kv_udar.py --test                 — прогон на примерах Толкина (Прил. E) и курса (§2.1.3.2)
  python3 -I kv_udar.py слово [слово …]        — разбивка на слоги, тяжесть, ударный слог
  python3 -I kv_udar.py --stih файл [--metr x/] [--ot N --do M]  — каждую строку: схема ударений и сбои метра

Правило (курс §2.1.3.1, из Прил. E): односложное — ударно (служебные могут терять ударение); двусложное — на
первый; длиннее — на предпоследний, если он тяжёлый (долгий гласный, дифтонг ai oi ui iu eu au, или за гласным
два согласных и больше), иначе на третий от конца. Суффиксы — часть слова.
Допущения, мной не проверенные по первоисточнику (помечаю «по памяти»): qu и x считаются за два согласных
(kw, ks); hy/hl/hr/hw/ny/ty/ly/ry/nw в середине слова — за два; þ, ñ, ç — один согласный.
Апостроф (элизия: vanw’ Elenwe, or’mardi) — слово остаётся отдельным, усечённым.
Метр: «-» сильное место, «u» слабое; по умолчанию хорей «-u» (--metr u- — ямб). В выводе: - ударный, u безударный.
Односложные слова считаются «гибкими» (могут стоять и в сильном, и в слабом месте) — обычная условность.
2026-10-19 (перевод «Ворона» По на квенья Luinyelle, Elvish Composition Archive)."""
import re, sys, unicodedata

VOW = "aeiouáéíóúëäöüâêîôûy"  # y — согласный, исключаем ниже
LONG = set("áéíóúâêîôû")
DIPH = ("ai", "oi", "ui", "iu", "eu", "au")

def norm(w):
    w = unicodedata.normalize("NFC", w.lower())
    w = w.replace("’", "'").replace("‘", "'").strip("'\".,;:!?()[]–—-«»“”")
    return w

def units(w):
    """Разбить слово на гласные ядра и согласные с весом: список ('V', текст, долгое?) / ('C', текст, число)."""
    w = norm(w).replace("'", "")
    out, i = [], 0
    while i < len(w):
        ch = w[i]
        if ch in VOW and ch != "y":
            two = w[i:i + 2]
            # дифтонг, только если второй гласный — краткий i/u (не í, не ú)
            if two in DIPH:
                out.append(("V", two, True)); i += 2; continue
            out.append(("V", ch, ch in LONG)); i += 1; continue
        if w.startswith("qu", i):
            out.append(("C", "qu", 2)); i += 2; continue
        if ch == "x":
            out.append(("C", "x", 2)); i += 1; continue
        if ch.isalpha() or ch in "þñç":
            out.append(("C", ch, 1)); i += 1; continue
        i += 1
    return out

def syllables(w):
    """[(ядро, тяжёлый?)] — ядро с последующими согласными до следующего ядра."""
    u = units(w)
    res = []
    for k, (t, s, x) in enumerate(u):
        if t != "V":
            continue
        cons = 0
        for t2, s2, n2 in u[k + 1:]:
            if t2 == "V":
                break
            cons += n2
        # конечные согласные слова тяжести не дают (в правиле важен только предпоследний)
        res.append([s, x or cons >= 2, cons])
    return res

def stress(w):
    """Индекс ударного слога (0-based) или None для слов без гласных."""
    s = syllables(w)
    n = len(s)
    if n == 0:
        return None, s
    if n == 1:
        return 0, s
    if n == 2:
        return 0, s
    return (n - 2 if s[n - 2][1] else n - 3), s

def show(w):
    i, s = stress(w)
    parts = [(x[0].upper() if k == i else x[0]) + ("·тяж" if x[1] else "") for k, x in enumerate(s)]
    return "%s: %s" % (w, " . ".join(parts))

TESTS = [  # слово, номер ударного слога с 1 — из Прил. E (через курс §2.1.3.3) и примеров §2.1.3.2
    ("isildur", 2), ("oromë", 1), ("eressëa", 2), ("ancalima", 2), ("elentári", 3), ("andúnë", 2),
    ("aiwë", 1), ("aiwëo", 1), ("ambo", 1), ("ambonna", 2), ("tíra", 1), ("tíranyë", 2), ("tíranyes", 2),
    ("telumë", 1), ("telumerya", 3), ("telumeryallo", 4), ("tië", 1), ("taurë", 1), ("tirmo", 1),
]

def line_scheme(line):
    """Для строки: список (слово, число слогов, ударный индекс). Пропускает пустые."""
    res = []
    for tok in re.split(r"[\s\-–—]+", line):
        w = norm(tok)
        if not w or not re.search(r"[a-zá-úëþñ]", w):
            continue
        i, s = stress(w)
        if not s:
            continue
        res.append((tok, len(s), i))
    return res

def check(line, metr="-u"):
    sch = line_scheme(line)
    pos, marks, bad = 0, [], []
    for tok, n, i in sch:
        for k in range(n):
            strong = metr[(pos + k) % len(metr)] == "-"
            if n == 1:
                marks.append("?")
            elif k == i:
                marks.append("-")
                if not strong:
                    bad.append(tok)
            else:
                marks.append("u")
        pos += n
    return pos, "".join(marks), bad

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(1)
    if a[0] == "--test":
        ok = 0
        for w, want in TESTS:
            i, s = stress(w)
            got = i + 1
            ok += got == want
            print(("OK  " if got == want else "СБОЙ") + "  " + show(w) + ("" if got == want else "   (ждали %d)" % want))
        print("%d из %d" % (ok, len(TESTS)))
    elif a[0] == "--stih":
        metr = "-u"
        if "--metr" in a:
            metr = a[a.index("--metr") + 1]
        lines = open(a[1], encoding="utf-8").read().splitlines()
        lo = int(a[a.index("--ot") + 1]) if "--ot" in a else 1
        hi = int(a[a.index("--do") + 1]) if "--do" in a else len(lines)
        for no in range(lo, hi + 1):
            L = lines[no - 1]
            if not L.strip():
                continue
            n, m, bad = check(L, metr)
            print("%4d %2d %-24s %s%s" % (no, n, m, L.strip()[:70], ("   СБОЙ: " + ", ".join(bad)) if bad else ""))
    else:
        for w in a:
            print(show(w))
