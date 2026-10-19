"""webmap_klik.py [--sloj sim|real|diff] [--absorb] x,y [x,y …] — клики по «Коалесцентной карте» (inbox/html-generated/webmap)
в точках окна 1400×900 и текст панели «Выбранная область» после каждого клика. Печатает текст; снимок — ext/tmp/wm/klik.png.
2026-10-19, пробуждение 00:08: snimok.py кликает только по селекторам, а карте нужны координаты."""
import os, sys, threading, functools, http.server
ROOT = "/home/diarai/diarai"
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", ROOT + "/ext/pw-browsers")
from playwright.sync_api import sync_playwright

args = sys.argv[1:]
sloj = "sim"
if "--sloj" in args:
    i = args.index("--sloj"); sloj = args[i + 1]; del args[i:i + 2]
absorb = "--absorb" in args
args = [a for a in args if a != "--absorb"]
kadry = []   # --kadry 10,30,60 — снимки анимации роста на этих процентах: ext/tmp/wm/kadr-NN.png
if "--kadry" in args:
    i = args.index("--kadry"); kadry = [float(v) for v in args[i + 1].split(",")]; del args[i:i + 2]
tochki = [tuple(float(v) for v in a.split(",")) for a in args]

H_ = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H_)
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = "http://127.0.0.1:%d/inbox/html-generated/webmap/index.html" % srv.server_address[1]

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1400, "height": 900})
    pg.goto(url, wait_until="load", timeout=30000)
    pg.wait_for_timeout(3000)
    if absorb:
        pg.check("input[name='mode'][value='absorb']"); pg.wait_for_timeout(3000)
    pg.check("input[name='layer'][value='%s']" % sloj); pg.wait_for_timeout(1500)
    for (x, y) in tochki:
        pg.mouse.click(x, y)
        pg.wait_for_timeout(800)
        t = pg.inner_text("#info-body")
        print("== %g,%g ::" % (x, y), " | ".join(s for s in t.split("\n") if s.strip()))
    for pr in kadry:
        v = 65535 * pr / 100
        pg.evaluate("v => { const s = document.querySelector('#seek'); s.value = v; s.dispatchEvent(new Event('input')); }", v)
        pg.wait_for_timeout(1200)
        pg.screenshot(path=ROOT + "/ext/tmp/wm/kadr-%02d.png" % int(pr), clip={"x": 300, "y": 0, "width": 1100, "height": 820})
        print("кадр", pr, pg.inner_text("#tlabel"), "|", pg.inner_text("#counter"))
    pg.screenshot(path=ROOT + "/ext/tmp/wm/klik.png")
    b.close()
srv.shutdown()
