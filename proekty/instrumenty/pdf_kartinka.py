"""pdf_kartinka.py in.pdf страница(с 1) dpi out.png — рендер одной страницы в PNG (PyMuPDF), текст НЕ выводится.
Для слепых проб: ни текстового слоя, ни соседних страниц. Запуск: ext/venv-pdf/bin/python -I. 2026-10-21."""
import sys
import fitz
doc = fitz.open(sys.argv[1])
n = int(sys.argv[2]) - 1
pix = doc[n].get_pixmap(dpi=int(sys.argv[3]))
pix.save(sys.argv[4])
print(pix.width, "x", pix.height)
