"""novoe.py [ГГГГ-ММ-ДД] — что в inbox/ (и в корне репозитория) новое или изменённое с даты и что о нём знает карта.

Без даты берётся дата предпоследнего файла дневника, то есть прошлого пробуждения. Если между пробуждениями был долгий
сон, дату лучше дать явно (например, 2026-10-28 для месячного сна 27.10–27.11).
Статусы — из upominaniya.tsv (порождается karta.py; перед запуском karta.py стоит перестроить).
Печатает: по единицам (папка в inbox или файл) — сколько новых и сколько из них «не упомянут» или «статус не поставлен»;
затем сами такие файлы, кроме картинок, шрифтов и прочих ассетов (их только счётом).
28.11, пробуждение 05:47. Автор: «У тебя же есть карта изменений файлов? И карта непрочитанных файлов есть». Карты были,
а обход нового после сна я делал по памяти и пропустил 73 страницы в html-generated."""
import collections, datetime, os, subprocess, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
INBOX = os.path.join(ROOT, "inbox")
ASSET = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".mp3", ".wav", ".mid", ".ttf", ".otf", ".woff", ".woff2",
         ".glb", ".stl", ".npy", ".pyc", ".map")
ASSET_PARTS = ("/fonts/", "/assets/", "-assets/", "/thumbs/", "/node_modules/", "/.git/", "tpm2-font-")


def data_po_umolchaniyu():
    d = sorted(f for f in os.listdir(os.path.join(ROOT, "diary")) if f[:4].isdigit())
    return d[-2][:10] if len(d) >= 2 else "2000-01-01"


def main():
    s = sys.argv[1] if len(sys.argv) > 1 else data_po_umolchaniyu()
    t0 = datetime.datetime.fromisoformat(s).timestamp()
    status = {}
    up = os.path.join(ROOT, "proekty", "karta", "upominaniya.tsv")
    for line in open(up, encoding="utf-8"):
        if line.startswith("#"):
            continue
        c = line.rstrip("\n").split("\t")
        if len(c) > 2:
            status[c[0]] = c[2]
    novye = []
    for d, _, fs in os.walk(INBOX):
        for f in fs:
            p = os.path.join(d, f)
            try:
                if os.path.getmtime(p) >= t0:
                    novye.append(os.path.relpath(p, INBOX))
            except OSError:
                pass
    po_edinice = collections.defaultdict(lambda: [0, 0, 0, 0])
    statusy = collections.defaultdict(collections.Counter)
    neizv = []
    for r in sorted(novye):
        u = r.split("/")[0]
        st = status.get(r, "нет в карте")
        nichego = st.startswith("не упомянут") or "не поставлен" in st or st == "нет в карте"
        asset = r.lower().endswith(ASSET) or any(a in "/" + r for a in ASSET_PARTS)
        po_edinice[u][0] += 1
        if nichego or st.startswith("нет") or st.startswith("бегло"):
            po_edinice[u][3] += 1  # не прочитано: без статуса, «нет» или «бегло»
        statusy[u][st.split(" (")[0][:20]] += 1
        if nichego:
            po_edinice[u][1] += 1
            if asset:
                po_edinice[u][2] += 1
            else:
                neizv.append(r)
    print("с %s: новых или изменённых файлов в inbox — %d" % (s, len(novye)))
    print("%7s %7s %7s %7s  %s" % ("новых", "без", "из них", "не про-", "единица"))
    print("%7s %7s %7s %7s" % ("", "статуса", "ассеты", "читано"))
    for u, (n, b, a, ne) in sorted(po_edinice.items(), key=lambda x: (-x[1][1], -x[1][3])):
        st = ", ".join("%s %d" % kv for kv in statusy[u].most_common())
        print("%7d %7d %7d %7d  %s  [%s]" % (n, b, a, ne, u, st))
    print("\nне упомянуты и не ассеты (%d):" % len(neizv))
    for r in neizv:
        print("  " + r)
    # корень репозитория: что автор положил туда (не моё) после даты
    try:
        out = subprocess.run(["git", "-C", ROOT, "log", "--since=" + s, "--author=Ranatar", "--diff-filter=A",
                              "--name-only", "--format="], capture_output=True, text=True).stdout.split("\n")
        moi = {"diary", "notes", "proekty", "CLAUDE.md", ".gitignore"}
        chuzh = sorted({o for o in out if o and "/" not in o and o not in moi})
        if chuzh:
            print("\nв корне репозитория добавлено (git, коммиты под именем Ranatar — проверить, не мои ли):")
            for o in chuzh:
                print("  " + o)
    except Exception as e:
        print("git:", e)


main()
