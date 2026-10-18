"""karta.py — карта архива inbox/: что прочитано, что упомянуто, где.

Запуск:  python3 -I proekty/karta/karta.py        (пишет karta.md и upominaniya.tsv рядом)

Два слоя, и они не смешиваются:
1. Ручной статус — status.tsv (префикс пути → статус → где разобрано). Самый длинный префикс побеждает.
   Статусы: полностью / частично / бегло / нет / служебное (код библиотек, шрифты, сборки — не для чтения).
   Это моё утверждение, и оно может врать: ставить только по дневнику или заметке, ссылку — в третьем столбце.
2. Автоматические упоминания — в каких моих файлах (diary, notes, proekty) встречается имя файла.
   Это не «прочитано»: упомянуть можно и непрочитанное (как в karta-inbox: «не прочитаны: …»).
   Ключ — имя без расширения. Если имя короткое (< 6 знаков) или в inbox оно не единственное,
   засчитываю только вместе с именем родительской папки в том же моём файле (пометка «~»).
"""
import os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
INBOX = os.path.join(ROOT, "inbox")
SLUZH = ("node_modules", ".git", "jre", "fonts", "vendor", "build", "katex", "cache", "__pycache__", ".gradle")

# --- мои тексты
mine = {}
for d in ("diary", "notes", "proekty"):
    for dp, dn, fn in os.walk(os.path.join(ROOT, d)):
        for f in fn:
            if not f.endswith((".md", ".tsv", ".txt", ".py")):
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, ROOT)
            if rel.startswith("proekty/karta/") or rel == "notes/karta-html.md" or os.path.basename(rel).startswith(("smesh", "test8-mesta", "test8-vyborka")):
                continue  # механические прогоны по всему inbox — не упоминание
            try:
                mine[rel] = open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                pass

# --- ручной статус
status = []
sp = os.path.join(HERE, "status.tsv")
if os.path.exists(sp):
    for line in open(sp, encoding="utf-8"):
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.rstrip("\n").split("\t")
        parts += [""] * (3 - len(parts))
        status.append((parts[0], parts[1], parts[2], len(status)))
# длиннее префикс — точнее; при равной длине побеждает строка ниже (дописанная позже уточняет прежнюю).
# Прежде побеждала верхняя, и «нет» у «Великанов» заслоняло дописанное «частично» (пробуждение 19:01).
status.sort(key=lambda s: (-len(s[0]), -s[3]))
status = [s[:3] for s in status]

def stat_of(rel):
    if any(part in SLUZH for part in rel.split("/")):
        return "служебное", ""
    for pref, st, where in status:
        if rel.startswith(pref.rstrip("*")):  # префикс как есть: «gnostic-treatise-part» берёт все восемь
            return st, where
    if any(part in SLUZH for part in rel.split("/")):
        return "служебное", ""
    return "?", ""

# --- файлы inbox
files = []
for dp, dn, fn in os.walk(INBOX):
    dn.sort()
    for f in sorted(fn):
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, INBOX)
        try:
            size = os.path.getsize(p)
        except OSError:
            size = 0
        files.append((rel, size))

stems = collections.Counter(os.path.splitext(os.path.basename(r))[0] for r, _ in files)

def mentions(rel):
    base = os.path.basename(rel)
    stem = os.path.splitext(base)[0]
    parent = os.path.basename(os.path.dirname(rel))
    weak = len(stem) < 6 or stems[stem] > 1
    out = []
    for name, text in mine.items():
        if base in text or rel in text:
            out.append(name)
        elif stem and stem in text:
            if not weak:
                out.append(name)
            elif parent and parent in text:
                out.append("~" + name)
    return out

# служебное не ищу — экономия
rows = []
for rel, size in files:
    st, where = stat_of(rel)
    m = [] if st == "служебное" else mentions(rel)
    if st == "?" and not m:
        st = "не упомянут"  # имя нигде у меня не встречается: скорее всего не открывал, но это вывод из поиска, не из памяти
    elif st == "?":
        st = "упомянут, статус не поставлен"  # ср. `unspecified` в ФилоСфере (readme §13-бис): не искал, а не «нет»
    rows.append((rel, size, st, where, m))

with open(os.path.join(HERE, "upominaniya.tsv"), "w", encoding="utf-8") as out:
    out.write("# файл inbox\tбайт\tстатус\tгде разобрано\tупоминаний\tмои файлы (до 8; ~ — слабое, по имени папки)\n")
    for rel, size, st, where, m in rows:
        out.write("%s\t%d\t%s\t%s\t%d\t%s\n" % (rel, size, st, where, len(m), ", ".join(m[:8])))

# --- сводка по единицам: верхний уровень, а для крупных папок — второй
def unit(rel):
    parts = rel.split("/")
    if len(parts) == 1:
        return rel
    if parts[0] in ("gpt", "Synthesises-of-concepts", "html-generated", "нян", "Доклад") and len(parts) > 2:
        return parts[0] + "/" + parts[1]
    return parts[0] + "/"

U = collections.OrderedDict()
for rel, size, st, where, m in rows:
    u = unit(rel)
    d = U.setdefault(u, {"n": 0, "size": 0, "st": collections.Counter(), "upom": 0, "where": set(), "kto": collections.Counter()})
    d["n"] += 1
    d["size"] += size
    d["st"][st] += 1
    d["upom"] += bool([x for x in m if not x.startswith("~")])
    if where:
        d["where"].add(where)
    for x in m:
        d["kto"][x.lstrip("~")] += 1

def hum(b):
    for u in ("Б", "КБ", "МБ", "ГБ"):
        if b < 1024:
            return "%.0f %s" % (b, u)
        b /= 1024
    return "%.1f ТБ" % b

tot = collections.Counter(st for _, _, st, _, _ in rows)
lines = ["# Карта архива inbox/", "",
         "Порождается `karta.py` (не править руками; править `status.tsv`). Файлов: %d. Статусы: %s." %
         (len(rows), ", ".join("%s — %d" % kv for kv in tot.most_common())), "",
         "Статус — моё утверждение по дневнику и заметкам; «упом.» — сколько файлов единицы названы по имени хоть в одном моём файле (автоматически, не значит «прочитано»). Подробно по файлам — `upominaniya.tsv`.", "",
         "| единица | файлов | объём | статус | упом. | где разобрано | чаще всего упоминается в |",
         "|---|---|---|---|---|---|---|"]
for u, d in U.items():
    st = ", ".join("%s %d" % (k, v) if len(d["st"]) > 1 else k for k, v in d["st"].most_common())
    kto = ", ".join("`%s`" % k for k, _ in d["kto"].most_common(2))
    lines.append("| `%s` | %d | %s | %s | %d | %s | %s |" % (u, d["n"], hum(d["size"]), st, d["upom"], "; ".join(sorted(d["where"])), kto))
open(os.path.join(HERE, "karta.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("файлов %d; %s" % (len(rows), dict(tot)))
