"""Каталог html-страниц папки: заголовок, слов текста, строк скрипта, canvas/three.js.

python3 -I katalog_html.py папка > каталог.md
"""
import html, os, re, sys

src = sys.argv[1]
rows = []
for f in sorted(os.listdir(src)):
    if not f.lower().endswith(".html"):
        continue
    t = open(os.path.join(src, f), encoding="utf-8", errors="ignore").read()
    m = re.search(r"<title>(.*?)</title>", t, re.S | re.I)
    title = re.sub(r"\s+", " ", html.unescape(m.group(1))).strip() if m else ""
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", t, re.S | re.I)
    js_lines = sum(s.count("\n") for s in scripts)
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S | re.I)
    words = len(html.unescape(re.sub(r"<[^>]+>", " ", body)).split())
    tags = []
    if "<canvas" in t or "getContext(" in t:
        tags.append("canvas")
    if "THREE." in t or "three.min.js" in t or "three.module" in t:
        tags.append("3d")
    if "AudioContext" in t:
        tags.append("звук")
    kind = "текст" if words > 1500 and js_lines < 300 else ("игра/визуализация" if js_lines >= 300 else "")
    rows.append((f, title, words, js_lines, ",".join(tags), kind))

print("| файл | заголовок | слов | строк JS | что внутри | |")
print("|---|---|---|---|---|---|")
for r in rows:
    print("| `%s` | %s | %d | %d | %s | %s |" % (r[0], r[1].replace("|", "/")[:70], r[2], r[3], r[4], r[5]))
print(f"\nвсего {len(rows)} страниц; текстовых (>1500 слов, <300 строк JS): {sum(1 for r in rows if r[5]=='текст')}")
