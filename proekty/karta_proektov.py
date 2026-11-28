"""karta_proektov.py — порождает proekty/README.md: карту моих проектов.
По каждой папке proekty/: заголовок и первая содержательная строка её README.md (если есть), число файлов в git,
даты первого и последнего коммита (git log). Ручной слой — словарь SOSTOYANIE ниже: одно слово о состоянии
(«идёт», «пауза», «закончено», «служебное»); где не проставлено — «?».
28.11, пробуждение 05:47. Автор: «И карта сделанных проектов вроде тоже есть?» Не было: были карта inbox
(proekty/karta/) и раздел в CLAUDE.md, где перечислено только начатое."""
import os, re, subprocess

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
P = os.path.join(ROOT, "proekty")

SOSTOYANIE = {
    "faust-kvenya": "идёт", "tractatus-quenya": "идёт", "tlpt-qu": "идёт", "hokku": "идёт", "blanki": "идёт",
    "elfijskoe": "идёт", "stranicy-avtora": "идёт", "rody-oshibok": "идёт", "karta": "идёт",
    "instrumenty": "служебное", "json-export": "служебное (приватно)",
}


def git(*a):
    return subprocess.run(["git", "-C", ROOT] + list(a), capture_output=True, text=True).stdout.strip()


def readme(d):
    for name in ("README.md", "readme.md"):
        f = os.path.join(P, d, name)
        if os.path.isfile(f):
            zag, pervaya = "", ""
            for line in open(f, encoding="utf-8"):
                s = line.strip()
                if not s:
                    continue
                if s.startswith("#") and not zag:
                    zag = s.lstrip("# ").strip()
                elif not s.startswith("#") and not pervaya:
                    pervaya = re.sub(r"\s+", " ", s)
                if zag and pervaya:
                    break
            return zag, pervaya
    return "", ""


def main():
    rows = []
    for d in sorted(os.listdir(P)):
        if not os.path.isdir(os.path.join(P, d)) or d.startswith((".", "__")):
            continue
        files = [x for x in git("ls-files", "proekty/" + d).split("\n") if x]
        dates = git("log", "--format=%ad", "--date=short", "--", "proekty/" + d).split("\n")
        dates = [x for x in dates if x]
        zag, perv = readme(d)
        if len(perv) > 160:
            perv = perv[:157] + "…"
        rows.append((d, SOSTOYANIE.get(d, "?"), len(files), dates[-1] if dates else "—", dates[0] if dates else "—",
                     zag or "(нет README)", perv))
    out = ["# Карта проектов", "",
           "Порождается `python3 -I proekty/karta_proektov.py` (не править руками; состояние — словарь SOSTOYANIE в скрипте).",
           "Начатое и что делать дальше — мой раздел в CLAUDE.md; здесь — всё, что есть в `proekty/`, с датами из git.", "",
           "| папка | состояние | файлов | начато | последнее | README: заголовок — первая строка |", "|---|---|---|---|---|---|"]
    for d, st, n, d0, d1, zag, perv in rows:
        out.append("| `%s` | %s | %d | %s | %s | **%s** — %s |" % (d, st, n, d0, d1, zag.replace("|", "/"),
                                                                     perv.replace("|", "/")))
    open(os.path.join(P, "README.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("проектов: %d; без README: %d" % (len(rows), sum(1 for r in rows if r[5] == "(нет README)")))


main()
