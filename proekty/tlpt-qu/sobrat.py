"""sobrat.py — собирает «издание qu» для читалки «Трактата» автора (inbox/tlpt) из двух источников:
  1) перевод автора, 17 мая 2022 (inbox/Suite_.txt), — основной текст там, где он есть;
  2) мои черновики ученика (proekty/tractatus-quenya/stranica.md, сводная таблица), — основной текст там,
     где у автора положения нет, и комментарий «Третий» там, где есть оба.
Формат — как у inbox/tlpt/data/ed/*.js: TLP.put("ed/qu", {texts, pages, front, notes, comments, apparatus, figs}).
inbox не трогаю: пишу в proekty/tlpt-qu/ (qu.js и manifest-qu.json — запись для манифеста).
Запуск: python3 -I proekty/tlpt-qu/sobrat.py
2026-11-27, пробуждение 20:32."""
import json, os, re

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
out = os.path.join(root, "proekty", "tlpt-qu")

# канонический список номеров — из дерева читалки
t = open(os.path.join(root, "inbox", "tlpt", "data", "tree.js"), encoding="utf-8").read()
nums = json.loads(t[t.index(",") + 1:t.rindex(")")])["nums"]
kanon = set(nums)

# 1. автор
avtor = {}
for l in open(os.path.join(root, "inbox", "Suite_.txt"), encoding="utf-8"):
    m = re.match(r"(\d(?:\.\d)*)\.?\s+(.*)", l.strip())
    if not m:
        continue
    cif = m.group(1).replace(".", "")
    num = cif[0] + ("." + cif[1:] if len(cif) > 1 else "")
    avtor[num] = m.group(2).strip()

# 2. я: | номер [уточнение] | немецкий | квенья (пометки) | обратно |
moi, avtor_var = {}, {}
v_tablice = False
for l in open(os.path.join(root, "proekty", "tractatus-quenya", "stranica.md"), encoding="utf-8"):
    # только первая (сводная) таблица: ниже есть другие таблицы с номерами строк в первом столбце
    if l.startswith("|"):
        v_tablice = True
    elif v_tablice:
        break
    m = re.match(r"\|\s*(\d(?:\.\d+)?)\s*([^|]*)\|[^|]*\|([^|]*)\|([^|]*)\|", l)
    if not m:
        continue
    num, utochn, kv, obr = (x.strip() for x in m.groups())
    kursiv = re.findall(r"\*([^*]+)\*", kv)
    if "(автор" in kv:
        # строка автора, взятая мной как есть. Если она совпадает с Suite — пропускаю; если нет (7: доклад
        # «Философские термины на квэнья» против Suite 2022) — это второй вариант автора, его не терять.
        norm = lambda x: re.sub(r"[\W_]+", " ", x).strip().lower()
        if kursiv and norm(kursiv[0]) != norm(avtor.get(num, "")):
            avtor_var.setdefault(num, []).append(kursiv[0].strip())
        continue
    tekst = kursiv[0].strip() if kursiv else kv
    pomety = kv.replace("*" + kursiv[0] + "*", "", 1).strip() if kursiv else ""
    moi.setdefault(num, []).append({"utochn": utochn, "tekst": tekst, "pomety": pomety, "obr": obr})

texts, comments, chuzhie = {}, [], []
for num in nums:
    a, my = avtor.get(num), moi.get(num, [])
    if a:
        texts[num] = a
    elif my:
        v = my[0]
        texts[num] = ("[…] " if v["utochn"] else "") + v["tekst"]
    for x in avtor_var.get(num, []):
        comments.append({"covers": [num], "text": "Вариант автора (доклад «Философские термины на квэнья»): *" + x + "*"})
    for i, v in enumerate(my):
        if not a and i == 0:
            head = "Черновик Третьего" + (" (" + v["utochn"].strip("() ") + ")" if v["utochn"] else "") + "."
        else:
            head = "Вариант Третьего" + (" (" + v["utochn"].strip("() ") + ")" if v["utochn"] else "") + ": *" + v["tekst"] + "*"
        parts = [head]
        if v["obr"]:
            parts.append("Обратный перевод: «" + v["obr"].rstrip(".") + "».")
        if v["pomety"]:
            parts.append("Пометы: " + v["pomety"])
        comments.append({"covers": [num], "text": " ".join(parts)})
for num in list(avtor) + list(moi):
    if num not in kanon:
        chuzhie.append(num)

n_a = sum(1 for n in nums if n in avtor)
n_m = sum(1 for n in nums if n not in avtor and n in moi)
note = ("Перевод «Трактата» на квенья: основной текст — перевод автора архива (Ránatar, 17 мая 2022; %d положений); "
        "где его перевода нет, стоит черновик ученика Третьего (2026; %d положений, неполные помечены «[…]»). "
        "Варианты Третьего к положениям автора и обратные переводы — в комментарии. Разборы слов и правил: "
        "proekty/tractatus-quenya/perevod.md и stranica.md в репозитории Ranatar/diarai. "
        "Остальных %d положений на квенья пока нет.") % (n_a, n_m, len(nums) - n_a - n_m)
ed = {"texts": texts, "pages": {}, "front": {}, "notes": {}, "comments": comments, "apparatus": [], "figs": {}}
with open(os.path.join(out, "qu.js"), "w", encoding="utf-8") as f:
    f.write('TLP.put("ed/qu",' + json.dumps(ed, ensure_ascii=False) + ");\n")
man = {"id": "qu", "file": "ed/qu.js", "lang": "qya", "year": "2022–2026",
       "title": "Ea na ilqua ya ea nanwienna (квенья: Ránatar 2022, Третий 2026)", "short": "Квенья",
       "note": note, "missing": [], "cite": "Ránatar 2022 / Третий 2026, {p}", "comment_label": "Третий",
       "has_comments": True}
json.dump(man, open(os.path.join(out, "manifest-qu.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("автор: %d, только я: %d, комментариев: %d, всего положений: %d" % (n_a, n_m, len(comments), len(nums)))
if chuzhie:
    print("номера вне канона (проверить!):", chuzhie)
