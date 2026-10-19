"""igraf.py путь_файла_выборов — запустить igra.py с выборами из файла (по строке), напечатать сцену после статов."""
import subprocess, sys
ROOT = "/home/diarai/diarai"
vybory = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip() and not l.startswith("#")]
cmd = [ROOT + "/ext/venv-pw/bin/python", "-I", ROOT + "/proekty/instrumenty/brauzer/igra.py",
       ROOT + "/inbox/html-generated/silm_game.html", ROOT + "/ext/tmp/g.png", "--semya", "123456789"] + vybory
out = subprocess.run(cmd, capture_output=True, text=True).stdout + subprocess.run(["true"]).__class__.__name__ * 0
lines = out.splitlines()
# статы — первые строки до «Сила:» + число
try:
    i = max(k for k, l in enumerate(lines) if l.startswith("Сила:"))
    stats = lines[:i + 2]
    print(" ".join(s for s in stats if s.strip() and s not in ("Кузница Феанора", "Феанор", "Сильмариллы")))
    print("\n".join(lines[i + 2:]))
except ValueError:
    print(out[-3000:])
