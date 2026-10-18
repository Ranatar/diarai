"""Слова, набранные вперемешку кириллицей и латиницей (Mелькор, Меyer): они ломают поиск.

python3 -I smesh.py папка [папка…] > отчёт.md
Смотрит .md .txt .html .json до 5 МБ; из html выбрасывает script/style и теги.
Не считает смешанными слова с цифрами и подчёркиванием (идентификаторы кода).
"""
import html, os, re, sys

MIX = re.compile(r"\b(?=[^\W\d_]*[а-яёА-ЯЁ])(?=[^\W\d_]*[a-zA-Z])[^\W\d_]+\b")
total = 0
for root in sys.argv[1:]:
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ("node_modules", ".git", "build", "dist")]
        for f in sorted(fn):
            if not f.lower().endswith((".md", ".txt", ".html", ".json")):
                continue
            p = os.path.join(dp, f)
            if os.path.getsize(p) > 5_000_000:
                continue
            try:
                t = open(p, encoding="utf-8").read()
            except UnicodeDecodeError:
                continue
            if f.lower().endswith(".html"):
                t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S | re.I)
                t = html.unescape(re.sub(r"<[^>]+>", " ", t))
            t = t.replace("\\n", " ").replace("\\t", " ")  # экранированные переводы строк в JSON
            words = sorted(set(MIX.findall(t)))
            # дореформенное «і», набранное латинской i, — отдельная категория
            only_i = [w for w in words if set(re.findall(r"[a-zA-Z]", w)) <= {"i", "I"}]
            words = [w for w in words if w not in only_i]
            if words:
                total += len(words)
                print(f"- `{os.path.relpath(p, root)}`: " + ", ".join(words[:40]) + (" …" if len(words) > 40 else ""))
            if only_i:
                print(f"  - (латинская i вместо «і»: {len(only_i)} слов, напр. {', '.join(only_i[:5])})")
print(f"\nвсего разных смешанных слов (без «і»): {total}")
