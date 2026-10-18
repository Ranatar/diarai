"""schet_ssylok.py папка — сколько в папке ссылок на классиков по их пагинации (Гегель Энц. §, Спиноза, Платон по
Стефанусу, Хайдеггер SZ §, Лунь юй) и в каких файлах. Искал корпус для теста 12 (`proekty/rody-oshibok/`).
Жил в ext/tmp, перенесён 2026-10-18 (пробуждение 19:01)."""
import os, re, sys, collections
pats = {
 "Гегель Энц §": re.compile(r"(Энциклопеди|Enzyklop|Encyclop)[^§]{0,80}§\s?\d+"),
 "Спиноза Этика": re.compile(r"(Этик[аи]|Ethic[ae]|Ethica)[^.\n]{0,40}(ч\.|част|pars|E)\s?[IVX1-5]+[^.\n]{0,20}(теорем|prop|P\s?\d|схоли|определ|def)", re.I),
 "Кант KrV A/B": re.compile(r"\b(KrV|КЧР|Критик[аи] чистого разума)[^.\n]{0,40}\b[AB]\s?\d{2,3}"),
 "Аристотель Беккер": re.compile(r"\b\d{3,4}\s?[ab]\s?\d{1,2}\b"),
 "Платон Стефанус": re.compile(r"\b(Государств|Тимей|Федон|Федр|Пир|Теэтет|Парменид|Софист|Менон|Rep\.|Tim\.)[^.\n]{0,20}\b\d{2,3}\s?[a-eа-д]\b"),
 "Хайдеггер SZ": re.compile(r"(Sein und Zeit|Бытие и время|SZ)[^.\n]{0,30}(§\s?\d+|S\.\s?\d+)"),
 "Лунь юй": re.compile(r"(Лунь ?юй|Analects)[^.\n]{0,30}\b\d{1,2}[.:]\d{1,2}"),
}
c = collections.Counter(); files = collections.defaultdict(collections.Counter)
for dp, dn, fn in os.walk(sys.argv[1]):
    for f in fn:
        if not f.endswith((".md", ".html", ".txt", ".json")): continue
        p = os.path.join(dp, f)
        try: t = open(p, encoding="utf-8").read()
        except Exception: continue
        for k, rx in pats.items():
            n = len(rx.findall(t))
            if n: c[k] += n; files[k][p] += n
for k in pats:
    print(k, c[k], files[k].most_common(4))
