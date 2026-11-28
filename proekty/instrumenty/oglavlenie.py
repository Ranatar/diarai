"""oglavlenie.py — порождает proekty/instrumenty/README.md: по каждому скрипту первая строка его docstring.
28.11, пробуждение 05:47: карта проектов (proekty/karta_proektov.py) показала, что у instrumenty нет README.
Запуск: python3 -I proekty/instrumenty/oglavlenie.py (после нового скрипта)."""
import ast, os

D = os.path.dirname(os.path.abspath(__file__))
rows = []
for root, dirs, files in os.walk(D):
    dirs[:] = sorted(d for d in dirs if not d.startswith((".", "__")))
    for f in sorted(files):
        if not f.endswith(".py"):
            continue
        p = os.path.join(root, f)
        try:
            doc = ast.get_docstring(ast.parse(open(p, encoding="utf-8").read())) or ""
        except Exception:
            doc = ""
        first = " ".join(doc.strip().split("\n")[0].split()) if doc else "(нет docstring)"
        if len(first) > 170:
            first = first[:167] + "…"
        rows.append((os.path.relpath(p, D), first.replace("|", "/")))
out = ["# Инструменты", "", "Порождается `python3 -I proekty/instrumenty/oglavlenie.py` — первая строка docstring каждого скрипта.",
       "Самые нужные — в моём разделе CLAUDE.md и в `notes/tehnika.md`.", "", "| скрипт | что |", "|---|---|"]
out += ["| `%s` | %s |" % r for r in rows]
open(os.path.join(D, "README.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("скриптов: %d; без docstring: %d" % (len(rows), sum(1 for r in rows if r[1] == "(нет docstring)")))
