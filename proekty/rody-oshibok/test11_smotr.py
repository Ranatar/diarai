"""test11_smotr.py — места переписи теста 11: контекст и синодальный текст стиха (диапазона), ±1 стих мелко.
Жанр не печатается, чтобы не подсказывать вердикт (он размечен машиной и в таблице есть).
Запуск: python3 -I test11_smotr.py test11-perepis.tsv ext/bible/ru_synod.json [с] [по]"""
import sys, json

rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[1], encoding="utf-8")][1:]
B = {x["abbrev"]: x["chapters"] for x in json.load(open(sys.argv[2], encoding="utf-8-sig"))}
a = int(sys.argv[3]) if len(sys.argv) > 3 else 0
b = int(sys.argv[4]) if len(sys.argv) > 4 else len(rows)

def stih(kn, g, s):
    try:
        return B[kn][g - 1][s - 1]
    except (KeyError, IndexError):
        return "—"

for r in rows[a:b]:
    i, f, ref, kn, g, s, po = r[0], r[1], r[2], r[3], int(r[4]), int(r[5]), r[6]
    print("=" * 20, i, "|", f[-45:], "|", ref)
    print("АРХИВ:", r[8][120:])
    if kn == "None":
        print("СИН:   нет источника"); continue
    kon = int(po) if po else s
    print("СИН:  ", " / ".join("%d %s" % (v, stih(kn, g, v)) for v in range(s, min(kon, s + 6) + 1)))
    print("  -1:", stih(kn, g, s - 1)[:120] if s > 1 else "", "| +1:", stih(kn, g, kon + 1)[:120])
