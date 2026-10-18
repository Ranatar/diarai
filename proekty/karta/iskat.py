"""iskat.py слово1 слово2 ... — в каких моих .md (diary, notes, proekty) встречается каждое слово (без учёта регистра).
Замена циклу for в оболочке, который здесь запрещён."""
import os, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
texts = {}
for d in ("diary", "notes", "proekty"):
    for dp, dn, fn in os.walk(os.path.join(ROOT, d)):
        for f in fn:
            if f.endswith(".md"):
                p = os.path.join(dp, f)
                texts[os.path.relpath(p, ROOT)] = open(p, encoding="utf-8", errors="replace").read().lower()
for w in sys.argv[1:]:
    hits = sorted(k for k, t in texts.items() if w.lower() in t)
    print("%s (%d): %s" % (w, len(hits), " ".join(hits[:8])))
