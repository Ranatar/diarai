"""pdf_vzglyad.py in.pdf [страниц] — число страниц, метаданные и текст первых страниц (pypdf, ext/venv-pdf).
Для больших PDF, которые целиком извлекать не хочется."""
import sys
import pypdf
r = pypdf.PdfReader(sys.argv[1])
n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
print("страниц:", len(r.pages), "| метаданные:", dict(r.metadata or {}))
for i in range(min(n, len(r.pages))):
    t = (r.pages[i].extract_text() or "").strip()
    print("--- стр. %d (%d знаков)" % (i + 1, len(t)))
    print(t[:700])
