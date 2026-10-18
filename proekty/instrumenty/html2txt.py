"""html2txt.py in.html out.txt — текст страницы без скриптов и стилей, абзацы сохраняются."""
import sys, re
from html.parser import HTMLParser

BLOCK = {'p', 'div', 'br', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'tr', 'section',
         'article', 'blockquote', 'header', 'footer', 'table', 'pre', 'figcaption', 'dt', 'dd'}

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out, self.skip = [], 0
    def handle_starttag(self, t, a):
        if t in ('script', 'style'):
            self.skip += 1
        if t in BLOCK:
            self.out.append('\n')
        if t in ('h1', 'h2', 'h3', 'h4'):
            self.out.append('#' * int(t[1]) + ' ')
    def handle_endtag(self, t):
        if t in ('script', 'style'):
            self.skip -= 1
        if t in BLOCK:
            self.out.append('\n')
    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)

p = P()
p.feed(open(sys.argv[1], encoding='utf-8').read())
txt = ''.join(p.out)
txt = re.sub(r'[ \t]+', ' ', txt)
txt = re.sub(r'\n\s*\n\s*(\n\s*)+', '\n\n', txt)
open(sys.argv[2], 'w', encoding='utf-8').write(txt.strip() + '\n')
print(len(txt.split()), 'слов')
