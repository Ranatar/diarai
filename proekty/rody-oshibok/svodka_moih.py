"""svodka_moih.py — сводка МОИХ ошибок по всем oshibki-*.tsv (первый столбец — род), с картой синонимов,
потому что названия родов от пробуждения к пробуждению плавают («ложное «нет»», «нет до досмотра», «ложное «только»» — одно).
Запуск: python3 -I proekty/rody-oshibok/svodka_moih.py [--po-probuzhdeniyam]
Печатает: сколько записей у каждого рода (после склейки) и, с ключом, разбивку по файлам.
Счёт — только записи реестра; что не записано, сюда не попало. 2026-11-28, пробуждение 23:58."""
import collections, glob, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
SINONIMY = [  # (регулярное выражение по началу рода, общее имя)
    (r"ложное «(нет|только)»|нет до досмотра|ложное «только»", "ложное «нет/только»"),
    (r"пропущенное (у Толкина|у автора|позднее)", "пропущенное (у Толкина/автора/позднее)"),
    (r"забытое своё", "забытое своё"),
    (r"дорисованн", "дорисованное"),
    (r"счёт/время на глаз|время", "время"),
]
def obshchee(rod):
    for rx, imya in SINONIMY:
        if re.match(rx, rod):
            return imya
    return rod
c = collections.Counter()
po = collections.defaultdict(collections.Counter)
for f in sorted(glob.glob(os.path.join(here, "oshibki-*.tsv"))):
    tag = os.path.basename(f)[8:-4]
    for line in open(f, encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        r = obshchee(line.split("\t")[0].strip())
        c[r] += 1
        po[r][tag] += 1
print("файлов: %d, записей: %d" % (len(glob.glob(os.path.join(here, "oshibki-*.tsv"))), sum(c.values())))
for r, n in c.most_common():
    s = "%4d  %s" % (n, r)
    if "--po-probuzhdeniyam" in sys.argv:
        s += "   " + ", ".join("%s:%d" % (k, v) for k, v in sorted(po[r].items()))
    print(s)
