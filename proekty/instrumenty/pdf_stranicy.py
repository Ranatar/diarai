"""pdf_stranicy.py in.pdf out.txt от до — текст страниц [от, до] (с 1) через pypdf; запуск ext/venv-pdf/bin/python -I."""
import sys
import pypdf
r = pypdf.PdfReader(sys.argv[1])
a, b = int(sys.argv[3]), int(sys.argv[4])
with open(sys.argv[2], "w", encoding="utf-8") as f:
    for i in range(a - 1, min(b, len(r.pages))):
        f.write("\n=== стр. %d ===\n" % (i + 1))
        f.write(r.pages[i].extract_text() or "")
print(sys.argv[2])
