"""namarie_slogi.py — сверка SYL/LONG из inbox/immollimma/requests/namarie/piece.py со слогами и ударениями
«Намариэ» по proekty/instrumenty/kv_udar.py (дифтонги ai, oi, ui, au, eu, iu — один слог: Eldamo «q diphthongs»,
LotR/1116; ударение — по правилу квенья: двусложные — на первый, иначе на предпоследний, если он тяжёлый, иначе на
третий от конца).
В piece.py: «Каждая из 17 строк — два такта; ритм голосов построен по числу слогов строки и долгому ударному
слогу (SYL, LONG), так что текст подкладывается под ноты слог в слог». LONG — 0-based (rhythm(): i == long_i).
Строки — 17, как в LotR (текст в ext/tmp/namarie17.txt; Eldamo делит их на 16 фраз по-другому).
Запуск: python3 -I proekty/stranicy-avtora/namarie_slogi.py ext/tmp/namarie17.txt
2026-11-27, пробуждение 20:32."""
import ast, os, re, sys

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, os.path.join(root, "proekty", "instrumenty"))
import kv_udar  # noqa: E402

src = open(os.path.join(root, "inbox", "immollimma", "requests", "namarie", "piece.py"), encoding="utf-8").read()
SYL = ast.literal_eval(re.search(r"^SYL = (\[.*?\])", src, re.M).group(1))
LONG = ast.literal_eval(re.search(r"^LONG = (\[.*?\])", src, re.M).group(1))
lines = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
assert len(lines) == len(SYL) == len(LONG) == 17, (len(lines), len(SYL), len(LONG))

ne_syl = ne_long = 0
for i, l in enumerate(lines):
    slogi, udar = [], set()
    for w, n, s in kv_udar.line_scheme(l):
        if s is not None and n > 1:
            udar.add(len(slogi) + s)
        slogi += ["%s:%s" % (kv_udar.norm(w), x[0]) for x in kv_udar.syllables(kv_udar.norm(w))]
    n = len(slogi)
    ok_syl = n == SYL[i]
    if not ok_syl:
        ne_syl += 1
    # LONG сравниваю только там, где число слогов совпало (иначе индексы сдвинуты)
    ok_long = (LONG[i] in udar) if ok_syl else None
    if ok_long is False:
        ne_long += 1
    print("%2d  слогов: моё %2d, piece %2d %s | LONG=%d → «%s» %s | ударные: %s | %s" % (
        i + 1, n, SYL[i], "  " if ok_syl else "≠", LONG[i],
        slogi[LONG[i]] if LONG[i] < n else "?",
        {True: "ударный", False: "БЕЗУДАРНЫЙ", None: "(не сверял)"}[ok_long],
        ",".join(str(x) for x in sorted(udar)), l))
print("строк: %d; не совпало число слогов: %d; LONG на безударном (из строк с совпавшим числом): %d" % (
    len(lines), ne_syl, ne_long))
