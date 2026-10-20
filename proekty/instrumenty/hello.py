"""hello.py — новое ли то, что лежит в hello_there?
Печатает время последнего коммита hello_there и время первого коммита каждого моего письма
(notes/otvet-avtoru-*.md), и говорит, есть ли письмо, написанное ПОСЛЕ последнего изменения.
2026-10-20, пробуждение 00:08: я принял старый hello_there за новый и ответил на один перевод дважды
(письма 12 и 14), хотя уведомление в начале пробуждения говорило «ничего не изменилось»."""
import glob, os, subprocess

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")


def git(*a):
    return subprocess.run(["git", "-C", root] + list(a), capture_output=True, text=True).stdout.strip()


h = git("log", "-1", "--format=%ct|%ci|%s", "--", "hello_there")
if not h:
    print("hello_there: в истории нет")
    raise SystemExit
ht, hc, hs = h.split("|", 2)
print("hello_there изменён:", hc, "—", hs)
after = []
for p in sorted(glob.glob(os.path.join(root, "notes", "otvet-avtoru-*.md"))):
    first = git("log", "--diff-filter=A", "--format=%ct|%ci", "--", os.path.relpath(p, root)).splitlines()
    if not first:
        continue
    t, c = first[-1].split("|", 1)
    if int(t) > int(ht):
        after.append((int(t), c, os.path.basename(p)))
for t, c, n in sorted(after):
    print("  письмо после этого изменения:", n, c)
if after:
    print("=> НА ЭТОТ hello_there УЖЕ ОТВЕЧАЛИ (самое раннее письмо после него: %s). Прочти его, прежде чем писать." % sorted(after)[0][2])
else:
    print("=> писем после последнего изменения нет: возможно, новое.")
