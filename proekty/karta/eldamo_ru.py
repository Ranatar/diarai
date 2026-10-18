"""eldamo_ru.py — насколько заполнена русская база перевода Eldamo (inbox/eldamo/src/data/eldamo-data-ru.xml):
по таблицам (gloss, title, phrase, label) — сколько строк переведено и сколько пустых; число сегментов заметок и overrides.
Формат описан в inbox/eldamo/L10N-ru.md."""
import re, collections
t = open("/home/diarai/diarai/inbox/eldamo/src/data/eldamo-data-ru.xml", encoding="utf-8").read()
head = re.search(r"<l10n[^>]*>", t)
print(head.group(0) if head else "?")
for m in re.finditer(r'<table name="(\w+)">(.*?)</table>', t, re.S):
    body = m.group(2)
    full = len(re.findall(r"<e\b[^>]*[^/]>[^<]+</e>", body))
    empty = len(re.findall(r"<e\b[^>]*/>", body))
    print("таблица %-7s переведено %6d, пусто %6d  (%.0f%%)" % (m.group(1), full, empty, 100 * full / max(1, full + empty)))
ov = len(re.findall(r"<gloss\b[^>]*page-id", t))
print("overrides:", ov)
nm = re.search(r"<notes>(.*?)</notes>", t, re.S)
if nm:
    segs = re.findall(r"<seg\b([^>]*)>(.*?)</seg>|<seg\b([^>]*)/>", nm.group(1), re.S)
    tags = collections.Counter(re.findall(r"<(\w+)\b", nm.group(1)))
    print("в разделе notes теги:", tags.most_common(6))
# пример: «king»
for w in ("king", "world", "silence", "oath"):
    mm = re.search(r'<e en="%s"[^>]*>([^<]*)</e>' % w, t)
    print(w, "→", mm.group(1) if mm else "—")
