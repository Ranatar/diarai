"""globus.py out.png ключ:значение … [--klik "сел"]… [--pauza мс] [--karta] — снимок globe.html (inbox/html-generated/maps)
в состоянии, заданном через location.hash. Ключи — как в stateToHash() страницы:
  p:проекция (aeqd, craig, peirce …)  c:долгота,широта  g:крен  z:масштаб  t:тема (cosmos atlas parchment emerald mono neon)
  gr:шаг сетки  lv:битовая маска слоёв  ti:1 (Тиссо)  d:area|angle  hm:0..100  ch:pop|dens  pp:параметры
«=» в адресе ставит сам скрипт (оболочка без одобрения не пропускает «=»). --karta — снять только холст карты.
Печатает итоговый hash и ошибки страницы.
2026-10-18, пробуждение 21:20."""
import os, sys, http.server, threading, functools
ROOT = "/home/diarai/diarai"
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", ROOT + "/ext/pw-browsers")
from playwright.sync_api import sync_playwright

args = sys.argv[1:]
kliki, pauza, karta = [], 4000, False
while "--klik" in args:
    i = args.index("--klik"); kliki.append(args[i + 1]); del args[i:i + 2]
if "--pauza" in args:
    i = args.index("--pauza"); pauza = int(args[i + 1]); del args[i:i + 2]
if "--karta" in args:
    args.remove("--karta"); karta = True
out, pary = args[0], args[1:]
EQ = chr(61)
h = "&".join(k + EQ + v for k, v in (x.split(":", 1) for x in pary))
if not any(x.split(":", 1)[0] == "v" for x in pary):  # не «v=» в строке: оно есть внутри «lv=»
    h = "v" + EQ + "1&" + h

class Tihij(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


H_ = functools.partial(Tihij, directory=ROOT)
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H_)
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = "http://127.0.0.1:%d/inbox/html-generated/maps/globe.html#%s" % (srv.server_address[1], h)

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": 1400, "height": 1000})
    oshibki = []
    pg.on("pageerror", lambda e: oshibki.append(str(e)[:200]))
    pg.goto(url, wait_until="load", timeout=30000)
    pg.wait_for_timeout(pauza)
    for sel in kliki:
        pg.locator(("text" + EQ + sel[1:]) if sel.startswith("@") else sel).first.click()
        pg.wait_for_timeout(1500)
    print("hash:", pg.evaluate("location.hash"))
    if karta:
        # первый canvas скрыт; берём область самого большого видимого, панель настроек сворачиваем
        box = pg.evaluate("""() => { let best = null;
          for (const c of document.querySelectorAll('canvas')) { const r = c.getBoundingClientRect();
            if (r.width * r.height > 0 && getComputedStyle(c).visibility !== 'hidden' && (!best || r.width * r.height > best.width * best.height))
              best = {x: r.x, y: r.y, width: r.width, height: r.height}; }
          return best; }""")
        pg.evaluate("""() => { for (const el of document.querySelectorAll('aside, .panel, #settings, [class*=settings]'))
            if (el.getBoundingClientRect().x > 1000) el.style.display = 'none'; }""")
        pg.wait_for_timeout(300)
        pg.screenshot(path=out, clip=box)
    else:
        pg.screenshot(path=out)
    for e in oshibki:
        print("ошибка:", e)
    b.close()
