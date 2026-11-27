"""devizy.py — девизы кларнета из музыки автора к «Трактату» (inbox/immollimma/requests/tractatus/piece.py), но по
квенийскому тексту семи положений (перевод автора, inbox/Suite_.txt, через proekty/tlpt-qu/qu.js).

Правило автора (piece.py, строки 6–8 и motto()): ударный слог — четверть, безударный — восьмая, запятая/точка/
двоеточие — пауза в восьмую, последний слог — половинная; высота — первая буква слога, (индекс буквы) mod 7, как
ступень лада части; лад у каждой части свой (SATZ). Ударение и ядра слогов — proekty/instrumenty/kv_udar.py
(правило квенья: двусложные — на первый; иначе на предпоследний, если он тяжёлый, иначе на третий от конца).
Деление на слоги (куда отходят согласные) — простое правило здесь: одна согласная между гласными уходит в следующий
слог, из группы первая остаётся в предыдущем; qu, ny, ty, ly, ry, hy, hw, hl, hr, gw — одна согласная (*nw*, *ngw* делятся: *nan-wi-*, *en-gwa-*; первый вариант с *nw*, *ng* как одной согласной давал *na-nwi-en-na*).
Это влияет только на первую букву слога, то есть на высоту.

Мои решения (у автора их нет): 5 — без скобки (как и немецкий девиз без «(Der Elementarsatz …)»); 6 — без формулы
«(qui,ni,l(ni))», кончается двоеточием, как немецкое «ist:»; 7 — обрыв на «I ú-» (у автора немецкий — на «Wo-von»):
на отрицательной приставке.

Выход: строки SATZ в формате автора (печать) и MIDI (format 0, кларнет, 96 bpm): для каждого положения сперва
немецкий девиз автора, потом квенийский. Запуск: python3 -I proekty/tlpt-qu/devizy.py proekty/tlpt-qu/devizy.mid
2026-11-27, пробуждение 20:32."""
import ast, json, os, re, struct, sys

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, os.path.join(root, "proekty", "instrumenty"))
import kv_udar  # noqa: E402

src = open(os.path.join(root, "inbox", "immollimma", "requests", "tractatus", "piece.py"), encoding="utf-8").read()
modes = {}
for name in ("IONIAN", "LYDIAN", "DORIAN", "MIXO", "AEOLIAN", "PHRYG"):
    modes[name] = ast.literal_eval(re.search(r"^%s = (\[.*?\])" % name, src, re.M).group(1))
satz_de = {}
for m in re.finditer(r'^\s+(\d): \("(.*?)", (\w+)\)', src, re.M):
    satz_de[int(m.group(1))] = (m.group(2), m.group(3))
assert len(satz_de) == 7, satz_de

s = open(os.path.join(root, "proekty", "tlpt-qu", "qu.js"), encoding="utf-8").read()
qu = json.loads(s[s.index(",") + 1:s.rindex(")")])["texts"]
tekst = {k: qu[str(k)] for k in range(1, 8)}
tekst[5] = tekst[5].split("(")[0].strip()          # без скобки
tekst[6] = tekst[6].split("(")[0].strip().rstrip(".") + ":"   # без формулы
DIGR = ("qu", "ny", "ty", "ly", "ry", "hy", "hw", "hl", "hr", "gw")
VOW = set("aeiouáéíóúëäöy")


def razbit(word):
    """слово → список слогов (строк), по ядрам kv_udar"""
    w = kv_udar.norm(word)
    nuclei = [x[0] for x in kv_udar.syllables(w)]
    # позиции ядер в слове
    pos, i = [], 0
    for nu in nuclei:
        j = w.find(nu, i)
        pos.append((j, j + len(nu)))
        i = j + len(nu)
    if not pos:
        return [w]
    cuts = []
    for (a1, b1), (a2, b2) in zip(pos, pos[1:]):
        mid = w[b1:a2]
        units, k = [], 0
        while k < len(mid):
            if mid[k:k + 2] in DIGR:
                units.append(mid[k:k + 2]); k += 2
            else:
                units.append(mid[k]); k += 1
        keep = 0 if len(units) <= 1 else 1
        cuts.append(b1 + sum(len(u) for u in units[:keep]))
    parts, prev = [], 0
    for c in cuts:
        parts.append(w[prev:c]); prev = c
    parts.append(w[prev:])
    return parts


def satz_qu(text, obryv=None):
    out = []
    for tok in text.split():
        punct = tok[-1] if tok[-1] in ",.:" else ""
        word = tok.rstrip(",.:")
        if not re.search(r"[a-zá-úë]", word.lower()):
            continue
        sl = razbit(word)
        st, _ = kv_udar.stress(word)
        if len(sl) < 2:
            st = None                                  # односложные служебные — безударные, как «der», «ist» у автора
        out.append("-".join(("!" if k == st else "") + x for k, x in enumerate(sl)) + punct)
    line = " ".join(out)
    if obryv:
        line = obryv
    return line


SATZ_QU = {}
for k in range(1, 8):
    mode = satz_de[k][1]
    SATZ_QU[k] = (satz_qu(tekst[k], obryv="I !ú" if k == 7 else None), mode)

# --- ритм и высоты, как motto() автора
D = 62


def syllables(text):
    out = []
    for word in text.split():
        rest = word[-1] in ",.:"
        parts = word.rstrip(",.:").split("-")
        for i, x in enumerate(parts):
            out.append((x.lstrip("!"), x.startswith("!"), rest and i == len(parts) - 1))
    return out


def letter_degree(x):
    c = x[0].lower()
    c = {"ä": "a", "ö": "o", "ü": "u", "ß": "s", "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ë": "e"}.get(c, c)
    return (ord(c) - ord("a")) % 7


def motto(text, mode):
    """→ [(midi, доли, ударный)] и пауза после — как motto() у автора"""
    syl = syllables(text)
    notes = []
    for i, (x, stress, rest) in enumerate(syl):
        last = i == len(syl) - 1
        beats = 2.0 if last else (1.0 if stress else 0.5)
        notes.append((D + modes[mode][letter_degree(x)], beats, stress, 0.5 if rest and not last else 0.0, x))
    return notes


# --- MIDI format 0
def vlq(n):
    b = [n & 0x7F]
    n >>= 7
    while n:
        b.append((n & 0x7F) | 0x80); n >>= 7
    return bytes(reversed(b))


TPB = 480
ev = bytearray()
ev += vlq(0) + b"\xFF\x51\x03" + struct.pack(">I", int(60_000_000 / 96))[1:]
ev += vlq(0) + b"\xC0\x47"                          # программа 72 (с 1) — кларнет
pending = 0
for k in range(1, 8):
    for text, mode in (satz_de[k], SATZ_QU[k]):
        for m, beats, stress, rest, x in motto(text, mode):
            vel = int(127 * (0.61 if stress else 0.55))
            ev += vlq(pending) + bytes([0x90, m, vel]); pending = 0
            ev += vlq(int(beats * TPB * 0.92)) + bytes([0x80, m, 0])
            pending = int(beats * TPB * 0.08) + int(rest * TPB)
        pending += 2 * TPB                            # две доли между девизами
ev += vlq(pending) + b"\xFF\x2F\x00"
if len(sys.argv) > 1:
    with open(sys.argv[1], "wb") as f:
        f.write(b"MThd" + struct.pack(">IHHH", 6, 0, 1, TPB) + b"MTrk" + struct.pack(">I", len(ev)) + ev)

names = "CDEFGAB"
for k in range(1, 8):
    for tag, (text, mode) in (("de", satz_de[k]), ("qu", SATZ_QU[k])):
        mt = motto(text, mode)
        print("%d %s %-8s %s" % (k, tag, mode, text))
        print("           " + " ".join("%s%s%s" % (x, "!" if st else "", {0.5: "♪", 1.0: "♩", 2.0: "𝅗𝅥"}[b])
                                       for m, b, st, r, x in mt))
        print("           доль: %.1f, слогов: %d" % (sum(b + r for m, b, st, r, x in mt), len(mt)))
