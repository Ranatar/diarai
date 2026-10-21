"""atlas.py — открыть complex-atlas автора с заданной формулой и вкладкой, кликнуть, снять, прочитать боковую панель.
Запуск:
  ext/venv-pw/bin/python -I proekty/instrumenty/brauzer/atlas.py "z^2+1" analysis out.png [опции]
Опции:
  --vid cx cy scale     вид (scale — единиц на пиксель; по умолчанию 0 0 5/600)
  --knopka "Текст"      нажать кнопку/вкладку в боковой панели по тексту (можно несколько, по порядку)
  --potom "Текст"       кнопка после кликов по полю
  --tochka re im        клик по полю в точке z = re + i·im (можно несколько; после кнопок)
  --zhdat мс            пауза перед снимком (по умолчанию 1500)
  --fajl путь           копия страницы вместо оригинала
  --panel               напечатать текст боковой панели
Состояние передаётся через location.hash (s=base64(JSON)), как в самой странице (строки 9276–9355).
2026-10-21, пробуждение 06:08: письмо 19, «попробуй изучить complex-atlas»."""
import os, sys, json, base64
ROOT = "/home/diarai/diarai"
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", ROOT + "/ext/pw-browsers")
from playwright.sync_api import sync_playwright

a = sys.argv[1:]
def opt(name, n):
    out = []
    while name in a:
        i = a.index(name); out.append(a[i + 1:i + 1 + n]); del a[i:i + 1 + n]
    return out
vid = opt("--vid", 3)
knopki = [x[0] for x in opt("--knopka", 1)]
potom = [x[0] for x in opt("--potom", 1)]   # кнопки после кликов по полю («замкнуть петлю»)
tochki = [(float(x[0]), float(x[1])) for x in opt("--tochka", 2)]
zh = opt("--zhdat", 1); zhdat = int(zh[0][0]) if zh else 1500
fj = opt("--fajl", 1)   # другая копия страницы (для опытов с правкой)
fajl = fj[0][0] if fj else "inbox/html-generated/complex-atlas.html"
panel = "--panel" in a
if panel: a.remove("--panel")
expr, mode, out = a[0], a[1], a[2]
cx, cy, sc = (0.0, 0.0, 5 / 600)
if vid: cx, cy, sc = float(vid[0][0]), float(vid[0][1]), eval(vid[0][2], {})
st = {"expr": expr, "mode": mode}
if mode in ("phase", "analysis", "compare", "conformal", "fractal"):
    st["view"] = {"cx": cx, "cy": cy, "scale": sc}
h = base64.b64encode(json.dumps(st, ensure_ascii=False).encode("utf-8")).decode()
url = "file://" + ROOT + "/" + fajl + "#s=" + h

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1400, "height": 900})
    pg.on("pageerror", lambda e: print("ОШИБКА:", e))
    pg.goto(url)
    pg.wait_for_timeout(1200)
    def nazhat(k):
        loc = pg.locator("#sidebar").get_by_text(k, exact=True)
        if loc.count() == 0:
            loc = pg.get_by_text(k, exact=True)
        print("кнопка", k, "найдено", loc.count())
        if loc.count(): loc.first.click(); pg.wait_for_timeout(500)
    for k in knopki: nazhat(k)
    if tochki:
        cv = pg.locator("#cv-" + mode)
        bb = cv.bounding_box()
        # scale в вьюхе — на пиксель холста, а холст бывает шире своего CSS-бокса (21.10: клик в 1+i попадал в 1.552+1.552i)
        k = cv.evaluate("c => c.width / c.getBoundingClientRect().width")
        for re_, im_ in tochki:
            x = bb["x"] + bb["width"] / 2 + (re_ - cx) / sc / k
            y = bb["y"] + bb["height"] / 2 - (im_ - cy) / sc / k
            pg.mouse.click(x, y); pg.wait_for_timeout(600)
    for k in potom: nazhat(k)
    pg.wait_for_timeout(zhdat)
    pg.screenshot(path=out)
    if panel:
        print(pg.locator("#sidebar").inner_text())
    b.close()
