"""js_strings.py файл.html|.js — русские строковые литералы из кода (≥12 знаков, теги сняты, без повторов).
Чтобы прочесть текст интерактивных страниц, где слова живут в JS, а не в HTML (html2txt их не видит).
Жил в ext/tmp, перенесён 2026-10-18 (пробуждение 19:01) по замечанию автора: своё — в proekty."""
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
seen = set()
for m in re.finditer(r"""(['"`])((?:(?!\1).){12,}?)\1""", t, re.S):
    s = m.group(2)
    if re.search(r"[а-яА-ЯёЁ]{3,}", s) and s not in seen:
        seen.add(s)
        print(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip())
