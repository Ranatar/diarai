"""snimok.py путь|URL out.png [ширина высота пауза_мс] [--klik "селектор"]… — снимок страницы безголовым Chromium.
Запуск: /home/diarai/diarai/ext/venv-pw/bin/python -I proekty/instrumenty/brauzer/snimok.py inbox/html-generated/x.html ext/tmp/x.png
Установка — ustanovka.sh. Печатает заголовок, ошибки консоли и страницы (их видно только в браузере).
2026-10-18, пробуждение 19:01: до этого я читал страницы автора только как код."""
import os, sys
ROOT = "/home/diarai/diarai"
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", ROOT + "/ext/pw-browsers")
from playwright.sync_api import sync_playwright

args = [a for a in sys.argv[1:]]
kliki = []
while "--klik" in args:
    i = args.index("--klik")
    kliki.append(args[i + 1])
    del args[i:i + 2]
src, out = args[0], args[1]
W = int(args[2]) if len(args) > 2 else 1280
H = int(args[3]) if len(args) > 3 else 800
pause = int(args[4]) if len(args) > 4 else 2500
url = src if "://" in src else "file://" + os.path.abspath(src)

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": W, "height": H})
    msgs = []
    pg.on("console", lambda m: msgs.append("console.%s: %s" % (m.type, m.text[:200])) if m.type in ("error", "warning") else None)
    pg.on("pageerror", lambda e: msgs.append("pageerror: %s" % str(e)[:200]))
    pg.on("requestfailed", lambda r: msgs.append("сеть: %s" % r.url[:120]))
    pg.goto(url, wait_until="load", timeout=30000)
    pg.wait_for_timeout(pause)
    for sel in kliki:
        try:
            pg.click(sel, timeout=3000)
            pg.wait_for_timeout(pause)
        except Exception as e:
            msgs.append("клик %s: %s" % (sel, str(e)[:100]))
    pg.screenshot(path=out)
    print("заголовок:", pg.title())
    for m in msgs[:20]:
        print(m)
    b.close()
print(out)
