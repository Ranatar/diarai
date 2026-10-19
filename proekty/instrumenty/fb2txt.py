"""fb2txt.py in.fb2 out.txt — FictionBook 2 → простой текст: заголовки секций как «## …», абзацы через пустую строку,
бинарные вложения (картинки) отброшены. Только стандартная библиотека. 2026-10-19 (роман из inbox, для чтения)."""
import re, sys, html
raw = open(sys.argv[1], "rb").read()
m = re.search(rb'encoding="([^"]+)"', raw[:200])
t = raw.decode(m.group(1).decode() if m else "utf-8", errors="replace")
t = re.sub(r"<binary\b.*?</binary>", "", t, flags=re.S)
t = re.sub(r"<title>(.*?)</title>", lambda mm: "\n## " + re.sub(r"<[^>]+>", " ", mm.group(1)).strip() + "\n", t, flags=re.S)
t = re.sub(r"</p>|<empty-line\s*/>", "\n\n", t)
t = re.sub(r"<[^>]+>", "", t)
t = html.unescape(t)
t = re.sub(r"[ \t]+", " ", t)
t = re.sub(r"\n\s*\n\s*\n+", "\n\n", t)
open(sys.argv[2], "w", encoding="utf-8").write(t.strip() + "\n")
print(len(t.split()), "слов")
