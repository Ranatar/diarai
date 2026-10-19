"""poet.py корпус.txt словарь.tsv размер семя строф [тема] — запустить веб-порт программы-поэта Каганова
(inbox/lleo_poet_bundle/lleo_poet.html) в headless-браузере, обучить на корпусе и сочинить.
Ударения: сначала из словаря (slovar.py), остальные — прогнозом приложения (autoRest).
Запуск: ext/venv-pw/bin/python -I proekty/lleo/poet.py ..."""
import sys, json, os
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/home/diarai/diarai/ext/pw-browsers")
from playwright.sync_api import sync_playwright
PAGE = "file:///home/diarai/diarai/inbox/lleo_poet_bundle/lleo_poet.html"
korpus = open(sys.argv[1], encoding="utf-8").read()
slovar = open(sys.argv[2], encoding="utf-8").read()
razmer, semya, n = sys.argv[3], sys.argv[4], int(sys.argv[5])
tema = sys.argv[6] if len(sys.argv) > 6 else ""

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page()
    pg.on("dialog", lambda d: d.accept())
    pg.route("**/fonts.googleapis.com/**", lambda r: r.abort())
    pg.goto(PAGE)
    pg.wait_for_timeout(500)
    pg.click("#clearBase")
    pg.wait_for_timeout(200)
    res = pg.evaluate("""([slovar, korpus]) => {
        const d = importStressDict(slovar, {populate:false, addWords:true});
        const t = trainFromText(korpus);
        const q = buildStressQueue(); startStress(q); if (q.length) autoRest();
        return {N: base.N, dict: d.added, sentences: t.sentences, assoc: t.assoc, autostress: q.length,
                meters: Object.keys(meterLib)};
    }""", [slovar, korpus])
    print(json.dumps(res, ensure_ascii=False), file=sys.stderr)
    out = pg.evaluate("""([razmer, semya, n, tema]) => {
        scheme = clonePreset(meterLib[razmer]); setSeed(semya);
        const c = generateVerse(scheme, n, tema);
        return c.map(x => x.join('\\n')).join('\\n\\n');
    }""", [razmer, semya, n, tema])
    print(out)
    b.close()
