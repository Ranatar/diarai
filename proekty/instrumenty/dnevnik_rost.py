"""dnevnik_rost.py — как растёт дневник: по файлу на пробуждение — слов, заголовков, длительность
(от времени в имени файла до последней метки ЧЧ:ММ в заголовках) и слов в минуту.
Вопрос: не раздувается ли дневник от пробуждения к пробуждению (инфляция сюжета)?"""
import os, re, glob, datetime

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "diary")
print("%-16s %6s %5s %6s %7s" % ("пробуждение", "слов", "загол", "минут", "слов/мин"))
for p in sorted(glob.glob(os.path.join(root, "*.md"))):
    name = os.path.basename(p)[:-3]
    t = open(p, encoding="utf-8").read()
    words = len(re.findall(r"\w+", t))
    heads = re.findall(r"^## .*", t, re.M)
    try:
        start = datetime.datetime.strptime(name, "%Y-%m-%d-%H%M")
    except ValueError:
        continue
    times = []
    for h in heads:
        m = re.search(r"\b(\d{1,2}):(\d{2})", h)
        if m:
            times.append(start.replace(hour=int(m.group(1)), minute=int(m.group(2))))
    mins = None
    if times:
        last = max(times)
        if last < start:
            last += datetime.timedelta(days=1)
        mins = (last - start).total_seconds() / 60
    rate = "%.0f" % (words / mins) if mins and mins > 0 else "—"
    print("%-16s %6d %5d %6s %7s" % (name, words, len(heads), "%.0f" % mins if mins is not None else "—", rate))
