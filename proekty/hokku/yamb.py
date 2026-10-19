"""Найденный четырёхстопный ямб и онегинская строфа из собственного текста.

По мотивам inbox/Tsiolkovskiy_oneginskaya.txt. Там строки набраны из слов
Циолковского с пропусками. Здесь строка — это всегда подряд идущие слова
текста, ничего не выкинуто и не переставлено. Пропуски бывают только
между строками.

Строка годится, если:
  * в ней 8 слогов (мужское окончание) или 9 (женское);
  * у каждого многосложного слова ударение может падать на чётный слог
    (2, 4, 6, 8); односложные стоят где угодно, как и в настоящих стихах;
  * последнее ударение приходится ровно на 8-й слог;
  * все многосложные слова есть в словаре (udar.py); незнакомое слово — отказ.

Строфа: AbAbCCddEffEgg, заглавные — женские рифмы (9 слогов), строчные —
мужские (8). Строки берутся по порядку текста, жадно.

Запуск: python3 yamb.py файлы... [--lines] > out.txt
        python3 yamb.py --check стихи.md   — каждая строка своих стихов отдельно, OK/--
"""
import re
import sys

from udar import stress, nsyl, VOWELS

SCHEME = "AbAbCCddEffEgg"


def words_of(text):
    text = re.sub(r"`[^`]*`|https?://\S+", " ", text)
    text = text.replace("́", "")
    out, pending = [], ""
    for w in re.findall(r"[А-Яа-яЁё]+(?:-[А-Яа-яЁё]+)*|[.!?;:—]", text):
        if not w[0].isalpha():
            if out:
                out.append("|")  # граница фразы
            pending = ""
            continue
        if w.isupper() and len(w) > 1:  # аббревиатуры (ГБ, МБ, ИИ) — граница
            out.append("|")
            pending = ""
            continue
        if nsyl(w.lower()):
            out.append(pending + w)
            pending = ""
        elif w.lower() not in ("в", "к", "с", "б", "ж"):
            # «ч», «м», «мин» в таблицах — единицы измерения, не слова
            out.append("|")
            pending = ""
        else:
            pending += w + " "
    return out


# служебные слова, на которых строка не может кончаться
WEAK_END = set("и а но что кто же из в не ли как то бы для до по о у с к"
               " от за на со ко во об при без над под про через".split())


# составные предлоги в речи безударны («не из-за клятвы»): место в размере любое
CLITIC = {"из-за", "из-под", "по-над"}


# --stop N: N-стопный ямб (по умолчанию 4, т.е. ударение на 8-м слоге); добавлено 19.10 для сестины
LAST = 2 * int(sys.argv[sys.argv.index("--stop") + 1]) if "--stop" in sys.argv else 8


def fits(words):
    """Вернуть (строка с ударениями, рифмоключ, женская?) или None."""
    pos, marked, last = 0, [], None
    for i, w in enumerate(words):
        core = w.split()[-1].lower()  # без приклеенного предлога
        n = nsyl(core)
        if core in CLITIC and i < len(words) - 1:
            marked.append(w)
            pos += n
            continue
        ss = stress(core.replace("-", ""))
        if ss is None and "-" in core:
            # «где-то», «кто-нибудь», «как-либо»: частица безударна, ударение — у первой части
            ss = stress(core.split("-")[0])
        if ss is None:
            return None
        if n == 1:
            s = 1
            if i == len(words) - 1 and pos + 1 != LAST:
                return None
        else:
            good = [s for s in ss if (pos + s) % 2 == 0]
            if not good:
                return None
            s = good[0]
        if pos + s > LAST and i == len(words) - 1:
            return None
        # омограф: у слова есть ударение, которое в размер не ложится
        # («слОва/слова́», «глубИны/глубины́»). Помечаем «~», проверять на слух.
        marked.append(mark(w, s) + ("~" if n > 1 and len(good) < len(ss) else ""))
        last = (core, s)
        pos += n
    if pos not in (LAST, LAST + 1):
        return None
    core, s = last
    if core in WEAK_END:
        return None
    if (pos - nsyl(core) + s) != LAST:
        return None
    return " ".join(marked), rhyme_key(core, s), pos == LAST + 1


def why(words):
    """Причина отказа fits() — для --check (2026-10-19: причины я угадывал и угадал не все)."""
    pos = 0
    for i, w in enumerate(words):
        core = w.split()[-1].lower()
        n = nsyl(core)
        if core in CLITIC and i < len(words) - 1:
            pos += n
            continue
        ss = stress(core.replace("-", ""))
        if ss is None and "-" in core:
            ss = stress(core.split("-")[0])
        if ss is None:
            return "нет в словаре: «%s»" % core
        if n > 1 and not [s for s in ss if (pos + s) % 2 == 0]:
            return "«%s»: ударение %s в слове не ложится на чётный слог строки (слово с %d-го)" % (
                core, "/".join(map(str, sorted(ss))), pos + 1)
        pos += n
    if pos not in (LAST, LAST + 1):
        return "слогов %d, а нужно %d или %d" % (pos, LAST, LAST + 1)
    if words and words[-1].split()[-1].lower() in WEAK_END:
        return "конец на слабое слово «%s» (WEAK_END)" % words[-1].split()[-1].lower()
    return "последнее ударение не на %d-м слоге" % LAST


def mark(w, s):
    pre, core = (w.rsplit(" ", 1) + [""])[:2] if " " in w else ("", w)
    k, out = 0, []
    pre = pre.lower()
    for c in core.lower():
        if c in VOWELS:
            k += 1
            if k == s:
                c = c.upper()
        out.append(c)
    return (pre + " " if pre else "") + "".join(out)


V_NORM = str.maketrans("яюеёыэ", "ауэоиэ")
DEVOICE = str.maketrans("бдгвзж", "пткфсш")


def rhyme_key(word, s):
    w = word.lower().replace("ь", "").replace("ъ", "").replace("-", "")
    k = 0
    for i, c in enumerate(w):
        if c in VOWELS:
            k += 1
            if k == s:
                tail = w[i:]
                # мужская открытая рифма: нужна опорная согласная
                if len(tail) == 1 and i > 0:
                    tail = w[i - 1:]
                tail = tail.translate(V_NORM)
                return tail[:-1] + tail[-1:].translate(DEVOICE)
    return w


def lines(words):
    """Все подходящие строки, без пересечений, в порядке текста."""
    i = 0
    while i < len(words):
        found = None
        if words[i] != "|":
            for j in range(i + 1, min(i + 10, len(words)) + 1):
                if "|" in words[i:j]:
                    break
                r = fits(words[i:j])
                if r:
                    found = (j, r)
                    if r[2]:
                        break  # женская длиннее — дальше не ищем
        if found:
            j, r = found
            last = words[j - 1].split()[-1].lower()
            yield (*r, last)
            i = j
        else:
            i += 1


def stanzas(ls):
    """Жадно: идём по строкам, заполняем слоты схемы."""
    ls = list(ls)
    start = 0
    while start < len(ls):
        slots, keys, used, words_used = [], {}, start, {}
        k = start
        for letter in SCHEME:
            fem = letter.isupper()
            want = keys.get(letter)
            while k < len(ls):
                text, key, isfem, last = ls[k]
                k += 1
                if isfem != fem:
                    continue
                if want is None:
                    # новая рифма: должна найтись пара дальше
                    if not any(l[1] == key and l[2] == fem and l[3] != last
                               for l in ls[k:]):
                        continue
                    keys[letter], words_used[letter] = key, {last}
                    slots.append(text)
                    break
                if key == want and last not in words_used[letter]:
                    words_used[letter].add(last)
                    slots.append(text)
                    break
            else:
                return
        yield slots
        start = k


if __name__ == "__main__":
    files = [a for i, a in enumerate(sys.argv[1:], 1)
             if not a.startswith("--") and sys.argv[i - 1] != "--stop"]
    if "--src" in sys.argv:  # все строки всех файлов, с именем файла (для центонов)
        import os
        for p in files:
            try:
                t = open(p, encoding="utf-8").read()
            except UnicodeDecodeError:
                continue
            for s, key, fem, last in lines(words_of(t)):
                print("\t".join(("Ж" if fem else "М", key, s, os.path.basename(p))))
        sys.exit()
    if "--check" in sys.argv:  # свои стихи: каждая строка файла как есть (до первой «---»)
        for p in files:
            for l in open(p, encoding="utf-8").read().split("\n---")[0].splitlines():
                if not l.strip() or l.lstrip()[0] in "#*>":
                    continue
                ws = [w for w in words_of(l) if w != "|"]
                r = fits(ws)
                print(("OK  " + r[0] + "   [" + r[1] + "]") if r else ("--  " + l + "   ← " + why(ws)))
        sys.exit()
    if "--each" in sys.argv:  # каждый файл отдельно, с заголовком
        for p in files:
            try:
                t = open(p, encoding="utf-8").read()
            except UnicodeDecodeError:
                continue
            for st in stanzas(lines(words_of(t))):
                print("##", p)
                print("\n".join(st[:4]) + "\n" + "\n".join(st[4:8]) + "\n"
                      + "\n".join(st[8:12]) + "\n" + "\n".join(st[12:]) + "\n")
        sys.exit()
    text = "\n".join(open(p, encoding="utf-8").read() for p in files)
    ls = list(lines(words_of(text)))
    if "--lines" in sys.argv:
        for t, key, fem, last in ls:
            print(("Ж " if fem else "М ") + t + "   [" + key + "]")
    else:
        out = []
        for st in stanzas(ls):
            out.append("\n".join(st[:4]) + "\n" + "\n".join(st[4:8]) + "\n"
                       + "\n".join(st[8:12]) + "\n" + "\n".join(st[12:]))
        print("\n\n".join(out))
