"""PDF -> текст. Запуск: ext/venv-pdf/bin/python -I proekty/instrumenty/pdf2txt.py ВХОД.pdf ВЫХОД.txt
Нужен pypdf в ext/venv-pdf (python3 -m venv ext/venv-pdf; ext/venv-pdf/bin/pip install pypdf)."""
import sys
import pypdf

r = pypdf.PdfReader(sys.argv[1])
print(len(r.pages), "стр.")
with open(sys.argv[2], "w", encoding="utf-8") as f:
    for i, p in enumerate(r.pages, 1):
        f.write(f"\n\n=== стр. {i} ===\n")
        f.write(p.extract_text() or "")
