"""opcii.py путь|srv:путь [пауза_мс] — выписать с живой страницы все <select> (id и все варианты, включая
заполненные скриптом), кнопки и чекбоксы с подписями. Для разведки интерфейса прежде снимков.
2026-10-18, пробуждение 21:20 (разведка globe.html и hwph по просьбе автора)."""
import os, sys, http.server, threading, functools
ROOT = "/home/diarai/diarai"
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", ROOT + "/ext/pw-browsers")
from playwright.sync_api import sync_playwright

src = sys.argv[1]
pause = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
if src.startswith("srv:"):
    H_ = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    H_.log_message = lambda *a: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H_)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = "http://127.0.0.1:%d/%s" % (srv.server_address[1], src[4:])
else:
    url = "file://" + os.path.abspath(src)

JS = """() => {
  const out = [];
  for (const s of document.querySelectorAll('select')) {
    out.push('== select #' + s.id + ' (' + s.options.length + ')');
    let grp = null;
    for (const o of s.options) {
      const g = o.parentElement.tagName === 'OPTGROUP' ? o.parentElement.label : null;
      if (g !== grp) { grp = g; if (g) out.push('  [' + g + ']'); }
      out.push('    ' + o.value + ' | ' + o.textContent.trim());
    }
  }
  out.push('== кнопки');
  for (const b of document.querySelectorAll('button')) {
    const t = (b.textContent || b.title || '').trim().replace(/\\s+/g, ' ');
    if (t) out.push('    ' + (b.id ? '#' + b.id + ' ' : '') + t.slice(0, 80));
  }
  out.push('== чекбоксы');
  for (const c of document.querySelectorAll('input[type=checkbox]')) {
    const l = c.closest('label') || document.querySelector('label[for="' + c.id + '"]');
    out.push('    #' + c.id + ' ' + (l ? l.textContent.trim().replace(/\\s+/g, ' ').slice(0, 80) : ''));
  }
  return out.join('\\n');
}"""
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1400, "height": 1000})
    pg.goto(url, wait_until="load", timeout=30000)
    pg.wait_for_timeout(pause)
    print(pg.evaluate(JS))
    b.close()
