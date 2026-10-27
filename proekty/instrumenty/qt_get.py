"""qt_get.py ПУТЬ [ВЫХОД] — GET к API Quettali (https://quettali.org/api/v1/ПУТЬ), ответ в файл (по умолчанию
ext/tmp/qt-get.json) и размер на экран. Пример: qt_get.py "wordinfo?qwid=w6476,w3227"."""
import sys
import urllib.request

url = "https://quettali.org/api/v1/" + sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else "ext/tmp/qt-get.json"
with urllib.request.urlopen(url, timeout=60) as f:
    b = f.read()
with open(out, "wb") as g:
    g.write(b)
print(url, "->", out, len(b), "байт")
