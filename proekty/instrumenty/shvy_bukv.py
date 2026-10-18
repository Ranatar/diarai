"""shvy_bukv.py файл.html ... — ищет в тексте страниц слова-мутанты: строчная кириллица, внутри которой
заглавная кириллическая буква или греческая буква («пармениДовский», «пармениδовский»).
Печатает по файлу: слово, число, номера строк текста (первая и последняя), чтобы видеть, где форма живёт."""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.out = []; self.skip = 0
    def handle_starttag(self, t, a):
        if t in ("script", "style"): self.skip += 1
        if t in ("p", "div", "br", "li", "h1", "h2", "h3", "h4", "tr", "td"): self.out.append("\n")
    def handle_endtag(self, t):
        if t in ("script", "style"): self.skip -= 1
    def handle_data(self, d):
        if not self.skip: self.out.append(d)

MUT = re.compile(r"\b[а-яё]+(?:[А-ЯЁ]|[α-ωΑ-Ω])[а-яё]+\b")
for path in sys.argv[1:]:
    p = P(); p.feed(open(path, encoding="utf-8", errors="replace").read())
    lines = "".join(p.out).splitlines()
    seen = {}
    for i, l in enumerate(lines):
        for w in MUT.findall(l):
            seen.setdefault(w, []).append(i)
    if seen:
        print("==", os.path.basename(path), "строк", len(lines))
        for w, ix in sorted(seen.items(), key=lambda kv: kv[1][0]):
            print("  %-28s %3d  %d..%d" % (w, len(ix), ix[0], ix[-1]))
