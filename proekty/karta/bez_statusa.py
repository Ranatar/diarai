"""bez_statusa.py [префикс] — файлы со статусом «упомянут, статус не поставлен» и строки моих текстов, где они названы
вместе со словами о чтении («прочит», «прочёл», «читал», «смотрел», «открыл»). Помогает проставить ручной статус в status.tsv."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
pref = sys.argv[1] if len(sys.argv) > 1 else ""
texts = []
for d in ("diary", "notes", "proekty"):
    for dp, dn, fn in os.walk(os.path.join(ROOT, d)):
        for f in fn:
            if f.endswith(".md") and "karta" not in dp:
                p = os.path.join(dp, f)
                for line in open(p, encoding="utf-8", errors="replace"):
                    texts.append((os.path.relpath(p, ROOT), line))
RX = re.compile(r"прочит|прочёл|прочла|читал|смотрел|открыл|разобран", re.I)
for line in open(os.path.join(HERE, "upominaniya.tsv"), encoding="utf-8"):
    f = line.split("\t")
    if f[0].startswith("#") or not f[0].startswith(pref) or f[2] != "упомянут, статус не поставлен":
        continue
    stem = os.path.splitext(os.path.basename(f[0]))[0]
    hits = [(p, l.strip()) for p, l in texts if stem in l and RX.search(l)]
    # 20.10: «[0]» я прочёл как «не упомянут», а это только «нет строк со словами о чтении».
    # Так я перечитал три файла, уже прочитанных, и повторил свою же «Присказку № 20». Теперь печатается и всё упоминание.
    allm = [(p, l.strip()) for p, l in texts if stem in l]
    print("%s  [строк со словами о чтении: %d; всего упоминаний: %d]" % (f[0], len(hits), len(allm)))
    if not hits and allm:
        p, l = allm[0]
        i = l.find(stem)
        print("     УПОМИНАЛСЯ: %s: …%s…" % (p, l[max(0, i - 60):i + 160]))
    for p, l in hits[:2]:
        i = l.find(stem)
        print("     %s: …%s…" % (p, l[max(0, i - 60):i + 120]))
