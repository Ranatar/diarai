"""rodoslovnaya.py — даты (mtime: первая, медиана, последняя) проектов «синтеза понятий» в inbox.
mtime — слабый свидетель (копирование может сбить), поэтому печатаю и медиану, и края; служебные папки пропускаю."""
import os, time, statistics
R = "/home/diarai/diarai/inbox"
P = ["metamystic-dictionary-extended", "philosophical-concepts-omnidirectional", "Synthesises-of-concepts/synthesis-project",
     "Synthesises-of-concepts/synthesis-project-m4opus", "Synthesises-of-concepts/synthesises", "Synthesises-of-concepts/various",
     "Synthesises-of-concepts/philosophy-graph-descriptions", "Synthesises-of-concepts/heidegger-deleuze",
     "Synthesises-of-concepts/wittgenstein-hesychasm", "Synthesises-of-concepts/hegel-pythagoras",
     "philosphaira", "hwph-xml", "philosynth"]
SL = {"node_modules", ".git", "jre", "fonts", "vendor", "build", "cache", "katex", "lib"}
d = lambda t: time.strftime("%Y-%m-%d", time.localtime(t))
for p in P:
    ts = []
    for dp, dn, fn in os.walk(os.path.join(R, p)):
        dn[:] = [x for x in dn if x not in SL]
        ts += [os.path.getmtime(os.path.join(dp, f)) for f in fn]
    if ts:
        print("%-55s %4d ф.  %s … %s … %s" % (p, len(ts), d(min(ts)), d(statistics.median(ts)), d(max(ts))))
