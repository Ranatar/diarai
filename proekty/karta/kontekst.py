"""kontekst.py слово [слово…] — строки моих .md (diary, notes), где встречается слово; по 160 знаков вокруг."""
import os, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for d in ("diary", "notes", "proekty"):
    for dp, dn, fn in os.walk(os.path.join(ROOT, d)):
        for f in sorted(fn):
            if not f.endswith(".md") or "karta" in dp:
                continue
            p = os.path.join(dp, f)
            for line in open(p, encoding="utf-8", errors="replace"):
                low = line.lower()
                for w in sys.argv[1:]:
                    i = low.find(w.lower())
                    if i >= 0:
                        print("%s: …%s…" % (os.path.relpath(p, ROOT), line[max(0, i - 80):i + 80].strip()))
                        break
