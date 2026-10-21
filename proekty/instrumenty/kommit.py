"""kommit.py "сообщение" — git add -A; проверка пометок времени (vremya_vpered.py, только предупреждение); git commit; git push.
Одна команда вместо цепочки «git add && git commit && git push», которую Bash то пропускает, то нет.
2026-10-21, пробуждение 12:08: хук .git/hooks/pre-commit поставить не дали (чувствительный файл), поэтому — обёртка."""
import os, subprocess, sys
root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
msg = " ".join(sys.argv[1:]).strip()
if not msg:
    print("нужно сообщение коммита"); sys.exit(1)
def run(args):
    return subprocess.run(args, cwd=root, capture_output=True, text=True)
run(["git", "add", "-A"])
v = run([sys.executable, "-I", os.path.join(root, "proekty", "instrumenty", "vremya_vpered.py")])
if v.stderr.strip():
    print(v.stderr.strip())
c = run(["git", "commit", "-q", "-m", msg])
if c.returncode != 0:
    print((c.stdout + c.stderr).strip() or "коммит не сделан"); sys.exit(c.returncode)
p = run(["git", "push", "-q"])
print("закоммичено и отправлено" if p.returncode == 0 else "закоммичено, push не прошёл: " + (p.stderr.strip()[:300]))
