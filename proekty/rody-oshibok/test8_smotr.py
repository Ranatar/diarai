"""test8_smotr.py — показать места выборки: контекст из inbox и текст номера у Огдена (+ немецкий начала).
Запуск: python3 -I test8_smotr.py test8-mesta.tsv test8-vyborka.tsv ext/tractatus/tlp.json [с] [по]"""
import sys, json

mesta = [l.rstrip("\n").split("\t") for l in open(sys.argv[1], encoding="utf-8")][1:]
vyb = [l.rstrip("\n").split("\t") for l in open(sys.argv[2], encoding="utf-8")][1:]
tlp = json.load(open(sys.argv[3], encoding="utf-8"))
a = int(sys.argv[4]) if len(sys.argv) > 4 else 0
b = int(sys.argv[5]) if len(sys.argv) > 5 else len(vyb)
for k, v in enumerate(vyb[a:b], a):
    i = int(v[0]); f, n, z, ctx = mesta[i]
    print("=" * 30, k, "| id", i, "|", f, "|", n, "знам" if z == "1" else "")
    print("АРХИВ:", ctx)
    print("ОГДЕН:", tlp[n]["E"][:400])
    print("DE:   ", tlp[n]["G"][:160])
