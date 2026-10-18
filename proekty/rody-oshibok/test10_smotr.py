"""test10_smotr.py — показать места переписи теста 10: контекст и начало § по немецкому тексту.
Запуск: python3 -I test10_smotr.py test10-perepis.tsv ext/pu/pu.json [с] [по] [длина §]"""
import sys, json

rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[1], encoding="utf-8")][1:]
pu = json.load(open(sys.argv[2], encoding="utf-8"))
a = int(sys.argv[3]) if len(sys.argv) > 3 else 0
b = int(sys.argv[4]) if len(sys.argv) > 4 else len(rows)
dl = int(sys.argv[5]) if len(sys.argv) > 5 else 350
for r in rows[a:b]:
    print("=" * 20, r[0], "|", r[1], "| §", r[2], "знам" if r[3] == "1" else "")
    print("АРХИВ:", r[4])
    print("PU:   ", pu[r[2]][:dl])
