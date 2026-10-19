"""eldamo_poisk.py запрос [запрос …] [--strok 25] [--bez-neo] — живой поиск eldamo.org в браузере, выдача текстом.
Запуск: ext/venv-pw/bin/python -I proekty/instrumenty/brauzer/eldamo_poisk.py 'yaim*' 'word=lúny*'
Синтаксис запроса — сайта (см. «?» на странице): *, «,» — или, «+» — и, word= / gloss=.
По умолчанию страница открывается с ?neo (автор, 19.10: «если в адресной строке добавлять '?neo', будет больше
информации»). Сеть — через прокси песочницы (как в snimok.py). Нужен allowed_domains eldamo.org.
2026-10-19: до этого я брал Eldamo только из XML и трижды ошибся одним ключом; у сайта свой поиск по формам."""
import os, sys
from urllib.parse import urlsplit
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/home/diarai/diarai/ext/pw-browsers")
from playwright.sync_api import sync_playwright

args = sys.argv[1:]
strok = 25
if "--strok" in args:
    i = args.index("--strok"); strok = int(args[i + 1]); del args[i:i + 2]
if "--fajl" in args:   # запросы по строке из файла: Bash отклоняет «=» в командной строке
    i = args.index("--fajl"); f = args[i + 1]; del args[i:i + 2]
    args += [l.strip() for l in open(f, encoding="utf-8") if l.strip()]
neo = "--bez-neo" not in args
args = [a for a in args if a != "--bez-neo"]
url = "https://eldamo.org/content/search/search.html" + ("?neo" if neo else "")

kw = {}
px = os.environ.get("HTTPS_PROXY")
if px:
    u = urlsplit(px)
    kw["proxy"] = {"server": "%s://%s:%s" % (u.scheme, u.hostname, u.port),
                   "username": u.username or "", "password": u.password or ""}
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"], **kw)
    pg = b.new_page()
    pg.goto(url, wait_until="load", timeout=60000)
    for q in args:
        box = pg.locator("#searchBox")
        box.fill("")
        box.type(q, delay=30)
        pg.wait_for_timeout(1500)
        txt = pg.evaluate("""() => {
            const hr = document.querySelector('hr');
            let out = [], n = hr ? hr.nextElementSibling : null;
            while (n) { out.push(n.innerText); n = n.nextElementSibling; }
            return out.join('\\n');
        }""")
        lines = [l for l in txt.splitlines() if l.strip()]
        print("== %s  (%d строк)" % (q, len(lines)))
        for l in lines[:strok]:
            print("  " + l)
    b.close()
