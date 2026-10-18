"""snimok.py путь|URL out.png [ширина высота пауза_мс] [--klik "селектор"]… — снимок страницы безголовым Chromium.
Запуск: /home/diarai/diarai/ext/venv-pw/bin/python -I proekty/instrumenty/brauzer/snimok.py inbox/html-generated/x.html ext/tmp/x.png
Установка — ustanovka.sh. Печатает заголовок, ошибки консоли и страницы (их видно только в браузере).
2026-10-18, пробуждение 19:01: до этого я читал страницы автора только как код."""
import os, sys
ROOT = "/home/diarai/diarai"
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", ROOT + "/ext/pw-browsers")
from playwright.sync_api import sync_playwright

args = [a for a in sys.argv[1:]]
vvod = []   # --vvod селектор файл.txt — вписать текст из файла в поле (page.fill: событие input срабатывает)
while "--vvod" in args:
    i = args.index("--vvod")
    vvod.append((args[i + 1], open(args[i + 2], encoding="utf-8").read()))
    del args[i:i + 3]
klavishi = []   # --nazhat селектор Клавиша — нажать клавишу в элементе (End на ползунке = максимум)
while "--nazhat" in args:
    i = args.index("--nazhat")
    klavishi.append((args[i + 1], args[i + 2]))
    del args[i:i + 3]
kliki = []
while "--klik" in args:
    i = args.index("--klik")
    s = args[i + 1]
    kliki.append("text" + chr(61) + s[1:] if s.startswith("@") else s)  # «@Текст» = text=Текст (без «=» и «~» в оболочке)
    del args[i:i + 2]
src, out = args[0], args[1]
W = int(args[2]) if len(args) > 2 else 1280
H = int(args[3]) if len(args) > 3 else 800
pause = int(args[4]) if len(args) > 4 else 2500
if src.startswith("srv:"):
    # страницы с ES-модулями по file:// не грузятся: поднимаю http-сервер на корень пространства в этом же процессе
    # (фоновый сервер из другой команды недоступен — у каждой команды своя песочница)
    import threading, functools, http.server
    H_ = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H_)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = "http://127.0.0.1:%d/%s" % (srv.server_address[1], src[4:])
else:
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
    for sel in kliki:  # сначала клики (поле ввода может появиться только после выбора режима), потом ввод
        try:
            pg.click(sel, timeout=3000)
            pg.wait_for_timeout(pause)
        except Exception as e:
            msgs.append("клик %s: %s" % (sel, str(e)[:100]))
    for sel, key in klavishi:
        try:
            pg.press(sel, key, timeout=3000)
        except Exception as e:
            msgs.append("клавиша %s: %s" % (sel, str(e)[:100]))
    for sel, txt in vvod:
        try:
            pg.fill(sel, txt, timeout=3000)
            pg.wait_for_timeout(pause)
        except Exception as e:
            msgs.append("ввод %s: %s" % (sel, str(e)[:100]))
    pg.screenshot(path=out)
    print("заголовок:", pg.title())
    for m in msgs[:20]:
        print(m)
    b.close()
print(out)
