"""tractatus_razbor.py — разобрать TeX «Трактата» (Gutenberg 5740, немецкий + Огден) в JSON {номер: {"E":…, "G":…}}.
Запуск: python3 -I tractatus_razbor.py ext/tractatus/5740-t.tex ext/tractatus/tlp.json"""
import sys, re, json

tex = open(sys.argv[1], encoding="utf-8").read()
out = {}
# \PropositionE{5.64}\n{текст}  — текст в фигурных скобках, могут быть вложенные
for m in re.finditer(r"\\Proposition([EG])\{([0-9.]+)\}\s*\{", tex):
    lang, num = m.group(1), m.group(2)
    i, depth = m.end(), 1
    while depth and i < len(tex):
        c = tex[i]
        if c == "{": depth += 1
        elif c == "}": depth -= 1
        i += 1
    body = tex[m.end():i - 1]
    body = body.replace("\\-", "").replace("``", "\u201c").replace("''", "\u201d").replace("---", "\u2014")
    body = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", body)
    body = re.sub(r"[{}]", "", body)
    body = re.sub(r"\s+", " ", body).strip()
    out.setdefault(num, {})[lang] = body
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(out), "номеров;", sum(1 for v in out.values() if "E" in v and "G" in v), "с обоими языками")
for k in ("1", "5.6", "5.64", "7", "6.54", "4.0031"):
    print(k, "|", out.get(k, {}).get("E", "—")[:120])
