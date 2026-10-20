"""karniz.py ФАЙЛ [ЗАГОЛОВОК] — выписать «карнизы»: последнюю фразу каждого абзаца и пункта списка.

Зачем (20.10, пробуждение 21:07): из 29 ошибок вечера 12 — «закругления», фразы в конце абзаца,
которые подводят итог и потому звучат как вывод, а не как утверждение («Scheingesims», PI § 217).
Перед тем как отдавать текст проверяющему, перечитывать надо их. Инструмент их собирает.

ЗАГОЛОВОК — подстрока заголовка (## …): тогда берётся только этот раздел, до следующего заголовка
того же или высшего уровня. Без него — весь файл. Цитаты (строки с >) и таблицы пропускаются:
в них карнизы чужие или их нет.
"""
import re, sys

def razdel(lines, key):
    start = None
    for i, l in enumerate(lines):
        m = re.match(r"^(#+)\s", l)
        if start is None and m and key in l:
            start, level = i, len(m.group(1))
            continue
        if start is not None and m and len(m.group(1)) <= level:
            return lines[start:i]
    return lines[start:] if start is not None else []

def bloki(lines):
    """Абзацы и пункты списка как отдельные блоки текста."""
    cur = []
    for l in lines:
        s = l.rstrip("\n")
        if not s.strip() or s.startswith("#") or s.startswith(">") or s.startswith("|") or s.strip() == "---":
            if cur:
                yield " ".join(cur); cur = []
            continue
        if re.match(r"^\s*[-*]\s|^\s*\d+\.\s", s) and cur:
            yield " ".join(cur); cur = []
        cur.append(s.strip())
    if cur:
        yield " ".join(cur)

KONEC = re.compile(r"[.!?…][»”)\]*]?\s+(?=[А-ЯЁA-Z*«(\[])")

def frazy(t):
    """Делит на фразы: конец — . ! ? … (с закрывающими кавычками/скобками), дальше пробел и заглавная.
    Сокращения вроде «мн. ч.» не делят, потому что за ними строчная."""
    t = t.strip(); out = []; start = 0
    for m in KONEC.finditer(t):
        end = m.end()
        out.append(t[start:end].strip()); start = end
    out.append(t[start:].strip())
    return [x for x in out if x]

def poslednyaya(t):
    f = frazy(t)
    return f[-1] if f else t.strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
    if len(sys.argv) > 2:
        lines = razdel(lines, sys.argv[2])
        if not lines:
            print("— раздел с заголовком, содержащим %r, не найден" % sys.argv[2]); sys.exit(1)
    n = 0
    for b in bloki(lines):
        f = poslednyaya(b)
        if len(f) < 15:   # короткие хвосты вроде «Потеря.» печатаются вместе с предыдущей фразой
            parts = frazy(b)
            f = " ".join(parts[-2:]) if len(parts) > 1 else f
        n += 1
        print("%3d  %s" % (n, f))
    print("— карнизов: %d" % n)
