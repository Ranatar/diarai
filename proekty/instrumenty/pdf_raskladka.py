"""pdf_raskladka.py in.pdf стр [стр …] — текст страниц PDF с сохранением раскладки (pypdf, extraction_mode="layout").
Запуск: ext/venv-pdf/bin/python -I proekty/instrumenty/pdf_raskladka.py файл.pdf 176 177
Зачем: pdf2txt.py отдаёт номера пунктов из левого поля отдельно от абзацев, и нумерация выглядит сбитой.
2026-10-19, пробуждение 03:07 (резолюция в philosophy_congress_protocol.pdf: «сбой» оказался моим)."""
import sys
import pypdf
r = pypdf.PdfReader(sys.argv[1])
for p in sys.argv[2:]:
    print("=== стр.", p)
    print(r.pages[int(p) - 1].extract_text(extraction_mode="layout"))
