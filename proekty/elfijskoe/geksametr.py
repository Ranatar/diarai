"""geksametr.py — насколько строка квенья ложится в количественный (метрический) дактилический гекзаметр.

Долгота слога: долгий гласный или дифтонг (ai oi ui iu eu au) — долгий «по природе»; краткий гласный, за которым
два согласных и больше (считая через границу слов, как в латинском стихе; qu, x, ny, ty, ly… = два, как в kv_udar.py),
— долгий «по положению»; иначе краткий. Последний слог строки — anceps.
Гекзаметр: стопы 1–5 — дактиль «— u u» или спондей «— —», стопа 6 — «— x». Скрипт ищет разбор с наименьшим числом
нарушений (краткий на месте долгого или долгий на месте краткого) и печатает его.
Слоговое деление и долгота — функции proekty/instrumenty/kv_udar.py (units). Зияние на стыке слов не сливается
(элизия только там, где апостроф).
Оговорки: правило «долгота по положению через границу слов» взято из латыни; как считал бы эльф, неизвестно.
«Мute cum liquida» (краткость перед смычным + плавным) не учтена: все такие слоги долгие.
Запуск: python3 -I proekty/elfijskoe/geksametr.py файл_со_строками
21.10, пробуждение 03:07: к «Эллинам и эльфам» автора — он пожалел, что не вышло метрического гекзаметра."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "instrumenty"))
from kv_udar import units  # noqa: E402


def kolichestvo(line):
    u = []
    for w in line.split():
        u += units(w)
    sl = []
    for k, (t, s, x) in enumerate(u):
        if t != "V":
            continue
        cons = 0
        for t2, s2, n2 in u[k + 1:]:
            if t2 == "V":
                break
            cons += n2
        sl.append("-" if (x or cons >= 2) else "u")
    return sl


def razbor(sl):
    n = len(sl)
    INF = 10 ** 9
    # best[i][f] = (цена, схема) — разобрано i слогов, f стоп
    best = {(0, 0): (0, "")}
    for f in range(6):
        nxt = {}
        for (i, ff), (c, sch) in best.items():
            if ff != f:
                continue
            stopy = [("-", "-")] if f == 5 else [("-", "u", "u"), ("-", "-")]
            for st in stopy:
                if i + len(st) > n:
                    continue
                cost = 0
                for j, m in enumerate(st):
                    real = sl[i + j]
                    last = (f == 5 and j == 1)
                    if not last and real != m:
                        cost += 1
                key = (i + len(st), f + 1)
                val = (c + cost, sch + "".join(st) + "|")
                if key not in nxt or nxt[key][0] > val[0]:
                    nxt[key] = val
        best.update(nxt)
    if (n, 6) in best:
        return best[(n, 6)]
    return (None, "")


if __name__ == "__main__":
    lines = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
    tochno = 0
    for l in lines:
        sl = kolichestvo(l)
        c, sch = razbor(sl)
        if c == 0:
            tochno += 1
        print("%2d слогов  %s" % (len(sl), "".join(sl)))
        print("   %s  %s" % (("нарушений: %d" % c) if c is not None else "не 13–17 слогов, разбора нет", sch))
        print("   " + l)
    print("строк: %d; ложатся без нарушений: %d" % (len(lines), tochno))
