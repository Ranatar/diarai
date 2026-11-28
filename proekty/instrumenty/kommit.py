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
# 2026-11-28: напоминание об утверждениях «только / нет / не нашёл» в добавляемых строках (tolko.py)
tk = run([sys.executable, "-I", os.path.join(root, "proekty", "instrumenty", "tolko.py")])
if tk.stderr.strip():
    print(tk.stderr.strip())
# 2026-11-28, 03:07: номера строк «Фауста» — если README перевода в коммите (faust_nomera.py; сдвиг 670–696 нашёл проверяющий)
st = run(["git", "diff", "--cached", "--name-only"]).stdout
if "proekty/faust-kvenya/README.md" in st:
    fn = run([sys.executable, "-I", os.path.join(root, "proekty", "instrumenty", "faust_nomera.py")]).stdout.strip()
    if fn and not fn.endswith("расхождений: 0"):
        print("faust_nomera: " + fn)
# 2026-11-28, 05:47: недописанный audio.wav рендера (26 МБ) ушёл в коммит, потому что .gitignore его не закрывал.
# Теперь всё, что больше 20 МБ, снимается с индекса до коммита, и об этом печатается строка.
krupnye = []
for f in st.split("\n"):
    pf = os.path.join(root, f)
    if f and os.path.isfile(pf) and os.path.getsize(pf) > 20 * 1024 * 1024:
        run(["git", "reset", "-q", "HEAD", "--", f])
        krupnye.append("%s (%d МБ)" % (f, os.path.getsize(pf) // (1024 * 1024)))
if krupnye:
    print("НЕ КОММИЧУ, больше 20 МБ (дописать в .gitignore): " + "; ".join(krupnye))
c = run(["git", "commit", "-q", "-m", msg])
if c.returncode != 0:
    print((c.stdout + c.stderr).strip() or "коммит не сделан"); sys.exit(c.returncode)
p = run(["git", "push", "-q"])
print("закоммичено и отправлено" if p.returncode == 0 else "закоммичено, push не прошёл: " + (p.stderr.strip()[:300]))
