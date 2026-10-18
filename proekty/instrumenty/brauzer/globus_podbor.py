"""globus_podbor.py out-префикс долгота широта [секунд_теста] — в globe.html: орто-вид на точку, слой «Регионы»,
клик в центр (выбор региона), «⌖ Подобрать проекцию» → «Запустить тест», снимки после каждого шага
(префикс-1-tip.png, -2-finder.png, -3-result.png) и текст результатов.
2026-10-18, пробуждение 21:20."""
import os, sys, http.server, threading, functools
ROOT = "/home/diarai/diarai"
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", ROOT + "/ext/pw-browsers")
from playwright.sync_api import sync_playwright

pref, lon, lat = sys.argv[1], sys.argv[2], sys.argv[3]
sek = int(sys.argv[4]) if len(sys.argv) > 4 else 60
EQ = chr(61)
h = "&".join(k + EQ + v for k, v in [("v", "1"), ("p", "orthographic"), ("c", lon + "," + lat), ("lv", str(1 + 2 + 16 + 64)), ("t", "atlas")])


class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(H, directory=ROOT))
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = "http://127.0.0.1:%d/inbox/html-generated/maps/globe.html#%s" % (srv.server_address[1], h)

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1400, "height": 1000})
    oshibki = []
    pg.on("pageerror", lambda e: oshibki.append(str(e)[:200]))
    pg.goto(url, wait_until="load", timeout=30000)
    pg.wait_for_timeout(4000)
    box = pg.evaluate("""() => { let best = null;
      for (const c of document.querySelectorAll('canvas')) { const r = c.getBoundingClientRect();
        if (r.width * r.height > 0 && (!best || r.width * r.height > best.w * best.h)) best = {x: r.x, y: r.y, w: r.width, h: r.height}; }
      return best; }""")
    cx, cy = box["x"] + box["w"] / 2, box["y"] + box["h"] / 2
    pg.mouse.click(cx, cy)
    pg.wait_for_timeout(1500)
    pg.screenshot(path=pref + "-1-tip.png")
    tip = pg.locator("#pickTip")
    print("== подсказка:", tip.inner_text()[:800] if tip.count() else "(нет #pickTip)")
    btn = pg.locator(".pt-finder-btn")
    if btn.count() and btn.first.is_visible():
        btn.first.click()
        pg.wait_for_timeout(1500)
        pg.screenshot(path=pref + "-2-finder.png")
        print("== окно подбора:", pg.locator("#projfinder").inner_text()[:1500])
        pg.locator(".pf-run").first.click()
        for i in range(sek):
            pg.wait_for_timeout(1000)
            if pg.locator(".pf-stop").first.is_hidden() and i > 2:
                break
        print("== прошло секунд:", i + 1)
        pg.screenshot(path=pref + "-3-result.png", full_page=True)
        print("== результаты:", pg.locator("#projfinder .pf-results").inner_text()[:3000])
    else:
        print("кнопки подбора нет")
    for e in oshibki:
        print("ошибка:", e)
    b.close()
