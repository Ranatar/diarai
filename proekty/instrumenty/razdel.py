"""razdel.py — сколько слов и строк в моём разделе CLAUDE.md (предел: ~700 слов, 40 строк). 2026-10-18."""
import os
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
text = open(os.path.join(root, "CLAUDE.md"), encoding="utf-8").read()
part = text.split("## Раздел, который принадлежит тебе")[1]
print("слов:", len(part.split()), "| строк:", len(part.strip().splitlines()))
