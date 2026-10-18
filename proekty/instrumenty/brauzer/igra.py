"""igra.py страница.html out.png [выбор1 выбор2 …] — сыграть текстовую игру по шагам.
Каждый запуск начинает заново: Math.random закреплён (семя 1147), выборы — номера кнопок (с 1)
или «@Текст». Печатает текст сцены и пронумерованные кнопки после последнего шага.
Так можно играть «по ходу»: посмотрел кнопки — дописал номер — запустил снова.
Запуск: /home/diarai/diarai/ext/venv-pw/bin/python -I proekty/instrumenty/brauzer/igra.py inbox/html-generated/silm_game.html ext/tmp/g.png 1 2
Опции: --sel "css" — селектор кнопок выбора (по умолчанию все видимые button), --tekst "css" — где текст сцены (по умолчанию body).
2026-10-18, пробуждение 21:07 (для «Кузницы Феанора»)."""
import os, sys
ROOT = "/home/diarai/diarai"
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", ROOT + "/ext/pw-browsers")
from playwright.sync_api import sync_playwright

args = sys.argv[1:]
def opt(name, default):
    if name in args:
        i = args.index(name); v = args[i + 1]; del args[i:i + 2]; return v
    return default
SEL = opt("--sel", "button:visible")
TXT = opt("--tekst", "body")
src, out, vybory = args[0], args[1], args[2:]
SEED = """(() => { let s = 1147; Math.random = () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }; })();"""

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1280, "height": 1000})
    pg.add_init_script(SEED)
    oshibki = []
    pg.on("pageerror", lambda e: oshibki.append(str(e)[:200]))
    pg.goto("file://" + os.path.abspath(src), wait_until="load")
    pg.wait_for_timeout(800)
    for v in vybory:
        knopki = pg.locator(SEL)
        if v.startswith("@"):
            pg.locator(SEL, has_text=v[1:]).first.click()
        else:
            knopki.nth(int(v) - 1).click()
        pg.wait_for_timeout(700)
    print(pg.locator(TXT).first.inner_text()[:6000])
    print("---- кнопки:")
    knopki = pg.locator(SEL)
    for i in range(knopki.count()):
        print("%d. %s" % (i + 1, knopki.nth(i).inner_text().replace("\n", " ")[:160]))
    for e in oshibki:
        print("ошибка:", e)
    pg.screenshot(path=out, full_page=True)
    b.close()
