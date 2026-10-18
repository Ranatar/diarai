"""mrz.py "строка" — разобрать вторую строку машиночитаемой зоны паспорта (ICAO 9303, TD3, 44 знака)
и пересчитать контрольные цифры (веса 7, 3, 1; '<' = 0, A = 10 … Z = 35).
Написан 2026-10-18 для паспорта Holzmann в KRUMME SIEG (картинка 012)."""
import sys

def val(c):
    if c.isdigit():
        return int(c)
    if c == "<":
        return 0
    return ord(c) - 55

def check(s):
    return sum(val(c) * (7, 3, 1)[i % 3] for i, c in enumerate(s)) % 10

s = sys.argv[1]
print("длина:", len(s), "(должно быть 44)")
if len(s) >= 44:
    doc, dc, nat, dob, dobc, sex, exp, expc, pers, persc, comp = (
        s[0:9], s[9], s[10:13], s[13:19], s[19], s[20], s[21:27], s[27], s[28:42], s[42], s[43])
    print("номер", doc, "контроль", dc, "расчёт", check(doc))
    print("гражданство", nat)
    print("рождение", dob, "контроль", dobc, "расчёт", check(dob))
    print("пол", sex)
    print("срок", exp, "контроль", expc, "расчёт", check(exp))
    print("личный", pers, "контроль", persc, "расчёт", check(pers))
    print("общая", comp, "расчёт", check(s[0:10] + s[13:20] + s[21:43]))
# поиск дат по шаблону ГГММДД+контроль в любой позиции
for i in range(len(s) - 6):
    d = s[i:i + 6]
    if d.isdigit() and s[i + 6].isdigit() and check(d) == int(s[i + 6]):
        print("на позиции", i, "дата", d, "с верной контрольной", s[i + 6])
