"""vremya_vpered.py — ищет в добавляемых строках (git diff --cached, иначе git diff) пометки времени ЧЧ:ММ,
которые позже текущего времени больше чем на 2 минуты. Такая пометка — время «на глаз», ушедшее вперёд.
Печатает предупреждения и всегда выходит с кодом 0 (ничего не запрещает).
Исключения: строки с «UTC», с датой не сегодняшнего дня (ГГГГ-ММ-ДД), диапазоны вида «12:41:58 → 12:46:03» проверяются
так же (секунды игнорируются). Время в цитатах чужих текстов тоже может попасться — смотреть глазами.
2026-10-21, пробуждение 12:08: за час семь пометок времени ушли вперёд на 5–35 минут («12:35» в 12:12).
Повешено на .git/hooks/pre-commit (только предупреждение)."""
import datetime, re, subprocess, sys, os
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
def diff(args):
    try:
        return subprocess.run(["git", "-C", root, "diff", "-U0"] + args, capture_output=True, text=True).stdout
    except Exception:
        return ""
d = diff(["--cached"]) or diff([])
now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d")
nowmin = now.hour * 60 + now.minute
found = 0
fname = "?"
for line in d.splitlines():
    if line.startswith("+++ "):
        fname = line[6:] if line.startswith("+++ b/") else line[4:]
        continue
    if not line.startswith("+") or line.startswith("+++"):
        continue
    if "UTC" in line:
        continue
    dates = re.findall(r"\b(20\d\d-\d\d-\d\d)\b", line)
    if dates and today not in dates:
        continue
    for m in re.finditer(r"(?<![\d:.])([01]\d|2[0-3]):([0-5]\d)(?::\d\d)?(?![\d])", line):
        t = int(m.group(1)) * 60 + int(m.group(2))
        if t - nowmin > 2:
            found += 1
            s = line[max(0, m.start() - 50): m.end() + 30].strip()
            print("ВРЕМЯ ВПЕРЕДИ: %s в %s (сейчас %s): …%s…" % (m.group(0), fname, now.strftime("%H:%M"), s), file=sys.stderr)
if found:
    print("vremya_vpered: %d пометок времени позже, чем сейчас. Время — из metka.py или date, не из головы." % found, file=sys.stderr)
sys.exit(0)
